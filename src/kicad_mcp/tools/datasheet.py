"""Datasheet intake: store part datasheets in the project and read them.

Datasheets live in ``<project>/docs/datasheets/<part>/``. The tools return page
text for searching and page images for everything a text dump loses: pin
tables, example circuits and recommended-layout figures. Figures a design
relies on can be saved next to the datasheet in ``figures/`` so later sessions
reuse them.
"""

from __future__ import annotations

import io
import re
import shutil
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING, Any

from mcp.server.fastmcp import FastMCP, Image

from ..config import get_config
from .metadata import headless_compatible, requires_dependency

if TYPE_CHECKING:
    from collections.abc import Iterator

_DATASHEET_DIR = Path("docs") / "datasheets"
_FIGURES_DIRNAME = "figures"
_MAX_DOWNLOAD_BYTES = 60 * 1024 * 1024
_MAX_READ_PAGES = 12
_MAX_IMAGE_PIXELS = 2000
_PART_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
_FIGURE_PATTERN = re.compile(r"^\s*(Figure|Fig\.)\s+([0-9]+(?:[-.][0-9]+)*)[.:]?\s+([A-Z0-9].*)$")
_MISSING_DEPENDENCY = (
    "Datasheet reading needs the optional 'datasheets' dependencies. "
    "Install them with: pip install 'kicad-mcp-pro[datasheets]'"
)


def _datasheet_root() -> Path:
    cfg = get_config()
    if cfg.project_dir is None:
        raise ValueError("No active project is configured. Call kicad_set_project() first.")
    return cfg.project_dir / _DATASHEET_DIR


def _part_dir(part: str) -> Path:
    if not _PART_PATTERN.match(part):
        raise ValueError(
            f"Invalid part name {part!r}. Use letters, digits and . _ + - (for example 'LMR36503')."
        )
    return _datasheet_root() / part


def _pdf_for(part: str, filename: str = "") -> Path:
    directory = _part_dir(part)
    pdfs = sorted(directory.glob("*.pdf")) if directory.is_dir() else []
    if not pdfs:
        raise ValueError(
            f"No datasheet stored for {part!r}. Add one with ds_add(), or see ds_list()."
        )
    if filename:
        for pdf in pdfs:
            if pdf.name == filename:
                return pdf
        names = ", ".join(pdf.name for pdf in pdfs)
        raise ValueError(f"{part!r} has no datasheet named {filename!r}. Available: {names}")
    return pdfs[0]


def _pdfium() -> Any:  # noqa: ANN401
    try:
        import pypdfium2  # type: ignore[import-untyped]
    except ImportError as exc:
        raise RuntimeError(_MISSING_DEPENDENCY) from exc
    return pypdfium2


def _open(pdf: Path) -> Any:  # noqa: ANN401
    return _pdfium().PdfDocument(str(pdf))


def _page_text(document: Any, index: int) -> str:  # noqa: ANN401
    page = document[index]
    textpage = page.get_textpage()
    try:
        return str(textpage.get_text_range())
    finally:
        textpage.close()
        page.close()


def _parse_pages(spec: str, page_count: int) -> list[int]:
    """Parse ``"3"``, ``"3-5"`` or ``"3,7-9"`` into 0-based page indexes."""
    indexes: list[int] = []
    for chunk in spec.replace(" ", "").split(","):
        if not chunk:
            continue
        first, _, last = chunk.partition("-")
        try:
            start, end = int(first), int(last or first)
        except ValueError as exc:
            raise ValueError(f"Invalid page range {chunk!r}. Use forms like '3' or '3-5'.") from exc
        if start < 1 or end < start or end > page_count:
            raise ValueError(f"Page range {chunk!r} is outside 1-{page_count}.")
        indexes.extend(range(start - 1, end))
    if not indexes:
        raise ValueError("No pages requested.")
    return indexes


def _parse_crop(crop: str) -> tuple[float, float, float, float] | None:
    """Parse ``"left,top,right,bottom"`` fractions of the page (0-1)."""
    if not crop.strip():
        return None
    try:
        left, top, right, bottom = (float(part) for part in crop.split(","))
    except ValueError as exc:
        raise ValueError(
            "crop must be 'left,top,right,bottom' as fractions of the page, "
            "for example '0.25,0.3,0.8,0.6'."
        ) from exc
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise ValueError(
            "crop fractions must satisfy 0 <= left < right <= 1 and 0 <= top < bottom <= 1."
        )
    return left, top, right, bottom


