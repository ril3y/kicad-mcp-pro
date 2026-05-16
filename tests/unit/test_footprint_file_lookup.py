"""Regression tests for ``kicad_mcp.tools.pcb._footprint_file`` and the
``Library:Footprint`` header rewrite in ``_render_board_footprint_block``.

Pre-PR ``_footprint_file`` only consulted ``cfg.footprint_library_dir`` (the
global KiCad library), so user-imported libraries registered in the project
``fp-lib-table`` (e.g. easyeda2kicad's CONN-TH_*.pretty paths) couldn't be
resolved by headless flows like ``pcb_sync_from_schematic``. The junction-
passive board hit this directly: its TE 26-pin Amphenol footprint
(``easyeda2kicad:CONN-TH_9-6437287-8``) raised ``FileNotFoundError`` even
though pcbnew's GUI resolved it fine.

These tests build a synthetic project with a project-local
``fp-lib-table`` + ``.pretty`` directory and confirm:
1. Project-local libraries resolve before the global directory.
2. ``${KIPRJMOD}`` and ``${KICAD_PROJECT_DIR}`` URIs expand.
3. Falls through to the global directory when the local table doesn't list
   the library or the candidate file doesn't exist.
4. ``_render_board_footprint_block`` rewrites the footprint header to the
   ``Library:Footprint`` form expected inside ``.kicad_pcb`` files.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_FAKE_KICAD_MOD = """\
(footprint "CONN-TH_9-6437287-8"
    (layer "F.Cu")
    (uuid "abc")
    (at 0 0 0)
    (property "Reference" "REF**" (at 0 -1.5 0) (layer "F.SilkS"))
    (property "Value" "Conn" (at 0 1.5 0) (layer "F.Fab"))
)
"""


def _build_project_with_local_lib(
    tmp_path: Path,
    *,
    library_name: str,
    footprint_name: str,
    uri_template: str,
) -> tuple[Path, Path]:
    """Create a fake project dir with a project-local fp-lib-table + .pretty."""
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    pretty_dir = project_dir / f"{library_name}.pretty"
    pretty_dir.mkdir()
    (pretty_dir / f"{footprint_name}.kicad_mod").write_text(_FAKE_KICAD_MOD, encoding="utf-8")
    fp_table = project_dir / "fp-lib-table"
    # Use ``.replace`` rather than ``.format`` so ``${KIPRJMOD}`` etc. don't
    # collide with str.format's ``{...}`` syntax. The template uses ``<LIB>``
    # as the substitution token.
    uri = uri_template.replace("<LIB>", library_name)
    fp_table.write_text(
        f'(fp_lib_table\n  (lib (name "{library_name}") (type "KiCad") '
        f'(uri "{uri}") (options "") (descr ""))\n)\n',
        encoding="utf-8",
    )
    return project_dir, pretty_dir


def _patch_config(
    monkeypatch: pytest.MonkeyPatch,
    *,
    project_dir: Path | None,
    footprint_library_dir: Path | None,
) -> None:
    from types import SimpleNamespace

    fake_cfg = SimpleNamespace(
        project_dir=project_dir,
        footprint_library_dir=footprint_library_dir,
    )
    monkeypatch.setattr("kicad_mcp.tools.pcb.get_config", lambda: fake_cfg)


def test_footprint_file_resolves_via_project_local_fp_lib_table(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The local fp-lib-table must win when it lists the library.

    Mutation kill: the pre-PR helper only consults the global directory,
    so a project-local ``easyeda2kicad`` library would never be found.
    """
    from kicad_mcp.tools.pcb import _footprint_file

    project_dir, pretty_dir = _build_project_with_local_lib(
        tmp_path,
        library_name="easyeda2kicad",
        footprint_name="CONN-TH_9-6437287-8",
        uri_template="${KIPRJMOD}/<LIB>.pretty",
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=None)

    resolved = _footprint_file("easyeda2kicad", "CONN-TH_9-6437287-8")
    assert resolved == pretty_dir / "CONN-TH_9-6437287-8.kicad_mod"
    assert resolved.exists()


