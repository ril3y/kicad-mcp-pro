"""Headless mode: which background KiCad API server a command goes to."""

from __future__ import annotations

from pathlib import Path

import pytest

from kicad_mcp._master_proto.mp.board.board_commands_pb2 import ImportNetlist
from kicad_mcp._master_proto.mp.common.commands.base_commands_pb2 import GetVersion
from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
    CreateItems,
    GetOpenDocuments,
)
from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType
from kicad_mcp._master_proto.mp.schematic.schematic_commands_pb2 import PlaceSymbolFromLibrary
from kicad_mcp.discovery import scan_project_dir
from kicad_mcp.ipc import headless


def test_commands_are_routed_by_the_document_they_name() -> None:
    assert headless.kind_of(ImportNetlist()) == "board"
    assert headless.kind_of(PlaceSymbolFromLibrary()) == "schematic"

    open_boards = GetOpenDocuments()
    open_boards.type = DocumentType.DOCTYPE_PCB
    assert headless.kind_of(open_boards) == "board"
    open_schematics = GetOpenDocuments()
    open_schematics.type = DocumentType.DOCTYPE_SCHEMATIC
    assert headless.kind_of(open_schematics) == "schematic"

    on_board = CreateItems()
    on_board.header.document.type = DocumentType.DOCTYPE_PCB
    assert headless.kind_of(on_board) == "board"
    # A command that names no document follows the last one that did.
    assert headless.kind_of(GetVersion()) == "board"
    on_schematic = CreateItems()
    on_schematic.header.document.type = DocumentType.DOCTYPE_SCHEMATIC
    assert headless.kind_of(on_schematic) == "schematic"
    assert headless.kind_of(GetVersion()) == "schematic"


def test_headless_is_off_unless_asked_for(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KICAD_MCP_HEADLESS", raising=False)
    assert headless.enabled() is False
    monkeypatch.setenv("KICAD_MCP_HEADLESS", "1")
    assert headless.enabled() is True


def test_root_schematic_is_the_one_named_like_the_project(tmp_path: Path) -> None:
    folder = tmp_path / "any-folder-name"
    folder.mkdir()
    for name in ("board.kicad_pro", "board.kicad_pcb", "board.kicad_sch", "a_subsheet.kicad_sch"):
        (folder / name).write_text("", encoding="utf-8")

    found = scan_project_dir(folder)

    assert found["schematic"] == folder / "board.kicad_sch"
    assert found["pcb"] == folder / "board.kicad_pcb"
