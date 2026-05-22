# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
"""IPC client for eeschema schematic editing.

This module provides :class:`Schematic`, a 1:1 analogue of
:class:`kipy.board.Board` for schematic documents. The shape of the API
mirrors ``Board`` deliberately so callers that already understand the PCB
wrappers can transfer the same mental model to schematic edits.

Compatibility
-------------

The KiCad C++ handler that backs these mutation calls landed in upstream
commit ``3dca4e0e38`` ("API: implement schematic item creation", Jon Evans,
2026-04-07) and is currently only available on the ``master`` branch.

**Against KiCad 10.0.1, 10.0.2, and 10.0.3 stable releases, every
mutation call in this module will crash eeschema.** The crash is
observable via ``scripts/sch_ipc_sanity.py`` — the input-validation path
in ``api_handler_sch.cpp::validateDocumentInternal`` is a TODO stub in
those releases, so malformed-looking requests are not rejected gracefully.

The MCP server layer (not this module) is responsible for gating these
calls at runtime based on the connected KiCad's version. This module just
builds the right protobufs and shuttles them through the IPC client.

Why we built this on top of :mod:`kipy` instead of forking it: the
:class:`kipy.client.KiCadClient` already gives us a fully functional
transport and proto stubs. The gap is purely at the convenience layer.
Forking kipy would create a maintenance burden every time upstream ships a
new release; layering keeps us synchronised for free.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from google.protobuf.empty_pb2 import Empty  # type: ignore[import-untyped]
from google.protobuf.message import Message  # type: ignore[import-untyped]
from kipy.client import ApiError, KiCadClient  # type: ignore[attr-defined]
from kipy.common_types import Commit
from kipy.geometry import Vector2
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
from kipy.proto.common.types import (
    KIID,
    DocumentSpecifier,
    DocumentType,
)
from kipy.proto.schematic.schematic_types_pb2 import (
    GlobalLabel,
    HierarchicalLabel,
    Line,
    LocalLabel,
    SchematicLayer,
)
from kipy.util import pack_any  # type: ignore[attr-defined]

if TYPE_CHECKING:
    from kipy.kicad import KiCad


# ---------------------------------------------------------------------------
# Defensive proto-feature detection.
#
# The installed ``kipy`` (and even today's upstream master) defines the
# ``SchematicLayer`` enum with only ``SL_UNKNOWN``. The docstring on
# ``Line.layer`` advertises ``LAYER_WIRE`` / ``LAYER_BUS`` / ``LAYER_NOTES``
# but those values have not been added to the proto. We resolve them at
# import time so that as soon as a future kipy ships the values, this module
# uses them; until then we fall back to ``SL_UNKNOWN``.
#
# Similarly, ``Junction`` and ``NoConnect`` proto messages are referenced in
# the C++ handler's allow-list (SCH_JUNCTION_T, SCH_NO_CONNECT_T) but do not
# yet exist on the Python side. We probe for them and surface a clear
# NotImplementedError if the caller tries to use them on an older kipy.
# ---------------------------------------------------------------------------

_LAYER_WIRE = getattr(SchematicLayer, "LAYER_WIRE", SchematicLayer.SL_UNKNOWN)

try:  # pragma: no cover - exercised indirectly through monkeypatching in tests
    from kipy.proto.schematic.schematic_types_pb2 import (  # type: ignore[attr-defined]
        Junction as _JunctionProto,
    )
except ImportError:  # pragma: no cover - depends on installed kipy version
    _JunctionProto = None

try:  # pragma: no cover - same rationale as above
    from kipy.proto.schematic.schematic_types_pb2 import (  # type: ignore[attr-defined]
        NoConnect as _NoConnectProto,
    )
except ImportError:  # pragma: no cover - depends on installed kipy version
    _NoConnectProto = None


def _require_schematic_response(response: CreateItemsResponse | UpdateItemsResponse) -> None:
    """Raise :class:`ApiError` if any per-item status is not OK.

    The transport layer (:meth:`kipy.client.KiCadClient.send`) already
    raises on transport-level errors and on a non-OK :class:`ApiStatusCode`.
    What it does *not* check is the per-item :class:`ItemStatus` payload
    embedded inside ``CreateItemsResponse`` / ``UpdateItemsResponse`` — a
    request can succeed as a whole while individual items fail. We surface
    those failures so callers do not silently swallow a bad write.
    """

    items: list[ItemCreationResult] | list[ItemUpdateResult]
    if isinstance(response, CreateItemsResponse):
        items = list(response.created_items)
    else:
        items = list(response.updated_items)

    for entry in items:
        if entry.status.code != ItemStatusCode.ISC_OK:
            message = entry.status.error_message or "(no message)"
            raise ApiError(
                f"KiCad rejected schematic item: {message}",
                raw_message=message,
            )


def _kiid_from_any(packed: object) -> KIID:
    """Extract the KIID from a packed proto returned by the server.

    The server returns each created item as a ``google.protobuf.Any``
    wrapping the concrete proto (GlobalLabel, Line, etc). Every schematic
    item proto carries an ``id`` field of type KIID, so we unpack the Any
    into a fresh instance and read it off.
    """

    # The packed proto always has a ``type_url``. Inspect it to choose the
    # right destination type. ``pack_any`` does this on the way in; on the
    # way out we lazily route based on the URL suffix.
    if not isinstance(packed, Message):
        # ``ItemCreationResult.item`` is an ``Any``, which is a Message
        # subclass; this branch is defensive.
        raise ApiError("Schematic IPC returned a non-message item payload")

    type_url = getattr(packed, "type_url", "")
    # The Any type carries a ``type_url`` attribute even though the
    # checker can't always infer that. Map known URL suffixes to types.
    suffix = type_url.rsplit("/", 1)[-1] if type_url else ""

    target: Message | None = None
    if suffix == "kiapi.schematic.types.GlobalLabel":
        target = GlobalLabel()
    elif suffix == "kiapi.schematic.types.LocalLabel":
        target = LocalLabel()
    elif suffix == "kiapi.schematic.types.HierarchicalLabel":
        target = HierarchicalLabel()
    elif suffix == "kiapi.schematic.types.Line":
        target = Line()
    elif _JunctionProto is not None and suffix == "kiapi.schematic.types.Junction":
        target = _JunctionProto()
    elif _NoConnectProto is not None and suffix == "kiapi.schematic.types.NoConnect":
        target = _NoConnectProto()
    else:
        raise ApiError(
            f"Unrecognised schematic item type returned by KiCad: {type_url!r}",
            raw_message=type_url,
        )

    # ``Any.Unpack`` writes the inner proto into ``target`` and returns a
    # bool indicating whether the type_url matched. We already filtered by
    # suffix above, so a False here is a real error.
    if not packed.Unpack(target):
        raise ApiError(
            f"Failed to unpack {type_url!r} from schematic IPC response",
            raw_message=type_url,
        )

    return cast(KIID, target.id)


class Schematic:
    """Represents an open schematic (``.kicad_sch``) document in KiCad.

    Mirrors the public surface of :class:`kipy.board.Board` so that code
    targeting both surfaces can share style and patterns.

    The methods on this class build proto messages and dispatch them via
    :meth:`kipy.client.KiCadClient.send`. The transport raises
    :class:`kipy.client.ApiError` on non-OK responses; the convenience
    helpers additionally surface per-item failures as :class:`ApiError`.
    """

    def __init__(self, kicad: KiCad, document: DocumentSpecifier) -> None:
        self._kicad = kicad
        self._doc = document

    def __repr__(self) -> str:
        return f"Schematic(filename={self.name!r})"

    # ------------------------------------------------------------------
    # Read-only accessors mirroring Board
    # ------------------------------------------------------------------

    @property
    def client(self) -> KiCadClient:
        """The KiCad client used to communicate with the API server."""

        # ``kipy.KiCad`` keeps the client on a private attribute. Access it
        # the same way :class:`kipy.board.Board` does internally so we stay
        # in lockstep with kipy's conventions.
        return self._kicad._client  # noqa: SLF001 - mirror Board's pattern

    @property
    def document(self) -> DocumentSpecifier:
        """The document specifier for the schematic."""

        return self._doc

    @property
    def name(self) -> str:
        """Returns the file name of the schematic document.

        The installed kipy ``DocumentSpecifier`` proto exposes a single
        ``board_filename`` oneof slot which eeschema reuses for schematic
        documents. Future kipy versions may add a ``schematic_filename``
        accessor (master kicad already populates it that way in C++), but
        until kipy ships that proto we read the original field.
        """

        return self._doc.board_filename

    # ------------------------------------------------------------------
    # Document-level commands
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Persist the schematic to disk via IPC."""

        command = SaveDocument()
        command.document.CopyFrom(self._doc)
        self.client.send(command, Empty)

    def begin_commit(self) -> Commit:
        """Begin a transaction that groups subsequent mutations into one undo step.

        See :meth:`kipy.board.Board.begin_commit` for the full semantic
        contract; the schematic side behaves identically.
        """

        command = BeginCommit()
        response = self.client.send(command, BeginCommitResponse)
        return Commit(response.id)

    def push_commit(self, commit: Commit, message: str = "") -> None:
        """Finalise an open transaction, applying its changes."""

        command = EndCommit()
        command.id.CopyFrom(commit.id)
        command.action = CommitAction.CMA_COMMIT
        command.message = message
        self.client.send(command, EndCommitResponse)

    def drop_commit(self, commit: Commit) -> None:
        """Cancel an open transaction, discarding any pending changes."""

        command = EndCommit()
        command.id.CopyFrom(commit.id)
        command.action = CommitAction.CMA_DROP
        self.client.send(command, EndCommitResponse)

    # ------------------------------------------------------------------
    # Generic create / update mutation surface
    # ------------------------------------------------------------------

    def create_items(self, items: list[Message]) -> list[ItemCreationResult]:
        """Send a batch of pre-built schematic proto messages to KiCad.

        Use this when the convenience wrappers below are not enough — for
        example when the caller already has a fully populated proto built
        elsewhere. Returns the per-item creation results, including the
        server-assigned KIIDs.

        Raises :class:`ApiError` if any per-item status is non-OK.
        """

        command = CreateItems()
        command.header.document.CopyFrom(self._doc)
        for item in items:
            command.items.append(pack_any(item))

        response = self.client.send(command, CreateItemsResponse)
        _require_schematic_response(response)
        return list(response.created_items)

    def update_items(self, items: list[Message]) -> list[ItemUpdateResult]:
        """Update existing schematic items by KIID.

        The items must already exist on the document; matching is done by
        the KIID carried inside each proto. Returns the updated items,
        which may differ from the input if the server clamped any values.

        Raises :class:`ApiError` if any per-item status is non-OK.
        """

        command = UpdateItems()
        command.header.document.CopyFrom(self._doc)
        for item in items:
            command.items.append(pack_any(item))

        response = self.client.send(command, UpdateItemsResponse)
        _require_schematic_response(response)
        return list(response.updated_items)

    # ------------------------------------------------------------------
    # Convenience wrappers for the most common schematic items
    # ------------------------------------------------------------------

    def _create_single(self, item: Message) -> KIID:
        """Helper: send a single item and extract its assigned KIID."""

        results = self.create_items([item])
        if not results:
            raise ApiError("KiCad returned no created item for schematic create call")
        return _kiid_from_any(results[0].item)

    def add_global_label(self, x_mm: float, y_mm: float, text: str) -> KIID:
        """Add a global label at ``(x_mm, y_mm)`` carrying ``text``."""

        label = GlobalLabel()
        position = Vector2.from_xy_mm(x_mm, y_mm)
        label.position.CopyFrom(position.proto)
        label.text.text.text = text
        return self._create_single(label)

    def add_local_label(self, x_mm: float, y_mm: float, text: str) -> KIID:
        """Add a local (net-name) label at ``(x_mm, y_mm)`` carrying ``text``."""

        label = LocalLabel()
        position = Vector2.from_xy_mm(x_mm, y_mm)
        label.position.CopyFrom(position.proto)
        label.text.text.text = text
        return self._create_single(label)

    def add_hierarchical_label(self, x_mm: float, y_mm: float, text: str) -> KIID:
        """Add a hierarchical label at ``(x_mm, y_mm)`` carrying ``text``."""

        label = HierarchicalLabel()
        position = Vector2.from_xy_mm(x_mm, y_mm)
        label.position.CopyFrom(position.proto)
        label.text.text.text = text
        return self._create_single(label)

    def add_wire(
        self,
        x1_mm: float,
        y1_mm: float,
        x2_mm: float,
        y2_mm: float,
    ) -> KIID:
        """Add a wire segment between ``(x1_mm, y1_mm)`` and ``(x2_mm, y2_mm)``.

        The proto layer for a wire is ``LAYER_WIRE``. The installed kipy
        does not yet ship that enum value; in that case we set
        :attr:`Line.layer` to ``SL_UNKNOWN`` and trust the server-side
        handler to interpret a Line on a schematic as a wire. As soon as
        kipy ships the new enum value, this code switches over
        automatically.
        """

        line = Line()
        start = Vector2.from_xy_mm(x1_mm, y1_mm)
        end = Vector2.from_xy_mm(x2_mm, y2_mm)
        line.start.CopyFrom(start.proto)
        line.end.CopyFrom(end.proto)
        line.layer = cast(SchematicLayer.ValueType, _LAYER_WIRE)
        return self._create_single(line)

    def add_junction(self, x_mm: float, y_mm: float) -> KIID:
        """Add a junction dot at ``(x_mm, y_mm)``.

        The ``Junction`` proto message is not yet present in the installed
        kipy distribution but is in the upstream C++ allow-list. We probe
        for it at import time; if absent, we raise
        :class:`NotImplementedError` with a hint that points operators at
        the kipy version requirement.
        """

        if _JunctionProto is None:
            raise NotImplementedError(
                "Schematic.add_junction requires a kipy build that ships the "
                "Junction proto message (not present in the installed kipy)."
            )

        junction = _JunctionProto()
        position = Vector2.from_xy_mm(x_mm, y_mm)
        # The Junction proto in master mirrors LocalLabel's shape: an ``id``
        # KIID and a ``position`` Vector2. Set just the position and let
        # the server assign the KIID.
        junction.position.CopyFrom(position.proto)
        return self._create_single(junction)

    def add_no_connect(self, x_mm: float, y_mm: float) -> KIID:
        """Add a no-connect marker at ``(x_mm, y_mm)``.

        See :meth:`add_junction` for the same compatibility caveat.
        """

        if _NoConnectProto is None:
            raise NotImplementedError(
                "Schematic.add_no_connect requires a kipy build that ships "
                "the NoConnect proto message (not present in the installed "
                "kipy)."
            )

        no_connect = _NoConnectProto()
        position = Vector2.from_xy_mm(x_mm, y_mm)
        no_connect.position.CopyFrom(position.proto)
        return self._create_single(no_connect)


def open_schematic(kicad: KiCad) -> Schematic:
    """Return a :class:`Schematic` wrapping the first open schematic document.

    Raises :class:`ApiError` if no schematic document is currently open in
    eeschema. The error message intentionally points at eeschema rather
    than the API socket, since the most common cause is the user opening
    the project in kicad.exe without launching eeschema itself.
    """

    documents = list(kicad.get_open_documents(DocumentType.DOCTYPE_SCHEMATIC))
    if not documents:
        raise ApiError(
            "No schematic document is open in eeschema. Open one before calling open_schematic()."
        )
    return Schematic(kicad, documents[0])
