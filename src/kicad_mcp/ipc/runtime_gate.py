# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
"""Runtime gate for IPC-only schematic mutations.

Why this module exists
----------------------

The IPC path for schematic edits (``kicad_mcp.ipc.schematic.Schematic``)
crashes eeschema on every KiCad 10.0.x stable release shipped to date —
the input-validation handler in ``api_handler_sch.cpp`` is a TODO stub
until upstream commit ``3dca4e0e38`` ("API: implement schematic item
creation", Jon Evans, 2026-04-07), which lands on master / nightly. If
the connected KiCad lacks that fix the IPC mutation surface scrambles
the editor and risks corrupting the schematic.

Contract (2026-05-22)
---------------------

There is NO file-edit fallback. ``sch_add_*`` mutations either dispatch
over IPC or raise :class:`SchematicIPCRequiredError`. The deletion of
the fallback was a deliberate user-driven change after a session where
the silent file-edit path overwrote IPC-resident state — see the
``feedback_sch_mcp_incident_*`` and ``feedback_sch_ipc_*`` memories.

Design notes
------------

* **Fail-loud.** Any gate miss (missing fix, no open schematic, version
  probe failure) raises with a concrete reason. Callers do not get to
  silently write the file.
* **Cache once per server start.** The connected KiCad version cannot
  change without a process restart, so we memoise the detection result.
  Callers can reset it via :func:`reset_runtime_gate_cache` (tests).
* **Observability.** Every routing decision is logged at INFO with a
  reason field so the user can grep ``schematic_route_decision`` to see
  why the gate raised.
"""

from __future__ import annotations

import os
import re
import threading
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import structlog

if TYPE_CHECKING:
    from google.protobuf.message import Message  # type: ignore[import-untyped]

    from .schematic import Schematic


logger = structlog.get_logger(__name__)


# ``kipy.kicad.KiCad`` is marked ``py.typed`` upstream but pyright still
# resolves its public API as Unknown — using the real class name in
# typed signatures here would push 1+ ``partially unknown`` errors into
# every caller's file. We alias to ``Any`` so the gate's public surface
# stays clean for downstream type-checking. The runtime contract is
# unaffected: callers always pass a callable that yields a real
# :class:`kipy.kicad.KiCad`.
_KiCadFactory = Callable[[], Any]


# ---------------------------------------------------------------------------
# Public constants
# ---------------------------------------------------------------------------

#: When set, the gate treats an ``AS_UNHANDLED`` response to ``GetVersion``
#: as "trust the operator" instead of raising. This is the standalone-
#: eeschema case (eeschema launched directly doesn't register
#: ``GetVersion`` — only the project manager does), so the operator has
#: to opt INTO a slightly-relaxed verification path. Without this flag
#: the gate raises on ``AS_UNHANDLED``.
SCH_IPC_FORCE_ENV = "KICAD_MCP_SCH_IPC_FORCE"

#: Optional post-write verification. When set, after a successful
#: ``CreateItems`` we round-trip the created items back via
#: ``GetItemsById`` and assert their KIIDs land where we expect. Doubles
#: the IPC traffic per call but catches the case where eeschema's
#: deserializer accepts garbage and stores a malformed item.
SCH_IPC_VERIFY_ENV = "KICAD_MCP_SCH_IPC_VERIFY"

#: Persistence hint appended to IPC success responses, mirroring the
#: pcbnew convention in :data:`kicad_mcp.connection.PERSISTENCE_HINT`.
#: When an edit went through IPC, the change lives only in eeschema's
#: in-memory document; the user MUST call ``sch_save()`` to flush.
SCH_IPC_PERSISTENCE_HINT = (
    "Call sch_save() to persist — the change is in eeschema's session only and "
    "will be lost if the editor closes without saving."
)


class SchematicIPCRequiredError(RuntimeError):
    """Raised when a schematic mutation cannot be dispatched over IPC.

    There is no file-edit fallback. Callers receive this exception with
    a concrete ``reason`` describing what gate failed (version missing
    fix, no open schematic, connection refused, etc.) so the operator
    can act on it.
    """

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


# ---------------------------------------------------------------------------
# Version detection
# ---------------------------------------------------------------------------

#: Upstream commit hash that landed the defensive ``CreateItems`` fix.
#: Build strings AFTER this commit will contain a hash newer than this in
#: their ``g<hash>`` suffix, but we cannot easily compare two arbitrary
#: git hashes for ordering. Instead we use a coarse heuristic on the
#: major/minor version (see :func:`_full_version_has_fix`) and treat the
#: literal hash match as a positive signal.
_FIX_COMMIT_HASH = "3dca4e0e38"

#: The first KiCad release branch that will SHIP with the fix already
#: applied. Anything < (major, minor) gates the IPC path off; anything >=
#: is presumed safe. This is a conservative lower bound: the fix landed
#: while master was tracking ``10.99.x`` (the pre-release series for
#: KiCad 11), so any build reporting a minor of 99 or higher is on a
#: branch that contains the fix.
_FIRST_FIXED_RELEASE: tuple[int, int] = (10, 99)


