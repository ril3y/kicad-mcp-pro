"""Regression tests for ``kicad_mcp.tools.schematic._symbol_file``.

Schematic-side counterpart of PR #9's ``_footprint_file`` fix. Pre-PR
the symbol-resolution path (used by ``_render_schematic_symbol_block``
and 4 sibling sites) only consulted ``cfg.symbol_library_dir`` (the
global KiCad symbol directory), so user-imported libraries registered
in the project ``sym-lib-table`` (e.g. easyeda2kicad's symbol libraries)
couldn't be resolved by headless flows.

These tests build a synthetic project with a project-local
``sym-lib-table`` + ``.kicad_sym`` file and confirm:
1. Project-local libraries resolve before the global directory.
2. ``${KIPRJMOD}`` and ``${KICAD_PROJECT_DIR}`` URIs expand.
3. Both URI styles work: full-path-to-file and directory-style.
4. Falls through to the global directory when the local table doesn't
   list the library or the candidate file doesn't exist.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

_FAKE_KICAD_SYM = """\
(kicad_symbol_lib
    (version 20240926)
    (generator "test")
    (symbol "WIDGET"
        (pin_numbers (hide no))
    )
)
"""


def _patch_config(
    monkeypatch: pytest.MonkeyPatch,
    *,
    project_dir: Path | None,
    symbol_library_dir: Path | None,
) -> None:
    fake_cfg = SimpleNamespace(
        project_dir=project_dir,
        symbol_library_dir=symbol_library_dir,
    )
    monkeypatch.setattr("kicad_mcp.tools.schematic.get_config", lambda: fake_cfg)


def test_symbol_file_resolves_via_project_local_sym_lib_table_full_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Most ``sym-lib-table`` URIs point directly at a ``.kicad_sym`` file
    (not a directory like ``fp-lib-table``). Lock the full-path style."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    sym_path = project_dir / "easyeda2kicad.kicad_sym"
    sym_path.write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    (project_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        '  (lib (name "easyeda2kicad") (type "KiCad") '
        '(uri "${KIPRJMOD}/easyeda2kicad.kicad_sym") '
        '(options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    assert _symbol_file("easyeda2kicad") == sym_path


def test_symbol_file_resolves_via_directory_style_uri(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Some setups point at a directory containing ``<name>.kicad_sym`` —
    mirror the fp-lib-table convention as a fallback."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    lib_dir = project_dir / "vendor"
    lib_dir.mkdir()
    sym_path = lib_dir / "vendor.kicad_sym"
    sym_path.write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    (project_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        '  (lib (name "vendor") (type "KiCad") '
        '(uri "${KIPRJMOD}/vendor") '
        '(options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    assert _symbol_file("vendor") == sym_path


def test_symbol_file_expands_kicad_project_dir_variable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``${KICAD_PROJECT_DIR}`` is the older variable name; locked here
    just like the fp-lib-table tests do."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    sym_path = project_dir / "legacy.kicad_sym"
    sym_path.write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    (project_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        '  (lib (name "legacy") (type "KiCad") '
        '(uri "${KICAD_PROJECT_DIR}/legacy.kicad_sym") '
        '(options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    assert _symbol_file("legacy") == sym_path


def test_symbol_file_handles_absolute_uri(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Absolute path URIs (no template) honored verbatim."""
    from kicad_mcp.tools.schematic import _symbol_file

    abs_lib = tmp_path / "shared" / "myimport.kicad_sym"
    abs_lib.parent.mkdir()
    abs_lib.write_text(_FAKE_KICAD_SYM, encoding="utf-8")

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    (project_dir / "sym-lib-table").write_text(
        f"(sym_lib_table\n"
        f'  (lib (name "myimport") (type "KiCad") '
        f'(uri "{abs_lib.as_posix()}") '
        f'(options "") (descr ""))\n'
        f")\n",
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    assert _symbol_file("myimport") == abs_lib


def test_symbol_file_falls_through_to_global_when_local_misses(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A library not listed in sym-lib-table must fall through to the
    global directory — preserves legacy single-source behavior for
    KiCad's bundled symbol libraries."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    (project_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        '  (lib (name "OTHER") (type "KiCad") '
        '(uri "${KIPRJMOD}/other.kicad_sym") '
        '(options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    global_dir = tmp_path / "kicad_global"
    global_dir.mkdir()
    (global_dir / "Device.kicad_sym").write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=global_dir)

    assert _symbol_file("Device") == global_dir / "Device.kicad_sym"


def test_symbol_file_falls_through_when_local_candidate_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If the local table lists the library but the .kicad_sym file isn't
    on disk, fall through rather than return a non-existent path."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    # Note: no stale.kicad_sym file inside.
    (project_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        '  (lib (name "stale") (type "KiCad") '
        '(uri "${KIPRJMOD}/stale.kicad_sym") '
        '(options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    global_dir = tmp_path / "kicad_global"
    global_dir.mkdir()
    (global_dir / "stale.kicad_sym").write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=global_dir)

    assert _symbol_file("stale") == global_dir / "stale.kicad_sym"


def test_symbol_file_no_project_dir_uses_global(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without an active project, fall back to the global directory."""
    from kicad_mcp.tools.schematic import _symbol_file

    global_dir = tmp_path / "kicad_global"
    global_dir.mkdir()
    (global_dir / "Device.kicad_sym").write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    _patch_config(monkeypatch, project_dir=None, symbol_library_dir=global_dir)

    assert _symbol_file("Device") == global_dir / "Device.kicad_sym"


def test_symbol_file_matches_library_name_case_insensitively(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mirror PR #9: regex uses ``re.IGNORECASE`` so callers can use
    different capitalization than the table entry."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    sym_path = project_dir / "EasyEda.kicad_sym"
    sym_path.write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    (project_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        '  (lib (name "EasyEda") (type "KiCad") '
        '(uri "${KIPRJMOD}/EasyEda.kicad_sym") '
        '(options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    assert _symbol_file("easyeda") == sym_path


def test_symbol_file_picks_correct_entry_among_multiple_libraries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Real projects list many libraries; regex must anchor on the
    requested name and not bleed across siblings."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    target = project_dir / "target_lib.kicad_sym"
    decoy = project_dir / "decoy_lib.kicad_sym"
    target.write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    decoy.write_text("(WRONG)", encoding="utf-8")
    (project_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        '  (lib (name "decoy_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/decoy_lib.kicad_sym") (options "") (descr ""))\n'
        '  (lib (name "target_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/target_lib.kicad_sym") (options "") (descr ""))\n'
        '  (lib (name "another_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/another_lib.kicad_sym") (options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    assert _symbol_file("target_lib") == target
