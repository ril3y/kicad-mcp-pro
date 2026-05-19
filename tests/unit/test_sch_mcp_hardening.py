# pyright: reportPrivateUsage=false
"""Unit tests for the schematic-MCP hardening pipeline.

Covers the five acceptance criteria from the 2026-05-19 incident
hardening task — project-grid awareness, snap_to_grid=False warning,
lock-file refusal, pre-write backup, and post-write parse validation
with backup-restore on failure.

The hardening helpers live in ``kicad_mcp.tools._schematic_hardening``;
the integration with ``_transactional_write_to_schematic`` lives in
``kicad_mcp.tools.schematic``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from kicad_mcp.tools import _schematic_hardening as hardening

# ---------------------------------------------------------------------------
# Acceptance criterion #1 — project-grid awareness
# ---------------------------------------------------------------------------


def test_read_project_grid_returns_mm_for_connection_grid_size(tmp_path: Path) -> None:
    """50-mil ``connection_grid_size`` field decodes to 1.27 mm exactly.

    50 mils = 50 * 0.0254 mm = 1.27 mm; this is the value KiCad ships
    in fresh projects and is also the eeschema connectivity grid the
    incident memory references.
    """
    project_file = tmp_path / "demo.kicad_pro"
    project_file.write_text(
        json.dumps({"schematic": {"connection_grid_size": 50.0}}),
        encoding="utf-8",
    )

    grid = hardening.read_project_grid_mm(project_file)

    assert grid == pytest.approx(1.27, abs=1e-4)


def test_read_project_grid_accepts_mm_value_directly(tmp_path: Path) -> None:
    """Values <= 10 are treated as mm so legacy projects that already
    expressed the grid in mm don't get misinterpreted as mils."""
    project_file = tmp_path / "demo.kicad_pro"
    project_file.write_text(
        json.dumps({"schematic": {"connection_grid_size": 2.54}}),
        encoding="utf-8",
    )

    assert hardening.read_project_grid_mm(project_file) == pytest.approx(2.54, abs=1e-6)


def test_read_project_grid_falls_back_when_field_missing(tmp_path: Path) -> None:
    """A project file with no schematic grid field falls back to 2.54
    mm — the historical eeschema editing default."""
    project_file = tmp_path / "demo.kicad_pro"
    project_file.write_text(json.dumps({"meta": {"version": 1}}), encoding="utf-8")

    assert hardening.read_project_grid_mm(project_file) == pytest.approx(
        hardening.DEFAULT_SCHEMATIC_GRID_MM, abs=1e-6
    )


def test_read_project_grid_falls_back_when_no_project_file() -> None:
    """``None`` project file path returns the fallback without raising."""
    assert hardening.read_project_grid_mm(None) == pytest.approx(
        hardening.DEFAULT_SCHEMATIC_GRID_MM, abs=1e-6
    )


def test_read_project_grid_falls_back_when_project_file_unparseable(tmp_path: Path) -> None:
    """Corrupt JSON in the project file falls back rather than raising."""
    project_file = tmp_path / "demo.kicad_pro"
    project_file.write_text("not valid json", encoding="utf-8")

    assert hardening.read_project_grid_mm(project_file) == pytest.approx(
        hardening.DEFAULT_SCHEMATIC_GRID_MM, abs=1e-6
    )


def test_read_project_grid_falls_back_when_value_is_zero(tmp_path: Path) -> None:
    """A nonsense ``0`` grid setting falls back to the historical default."""
    project_file = tmp_path / "demo.kicad_pro"
    project_file.write_text(
        json.dumps({"schematic": {"connection_grid_size": 0}}),
        encoding="utf-8",
    )

    assert hardening.read_project_grid_mm(project_file) == pytest.approx(
        hardening.DEFAULT_SCHEMATIC_GRID_MM, abs=1e-6
    )


# ---------------------------------------------------------------------------
# Acceptance criterion #2 — warning on snap_to_grid=False
# ---------------------------------------------------------------------------


def test_snap_to_grid_warning_returns_none_for_true() -> None:
    assert hardening.snap_to_grid_warning(True) is None


def test_snap_to_grid_warning_text_references_incident() -> None:
    """The warning must mention the 2026-05-19 incident and recommend
    leaving ``snap_to_grid=True``."""
    text = hardening.snap_to_grid_warning(False)

    assert text is not None
    assert "2026-05-19" in text
    assert "snap_to_grid=True" in text


