"""Live component search helpers."""

from __future__ import annotations

import json
import os
import re
import time
import urllib.parse
import urllib.request
from collections import deque
from dataclasses import dataclass, replace
from html import unescape
from html.parser import HTMLParser
from typing import Any, Protocol, cast

DEFAULT_USER_AGENT = "kicad-mcp-pro/2.0 (+https://github.com/oaslananka/kicad-mcp-pro)"


@dataclass(frozen=True)
class ComponentRecord:
    """Normalized part record returned by live search providers."""

    source: str
    lcsc_code: str
    mpn: str
    package: str
    description: str
    stock: int
    price: float | None
    is_basic: bool
    is_preferred: bool


class ComponentSearchClient(Protocol):
    """Protocol shared by live part search providers."""

    def search(
        self,
        keyword: str,
        *,
        package: str | None = None,
        only_basic: bool = True,
        limit: int = 20,
    ) -> list[ComponentRecord]:
        raise NotImplementedError

    def get_part(self, lcsc_code_or_mpn: str) -> ComponentRecord | None:
        raise NotImplementedError


class RateLimiter:
    """Simple synchronous sliding-window limiter for external component APIs."""

    def __init__(self, max_calls: int, period_seconds: float) -> None:
        self.max_calls = max_calls
        self.period_seconds = period_seconds
        self.calls: deque[float] = deque()

    def acquire(self) -> None:
        now = time.monotonic()
        while self.calls and now - self.calls[0] > self.period_seconds:
            self.calls.popleft()
        if len(self.calls) >= self.max_calls:
            wait_seconds = self.period_seconds - (now - self.calls[0])
            if wait_seconds > 0:
                time.sleep(wait_seconds)
            now = time.monotonic()
            while self.calls and now - self.calls[0] > self.period_seconds:
                self.calls.popleft()
        self.calls.append(time.monotonic())


_jlcsearch_limiter = RateLimiter(max_calls=5, period_seconds=1.0)


def normalize_lcsc_code(value: str | int) -> str:
    """Normalize a user-supplied LCSC identifier."""
    raw = str(value).strip().upper()
    if raw.startswith("C"):
        suffix = raw[1:]
    else:
        suffix = raw
    return f"C{suffix}" if suffix.isdigit() else raw


def _request_json(url: str, params: dict[str, object]) -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {key: value for key, value in params.items() if value not in (None, "")}
    )
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only https component-search endpoints are permitted.")
    request = urllib.request.Request(  # noqa: S310 - scheme is validated above
        f"{url}?{query}",
        headers={"User-Agent": DEFAULT_USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=20) as response:  # noqa: S310  # nosec B310
        return cast(dict[str, Any], json.load(response))


def _record_from_jlcsearch(item: dict[str, Any]) -> ComponentRecord:
    raw_lcsc = item.get("lcsc", "")
    return ComponentRecord(
        source="jlcsearch",
        lcsc_code=normalize_lcsc_code(raw_lcsc),
        mpn=str(item.get("mfr", "")),
        package=str(item.get("package", "")),
        description=str(item.get("description", "")),
        stock=int(item.get("stock", 0) or 0),
        price=_first_price(item),
        is_basic=bool(item.get("is_basic", False)),
        is_preferred=bool(item.get("is_preferred", False)),
    )


def _first_price(item: dict[str, Any]) -> float | None:
    for key in ("price", "price1"):
        if item.get(key) is not None:
            return float(item[key])
    return None


_VALUE_PATTERN = re.compile(r"^\s*([0-9]*\.?[0-9]+)\s*([pnuµmkMGR]?)\s*(F|H|ohm|Ω|R)?\s*$")
_VALUE_SCALE = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3, "": 1.0, "R": 1.0,
                "k": 1e3, "M": 1e6, "G": 1e9}  # fmt: skip


def parse_passive_value(text: str) -> float:
    """Turn ``"100nF"``, ``"4.7u"``, ``"715k"``, ``"30.1k"`` or ``"10R"`` into base units."""
    match = _VALUE_PATTERN.match(text)
    if match is None:
        raise ValueError(
            f"Could not read the value {text!r}. Use forms like 100nF, 4.7uF, 715k, 30.1k, 10R."
        )
    return float(match.group(1)) * _VALUE_SCALE[match.group(2)]