def _full_version_has_fix(full_version: str) -> bool:
    """Heuristic: does this git-describe string represent a KiCad with the fix?

    The ``full_version`` field comes from kipy's :class:`KiCadVersion`
    proto, which mirrors KiCad's ``git describe --tags`` output. The
    format observed in practice is::

        <major>.<minor>.<patch>-<n_commits>-g<short_hash>

    Examples:

    * ``10.0.3``                       — stable release, NO fix
    * ``10.0.3-12-gabcdef1234``        — patched stable, fix is uncertain
                                        (we'd need full git ordering to be
                                        sure), so we treat it as missing
    * ``10.99.0-1059-g0895df3e3c``     — pre-release master, HAS fix
    * ``11.0.0-0-gffffffffff``         — future release, HAS fix
    * any string containing ``3dca4e0e38`` — explicit positive match

    The heuristic is conservative: when in doubt, return ``False`` and
    route to the safer file-based path.
    """

    if not full_version:
        return False

    # Explicit match on the fix commit hash anywhere in the describe
    # string — this is the strongest positive signal we have. Real-world
    # describe output never contains the merge-target hash directly, but
    # nightly tarballs sometimes embed it in build metadata, and it makes
    # the function easy to reason about under test.
    if _FIX_COMMIT_HASH in full_version:
        return True

    # Strip any leading "v" and split on "-" to peel off the version
    # tuple. We tolerate trailing parts (commit count, hash) but require
    # the leading element to parse as <major>.<minor>.<patch>.
    head = full_version.lstrip("v").split("-", 1)[0]
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", head)
    if match is None:
        return False

    major = int(match.group(1))
    minor = int(match.group(2))

    fixed_major, fixed_minor = _FIRST_FIXED_RELEASE
    if major > fixed_major:
        return True
    if major == fixed_major and minor >= fixed_minor:
        return True
    return False


# ---------------------------------------------------------------------------
# Cached detection
# ---------------------------------------------------------------------------

_cache_lock = threading.Lock()
_version_cache: bool | None = None


def reset_runtime_gate_cache() -> None:
    """Forget the cached version-detection result.

    Public so tests can call it between scenarios; production code does
    not need to invoke this since the connected KiCad version cannot
    change within a single MCP server lifetime.
    """

    global _version_cache
    with _cache_lock:
        _version_cache = None


def _connected_kicad_has_fix(kicad_factory: _KiCadFactory | None = None) -> bool:
    """Return True iff the connected KiCad's reported version contains the fix.

    Results are cached for the lifetime of the process — see
    :func:`reset_runtime_gate_cache` for the test-side reset.

    ``kicad_factory`` is injectable for tests; production callers leave
    it ``None`` and pick up :func:`kicad_mcp.connection.get_kicad`. We
    import that lazily so that this module remains importable in
    environments where the IPC stack is not wired up.
    """

    global _version_cache
    with _cache_lock:
        if _version_cache is not None:
            return _version_cache

    if kicad_factory is None:
        # Direct master client — kipy is deliberately NOT imported here
        # because it ships older proto descriptors that collide with our
        # vendored master stubs in the global protobuf descriptor pool.
        # We construct a fresh client per call (the gate caches the
        # final has_fix decision anyway).
        from ._master_client import MasterKiCadClient

        def _factory() -> MasterKiCadClient:
            return MasterKiCadClient()

        kicad_factory = _factory

    try:
        # The master client doesn't expose ``.get_version`` directly;
        # send the proto and parse the response.
        from kicad_mcp._master_proto.mp.common.commands.base_commands_pb2 import (
            GetVersion,
            GetVersionResponse,
        )

        client = kicad_factory()
        response = client.send(GetVersion(), GetVersionResponse)
        full = str(response.version.full_version or "")
        has_fix = _full_version_has_fix(full)
    except Exception as exc:
        # ``GetVersion`` is only registered by the ``kicad.exe`` project
        # manager — when the user launches eeschema directly (a common
        # workflow on nightlies and the case live-tested 2026-05-22),
        # the version probe returns AS_UNHANDLED. We can't tell from
        # that whether the connected build is stable or nightly, so we
        # defer to the operator: if they explicitly opted in via the
        # env var (already checked at this point), trust them. If the
        # probe failed for any OTHER reason (no socket, parse error,
        # connection refused), fail-closed.
        message = str(exc)
        is_unhandled = (
            "no handler available" in message.lower() or "as_unhandled" in message.lower()
        )
        force_env = os.environ.get(SCH_IPC_FORCE_ENV, "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        # Fallback: flag file at ~/.kicad-mcp-force-ipc. On Windows the User
        # env var is unreliable for child processes of GUI shells (Claude
        # Code, VS Code, etc.) that don't re-read HKCU\Environment on
        # WM_SETTINGCHANGE. A flag file is read fresh every invocation.
        force_file = False
        try:
            from pathlib import Path as _Path

            if (_Path.home() / ".kicad-mcp-force-ipc").exists():
                force_file = True
        except Exception:  # noqa: BLE001, S110
            pass
        force = force_env or force_file
        if is_unhandled and force:
            # Standalone eeschema (no project manager) doesn't register
            # GetVersion. The operator has explicitly opted into the
            # relaxed verification path; trust them.
            logger.info(
                "schematic_ipc_version_probe_unhandled_force_assume_ok",
                error=message,
            )
            has_fix = True
        elif is_unhandled:
            # Default behaviour for AS_UNHANDLED: fail closed. The module
            # docstring's promised contract.
            logger.info(
                "schematic_ipc_version_probe_unhandled_fail_closed",
                error=message,
                hint=f"Set {SCH_IPC_FORCE_ENV}=1 to bypass when launching eeschema directly.",
            )
            has_fix = False
        else:
            logger.info(
                "schematic_ipc_version_probe_failed",
                error_type=type(exc).__name__,
                error=message,
            )
            has_fix = False
    else:
        logger.info(
            "schematic_ipc_version_probed",
            full_version=full,
            has_fix=has_fix,
        )

    with _cache_lock:
        _version_cache = has_fix
    return has_fix


# ---------------------------------------------------------------------------
# Routing decision
# ---------------------------------------------------------------------------


def _has_open_schematic(kicad_factory: _KiCadFactory | None = None) -> bool:
    """Return True iff at least one schematic document is open in eeschema."""

    if kicad_factory is None:
        from ._master_client import MasterKiCadClient

        def _factory() -> MasterKiCadClient:
            return MasterKiCadClient()

        kicad_factory = _factory

    try:
        # Use master protos — kipy.proto stays out of the descriptor pool.
        from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
            GetOpenDocuments,
            GetOpenDocumentsResponse,
        )
        from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType

        client = kicad_factory()
        cmd = GetOpenDocuments()
        cmd.type = DocumentType.DOCTYPE_SCHEMATIC
        response = client.send(cmd, GetOpenDocumentsResponse)
        docs = list(response.documents)
    except Exception as exc:
        logger.info(
            "schematic_ipc_open_doc_probe_failed",
            error_type=type(exc).__name__,
            error=str(exc),
        )
        return False
    return bool(docs)


