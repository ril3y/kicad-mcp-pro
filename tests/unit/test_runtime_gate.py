# pyright: reportPrivateUsage=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportArgumentType=false
# pyright: reportUnusedFunction=false
# ruff: noqa: ANN401
"""Unit tests for :mod:`kicad_mcp.ipc.runtime_gate` — IPC-only edition.

The gate decides whether a schematic mutation should be sent over IPC.
Since 2026-05-22 there is no file-edit fallback: a closed gate causes
the routing helper to raise :class:`SchematicIPCRequiredError` with a
human-readable reason. These tests pin the new contract.

Every IPC call is mocked through a fake ``MasterKiCadClient`` — no
socket is opened and no KiCad process is required.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from kicad_mcp._master_proto.mp.common.commands.base_commands_pb2 import (
    GetVersion,
    GetVersionResponse,
)
from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
    CreateItems,
    CreateItemsResponse,
    GetOpenDocuments,
    GetOpenDocumentsResponse,
    ItemCreationResult,
    ItemStatusCode,
)
from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import (
    DocumentSpecifier,
    DocumentType,
)
from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
    GlobalLabel,
    HierarchicalLabel,
    LocalLabel,
    SchematicLine,
    SchematicLineType,
)
from kicad_mcp.ipc import runtime_gate
from kicad_mcp.ipc._master_client import ApiError, MasterAny
from kicad_mcp.ipc.runtime_gate import (
    SCH_IPC_FORCE_ENV,
    SCH_IPC_PERSISTENCE_HINT,
    SchematicIPCRequiredError,
    _connected_kicad_has_fix,
    _full_version_has_fix,
    _has_open_schematic,
    build_global_label_proto,
    build_hierarchical_label_proto,
    build_local_label_proto,
    build_wire_proto,
    check_ipc_gate,
    reset_runtime_gate_cache,
    route_schematic_create,
)

if TYPE_CHECKING:
    from google.protobuf.message import Message


# ---------------------------------------------------------------------------
# Scaffolding
# ---------------------------------------------------------------------------


class FakeClient:
    """Stand-in for :class:`MasterKiCadClient` driven by command type."""

    def __init__(
        self,
        *,
        responses_by_cmd: dict[type, list[Message]] | None = None,
        raise_on: type | tuple[type, ...] | None = None,
        raise_with: Exception | None = None,
    ) -> None:
        self.sent: list[tuple[Message, type[Message]]] = []
        self._responses = {k: list(v) for k, v in (responses_by_cmd or {}).items()}
        self._raise_on = raise_on
        self._raise_with = raise_with

    def send(self, command, response_cls):  # type: ignore[no-untyped-def]  # noqa: ANN201
        self.sent.append((command, response_cls))
        if self._raise_on is not None and isinstance(command, self._raise_on):
            raise self._raise_with or ApiError("scripted failure")
        queue = self._responses.get(type(command))
        if queue:
            return queue.pop(0)
        return response_cls()


def _version_response(full_version: str) -> GetVersionResponse:
    response = GetVersionResponse()
    response.version.full_version = full_version
    return response


def _docs_response(filenames: list[str]) -> GetOpenDocumentsResponse:
    response = GetOpenDocumentsResponse()
    for name in filenames:
        doc = DocumentSpecifier()
        doc.type = DocumentType.DOCTYPE_SCHEMATIC
        doc.board_filename = name
        response.documents.append(doc)
    return response


def _ok_create_response() -> CreateItemsResponse:
    response = CreateItemsResponse()
    result = ItemCreationResult()
    result.status.code = ItemStatusCode.ISC_OK
    any_item = MasterAny()
    any_item.Pack(GlobalLabel())
    result.item.CopyFrom(any_item)
    response.created_items.append(result)
    return response


@pytest.fixture(autouse=True)
def _reset_cache() -> None:
    """Each test starts with a clean version-detection cache."""

    reset_runtime_gate_cache()


# ---------------------------------------------------------------------------
# _full_version_has_fix — string heuristic
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "version,expected",
    [
        ("", False),
        ("10.0.3", False),
        ("10.0.1", False),
        ("garbage", False),
        ("not-a-version", False),
        ("not.a.version-15-ghashy", False),
        ("10.0.3-12-gabcdef1234", False),  # patched stable, uncertain
        ("9.99.0", False),  # major < fixed
        ("10.98.0", False),  # minor < fixed
        ("10.99.0-1059-g0895df3e3c", True),  # master nightly
        ("v10.99.0-1-gdeadbeef00", True),  # leading 'v' tolerated
        ("11.0.0", True),  # future release
        ("11.2.5-7-gabcdef1234", True),  # patched future release
        ("0.0.0-99-g3dca4e0e38ff", True),  # explicit hash match
        ("anything-with-3dca4e0e38-inside", True),
    ],
)
def test_full_version_has_fix(version: str, expected: bool) -> None:
    assert _full_version_has_fix(version) is expected


# ---------------------------------------------------------------------------
# _connected_kicad_has_fix
# ---------------------------------------------------------------------------


def test_version_probe_returns_true_for_master() -> None:
    client = FakeClient(
        responses_by_cmd={GetVersion: [_version_response("10.99.0-1059-g0895df3e3c")]}
    )
    assert _connected_kicad_has_fix(kicad_factory=lambda: client) is True


def test_version_probe_returns_false_for_stable() -> None:
    client = FakeClient(responses_by_cmd={GetVersion: [_version_response("10.0.3")]})
    assert _connected_kicad_has_fix(kicad_factory=lambda: client) is False


def test_version_probe_fails_closed_on_no_handler_available_by_default() -> None:
    """AS_UNHANDLED + no force flag -> False.

    Standalone eeschema doesn't register GetVersion, so the probe gets
    'no handler available'. The default policy is to refuse — operators
    set ``KICAD_MCP_SCH_IPC_FORCE=1`` to bypass.
    """

    client = FakeClient(
        raise_on=GetVersion,
        raise_with=ApiError("no handler available for GetVersion"),
    )
    assert _connected_kicad_has_fix(kicad_factory=lambda: client) is False


def test_version_probe_returns_true_on_no_handler_with_force(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``KICAD_MCP_SCH_IPC_FORCE=1`` flips AS_UNHANDLED handling to assume-ok."""

    monkeypatch.setenv(SCH_IPC_FORCE_ENV, "1")
    client = FakeClient(
        raise_on=GetVersion,
        raise_with=ApiError("no handler available for GetVersion"),
    )
    assert _connected_kicad_has_fix(kicad_factory=lambda: client) is True