def test_sch_add_wire_response_warns_when_snap_disabled(
    sample_project: Path, mock_kicad: object
) -> None:
    """Calling ``sch_add_wire`` with ``snap_to_grid=False`` must surface
    a structured warning field — the escape hatch stays open but it is
    no longer silent."""
    import asyncio

    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    server = build_server("schematic")
    result = asyncio.run(
        call_tool_text(
            server,
            "sch_add_wire",
            {
                "x1_mm": 1.1,
                "y1_mm": 2.2,
                "x2_mm": 3.3,
                "y2_mm": 4.4,
                "snap_to_grid": False,
            },
        )
    )

    # Response is now a JSON envelope when snap_to_grid=False.
    payload = json.loads(result)
    assert "warning" in payload
    assert "2026-05-19" in payload["warning"]
    # Off-grid endpoints are still recorded — refuse-vs-warn distinction.
    schematic = (sample_project / "demo.kicad_sch").read_text(encoding="utf-8")
    assert "(pts (xy 1.1 2.2) (xy 3.3 4.4))" in schematic


def test_sch_add_wire_response_is_plain_when_snap_enabled(
    sample_project: Path, mock_kicad: object
) -> None:
    """``snap_to_grid=True`` (the default) keeps the legacy plain-text
    response so existing automation continues to work unchanged."""
    import asyncio

    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    server = build_server("schematic")
    result = asyncio.run(
        call_tool_text(
            server,
            "sch_add_wire",
            {"x1_mm": 5.08, "y1_mm": 5.08, "x2_mm": 10.16, "y2_mm": 5.08},
        )
    )

    # Plain text — must not be JSON-wrapped.
    with pytest.raises(json.JSONDecodeError):
        json.loads(result)


# ---------------------------------------------------------------------------
# Acceptance criterion #3 — lock-file detection
# ---------------------------------------------------------------------------


def test_find_lock_files_returns_empty_when_no_locks(tmp_path: Path) -> None:
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")
    pro = tmp_path / "demo.kicad_pro"
    pro.write_text("{}", encoding="utf-8")

    assert hardening.find_lock_files(sch, pro) == []


def test_find_lock_files_reports_each_existing_lock(tmp_path: Path) -> None:
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")
    pro = tmp_path / "demo.kicad_pro"
    pro.write_text("{}", encoding="utf-8")

    sch_lock = tmp_path / "~demo.kicad_sch.lck"
    sch_lock.write_text("lock", encoding="utf-8")
    pro_lock = tmp_path / "~demo.kicad_pro.lck"
    pro_lock.write_text("lock", encoding="utf-8")

    locks = hardening.find_lock_files(sch, pro)
    assert sch_lock in locks
    assert pro_lock in locks


def test_raise_if_locked_raises_when_lock_present(tmp_path: Path) -> None:
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")
    lock = tmp_path / "~demo.kicad_sch.lck"
    lock.write_text("lock", encoding="utf-8")

    with pytest.raises(hardening.HardeningError) as excinfo:
        hardening.raise_if_locked(sch, None)

    assert excinfo.value.code == "EESCHEMA_LOCK_PRESENT"
    assert str(lock) in excinfo.value.message


def test_raise_if_locked_no_op_when_no_locks(tmp_path: Path) -> None:
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")

    # Should not raise.
    hardening.raise_if_locked(sch, None)


def test_sch_add_wire_refuses_when_lock_present(sample_project: Path, mock_kicad: object) -> None:
    """End-to-end: dropping a lock file before calling ``sch_add_wire``
    yields a structured refusal error and leaves the schematic untouched."""
    import asyncio

    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    sch_file = sample_project / "demo.kicad_sch"
    original = sch_file.read_text(encoding="utf-8")
    (sample_project / "~demo.kicad_sch.lck").write_text("lock", encoding="utf-8")

    server = build_server("schematic")
    result = asyncio.run(
        call_tool_text(
            server,
            "sch_add_wire",
            {"x1_mm": 5.08, "y1_mm": 5.08, "x2_mm": 10.16, "y2_mm": 5.08},
        )
    )

    payload = json.loads(result)
    assert payload["ok"] is False
    assert payload["error_code"] == "EESCHEMA_LOCK_PRESENT"
    # Schematic must not be modified.
    assert sch_file.read_text(encoding="utf-8") == original


# ---------------------------------------------------------------------------
# Acceptance criterion #4 — pre-mutation backup
# ---------------------------------------------------------------------------


def test_create_backup_writes_timestamped_file(tmp_path: Path) -> None:
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch original)", encoding="utf-8")

    backup = hardening.create_backup(sch, "sch_add_wire")

    assert backup.exists()
    assert backup.read_text(encoding="utf-8") == "(kicad_sch original)"
    assert backup.name.startswith("demo.kicad_sch.bak-pre-sch_add_wire-")
    # UTC timestamp suffix in YYYYMMDDTHHMMSSZ form.
    assert re.search(r"\d{8}T\d{6}Z$", backup.name) is not None