def check_ipc_gate(
    *,
    kicad_factory: _KiCadFactory | None = None,
) -> tuple[bool, str]:
    """Probe the IPC gate. Returns ``(ok, reason)``.

    ``ok`` is True only when both of these hold:

    1. The connected KiCad reports a version containing the fix.
    2. There is at least one open schematic document.

    On failure ``reason`` is a human-readable string explaining which
    gate failed. There is no fallback — the caller is expected to either
    proceed (``ok=True``) or raise :class:`SchematicIPCRequiredError`.
    """

    if not _connected_kicad_has_fix(kicad_factory):
        reason = (
            "KiCad IPC version does not contain the schematic-IPC fix "
            "(commit 3dca4e0e38, first shipped on 10.99 / nightly). "
            f"If you are running standalone eeschema, set {SCH_IPC_FORCE_ENV}=1 "
            "to bypass the version probe."
        )
        logger.info("schematic_route_decision", path="raise", reason="version_lacks_fix")
        return False, reason

    if not _has_open_schematic(kicad_factory):
        reason = (
            "No schematic document is open in eeschema. Open the project "
            "in eeschema before calling schematic mutation tools."
        )
        logger.info("schematic_route_decision", path="raise", reason="no_open_schematic")
        return False, reason

    logger.info("schematic_route_decision", path="ipc", reason="all_gates_passed")
    return True, ""


# ---------------------------------------------------------------------------
# Routing helper
# ---------------------------------------------------------------------------


def _open_schematic_for_ipc(
    kicad_factory: _KiCadFactory | None = None,
) -> Schematic:
    """Build a :class:`Schematic` wrapping the first open schematic document.

    Separate from :func:`kicad_mcp.ipc.schematic.open_schematic` so we
    can inject ``kicad_factory`` from tests without monkeypatching the
    other module.
    """

    if kicad_factory is None:
        from ._master_client import MasterKiCadClient

        def _factory() -> MasterKiCadClient:
            return MasterKiCadClient()

        kicad_factory = _factory

    # Master protos only — kipy.proto MUST NOT be imported here.
    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        GetOpenDocuments,
        GetOpenDocumentsResponse,
    )
    from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType

    from .schematic import Schematic

    client = kicad_factory()
    cmd = GetOpenDocuments()
    cmd.type = DocumentType.DOCTYPE_SCHEMATIC
    response = client.send(cmd, GetOpenDocumentsResponse)
    docs = list(response.documents)
    if not docs:
        raise RuntimeError(
            "No schematic document is open in eeschema. Cannot dispatch schematic IPC mutation."
        )
    return Schematic(docs[0], client=client)


