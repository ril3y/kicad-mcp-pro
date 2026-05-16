# pyright: reportPrivateUsage=false, reportUnknownLambdaType=false
# pyright: reportMissingImports=false, reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
"""Unit tests for :func:`_reload_schematic_via_ipc`.

The helper is the single chokepoint that decides whether a schematic-mutating
MCP tool tells the agent ``Saved. KiCad refreshed.`` (live reload succeeded)
or one of three ``Saved. ...`` variants that mean ``file is on disk; KiCad
won't show the change until you do something``. Earlier the failure paths
either leaked a ``[debug: ...]`` suffix into the response or silently
swallowed the only signal that distinguishes ``KiCad isn't running'' from
``KiCad is running but rejected our request''. These tests pin down the
five return strings without requiring a live KiCad IPC peer.
"""

from __future__ import annotations

import sys
from typing import Any

import pytest

from kicad_mcp.connection import KiCadConnectionError
from kicad_mcp.tools import schematic as schematic_module
from kicad_mcp.tools.schematic import _reload_schematic_via_ipc


class _StubClient:
    def __init__(self, send_exc: BaseException | None = None) -> None:
        self.send_exc = send_exc
        self.calls: list[tuple[Any, Any]] = []

    def send(self, command: Any, response_type: Any) -> Any:
        self.calls.append((command, response_type))
        if self.send_exc is not None:
            raise self.send_exc
        return None


class _StubKiCad:
    def __init__(self, documents: list[Any], send_exc: BaseException | None = None) -> None:
        self._documents = documents
        self._client = _StubClient(send_exc=send_exc)

    def get_open_documents(self, _doctype: Any) -> list[Any]:
        return list(self._documents)


def test_returns_saved_no_kicad_when_get_kicad_raises_connection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise() -> None:
        raise KiCadConnectionError("Connection refused")

    monkeypatch.setattr(schematic_module, "get_kicad", _raise)

    result = _reload_schematic_via_ipc()

    assert result.startswith("Saved. KiCad isn't running for a live refresh")


def test_returns_saved_no_doc_when_no_schematic_is_open(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: _StubKiCad(documents=[]))

    result = _reload_schematic_via_ipc()

    assert result == "Saved. No schematic is open in KiCad — open it to see the change."


def _real_document_id() -> Any:
    # Use a real protobuf ``DocumentSpecifier`` so CopyFrom inside the helper
    # operates on a genuine proto message rather than a fake. This avoids
    # mocking the kipy proto factories and keeps the test honest about the
    # real call path.
    from kipy.proto.common.types.base_types_pb2 import DocumentSpecifier, DocumentType

    doc = DocumentSpecifier()
    doc.type = DocumentType.DOCTYPE_SCHEMATIC
    return doc


def test_returns_saved_refresh_failed_when_send_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub = _StubKiCad(documents=[_real_document_id()], send_exc=ConnectionError("boom"))
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: stub)

    result = _reload_schematic_via_ipc()

    assert result == "Saved. Live refresh request failed; reload manually in KiCad."
    assert len(stub._client.calls) == 1, "send() must have been attempted exactly once"


def test_returns_saved_refreshed_when_send_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stub = _StubKiCad(documents=[_real_document_id()])
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: stub)

    result = _reload_schematic_via_ipc()

    assert result == "Saved. KiCad refreshed."
    # Verify the response type passed to send() is ``Empty``; passing
    # ``NoneType`` was the original silent-failure bug.
    from google.protobuf.empty_pb2 import Empty  # type: ignore[import-untyped]

    assert stub._client.calls[0][1] is Empty


def test_returns_saved_no_kicad_when_proto_imports_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Simulate a dev environment where the kipy proto modules cannot be
    # imported — the helper must still confirm the file-side save without
    # crashing.
    for name in (
        "google.protobuf.empty_pb2",
        "kipy.proto.common.commands.editor_commands_pb2",
        "kipy.proto.common.types.base_types_pb2",
    ):
        monkeypatch.setitem(sys.modules, name, None)

    # If the helper progressed past the import block we'd hit get_kicad;
    # make that loud so the test fails informatively rather than from a
    # downstream NoneType error.
    def _should_not_reach() -> None:
        raise AssertionError("import-unavailable branch must short-circuit before get_kicad")

    monkeypatch.setattr(schematic_module, "get_kicad", _should_not_reach)

    result = _reload_schematic_via_ipc()

    assert result.startswith("Saved. KiCad isn't running for a live refresh")