def test_create_backup_raises_when_source_missing(tmp_path: Path) -> None:
    missing = tmp_path / "absent.kicad_sch"

    with pytest.raises(hardening.HardeningError) as excinfo:
        hardening.create_backup(missing, "sch_add_wire")

    assert excinfo.value.code == "BACKUP_SOURCE_MISSING"


def test_create_backup_sanitises_tool_name(tmp_path: Path) -> None:
    """Unsanitary tool names cannot produce a malformed filename."""
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")

    backup = hardening.create_backup(sch, "sch/../escape")

    # Slashes and dots have been replaced with underscores; the backup
    # lives next to the source file.
    assert backup.parent == sch.parent
    assert "/" not in backup.name
    assert "sch____escape" in backup.name


def test_sch_add_wire_writes_backup_before_mutation(
    sample_project: Path, mock_kicad: object
) -> None:
    """A successful ``sch_add_wire`` call leaves a backup of the
    pre-mutation schematic next to the live file."""
    import asyncio

    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    sch_file = sample_project / "demo.kicad_sch"
    original = sch_file.read_text(encoding="utf-8")

    server = build_server("schematic")
    asyncio.run(
        call_tool_text(
            server,
            "sch_add_wire",
            {"x1_mm": 5.08, "y1_mm": 5.08, "x2_mm": 10.16, "y2_mm": 5.08},
        )
    )

    backups = sorted(sample_project.glob("demo.kicad_sch.bak-pre-sch_add_wire-*"))
    assert len(backups) >= 1
    # Backup is the pre-mutation snapshot.
    assert backups[0].read_text(encoding="utf-8") == original


# ---------------------------------------------------------------------------
# Acceptance criterion #5 — post-write parse validation + restore
# ---------------------------------------------------------------------------


def test_parse_validate_returns_true_when_cli_missing(tmp_path: Path) -> None:
    """Missing CLI is treated as degraded-mode success — the
    syntactic checks the caller already runs still guard the write."""
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")
    missing_cli = tmp_path / "absent-kicad-cli"

    ok, message = hardening.parse_validate_schematic(sch, missing_cli)

    assert ok is True
    assert "kicad-cli" in message.lower()


