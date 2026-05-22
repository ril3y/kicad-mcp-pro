# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
"""IPC client for eeschema schematic editing — master-proto edition.

Talks to eeschema via the IPC `CreateItems` / `UpdateItems` / `SaveDocument`
flow using the *master KiCad* proto field layouts. Vendored stubs live in
:mod:`kicad_mcp._master_proto` (regenerated from
`X:/Projects/kicad-source/api/proto/` against master).

Why we don't reuse :mod:`kipy`
-----------------------------

kipy 0.7.1 ships older schematic proto stubs whose field shape doesn't
match KiCad master's wire format:

* kipy: ``GlobalLabel.text -> schematic_types.Text -> base_types.Text``
  (three-deep nesting; the inner ``text`` string field is at
  ``label.text.text.text``).
* master: ``GlobalLabel.text -> base_types.Text`` directly (two-deep;
  the text string field is at ``label.text.text``).

When kipy's proto descriptors are loaded into the global protobuf
descriptor pool, our master-aligned stubs can't co-exist (duplicate
file name registration). So this module talks to KiCad via its own
nanomsg transport (:class:`_master_client.MasterKiCadClient`) and
imports only the master stubs. No ``import kipy`` anywhere in this
file or its transitive callers.

Compatibility
-------------

This works against KiCad master (or any release containing
``3dca4e0e38`` "API: implement schematic item creation" + the April
2026 schematic serialization follow-ups). Stable releases 10.0.x
through 10.0.3 either crash on input or return empty items. The
:mod:`kicad_mcp.ipc.runtime_gate` gates calls to this module so
the MCP tools never invoke it against a non-master eeschema.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

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
    KIID,
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
from kicad_mcp.ipc._master_client import ApiError, MasterKiCadClient

if TYPE_CHECKING:
    from google.protobuf.message import Message  # type: ignore[import-untyped]


# Default text size for new labels — 1.27mm × 1.27mm, matches KiCad's
# GUI default for new labels. Without explicit attributes, eeschema
# renders zero-size text (invisible).
DEFAULT_LABEL_TEXT_SIZE_NM = 1_270_000


def mm_to_nm(value_mm: float) -> int:
    return int(round(value_mm * 1_000_000))


def _require_item_status(
    response: CreateItemsResponse | UpdateItemsResponse,
) -> None:
    """Raise :class:`ApiError` if any per-item status is not OK.

    The transport already raises on ApiStatusCode failures, but per-
    item :class:`ItemStatus` payloads inside the response can still
    indicate trouble (invalid type, wrong container, etc.).
    """
    for result in _iter_results(response):
        if result.status.code != ItemStatusCode.ISC_OK:
            raise ApiError(
                f"KiCad rejected schematic item: {result.status.error_message}",
                status_code=int(result.status.code),
                raw_message=result.status.error_message,
            )


def _iter_results(
    response: CreateItemsResponse | UpdateItemsResponse,
) -> list[ItemCreationResult] | list[ItemUpdateResult]:
    # CreateItems and UpdateItems use slightly different field names
    # for the per-item result list. Accept either.
    if isinstance(response, CreateItemsResponse):
        return list(response.created_items)
    return list(response.updated_items)


class Commit:
    """Lightweight Commit handle.

    Mirrors :class:`kipy.common_types.Commit` so callers can treat
    schematic commits the same way they treat board commits.
    """

    __slots__ = ("id",)

    def __init__(self, kiid: KIID) -> None:
        self.id = kiid


class Schematic:
    """Open schematic document accessible via IPC.

    Mirrors the public surface of :class:`kipy.board.Board` for
    schematic items. Uses master proto stubs and a self-contained
    nanomsg transport — no kipy dependency.
    """

    def __init__(
        self,
        document: DocumentSpecifier,
        *,
        client: MasterKiCadClient | None = None,
    ) -> None:
        self._client = client or MasterKiCadClient()
        self._doc = document

    @property
    def client(self) -> MasterKiCadClient:
        return self._client

    @property
    def document(self) -> DocumentSpecifier:
        return self._doc

    @property
    def name(self) -> str:
        return self._doc.board_filename

    # ----- save / commit lifecycle -----

    def save(self) -> None:
        """Save not supported via IPC against master.

        Master's editor_commands.proto removed the explicit
        ``SaveDocument`` message (line 53 is commented). The user must
        Ctrl-S in eeschema, OR we rely on the user's persistence flow.
        Provided as a no-op stub for API compatibility with the
        previous kipy-backed wrapper; callers should check
        ``schematic.save_supported`` before invoking.
        """
        raise NotImplementedError(
            "SaveDocument is not part of master KiCad's IPC. Save manually in eeschema (Ctrl-S)."
        )

    save_supported: bool = False

    def begin_commit(self) -> Commit:
        command = BeginCommit()
        response = self._client.send(command, BeginCommitResponse)
        return Commit(response.id)

    def push_commit(self, commit: Commit, message: str = "") -> None:
        command = EndCommit()
        command.id.CopyFrom(commit.id)
        command.action = CommitAction.CMA_COMMIT
        command.message = message
        self._client.send(command, EndCommitResponse)

    def drop_commit(self, commit: Commit) -> None:
        command = EndCommit()
        command.id.CopyFrom(commit.id)
        command.action = CommitAction.CMA_DROP
        self._client.send(command, EndCommitResponse)

    # ----- generic mutation -----

    def create_items(self, items: list[Message]) -> list[ItemCreationResult]:
        from kicad_mcp.ipc._master_client import MasterAny as Any  # noqa

        command = CreateItems()
        command.header.document.CopyFrom(self._doc)
        for item in items:
            any_item = Any()
            any_item.Pack(item)
            command.items.append(any_item)
        response = self._client.send(command, CreateItemsResponse)
        _require_item_status(response)
        return list(response.created_items)

    def update_items(self, items: list[Message]) -> list[ItemUpdateResult]:
        from kicad_mcp.ipc._master_client import MasterAny as Any  # noqa

        command = UpdateItems()
        command.header.document.CopyFrom(self._doc)
        for item in items:
            any_item = Any()
            any_item.Pack(item)
            command.items.append(any_item)
        response = self._client.send(command, UpdateItemsResponse)
        _require_item_status(response)
        return list(response.updated_items)

    # ----- helpers -----

    def _create_single(self, item: Message) -> KIID:
        results = self.create_items([item])
        if not results:
            raise ApiError("KiCad returned no created item")
        from kicad_mcp.ipc._master_client import MasterAny as Any  # noqa

        # Unpack the response into the same proto type so we can read
        # the assigned KIID back.
        target_cls = type(item)
        unpacked = target_cls()
        any_msg = cast(Any, results[0].item)
        if not any_msg.Unpack(unpacked):
            raise ApiError("Could not unpack item from CreateItems response")
        return unpacked.id  # type: ignore[no-any-return]

    def _populate_label_text(
        self,
        label: GlobalLabel | LocalLabel | HierarchicalLabel,
        x_mm: float,
        y_mm: float,
        text: str,
    ) -> None:
        """Set position + inner text string + sane text attributes.

        Master's proto layout: ``label.text`` is directly a
        ``base_types.Text`` proto (not wrapped). The string lives at
        ``label.text.text``. Without explicit ``attributes.size``
        eeschema renders zero-height text (invisible).
        """
        x_nm = mm_to_nm(x_mm)
        y_nm = mm_to_nm(y_mm)
        label.position.x_nm = x_nm
        label.position.y_nm = y_nm
        label.text.text = text
        label.text.position.x_nm = x_nm
        label.text.position.y_nm = y_nm
        label.text.attributes.size.x_nm = DEFAULT_LABEL_TEXT_SIZE_NM
        label.text.attributes.size.y_nm = DEFAULT_LABEL_TEXT_SIZE_NM

    # ----- typed convenience wrappers -----

    def add_global_label(self, x_mm: float, y_mm: float, text: str) -> KIID:
        label = GlobalLabel()
        self._populate_label_text(label, x_mm, y_mm, text)
        return self._create_single(label)

    def add_local_label(self, x_mm: float, y_mm: float, text: str) -> KIID:
        label = LocalLabel()
        self._populate_label_text(label, x_mm, y_mm, text)
        return self._create_single(label)

    def add_hierarchical_label(self, x_mm: float, y_mm: float, text: str) -> KIID:
        label = HierarchicalLabel()
        self._populate_label_text(label, x_mm, y_mm, text)
        return self._create_single(label)

    def add_wire(
        self,
        x1_mm: float,
        y1_mm: float,
        x2_mm: float,
        y2_mm: float,
    ) -> KIID:
        line = SchematicLine()
        line.start.x_nm = mm_to_nm(x1_mm)
        line.start.y_nm = mm_to_nm(y1_mm)
        line.end.x_nm = mm_to_nm(x2_mm)
        line.end.y_nm = mm_to_nm(y2_mm)
        line.line_type = SchematicLineType.SLT_WIRE
        return self._create_single(line)

    def add_junction(self, x_mm: float, y_mm: float) -> KIID:
        junction = Junction()
        junction.position.x_nm = mm_to_nm(x_mm)
        junction.position.y_nm = mm_to_nm(y_mm)
        return self._create_single(junction)

    def add_no_connect(self, x_mm: float, y_mm: float) -> KIID:
        nc = NoConnectMarker()
        nc.position.x_nm = mm_to_nm(x_mm)
        nc.position.y_nm = mm_to_nm(y_mm)
        return self._create_single(nc)


def open_schematic(*, client: MasterKiCadClient | None = None) -> Schematic:
    """Return a :class:`Schematic` for the first open eeschema document.

    Raises :class:`ApiError` if no schematic is open.
    """
    c = client or MasterKiCadClient()
    cmd = GetOpenDocuments()
    cmd.type = DocumentType.DOCTYPE_SCHEMATIC
    response = c.send(cmd, GetOpenDocumentsResponse)
    docs = list(response.documents)
    if not docs:
        raise ApiError("No schematic document open in eeschema")
    return Schematic(docs[0], client=c)
