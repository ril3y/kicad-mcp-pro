"""The review page: datasheet figure beside the project picture."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import pytest

from kicad_mcp.server import build_server
from kicad_mcp.tools import review
from tests.conftest import call_tool_text

pytest.importorskip("pypdfium2")


@pytest.mark.anyio
async def test_review_items_are_added_replaced_served_and_removed(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from tests.unit.test_datasheet_tools import _make_pdf

    def fake_run_cli_variants(variants: list[list[str]]) -> tuple[int, str, str]:
        args = variants[0]
        _make_pdf(Path(args[args.index("--output") + 1]))
        return 0, "", ""

    monkeypatch.setattr("kicad_mcp.tools.export_support._run_cli_variants", fake_run_cli_variants)
    monkeypatch.setattr(review, "_server", None)
    server = build_server("full")

    first = await call_tool_text(
        server,
        "review_add",
        {"title": "Buck: layout", "section": "3.3 V", "notes": "<b>draft</b>",
         "board_region": "20,20,120,100"},
    )  # fmt: skip
    again = await call_tool_text(
        server,
        "review_add",
        {"title": "Buck: layout", "section": "3.3 V", "notes": "placed", "sheet": "/"},
    )

    folder = sample_project / "review"
    items = json.loads((folder / "items.json").read_text("utf-8"))
    page = (folder / "index.html").read_text("utf-8")
    assert "board picture" in first
    assert "schematic picture" in again
    assert len(items) == 1
    assert items[0]["notes"] == "placed"
    assert (folder / "img" / "buck-layout-project.png").exists()
    assert "Buck: layout" in page
    assert "<b>draft</b>" not in page

    served = await call_tool_text(server, "review_serve", {"port": 8931})
    url = served.split("Review page: ")[1].split(" ")[0]
    with urllib.request.urlopen(url) as response:  # noqa: S310 - localhost test server
        assert response.status == 200
        assert b"Buck: layout" in response.read()
    assert url.startswith("http://127.0.0.1:")

    removed = await call_tool_text(server, "review_remove", {"title": "Buck: layout"})
    missing = await call_tool_text(server, "review_remove", {"title": "Buck: layout"})
    assert "0 item(s) left" in removed
    assert "No review item" in missing
    if review._server is not None:
        review._server.shutdown()
        review._server.server_close()
