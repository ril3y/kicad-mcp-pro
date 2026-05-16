# pyright: reportPrivateUsage=false, reportUnknownLambdaType=false
# pyright: reportMissingImports=false, reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
"""Unit tests for :func:`_reload_schematic_via_ipc`.

The helper is the single chokepoint that decides whether a schematic-mutating
MCP tool tells the agent ``Saved. KiCad refreshed.`` (live reload succeeded)
or one of four ``Saved. ...`` variants that mean ``file is on disk; KiCad
won't show the change until you do something``. Earlier the failure paths
either leaked a ``[debug: ...]`` suffix into the response or silently
swallowed the only signal that distinguishes ``KiCad isn't running``,
``KiCad is running but the wrong project is open``, ``kipy isn't even
installed``, and ``KiCad rejected our request``. These tests pin down all
six return strings + project-matching behavior without requiring a live
KiCad IPC peer.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

from kicad_mcp.connection import KiCadConnectionError
from kicad_mcp.tools import schematic as schematic_module
from kicad_mcp.tools.schematic import (
    _pick_matching_schematic_document,
    _reload_schematic_via_ipc,
)


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
    def __init__(
        self,
        documents: list[Any],
        send_exc: BaseException | None = None,
        get_open_documents_exc: BaseException | None = None,
    ) -> None:
        self._documents = documents
        self._client = _StubClient(send_exc=send_exc)
        self._get_open_documents_exc = get_open_documents_exc

    def get_open_documents(self, _doctype: Any) -> list[Any]:
        if self._get_open_documents_exc is not None:
            raise self._get_open_documents_exc
        return list(self._documents)


class _StubConfig:
    def __init__(self, sch_file: Path | None) -> None:
        self.sch_file = sch_file


def _patch_no_configured_project(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the helper see ``config.sch_file is None`` so it falls back to
    ``documents[0]`` — the pre-multi-project compat path."""
    monkeypatch.setattr(schematic_module, "get_config", lambda: _StubConfig(sch_file=None))


def _make_schematic_doc(project_name: str = "", project_path: str = "") -> Any:
    # Use a real protobuf ``DocumentSpecifier`` so CopyFrom inside the helper
    # operates on a genuine proto message rather than a fake. This keeps the
    # test honest about the real call path (SimpleNamespace mocks let the
    # original NoneType bug slip through).
    from kipy.proto.common.types.base_types_pb2 import DocumentSpecifier, DocumentType

    doc = DocumentSpecifier()
    doc.type = DocumentType.DOCTYPE_SCHEMATIC
    if project_name:
        doc.project.name = project_name
    if project_path:
        doc.project.path = project_path
    return doc


def test_returns_saved_no_kicad_when_get_kicad_raises_connection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_no_configured_project(monkeypatch)

    def _raise() -> None:
        raise KiCadConnectionError("Connection refused")

    monkeypatch.setattr(schematic_module, "get_kicad", _raise)

    result = _reload_schematic_via_ipc()

    assert result.startswith("Saved. KiCad isn't running for a live refresh")


def test_returns_saved_no_doc_when_no_schematic_is_open(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_no_configured_project(monkeypatch)
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: _StubKiCad(documents=[]))

    result = _reload_schematic_via_ipc()

    assert result == "Saved. No schematic is open in KiCad — open it to see the change."


def test_returns_saved_refresh_failed_when_send_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_no_configured_project(monkeypatch)
    stub = _StubKiCad(documents=[_make_schematic_doc()], send_exc=ConnectionError("boom"))
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: stub)

    result = _reload_schematic_via_ipc()

    assert result == "Saved. Live refresh request failed; reload manually in KiCad."
    assert len(stub._client.calls) == 1, "send() must have been attempted exactly once"


def test_returns_saved_refresh_failed_when_get_open_documents_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Regression guard: a stale socket can make ``get_open_documents`` throw
    # after ``get_kicad()`` succeeded. The helper must still degrade
    # gracefully rather than propagate the exception.
    _patch_no_configured_project(monkeypatch)
    stub = _StubKiCad(
        documents=[],
        get_open_documents_exc=RuntimeError("ipc-stale"),
    )
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: stub)

    result = _reload_schematic_via_ipc()

    assert result == "Saved. Live refresh request failed; reload manually in KiCad."
    assert stub._client.calls == [], "send() must not have been attempted"


