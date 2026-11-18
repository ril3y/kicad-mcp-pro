"""Stackup and fabricator rule presets, and the tools that apply them."""

from __future__ import annotations

from pathlib import Path

import pytest

from kicad_mcp.ipc import board_setup
from kicad_mcp.server import build_server
from tests.conftest import call_tool_text


def test_stackup_presets_are_consistent() -> None:
    for name, spec in board_setup.STACKUP_PRESETS.items():
        assert len(spec["dielectrics"]) == len(spec["copper_mm"]) - 1, name
    four = board_setup.STACKUP_PRESETS["jlcpcb-4-7628"]
    total = sum(four["copper_mm"]) + sum(layer[0] for layer in four["dielectrics"])
    assert total == pytest.approx(1.586, abs=0.01)


def test_rule_presets_only_name_real_constraints() -> None:
    from kicad_mcp._master_proto.mp.board.board_rules_pb2 import MinimumConstraints

    known = {field.name for field in MinimumConstraints.DESCRIPTOR.fields}
    for name, spec in board_setup.RULE_PRESETS.items():
        assert set(spec) - {"description"} <= known, name
    multilayer = board_setup.RULE_PRESETS["jlcpcb-multilayer"]
    assert (
        multilayer["min_through_drill"]
        < board_setup.RULE_PRESETS["jlcpcb-2-layer"]["min_through_drill"]
    )


@pytest.mark.anyio
async def test_stackup_and_rule_tools_report_what_kicad_holds(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        board_setup, "set_stackup", lambda preset: ["copper: F_Cu, 0.0350 mm", "total: 1.586 mm"]
    )
    monkeypatch.setattr(board_setup, "set_rules", lambda preset: ["min_clearance: 0.127 mm"])
    server = build_server("full")

    stackup = await call_tool_text(server, "pcb_set_layer_stackup", {})
    rules = await call_tool_text(server, "pcb_set_fab_rules", {})

    assert "JLC04161H-7628" in stackup
    assert "total: 1.586 mm" in stackup
    assert "min_clearance: 0.127 mm" in rules


@pytest.mark.anyio
async def test_unknown_presets_are_refused(sample_project: Path) -> None:
    server = build_server("full")
    assert "Unknown stackup" in await call_tool_text(
        server, "pcb_set_layer_stackup", {"preset": "nope"}
    )
    assert "Unknown rule set" in await call_tool_text(
        server, "pcb_set_fab_rules", {"preset": "nope"}
    )
