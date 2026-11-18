"""Symbol libraries are readable in both the single-file and KiCad 11 folder layouts."""

from __future__ import annotations

from pathlib import Path

from kicad_mcp.discovery import discover_library_paths
from kicad_mcp.utils import symbol_library


def _symbol_file(*blocks: str) -> str:
    body = "\n".join(f"\t{block}" for block in blocks)
    return f'(kicad_symbol_lib\n\t(version 20251024)\n\t(generator "test")\n{body}\n)\n'


PARENT = '(symbol "BASE"\n\t\t(property "Description" "Parent part")\n\t)'
CHILD = '(symbol "DERIVED"\n\t\t(extends "BASE")\n\t)'


def _make_libraries(root: Path) -> None:
    (root / "Flat.kicad_sym").write_text(_symbol_file(PARENT, CHILD), encoding="utf-8")
    folder = root / "Split.kicad_symdir"
    folder.mkdir()
    (folder / "BASE.kicad_sym").write_text(_symbol_file(PARENT), encoding="utf-8")
    (folder / "DERIVED.kicad_sym").write_text(_symbol_file(CHILD), encoding="utf-8")


def test_library_names_cover_both_layouts(tmp_path: Path) -> None:
    _make_libraries(tmp_path)
    assert symbol_library.library_names(tmp_path) == ["Flat", "Split"]


def test_library_path_prefers_what_exists(tmp_path: Path) -> None:
    _make_libraries(tmp_path)
    assert symbol_library.library_path(tmp_path, "Flat") == tmp_path / "Flat.kicad_sym"
    assert symbol_library.library_path(tmp_path, "Split") == tmp_path / "Split.kicad_symdir"
    assert symbol_library.library_path(tmp_path, "Missing") is None


def test_folder_library_reads_as_one_text_with_parent_and_child(tmp_path: Path) -> None:
    _make_libraries(tmp_path)
    text = symbol_library.read_library_text(tmp_path / "Split.kicad_symdir")
    assert text.startswith("(kicad_symbol_lib")
    assert text.count("(kicad_symbol_lib") == 1
    assert '(symbol "BASE"' in text
    assert '(symbol "DERIVED"' in text
    assert text.count("(") == text.count(")")


def test_symbol_files_lists_one_file_per_symbol(tmp_path: Path) -> None:
    _make_libraries(tmp_path)
    names = [path.stem for path in symbol_library.symbol_files(tmp_path / "Split.kicad_symdir")]
    assert names == ["BASE", "DERIVED"]
    assert symbol_library.symbol_files(tmp_path / "Flat.kicad_sym") == [tmp_path / "Flat.kicad_sym"]


def test_discover_library_paths_in_macos_app_bundle(tmp_path: Path) -> None:
    contents = tmp_path / "KiCad.app" / "Contents"
    cli = contents / "MacOS" / "kicad-cli"
    cli.parent.mkdir(parents=True)
    cli.write_text("", encoding="utf-8")
    (contents / "SharedSupport" / "symbols").mkdir(parents=True)
    (contents / "SharedSupport" / "footprints").mkdir(parents=True)

    paths = discover_library_paths(cli)

    assert paths["symbols"] == contents / "SharedSupport" / "symbols"
    assert paths["footprints"] == contents / "SharedSupport" / "footprints"
