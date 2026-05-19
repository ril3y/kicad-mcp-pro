"""Regression tests for ``kicad_mcp.tools.schematic._symbol_file`` and the
shared ``_load_symbol_blocks`` resolver that backs ``sch_get_pin_positions``,
``sch_add_symbol``, ``get_symbol_available_units``, and ``load_lib_symbol``.

Pre-PR ``_symbol_file`` only expanded ``${KIPRJMOD}`` / ``${KICAD_PROJECT_DIR}``
in ``sym-lib-table`` URIs, so user-imported libraries that referenced
``${EASYEDA2KICAD}`` (or any other ``kicad_common.json``-defined env var)
failed to resolve in headless flows. The schematic-side counterpart of PR #20's
footprint fix in ``tools/pcb.py``: same precedence rules
(``${KIPRJMOD}`` -> OS env -> ``kicad_common.json::environment.vars``),
same fall-through-to-global semantics.

A second class of failure: the project's schematic can reference a library
name (``easyeda:G2R-2-DC12V``) that no longer exists in the
``sym-lib-table`` because the library was later renamed (``easyeda2kicad``).
KiCad's GUI papers over this with the schematic's embedded
``(lib_symbols ...)`` cache. ``_load_symbol_blocks`` mirrors that by falling
back to the embedded cache when the table lookup misses.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_FAKE_KICAD_SYM = """\
(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor)
  (symbol "G2R-2-DC12V"
    (pin_names (offset 0.508) hide)
    (in_bom yes)
    (on_board yes)
    (symbol "G2R-2-DC12V_0_1"
      (rectangle (start -5.08 -5.08) (end 5.08 5.08)
        (stroke (width 0.254) (type default))
        (fill (type background))
      )
    )
    (symbol "G2R-2-DC12V_1_1"
      (pin passive line (at -7.62 2.54 0) (length 2.54)
        (name "COIL+") (number "1"))
      (pin passive line (at -7.62 -2.54 0) (length 2.54)
        (name "COIL-") (number "2"))
      (pin passive line (at 7.62 2.54 180) (length 2.54)
        (name "NO") (number "3"))
      (pin passive line (at 7.62 0.0 180) (length 2.54)
        (name "COM") (number "4"))
      (pin passive line (at 7.62 -2.54 180) (length 2.54)
        (name "NC") (number "5"))
    )
  )
)
"""


def _build_project_with_sym_lib(
    tmp_path: Path,
    *,
    library_name: str,
    uri_template: str,
    sym_filename: str = "lib.kicad_sym",
    sym_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Create a fake project with a project-local sym-lib-table + .kicad_sym."""
    project_dir = tmp_path / "proj"
    project_dir.mkdir(exist_ok=True)
    target_dir = sym_dir if sym_dir is not None else project_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    sym_file = target_dir / sym_filename
    sym_file.write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    sym_table = project_dir / "sym-lib-table"
    # Use ``.replace`` so ``${KIPRJMOD}`` placeholders don't collide with
    # str.format's ``{}`` syntax. ``<LIB>`` / ``<FILE>`` are our own tokens.
    uri = uri_template.replace("<LIB>", library_name).replace("<FILE>", sym_filename)
    sym_table.write_text(
        f"(sym_lib_table\n  (version 7)\n"
        f'  (lib (name "{library_name}") (type "KiCad") '
        f'(uri "{uri}") (options "") (descr ""))\n)\n',
        encoding="utf-8",
    )
    return project_dir, sym_file


def _patch_config(
    monkeypatch: pytest.MonkeyPatch,
    *,
    project_dir: Path | None,
    symbol_library_dir: Path | None = None,
    sch_file: Path | None = None,
) -> None:
    from types import SimpleNamespace

    fake_cfg = SimpleNamespace(
        project_dir=project_dir,
        symbol_library_dir=symbol_library_dir,
        sch_file=sch_file,
    )
    monkeypatch.setattr("kicad_mcp.tools.schematic.get_config", lambda: fake_cfg)