class JLCSearchClient:
    """Zero-auth live search against jlcsearch.tscircuit.com."""

    BASE = "https://jlcsearch.tscircuit.com"
    JLCPCB_BASE = "https://jlcpcb.com"

    def search(
        self,
        keyword: str,
        *,
        package: str | None = None,
        only_basic: bool = True,
        limit: int = 20,
    ) -> list[ComponentRecord]:
        _jlcsearch_limiter.acquire()
        payload = _request_json(
            f"{self.BASE}/api/search",
            {
                "q": keyword,
                "package": package,
                "limit": str(limit),
                "is_basic": "true" if only_basic else None,
            },
        )
        records = [_record_from_jlcsearch(item) for item in payload.get("components", [])]
        if records:
            return records
        fallback = self._search_jlcpcb_public(keyword, limit=limit)
        if only_basic:
            fallback = [item for item in fallback if item.is_basic]
        if package:
            package_folded = package.casefold()
            fallback = [
                item
                for item in fallback
                if package_folded in item.package.casefold()
                or package_folded in item.description.casefold()
            ]
        return fallback[:limit]

    def search_passives(
        self,
        kind: str,
        value: str,
        *,
        package: str = "",
        min_voltage: float = 0.0,
        max_tolerance_percent: float = 0.0,
        dielectric: str = "",
        limit: int = 10,
    ) -> list[tuple[ComponentRecord, dict[str, Any]]]:
        """Find resistors or capacitors by value from the service's per-category lists.

        The keyword search rarely finds ceramic capacitors or exact resistor values;
        these lists are indexed by value and package. Returns each record with the
        raw row (voltage, tolerance, dielectric), basic parts and high stock first.
        """
        wanted = parse_passive_value(value)
        if kind == "capacitor":
            path, rows_key, value_key = "capacitors", "capacitors", "capacitance_farads"
            # The service matches a number in farads; unit text such as "2.2uF" finds nothing.
            params: dict[str, object] = {"capacitance": repr(wanted)}
        elif kind == "resistor":
            path, rows_key, value_key = "resistors", "resistors", "resistance"
            params = {"resistance": f"{wanted:g}"}
        else:
            raise ValueError("kind must be 'capacitor' or 'resistor'.")
        params["package"] = package or None
        _jlcsearch_limiter.acquire()
        rows = _request_json(f"{self.BASE}/{path}/list.json", params).get(rows_key, [])

        matches: list[tuple[ComponentRecord, dict[str, Any]]] = []
        for row in rows:
            actual = float(row.get(value_key) or 0)
            if abs(actual - wanted) > 0.02 * wanted:
                continue
            if min_voltage and float(row.get("voltage_rating") or 0) < min_voltage:
                continue
            tolerance = float(row.get("tolerance_fraction") or 0) * 100
            if max_tolerance_percent and (tolerance == 0 or tolerance > max_tolerance_percent):
                continue
            if (
                dielectric
                and dielectric.casefold()
                not in str(
                    row.get("temperature_coefficient") or row.get("description") or ""
                ).casefold()
            ):
                continue
            matches.append((_record_from_jlcsearch(row), row))
        matches.sort(key=lambda pair: (not pair[0].is_basic, -pair[0].stock))
        return matches[:limit]

    def get_part(self, lcsc_code_or_mpn: str) -> ComponentRecord | None:
        query = normalize_lcsc_code(lcsc_code_or_mpn)
        results = self.search(query, only_basic=False, limit=10)
        lcsc_matches = [item for item in results if item.lcsc_code == query]
        if lcsc_matches:
            match = lcsc_matches[0]
            if match.stock == 0:
                # The search service often has no stock figure for a part looked up by
                # code; JLCPCB's own part page does.
                public = self._get_jlcpcb_public_part(query)
                if public is not None and public.stock:
                    match = replace(match, stock=public.stock)
            return match

        raw_query = lcsc_code_or_mpn.strip()
        for item in results:
            if item.mpn.casefold() == raw_query.casefold():
                return item
        if query.startswith("C") and query[1:].isdigit():
            return self._get_jlcpcb_public_part(query)
        public_matches = self._search_jlcpcb_public(raw_query, limit=10)
        for item in public_matches:
            if item.mpn.casefold() == raw_query.casefold():
                return item
        return None

    def _request_text(self, url: str, params: dict[str, object] | None = None) -> str:
        query = urllib.parse.urlencode(
            {key: value for key, value in (params or {}).items() if value not in (None, "")}
        )
        target = f"{url}?{query}" if query else url
        parsed = urllib.parse.urlparse(target)
        if parsed.scheme != "https" or parsed.netloc not in {"jlcpcb.com", "www.jlcpcb.com"}:
            raise ValueError("Only https JLCPCB public endpoints are permitted.")
        request = urllib.request.Request(  # noqa: S310 - endpoint allow-list is enforced above
            target,
            headers={"User-Agent": DEFAULT_USER_AGENT},
        )
        with urllib.request.urlopen(request, timeout=20) as response:  # noqa: S310  # nosec B310
            return cast(bytes, response.read()).decode("utf-8", errors="replace")

    def _search_jlcpcb_public(self, keyword: str, *, limit: int) -> list[ComponentRecord]:
        if not keyword.strip():
            return []
        try:
            html = self._request_text(
                f"{self.JLCPCB_BASE}/parts/componentSearch",
                {"isSearch": "true", "searchTxt": keyword.strip()},
            )
        except (OSError, ValueError):
            return []
        codes = []
        for match in re.finditer(r'componentCode:"(C\d+)"', html):
            code = match.group(1)
            if code not in codes:
                codes.append(code)
            if len(codes) >= limit:
                break
        return [
            record for code in codes if (record := self._get_jlcpcb_public_part(code)) is not None
        ][:limit]

    def _get_jlcpcb_public_part(self, lcsc_code: str) -> ComponentRecord | None:
        try:
            html = self._request_text(f"{self.JLCPCB_BASE}/partdetail/-/{lcsc_code}")
        except (OSError, ValueError):
            return None
        return _record_from_jlcpcb_detail_page(html, lcsc_code)