def _render_png(pdf: Path, page_number: int, dpi: int, crop: str) -> bytes:
    box = _parse_crop(crop)
    document = _open(pdf)
    try:
        index = _parse_pages(str(page_number), len(document))[0]
        page = document[index]
        try:
            image = page.render(scale=dpi / 72).to_pil()
        finally:
            page.close()
    finally:
        document.close()
    if box is not None:
        width, height = image.size
        image = image.crop(
            (int(box[0] * width), int(box[1] * height), int(box[2] * width), int(box[3] * height))
        )
    if max(image.size) > _MAX_IMAGE_PIXELS:
        image.thumbnail((_MAX_IMAGE_PIXELS, _MAX_IMAGE_PIXELS))
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def _iter_figures(document: Any) -> Iterator[tuple[int, str, str]]:  # noqa: ANN401
    for index in range(len(document)):
        for line in _page_text(document, index).splitlines():
            match = _FIGURE_PATTERN.match(line)
            if match:
                yield index + 1, match.group(2), match.group(3).strip()


def _download(url: str, target: Path) -> None:
    if not url.lower().startswith("https://"):
        raise ValueError("Only https:// datasheet URLs are accepted.")
    request = urllib.request.Request(url, headers={"User-Agent": "kicad-mcp-pro datasheet fetch"})  # noqa: S310
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310  # nosec B310
        data = response.read(_MAX_DOWNLOAD_BYTES + 1)
    if len(data) > _MAX_DOWNLOAD_BYTES:
        raise ValueError("The download is larger than 60 MB; refusing to store it.")
    if not data.startswith(b"%PDF"):
        raise ValueError(
            "The server did not return a PDF (some manufacturer sites refuse automated "
            "downloads). Download it in a browser and pass the local file path instead."
        )
    target.write_bytes(data)