def test_symbol_file_resolves_via_project_local_sym_lib_table_with_kiprjmod(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``${KIPRJMOD}`` URIs in project-local sym-lib-table must resolve.

    Mutation kill: drop the ``${KIPRJMOD}`` substitution and this fails.
    """
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir, sym_file = _build_project_with_sym_lib(
        tmp_path,
        library_name="easyeda2kicad",
        uri_template="${KIPRJMOD}/<FILE>",
        sym_filename="easyeda2kicad.kicad_sym",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    resolved = _symbol_file("easyeda2kicad")
    assert resolved == sym_file
    assert resolved.exists()


def test_symbol_file_falls_through_to_global_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A library not in sym-lib-table falls through to ``symbol_library_dir``."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    global_dir = tmp_path / "global_syms"
    global_dir.mkdir()
    (global_dir / "Device.kicad_sym").write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=global_dir)

    resolved = _symbol_file("Device")
    assert resolved == global_dir / "Device.kicad_sym"


def test_symbol_file_no_project_dir_falls_through_to_global(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No project dir set: resolution lands directly on the global directory."""
    from kicad_mcp.tools.schematic import _symbol_file

    global_dir = tmp_path / "global_syms"
    global_dir.mkdir()
    (global_dir / "Device.kicad_sym").write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    _patch_config(monkeypatch, project_dir=None, symbol_library_dir=global_dir)

    resolved = _symbol_file("Device")
    assert resolved == global_dir / "Device.kicad_sym"


def test_symbol_file_raises_when_global_dir_unset(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Library not in table + no global dir = clean ``FileNotFoundError``.

    Pre-PR ``sch_get_pin_positions`` would return ``"Could not calculate
    pin positions for X:Y"`` — opaque to the caller. The lower-level
    resolver should surface a structured error so the tool can offer a
    better message later.
    """
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    # No table file -> falls through. No global dir configured -> raises.
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    with pytest.raises(FileNotFoundError):
        _symbol_file("does_not_exist")


def test_symbol_file_expands_user_env_var_from_kicad_common(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """User-defined env vars (``kicad_common.json::environment.vars``)
    must expand inside ``sym-lib-table`` URIs. This is the actual
    golfcart-junction-passive repro: the project sym-lib-table contains
    ``(uri "${EASYEDA2KICAD}/easyeda2kicad.kicad_sym")`` and ``sch_get_pin_positions``
    raised ``Could not calculate pin positions for easyeda2kicad:G2R-2-DC12V``
    pre-PR.
    """
    from kicad_mcp.tools.schematic import _symbol_file

    # 1. The .kicad_sym lives under a directory referenced by a KiCad-user env var.
    libroot = tmp_path / "external_libs"
    libroot.mkdir()
    (libroot / "easyeda2kicad.kicad_sym").write_text(_FAKE_KICAD_SYM, encoding="utf-8")

    # 2. Project sym-lib-table uses ${EASYEDA2KICAD}.
    project_dir, _ = _build_project_with_sym_lib(
        tmp_path,
        library_name="easyeda2kicad",
        uri_template="${EASYEDA2KICAD}/easyeda2kicad.kicad_sym",
        sym_filename="ignored.kicad_sym",  # not actually probed since URI is absolute
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    # 3. The user env var is in KiCad's config, NOT the OS env. The expander
    #    consults find_kicad_user_env_vars — patch it directly.
    monkeypatch.setattr(
        "kicad_mcp.discovery.find_kicad_user_env_vars",
        lambda: {"EASYEDA2KICAD": str(libroot)},
    )

    resolved = _symbol_file("easyeda2kicad")
    assert resolved == libroot / "easyeda2kicad.kicad_sym"
    assert resolved.exists()


def test_symbol_file_os_env_overrides_kicad_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OS env wins over ``kicad_common.json`` — matches KiCad GUI precedence
    so a CI runner exporting ``EASYEDA2KICAD`` overrides whatever the
    developer's Configure Paths happens to have."""
    from kicad_mcp.tools.schematic import _symbol_file

    libroot_os = tmp_path / "from_os_env"
    libroot_os.mkdir()
    (libroot_os / "easyeda2kicad.kicad_sym").write_text(_FAKE_KICAD_SYM, encoding="utf-8")

    project_dir, _ = _build_project_with_sym_lib(
        tmp_path,
        library_name="easyeda2kicad",
        uri_template="${EASYEDA2KICAD}/easyeda2kicad.kicad_sym",
        sym_filename="ignored.kicad_sym",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    # OS env wins; kicad_common.json points elsewhere with no file present.
    monkeypatch.setenv("EASYEDA2KICAD", str(libroot_os))
    monkeypatch.setattr(
        "kicad_mcp.discovery.find_kicad_user_env_vars",
        lambda: {"EASYEDA2KICAD": str(tmp_path / "kicad_config_should_lose")},
    )

    resolved = _symbol_file("easyeda2kicad")
    assert resolved == libroot_os / "easyeda2kicad.kicad_sym"


def test_get_pin_positions_resolves_easyeda_via_sym_lib_table(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End-to-end: ``get_pin_positions`` must return pin coordinates for
    a symbol whose library is registered in the project sym-lib-table
    only. Locks the contract that ``sch_get_pin_positions`` no longer
    returns the opaque ``Could not calculate pin positions`` error for
    project-local libraries."""
    from kicad_mcp.tools.schematic import get_pin_positions

    project_dir, _ = _build_project_with_sym_lib(
        tmp_path,
        library_name="easyeda2kicad",
        uri_template="${KIPRJMOD}/<FILE>",
        sym_filename="easyeda2kicad.kicad_sym",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    pins = get_pin_positions("easyeda2kicad", "G2R-2-DC12V", 100.0, 50.0, rotation=0, unit=1)
    # G2R-2-DC12V has five pins (1-5). Real coordinates depend on the
    # symbol's pin offsets but the contract is "non-empty result for a
    # library reachable via the project sym-lib-table".
    assert set(pins.keys()) == {"1", "2", "3", "4", "5"}
    # Pin 1 sits at symbol-local (-7.62, 2.54). At placement (100, 50)
    # with rotation 0 the absolute coordinate is (100 + (-7.62), 50 - 2.54).
    assert pins["1"] == pytest.approx((92.38, 52.54), abs=1e-3)


def test_get_pin_positions_falls_back_to_embedded_lib_symbols_on_library_rename(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A schematic can reference ``easyeda:G2R-2-DC12V`` even after the
    library was renamed to ``easyeda2kicad`` in the sym-lib-table. KiCad
    keeps a cached copy in the schematic's ``(lib_symbols ...)`` block;
    ``_load_symbol_blocks`` must fall back to it so headless flows
    behave like the GUI.

    Mutation kill: remove the embedded-fallback branch and this fails
    with an empty dict (the original golfcart-junction-passive repro).
    """
    from kicad_mcp.tools.schematic import get_pin_positions

    # Project has a sym-lib-table that does NOT list ``easyeda`` (the
    # name the schematic uses); only ``easyeda2kicad``.
    project_dir, _ = _build_project_with_sym_lib(
        tmp_path,
        library_name="easyeda2kicad",
        uri_template="${KIPRJMOD}/<FILE>",
        sym_filename="easyeda2kicad.kicad_sym",
    )

    # Build a minimal schematic with an embedded lib_symbols block under
    # the renamed library prefix ``easyeda:``.
    sch_file = project_dir / "junction.kicad_sch"
    sch_file.write_text(
        "(kicad_sch (version 20230121) (generator eeschema)\n"
        "  (lib_symbols\n"
        '    (symbol "easyeda:G2R-2-DC12V"\n'
        "      (pin_names (offset 0.508) hide)\n"
        "      (in_bom yes) (on_board yes)\n"
        '      (symbol "G2R-2-DC12V_0_1"\n'
        "        (rectangle (start -5.08 -5.08) (end 5.08 5.08)\n"
        "          (stroke (width 0.254) (type default)) (fill (type background))))\n"
        '      (symbol "G2R-2-DC12V_1_1"\n'
        "        (pin passive line (at -7.62 2.54 0) (length 2.54)\n"
        '          (name "COIL+") (number "1"))\n'
        "        (pin passive line (at -7.62 -2.54 0) (length 2.54)\n"
        '          (name "COIL-") (number "2")))\n'
        "    )\n"
        "  )\n"
        ")\n",
        encoding="utf-8",
    )
    _patch_config(
        monkeypatch,
        project_dir=project_dir,
        symbol_library_dir=None,
        sch_file=sch_file,
    )

    pins = get_pin_positions("easyeda", "G2R-2-DC12V", 100.0, 50.0, rotation=0, unit=1)
    assert set(pins.keys()) == {"1", "2"}
    assert pins["1"] == pytest.approx((92.38, 52.54), abs=1e-3)


def test_load_lib_symbol_returns_none_for_unknown_library(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``load_lib_symbol`` must return ``None`` (not raise) when the
    library can't be resolved in the project or global location, since
    ``sch_add_symbol`` relies on the ``None`` sentinel to emit
    ``Symbol '...' was not found.``"""
    from kicad_mcp.tools.schematic import load_lib_symbol

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    global_dir = tmp_path / "global_syms"
    global_dir.mkdir()  # exists but doesn't contain the requested lib
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=global_dir)

    assert load_lib_symbol("Nonexistent", "Whatever") is None


def test_load_lib_symbol_uses_embedded_cache_when_sym_lib_table_misses(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``sch_add_symbol`` reuses ``load_lib_symbol`` to embed the library
    definition into the schematic. When the table lookup misses but the
    embedded lib_symbols cache has the symbol, the helper returns the
    cached block with the header rewritten back to ``library:symbol_name``
    so it can be safely re-inserted without breaking placement code.
    """
    from kicad_mcp.tools.schematic import load_lib_symbol

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    # No sym-lib-table; only the schematic's embedded cache has the symbol.
    sch_file = project_dir / "junction.kicad_sch"
    sch_file.write_text(
        "(kicad_sch (version 20230121) (generator eeschema)\n"
        "  (lib_symbols\n"
        '    (symbol "easyeda:G2R-2-DC12V"\n'
        "      (in_bom yes) (on_board yes)\n"
        '      (symbol "G2R-2-DC12V_1_1"\n'
        "        (pin passive line (at -7.62 2.54 0) (length 2.54)\n"
        '          (name "COIL+") (number "1")))\n'
        "    )\n"
        "  )\n"
        ")\n",
        encoding="utf-8",
    )
    _patch_config(
        monkeypatch,
        project_dir=project_dir,
        symbol_library_dir=None,
        sch_file=sch_file,
    )

    rendered = load_lib_symbol("easyeda", "G2R-2-DC12V")
    assert rendered is not None
    # The header is rewritten back to the prefixed form so it survives
    # re-insertion into a fresh lib_symbols block.
    assert '(symbol "easyeda:G2R-2-DC12V"' in rendered


def test_symbol_file_picks_correct_entry_among_multiple_libraries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A real project's sym-lib-table can list many libraries — the
    regex must anchor on the requested name and not bleed across
    siblings (the contract that test_footprint_file pins for the PCB
    side)."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    target = project_dir / "target.kicad_sym"
    decoy = project_dir / "decoy.kicad_sym"
    target.write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    decoy.write_text(_FAKE_KICAD_SYM, encoding="utf-8")
    (project_dir / "sym-lib-table").write_text(
        "(sym_lib_table\n"
        "  (version 7)\n"
        '  (lib (name "decoy_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/decoy.kicad_sym") (options "") (descr ""))\n'
        '  (lib (name "target_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/target.kicad_sym") (options "") (descr ""))\n'
        '  (lib (name "another_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/another.kicad_sym") (options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    resolved = _symbol_file("target_lib")
    assert resolved == target


def test_symbol_file_case_insensitive_library_name_match(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """KiCad treats library names case-insensitively in sym-lib-table —
    a project-local entry must match regardless of how the caller
    capitalizes the library prefix."""
    from kicad_mcp.tools.schematic import _symbol_file

    project_dir, sym_file = _build_project_with_sym_lib(
        tmp_path,
        library_name="EasyEda2KiCad",  # mixed case in the table
        uri_template="${KIPRJMOD}/<FILE>",
        sym_filename="easyeda2kicad.kicad_sym",
    )
    _patch_config(monkeypatch, project_dir=project_dir, symbol_library_dir=None)

    # Caller passes lowercase — must still resolve.
    resolved = _symbol_file("easyeda2kicad")
    assert resolved == sym_file
