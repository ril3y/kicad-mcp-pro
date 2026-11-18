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


def test_set_net_classes_changes_default_and_adds_a_class_with_patterns() -> None:
    from kicad_mcp._master_proto.mp.common.commands import project_commands_pb2 as commands
    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        GetOpenDocumentsResponse,
    )
    from kicad_mcp.ipc import board_setup

    sent: dict[str, object] = {}

    class Client:
        def send(self, command: object, response_cls: type) -> object:
            name = type(command).__name__
            if name == "GetOpenDocuments":
                reply = GetOpenDocumentsResponse()
                reply.documents.add().project.name = "demo"
                return reply
            if name == "GetNetClasses":
                reply = commands.NetClassesResponse()
                default = reply.net_classes.add()
                default.name = "Default"
                default.board.clearance.value_nm = 200_000
                return reply
            sent[name] = command
            return response_cls()

    done = board_setup.set_net_classes(
        [
            {"name": "Default", "clearance_mm": 0.15},
            {
                "name": "Power",
                "track_width_mm": 0.6,
                "via_diameter_mm": 0.8,
                "patterns": ["/+24V*"],
            },
        ],
        client=Client(),  # type: ignore[arg-type]
    )

    classes = {item.name: item for item in sent["SetNetClasses"].net_classes}  # type: ignore[attr-defined]
    assert classes["Default"].board.clearance.value_nm == 150_000
    assert classes["Power"].board.clearance.value_nm == 200_000  # copied from Default
    assert classes["Power"].board.track_width.value_nm == 600_000
    assert classes["Power"].board.via_stack.copper_layers[0].size.x_nm == 800_000
    patterns = sent["SetNetClassAssignments"].pattern_assignments  # type: ignore[attr-defined]
    assert [(item.pattern, item.netclass) for item in patterns] == [("/+24V*", "Power")]
    assert done == ["Default: clearance 0.15 mm", "Power: track 0.6 mm; via 0.8 mm; nets /+24V*"]