def _plain_text_lines(html: str) -> list[str]:
    parser = _VisibleTextParser()
    parser.feed(html)
    parser.close()
    return parser.lines


class _VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._ignored_depth = 0
        self._chunks: list[str] = []

    @property
    def lines(self) -> list[str]:
        return [line.strip() for line in "\n".join(self._chunks).splitlines() if line.strip()]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        _ = attrs
        if tag.lower() in {"script", "style"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._ignored_depth == 0:
            self._chunks.append(data)


def _line_after_label(lines: list[str], label: str) -> str:
    for index, line in enumerate(lines):
        if line == label and index + 1 < len(lines):
            return lines[index + 1]
    return ""


def _record_from_jlcpcb_detail_page(html: str, lcsc_code: str) -> ComponentRecord | None:
    if lcsc_code not in html:
        return None
    lines = _plain_text_lines(html)
    title_match = re.search(r"<title>([^|<]+)", html, re.IGNORECASE)
    mpn = _line_after_label(lines, "MFR.Part #") or (
        unescape(title_match.group(1)).strip() if title_match else ""
    )
    package = _line_after_label(lines, "Package")
    description = _line_after_label(lines, "Description")
    library_type = " ".join(lines[:80]).casefold()
    stock_match = re.search(r"In Stock:\s*([\d,]+)", "\n".join(lines), re.IGNORECASE)
    price_match = re.search(r"1\+\s*\$([0-9.]+)", "\n".join(lines))
    return ComponentRecord(
        source="jlcpcb-public",
        lcsc_code=normalize_lcsc_code(lcsc_code),
        mpn=mpn,
        package=package,
        description=description,
        stock=int(stock_match.group(1).replace(",", "")) if stock_match else 0,
        price=float(price_match.group(1)) if price_match else None,
        is_basic="basic" in library_type and "extended" not in library_type,
        is_preferred=False,
    )


class NexarClient:
    """Optional Nexar GraphQL client."""

    ENDPOINT = "https://api.nexar.com/graphql"
    TOKEN_URL = "https://identity.nexar.com/connect/token"  # noqa: S105

    def __init__(self) -> None:
        self._client_id = os.getenv("NEXAR_CLIENT_ID")
        self._client_secret = os.getenv("NEXAR_CLIENT_SECRET")

    def search(
        self,
        keyword: str,
        *,
        package: str | None = None,
        only_basic: bool = True,
        limit: int = 20,
    ) -> list[ComponentRecord]:
        _ = (package, only_basic, limit)
        if not self._client_id or not self._client_secret:
            raise RuntimeError("Nexar search requires NEXAR_CLIENT_ID and NEXAR_CLIENT_SECRET.")
        raise RuntimeError(
            "Nexar live search is reserved for authenticated deployments. "
            f"Use the zero-auth 'jlcsearch' source for local usage. Query was: {keyword}"
        )

    def get_part(self, lcsc_code_or_mpn: str) -> ComponentRecord | None:
        _ = lcsc_code_or_mpn
        raise RuntimeError("Nexar component detail lookups require authenticated deployment.")


class DigiKeyClient:
    """Optional DigiKey client placeholder."""

    def __init__(self) -> None:
        self._client_id = os.getenv("DIGIKEY_CLIENT_ID")
        self._client_secret = os.getenv("DIGIKEY_CLIENT_SECRET")

    def search(
        self,
        keyword: str,
        *,
        package: str | None = None,
        only_basic: bool = True,
        limit: int = 20,
    ) -> list[ComponentRecord]:
        _ = (package, only_basic, limit)
        if not self._client_id or not self._client_secret:
            raise RuntimeError(
                "DigiKey search requires DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET."
            )
        raise RuntimeError(
            "DigiKey live search wiring is not enabled in the default zero-auth profile. "
            f"Query was: {keyword}"
        )

    def get_part(self, lcsc_code_or_mpn: str) -> ComponentRecord | None:
        _ = lcsc_code_or_mpn
        raise RuntimeError("DigiKey component detail lookups require authenticated deployment.")