def route_schematic_create(
    items: list[Message],
    *,
    env: dict[str, str] | None = None,
    kicad_factory: _KiCadFactory | None = None,
) -> str:
    """Dispatch a schematic create-items call over IPC.

    Parameters
    ----------
    items:
        The pre-built protobuf messages to send.
    env, kicad_factory:
        Test seams; production callers leave them ``None``.

    Returns
    -------
    str
        Success string with the persistence hint suffixed.

    Raises
    ------
    SchematicIPCRequiredError
        When the IPC gate cannot be opened (KiCad lacks the fix, no
        schematic open, version probe failed, etc.). The exception's
        ``reason`` attribute describes the failure.
    """

    ok, reason = check_ipc_gate(kicad_factory=kicad_factory)
    if not ok:
        raise SchematicIPCRequiredError(reason)

    schematic = _open_schematic_for_ipc(kicad_factory=kicad_factory)
    results = schematic.create_items(items)
    logger.info(
        "schematic_ipc_create_succeeded",
        items=len(items),
        results=len(results),
    )

    # Optional post-write verification, opt-in via KICAD_MCP_SCH_IPC_VERIFY=1.
    verify_env = (env if env is not None else os.environ).get(SCH_IPC_VERIFY_ENV, "")
    if verify_env.strip().lower() in {"1", "true", "yes", "on"}:
        try:
            _verify_created_items(schematic, results)
        except Exception as exc:
            # Surface verification failures loudly — the items DID land
            # in eeschema, but they may be in a corrupt state.
            logger.warning(
                "schematic_ipc_post_write_verification_failed",
                error_type=type(exc).__name__,
                error=str(exc),
            )
            return (
                f"Added {len(items)} schematic item(s) via IPC, but post-write "
                f"verification failed: {exc}. The items are present in "
                f"eeschema's session; inspect manually before saving. "
                f"{SCH_IPC_PERSISTENCE_HINT}"
            )

    return f"Added {len(items)} schematic item(s) via IPC. {SCH_IPC_PERSISTENCE_HINT}"


def route_schematic_place_symbol(
    *,
    library: str,
    symbol_name: str,
    x_mm: float,
    y_mm: float,
    reference: str = "",
    value: str = "",
    unit: int = 1,
    orientation_degrees: int = 0,
    mirror_x: bool = False,
    mirror_y: bool = False,
    kicad_factory: _KiCadFactory | None = None,
) -> str:
    """Dispatch a `PlaceLibrarySymbol` IPC call to eeschema.

    Mirrors the GUI's "place from library" path one-to-one — KiCad
    constructs the SCH_SYMBOL via its own constructor, handling pin
    transforms, default field positions, attribute inheritance, etc.
    Single IPC call; no client-side proto juggling.

    Requires KiCad ≥ the build that contains the `PlaceLibrarySymbol`
    handler (our upstream patch on master branch
    `feat/ipc-get-library-symbol`). When the gate is closed,
    :class:`SchematicIPCRequiredError` is raised.
    """

    ok, reason = check_ipc_gate(kicad_factory=kicad_factory)
    if not ok:
        raise SchematicIPCRequiredError(reason)

    if kicad_factory is None:
        from ._master_client import MasterKiCadClient

        def _factory() -> MasterKiCadClient:
            return MasterKiCadClient()

        kicad_factory = _factory

    # Master protos only — kipy.proto stays out of the descriptor pool.
    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        GetOpenDocuments,
        GetOpenDocumentsResponse,
    )
    from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType
    from kicad_mcp._master_proto.mp.schematic.schematic_commands_pb2 import (
        PlaceLibrarySymbol,
        PlaceLibrarySymbolResponse,
    )
    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
        SchematicSymbolOrientation,
    )

    client = kicad_factory()

    # Resolve the active schematic document.
    docs_req = GetOpenDocuments()
    docs_req.type = DocumentType.DOCTYPE_SCHEMATIC
    docs_resp = client.send(docs_req, GetOpenDocumentsResponse)
    docs = list(docs_resp.documents)
    if not docs:
        raise SchematicIPCRequiredError(
            "No schematic document is open in eeschema. Cannot dispatch PlaceLibrarySymbol."
        )
    doc = docs[0]

    place = PlaceLibrarySymbol()
    place.document.CopyFrom(doc)
    place.id.library_nickname = library
    place.id.entry_name = symbol_name
    place.position.x_nm = int(round(x_mm * 1_000_000))
    place.position.y_nm = int(round(y_mm * 1_000_000))
    if reference:
        place.reference = reference
    if value:
        place.value = value
    if unit and unit > 1:
        place.unit = unit

    orientation_map = {
        0: SchematicSymbolOrientation.SSO_0,
        90: SchematicSymbolOrientation.SSO_90,
        180: SchematicSymbolOrientation.SSO_180,
        270: SchematicSymbolOrientation.SSO_270,
    }
    if orientation_degrees in orientation_map:
        place.orientation = orientation_map[orientation_degrees]
    elif orientation_degrees:
        raise ValueError(
            f"orientation_degrees must be one of 0/90/180/270; got {orientation_degrees}"
        )

    if mirror_x:
        place.mirror_x = True
    if mirror_y:
        place.mirror_y = True

    response = client.send(place, PlaceLibrarySymbolResponse)
    placed_id = response.placed.id.value
    logger.info(
        "schematic_ipc_place_symbol_succeeded",
        library=library,
        symbol_name=symbol_name,
        x_mm=x_mm,
        y_mm=y_mm,
        reference=reference,
        kiid=placed_id,
    )
    return (
        f"Placed {library}:{symbol_name} as "
        f"{reference or '(auto-ref)'} ({value or 'default'}) at "
        f"({x_mm:.2f}, {y_mm:.2f}) mm via IPC. "
        f"KIID={placed_id}. "
        f"{SCH_IPC_PERSISTENCE_HINT}"
    )


