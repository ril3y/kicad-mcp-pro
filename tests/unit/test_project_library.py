"""Project-local libraries and the pad-table footprint generator."""

from __future__ import annotations

from pathlib import Path

import pytest

from kicad_mcp.utils import project_library
from kicad_mcp.utils.footprint_gen import generate_footprint_from_pads
from kicad_mcp.utils.symbol_gen import PinSpec, generate_symbol


def _symbol(name: str, pin_name: str = "IN") -> str:
    return generate_symbol(name, [PinSpec(number="1", name=pin_name)])


def test_add_symbol_creates_library_and_lists_it(tmp_path: Path) -> None:
    lib_file = project_library.add_symbol(tmp_path, "Parts", "ABC1", _symbol("ABC1"))

    assert lib_file == tmp_path / "libs" / "Parts.kicad_sym"
    text = lib_file.read_text(encoding="utf-8")
    assert text.count("(kicad_symbol_lib") == 1
    assert '(symbol "ABC1"' in text
    assert text.count("(") == text.count(")")
    table = (tmp_path / "sym-lib-table").read_text(encoding="utf-8")
    assert '(name "Parts")' in table
    assert "${KIPRJMOD}/libs/Parts.kicad_sym" in table


def test_add_symbol_appends_and_replaces(tmp_path: Path) -> None:
    project_library.add_symbol(tmp_path, "Parts", "ABC1", _symbol("ABC1", "OLD"))
    project_library.add_symbol(tmp_path, "Parts", "XYZ2", _symbol("XYZ2"))
    lib_file = project_library.add_symbol(tmp_path, "Parts", "ABC1", _symbol("ABC1", "NEW"))

    text = lib_file.read_text(encoding="utf-8")
    assert text.count('(symbol "ABC1"\n') == 1
    assert '(symbol "XYZ2"' in text
    assert '"NEW"' in text
    assert '"OLD"' not in text
    assert text.count("(") == text.count(")")
    table = (tmp_path / "sym-lib-table").read_text(encoding="utf-8")
    assert table.count('(name "Parts")') == 1


def test_register_library_keeps_existing_entries(tmp_path: Path) -> None:
    (tmp_path / "fp-lib-table").write_text(
        '(fp_lib_table\n\t(version 7)\n\t(lib (name "Other") (type "KiCad") (uri "x.pretty")'
        ' (options "") (descr ""))\n)\n',
        encoding="utf-8",
    )

    assert project_library.register_library(tmp_path, "footprint", "Parts", "y.pretty") is True
    assert project_library.register_library(tmp_path, "footprint", "Parts", "y.pretty") is False

    table = (tmp_path / "fp-lib-table").read_text(encoding="utf-8")
    assert '(name "Other")' in table
    assert table.count('(name "Parts")') == 1
    assert table.count("(") == table.count(")")


def test_bad_library_name_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Invalid library name"):
        project_library.add_symbol(tmp_path, "../escape", "ABC1", _symbol("ABC1"))


def test_footprint_from_pads_allows_shared_numbers_and_paste_openings(tmp_path: Path) -> None:
    text = generate_footprint_from_pads(
        "ODD-3",
        [
            {"number": 1, "x_mm": -0.8, "y_mm": -0.7, "w_mm": 0.75, "h_mm": 0.225},
            {"number": 1, "x_mm": -0.65, "y_mm": -0.9, "w_mm": 0.4, "h_mm": 0.575},
            {"number": 2, "x_mm": 0.9, "y_mm": 0.25, "w_mm": 0.6, "h_mm": 0.25,
             "corner_radius_mm": 0.05},
            {"number": 3, "x_mm": 0.0, "y_mm": -0.55, "w_mm": 0.35, "h_mm": 1.3, "paste": False},
        ],
        2.0,
        2.0,
        paste_apertures=[{"x_mm": 0.0, "y_mm": -0.925, "w_mm": 0.35, "h_mm": 0.55}],
    )  # fmt: skip

    assert text.count('(pad "1" smd rect') == 2
    assert '(pad "2" smd roundrect' in text
    assert "(roundrect_rratio 0.2000)" in text
    assert (
        '(pad "3" smd rect (at 0.0000 -0.5500) (size 0.3500 1.3000) (layers F.Cu F.Mask))' in text
    )
    assert '(pad "" smd rect (at 0.0000 -0.9250) (size 0.3500 0.5500) (layers F.Paste))' in text
    assert "F.CrtYd" in text
    assert text.count("(") == text.count(")")

    fp_file = project_library.add_footprint(tmp_path, "Parts", "ODD-3", text)
    assert fp_file == tmp_path / "libs" / "Parts.pretty" / "ODD-3.kicad_mod"
    assert "${KIPRJMOD}/libs/Parts.pretty" in (tmp_path / "fp-lib-table").read_text("utf-8")


def test_footprint_from_pads_courtyard_covers_pads_beyond_body() -> None:
    text = generate_footprint_from_pads(
        "WIDE",
        [{"number": 1, "x_mm": -1.0, "y_mm": 0.0, "w_mm": 0.6, "h_mm": 0.25}],
        1.0,
        1.0,
    )
    # Pad reaches x = -1.3; courtyard is 0.25 beyond that.
    assert "(start -1.5500 -0.7500)" in text


def test_footprint_from_pads_needs_complete_pads() -> None:
    with pytest.raises(ValueError, match="missing 'w_mm'"):
        generate_footprint_from_pads(
            "BAD", [{"number": 1, "x_mm": 0, "y_mm": 0, "h_mm": 1}], 1.0, 1.0
        )
