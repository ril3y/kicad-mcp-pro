# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportArgumentType=false
# pyright: reportPrivateUsage=false
"""Unit tests for :mod:`kicad_mcp.ipc.schematic` against master protos.

The transport is mocked everywhere — no nanomsg socket is opened and no
KiCad process is required. The fake client captures every command sent
to ``MasterKiCadClient.send`` so we can assert wire-format correctness
on the way out, and lets us script per-call responses to exercise the
unpacking + status-check paths on the way back in.

Coverage focus:

1. **Wire-format correctness** — each ``add_*`` helper produces a master
   proto with the right shape (``GlobalLabel.text -> base_types.Text``
   directly, not the three-deep kipy layout), and the document specifier
   is copied into the request header.
2. **Coordinate fidelity** — mm-to-nm conversion via ``mm_to_nm`` is
   parametrised over edge cases (zero, integer, sub-mm fraction,
   negative).
3. **Status handling** — per-item ``ItemStatus.code != ISC_OK`` raises
   ``ApiError`` even when the transport itself succeeded.
4. **Lifecycle** — begin/push/drop_commit dispatch the right
   ``CommitAction``; ``save()`` raises ``NotImplementedError``.
5. **Discovery** — ``open_schematic`` filters by
   ``DOCTYPE_SCHEMATIC`` and raises ``ApiError`` on an empty document
   list.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
    BeginCommit,
    BeginCommitResponse,
    CommitAction,
    CreateItems,
    CreateItemsResponse,
    EndCommit,
    EndCommitResponse,
    GetOpenDocuments,
    GetOpenDocumentsResponse,
    ItemCreationResult,
    ItemStatusCode,
    ItemUpdateResult,
    UpdateItems,
    UpdateItemsResponse,
)
from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import (
    DocumentSpecifier,
    DocumentType,
)
from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
    GlobalLabel,
    HierarchicalLabel,
    Junction,
    LocalLabel,
    NoConnectMarker,
    SchematicLine,
    SchematicLineType,
)
from kicad_mcp.ipc._master_client import ApiError, MasterAny
from kicad_mcp.ipc.schematic import (
    DEFAULT_LABEL_TEXT_SIZE_NM,
    Commit,
    Schematic,
    mm_to_nm,
    open_schematic,
)

if TYPE_CHECKING:
    from google.protobuf.message import Message


# ---------------------------------------------------------------------------
# Test scaffolding
# ---------------------------------------------------------------------------


class FakeClient:
    """Minimal stand-in for :class:`MasterKiCadClient`.

    Each call to :meth:`send` records the command and returns the next
    scripted response, mirroring the upstream kipy mock pattern. We
    deliberately don't subclass ``MasterKiCadClient`` to avoid touching
    the nanomsg machinery during construction.
    """

    def __init__(
        self,
        *,
        responses: list[Message] | None = None,
        raise_on: type | tuple[type, ...] | None = None,
        raise_with: Exception | None = None,
    ) -> None:
        self.sent: list[tuple[Message, type[Message]]] = []
        self._responses = list(responses or [])
        self._raise_on = raise_on
        self._raise_with = raise_with

    def queue(self, response: Message) -> None:
        self._responses.append(response)

    def send(self, command, response_cls):  # type: ignore[no-untyped-def]  # noqa: ANN201
        self.sent.append((command, response_cls))
        if self._raise_on is not None and isinstance(command, self._raise_on):
            raise self._raise_with or ApiError("scripted failure")
        if self._responses:
            return self._responses.pop(0)
        # Zero-default response so methods that only look at the
        # *response* envelope (e.g. EndCommitResponse with no fields)
        # don't have to script anything.
        return response_cls()


def _make_doc(filename: str = "demo.kicad_sch") -> DocumentSpecifier:
    doc = DocumentSpecifier()
    doc.type = DocumentType.DOCTYPE_SCHEMATIC
    doc.board_filename = filename
    return doc


def _ok_create_response(item: Message) -> CreateItemsResponse:
    """Build a ``CreateItemsResponse`` echoing one OK-status item."""

    response = CreateItemsResponse()
    result = ItemCreationResult()
    result.status.code = ItemStatusCode.ISC_OK
    any_item = MasterAny()
    any_item.Pack(item)
    result.item.CopyFrom(any_item)
    response.created_items.append(result)
    return response


def _ok_update_response(item: Message) -> UpdateItemsResponse:
    response = UpdateItemsResponse()
    result = ItemUpdateResult()
    result.status.code = ItemStatusCode.ISC_OK
    any_item = MasterAny()
    any_item.Pack(item)
    result.item.CopyFrom(any_item)
    response.updated_items.append(result)
    return response


def _bad_create_response(error: str = "invalid type") -> CreateItemsResponse:
    response = CreateItemsResponse()
    result = ItemCreationResult()
    result.status.code = ItemStatusCode.ISC_INVALID_TYPE  # any non-OK
    result.status.error_message = error
    response.created_items.append(result)
    return response


def _bad_update_response(error: str = "wrong container") -> UpdateItemsResponse:
    response = UpdateItemsResponse()
    result = ItemUpdateResult()
    result.status.code = ItemStatusCode.ISC_INVALID_TYPE
    result.status.error_message = error
    response.updated_items.append(result)
    return response


@pytest.fixture
def doc() -> DocumentSpecifier:
    return _make_doc()


@pytest.fixture
def client() -> FakeClient:
    return FakeClient()


@pytest.fixture
def schematic(doc: DocumentSpecifier, client: FakeClient) -> Schematic:
    return Schematic(doc, client=client)


# ---------------------------------------------------------------------------
# Coordinate round-trip
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mm,expected_nm",
    [
        (0.0, 0),
        (1.0, 1_000_000),
        (2.54, 2_540_000),
        (100.8, 100_800_000),
        (50.4, 50_400_000),
        (-12.7, -12_700_000),
        (0.0005, 500),  # half micron rounds to int
    ],
)
def test_mm_to_nm_roundtrip(mm: float, expected_nm: int) -> None:
    assert mm_to_nm(mm) == expected_nm


# ---------------------------------------------------------------------------
# Schematic — properties + constructor
# ---------------------------------------------------------------------------


def test_constructor_uses_provided_client(doc: DocumentSpecifier, client: FakeClient) -> None:
    sch = Schematic(doc, client=client)
    assert sch.client is client
    assert sch.document is doc


def test_constructor_defaults_to_master_client(doc: DocumentSpecifier) -> None:
    # No client supplied -> a real MasterKiCadClient is constructed.
    # We only check the type to avoid touching nanomsg.
    from kicad_mcp.ipc._master_client import MasterKiCadClient

    sch = Schematic(doc)
    assert isinstance(sch.client, MasterKiCadClient)


def test_name_property_reads_filename(doc: DocumentSpecifier, client: FakeClient) -> None:
    sch = Schematic(doc, client=client)
    assert sch.name == "demo.kicad_sch"


# ---------------------------------------------------------------------------
# Save lifecycle
# ---------------------------------------------------------------------------


def test_save_raises_not_implemented(schematic: Schematic) -> None:
    with pytest.raises(NotImplementedError, match="SaveDocument"):
        schematic.save()


def test_save_supported_flag_is_false() -> None:
    assert Schematic.save_supported is False


# ---------------------------------------------------------------------------
# Commit lifecycle
# ---------------------------------------------------------------------------


def test_begin_commit_sends_begin_and_returns_handle(
    schematic: Schematic, client: FakeClient
) -> None:
    response = BeginCommitResponse()
    response.id.value = "11111111-2222-3333-4444-555555555555"
    client.queue(response)

    commit = schematic.begin_commit()

    assert isinstance(commit, Commit)
    assert commit.id.value == response.id.value
    assert len(client.sent) == 1
    command, response_cls = client.sent[0]
    assert isinstance(command, BeginCommit)
    assert response_cls is BeginCommitResponse


def test_push_commit_sends_end_commit_action_commit(
    schematic: Schematic, client: FakeClient
) -> None:
    commit = Commit(BeginCommitResponse().id)
    commit.id.value = "abc"

    schematic.push_commit(commit, message="my change")

    assert len(client.sent) == 1
    command, response_cls = client.sent[0]
    assert isinstance(command, EndCommit)
    assert response_cls is EndCommitResponse
    assert command.action == CommitAction.CMA_COMMIT
    assert command.message == "my change"
    assert command.id.value == "abc"


def test_push_commit_default_message_is_empty(schematic: Schematic, client: FakeClient) -> None:
    commit = Commit(BeginCommitResponse().id)
    commit.id.value = "abc"

    schematic.push_commit(commit)

    command, _ = client.sent[0]
    assert isinstance(command, EndCommit)
    assert command.message == ""


def test_drop_commit_sends_end_commit_action_drop(schematic: Schematic, client: FakeClient) -> None:
    commit = Commit(BeginCommitResponse().id)
    commit.id.value = "abc"

    schematic.drop_commit(commit)

    command, _ = client.sent[0]
    assert isinstance(command, EndCommit)
    assert command.action == CommitAction.CMA_DROP
    assert command.id.value == "abc"


# ---------------------------------------------------------------------------
# Label helpers — wire shape
#
# Master proto layout: ``label.text`` is directly a ``base_types.Text``
# proto (NOT the three-deep kipy nesting). The string lives at
# ``label.text.text``. The default text attributes (size 1.27 mm) are
# populated so eeschema doesn't render an invisible zero-height label.
# ---------------------------------------------------------------------------


def _extract_sent_item(client: FakeClient) -> Message:
    """Pull the single CreateItems out of the call log and unpack item[0]."""

    assert len(client.sent) == 1
    command, response_cls = client.sent[0]
    assert isinstance(command, CreateItems)
    assert response_cls is CreateItemsResponse
    assert len(command.items) == 1
    return command.items[0]


@pytest.mark.parametrize(
    "method_name,proto_cls",
    [
        ("add_global_label", GlobalLabel),
        ("add_local_label", LocalLabel),
        ("add_hierarchical_label", HierarchicalLabel),
    ],
)
def test_label_helpers_build_master_shape(
    schematic: Schematic,
    client: FakeClient,
    doc: DocumentSpecifier,
    method_name: str,
    proto_cls: type[Message],
) -> None:
    label = proto_cls()
    label.id.value = "ffffffff-0000-0000-0000-000000000001"
    client.queue(_ok_create_response(label))

    kiid = getattr(schematic, method_name)(12.0, 34.0, "NET_A")

    # Outgoing proto on the wire
    sent_any = _extract_sent_item(client)
    sent = proto_cls()
    assert sent_any.Unpack(sent)
    # Master is 2-deep: label.text.text holds the string directly.
    assert sent.text.text == "NET_A"
    assert sent.position.x_nm == 12_000_000
    assert sent.position.y_nm == 34_000_000
    # The inner Text proto carries its own position copy.
    assert sent.text.position.x_nm == 12_000_000
    assert sent.text.position.y_nm == 34_000_000
    # Default text size (1.27 mm in both axes) — without this eeschema
    # renders zero-height text and the label is invisible.
    assert sent.text.attributes.size.x_nm == DEFAULT_LABEL_TEXT_SIZE_NM
    assert sent.text.attributes.size.y_nm == DEFAULT_LABEL_TEXT_SIZE_NM
    assert DEFAULT_LABEL_TEXT_SIZE_NM == 1_270_000

    # Header.document is copied into the request.
    command, _ = client.sent[0]
    assert command.header.document.board_filename == doc.board_filename
    assert command.header.document.type == doc.type

    # Returned KIID echoes the server's assignment.
    assert kiid.value == "ffffffff-0000-0000-0000-000000000001"


def test_global_label_text_position_tracks_outer_position(
    schematic: Schematic, client: FakeClient
) -> None:
    label = GlobalLabel()
    label.id.value = "aaa"
    client.queue(_ok_create_response(label))

    schematic.add_global_label(99.5, 0.0, "RST")

    sent_any = _extract_sent_item(client)
    sent = GlobalLabel()
    assert sent_any.Unpack(sent)
    # Outer position and inner text position must agree — eeschema uses
    # the inner one for label placement.
    assert sent.position.x_nm == sent.text.position.x_nm == 99_500_000
    assert sent.position.y_nm == sent.text.position.y_nm == 0


# ---------------------------------------------------------------------------
# Wire helper
# ---------------------------------------------------------------------------


def test_add_wire_builds_schematic_line(schematic: Schematic, client: FakeClient) -> None:
    line_echo = SchematicLine()
    line_echo.id.value = "wire-1"
    client.queue(_ok_create_response(line_echo))

    schematic.add_wire(0.0, 0.0, 2.54, 5.08)

    sent_any = _extract_sent_item(client)
    sent = SchematicLine()
    assert sent_any.Unpack(sent)
    assert sent.start.x_nm == 0
    assert sent.start.y_nm == 0
    assert sent.end.x_nm == 2_540_000
    assert sent.end.y_nm == 5_080_000
    # The master proto field name is ``type``; the upstream pcb side
    # called it ``line_type`` in older builds, but master renamed it.
    assert sent.type == SchematicLineType.SLT_WIRE


# ---------------------------------------------------------------------------
# Junction + NoConnect
# ---------------------------------------------------------------------------


def test_add_junction_builds_junction(schematic: Schematic, client: FakeClient) -> None:
    j = Junction()
    j.id.value = "junc"
    client.queue(_ok_create_response(j))

    schematic.add_junction(7.5, 3.25)

    sent_any = _extract_sent_item(client)
    sent = Junction()
    assert sent_any.Unpack(sent)
    assert sent.position.x_nm == 7_500_000
    assert sent.position.y_nm == 3_250_000


def test_add_no_connect_builds_marker(schematic: Schematic, client: FakeClient) -> None:
    nc = NoConnectMarker()
    nc.id.value = "nc"
    client.queue(_ok_create_response(nc))

    schematic.add_no_connect(10.0, 20.0)

    sent_any = _extract_sent_item(client)
    sent = NoConnectMarker()
    assert sent_any.Unpack(sent)
    assert sent.position.x_nm == 10_000_000
    assert sent.position.y_nm == 20_000_000


# ---------------------------------------------------------------------------
# create_items / update_items — generic dispatch + status handling
# ---------------------------------------------------------------------------


def test_create_items_packs_each_into_any_and_copies_document(
    schematic: Schematic, client: FakeClient, doc: DocumentSpecifier
) -> None:
    junc_echo = Junction()
    junc_echo.id.value = "j1"
    nc_echo = NoConnectMarker()
    nc_echo.id.value = "nc1"

    response = CreateItemsResponse()
    for echo in (junc_echo, nc_echo):
        result = ItemCreationResult()
        result.status.code = ItemStatusCode.ISC_OK
        any_item = MasterAny()
        any_item.Pack(echo)
        result.item.CopyFrom(any_item)
        response.created_items.append(result)
    client.queue(response)

    j_in = Junction()
    j_in.position.x_nm = 1_000_000
    nc_in = NoConnectMarker()
    nc_in.position.x_nm = 2_000_000

    results = schematic.create_items([j_in, nc_in])

    assert len(results) == 2
    # Sent command carries both items, each Pack()ed into a MasterAny.
    command, response_cls = client.sent[0]
    assert isinstance(command, CreateItems)
    assert response_cls is CreateItemsResponse
    assert len(command.items) == 2
    assert command.header.document.board_filename == doc.board_filename
    # Verify the document is COPIED — mutating the original after the
    # send must not retroactively change the request's view.
    original_filename = doc.board_filename
    doc.board_filename = "mutated.kicad_sch"
    assert command.header.document.board_filename == original_filename


def test_create_items_raises_on_non_ok_per_item_status(
    schematic: Schematic, client: FakeClient
) -> None:
    client.queue(_bad_create_response("KiCad refused"))

    with pytest.raises(ApiError, match="KiCad refused"):
        schematic.create_items([Junction()])


def test_update_items_packs_each_into_any_and_copies_document(
    schematic: Schematic, client: FakeClient, doc: DocumentSpecifier
) -> None:
    junc_echo = Junction()
    junc_echo.id.value = "j1"
    client.queue(_ok_update_response(junc_echo))

    results = schematic.update_items([junc_echo])

    assert len(results) == 1
    command, response_cls = client.sent[0]
    assert isinstance(command, UpdateItems)
    assert response_cls is UpdateItemsResponse
    assert len(command.items) == 1
    assert command.header.document.board_filename == doc.board_filename


def test_update_items_raises_on_non_ok_per_item_status(
    schematic: Schematic, client: FakeClient
) -> None:
    client.queue(_bad_update_response("editor not in mutation mode"))

    with pytest.raises(ApiError, match="editor not in mutation mode"):
        schematic.update_items([Junction()])


def test_create_single_raises_when_response_has_no_items(
    schematic: Schematic, client: FakeClient
) -> None:
    # A response with zero items would be a server bug but the wrapper
    # must surface it as ApiError, not IndexError.
    client.queue(CreateItemsResponse())

    with pytest.raises(ApiError, match="no created item"):
        schematic.add_junction(0.0, 0.0)


def test_create_single_raises_when_unpack_fails(schematic: Schematic, client: FakeClient) -> None:
    """Server echoes a wrong-typed proto -> Unpack returns False."""

    # We Pack a Junction into the Any but ask the wrapper to add a
    # GlobalLabel; Unpack into GlobalLabel should refuse a Junction Any.
    response = CreateItemsResponse()
    result = ItemCreationResult()
    result.status.code = ItemStatusCode.ISC_OK
    any_item = MasterAny()
    any_item.Pack(Junction())
    result.item.CopyFrom(any_item)
    response.created_items.append(result)
    client.queue(response)

    with pytest.raises(ApiError, match="Could not unpack"):
        schematic.add_global_label(0.0, 0.0, "X")


# ---------------------------------------------------------------------------
# open_schematic — discovery
# ---------------------------------------------------------------------------


def test_open_schematic_returns_first_open_document() -> None:
    doc_a = _make_doc("a.kicad_sch")
    doc_b = _make_doc("b.kicad_sch")
    response = GetOpenDocumentsResponse()
    response.documents.append(doc_a)
    response.documents.append(doc_b)
    client = FakeClient(responses=[response])

    sch = open_schematic(client=client)

    assert isinstance(sch, Schematic)
    assert sch.document.board_filename == "a.kicad_sch"
    # GetOpenDocuments must filter by DOCTYPE_SCHEMATIC.
    command, response_cls = client.sent[0]
    assert isinstance(command, GetOpenDocuments)
    assert response_cls is GetOpenDocumentsResponse
    assert command.type == DocumentType.DOCTYPE_SCHEMATIC


def test_open_schematic_raises_when_no_documents() -> None:
    client = FakeClient(responses=[GetOpenDocumentsResponse()])

    with pytest.raises(ApiError, match="No schematic document"):
        open_schematic(client=client)


def test_open_schematic_uses_default_master_client_when_none() -> None:
    """No client passed -> a MasterKiCadClient is constructed for the probe.

    We don't drive the probe; constructing the client must not raise
    (it must NOT dial the socket eagerly).
    """

    from kicad_mcp.ipc._master_client import MasterKiCadClient

    # We can't actually call open_schematic() without a live socket,
    # so just confirm MasterKiCadClient() constructs cleanly.
    client = MasterKiCadClient()
    assert client.socket_path