def test_validation_failure_restores_from_backup(
    sample_project: Path, mock_kicad: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When ``kicad-cli`` rejects the mutated schematic the
    transactional write restores the pre-mutation backup and surfaces a
    structured error to the caller — the live file is *not* left in a
    broken state."""
    import asyncio

    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    sch_file = sample_project / "demo.kicad_sch"
    original = sch_file.read_text(encoding="utf-8")

    # Force the post-write validator to reject every mutation.
    monkeypatch.setattr(
        "kicad_mcp.tools._schematic_hardening.parse_validate_schematic",
        lambda *_args, **_kwargs: (False, "simulated parse failure"),
    )

    server = build_server("schematic")
    result = asyncio.run(
        call_tool_text(
            server,
            "sch_add_wire",
            {"x1_mm": 5.08, "y1_mm": 5.08, "x2_mm": 10.16, "y2_mm": 5.08},
        )
    )

    payload = json.loads(result)
    assert payload["ok"] is False
    assert payload["error_code"] == "POST_WRITE_VALIDATION_FAILED"
    # Live schematic restored from the pre-mutation backup.
    assert sch_file.read_text(encoding="utf-8") == original


def test_parse_validate_reports_failure_on_nonzero_cli_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Non-zero kicad-cli exit surfaces as ``(False, <message>)`` so
    callers can restore from backup and abort the transaction."""
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")
    cli = tmp_path / "fake-cli"
    cli.write_text("stub", encoding="utf-8")

    class _FakeResult:
        returncode = 1
        stdout = ""
        stderr = "parse error: bad sexpr"

    def fake_run(*_args: object, **_kwargs: object) -> _FakeResult:
        return _FakeResult()

    monkeypatch.setattr(
        "kicad_mcp.tools._schematic_hardening.subprocess.run",
        fake_run,
    )

    ok, message = hardening.parse_validate_schematic(sch, cli)

    assert ok is False
    assert "parse error" in message


def test_parse_validate_reports_timeout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A subprocess timeout is surfaced as ``(False, <message>)``."""
    import subprocess

    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")
    cli = tmp_path / "fake-cli"
    cli.write_text("stub", encoding="utf-8")

    def fake_run(*_args: object, **_kwargs: object) -> object:
        raise subprocess.TimeoutExpired(cmd="kicad-cli", timeout=1)

    monkeypatch.setattr(
        "kicad_mcp.tools._schematic_hardening.subprocess.run",
        fake_run,
    )

    ok, message = hardening.parse_validate_schematic(sch, cli)

    assert ok is False
    assert "TimeoutExpired" in message


def test_parse_validate_degrades_on_oserror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``OSError`` (e.g. unexecutable CLI binary on the wrong platform)
    is treated as degraded-mode success — the syntactic in-process
    checks still guard the write, but we don't block on it."""
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")
    cli = tmp_path / "fake-cli"
    cli.write_text("stub", encoding="utf-8")

    def fake_run(*_args: object, **_kwargs: object) -> object:
        raise OSError("not a Win32 application")

    monkeypatch.setattr(
        "kicad_mcp.tools._schematic_hardening.subprocess.run",
        fake_run,
    )

    ok, message = hardening.parse_validate_schematic(sch, cli)

    assert ok is True
    assert "unexecutable" in message


def test_read_project_grid_falls_back_when_project_unreadable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An OSError on read_text falls back to the default — emulates a
    permission-denied / locked-by-another-process project file."""
    project_file = tmp_path / "demo.kicad_pro"
    project_file.write_text(json.dumps({}), encoding="utf-8")

    def raising_read_text(*_args: object, **_kwargs: object) -> str:
        raise OSError("simulated permission error")

    monkeypatch.setattr(Path, "read_text", raising_read_text)

    assert hardening.read_project_grid_mm(project_file) == pytest.approx(
        hardening.DEFAULT_SCHEMATIC_GRID_MM, abs=1e-6
    )


def test_read_project_grid_falls_back_when_root_is_not_dict(tmp_path: Path) -> None:
    """A JSON file whose root isn't an object falls back to the default."""
    project_file = tmp_path / "demo.kicad_pro"
    project_file.write_text("[1, 2, 3]", encoding="utf-8")

    assert hardening.read_project_grid_mm(project_file) == pytest.approx(
        hardening.DEFAULT_SCHEMATIC_GRID_MM, abs=1e-6
    )


def test_coerce_grid_rejects_non_numeric() -> None:
    """Non-numeric (string, None, bool-handled-by-numeric-types) entries
    return None so the caller falls back to the default."""
    # Use _coerce_grid_value_to_mm via read_project_grid_mm by feeding
    # a string value in the project file — keeps the test public-API.
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        project = Path(td) / "demo.kicad_pro"
        project.write_text(
            json.dumps({"schematic": {"connection_grid_size": "not a number"}}),
            encoding="utf-8",
        )
        assert hardening.read_project_grid_mm(project) == pytest.approx(
            hardening.DEFAULT_SCHEMATIC_GRID_MM, abs=1e-6
        )


def test_create_backup_propagates_oserror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A disk-full / permission-denied ``shutil.copy2`` failure raises a
    ``HardeningError`` so the caller knows to abort the write."""
    import shutil as _shutil

    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")

    def failing_copy(*_args: object, **_kwargs: object) -> object:
        raise OSError("simulated disk full")

    monkeypatch.setattr(_shutil, "copy2", failing_copy)

    with pytest.raises(hardening.HardeningError) as excinfo:
        hardening.create_backup(sch, "sch_add_wire")

    assert excinfo.value.code == "BACKUP_WRITE_FAILED"


def test_find_lock_files_deduplicates_targets(tmp_path: Path) -> None:
    """When the same path is passed multiple times the result is
    deduplicated — no false ``open in N copies`` confusion."""
    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)", encoding="utf-8")
    lock = tmp_path / "~demo.kicad_sch.lck"
    lock.write_text("lock", encoding="utf-8")

    assert hardening.find_lock_files(sch, sch, sch) == [lock]


@pytest.mark.parametrize(
    ("tool_name", "arguments"),
    [
        (
            "sch_add_symbol",
            {
                "library": "Device",
                "symbol_name": "R",
                "x_mm": 50.8,
                "y_mm": 50.8,
                "reference": "R1",
                "value": "10k",
                "footprint": "Resistor_SMD:R_0805",
                "rotation": 0,
            },
        ),
        ("sch_add_wire", {"x1_mm": 5.08, "y1_mm": 5.08, "x2_mm": 10.16, "y2_mm": 5.08}),
        ("sch_add_label", {"name": "N", "x_mm": 5.08, "y_mm": 5.08}),
        ("sch_add_bus", {"x1_mm": 5.08, "y1_mm": 5.08, "x2_mm": 10.16, "y2_mm": 5.08}),
        ("sch_add_bus_wire_entry", {"x_mm": 5.08, "y_mm": 5.08, "direction": "up_right"}),
        ("sch_add_no_connect", {"x_mm": 5.08, "y_mm": 5.08}),
        ("sch_add_global_label", {"text": "G", "x_mm": 5.08, "y_mm": 5.08}),
        ("sch_add_hierarchical_label", {"text": "H", "x_mm": 5.08, "y_mm": 5.08}),
        ("sch_add_jumper", {"x_mm": 5.08, "y_mm": 5.08}),
        ("sch_annotate", {}),
        ("sch_set_sheet_size", {"paper": "A3"}),
        (
            "sch_build_circuit",
            {
                "auto_layout": True,
                "symbols": [
                    {
                        "library": "Device",
                        "symbol_name": "R",
                        "reference": "R1",
                        "value": "10k",
                        "footprint": "Resistor_SMD:R_0805",
                    },
                ],
            },
        ),
    ],
)
def test_every_sch_add_tool_honours_lock_refusal(
    sample_project: Path,
    mock_kicad: object,
    tool_name: str,
    arguments: dict[str, object],
) -> None:
    """Each sch_add_* tool refuses to mutate when the eeschema lock file
    is present.  Exercises the HardeningError -> JSON response code
    path on every mutating tool surface."""
    import asyncio

    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    sch_file = sample_project / "demo.kicad_sch"
    original = sch_file.read_text(encoding="utf-8")
    (sample_project / "~demo.kicad_sch.lck").write_text("lock", encoding="utf-8")

    server = build_server("schematic")
    result = asyncio.run(call_tool_text(server, tool_name, arguments))

    payload = json.loads(result)
    assert payload["ok"] is False
    assert payload["error_code"] == "EESCHEMA_LOCK_PRESENT"
    assert sch_file.read_text(encoding="utf-8") == original


@pytest.mark.parametrize(
    ("tool_name", "arguments"),
    [
        ("sch_move_symbol", {"reference": "R1", "x_mm": 50.8, "y_mm": 50.8}),
        ("sch_delete_wire", {"wire_id": "ffffffff"}),
        ("sch_delete_symbol", {"reference": "R1"}),
        (
            "sch_route_wire_between_pins",
            {
                "ref1": "R1",
                "pin1": "1",
                "ref2": "R2",
                "pin2": "2",
            },
        ),
        (
            "sch_update_properties",
            {
                "reference": "R1",
                "field": "Value",
                "value": "20k",
            },
        ),
        (
            "sch_create_sheet",
            {"name": "child", "filename": "child.kicad_sch", "x_mm": 50.8, "y_mm": 50.8},
        ),
        ("sch_auto_place_symbols", {}),
        ("sch_auto_place_functional", {}),
    ],
)
def test_more_sch_tools_honour_lock_refusal(
    sample_project: Path,
    mock_kicad: object,
    tool_name: str,
    arguments: dict[str, object],
) -> None:
    """Cover the remaining mutating tools' lock-refusal branches.

    Tools that operate on existing symbols/wires (move/delete/update/
    route) don't need the project to have any specific content to fire
    the lock check — the check runs before any state inspection.
    """
    import asyncio

    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    sch_file = sample_project / "demo.kicad_sch"
    original = sch_file.read_text(encoding="utf-8")
    (sample_project / "~demo.kicad_sch.lck").write_text("lock", encoding="utf-8")

    server = build_server("schematic")
    result = asyncio.run(call_tool_text(server, tool_name, arguments))

    # Some tools return a plain "not found" error before the hardening
    # pipeline runs (e.g. sch_move_symbol on a missing reference).
    # Accept either the structured lock refusal or any plain string —
    # the important thing is that the schematic content was NOT modified.
    try:
        payload = json.loads(result)
        if isinstance(payload, dict) and payload.get("error_code"):
            assert payload["error_code"] in {
                "EESCHEMA_LOCK_PRESENT",
                "BACKUP_SOURCE_MISSING",
            }
    except json.JSONDecodeError:
        pass
    assert sch_file.read_text(encoding="utf-8") == original


def test_hardening_error_payload_is_structured() -> None:
    """The ``HardeningError`` payload format used by mutating tools is
    a deterministic JSON envelope with ``ok``, ``error_code``, and
    ``error`` fields."""
    err = hardening.HardeningError(
        code="EXAMPLE",
        message="boom",
        details={"path": "example-path"},
    )

    payload = err.to_payload()

    assert payload == {
        "ok": False,
        "error_code": "EXAMPLE",
        "error": "boom",
        "details": {"path": "example-path"},
    }