def register(mcp: FastMCP) -> None:
    """Register datasheet tools."""

    @mcp.tool()
    @headless_compatible
    def ds_list() -> str:
        """List the datasheets stored in the project, by part, with saved figures."""
        root = _datasheet_root()
        parts = sorted(path for path in root.iterdir() if path.is_dir()) if root.is_dir() else []
        lines: list[str] = []
        for directory in parts:
            pdfs = sorted(directory.glob("*.pdf"))
            if not pdfs:
                continue
            figures = sorted((directory / _FIGURES_DIRNAME).glob("*.png"))
            lines.append(f"- {directory.name}: {', '.join(pdf.name for pdf in pdfs)}")
            if figures:
                lines.append(f"  figures: {', '.join(figure.name for figure in figures)}")
        if not lines:
            return f"No datasheets stored yet. Add one with ds_add(). Folder: {root}"
        return f"Datasheets in {root} ({len(lines)} line(s)):\n" + "\n".join(lines)

    @mcp.tool()
    @headless_compatible
    def ds_add(part: str, source: str) -> str:
        """Store a datasheet PDF for a part.

        Args:
            part: Short part name used as the folder name, for example "LMR36503".
            source: An https:// URL to the PDF, or the path of a PDF already on disk.
        """
        directory = _part_dir(part)
        directory.mkdir(parents=True, exist_ok=True)
        if source.lower().startswith(("http://", "https://")):
            name = Path(source.split("?", 1)[0]).name or f"{part}.pdf"
            if not name.lower().endswith(".pdf"):
                name = f"{name}.pdf"
            target = directory / name
            _download(source, target)
        else:
            local = Path(source).expanduser()
            if not local.is_file():
                raise ValueError(f"No file at {local}.")
            with local.open("rb") as handle:
                if handle.read(4) != b"%PDF":
                    raise ValueError(f"{local} is not a PDF.")
            target = directory / local.name
            shutil.copy2(local, target)
        return (
            f"Stored {target.name} for {part} ({target.stat().st_size // 1024} KB) in {directory}."
        )

    @mcp.tool()
    @headless_compatible
    @requires_dependency("datasheets")
    def ds_search(part: str, query: str, max_hits: int = 30, filename: str = "") -> str:
        """Find where a datasheet mentions something; returns page numbers and matching lines.

        Args:
            part: Part name as stored by ds_add().
            query: Case-insensitive text or regular expression, e.g. "absolute maximum".
            max_hits: Stop after this many matching lines.
            filename: Which PDF, when the part has more than one.
        """
        try:
            pattern = re.compile(query, re.IGNORECASE)
        except re.error:
            pattern = re.compile(re.escape(query), re.IGNORECASE)
        document = _open(_pdf_for(part, filename))
        hits: list[str] = []
        try:
            page_count = len(document)
            for index in range(page_count):
                for line in _page_text(document, index).splitlines():
                    if pattern.search(line):
                        hits.append(f"p{index + 1}: {' '.join(line.split())[:200]}")
                        if len(hits) >= max_hits:
                            break
                if len(hits) >= max_hits:
                    break
        finally:
            document.close()
        if not hits:
            return f"No match for {query!r} in the {part} datasheet ({page_count} pages)."
        return f"{len(hits)} match(es) for {query!r} in {part} ({page_count} pages):\n" + "\n".join(
            hits
        )

    @mcp.tool()
    @headless_compatible
    @requires_dependency("datasheets")
    def ds_read(part: str, pages: str, filename: str = "") -> str:
        """Return the text of datasheet pages.

        Tables lose their columns in text; use ds_page_image() for those.

        Args:
            part: Part name as stored by ds_add().
            pages: Pages to read, for example "5", "5-7" or "5,12-13" (at most 12 pages).
            filename: Which PDF, when the part has more than one.
        """
        document = _open(_pdf_for(part, filename))
        try:
            indexes = _parse_pages(pages, len(document))
            if len(indexes) > _MAX_READ_PAGES:
                raise ValueError(f"Read at most {_MAX_READ_PAGES} pages per call.")
            sections = [
                f"--- {part} page {index + 1} ---\n{_page_text(document, index).strip()}"
                for index in indexes
            ]
        finally:
            document.close()
        return "\n\n".join(sections)

    @mcp.tool()
    @headless_compatible
    @requires_dependency("datasheets")
    def ds_figures(part: str, keyword: str = "", filename: str = "") -> str:
        """List the figure captions in a datasheet with their page numbers.

        Args:
            part: Part name as stored by ds_add().
            keyword: Only list captions containing this text, e.g. "layout".
            filename: Which PDF, when the part has more than one.
        """
        document = _open(_pdf_for(part, filename))
        try:
            needle = keyword.casefold()
            rows = [
                f"p{page}: Figure {number}. {caption[:160]}"
                for page, number, caption in _iter_figures(document)
                if needle in caption.casefold()
            ]
        finally:
            document.close()
        if not rows:
            suffix = f" matching {keyword!r}" if keyword else ""
            return f"No figure captions{suffix} found in the {part} datasheet."
        return f"{len(rows)} figure caption(s) in {part}:\n" + "\n".join(rows)

    @mcp.tool()
    @headless_compatible
    @requires_dependency("datasheets")
    def ds_page_image(
        part: str,
        page: int,
        dpi: int = 110,
        crop: str = "",
        save_as: str = "",
        filename: str = "",
    ) -> Image:
        """Return a datasheet page, or a region of it, as an image to look at.

        Use this for pin tables, example circuits and recommended-layout figures.

        Args:
            part: Part name as stored by ds_add().
            page: Page number, starting at 1.
            dpi: Render resolution, 50-300. Raise it together with crop to read small print.
            crop: Optional region as "left,top,right,bottom" fractions of the page, e.g.
                "0.25,0.3,0.8,0.6".
            save_as: Optional name; also saves the image as figures/<name>.png beside the datasheet.
            filename: Which PDF, when the part has more than one.
        """
        if not 50 <= dpi <= 300:
            raise ValueError("dpi must be between 50 and 300.")
        pdf = _pdf_for(part, filename)
        data = _render_png(pdf, page, dpi, crop)
        if save_as:
            if not _PART_PATTERN.match(save_as):
                raise ValueError("save_as must use letters, digits and . _ + - only.")
            figures = pdf.parent / _FIGURES_DIRNAME
            figures.mkdir(exist_ok=True)
            (figures / f"{save_as}.png").write_bytes(data)
        return Image(data=data, format="png")
