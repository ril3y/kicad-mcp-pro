"""sch_draw places a whole group of schematic items in one call."""

from __future__ import annotations

from typing import Any

import pytest

from kicad_mcp.server import build_server
from tests.conftest import call_tool_text


@pytest.mark.anyio
async def test_sch_draw_places_everything_and_numbers_power_symbols(
    sample_project: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    placed: list[dict[str, Any]] = []
    created: list[Any] = []

    def fake_place(**kwargs: Any) -> str:  # noqa: ANN401
        placed.append(kwargs)
        return "ok"

    def fake_create(items: list[Any]) -> str:
        created.extend(items)
        return "ok"

    monkeypatch.setattr("kicad_mcp.tools.schematic.route_schematic_place_symbol", fake_place)
    monkeypatch.setattr("kicad_mcp.tools.schematic.route_schematic_create", fake_create)
    server = build_server("full")

    result = await call_tool_text(
        server,
        "sch_draw",
        {
            "symbols": [
                {"library": "Parts", "symbol": "R_10k", "ref": "R1", "x": 93.98, "y": 119.4}
            ],
            "power": [
                {"name": "GND", "x": 93.98, "y": 138.43},
                {"name": "PWR_FLAG", "x": 10, "y": 10},
            ],
            "wires": [[93.98, 123.19, 93.98, 128.27]],
            "junctions": [[93.98, 125.73]],
            "labels": [{"name": "MODE", "x": 88.9, "y": 125.73}],
            "hier_labels": [{"name": "PG", "x": 116.84, "y": 125.73}],
            "no_connects": [[50.8, 50.8]],
            "power_ref_start": 20,
        },
    )  # fmt: skip

    assert "Drew 1 symbol(s), 2 power symbol(s), 1 wire(s), 1 junction(s)" in result
    assert placed[0]["reference"] == "R1"
    assert placed[0]["y_mm"] == pytest.approx(119.38)  # snapped to the 1.27 mm grid
    assert [item["reference"] for item in placed[1:]] == ["#PWR020", "#FLG021"]
    assert len(created) == 5


@pytest.mark.anyio
async def test_sch_draw_stops_at_the_first_part_that_cannot_be_placed(
    sample_project: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    created: list[Any] = []

    def failing_place(**kwargs: Any) -> str:  # noqa: ANN401
        raise RuntimeError("Symbol not found")

    monkeypatch.setattr("kicad_mcp.tools.schematic.route_schematic_place_symbol", failing_place)
    monkeypatch.setattr(
        "kicad_mcp.tools.schematic.route_schematic_create", lambda items: created.extend(items)
    )
    server = build_server("full")

    result = await call_tool_text(
        server,
        "sch_draw",
        {
            "symbols": [{"library": "Nope", "symbol": "X", "ref": "U9", "x": 0, "y": 0}],
            "wires": [[0, 0, 2.54, 0]],
        },
    )

    assert "could not place Nope:X as U9" in result
    assert created == []
