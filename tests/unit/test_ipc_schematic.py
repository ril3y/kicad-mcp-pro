"""Unit tests for :mod:`kicad_mcp.ipc.schematic`.

Every test in this file uses a **fake** KiCad client that captures the
proto sent over the wire and returns a scripted response. No real IPC is
performed, no socket is opened, and no KiCad process is required.

The tests focus on three concerns, in order:

1. **Wire-format correctness** — each public method has to build the right
   proto with the right fields populated, copy the document specifier
   into the request header, and dispatch through the client.
2. **Coordinate fidelity** — the convenience wrappers accept millimetres
   from callers but the proto wire format is in nanometres. We assert the
   resulting ``x_nm`` / ``y_nm`` values so a future regression here is
   caught loudly.
3. **Error surfacing** — the transport already raises on non-OK
   :class:`ApiStatusCode`; we additionally surface per-item
   :class:`ItemStatus` failures, which would otherwise be silently
   swallowed.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from google.protobuf.empty_pb2 import Empty
from google.protobuf.message import Message
from kipy.client import ApiError
from kipy.common_types import Commit
from kipy.proto.common.commands.editor_commands_pb2 import (
    BeginCommit,
    BeginCommitResponse,
    CommitAction,
    CreateItems,
    CreateItemsResponse,
    EndCommit,
    EndCommitResponse,
    ItemCreationResult,
    ItemStatusCode,
    ItemUpdateResult,
    SaveDocument,
    UpdateItems,
    UpdateItemsResponse,
)
from kipy.proto.common.types import KIID, DocumentSpecifier, DocumentType
from kipy.proto.schematic.schematic_types_pb2 import (
    GlobalLabel,
    HierarchicalLabel,
    Line,
    LocalLabel,
    SchematicLayer,
)
from kipy.util import pack_any

from kicad_mcp.ipc import schematic as schematic_module
from kicad_mcp.ipc.schematic import Schematic, open_schematic

# ---------------------------------------------------------------------------
# Test scaffolding
# ---------------------------------------------------------------------------


class FakeKiCadClient:
    """A minimal stand-in for :class:`kipy.client.KiCadClient`.

    Each call to :meth:`send` records the command and returns the next
    scripted response. We deliberately do not subclass ``KiCadClient`` to
    avoid touching any of its IPC plumbing during construction.
    """

    def __init__(self) -> None:
        self.calls: list[tuple[Message, type[Message]]] = []
        self.responses: list[Message] = []

    def queue_response(self, response: Message) -> None:
        self.responses.append(response)

    def send(self, command: Message, response_type: type[Message]) -> Message:
        self.calls.append((command, response_type))
        if not self.responses:
            raise AssertionError(
                f"FakeKiCadClient.send called with no scripted response queued; "
                f"command={type(command).__name__} expecting {response_type.__name__}"
            )
        return self.responses.pop(0)


class FakeKiCad:
    """Stand-in for :class:`kipy.kicad.KiCad` exposing the bare minimum.

    ``Schematic`` only reaches into the ``_client`` attribute (mirroring
    how :class:`kipy.board.Board` does it). For :func:`open_schematic`
    we also surface :meth:`get_open_documents`.
    """

    def __init__(
        self,
        client: FakeKiCadClient,
        documents: list[DocumentSpecifier] | None = None,
    ) -> None:
        self._client = client
        self._documents = list(documents or [])
        self.last_requested_type: int | None = None

    def get_open_documents(self, doc_type: int) -> list[DocumentSpecifier]:
        # The real API returns a ``RepeatedCompositeFieldContainer``; tests
        # don't care about that distinction — only that the type filter
        # is forwarded sensibly.
        self.last_requested_type = doc_type
        return list(self._documents)


def make_document(filename: str = "test.kicad_sch") -> DocumentSpecifier:
    """Build a DocumentSpecifier with the bits Schematic actually reads."""

    doc = DocumentSpecifier()
    doc.type = DocumentType.DOCTYPE_SCHEMATIC
    # eeschema reuses the ``board_filename`` slot for schematic docs in
    # the kipy currently shipped.
    doc.board_filename = filename
    return doc


def make_kiid(hex_value: str = "deadbeef-1234-5678-9abc-def012345678") -> KIID:
    kiid = KIID()
    kiid.value = hex_value
    return kiid


def make_create_response_for(
    item_proto: Message, *, kiid: KIID | None = None
) -> CreateItemsResponse:
    """Build a CreateItemsResponse echoing back ``item_proto`` with a fresh KIID.

    The real server fills in the KIID on the way back out; we replicate
    that here so the wrapper can extract it.
    """

    if kiid is not None:
        # Most schematic protos carry an ``id`` field of KIID type. Set it
        # via ``CopyFrom`` so we don't depend on the field's mutability.
        item_proto.id.CopyFrom(kiid)

    response = CreateItemsResponse()
    result = ItemCreationResult()
    result.status.code = ItemStatusCode.ISC_OK
    result.item.CopyFrom(pack_any(item_proto))
    response.created_items.append(result)
    return response


def make_update_response_for(item_proto: Message) -> UpdateItemsResponse:
    response = UpdateItemsResponse()
    result = ItemUpdateResult()
    result.status.code = ItemStatusCode.ISC_OK
    result.item.CopyFrom(pack_any(item_proto))
    response.updated_items.append(result)
    return response


@pytest.fixture
def doc() -> DocumentSpecifier:
    return make_document()


@pytest.fixture
def client() -> FakeKiCadClient:
    return FakeKiCadClient()


@pytest.fixture
def kicad(client: FakeKiCadClient, doc: DocumentSpecifier) -> FakeKiCad:
    return FakeKiCad(client, [doc])


@pytest.fixture
def schematic(kicad: FakeKiCad, doc: DocumentSpecifier) -> Schematic:
    return Schematic(kicad, doc)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------


def test_name_returns_board_filename(schematic: Schematic) -> None:
    # The DocumentSpecifier reuses the board_filename slot for schematic
    # docs in today's kipy, so ``name`` has to read from there.
    assert schematic.name == "test.kicad_sch"


def test_client_property_exposes_underlying_client(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    assert schematic.client is client


def test_document_property_returns_specifier(schematic: Schematic, doc: DocumentSpecifier) -> None:
    assert schematic.document is doc


def test_repr_includes_filename(schematic: Schematic) -> None:
    # Cheap regression guard: if someone refactors to printing the doc
    # proto we'd get a multi-line repr.
    assert "test.kicad_sch" in repr(schematic)


# ---------------------------------------------------------------------------
# Convenience wrappers — labels
# ---------------------------------------------------------------------------


def _assert_create_command(
    client: FakeKiCadClient,
    doc: DocumentSpecifier,
    expected_type_suffix: str,
) -> CreateItems:
    """Pull the single CreateItems out of the call log and validate the shape."""

    assert len(client.calls) == 1, f"expected 1 send(), got {len(client.calls)}"
    command, response_type = client.calls[0]
    assert isinstance(command, CreateItems)
    assert response_type is CreateItemsResponse
    # Header.document is the schematic doc, copied (not aliased).
    assert command.header.document.board_filename == doc.board_filename
    assert command.header.document.type == doc.type
    assert len(command.items) == 1
    assert command.items[0].type_url.endswith(expected_type_suffix)
    return command


def test_add_global_label_builds_correct_proto(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    expected_kiid = make_kiid("11111111-2222-3333-4444-555555555555")
    label_echo = GlobalLabel()
    label_echo.position.x_nm = 12_000_000
    label_echo.position.y_nm = 34_000_000
    label_echo.text.text.text = "VCC"
    client.queue_response(make_create_response_for(label_echo, kiid=expected_kiid))

    returned = schematic.add_global_label(12.0, 34.0, "VCC")

    command = _assert_create_command(client, doc, "kiapi.schematic.types.GlobalLabel")
    sent = GlobalLabel()
    assert command.items[0].Unpack(sent)
    # 1 mm == 1_000_000 nm
    assert sent.position.x_nm == 12_000_000
    assert sent.position.y_nm == 34_000_000
    assert sent.text.text.text == "VCC"
    assert returned.value == expected_kiid.value


def test_add_local_label_builds_correct_proto(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    expected_kiid = make_kiid("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
    label_echo = LocalLabel()
    label_echo.position.x_nm = 50_000_000
    label_echo.position.y_nm = 75_000_000
    label_echo.text.text.text = "DATA"
    client.queue_response(make_create_response_for(label_echo, kiid=expected_kiid))

    returned = schematic.add_local_label(50.0, 75.0, "DATA")

    command = _assert_create_command(client, doc, "kiapi.schematic.types.LocalLabel")
    sent = LocalLabel()
    assert command.items[0].Unpack(sent)
    assert sent.position.x_nm == 50_000_000
    assert sent.position.y_nm == 75_000_000
    assert sent.text.text.text == "DATA"
    assert returned.value == expected_kiid.value


def test_add_hierarchical_label_builds_correct_proto(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    expected_kiid = make_kiid("ffffffff-1111-2222-3333-444444444444")
    label_echo = HierarchicalLabel()
    label_echo.position.x_nm = 10_000_000
    label_echo.position.y_nm = 20_000_000
    label_echo.text.text.text = "BUS_A"
    client.queue_response(make_create_response_for(label_echo, kiid=expected_kiid))

    returned = schematic.add_hierarchical_label(10.0, 20.0, "BUS_A")

    command = _assert_create_command(client, doc, "kiapi.schematic.types.HierarchicalLabel")
    sent = HierarchicalLabel()
    assert command.items[0].Unpack(sent)
    assert sent.position.x_nm == 10_000_000
    assert sent.position.y_nm == 20_000_000
    assert sent.text.text.text == "BUS_A"
    assert returned.value == expected_kiid.value


# ---------------------------------------------------------------------------
# Convenience wrappers — geometry items
# ---------------------------------------------------------------------------


def test_add_wire_builds_line_with_wire_layer(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    expected_kiid = make_kiid("99999999-aaaa-bbbb-cccc-dddddddddddd")
    line_echo = Line()
    line_echo.start.x_nm = 1_000_000
    line_echo.start.y_nm = 2_000_000
    line_echo.end.x_nm = 3_000_000
    line_echo.end.y_nm = 4_000_000
    client.queue_response(make_create_response_for(line_echo, kiid=expected_kiid))

    returned = schematic.add_wire(1.0, 2.0, 3.0, 4.0)

    command = _assert_create_command(client, doc, "kiapi.schematic.types.Line")
    sent = Line()
    assert command.items[0].Unpack(sent)
    assert sent.start.x_nm == 1_000_000
    assert sent.start.y_nm == 2_000_000
    assert sent.end.x_nm == 3_000_000
    assert sent.end.y_nm == 4_000_000
    # Whatever value LAYER_WIRE resolves to in the installed kipy, the
    # module-level constant should be the one we use on the wire.
    assert sent.layer == schematic_module._LAYER_WIRE
    assert returned.value == expected_kiid.value


def test_add_wire_uses_layer_wire_when_kipy_ships_it(
    schematic: Schematic, client: FakeKiCadClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Today's kipy enum only has SL_UNKNOWN — the module falls back to
    # that. Once kipy ships LAYER_WIRE, the module-level _LAYER_WIRE will
    # resolve to the new value. Simulate that by monkeypatching and
    # verifying the wrapper picks up the change.
    fake_layer_value = 42
    monkeypatch.setattr(schematic_module, "_LAYER_WIRE", fake_layer_value)

    expected_kiid = make_kiid("12345678-1234-5678-1234-567812345678")
    line_echo = Line()
    client.queue_response(make_create_response_for(line_echo, kiid=expected_kiid))

    schematic.add_wire(0.0, 0.0, 1.0, 1.0)

    sent = Line()
    assert client.calls[0][0].items[0].Unpack(sent)
    assert sent.layer == fake_layer_value


def test_add_junction_raises_until_kipy_ships_proto(
    schematic: Schematic, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The installed kipy does not yet expose a Junction proto. Calling
    # ``add_junction`` should surface that gap clearly rather than
    # silently building a malformed message.
    monkeypatch.setattr(schematic_module, "_JunctionProto", None)
    with pytest.raises(NotImplementedError, match="Junction"):
        schematic.add_junction(10.0, 10.0)


def test_add_no_connect_raises_until_kipy_ships_proto(
    schematic: Schematic, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(schematic_module, "_NoConnectProto", None)
    with pytest.raises(NotImplementedError, match="NoConnect"):
        schematic.add_no_connect(10.0, 10.0)


def test_add_junction_uses_substituted_proto_when_available(
    schematic: Schematic, client: FakeKiCadClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When kipy eventually ships a Junction proto, the wrapper should
    pack it correctly. Until then, we test the dispatch path by
    substituting a stand-in proto class with the same shape (a ``position``
    field of type Vector2 and an ``id`` field of type KIID).

    We use ``LocalLabel`` as the stand-in: it already has both fields plus
    an unused ``text`` field which we tolerate.
    """

    monkeypatch.setattr(schematic_module, "_JunctionProto", LocalLabel)

    # Tell ``_kiid_from_any`` to recognise this Any URL too: patch the
    # whole helper to accept LocalLabel for the test. Easiest path: just
    # let the response come back as a LocalLabel — _kiid_from_any already
    # handles that type URL.
    expected_kiid = make_kiid("aaaaaaaa-1111-2222-3333-444444444444")
    junction_echo = LocalLabel()
    client.queue_response(make_create_response_for(junction_echo, kiid=expected_kiid))

    returned = schematic.add_junction(15.0, 25.0)

    command, _ = client.calls[0]
    assert isinstance(command, CreateItems)
    sent = LocalLabel()
    assert command.items[0].Unpack(sent)
    assert sent.position.x_nm == 15_000_000
    assert sent.position.y_nm == 25_000_000
    assert returned.value == expected_kiid.value