def test_footprint_file_expands_kicad_project_dir_variable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``${KICAD_PROJECT_DIR}`` is the older variable name and must expand too."""
    from kicad_mcp.tools.pcb import _footprint_file

    project_dir, pretty_dir = _build_project_with_local_lib(
        tmp_path,
        library_name="vendor_imports",
        footprint_name="CUSTOM-1",
        uri_template="${KICAD_PROJECT_DIR}/<LIB>.pretty",
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=None)

    resolved = _footprint_file("vendor_imports", "CUSTOM-1")
    assert resolved == pretty_dir / "CUSTOM-1.kicad_mod"


def test_footprint_file_handles_absolute_uri(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A non-templated absolute path in the URI must be honored verbatim."""
    from kicad_mcp.tools.pcb import _footprint_file

    abs_pretty = tmp_path / "shared" / "myimport.pretty"
    abs_pretty.mkdir(parents=True)
    (abs_pretty / "WIDGET.kicad_mod").write_text(_FAKE_KICAD_MOD, encoding="utf-8")

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    fp_table = project_dir / "fp-lib-table"
    fp_table.write_text(
        f'(fp_lib_table\n  (lib (name "myimport") (type "KiCad") '
        f'(uri "{abs_pretty.as_posix()}") (options "") (descr ""))\n)\n',
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=None)

    resolved = _footprint_file("myimport", "WIDGET")
    assert resolved == abs_pretty / "WIDGET.kicad_mod"


