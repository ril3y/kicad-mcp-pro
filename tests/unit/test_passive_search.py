"""Value-based resistor and capacitor search against the JLC parts lists."""

from __future__ import annotations

from typing import Any

import pytest

from kicad_mcp.server import build_server
from kicad_mcp.utils import component_search
from kicad_mcp.utils.component_search import JLCSearchClient, parse_passive_value
from tests.conftest import call_tool_text


@pytest.mark.parametrize(
    ("text", "expected"),
    [("100nF", 1e-7), ("2.2uF", 2.2e-6), ("715k", 715e3), ("30.1k", 30.1e3), ("10R", 10.0),
     ("0R", 0.0), ("4.7u", 4.7e-6), ("1M", 1e6)],
)  # fmt: skip
def test_parse_passive_value(text: str, expected: float) -> None:
    assert parse_passive_value(text) == pytest.approx(expected)


def test_parse_passive_value_rejects_nonsense() -> None:
    with pytest.raises(ValueError, match="Could not read the value"):
        parse_passive_value("lots")


def _rows() -> dict[str, Any]:
    return {
        "capacitors": [
            {"lcsc": 1, "mfr": "LOWV", "capacitance_farads": 2.2e-6, "voltage_rating": 16,
             "temperature_coefficient": "X5R", "stock": 900, "price1": 0.01},
            {"lcsc": 2, "mfr": "GOOD", "capacitance_farads": 2.2e-6, "voltage_rating": 100,
             "temperature_coefficient": "X7R", "stock": 50, "price1": 0.13},
            {"lcsc": 3, "mfr": "BASIC", "capacitance_farads": 2.2e-6, "voltage_rating": 100,
             "temperature_coefficient": "X7R", "stock": None, "is_basic": True, "price1": 0.2},
            {"lcsc": 4, "mfr": "OTHERVALUE", "capacitance_farads": 2.2e-9, "voltage_rating": 100,
             "temperature_coefficient": "X7R", "stock": 5000, "price1": 0.01},
        ]
    }  # fmt: skip


def test_search_passives_filters_and_puts_basic_parts_first(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: dict[str, Any] = {}

    def fake_request(url: str, params: dict[str, object]) -> dict[str, Any]:
        seen["url"], seen["params"] = url, params
        return _rows()

    monkeypatch.setattr(component_search, "_request_json", fake_request)

    matches = JLCSearchClient().search_passives(
        "capacitor", "2.2uF", package="1206", min_voltage=100, dielectric="X7R"
    )

    assert [record.mpn for record, _row in matches] == ["BASIC", "GOOD"]
    assert matches[1][0].price == pytest.approx(0.13)
    assert seen["url"].endswith("/capacitors/list.json")
    assert float(str(seen["params"]["capacitance"])) == pytest.approx(2.2e-6)


@pytest.mark.anyio
async def test_lib_search_passives_tool_reports_parts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(component_search, "_request_json", lambda url, params: _rows())
    server = build_server("full")

    found = await call_tool_text(
        server,
        "lib_search_passives",
        {"kind": "capacitor", "value": "2.2uF", "package": "1206", "min_voltage": 100},
    )
    bad = await call_tool_text(server, "lib_search_passives", {"kind": "diode", "value": "1k"})

    assert "C2 | GOOD" in found
    assert "stock not reported | basic" in found
    assert "kind must be" in bad


@pytest.mark.anyio
async def test_lib_import_lcsc_part_rejects_bad_part_numbers(sample_project: object) -> None:
    server = build_server("full")
    result = await call_tool_text(
        server, "lib_import_lcsc_part", {"lcsc_id": "12; rm -rf", "library": "Parts"}
    )
    assert "is not an LCSC part number" in result