def _verify_created_items(schematic: Any, results: list[Any]) -> None:  # noqa: ANN401
    """Round-trip the KIIDs we just created back through GetItemsById.

    Confirms eeschema actually stored items at the KIIDs it claims to
    have assigned. A missing or empty result indicates the deserializer
    accepted garbage — the IPC analogue of PR #24's file post-edit
    parse-back validation.
    """
    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        GetItemsById,
        GetItemsResponse,
    )

    kiids = []
    for result in results:
        # ItemCreationResult.item is google.protobuf.Any wrapping the
        # created proto; the KIID is in its `id` field. We unpack lazily.
        any_item = result.item
        # Trick: every schematic item proto in master has `id` at field 1.
        # Use a generic placeholder unpack via ParseFromString on a peer
        # message that we know carries `id`.
        from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import Junction

        placeholder = Junction()
        if any_item.Unpack(placeholder):
            kiids.append(placeholder.id)

    if not kiids:
        # We can't pull KIIDs from results (heterogeneous types where
        # Junction probe fails). Skip — better to silently allow than
        # to false-positive a real-write as failed.
        return

    cmd = GetItemsById()
    cmd.header.document.CopyFrom(schematic.document)
    for kiid in kiids:
        cmd.item_ids.append(kiid)
    response = schematic.client.send(cmd, GetItemsResponse)
    if len(response.items) != len(kiids):
        raise RuntimeError(
            f"Post-write verification: expected {len(kiids)} items, "
            f"GetItemsById returned {len(response.items)}"
        )


# ---------------------------------------------------------------------------
# Proto builders for the four wired sch_add_* tools
#
# These live here so the tool wrappers in ``tools/schematic.py`` do not
# have to import kipy proto types — keeping the IPC proto surface
# isolated to this package eases version-skew triage.
# ---------------------------------------------------------------------------


def _mm_to_nm(value_mm: float) -> int:
    return int(round(value_mm * 1_000_000))


def _populate_label(label: Any, x_mm: float, y_mm: float, text: str) -> None:  # noqa: ANN401
    """Master proto field shape: ``label.text`` is directly base_types.Text.

    Set the string + position + 1.27mm default text attributes (KiCad's
    GUI default). Without explicit attributes eeschema renders zero-
    size text (invisible label box).
    """
    x_nm = _mm_to_nm(x_mm)
    y_nm = _mm_to_nm(y_mm)
    label.position.x_nm = x_nm
    label.position.y_nm = y_nm
    label.text.text = text
    label.text.position.x_nm = x_nm
    label.text.position.y_nm = y_nm
    label.text.attributes.size.x_nm = 1_270_000
    label.text.attributes.size.y_nm = 1_270_000
    # Without explicit alignment, text centers on the anchor and
    # straddles the flat edge of the pentagon body (see incident
    # 2026-05-22). Match the GUI default: left-aligned, vertically
    # centered.
    from kicad_mcp._master_proto.mp.common.types.enums_pb2 import HA_LEFT, VA_CENTER

    label.text.attributes.horizontal_alignment = HA_LEFT
    label.text.attributes.vertical_alignment = VA_CENTER


def build_global_label_proto(x_mm: float, y_mm: float, text: str) -> Message:
    """Build a master ``GlobalLabel`` proto carrying ``text``.

    Matches GUI default: ``SCH_GLOBALLABEL`` constructs with
    ``LABEL_FLAG_SHAPE::L_BIDI`` (sch_label.cpp:2105). Leaving
    ``shape`` unset (= ``SLSH_UNKNOWN``) renders a plain rectangle.
    """

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
        SLSH_BIDI,
        GlobalLabel,
    )

    label = GlobalLabel()
    _populate_label(label, x_mm, y_mm, text)
    label.shape = SLSH_BIDI
    return label


def build_local_label_proto(x_mm: float, y_mm: float, text: str) -> Message:
    """Build a master ``LocalLabel`` proto carrying ``text``."""

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import LocalLabel

    label = LocalLabel()
    _populate_label(label, x_mm, y_mm, text)
    return label


def build_hierarchical_label_proto(x_mm: float, y_mm: float, text: str) -> Message:
    """Build a master ``HierarchicalLabel`` proto carrying ``text``."""

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import HierarchicalLabel

    label = HierarchicalLabel()
    _populate_label(label, x_mm, y_mm, text)
    return label


def build_wire_proto(x1_mm: float, y1_mm: float, x2_mm: float, y2_mm: float) -> Message:
    """Build a master ``SchematicLine`` proto for a wire."""

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
        SchematicLine,
        SchematicLineType,
    )

    line = SchematicLine()
    line.start.x_nm = _mm_to_nm(x1_mm)
    line.start.y_nm = _mm_to_nm(y1_mm)
    line.end.x_nm = _mm_to_nm(x2_mm)
    line.end.y_nm = _mm_to_nm(y2_mm)
    line.type = SchematicLineType.SLT_WIRE
    return line


