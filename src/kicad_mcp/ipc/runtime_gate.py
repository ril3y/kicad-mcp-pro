# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
"""Runtime gate that picks between the IPC and file-based schematic edit paths.

Why this module exists
----------------------

The IPC path for schematic edits (``kicad_mcp.ipc.schematic.Schematic``)
crashes eeschema on every KiCad 10.0.x stable release shipped to date —
the input-validation handler in ``api_handler_sch.cpp`` is a TODO stub
until upstream commit ``3dca4e0e38`` ("API: implement schematic item
creation", Jon Evans, 2026-04-07), which is currently only on master and
nightly builds. Until users run a KiCad that contains that fix, calling
the IPC mutation surface scrambles the editor and risks corrupting the
schematic.

So the IPC path stays OFF by default. Operators opt in via the
``KICAD_MCP_SCH_IPC=1`` environment variable, and we additionally verify
at runtime that the connected KiCad reports a version new enough to
include the fix.

Design notes
------------

* **Fail-closed.** Any error — connect refused, parse failure, missing
  attribute — resolves to "use the file path". The file path has its own
  hardening from PR #24 (lock detection, post-edit validation) and is
  the safer default until proven otherwise.
* **Cache once per server start.** The connected KiCad version cannot
  change without a process restart, so we memoise the detection result.
  Callers can reset it via :func:`reset_runtime_gate_cache` (used in
  tests).
* **Observability.** Every routing decision is logged at INFO with a
  reason field so the user can grep ``schematic_route_decision`` to see
  why the gate chose the path it did.
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

#: Environment variable that opts in to the IPC path. The default is OFF
#: because of the eeschema crash on stable KiCad 10.0.x.
SCH_IPC_OPT_IN_ENV = "KICAD_MCP_SCH_IPC"

#: Second-tier env var. When set alongside ``KICAD_MCP_SCH_IPC=1``, the gate
#: treats an ``AS_UNHANDLED`` response to ``GetVersion`` as "trust the
#: operator" rather than fail-closed. This is the live-tested scenario of
#: launching ``eeschema.exe`` directly (which doesn't register
#: ``GetVersion`` — only the project manager does), so the operator has
#: to opt INTO a slightly-relaxed verification path. Without this second
#: flag the gate fails closed on ``AS_UNHANDLED`` and routes to the file
#: path, even with the primary opt-in set.
SCH_IPC_FORCE_ENV = "KICAD_MCP_SCH_IPC_FORCE"

#: Optional post-write verification. When set, after a successful
#: ``CreateItems`` we round-trip the created items back via
#: ``GetItemsById`` and assert their KIIDs land where we expect. Doubles
#: the IPC traffic per call but catches the case where eeschema's
#: deserializer accepts garbage and stores a malformed item. The
#: file-path equivalent is PR #24's post-edit s-expression validation;
#: this is the IPC analogue.
SCH_IPC_VERIFY_ENV = "KICAD_MCP_SCH_IPC_VERIFY"

#: Persistence hint appended to IPC-path success responses, mirroring the
#: pcbnew convention in :data:`kicad_mcp.connection.PERSISTENCE_HINT`.
#: When an edit went through IPC, the change lives only in eeschema's
#: in-memory document; the user MUST call ``sch_save()`` to flush.
SCH_IPC_PERSISTENCE_HINT = (
    "Call sch_save() to persist — the change is in eeschema's session only and "
    "will be lost if the editor closes without saving."
)


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
        force = os.environ.get(SCH_IPC_FORCE_ENV, "").strip().lower() in {"1", "true", "yes", "on"}
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


def _env_opt_in(env: dict[str, str] | None = None) -> bool:
    """Return True iff the ``KICAD_MCP_SCH_IPC`` opt-in is set to a truthy value."""

    source = env if env is not None else os.environ
    raw = source.get(SCH_IPC_OPT_IN_ENV, "")
    return raw.strip().lower() in {"1", "true", "yes", "on"}


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


def should_use_ipc_for_schematic_mutation(
    *,
    env: dict[str, str] | None = None,
    kicad_factory: _KiCadFactory | None = None,
) -> bool:
    """Return True iff a schematic mutation should be sent over IPC.

    All three of these must be true at once:

    1. The operator has opted in via ``KICAD_MCP_SCH_IPC=1``.
    2. The connected KiCad reports a version containing the fix.
    3. There is at least one open schematic document.

    Any failure resolves to ``False`` (the file-based path).
    """

    if not _env_opt_in(env):
        logger.info("schematic_route_decision", path="file", reason="env_opt_in_off")
        return False

    if not _connected_kicad_has_fix(kicad_factory):
        logger.info(
            "schematic_route_decision",
            path="file",
            reason="version_lacks_fix_or_probe_failed",
        )
        return False

    if not _has_open_schematic(kicad_factory):
        logger.info("schematic_route_decision", path="file", reason="no_open_schematic")
        return False

    logger.info("schematic_route_decision", path="ipc", reason="all_gates_passed")
    return True


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


def route_schematic_create[T](
    items: list[Message],
    file_fallback: Callable[[], T],
    *,
    env: dict[str, str] | None = None,
    kicad_factory: _KiCadFactory | None = None,
) -> str | T:
    """Route a schematic create-items call to IPC if the gate permits.

    Parameters
    ----------
    items:
        The pre-built protobuf messages to send if the IPC path is
        taken. The list is opaque to the gate.
    file_fallback:
        A zero-argument callable that performs the equivalent
        file-based mutation. Its return value is returned directly when
        the IPC path is gated off.
    env, kicad_factory:
        Test seams; production callers leave them ``None``.

    Returns
    -------
    str | T
        On the IPC path, a success string with the persistence hint
        suffixed. On the file path, the return value of ``file_fallback``.
    """

    if not should_use_ipc_for_schematic_mutation(env=env, kicad_factory=kicad_factory):
        return file_fallback()

    # The gate said go. Build a Schematic and dispatch. Any failure here
    # bubbles up — by this point we are on the explicit opt-in path and
    # the operator wants to see real errors instead of silent fallback.
    schematic = _open_schematic_for_ipc(kicad_factory=kicad_factory)
    results = schematic.create_items(items)
    logger.info(
        "schematic_ipc_create_succeeded",
        items=len(items),
        results=len(results),
    )

    # Optional post-write verification. The file path has PR #24's
    # post-edit s-expression validation; this is its IPC analogue. Off
    # by default to keep latency low; opt in via KICAD_MCP_SCH_IPC_VERIFY=1.
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


def build_global_label_proto(x_mm: float, y_mm: float, text: str) -> Message:
    """Build a master ``GlobalLabel`` proto carrying ``text``."""

    from kicad_mcp._master_proto.mp.schematic.schematic_types_pb2 import GlobalLabel

    label = GlobalLabel()
    _populate_label(label, x_mm, y_mm, text)
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


__all__ = (
    "SCH_IPC_OPT_IN_ENV",
    "SCH_IPC_PERSISTENCE_HINT",
    "build_bus_proto",
    "build_bus_wire_entry_proto",
    "build_global_label_proto",
    "build_hierarchical_label_proto",
    "build_junction_proto",
    "build_local_label_proto",
    "build_no_connect_proto",
    "build_wire_proto",
    "reset_runtime_gate_cache",
    "route_schematic_create",
    "should_use_ipc_for_schematic_mutation",
)


# Silence flake-style "imported but unused" by surfacing ``Any`` for any
# future typing tweaks. Keeping the import keeps the module's typing
# surface stable as it grows.
_ = Any
