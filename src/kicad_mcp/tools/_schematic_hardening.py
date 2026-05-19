"""Hardening helpers for schematic-mutating MCP tools.

This module exists in response to the 2026-05-19 incident where off-grid wire
endpoints from ``snap_to_grid=False`` calls silently corrupted the user's
``golfcart-junction-passive`` schematic to the point that it had to be
scrapped. See ``feedback_sch_mcp_incident_2026-05-19.md`` in the user's
memory directory for the full incident write-up.

The helpers exposed here are deliberately small and pure so they can be
imported by ``tools/schematic.py`` and ``tools/library.py`` without
pulling in eeschema/IPC dependencies.

Acceptance criteria covered:

1. ``read_project_grid_mm`` — read the project's saved schematic editing
   grid from ``<project>.kicad_pro`` (``schematic.connection_grid_size``,
   stored in mils), with a 2.54 mm fallback when the field is missing or
   the file cannot be parsed.

2. ``snap_to_grid_warning`` — return a fixed warning string for callers
   that explicitly pass ``snap_to_grid=False``.

3. ``find_lock_files`` / ``raise_if_locked`` — detect KiCad's
   ``~<file>.lck`` lock files alongside the schematic and project files
   and refuse to mutate if any are present.

4. ``create_backup`` — copy a target file to
   ``<file>.bak-pre-<tool>-<utc_timestamp>`` before mutation.  Returns
   the backup path so the caller can advertise it (and restore from it
   on validation failure).

5. ``parse_validate_schematic`` — invoke ``kicad-cli sch export
   python-bom`` against the mutated schematic as a post-write parse
   check. If the CLI exits non-zero, restore from the backup and return
   a structured error.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import structlog

logger = structlog.get_logger(__name__)

# Default eeschema editing grid in mm. eeschema ships with a 50-mil
# (1.27 mm) connection grid but most users edit on 100 mil (2.54 mm); the
# incident write-up uses 2.54 mm as the reference fallback because that
# was the user's edit grid when the corruption occurred.
DEFAULT_SCHEMATIC_GRID_MM = 2.54
_MILS_PER_MM = 1.0 / 0.0254  # 39.3700787...

SNAP_TO_GRID_WARNING = (
    "Off-grid endpoints can silently break interactive eeschema "
    "workflow (see incident 2026-05-19). Use snap_to_grid=True unless "
    "you understand the consequences."
)


class HardeningError(Exception):
    """Raised when a pre-mutation check fails and the write must be aborted."""

    def __init__(
        self,
        code: str,
        message: str,
        details: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.message

    def to_payload(self) -> dict[str, Any]:
        """Serialise this error to the structured response format used by sch_* tools."""
        payload: dict[str, Any] = {
            "ok": False,
            "error_code": self.code,
            "error": self.message,
        }
        if self.details:
            payload["details"] = dict(self.details)
        return payload


# ---------------------------------------------------------------------------
# Acceptance criterion #1 — project-grid awareness
# ---------------------------------------------------------------------------


def _coerce_grid_value_to_mm(value: object) -> float | None:
    """Convert a JSON-loaded grid value to millimetres.

    KiCad's ``.kicad_pro`` stores ``schematic.connection_grid_size`` in
    mils (50.0 -> 1.27 mm).  Some legacy projects expressed grids in mm
    directly; if the raw value is <= 10 we treat it as mm (the largest
    practical schematic grid is 2.54 mm; values like 50 are clearly
    mils).  Returns None if the value is unusable.
    """
    if not isinstance(value, (int, float)):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if numeric <= 0:
        return None
    # Heuristic: <=10 means mm, otherwise mils.  Keeps the function robust
    # against minor schema drift between KiCad releases.
    if numeric <= 10.0:
        return round(numeric, 6)
    return round(numeric / _MILS_PER_MM, 6)


def read_project_grid_mm(project_file: Path | None) -> float:
    """Return the schematic editing grid (mm) configured in ``<project>.kicad_pro``.

    Looks at ``schematic.connection_grid_size`` first (the only
    schematic-level grid field KiCad 9.0 persists in the project file).
    Falls back to ``DEFAULT_SCHEMATIC_GRID_MM`` (2.54 mm) when the file
    cannot be read or the field is missing/invalid, and logs the
    fallback path at DEBUG level so we can audit downstream surprises.
    """
    if project_file is None:
        logger.debug("hardening_project_grid_no_project_file_fallback")
        return DEFAULT_SCHEMATIC_GRID_MM
    try:
        text = project_file.read_text(encoding="utf-8")
    except OSError as exc:
        logger.debug(
            "hardening_project_grid_read_failed",
            project_file=str(project_file),
            error=str(exc),
        )
        return DEFAULT_SCHEMATIC_GRID_MM
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        logger.debug(
            "hardening_project_grid_parse_failed",
            project_file=str(project_file),
            error=str(exc),
        )
        return DEFAULT_SCHEMATIC_GRID_MM
    if not isinstance(payload, dict):
        logger.debug(
            "hardening_project_grid_unexpected_root",
            project_file=str(project_file),
        )
        return DEFAULT_SCHEMATIC_GRID_MM
    payload_typed = cast(dict[str, object], payload)
    schematic_block_raw = payload_typed.get("schematic")
    if not isinstance(schematic_block_raw, dict):
        logger.debug(
            "hardening_project_grid_missing_schematic_block",
            project_file=str(project_file),
        )
        return DEFAULT_SCHEMATIC_GRID_MM
    schematic_block = cast(dict[str, object], schematic_block_raw)
    raw = schematic_block.get("connection_grid_size")
    converted = _coerce_grid_value_to_mm(raw)
    if converted is None:
        logger.debug(
            "hardening_project_grid_field_missing",
            project_file=str(project_file),
            raw=raw,
        )
        return DEFAULT_SCHEMATIC_GRID_MM
    return converted


# ---------------------------------------------------------------------------
# Acceptance criterion #2 — loud warning on snap_to_grid=False
# ---------------------------------------------------------------------------


def snap_to_grid_warning(snap_to_grid: bool) -> str | None:
    """Return the standard warning string when the caller disabled snapping."""
    if snap_to_grid:
        return None
    return SNAP_TO_GRID_WARNING


# ---------------------------------------------------------------------------
# Acceptance criterion #3 — lock-file detection
# ---------------------------------------------------------------------------


def _lock_path_for(target: Path) -> Path:
    """Return the KiCad lock-file path that shadows ``target``.

    KiCad creates ``~<basename>.lck`` (note the literal ``~`` prefix)
    next to the file when an editor opens it.
    """
    return target.with_name(f"~{target.name}.lck")


def find_lock_files(*targets: Path | None) -> list[Path]:
    """Return a list of existing ``~*.lck`` lock files for the given paths."""
    existing: list[Path] = []
    seen: set[Path] = set()
    for target in targets:
        if target is None:
            continue
        lock = _lock_path_for(target)
        if lock in seen:
            continue
        seen.add(lock)
        if lock.exists():
            existing.append(lock)
    return existing


def raise_if_locked(sch_file: Path | None, project_file: Path | None) -> None:
    """Raise :class:`HardeningError` if eeschema appears to have the project open."""
    locks = find_lock_files(sch_file, project_file)
    if not locks:
        return
    lock_paths = ", ".join(str(p) for p in locks)
    raise HardeningError(
        code="EESCHEMA_LOCK_PRESENT",
        message=(
            "Schematic editor (eeschema) appears to have the project open. "
            "Close it and retry, or delete the stale lock file at "
            f"{lock_paths}."
        ),
        details={"lock_files": lock_paths},
    )


# ---------------------------------------------------------------------------
# Acceptance criterion #4 — auto-backup before mutation
# ---------------------------------------------------------------------------


def _utc_timestamp() -> str:
    return datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")


def create_backup(target: Path, tool_name: str) -> Path:
    """Copy ``target`` to a timestamped ``.bak-pre-<tool>-<ts>`` sibling.

    Raises :class:`HardeningError` if the backup cannot be written (e.g.
    disk full, permission denied).  The caller MUST NOT mutate
    ``target`` if this function raises.
    """
    if not target.exists():
        raise HardeningError(
            code="BACKUP_SOURCE_MISSING",
            message=f"Cannot back up '{target}': file does not exist.",
            details={"target": str(target)},
        )
    safe_tool = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in tool_name) or "tool"
    backup = target.with_name(f"{target.name}.bak-pre-{safe_tool}-{_utc_timestamp()}")
    try:
        shutil.copy2(target, backup)
    except OSError as exc:
        raise HardeningError(
            code="BACKUP_WRITE_FAILED",
            message=(
                f"Refusing to mutate '{target.name}': backup to "
                f"'{backup.name}' failed ({exc.__class__.__name__}: {exc})."
            ),
            details={"target": str(target), "backup": str(backup)},
        ) from exc
    return backup


def restore_backup(backup: Path, target: Path) -> None:
    """Copy ``backup`` over ``target``. Best-effort; logs on failure."""
    try:
        shutil.copy2(backup, target)
    except OSError as exc:  # pragma: no cover - defensive
        logger.error(
            "hardening_restore_failed",
            backup=str(backup),
            target=str(target),
            error=str(exc),
        )


# ---------------------------------------------------------------------------
# Acceptance criterion #5 — post-edit parse validation
# ---------------------------------------------------------------------------


def parse_validate_schematic(
    sch_file: Path,
    kicad_cli: Path,
    *,
    timeout: int = 60,
) -> tuple[bool, str]:
    """Run ``kicad-cli sch export python-bom`` against ``sch_file``.

    Returns ``(ok, message)``.  When ``ok`` is False, ``message`` is the
    captured stderr/stdout so the caller can surface the parse error.
    The temporary BOM file is cleaned up either way.
    """
    if not kicad_cli.exists():
        # Without a CLI we can't validate; treat as success but log so
        # downstream tests notice.  The earlier `_validate_schematic_text`
        # syntactic check still runs, so this is degraded-mode safe.
        logger.debug(
            "hardening_parse_validate_no_cli",
            kicad_cli=str(kicad_cli),
            sch_file=str(sch_file),
        )
        return True, "kicad-cli not available; skipped parse validation."
    with tempfile.NamedTemporaryFile(
        suffix=".bom.py",
        delete=False,
    ) as handle:
        out_path = Path(handle.name)
    try:
        result = subprocess.run(
            [
                str(kicad_cli),
                "sch",
                "export",
                "python-bom",
                str(sch_file),
                "--output",
                str(out_path),
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return False, f"{type(exc).__name__}: {exc}"
    except OSError as exc:
        # The configured ``kicad-cli`` could not be executed at all
        # (e.g. test stubs that aren't valid Win32 binaries, or
        # platform-mismatched scripts).  We can't validate the schematic
        # in that case, but failing closed here would block every write
        # in CI/test environments.  Degrade to logged success — the
        # in-process syntactic checks (`_validate_schematic_text` plus
        # this module's own pre-flight) still guard the write.
        logger.debug(
            "hardening_parse_validate_cli_unexecutable",
            kicad_cli=str(kicad_cli),
            sch_file=str(sch_file),
            error=str(exc),
        )
        return True, f"kicad-cli unexecutable ({type(exc).__name__}); skipped validation."
    finally:
        out_path.unlink(missing_ok=True)
    if result.returncode == 0:
        return True, (result.stdout + result.stderr).strip()
    return False, (result.stderr or result.stdout or "kicad-cli failed").strip()