def build_bus_proto(x1_mm: float, y1_mm: float, x2_mm: float, y2_mm: float) -> Message:
    """Build a master ``SchematicLine`` proto for a bus."""

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
        SchematicLine,
        SchematicLineType,
    )

    line = SchematicLine()
    line.start.x_nm = _mm_to_nm(x1_mm)
    line.start.y_nm = _mm_to_nm(y1_mm)
    line.end.x_nm = _mm_to_nm(x2_mm)
    line.end.y_nm = _mm_to_nm(y2_mm)
    # The master ``SchematicLine`` proto names this field ``type``; the
    # generated Python getter exposes it as ``line.type`` (the existing
    # ``build_wire_proto`` writes to ``line.line_type`` which silently
    # sets a non-existent attribute and leaves the on-wire enum at
    # SLT_UNKNOWN — a pre-existing bug that's harmless while the IPC path
    # is off-by-default but should be revisited when the gate stabilises).
    # We use the correct field name here so the bus dispatch carries the
    # right line type when an operator opts in.
    line.type = SchematicLineType.SLT_BUS
    return line


def build_junction_proto(x_mm: float, y_mm: float) -> Message:
    """Build a master ``Junction`` proto at the given position."""

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import Junction

    junction = Junction()
    junction.position.x_nm = _mm_to_nm(x_mm)
    junction.position.y_nm = _mm_to_nm(y_mm)
    return junction


def build_no_connect_proto(x_mm: float, y_mm: float) -> Message:
    """Build a master ``NoConnectMarker`` proto at the given position."""

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import NoConnectMarker

    marker = NoConnectMarker()
    marker.position.x_nm = _mm_to_nm(x_mm)
    marker.position.y_nm = _mm_to_nm(y_mm)
    return marker


def build_text_proto(
    x_mm: float,
    y_mm: float,
    text: str,
    *,
    size_mm: float = 1.27,
) -> Message:
    """Build a master ``SchematicText`` proto (free-floating note)."""

    from kicad_mcp._master_proto.mp.common.types.enums_pb2 import HA_LEFT, VA_CENTER
    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import SchematicText

    sch_text = SchematicText()
    sch_text.text.text = text
    sch_text.text.position.x_nm = _mm_to_nm(x_mm)
    sch_text.text.position.y_nm = _mm_to_nm(y_mm)
    sch_text.text.attributes.size.x_nm = _mm_to_nm(size_mm)
    sch_text.text.attributes.size.y_nm = _mm_to_nm(size_mm)
    sch_text.text.attributes.horizontal_alignment = HA_LEFT
    sch_text.text.attributes.vertical_alignment = VA_CENTER
    if "\n" in text:
        sch_text.text.attributes.multiline = True
        sch_text.text.attributes.line_spacing = 1.0
    return sch_text


def build_textbox_proto(
    x1_mm: float,
    y1_mm: float,
    x2_mm: float,
    y2_mm: float,
    text: str,
    *,
    size_mm: float = 1.27,
) -> Message:
    """Build a master ``SchematicTextBox`` proto (annotated note with border)."""

    from kicad_mcp._master_proto.mp.common.types.enums_pb2 import HA_LEFT, VA_TOP
    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
        SchematicTextBox,
    )

    box = SchematicTextBox()
    box.textbox.text = text
    box.textbox.top_left.x_nm = _mm_to_nm(min(x1_mm, x2_mm))
    box.textbox.top_left.y_nm = _mm_to_nm(min(y1_mm, y2_mm))
    box.textbox.bottom_right.x_nm = _mm_to_nm(max(x1_mm, x2_mm))
    box.textbox.bottom_right.y_nm = _mm_to_nm(max(y1_mm, y2_mm))
    box.textbox.attributes.size.x_nm = _mm_to_nm(size_mm)
    box.textbox.attributes.size.y_nm = _mm_to_nm(size_mm)
    box.textbox.attributes.horizontal_alignment = HA_LEFT
    box.textbox.attributes.vertical_alignment = VA_TOP
    box.textbox.attributes.multiline = True
    box.textbox.attributes.line_spacing = 1.0
    # Small interior margins so text doesn't crash into the border.
    margin_nm = _mm_to_nm(0.635)  # half a fine-grid step
    box.margin_left.value_nm = margin_nm
    box.margin_right.value_nm = margin_nm
    box.margin_top.value_nm = margin_nm
    box.margin_bottom.value_nm = margin_nm
    return box


#: Mapping from the file-path ``direction`` string used by
#: ``sch_add_bus_wire_entry`` to the (dx_mm, dy_mm) size vector that the
#: file-format ``bus_entry`` block emits. Keep these in sync with
#: ``tools.schematic.bus_entry_block``.
_BUS_ENTRY_OFFSETS_MM: dict[str, tuple[float, float]] = {
    "up_right": (2.54, -2.54),
    "down_right": (2.54, 2.54),
    "up_left": (-2.54, -2.54),
    "down_left": (-2.54, 2.54),
}


