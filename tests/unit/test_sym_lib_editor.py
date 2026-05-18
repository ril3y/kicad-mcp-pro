# pyright: reportPrivateUsage=false, reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false
"""Unit tests for ``kicad_mcp.utils.sym_lib_editor``.

These tests exercise the tree-level editing primitives that back the
``lib_set_pin_name`` MCP tool. The original need was a real-world
incident: two prior regex-based attempts to rename pin "1"->"Coil1" on
an ``easyeda2kicad``-imported ``G2R-2-DC12V`` symbol corrupted the
library file by miscounting parens inside ``(effects ...)`` blocks and
inside string values like ``"OMRON(欧姆龙)"``. These tests use a
synthetic .kicad_sym fixture that includes both pitfalls (nested
``(effects ...)`` and a parens-in-string property value) so we can pin
that the parser handles them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from kicad_mcp.utils.sym_lib_editor import (
    dump_sym_lib,
    find_pin,
    find_symbol,
    iter_pins,
    iter_top_level_symbols,
    load_sym_lib,
    set_pin_name,
    set_pin_type,
)


_FIXTURE_LIB = """\
(kicad_symbol_lib (version 20241209) (generator "test")
  (symbol "TEST_RELAY"
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (property "Reference" "K" (at 0 16.51 0) (effects (font (size 1.27 1.27))))
    (property "Value" "TEST_RELAY" (at 0 -17.78 0) (effects (font (size 1.27 1.27))))
    (property "Manufacturer" "FAKECO(SOMECITY)" (at 0 -25.40 0) (effects (font (size 1.27 1.27)) hide))
    (property "ki_keywords" "test relay" (at 0 -33.02 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "TEST_RELAY_0_1"
      (rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width 0) (type default)) (fill (type background)))
      (pin unspecified line (at -7.62 2.54 0) (length 2.54)
        (name "1" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin unspecified line (at 7.62 2.54 180) (length 2.54)
        (name "2" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin unspecified line (at -7.62 -2.54 0) (length 2.54)
        (name "3" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
  )
  (symbol "OTHER_PART"
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (symbol "OTHER_PART_0_1"
      (pin power_in line (at 0 5.08 270) (length 2.54)
        (name "VCC" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
  )
)
"""


def _write_fixture(tmp_path: Path) -> Path:
    p = tmp_path / "fake.kicad_sym"
    p.write_text(_FIXTURE_LIB, encoding="utf-8")
    return p


def test_load_sym_lib_parses_real_kicad_sym_with_parens_in_strings(
    tmp_path: Path,
) -> None:
    """The fixture's "FAKECO(SOMECITY)" property has unbalanced parens
    when counted as raw bytes — sexpdata must treat them as string
    contents and parse the file cleanly. Pre-existing regex-based
    editors miscounted these and corrupted the file."""
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    assert isinstance(tree, list)
    # Two top-level symbols
    top_syms = list(iter_top_level_symbols(tree))
    names = [s[1] for s in top_syms]
    assert names == ["TEST_RELAY", "OTHER_PART"]


def test_load_sym_lib_rejects_non_kicad_sym_files(tmp_path: Path) -> None:
    """A file whose top-level token isn't ``kicad_symbol_lib`` is not a
    library and must be rejected with a clear error. Without this guard
    callers could silently corrupt e.g. a .kicad_sch file."""
    p = tmp_path / "not_a_lib.kicad_sym"
    p.write_text('(some_other_doc (version 1))\n', encoding="utf-8")
    with pytest.raises(ValueError, match="kicad_symbol_lib"):
        load_sym_lib(p)


def test_load_sym_lib_raises_when_file_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_sym_lib(tmp_path / "nope.kicad_sym")


def test_find_symbol_returns_matching_top_level_block(tmp_path: Path) -> None:
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    sym = find_symbol(tree, "TEST_RELAY")
    assert sym is not None
    assert sym[1] == "TEST_RELAY"


def test_find_symbol_returns_none_when_name_absent(tmp_path: Path) -> None:
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    assert find_symbol(tree, "DOES_NOT_EXIST") is None


def test_iter_pins_walks_into_nested_sub_symbol_block(tmp_path: Path) -> None:
    """Pins live one level deeper than the top-level symbol — under the
    ``<name>_0_1`` body sub-block. The iterator must descend; a naive
    children-only scan would return nothing for any real KiCad symbol."""
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    sym = find_symbol(tree, "TEST_RELAY")
    assert sym is not None
    pins = list(iter_pins(sym))
    assert len(pins) == 3


def test_find_pin_by_number(tmp_path: Path) -> None:
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    sym = find_symbol(tree, "TEST_RELAY")
    assert sym is not None
    pin2 = find_pin(sym, "2")
    assert pin2 is not None
    # Confirm the right pin came back
    nums = [c[1] for c in pin2 if isinstance(c, list) and len(c) >= 2
            and hasattr(c[0], "value") and c[0].value() == "number"]
    assert nums == ["2"]


def test_set_pin_name_rewrites_existing_name(tmp_path: Path) -> None:
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    sym = find_symbol(tree, "TEST_RELAY")
    assert sym is not None
    pin = find_pin(sym, "1")
    assert pin is not None
    assert set_pin_name(pin, "Coil1") is True
    # Re-find to confirm
    pin2 = find_pin(sym, "1")
    names = [c[1] for c in pin2 if isinstance(c, list) and len(c) >= 2
             and hasattr(c[0], "value") and c[0].value() == "name"]
    assert names == ["Coil1"]


def test_set_pin_name_returns_false_when_name_unchanged(tmp_path: Path) -> None:
    """No-op rewrites must signal "no change" so callers don't write the
    file back unnecessarily."""
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    sym = find_symbol(tree, "TEST_RELAY")
    pin = find_pin(sym, "1")
    assert set_pin_name(pin, "1") is False  # already "1"


def test_set_pin_type_rewrites_electrical_type(tmp_path: Path) -> None:
    """The pin's electrical type is the second element of the
    ``(pin TYPE SHAPE ...)`` block. Locking the in-place mutation here
    so a refactor that touched the wrong index would fail loudly."""
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    sym = find_symbol(tree, "TEST_RELAY")
    pin = find_pin(sym, "1")
    # Initial type is "unspecified"
    assert hasattr(pin[1], "value") and pin[1].value() == "unspecified"
    assert set_pin_type(pin, "passive") is True
    assert pin[1].value() == "passive"


def test_dump_sym_lib_round_trip_preserves_structure(tmp_path: Path) -> None:
    """Parse → dump → re-parse must produce the same tree of names/values.
    The output formatting may differ from the input (sexpdata is more
    compact than KiCad's canonical layout) but KiCad's parser is
    whitespace-agnostic so the file still loads."""
    p = _write_fixture(tmp_path)
    tree1 = load_sym_lib(p)
    text2 = dump_sym_lib(tree1)
    p2 = tmp_path / "round_trip.kicad_sym"
    p2.write_text(text2, encoding="utf-8")
    tree2 = load_sym_lib(p2)
    # Both must surface the same set of top-level symbol names
    names1 = sorted(s[1] for s in iter_top_level_symbols(tree1))
    names2 = sorted(s[1] for s in iter_top_level_symbols(tree2))
    assert names1 == names2
    # And both must have the same pin numbers per symbol
    for name in names1:
        s1 = find_symbol(tree1, name)
        s2 = find_symbol(tree2, name)
        pins1 = sorted(
            c[1] for p in iter_pins(s1) for c in p
            if isinstance(c, list) and len(c) >= 2
            and hasattr(c[0], "value") and c[0].value() == "number"
        )
        pins2 = sorted(
            c[1] for p in iter_pins(s2) for c in p
            if isinstance(c, list) and len(c) >= 2
            and hasattr(c[0], "value") and c[0].value() == "number"
        )
        assert pins1 == pins2, f"pin numbers differ for {name}"


def test_set_pin_name_then_dump_then_load_preserves_change(
    tmp_path: Path,
) -> None:
    """End-to-end edit: rename a pin, dump, reload, confirm the name
    survived the round-trip. This is what the MCP tool actually does."""
    p = _write_fixture(tmp_path)
    tree = load_sym_lib(p)
    sym = find_symbol(tree, "TEST_RELAY")
    set_pin_name(find_pin(sym, "1"), "Coil1")
    set_pin_name(find_pin(sym, "2"), "Coil2")
    set_pin_name(find_pin(sym, "3"), "COM_A")

    text2 = dump_sym_lib(tree)
    p2 = tmp_path / "edited.kicad_sym"
    p2.write_text(text2, encoding="utf-8")

    tree2 = load_sym_lib(p2)
    sym2 = find_symbol(tree2, "TEST_RELAY")

    def name_for(pin_num: str) -> str:
        pin = find_pin(sym2, pin_num)
        for ch in pin:
            if (isinstance(ch, list) and len(ch) >= 2
                    and hasattr(ch[0], "value") and ch[0].value() == "name"):
                return ch[1]
        return ""

    assert name_for("1") == "Coil1"
    assert name_for("2") == "Coil2"
    assert name_for("3") == "COM_A"