def test_version_probe_returns_true_on_as_unhandled_with_force(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(SCH_IPC_FORCE_ENV, "1")
    client = FakeClient(
        raise_on=GetVersion,
        raise_with=ApiError("AS_UNHANDLED on this message"),
    )
    assert _connected_kicad_has_fix(kicad_factory=lambda: client) is True


def test_version_probe_returns_false_on_other_api_error() -> None:
    client = FakeClient(
        raise_on=GetVersion,
        raise_with=ApiError("connection refused at socket"),
    )
    assert _connected_kicad_has_fix(kicad_factory=lambda: client) is False


def test_version_probe_returns_false_on_arbitrary_exception() -> None:
    client = FakeClient(
        raise_on=GetVersion,
        raise_with=RuntimeError("transport reset"),
    )
    assert _connected_kicad_has_fix(kicad_factory=lambda: client) is False


def test_version_probe_returns_false_on_factory_failure() -> None:
    def boom() -> FakeClient:
        raise RuntimeError("ipc unreachable")

    assert _connected_kicad_has_fix(kicad_factory=boom) is False


def test_version_probe_caches_result_across_calls() -> None:
    client = FakeClient(responses_by_cmd={GetVersion: [_version_response("10.99.0-1-gdeadbeef00")]})

    factory_calls: list[int] = []

    def factory() -> FakeClient:
        factory_calls.append(1)
        return client

    first = _connected_kicad_has_fix(kicad_factory=factory)
    second = _connected_kicad_has_fix(kicad_factory=factory)

    assert first is True
    assert second is True
    assert factory_calls == [1]
    assert len(client.sent) == 1


def test_reset_runtime_gate_cache_forces_reprobe() -> None:
    client = FakeClient(
        responses_by_cmd={
            GetVersion: [
                _version_response("10.99.0-1-gdeadbeef00"),
                _version_response("10.99.0-1-gdeadbeef00"),
            ]
        }
    )

    _connected_kicad_has_fix(kicad_factory=lambda: client)
    reset_runtime_gate_cache()
    _connected_kicad_has_fix(kicad_factory=lambda: client)

    sent_versions = [c for c, _ in client.sent if isinstance(c, GetVersion)]
    assert len(sent_versions) == 2


def test_version_probe_default_factory_constructs_master_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``kicad_factory=None`` -> the default factory creates a MasterKiCadClient."""

    constructed: list[Any] = []

    class _SpyClient:
        def __init__(self) -> None:
            constructed.append(self)

        def send(self, command, response_cls):  # type: ignore[no-untyped-def]  # noqa: ANN201
            return _version_response("10.99.0-1-gdeadbeef00")

    monkeypatch.setattr("kicad_mcp.ipc._master_client.MasterKiCadClient", _SpyClient)

    assert _connected_kicad_has_fix() is True
    assert len(constructed) == 1


# ---------------------------------------------------------------------------
# _has_open_schematic
# ---------------------------------------------------------------------------


def test_has_open_schematic_true_when_doc_present() -> None:
    client = FakeClient(responses_by_cmd={GetOpenDocuments: [_docs_response(["a.kicad_sch"])]})
    assert _has_open_schematic(kicad_factory=lambda: client) is True
    command, _ = client.sent[0]
    assert isinstance(command, GetOpenDocuments)
    assert command.type == DocumentType.DOCTYPE_SCHEMATIC


def test_has_open_schematic_false_when_empty() -> None:
    client = FakeClient(responses_by_cmd={GetOpenDocuments: [_docs_response([])]})
    assert _has_open_schematic(kicad_factory=lambda: client) is False


def test_has_open_schematic_false_when_factory_raises() -> None:
    def boom() -> FakeClient:
        raise RuntimeError("ipc unreachable")

    assert _has_open_schematic(kicad_factory=boom) is False


def test_has_open_schematic_false_when_send_raises() -> None:
    client = FakeClient(
        raise_on=GetOpenDocuments,
        raise_with=ApiError("transport reset"),
    )
    assert _has_open_schematic(kicad_factory=lambda: client) is False


def test_has_open_schematic_default_factory_constructs_master_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    constructed: list[Any] = []

    class _SpyClient:
        def __init__(self) -> None:
            constructed.append(self)

        def send(self, command, response_cls):  # type: ignore[no-untyped-def]  # noqa: ANN201
            return _docs_response(["a.kicad_sch"])

    monkeypatch.setattr("kicad_mcp.ipc._master_client.MasterKiCadClient", _SpyClient)

    assert _has_open_schematic() is True
    assert len(constructed) == 1


# ---------------------------------------------------------------------------
# check_ipc_gate — the public probe
#
# 4-cell matrix over (has_fix × has_open_doc). Returns (False, reason)
# unless both gates pass.
# ---------------------------------------------------------------------------


def _build_factory(*, has_fix: bool, has_open_doc: bool) -> Any:
    """Factory that yields a freshly configured FakeClient on every call."""

    full_version = "10.99.0-1059-g0895df3e3c" if has_fix else "10.0.3"
    docs = ["a.kicad_sch"] if has_open_doc else []

    def factory() -> FakeClient:
        return FakeClient(
            responses_by_cmd={
                GetVersion: [_version_response(full_version)],
                GetOpenDocuments: [_docs_response(docs)],
            }
        )

    return factory


def test_check_gate_ok_when_both_gates_pass() -> None:
    factory = _build_factory(has_fix=True, has_open_doc=True)
    ok, reason = check_ipc_gate(kicad_factory=factory)
    assert ok is True
    assert reason == ""


def test_check_gate_false_when_version_lacks_fix() -> None:
    factory = _build_factory(has_fix=False, has_open_doc=True)
    ok, reason = check_ipc_gate(kicad_factory=factory)
    assert ok is False
    assert "fix" in reason.lower() or "version" in reason.lower()


def test_check_gate_false_when_no_open_schematic() -> None:
    factory = _build_factory(has_fix=True, has_open_doc=False)
    ok, reason = check_ipc_gate(kicad_factory=factory)
    assert ok is False
    assert "schematic" in reason.lower() and "open" in reason.lower()


def test_check_gate_version_failure_short_circuits_before_doc_probe() -> None:
    """When the version probe fails, we must NOT also probe for documents."""

    sent_kinds: list[type] = []

    def factory() -> FakeClient:
        client = FakeClient(
            responses_by_cmd={
                GetVersion: [_version_response("10.0.3")],  # lacks fix
                GetOpenDocuments: [_docs_response(["a.kicad_sch"])],
            }
        )
        # Wrap send so we can capture command types.
        original_send = client.send

        def _record_send(command, response_cls):  # type: ignore[no-untyped-def]  # noqa: ANN202
            sent_kinds.append(type(command))
            return original_send(command, response_cls)

        client.send = _record_send  # type: ignore[method-assign]
        return client

    ok, _ = check_ipc_gate(kicad_factory=factory)
    assert ok is False
    assert GetVersion in sent_kinds
    assert GetOpenDocuments not in sent_kinds


# ---------------------------------------------------------------------------
# Proto builders
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "builder,proto_cls",
    [
        (build_global_label_proto, GlobalLabel),
        (build_local_label_proto, LocalLabel),
        (build_hierarchical_label_proto, HierarchicalLabel),
    ],
)
def test_label_builders_produce_master_shape(builder: Any, proto_cls: type[Any]) -> None:
    proto = builder(10.0, 20.0, "NET1")
    assert isinstance(proto, proto_cls)
    assert proto.text.text == "NET1"
    assert proto.position.x_nm == 10_000_000
    assert proto.position.y_nm == 20_000_000
    assert proto.text.position.x_nm == 10_000_000
    assert proto.text.position.y_nm == 20_000_000
    assert proto.text.attributes.size.x_nm == 1_270_000
    assert proto.text.attributes.size.y_nm == 1_270_000


def test_build_wire_proto_has_correct_endpoints_and_type() -> None:
    proto = build_wire_proto(0.0, 0.0, 2.54, 5.08)
    assert isinstance(proto, SchematicLine)
    assert proto.start.x_nm == 0
    assert proto.start.y_nm == 0
    assert proto.end.x_nm == 2_540_000
    assert proto.end.y_nm == 5_080_000
    assert proto.type == SchematicLineType.SLT_WIRE


@pytest.mark.parametrize(
    "x_mm,y_mm,expected_nm",
    [
        ((0.0, 0.0), (0.0, 0.0), (0, 0, 0, 0)),
        ((1.0, 1.0), (2.0, 2.0), (1_000_000, 1_000_000, 2_000_000, 2_000_000)),
        ((100.8, 50.4), (0.0, 0.0), (100_800_000, 50_400_000, 0, 0)),
        ((-2.5, -1.25), (-5.0, -6.25), (-2_500_000, -1_250_000, -5_000_000, -6_250_000)),
    ],
)
def test_build_wire_proto_coord_roundtrip(
    x_mm: tuple[float, float],
    y_mm: tuple[float, float],
    expected_nm: tuple[int, int, int, int],
) -> None:
    x1, y1 = x_mm
    x2, y2 = y_mm
    proto = build_wire_proto(x1, y1, x2, y2)
    assert proto.start.x_nm == expected_nm[0]
    assert proto.start.y_nm == expected_nm[1]
    assert proto.end.x_nm == expected_nm[2]
    assert proto.end.y_nm == expected_nm[3]


# ---------------------------------------------------------------------------
# route_schematic_create — IPC-only contract
# ---------------------------------------------------------------------------


def test_route_raises_when_version_lacks_fix() -> None:
    """Gate closed because of stable KiCad -> SchematicIPCRequiredError."""

    factory = _build_factory(has_fix=False, has_open_doc=True)
    proto = build_wire_proto(0.0, 0.0, 2.54, 0.0)

    with pytest.raises(SchematicIPCRequiredError) as excinfo:
        route_schematic_create([proto], kicad_factory=factory)

    assert "fix" in excinfo.value.reason.lower() or "version" in excinfo.value.reason.lower()


def test_route_raises_when_no_schematic_open() -> None:
    """Gate closed because no doc open -> SchematicIPCRequiredError."""

    factory = _build_factory(has_fix=True, has_open_doc=False)
    proto = build_wire_proto(0.0, 0.0, 2.54, 0.0)

    with pytest.raises(SchematicIPCRequiredError) as excinfo:
        route_schematic_create([proto], kicad_factory=factory)

    assert "schematic" in excinfo.value.reason.lower()


def test_route_dispatches_ipc_when_gate_permits() -> None:
    """Full gate-pass: master version + schematic open -> IPC."""

    create_response = _ok_create_response()
    client = FakeClient(
        responses_by_cmd={
            GetVersion: [_version_response("10.99.0-1059-g0895df3e3c")],
            GetOpenDocuments: [
                # First call: gate's _has_open_schematic probe.
                _docs_response(["a.kicad_sch"]),
                # Second call: _open_schematic_for_ipc.
                _docs_response(["a.kicad_sch"]),
            ],
            CreateItems: [create_response],
        }
    )

    proto = build_wire_proto(0.0, 0.0, 2.54, 0.0)
    result = route_schematic_create([proto], kicad_factory=lambda: client)

    assert isinstance(result, str)
    assert "via IPC" in result
    assert SCH_IPC_PERSISTENCE_HINT in result
    assert "sch_save()" in result


def test_route_returns_item_count_in_message() -> None:
    """The IPC success message includes the count of items created."""

    create_response = _ok_create_response()
    second = ItemCreationResult()
    second.status.code = ItemStatusCode.ISC_OK
    any_item = MasterAny()
    any_item.Pack(GlobalLabel())
    second.item.CopyFrom(any_item)
    create_response.created_items.append(second)

    client = FakeClient(
        responses_by_cmd={
            GetVersion: [_version_response("10.99.0-1059-g0895df3e3c")],
            GetOpenDocuments: [
                _docs_response(["a.kicad_sch"]),
                _docs_response(["a.kicad_sch"]),
            ],
            CreateItems: [create_response],
        }
    )

    result = route_schematic_create(
        [build_wire_proto(0, 0, 1, 1), build_wire_proto(0, 0, 2, 2)],
        kicad_factory=lambda: client,
    )

    assert isinstance(result, str)
    assert "2" in result


# ---------------------------------------------------------------------------
# _open_schematic_for_ipc helper
# ---------------------------------------------------------------------------


def test_open_schematic_for_ipc_raises_when_no_doc() -> None:
    client = FakeClient(responses_by_cmd={GetOpenDocuments: [_docs_response([])]})
    with pytest.raises(RuntimeError, match="No schematic document"):
        runtime_gate._open_schematic_for_ipc(kicad_factory=lambda: client)


def test_open_schematic_for_ipc_returns_schematic() -> None:
    from kicad_mcp.ipc.schematic import Schematic

    client = FakeClient(responses_by_cmd={GetOpenDocuments: [_docs_response(["a.kicad_sch"])]})
    result = runtime_gate._open_schematic_for_ipc(kicad_factory=lambda: client)
    assert isinstance(result, Schematic)
    assert result.document.board_filename == "a.kicad_sch"


def test_open_schematic_for_ipc_default_factory(monkeypatch: pytest.MonkeyPatch) -> None:
    """``kicad_factory=None`` -> constructor pulls MasterKiCadClient."""

    constructed: list[Any] = []

    class _SpyClient:
        def __init__(self) -> None:
            constructed.append(self)

        def send(self, command, response_cls):  # type: ignore[no-untyped-def]  # noqa: ANN201
            return _docs_response(["a.kicad_sch"])

    monkeypatch.setattr("kicad_mcp.ipc._master_client.MasterKiCadClient", _SpyClient)

    result = runtime_gate._open_schematic_for_ipc()
    from kicad_mcp.ipc.schematic import Schematic

    assert isinstance(result, Schematic)
    assert len(constructed) == 1


# ---------------------------------------------------------------------------
# Backward-compatibility removal checks
# ---------------------------------------------------------------------------


def test_no_env_opt_in_helper_remains() -> None:
    """The opt-in env var was removed when the file-edit fallback was deleted.

    There should be no ``SCH_IPC_OPT_IN_ENV`` / ``_env_opt_in`` /
    ``should_use_ipc_for_schematic_mutation`` exports remaining on the
    module — keeping them would re-introduce silent-fallback semantics.
    """

    assert not hasattr(runtime_gate, "SCH_IPC_OPT_IN_ENV")
    assert not hasattr(runtime_gate, "_env_opt_in")
    assert not hasattr(runtime_gate, "should_use_ipc_for_schematic_mutation")


def test_schematic_ipc_required_error_carries_reason() -> None:
    err = SchematicIPCRequiredError("anything went wrong")
    assert err.reason == "anything went wrong"
    assert "anything went wrong" in str(err)
