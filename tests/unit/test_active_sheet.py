from __future__ import annotations

import pytest

from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentSpecifier, DocumentType
from kicad_mcp._master_proto.mp.schematic.schematic_commands_pb2 import SchematicHierarchyResponse
from kicad_mcp.ipc import runtime_gate
from kicad_mcp.ipc.runtime_gate import SchematicIPCRequiredError


class _HierarchyClient:
    """Answers GetSchematicHierarchy with a root sheet and two children."""

    def send(self, command: object, response_cls: type) -> object:
        assert response_cls is SchematicHierarchyResponse
        response = SchematicHierarchyResponse()
        root = response.top_level_sheets.add()
        root.name = "board"
        root.path.path_human_readable = "/"
        root.path.path.add().value = "root-id"
        for name, sheet_id in (("Power 3V3", "power-id"), ("RS-485", "rs485-id")):
            child = root.children.add()
            child.name = name
            child.path.path_human_readable = f"/{name}/"
            child.path.path.add().value = "root-id"
            child.path.path.add().value = sheet_id
        return response


def _document() -> DocumentSpecifier:
    doc = DocumentSpecifier()
    doc.type = DocumentType.DOCTYPE_SCHEMATIC
    doc.sheet_path.path.add().value = "root-id"
    return doc


def test_root_is_the_default_target_and_is_named_outright() -> None:
    # KiCad reports the sheet edited last; the root must be named, not assumed.
    doc = _document()
    del doc.sheet_path.path[:]
    doc.sheet_path.path.add().value = "root-id"
    doc.sheet_path.path.add().value = "power-id"
    assert runtime_gate.get_active_sheet() == ""
    target = runtime_gate._target_document(_HierarchyClient(), [doc])
    assert [part.value for part in target.sheet_path.path] == ["root-id"]


@pytest.mark.parametrize("sheet", ["RS-485", "rs-485", "/RS-485/", "/RS-485"])
def test_active_sheet_selects_child_by_name_or_path(sheet: str) -> None:
    runtime_gate.set_active_sheet(sheet)
    doc = _document()
    target = runtime_gate._target_document(_HierarchyClient(), [doc])
    assert [part.value for part in target.sheet_path.path] == ["root-id", "rs485-id"]
    assert [part.value for part in doc.sheet_path.path] == ["root-id"]


@pytest.mark.parametrize("sheet", ["", "/", "  "])
def test_empty_or_slash_means_root(sheet: str) -> None:
    runtime_gate.set_active_sheet("RS-485")
    runtime_gate.set_active_sheet(sheet)
    assert runtime_gate.get_active_sheet() == ""


def test_unknown_sheet_is_an_error() -> None:
    runtime_gate.set_active_sheet("Missing")
    with pytest.raises(SchematicIPCRequiredError, match="'Missing' was not found"):
        runtime_gate._target_document(_HierarchyClient(), [_document()])


@pytest.mark.anyio
async def test_tool_sets_root_without_kicad_and_rejects_unreachable_sheet() -> None:
    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    server = build_server("full")
    root = await call_tool_text(server, "sch_set_active_sheet", {"sheet": "/"})
    assert "Active sheet: / (root)" in root
    refused = await call_tool_text(server, "sch_set_active_sheet", {"sheet": "RS-485"})
    assert "Active sheet not changed" in refused
    assert runtime_gate.get_active_sheet() == ""


def test_delete_items_matches_wires_and_labels_by_position(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """sch_delete_items: wires match in either direction; misses are reported."""
    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        DeleteItemsResponse,
        GetItemsResponse,
        GetOpenDocumentsResponse,
    )
    from kicad_mcp._master_proto.mp.common.types.enums_pb2 import KOT_SCH_LABEL, KOT_SCH_LINE
    from kicad_mcp._master_proto.mp.schematic import schematic_types_pb2 as sch_types
    from kicad_mcp.ipc._master_client import MasterAny

    wire = sch_types.SchematicLine()
    wire.id.value = "wire-1"
    wire.start.x_nm, wire.start.y_nm = 10_160_000, 20_320_000
    wire.end.x_nm, wire.end.y_nm = 30_480_000, 20_320_000
    label = sch_types.LocalLabel()
    label.id.value = "label-1"
    label.text.text = "LED_EN"
    label.position.x_nm, label.position.y_nm = 10_160_000, 20_320_000
    deleted: list[str] = []

    class Client(_HierarchyClient):
        def send(self, command: object, response_cls: type) -> object:
            name = type(command).__name__
            if name == "GetSchematicHierarchy":
                return super().send(command, response_cls)
            if name == "GetOpenDocuments":
                reply = GetOpenDocumentsResponse()
                reply.documents.add().CopyFrom(_document())
                return reply
            if name == "GetItems":
                reply = GetItemsResponse()
                kinds = list(command.types)  # type: ignore[attr-defined]
                for kind, item in ((KOT_SCH_LINE, wire), (KOT_SCH_LABEL, label)):
                    if kind in kinds:
                        packed = MasterAny()
                        packed.Pack(item)
                        reply.items.append(packed)
                return reply
            deleted.extend(item.value for item in command.item_ids)  # type: ignore[attr-defined]
            return DeleteItemsResponse()

    monkeypatch.setattr(runtime_gate, "check_ipc_gate", lambda **kwargs: (True, "ok"))
    done = runtime_gate.route_schematic_delete_items(
        wires=[[30.48, 20.32, 10.16, 20.32], [1.27, 1.27, 2.54, 1.27]],
        labels=[{"name": "LED_EN", "x": 10.16, "y": 20.32}, {"name": "LED_EN", "x": 0, "y": 0}],
        kicad_factory=Client,  # type: ignore[arg-type]
    )

    assert (done["wires"], done["labels"]) == (1, 1)
    assert sorted(deleted) == ["label-1", "wire-1"]
    assert done["missing"] == ["wire (1.27, 1.27) - (2.54, 1.27)", "label 'LED_EN' at (0, 0)"]