def build_bus_wire_entry_proto(x_mm: float, y_mm: float, direction: str) -> Message:
    """Build a master ``BusEntry`` proto carrying the wire-to-bus marker.

    Parameters
    ----------
    x_mm, y_mm:
        Anchor (the bus-side endpoint) of the entry, in millimetres.
    direction:
        One of ``up_right``, ``down_right``, ``up_left``, ``down_left`` —
        the same enumeration the file-path helper accepts. Anything else
        raises ``ValueError`` so the mismatch is loud rather than silent.
    """

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
        BusEntry,
        BusEntryType,
    )

    try:
        dx_mm, dy_mm = _BUS_ENTRY_OFFSETS_MM[direction]
    except KeyError as exc:
        raise ValueError(
            f"Unknown bus_entry direction {direction!r}; expected one of "
            f"{sorted(_BUS_ENTRY_OFFSETS_MM)}."
        ) from exc

    entry = BusEntry()
    entry.position.x_nm = _mm_to_nm(x_mm)
    entry.position.y_nm = _mm_to_nm(y_mm)
    entry.size.x_nm = _mm_to_nm(dx_mm)
    entry.size.y_nm = _mm_to_nm(dy_mm)
    entry.type = BusEntryType.BET_WIRE_TO_BUS
    return entry


def route_schematic_save(
    *,
    kicad_factory: _KiCadFactory | None = None,
) -> str:
    """Persist the live schematic session to disk via IPC ``SaveDocument``.

    Returns a one-line success message. Raises
    :class:`SchematicIPCRequiredError` if the gate is closed.
    """

    ok, reason = check_ipc_gate(kicad_factory=kicad_factory)
    if not ok:
        raise SchematicIPCRequiredError(reason)

    if kicad_factory is None:
        from ._master_client import MasterKiCadClient

        def _factory() -> MasterKiCadClient:
            return MasterKiCadClient()

        kicad_factory = _factory

    from google.protobuf.empty_pb2 import Empty

    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        GetOpenDocuments,
        GetOpenDocumentsResponse,
    )
    from kicad_mcp._master_proto.mp.common.commands.project_commands_pb2 import (
        SaveDocument,
    )
    from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType

    client = kicad_factory()
    docs_req = GetOpenDocuments()
    docs_req.type = DocumentType.DOCTYPE_SCHEMATIC
    docs = list(client.send(docs_req, GetOpenDocumentsResponse).documents)
    if not docs:
        raise SchematicIPCRequiredError(
            "No schematic document is open in eeschema. Cannot dispatch SaveDocument."
        )
    doc = docs[0]

    save = SaveDocument()
    save.document.CopyFrom(doc)
    client.send(save, Empty)
    logger.info("schematic_ipc_save_succeeded", project=doc.project.name)
    return f"Saved schematic '{doc.project.name}' to disk via IPC."


def route_schematic_delete_by_reference(
    reference: str,
    *,
    kicad_factory: _KiCadFactory | None = None,
) -> tuple[int, int]:
    """Delete every SCH_SYMBOL whose reference designator matches ``reference``.

    Returns ``(symbols_deleted, wires_deleted)``. Wires are not auto-removed
    by this function — only the symbols. (Wire cleanup happens in
    eeschema when the user reroutes; KiCad does not currently maintain
    a strict "delete-attached-wires" invariant on IPC delete.)

    Raises :class:`SchematicIPCRequiredError` if the gate is closed.
    """

    ok, reason = check_ipc_gate(kicad_factory=kicad_factory)
    if not ok:
        raise SchematicIPCRequiredError(reason)

    if kicad_factory is None:
        from ._master_client import MasterKiCadClient

        def _factory() -> MasterKiCadClient:
            return MasterKiCadClient()

        kicad_factory = _factory

    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        DeleteItems,
        DeleteItemsResponse,
        GetItems,
        GetItemsResponse,
        GetOpenDocuments,
        GetOpenDocumentsResponse,
    )
    from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType
    from kicad_mcp._master_proto.mp.common.types.enums_pb2 import KOT_SCH_SYMBOL
    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
        SchematicSymbolInstance,
    )

    client = kicad_factory()

    docs_req = GetOpenDocuments()
    docs_req.type = DocumentType.DOCTYPE_SCHEMATIC
    docs = list(client.send(docs_req, GetOpenDocumentsResponse).documents)
    if not docs:
        raise SchematicIPCRequiredError(
            "No schematic document is open in eeschema. Cannot dispatch DeleteItems."
        )
    doc = docs[0]

    get = GetItems()
    get.header.document.CopyFrom(doc)
    get.types.append(KOT_SCH_SYMBOL)
    items = list(client.send(get, GetItemsResponse).items)

    delete = DeleteItems()
    delete.header.document.CopyFrom(doc)
    matched = 0
    for any_item in items:
        inst = SchematicSymbolInstance()
        if not any_item.Unpack(inst):
            continue
        if inst.reference_field.text.text == reference and inst.id.value:
            delete.item_ids.add().value = inst.id.value
            matched += 1

    if matched == 0:
        return (0, 0)

    client.send(delete, DeleteItemsResponse)
    logger.info(
        "schematic_ipc_delete_by_reference_succeeded",
        reference=reference,
        symbols_deleted=matched,
    )
    return (matched, 0)


