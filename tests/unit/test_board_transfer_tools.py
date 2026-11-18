"""Sheet pins, KiCad's own netlist import, and board pictures."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from kicad_mcp.server import build_server
from tests.conftest import call_tool_text


@pytest.mark.anyio
async def test_sch_add_sheet_pins_reports_positions(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: dict[str, Any] = {}

    def fake_route(sheet: str, pins: list[dict[str, Any]]) -> list[tuple[str, float, float, bool]]:
        seen["sheet"], seen["pins"] = sheet, pins
        return [("+24V_PROT", 40.64, 43.18, True), ("PG_3V3", 71.12, 43.18, False)]

    monkeypatch.setattr("kicad_mcp.ipc.runtime_gate.route_schematic_add_sheet_pins", fake_route)
    server = build_server("full")

    result = await call_tool_text(
        server,
        "sch_add_sheet_pins",
        {
            "sheet": "Power 3V3",
            "pins": [{"name": "+24V_PROT"}, {"name": "PG_3V3", "side": "right"}],
        },
    )

    assert seen["sheet"] == "Power 3V3"
    assert "+24V_PROT at (40.64, 43.18) mm, added" in result
    assert "PG_3V3 at (71.12, 43.18) mm, already there" in result


@pytest.mark.anyio
async def test_sch_add_sheet_pins_reports_bad_requests(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def failing(sheet: str, pins: list[dict[str, Any]]) -> list[tuple[str, float, float, bool]]:
        raise ValueError("No sheet block named 'Nope' on the root sheet.")

    monkeypatch.setattr("kicad_mcp.ipc.runtime_gate.route_schematic_add_sheet_pins", failing)
    server = build_server("full")

    result = await call_tool_text(
        server, "sch_add_sheet_pins", {"sheet": "Nope", "pins": [{"name": "X"}]}
    )
    assert "Sheet pins not added: No sheet block named 'Nope'" in result


@pytest.mark.anyio
async def test_pcb_import_netlist_exports_then_asks_kicad(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from kicad_mcp.config import get_config

    cli = tmp_path / "kicad-cli"
    cli.write_text("", encoding="utf-8")
    monkeypatch.setattr(get_config(), "kicad_cli", cli)
    calls: dict[str, Any] = {}

    class Done:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(argv: list[str], **kwargs: Any) -> Done:  # noqa: ANN401
        calls["argv"] = argv
        Path(argv[argv.index("--output") + 1]).write_text("(export)", encoding="utf-8")
        return Done()

    def fake_import(netlist: Path, **kwargs: Any) -> tuple[int, int, int, str]:  # noqa: ANN401
        calls["netlist"], calls["kwargs"] = netlist, kwargs
        return 0, 1, 26, "Add C1 (Capacitor_SMD:C_1206_3216Metric)."

    monkeypatch.setattr("subprocess.run", fake_run)
    monkeypatch.setattr("kicad_mcp.ipc.runtime_gate.route_board_import_netlist", fake_import)
    server = build_server("full")

    result = await call_tool_text(server, "pcb_import_netlist", {"dry_run": True})

    assert calls["argv"][1:4] == ["sch", "export", "netlist"]
    assert calls["netlist"].name == "netlist.net"
    assert calls["kwargs"]["dry_run"] is True
    assert "Dry run: KiCad netlist import: 26 new footprint(s), 0 error(s), 1 warning(s)." in result
    assert "Add C1" in result


@pytest.mark.anyio
async def test_pcb_board_image_refuses_a_region_off_the_sheet(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pytest.importorskip("pypdfium2")
    from tests.unit.test_datasheet_tools import _make_pdf

    def fake_run_cli_variants(variants: list[list[str]]) -> tuple[int, str, str]:
        args = variants[0]
        _make_pdf(Path(args[args.index("--output") + 1]))
        return 0, "", ""

    monkeypatch.setattr("kicad_mcp.tools.export_support._run_cli_variants", fake_run_cli_variants)
    server = build_server("full")

    picture = await server.call_tool("pcb_board_image", {"region": "20,20,120,100", "dpi": 72})
    content = picture[0] if isinstance(picture, tuple) else picture
    assert any(getattr(item, "type", "") == "image" for item in content)

    outside = await call_tool_text(server, "pcb_board_image", {"region": "900,900,950,950"})
    assert "outside the" in outside


@pytest.mark.anyio
async def test_pcb_tidy_text_hides_values_and_sizes_references(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class Attributes:
        size: Any = None
        stroke_width = 0

    class Text:
        def __init__(self, value: str) -> None:
            self.value = value
            self.attributes = Attributes()

    class Field:
        def __init__(self, value: str) -> None:
            self.text = Text(value)
            self.visible = True

    class Footprint:
        def __init__(self, ref: str) -> None:
            self.reference_field = Field(ref)
            self.value_field = Field("10k")

    class Board:
        def __init__(self) -> None:
            self.footprints = [Footprint("R1"), Footprint("C1")]
            self.updated: list[Any] = []

        def get_footprints(self) -> list[Footprint]:
            return self.footprints

        def update_items(self, items: list[Any]) -> None:
            self.updated = items

    board = Board()
    monkeypatch.setattr("kicad_mcp.tools.pcb.get_board", lambda: board)
    monkeypatch.setattr("kicad_mcp.connection.get_board", lambda: board)
    server = build_server("full")

    result = await call_tool_text(server, "pcb_tidy_text", {"references": ["R1"]})

    assert "Tidied text on 1 footprint(s): values hidden, references 0.8 mm" in result
    assert board.footprints[0].value_field.visible is False
    assert board.footprints[0].reference_field.text.attributes.stroke_width == 150_000
    assert board.footprints[1].value_field.visible is True
    assert len(board.updated) == 1
    assert "must be" in await call_tool_text(server, "pcb_tidy_text", {"reference_size_mm": 0.1})


def test_sheet_block_grows_to_hold_its_pins(monkeypatch: pytest.MonkeyPatch) -> None:
    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        GetItemsResponse,
        GetOpenDocumentsResponse,
        UpdateItemsResponse,
    )
    from kicad_mcp._master_proto.mp.schematic import schematic_types_pb2 as sch_types
    from kicad_mcp._master_proto.mp.schematic.schematic_commands_pb2 import (
        SchematicHierarchyResponse,
    )
    from kicad_mcp.ipc import runtime_gate
    from kicad_mcp.ipc._master_client import MasterAny

    block = sch_types.SheetSymbol()
    block.name_field.text.text = "Controller"
    block.position.x_nm, block.position.y_nm = 162_560_000, 40_640_000
    block.size.x_nm, block.size.y_nm = 30_480_000, 20_320_000
    block.filename_field.text.position.y_nm = 61_000_000
    sent: dict[str, Any] = {}

    class Client:
        def send(self, command: Any, response_cls: Any) -> Any:  # noqa: ANN401
            name = type(command).__name__
            if name == "GetOpenDocuments":
                reply = GetOpenDocumentsResponse()
                reply.documents.add()
                return reply
            if name == "GetSchematicHierarchy":
                reply = SchematicHierarchyResponse()
                reply.top_level_sheets.add().path.path_human_readable = "/"
                return reply
            if name == "GetItems":
                reply = GetItemsResponse()
                packed = MasterAny()
                packed.Pack(block)
                reply.items.append(packed)
                return reply
            sent["update"] = command
            return UpdateItemsResponse()

    monkeypatch.setattr(runtime_gate, "check_ipc_gate", lambda **kwargs: (True, "ok"))
    names = [f"SIG{index}" for index in range(10)]
    results = runtime_gate.route_schematic_add_sheet_pins(
        "Controller",
        [{"name": name, "side": "left"} for name in names],
        kicad_factory=Client,  # type: ignore[arg-type]
    )

    updated = sch_types.SheetSymbol()
    sent["update"].items[0].Unpack(updated)
    assert updated.size.y_nm == 11 * 2_540_000  # ten pins and a margin
    assert updated.filename_field.text.position.y_nm == 61_000_000 + (27_940_000 - 20_320_000)
    assert [round(y, 2) for _name, _x, y, _added in results][:2] == [43.18, 45.72]
    assert results[-1][2] == pytest.approx(40.64 + 25.4)

    low = runtime_gate.route_schematic_add_sheet_pins(
        "Controller",
        [{"name": "LOW", "side": "right", "offset_mm": 43.18}],
        kicad_factory=Client,  # type: ignore[arg-type]
    )
    sent["update"].items[0].Unpack(updated)
    assert low[0][2] == pytest.approx(40.64 + 43.18)
    assert updated.size.y_nm == 43_180_000 + 2_540_000  # grown to hold the given position
