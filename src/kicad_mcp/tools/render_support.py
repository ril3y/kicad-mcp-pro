"""Pictures of schematic sheets and board regions, rendered from the saved files.

Shared by the image tools and the review page. Both go through ``kicad-cli`` to a
PDF and rasterise it with pypdfium2 (the optional ``datasheets`` dependencies).
"""

from __future__ import annotations

import io
from pathlib import Path

from . import datasheet as _datasheet
from . import export_support

MAX_PIXELS = 2000
_MM_PER_POINT = 25.4 / 72


def _render(pdf: Path, page_index: int, dpi: int, box: tuple[float, float, float, float]) -> bytes:
    """Render ``box`` (left, top, right, bottom as page fractions) of one PDF page.

    Only the box is rasterised, so a small region can be drawn at a high resolution
    without building the whole page first. The resolution is lowered when needed to
    keep the longer side within ``MAX_PIXELS``.
    """
    document = _datasheet._open(pdf)
    try:
        page = document[page_index]
        try:
            width_pt, height_pt = page.get_size()
            left, top, right, bottom = box
            box_w_pt = (right - left) * width_pt
            box_h_pt = (bottom - top) * height_pt
            scale = dpi / 72
            longest = max(box_w_pt, box_h_pt) * scale
            if longest > MAX_PIXELS:
                scale *= MAX_PIXELS / longest
            crop = (
                left * width_pt,
                (1 - bottom) * height_pt,
                (1 - right) * width_pt,
                top * height_pt,
            )
            image = page.render(scale=scale, crop=crop).to_pil()
        finally:
            page.close()
    finally:
        document.close()
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def render_sheet_png(sheet: str = "", dpi: int = 150, crop: str = "") -> bytes:
    """PNG of one schematic sheet (root when ``sheet`` is empty), optionally cropped."""
    if not 50 <= dpi <= 600:
        raise ValueError("dpi must be between 50 and 600.")
    sch_file = export_support._get_sch_file()
    pdf_path = export_support._ensure_output_dir() / "schematic.pdf"
    code, stdout, stderr = export_support._run_cli_variants(
        [["sch", "export", "pdf", "--output", str(pdf_path), str(sch_file)]]
    )
    if code != 0:
        raise ValueError(f"Schematic PDF export failed: {stderr or stdout or 'unknown error'}")

    page_number = 1
    wanted = sheet.strip().strip("/")
    if wanted:
        document = _datasheet._open(pdf_path)
        try:
            marker = f"/{wanted}/".casefold()
            matches = [
                index + 1
                for index in range(len(document))
                if marker in _datasheet._page_text(document, index).casefold()
            ]
        finally:
            document.close()
        if not matches:
            raise ValueError(
                f"No page for sheet {sheet!r} in the exported schematic. "
                "Check the name with sch_list_sheets()."
            )
        page_number = matches[0]
    box = _datasheet._parse_crop(crop) or (0.0, 0.0, 1.0, 1.0)
    return _render(pdf_path, page_number - 1, dpi, box)


def render_board_png(
    layers: str = "F.Cu,F.SilkS,F.Fab,F.CrtYd,Edge.Cuts",
    region: str = "",
    dpi: int = 200,
) -> bytes:
    """PNG of the board, or of ``region`` ("x1,y1,x2,y2" in board millimetres)."""
    if not 50 <= dpi <= 2400:
        raise ValueError("dpi must be between 50 and 2400.")
    pcb_file = export_support._get_pcb_file()
    pdf_path = export_support._ensure_output_dir() / "board.pdf"
    code, stdout, stderr = export_support._run_cli_variants(
        [
            ["pcb", "export", "pdf", "--mode-single", "--layers", layers,
             "--output", str(pdf_path), str(pcb_file)],
        ]
    )  # fmt: skip
    if code != 0:
        raise ValueError(f"Board PDF export failed: {stderr or stdout or 'unknown error'}")

    box = (0.0, 0.0, 1.0, 1.0)
    if region.strip():
        try:
            x1, y1, x2, y2 = (float(part) for part in region.split(","))
        except ValueError as exc:
            raise ValueError("region must be 'x1,y1,x2,y2' in millimetres.") from exc
        document = _datasheet._open(pdf_path)
        try:
            width_pt, height_pt = document[0].get_size()
        finally:
            document.close()
        width_mm, height_mm = width_pt * _MM_PER_POINT, height_pt * _MM_PER_POINT
        left, right = sorted((x1 / width_mm, x2 / width_mm))
        top, bottom = sorted((y1 / height_mm, y2 / height_mm))
        left, top = max(0.0, left), max(0.0, top)
        right, bottom = min(1.0, right), min(1.0, bottom)
        if not (left < right and top < bottom):
            raise ValueError(f"region lies outside the {width_mm:.0f} x {height_mm:.0f} mm sheet.")
        box = (left, top, right, bottom)
    return _render(pdf_path, 0, dpi, box)