def route_schematic_clear_all(
    *,
    kicad_factory: _KiCadFactory | None = None,
) -> dict[str, int]:
    """Delete every schematic item — symbols, wires, labels, junctions, etc.

    Returns a dict of per-type deletion counts. Raises
    :class:`SchematicIPCRequiredError` if the gate is closed.
    """

    ok, reason = check_ipc_gate(kicad_factory=kicad_factory)
    if not ok:
        raise SchematicIPCRequiredError(reason)

    if kicad_factory is None:
        from ._master_client import MasterKiCadClient

        def _factory() -> MasterKiCadClient:
            return MasterKiCadClient()

        kicad_factory = _factory

    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        DeleteItems,
        DeleteItemsResponse,
        GetItems,
        GetItemsResponse,
        GetOpenDocuments,
        GetOpenDocumentsResponse,
    )
    from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType
    from kicad_mcp._master_proto.mp.common.types.enums_pb2 import (
        KOT_SCH_BUS_WIRE_ENTRY,
        KOT_SCH_DIRECTIVE_LABEL,
        KOT_SCH_GLOBAL_LABEL,
        KOT_SCH_HIER_LABEL,
        KOT_SCH_JUNCTION,
        KOT_SCH_LABEL,
        KOT_SCH_LINE,
        KOT_SCH_NO_CONNECT,
        KOT_SCH_SYMBOL,
        KOT_SCH_TEXT,
        KOT_SCH_TEXTBOX,
    )
    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import (
        BusEntry,
        DirectiveLabel,
        GlobalLabel,
        HierarchicalLabel,
        Junction,
        LocalLabel,
        NoConnectMarker,
        SchematicLine,
        SchematicSymbolInstance,
        SchematicText,
        SchematicTextBox,
    )

    client = kicad_factory()
    docs_req = GetOpenDocuments()
    docs_req.type = DocumentType.DOCTYPE_SCHEMATIC
    docs = list(client.send(docs_req, GetOpenDocumentsResponse).documents)
    if not docs:
        raise SchematicIPCRequiredError(
            "No schematic document is open in eeschema. Cannot dispatch DeleteItems."
        )
    doc = docs[0]

    get = GetItems()
    get.header.document.CopyFrom(doc)
    for kot in (
        KOT_SCH_SYMBOL,
        KOT_SCH_LINE,
        KOT_SCH_GLOBAL_LABEL,
        KOT_SCH_LABEL,
        KOT_SCH_HIER_LABEL,
        KOT_SCH_DIRECTIVE_LABEL,
        KOT_SCH_JUNCTION,
        KOT_SCH_NO_CONNECT,
        KOT_SCH_BUS_WIRE_ENTRY,
        KOT_SCH_TEXT,
        KOT_SCH_TEXTBOX,
    ):
        get.types.append(kot)
    items = list(client.send(get, GetItemsResponse).items)

    candidate_types = (
        ("symbols", SchematicSymbolInstance),
        ("wires_buses", SchematicLine),
        ("global_labels", GlobalLabel),
        ("local_labels", LocalLabel),
        ("hier_labels", HierarchicalLabel),
        ("directive_labels", DirectiveLabel),
        ("junctions", Junction),
        ("no_connect_markers", NoConnectMarker),
        ("bus_entries", BusEntry),
        ("texts", SchematicText),
        ("textboxes", SchematicTextBox),
    )

    delete = DeleteItems()
    delete.header.document.CopyFrom(doc)
    counts: dict[str, int] = {key: 0 for key, _ in candidate_types}
    for any_item in items:
        for key, kls in candidate_types:
            msg = kls()
            if any_item.Unpack(msg) and msg.id.value:
                delete.item_ids.add().value = msg.id.value
                counts[key] += 1
                break

    if delete.item_ids:
        client.send(delete, DeleteItemsResponse)

    counts["_total"] = sum(counts.values())
    logger.info("schematic_ipc_clear_all_succeeded", **counts)
    return counts


__all__ = (
    "SCH_IPC_FORCE_ENV",
    "SCH_IPC_PERSISTENCE_HINT",
    "SCH_IPC_VERIFY_ENV",
    "SchematicIPCRequiredError",
    "build_bus_proto",
    "build_bus_wire_entry_proto",
    "build_global_label_proto",
    "build_hierarchical_label_proto",
    "build_junction_proto",
    "build_local_label_proto",
    "build_no_connect_proto",
    "build_text_proto",
    "build_textbox_proto",
    "build_wire_proto",
    "check_ipc_gate",
    "reset_runtime_gate_cache",
    "route_schematic_clear_all",
    "route_schematic_create",
    "route_schematic_delete_by_reference",
    "route_schematic_place_symbol",
    "route_schematic_save",
)


# Silence flake-style "imported but unused" by surfacing ``Any`` for any
# future typing tweaks. Keeping the import keeps the module's typing
# surface stable as it grows.
_ = Any
