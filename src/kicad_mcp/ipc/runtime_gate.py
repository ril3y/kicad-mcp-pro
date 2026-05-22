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
        # Imported lazily: bringing in ``connection`` at module scope
        # would create a circular dependency through ``tools.schematic``
        # which already imports from ``..connection``.
        from ..connection import get_kicad

        kicad_factory = get_kicad

    try:
        kicad = kicad_factory()
        version = kicad.get_version()
        full = str(getattr(version, "full_version", "") or "")
        has_fix = _full_version_has_fix(full)
    except Exception as exc:
        # Fail-closed: any error (no socket, parse failure, missing
        # attribute) flips the gate off so we keep using the file path.
        logger.info(
            "schematic_ipc_version_probe_failed",
            error_type=type(exc).__name__,
            error=str(exc),
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
        from ..connection import get_kicad

        kicad_factory = get_kicad

    try:
        # Imported lazily here too — see ``_connected_kicad_has_fix``.
        from kipy.proto.common.types import DocumentType

        kicad = kicad_factory()
        docs = list(kicad.get_open_documents(DocumentType.DOCTYPE_SCHEMATIC))
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
        from ..connection import get_kicad

        kicad_factory = get_kicad

    # Imported lazily: keeps the gate module importable even when the
    # heavy proto stubs in ``ipc.schematic`` are not needed.
    from kipy.proto.common.types import DocumentType

    from .schematic import Schematic

    kicad = kicad_factory()
    docs = list(kicad.get_open_documents(DocumentType.DOCTYPE_SCHEMATIC))
    if not docs:
        # The caller should have already gated on
        # ``should_use_ipc_for_schematic_mutation``; this branch is a
        # defensive guard for race conditions (user closes eeschema
        # between the gate check and the open call).
        raise RuntimeError(
            "No schematic document is open in eeschema. Cannot dispatch schematic IPC mutation."
        )
    return Schematic(kicad, docs[0])


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
    return f"Added {len(items)} schematic item(s) via IPC. {SCH_IPC_PERSISTENCE_HINT}"


# ---------------------------------------------------------------------------
# Proto builders for the four wired sch_add_* tools
#
# These live here so the tool wrappers in ``tools/schematic.py`` do not
# have to import kipy proto types — keeping the IPC proto surface
# isolated to this package eases version-skew triage.
# ---------------------------------------------------------------------------


def build_global_label_proto(x_mm: float, y_mm: float, text: str) -> Message:
    """Build a ``GlobalLabel`` protobuf carrying ``text`` at ``(x_mm, y_mm)``."""

    from kipy.geometry import Vector2
    from kipy.proto.schematic.schematic_types_pb2 import GlobalLabel

    label = GlobalLabel()
    position = Vector2.from_xy_mm(x_mm, y_mm)
    label.position.CopyFrom(position.proto)
    label.text.text.text = text
    return label


def build_local_label_proto(x_mm: float, y_mm: float, text: str) -> Message:
    """Build a ``LocalLabel`` protobuf carrying ``text`` at ``(x_mm, y_mm)``."""

    from kipy.geometry import Vector2
    from kipy.proto.schematic.schematic_types_pb2 import LocalLabel

    label = LocalLabel()
    position = Vector2.from_xy_mm(x_mm, y_mm)
    label.position.CopyFrom(position.proto)
    label.text.text.text = text
    return label


def build_hierarchical_label_proto(x_mm: float, y_mm: float, text: str) -> Message:
    """Build a ``HierarchicalLabel`` protobuf carrying ``text`` at ``(x_mm, y_mm)``."""

    from kipy.geometry import Vector2
    from kipy.proto.schematic.schematic_types_pb2 import HierarchicalLabel

    label = HierarchicalLabel()
    position = Vector2.from_xy_mm(x_mm, y_mm)
    label.position.CopyFrom(position.proto)
    label.text.text.text = text
    return label


def build_wire_proto(x1_mm: float, y1_mm: float, x2_mm: float, y2_mm: float) -> Message:
    """Build a ``Line`` protobuf for a schematic wire on ``LAYER_WIRE``.

    The installed kipy ships ``SchematicLayer`` with only ``SL_UNKNOWN``;
    we read the layer enum the same way :class:`Schematic.add_wire` does
    so that as soon as kipy exposes ``LAYER_WIRE``, this code uses it
    automatically.
    """

    from kipy.geometry import Vector2
    from kipy.proto.schematic.schematic_types_pb2 import Line, SchematicLayer

    layer_wire = getattr(SchematicLayer, "LAYER_WIRE", SchematicLayer.SL_UNKNOWN)
    line = Line()
    start = Vector2.from_xy_mm(x1_mm, y1_mm)
    end = Vector2.from_xy_mm(x2_mm, y2_mm)
    line.start.CopyFrom(start.proto)
    line.end.CopyFrom(end.proto)
    line.layer = layer_wire
    return line


__all__ = (
    "SCH_IPC_OPT_IN_ENV",
    "SCH_IPC_PERSISTENCE_HINT",
    "build_global_label_proto",
    "build_hierarchical_label_proto",
    "build_local_label_proto",
    "build_wire_proto",
    "reset_runtime_gate_cache",
    "route_schematic_create",
    "should_use_ipc_for_schematic_mutation",
)


# Silence flake-style "imported but unused" by surfacing ``Any`` for any
# future typing tweaks. Keeping the import keeps the module's typing
# surface stable as it grows.
_ = Any