def test_footprint_file_falls_through_to_global_when_local_misses(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A library not listed in fp-lib-table must fall through to the global dir
    so legacy single-source behavior is preserved for KiCad's bundled libs."""
    from kicad_mcp.tools.pcb import _footprint_file

    # Local table lists "OTHER", not "Device".
    project_dir, _ = _build_project_with_local_lib(
        tmp_path,
        library_name="OTHER",
        footprint_name="X",
        uri_template="${KIPRJMOD}/<LIB>.pretty",
    )
    global_dir = tmp_path / "kicad_global"
    (global_dir / "Device.pretty").mkdir(parents=True)
    (global_dir / "Device.pretty" / "R_0805.kicad_mod").write_text(
        _FAKE_KICAD_MOD, encoding="utf-8"
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=global_dir)

    resolved = _footprint_file("Device", "R_0805")
    assert resolved == global_dir / "Device.pretty" / "R_0805.kicad_mod"


def test_footprint_file_falls_through_when_local_candidate_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If the local table lists the library but the .kicad_mod file isn't
    actually on disk, fall through to the global directory rather than
    return a non-existent path. Defends against stale fp-lib-table entries.
    """
    from kicad_mcp.tools.pcb import _footprint_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    pretty_dir = project_dir / "stale.pretty"
    pretty_dir.mkdir()
    # Note: no GHOST.kicad_mod file inside.
    fp_table = project_dir / "fp-lib-table"
    fp_table.write_text(
        '(fp_lib_table\n  (lib (name "stale") (type "KiCad") '
        '(uri "${KIPRJMOD}/stale.pretty") (options "") (descr ""))\n)\n',
        encoding="utf-8",
    )
    global_dir = tmp_path / "kicad_global"
    (global_dir / "stale.pretty").mkdir(parents=True)
    (global_dir / "stale.pretty" / "GHOST.kicad_mod").write_text(_FAKE_KICAD_MOD, encoding="utf-8")
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=global_dir)

    resolved = _footprint_file("stale", "GHOST")
    assert resolved == global_dir / "stale.pretty" / "GHOST.kicad_mod"


def test_footprint_file_no_project_dir_uses_global(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When no project is set, use the global directory exactly as before."""
    from kicad_mcp.tools.pcb import _footprint_file

    global_dir = tmp_path / "kicad_global"
    (global_dir / "Device.pretty").mkdir(parents=True)
    (global_dir / "Device.pretty" / "R_0805.kicad_mod").write_text(
        _FAKE_KICAD_MOD, encoding="utf-8"
    )
    _patch_config(monkeypatch, project_dir=None, footprint_library_dir=global_dir)

    resolved = _footprint_file("Device", "R_0805")
    assert resolved == global_dir / "Device.pretty" / "R_0805.kicad_mod"


def test_footprint_file_matches_library_name_case_insensitively(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The fp-lib-table regex uses ``re.IGNORECASE`` so a project-local
    library entry can be matched regardless of how the caller capitalizes
    the library prefix. Locks that contract — a refactor that drops the
    flag would silently break case-mismatched lookups (which KiCad itself
    accepts)."""
    from kicad_mcp.tools.pcb import _footprint_file

    project_dir, pretty_dir = _build_project_with_local_lib(
        tmp_path,
        library_name="EasyEda2KiCad",  # mixed case in the table
        footprint_name="WIDGET",
        uri_template="${KIPRJMOD}/<LIB>.pretty",
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=None)

    # Caller passes lowercase — must still resolve.
    resolved = _footprint_file("easyeda2kicad", "WIDGET")
    assert resolved == pretty_dir / "WIDGET.kicad_mod"


def test_footprint_file_picks_correct_entry_among_multiple_libraries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A real project's fp-lib-table lists many libraries. The regex must
    anchor on the requested name and not bleed across siblings."""
    from kicad_mcp.tools.pcb import _footprint_file

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    target_pretty = project_dir / "target_lib.pretty"
    decoy_pretty = project_dir / "decoy_lib.pretty"
    target_pretty.mkdir()
    decoy_pretty.mkdir()
    (target_pretty / "WANTED.kicad_mod").write_text(_FAKE_KICAD_MOD, encoding="utf-8")
    (decoy_pretty / "WANTED.kicad_mod").write_text(
        '(footprint "WRONG-FOOTPRINT")', encoding="utf-8"
    )
    (project_dir / "fp-lib-table").write_text(
        "(fp_lib_table\n"
        '  (lib (name "decoy_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/decoy_lib.pretty") (options "") (descr ""))\n'
        '  (lib (name "target_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/target_lib.pretty") (options "") (descr ""))\n'
        '  (lib (name "another_lib") (type "KiCad") '
        '(uri "${KIPRJMOD}/another_lib.pretty") (options "") (descr ""))\n'
        ")\n",
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=None)

    resolved = _footprint_file("target_lib", "WANTED")
    assert resolved == target_pretty / "WANTED.kicad_mod"


def test_footprint_file_expands_user_env_var_from_kicad_common(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """User-defined env vars (KiCad ``Preferences > Configure Paths``) live
    in ``kicad_common.json::environment.vars`` — NOT in the OS environment.
    The MCP server process must read them out of the config file before
    expanding ``${EASYEDA2KICAD}`` and friends in ``fp-lib-table`` URIs,
    otherwise headless flows fail with ``Footprint '...' was not found``
    even when the file exists on disk. This was the junction-passive
    repro: ``easyeda2kicad:CONN-TH_9-6437287-8`` raised FileNotFoundError
    despite the file being present at ``${EASYEDA2KICAD}/...``.
    """
    from kicad_mcp.tools.pcb import _footprint_file

    # 1. The footprint lives under a directory referenced by a user env var.
    libroot = tmp_path / "external_libs"
    pretty_dir = libroot / "easyeda2kicad.pretty"
    pretty_dir.mkdir(parents=True)
    (pretty_dir / "CONN-TH_9-6437287-8.kicad_mod").write_text(
        _FAKE_KICAD_MOD, encoding="utf-8"
    )

    # 2. Build a project whose fp-lib-table uses ${EASYEDA2KICAD}.
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    (project_dir / "fp-lib-table").write_text(
        '(fp_lib_table\n  (lib (name "easyeda2kicad") (type "KiCad") '
        '(uri "${EASYEDA2KICAD}/easyeda2kicad.pretty") (options "") (descr ""))\n)\n',
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=None)

    # 3. The user env var is in KiCad's config, NOT the OS env. Surface it
    #    through find_kicad_user_env_vars (the discovery helper the
    #    resolver calls). This both pins the contract and exercises the
    #    only entry point that knows about KiCad's user vars.
    monkeypatch.setattr(
        "kicad_mcp.tools.pcb.find_kicad_user_env_vars",
        lambda: {"EASYEDA2KICAD": str(libroot)},
    )

    resolved = _footprint_file("easyeda2kicad", "CONN-TH_9-6437287-8")
    assert resolved == pretty_dir / "CONN-TH_9-6437287-8.kicad_mod"


def test_footprint_file_user_env_var_takes_precedence_over_os_env(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """KiCad's ``Configure Paths`` is the source of truth — when both the
    OS environment and ``kicad_common.json`` define the same var with
    different values, the KiCad config wins. This matches what the GUI
    does at runtime (KiCad doesn't read PROCESS env for these names)."""
    from kicad_mcp.tools.pcb import _footprint_file

    libroot_kicad = tmp_path / "from_kicad_config"
    libroot_kicad.mkdir()
    (libroot_kicad / "easyeda2kicad.pretty").mkdir()
    (libroot_kicad / "easyeda2kicad.pretty" / "PART.kicad_mod").write_text(
        _FAKE_KICAD_MOD, encoding="utf-8"
    )

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    (project_dir / "fp-lib-table").write_text(
        '(fp_lib_table\n  (lib (name "easyeda2kicad") (type "KiCad") '
        '(uri "${EASYEDA2KICAD}/easyeda2kicad.pretty") (options "") (descr ""))\n)\n',
        encoding="utf-8",
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=None)

    # OS env points at a wrong/empty place; KiCad config wins via the loader.
    monkeypatch.setenv("EASYEDA2KICAD", str(tmp_path / "from_os_env_should_lose"))
    monkeypatch.setattr(
        "kicad_mcp.tools.pcb.find_kicad_user_env_vars",
        lambda: {"EASYEDA2KICAD": str(libroot_kicad)},
    )

    resolved = _footprint_file("easyeda2kicad", "PART")
    assert resolved == libroot_kicad / "easyeda2kicad.pretty" / "PART.kicad_mod"


def test_find_kicad_user_env_vars_reads_environment_vars_from_kicad_common(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The discovery helper reads ``environment.vars`` from
    ``kicad_common.json``. Pinned here so the contract doesn't drift —
    a refactor that walked the wrong JSON path would silently produce
    an empty dict and break every downstream footprint lookup."""
    import json
    from kicad_mcp.discovery import find_kicad_user_env_vars

    fake_config_dir = tmp_path / "kicad_config" / "10.0"
    fake_config_dir.mkdir(parents=True)
    (fake_config_dir / "kicad_common.json").write_text(
        json.dumps(
            {
                "environment": {
                    "vars": {
                        "EASYEDA2KICAD": "X:/external/easyeda",
                        "MY_LIBS": "X:/external/mylibs",
                    }
                },
                # Unrelated keys we must not touch
                "appearance": {"theme": "dark"},
                "input": {"keymap": "default"},
            }
        ),
        encoding="utf-8",
    )

    # Patch _kicad_config_dirs to return our fake dir.
    monkeypatch.setattr(
        "kicad_mcp.discovery._kicad_config_dirs",
        lambda: [fake_config_dir],
    )

    env = find_kicad_user_env_vars()
    assert env == {
        "EASYEDA2KICAD": "X:/external/easyeda",
        "MY_LIBS": "X:/external/mylibs",
    }


def test_find_kicad_user_env_vars_returns_empty_when_no_config_present(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Graceful degrade: no kicad_common.json at any candidate dir means
    we return ``{}`` and fall through to the next resolution strategy.
    Used to fail at startup when kicad_common.json was absent or
    malformed."""
    from kicad_mcp.discovery import find_kicad_user_env_vars

    empty_dir = tmp_path / "no_kicad_config"
    empty_dir.mkdir()
    monkeypatch.setattr(
        "kicad_mcp.discovery._kicad_config_dirs",
        lambda: [empty_dir],
    )

    assert find_kicad_user_env_vars() == {}


def test_render_board_footprint_block_rewrites_header_to_library_form(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A stand-alone .kicad_mod has only the footprint name in its header
    (e.g. ``(footprint "CONN-TH_9-6437287-8" ...)``). When embedded in a
    board, KiCad expects ``(footprint "easyeda2kicad:CONN-TH_9-6437287-8" ...)``.
    The rewrite must happen exactly once on the first occurrence.
    """
    from kicad_mcp.tools.pcb import _render_board_footprint_block

    project_dir, _ = _build_project_with_local_lib(
        tmp_path,
        library_name="easyeda2kicad",
        footprint_name="CONN-TH_9-6437287-8",
        uri_template="${KIPRJMOD}/<LIB>.pretty",
    )
    _patch_config(monkeypatch, project_dir=project_dir, footprint_library_dir=None)

    block = _render_board_footprint_block(
        "easyeda2kicad:CONN-TH_9-6437287-8",
        reference="J_M1",
        value="Amphenol 26-pin",
        x_mm=20.0,
        y_mm=30.0,
        rotation=0,
        pad_nets={},
    )

    # The rewritten header must use the prefixed form.
    assert '(footprint "easyeda2kicad:CONN-TH_9-6437287-8"' in block
    # The bare form must NOT appear at the start of any line in the rewritten
    # block (regression guard: the rewrite is count=1 but must catch the
    # header, not just any random match).
    assert '(footprint "CONN-TH_9-6437287-8"' not in block
