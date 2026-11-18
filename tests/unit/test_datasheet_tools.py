from __future__ import annotations

import io
from pathlib import Path

import pytest

from kicad_mcp.server import build_server
from tests.conftest import call_tool_text

pdfium = pytest.importorskip("pypdfium2")
pil_image = pytest.importorskip("PIL.Image")


def _make_pdf(path: Path) -> None:
    """Write a two-page PDF: page 1 has ratings text, page 2 a figure caption."""
    pages = [
        ["Absolute Maximum Ratings", "VIN to GND 70 V"],
        ["Figure 9-18. Example Layout", "Place CIN close to VIN"],
    ]
    objects: list[bytes] = []
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(len(pages)))
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode())
    font_id = 3 + 2 * len(pages)
    for index, lines in enumerate(pages):
        text = " ".join(
            f"BT /F1 12 Tf 72 {700 - 20 * row} Td ({line}) Tj ET" for row, line in enumerate(lines)
        ).encode()
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Contents {4 + 2 * index} 0 R /Resources << /Font << /F1 {font_id} 0 R >> >> >>"
            ).encode()
        )
        objects.append(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(text), text))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    out = io.BytesIO()
    out.write(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(out.tell())
        out.write(b"%d 0 obj\n%s\nendobj\n" % (number, body))
    xref = out.tell()
    out.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1))
    for offset in offsets:
        out.write(b"%010d 00000 n \n" % offset)
    out.write(
        b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    )
    path.write_bytes(out.getvalue())


@pytest.fixture
async def server_with_datasheet(sample_project: Path, tmp_path: Path) -> object:
    server = build_server("full")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})
    source = tmp_path / "incoming" / "demo-part.pdf"
    source.parent.mkdir()
    _make_pdf(source)
    await call_tool_text(server, "ds_add", {"part": "DEMO1", "source": str(source)})
    return server


@pytest.mark.anyio
async def test_add_and_list(server_with_datasheet: object, sample_project: Path) -> None:
    stored = sample_project / "docs" / "datasheets" / "DEMO1" / "demo-part.pdf"
    assert stored.is_file()
    listing = await call_tool_text(server_with_datasheet, "ds_list", {})
    assert "- DEMO1: demo-part.pdf" in listing


@pytest.mark.anyio
async def test_search_reports_page_numbers(server_with_datasheet: object) -> None:
    result = await call_tool_text(
        server_with_datasheet, "ds_search", {"part": "DEMO1", "query": "absolute maximum"}
    )
    assert "p1: Absolute Maximum Ratings" in result
    none = await call_tool_text(
        server_with_datasheet, "ds_search", {"part": "DEMO1", "query": "zzz"}
    )
    assert "No match" in none


@pytest.mark.anyio
async def test_read_returns_requested_pages(server_with_datasheet: object) -> None:
    result = await call_tool_text(server_with_datasheet, "ds_read", {"part": "DEMO1", "pages": "2"})
    assert "--- DEMO1 page 2 ---" in result
    assert "Place CIN close to VIN" in result
    assert "VIN to GND 70 V" not in result


@pytest.mark.anyio
async def test_figures_lists_captions(server_with_datasheet: object) -> None:
    result = await call_tool_text(
        server_with_datasheet, "ds_figures", {"part": "DEMO1", "keyword": "layout"}
    )
    assert "p2: Figure 9-18. Example Layout" in result


@pytest.mark.anyio
async def test_page_image_returns_png_and_saves_figure(
    server_with_datasheet: object, sample_project: Path
) -> None:
    result = await server_with_datasheet.call_tool(  # type: ignore[attr-defined]
        "ds_page_image",
        {"part": "DEMO1", "page": 2, "dpi": 72, "crop": "0,0,0.5,0.5", "save_as": "layout"},
    )
    content = result[0] if isinstance(result, tuple) else result
    image = next(item for item in content if getattr(item, "type", "") == "image")
    assert image.mimeType == "image/png"
    saved = sample_project / "docs" / "datasheets" / "DEMO1" / "figures" / "layout.png"
    with pil_image.open(saved) as picture:
        assert picture.size == (306, 396)


@pytest.mark.anyio
async def test_rejects_bad_input(server_with_datasheet: object, tmp_path: Path) -> None:
    not_pdf = tmp_path / "note.pdf"
    not_pdf.write_text("hello")
    for name, arguments, expected in (
        ("ds_add", {"part": "DEMO2", "source": str(not_pdf)}, "is not a PDF"),
        ("ds_add", {"part": "../x", "source": str(not_pdf)}, "Invalid part name"),
        ("ds_add", {"part": "DEMO2", "source": "http://example.com/a.pdf"}, "Only https://"),
        ("ds_read", {"part": "DEMO1", "pages": "9"}, "outside 1-2"),
        ("ds_read", {"part": "NOPE", "pages": "1"}, "No datasheet stored"),
    ):
        try:
            text = await call_tool_text(server_with_datasheet, name, arguments)
        except Exception as exc:  # noqa: BLE001
            text = str(exc)
        assert expected in text, (name, text)


@pytest.mark.anyio
async def test_sheet_image_renders_exported_schematic(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_run_cli_variants(variants: list[list[str]]) -> tuple[int, str, str]:
        args = variants[0]
        _make_pdf(Path(args[args.index("--output") + 1]))
        return 0, "", ""

    monkeypatch.setattr("kicad_mcp.tools.export_support._run_cli_variants", fake_run_cli_variants)
    server = build_server("full")

    result = await server.call_tool("sch_sheet_image", {"dpi": 72, "crop": "0,0,0.5,0.5"})
    content = result[0] if isinstance(result, tuple) else result
    image = next(item for item in content if getattr(item, "type", "") == "image")
    assert image.mimeType == "image/png"

    missing = await call_tool_text(server, "sch_sheet_image", {"sheet": "No Such Sheet"})
    assert "No page for sheet" in missing
