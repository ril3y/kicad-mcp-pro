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


def test_root_is_the_default_target() -> None:
    doc = _document()
    assert runtime_gate.get_active_sheet() == ""
    assert runtime_gate._target_document(_HierarchyClient(), [doc]) is doc


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