def test_add_no_connect_uses_substituted_proto_when_available(
    schematic: Schematic, client: FakeKiCadClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(schematic_module, "_NoConnectProto", LocalLabel)
    expected_kiid = make_kiid("bbbbbbbb-1111-2222-3333-555555555555")
    nc_echo = LocalLabel()
    client.queue_response(make_create_response_for(nc_echo, kiid=expected_kiid))

    returned = schematic.add_no_connect(7.5, 8.5)

    command, _ = client.calls[0]
    sent = LocalLabel()
    assert command.items[0].Unpack(sent)
    assert sent.position.x_nm == 7_500_000
    assert sent.position.y_nm == 8_500_000
    assert returned.value == expected_kiid.value


# ---------------------------------------------------------------------------
# Generic create_items / update_items
# ---------------------------------------------------------------------------


def test_create_items_passes_through_prebuilt_protos(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    label1 = GlobalLabel()
    label1.position.x_nm = 1
    label1.position.y_nm = 2
    label1.text.text.text = "A"
    label2 = LocalLabel()
    label2.position.x_nm = 3
    label2.position.y_nm = 4
    label2.text.text.text = "B"

    response = CreateItemsResponse()
    for src in (label1, label2):
        result = ItemCreationResult()
        result.status.code = ItemStatusCode.ISC_OK
        result.item.CopyFrom(pack_any(src))
        response.created_items.append(result)
    client.queue_response(response)

    returned = schematic.create_items([label1, label2])

    command, response_type = client.calls[0]
    assert isinstance(command, CreateItems)
    assert response_type is CreateItemsResponse
    assert command.header.document.board_filename == doc.board_filename
    assert len(command.items) == 2
    assert command.items[0].type_url.endswith("kiapi.schematic.types.GlobalLabel")
    assert command.items[1].type_url.endswith("kiapi.schematic.types.LocalLabel")
    assert len(returned) == 2
    assert all(r.status.code == ItemStatusCode.ISC_OK for r in returned)


def test_update_items_passes_through_prebuilt_protos(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    label = GlobalLabel()
    label.id.CopyFrom(make_kiid("ffeeddcc-bbaa-9988-7766-554433221100"))
    label.position.x_nm = 99
    label.text.text.text = "VCC"

    response = UpdateItemsResponse()
    result = ItemUpdateResult()
    result.status.code = ItemStatusCode.ISC_OK
    result.item.CopyFrom(pack_any(label))
    response.updated_items.append(result)
    client.queue_response(response)

    returned = schematic.update_items([label])

    command, response_type = client.calls[0]
    assert isinstance(command, UpdateItems)
    assert response_type is UpdateItemsResponse
    assert command.header.document.board_filename == doc.board_filename
    assert len(command.items) == 1
    assert len(returned) == 1


# ---------------------------------------------------------------------------
# Document-level commands
# ---------------------------------------------------------------------------


def test_save_sends_save_document_with_the_doc(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    client.queue_response(Empty())
    schematic.save()
    assert len(client.calls) == 1
    command, response_type = client.calls[0]
    assert isinstance(command, SaveDocument)
    assert response_type is Empty
    assert command.document.board_filename == doc.board_filename
    assert command.document.type == DocumentType.DOCTYPE_SCHEMATIC


def test_begin_commit_returns_commit_with_server_id(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    commit_id = make_kiid("c0c0c0c0-c0c0-c0c0-c0c0-c0c0c0c0c0c0")
    response = BeginCommitResponse()
    response.id.CopyFrom(commit_id)
    client.queue_response(response)

    commit = schematic.begin_commit()
    assert isinstance(commit, Commit)
    assert commit.id.value == commit_id.value
    command, response_type = client.calls[0]
    assert isinstance(command, BeginCommit)
    assert response_type is BeginCommitResponse


def test_push_commit_sends_end_commit_with_cma_commit(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    commit = Commit(make_kiid("11112222-3333-4444-5555-666677778888"))
    client.queue_response(EndCommitResponse())

    schematic.push_commit(commit, "added a global label")
    command, response_type = client.calls[0]
    assert isinstance(command, EndCommit)
    assert response_type is EndCommitResponse
    assert command.id.value == commit.id.value
    assert command.action == CommitAction.CMA_COMMIT
    assert command.message == "added a global label"


def test_push_commit_defaults_empty_message(schematic: Schematic, client: FakeKiCadClient) -> None:
    commit = Commit(make_kiid("00000000-1111-2222-3333-444444444444"))
    client.queue_response(EndCommitResponse())

    schematic.push_commit(commit)
    command, _ = client.calls[0]
    assert command.message == ""


def test_drop_commit_sends_end_commit_with_cma_drop(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    commit = Commit(make_kiid("99998888-7777-6666-5555-444433332222"))
    client.queue_response(EndCommitResponse())

    schematic.drop_commit(commit)
    command, response_type = client.calls[0]
    assert isinstance(command, EndCommit)
    assert response_type is EndCommitResponse
    assert command.id.value == commit.id.value
    assert command.action == CommitAction.CMA_DROP


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


def test_create_items_raises_when_per_item_status_is_not_ok(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    label = GlobalLabel()
    label.text.text.text = "X"

    response = CreateItemsResponse()
    bad = ItemCreationResult()
    bad.status.code = ItemStatusCode.ISC_INVALID_DATA
    bad.status.error_message = "off-grid coordinates"
    bad.item.CopyFrom(pack_any(label))
    response.created_items.append(bad)
    client.queue_response(response)

    with pytest.raises(ApiError, match="off-grid coordinates"):
        schematic.create_items([label])


def test_update_items_raises_when_per_item_status_is_not_ok(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    label = GlobalLabel()
    label.id.CopyFrom(make_kiid())
    label.text.text.text = "X"

    response = UpdateItemsResponse()
    bad = ItemUpdateResult()
    bad.status.code = ItemStatusCode.ISC_NONEXISTENT
    bad.status.error_message = "no such item"
    bad.item.CopyFrom(pack_any(label))
    response.updated_items.append(bad)
    client.queue_response(response)

    with pytest.raises(ApiError, match="no such item"):
        schematic.update_items([label])


def test_create_items_error_with_empty_message_uses_placeholder(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    label = GlobalLabel()
    response = CreateItemsResponse()
    bad = ItemCreationResult()
    bad.status.code = ItemStatusCode.ISC_INVALID_TYPE
    # Note: no error_message set -- still has to raise with something
    # readable for the caller to log.
    bad.item.CopyFrom(pack_any(label))
    response.created_items.append(bad)
    client.queue_response(response)

    with pytest.raises(ApiError, match="no message"):
        schematic.create_items([label])


def test_convenience_wrapper_surfaces_api_error_from_transport(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    # If the underlying KiCadClient.send raises ApiError (transport-level
    # failure such as AS_BUSY), the convenience wrapper must let that
    # propagate untouched.

    def failing_send(_command: Message, _response_type: type[Message]) -> Message:
        raise ApiError("KiCad is busy", raw_message="busy")

    client.send = failing_send  # type: ignore[assignment]
    with pytest.raises(ApiError, match="busy"):
        schematic.add_global_label(0.0, 0.0, "X")


def test_create_single_helper_raises_on_empty_results(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    # A well-formed but empty response should not silently return None.
    response = CreateItemsResponse()
    client.queue_response(response)

    with pytest.raises(ApiError, match="no created item"):
        schematic.add_global_label(0.0, 0.0, "X")


def test_kiid_from_any_raises_on_unknown_type_url(
    schematic: Schematic, client: FakeKiCadClient
) -> None:
    # If the server returns an Any with a URL we don't recognise, we want
    # a clear failure rather than a confusing AttributeError later.
    response = CreateItemsResponse()
    result = ItemCreationResult()
    result.status.code = ItemStatusCode.ISC_OK
    # Pack a totally unrelated proto so the type_url won't match any
    # schematic proto suffix the wrapper knows about.
    result.item.CopyFrom(pack_any(Empty()))
    response.created_items.append(result)
    client.queue_response(response)

    with pytest.raises(ApiError, match="Unrecognised schematic item type"):
        schematic.add_global_label(0.0, 0.0, "X")


def test_kiid_from_any_rejects_non_message_payload() -> None:
    # Defensive branch: ItemCreationResult.item is always a Message but if
    # something other than a Message ever reaches the helper we want a
    # clear ApiError rather than a confusing AttributeError on
    # ``type_url``.
    with pytest.raises(ApiError, match="non-message item payload"):
        schematic_module._kiid_from_any("not a proto")


def test_kiid_from_any_raises_when_unpack_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    # If the suffix routes to a known proto type but ``Any.Unpack``
    # returns False (e.g. corrupted bytes), we surface the failure
    # instead of returning an empty KIID.
    from google.protobuf.any_pb2 import Any as PbAny

    broken = PbAny()
    broken.type_url = "type.googleapis.com/kiapi.schematic.types.GlobalLabel"
    # Leave value empty: Unpack will succeed against an empty payload for
    # GlobalLabel, so we monkeypatch Unpack to force a False return.
    monkeypatch.setattr(PbAny, "Unpack", lambda self, target: False)

    with pytest.raises(ApiError, match="Failed to unpack"):
        schematic_module._kiid_from_any(broken)


def test_kiid_from_any_routes_junction_url(monkeypatch: pytest.MonkeyPatch) -> None:
    # When the response carries the Junction URL and _JunctionProto is
    # available, the helper must use that path. We stub _JunctionProto
    # with LocalLabel (matching shape) and craft an Any with the right
    # type_url to exercise the Junction-specific branch.
    monkeypatch.setattr(schematic_module, "_JunctionProto", LocalLabel)

    from google.protobuf.any_pb2 import Any as PbAny

    # Use LocalLabel's serialised body but rewrite the type_url to claim
    # it's a Junction. The Unpack call only checks the URL when called
    # via the message's Unpack method that takes a target proto.
    label = LocalLabel()
    label.position.x_nm = 1
    label.position.y_nm = 2
    label.id.CopyFrom(make_kiid("11111111-1111-1111-1111-111111111111"))
    packed = pack_any(label)
    packed.type_url = "type.googleapis.com/kiapi.schematic.types.Junction"

    # Patch Any.Unpack to ignore the URL mismatch and just MergeFrom the
    # bytes — this mirrors the substituted-proto case.
    original_parse = LocalLabel.ParseFromString

    def fake_unpack(self: PbAny, target: Message) -> bool:
        original_parse(target, self.value)
        return True

    monkeypatch.setattr(PbAny, "Unpack", fake_unpack)

    kiid = schematic_module._kiid_from_any(packed)
    assert kiid.value == "11111111-1111-1111-1111-111111111111"


def test_kiid_from_any_routes_no_connect_url(monkeypatch: pytest.MonkeyPatch) -> None:
    # Symmetric to the junction test above, for NoConnect.
    monkeypatch.setattr(schematic_module, "_NoConnectProto", LocalLabel)

    from google.protobuf.any_pb2 import Any as PbAny

    label = LocalLabel()
    label.id.CopyFrom(make_kiid("22222222-2222-2222-2222-222222222222"))
    packed = pack_any(label)
    packed.type_url = "type.googleapis.com/kiapi.schematic.types.NoConnect"

    original_parse = LocalLabel.ParseFromString

    def fake_unpack(self: PbAny, target: Message) -> bool:
        original_parse(target, self.value)
        return True

    monkeypatch.setattr(PbAny, "Unpack", fake_unpack)

    kiid = schematic_module._kiid_from_any(packed)
    assert kiid.value == "22222222-2222-2222-2222-222222222222"


# ---------------------------------------------------------------------------
# open_schematic entry point
# ---------------------------------------------------------------------------


def test_open_schematic_returns_first_open_document(
    client: FakeKiCadClient,
) -> None:
    doc1 = make_document("first.kicad_sch")
    doc2 = make_document("second.kicad_sch")
    kicad = FakeKiCad(client, [doc1, doc2])

    result = open_schematic(kicad)  # type: ignore[arg-type]
    assert isinstance(result, Schematic)
    assert result.name == "first.kicad_sch"
    # Confirm the type filter was applied
    assert kicad.last_requested_type == DocumentType.DOCTYPE_SCHEMATIC


def test_open_schematic_raises_when_no_document_is_open(client: FakeKiCadClient) -> None:
    kicad = FakeKiCad(client, [])
    with pytest.raises(ApiError, match="No schematic document is open"):
        open_schematic(kicad)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Coordinate fidelity edge cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("x_mm", "y_mm", "expected_x_nm", "expected_y_nm"),
    [
        (0.0, 0.0, 0, 0),
        (1.0, 1.0, 1_000_000, 1_000_000),
        (0.001, 0.001, 1_000, 1_000),
        (-50.0, -50.0, -50_000_000, -50_000_000),
        (100.8, 50.4, 100_800_000, 50_400_000),
    ],
)
def test_add_global_label_coordinate_conversion(
    schematic: Schematic,
    client: FakeKiCadClient,
    x_mm: float,
    y_mm: float,
    expected_x_nm: int,
    expected_y_nm: int,
) -> None:
    label_echo = GlobalLabel()
    client.queue_response(make_create_response_for(label_echo, kiid=make_kiid()))

    schematic.add_global_label(x_mm, y_mm, "NET")

    sent = GlobalLabel()
    assert client.calls[0][0].items[0].Unpack(sent)
    assert sent.position.x_nm == expected_x_nm
    assert sent.position.y_nm == expected_y_nm


def test_module_documents_compatibility_in_module_docstring() -> None:
    """Smoke-test that the compat warning has not been silently removed.

    The docstring is part of the contract — without it, operators may
    enable schematic IPC mutations against KiCad 10.0.x and crash
    eeschema. We assert on the key phrase so a refactor that loses it
    fails this test instead of failing in production.
    """

    assert schematic_module.__doc__ is not None
    assert "crash" in schematic_module.__doc__.lower()
    assert "master" in schematic_module.__doc__.lower()


# ---------------------------------------------------------------------------
# Light usage-shape tests
# ---------------------------------------------------------------------------


def test_create_items_with_empty_list_still_sends_command(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    # The Board equivalent skips the send when items is empty; the
    # schematic wrapper currently does NOT — we lean toward making the
    # behaviour explicit (the server still ack's the empty request).
    # Lock that in so a future refactor is intentional.
    response = CreateItemsResponse()
    client.queue_response(response)

    result = schematic.create_items([])
    assert result == []
    command, _ = client.calls[0]
    assert isinstance(command, CreateItems)
    assert command.header.document.board_filename == doc.board_filename
    assert len(command.items) == 0


def test_update_items_with_empty_list_still_sends_command(
    schematic: Schematic, client: FakeKiCadClient, doc: DocumentSpecifier
) -> None:
    response = UpdateItemsResponse()
    client.queue_response(response)

    result = schematic.update_items([])
    assert result == []
    command, _ = client.calls[0]
    assert isinstance(command, UpdateItems)
    assert command.header.document.board_filename == doc.board_filename


def test_module_schematic_layer_constant_is_consistent() -> None:
    # Either the installed kipy ships LAYER_WIRE (then _LAYER_WIRE is
    # that value), or it doesn't (then _LAYER_WIRE falls back to
    # SL_UNKNOWN). Both are legal; we just want a sanity check that the
    # fallback ladder produces a SchematicLayer-valid integer.
    value = schematic_module._LAYER_WIRE
    valid_values = set(SchematicLayer.values())
    # ``getattr`` fallback may produce a value outside the enum if a
    # forward-compat addition has not yet been mapped — accept that too
    # since the server will validate.
    assert isinstance(value, int)
    assert value == SchematicLayer.SL_UNKNOWN or value in valid_values


def test_fake_client_records_response_type(schematic: Schematic, client: FakeKiCadClient) -> None:
    # Defensive: assert the wrapper passes the correct response_type
    # through, since the transport relies on it to know what message to
    # unpack into.
    client.queue_response(Empty())
    schematic.save()
    _, response_type = client.calls[0]
    assert response_type is Empty


def test_magic_mock_can_substitute_for_kicad(client: FakeKiCadClient) -> None:
    # Confirm that the Schematic class doesn't require a real ``KiCad``
    # instance — a duck-typed MagicMock with ``_client`` works too. This
    # is the shape MCP integration tests will hit.
    fake = MagicMock()
    fake._client = client
    doc = make_document("mock.kicad_sch")
    sch = Schematic(fake, doc)
    assert sch.client is client
    assert sch.name == "mock.kicad_sch"