def test_returns_saved_refreshed_and_sends_revert_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from google.protobuf.empty_pb2 import Empty  # type: ignore[import-untyped]
    from kipy.proto.common.commands import editor_commands_pb2
    from kipy.proto.common.types.base_types_pb2 import DocumentType

    _patch_no_configured_project(monkeypatch)
    stub = _StubKiCad(documents=[_make_schematic_doc()])
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: stub)

    result = _reload_schematic_via_ipc()

    assert result == "Saved. KiCad refreshed."
    # Strong-form assertion: pin the command class AND its document type,
    # because a future refactor could send ``SaveDocument`` (or any other
    # editor_commands_pb2 message) and the test would still pass under a
    # ``calls[0][1] is Empty`` check alone.
    assert len(stub._client.calls) == 1
    command, response_type = stub._client.calls[0]
    assert isinstance(command, editor_commands_pb2.RevertDocument)
    assert command.document.type == DocumentType.DOCTYPE_SCHEMATIC
    assert response_type is Empty


def test_picks_matching_project_when_multiple_schematics_open(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    # Audit found that ``documents[0]`` was unsafe in multi-project KiCad
    # sessions — we could revert the wrong project's schematic. The helper
    # must now pick the document whose project matches the configured
    # ``sch_file`` path/stem.
    project_dir = tmp_path / "wanted_project"
    project_dir.mkdir()
    sch_file = project_dir / "wanted_project.kicad_sch"
    sch_file.touch()

    other_project = _make_schematic_doc(project_name="other", project_path=str(tmp_path / "other"))
    wanted_project = _make_schematic_doc(
        project_name="wanted_project",
        project_path=str(project_dir),
    )

    stub = _StubKiCad(documents=[other_project, wanted_project])
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: stub)
    monkeypatch.setattr(schematic_module, "get_config", lambda: _StubConfig(sch_file=sch_file))

    result = _reload_schematic_via_ipc()

    assert result == "Saved. KiCad refreshed."
    # Strong: confirm the revert command targets the configured project,
    # not the first open schematic.
    sent_command, _ = stub._client.calls[0]
    assert sent_command.document.project.name == "wanted_project"


def test_returns_saved_no_doc_when_no_open_schematic_matches_configured_project(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    # Defense against reverting a stranger's schematic: if KiCad has
    # schematics open but none belong to the configured project, refuse the
    # revert and tell the user the schematic isn't open.
    project_dir = tmp_path / "wanted_project"
    project_dir.mkdir()
    sch_file = project_dir / "wanted_project.kicad_sch"
    sch_file.touch()

    stranger = _make_schematic_doc(project_name="stranger", project_path=str(tmp_path / "stranger"))

    stub = _StubKiCad(documents=[stranger])
    monkeypatch.setattr(schematic_module, "get_kicad", lambda: stub)
    monkeypatch.setattr(schematic_module, "get_config", lambda: _StubConfig(sch_file=sch_file))

    result = _reload_schematic_via_ipc()

    assert result == "Saved. No schematic is open in KiCad — open it to see the change."
    assert stub._client.calls == [], "must not revert a stranger's schematic"


def test_returns_saved_ipc_client_missing_when_proto_imports_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Distinct from ``KiCad isn't running'': a missing kipy install is a
    # deployment problem — the response should send the user to fix the
    # install, not to relaunch KiCad.
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

    assert result.startswith("Saved. KiCad IPC client (kipy) is unavailable")


def test_pick_matching_schematic_document_falls_back_to_documents_zero_without_config() -> None:
    # Unit test for the picker in isolation: with no configured sch_file
    # we keep the legacy ``documents[0]`` behavior so we don't break the
    # single-project workflow that PR-d9717b5 originally fixed.
    docs = [_make_schematic_doc(project_name=f"p{i}") for i in range(3)]

    chosen, idx = _pick_matching_schematic_document(docs, configured_sch_file=None)

    assert chosen is docs[0]
    assert idx == 0


def test_pick_matching_schematic_document_returns_none_when_no_match(
    tmp_path: Path,
) -> None:
    sch_file = tmp_path / "wanted.kicad_sch"
    docs = [_make_schematic_doc(project_name="stranger", project_path=str(tmp_path))]

    chosen, idx = _pick_matching_schematic_document(docs, configured_sch_file=sch_file)

    assert chosen is None
    assert idx == -1
