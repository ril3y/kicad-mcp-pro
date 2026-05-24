# pyright: reportPrivateUsage=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingParameterType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportReturnType=false
# pyright: reportInvalidTypeForm=false
# ruff: noqa: ANN001, ANN201
"""Regression tests for get_pin_positions y-flip behavior.

Protects against the double-flip bug previously at
``src/kicad_mcp/tools/schematic.py:2048`` where the code did
``rotate_point(px, -py, rotation)`` AND then post-flipped via
``sym_y - ry``. The two flips cancelled each other so the function
returned library-frame coordinates (off by a y-mirror around the
symbol center). For symbols whose pins all have lib-y == 0 (e.g.
``Device:R``) the bug was invisible, but multi-pin parts with a top
pin (e.g. VDD) and a bottom pin (e.g. GND) had those pins reported
swapped vertically.

The fix is to call ``rotate_point(px, py, rotation)`` so the only
y-flip is the schematic-side ``sym_y - ry``.
"""

from __future__ import annotations

from pathlib import Path

import pytest


def _write_optoisolator_lib(symbols_dir: Path) -> None:
    """Write a fixture library with an EL817-shaped 4-pin symbol.

    Pin 1 lives at lib (-7.62, 2.54) and pin 4 at lib (7.62, -2.54).
    These non-zero y values are what the buggy double-flip swapped.
    """
    (symbols_dir / "Isolator.kicad_sym").write_text(
        (
            "(kicad_symbol_lib (version 20250316) (generator pytest)\n"
            '  (symbol "EL817"\n'
            '    (property "Reference" "U" (id 0) (at 0 5.08 0))\n'
            '    (property "Value" "EL817" (id 1) (at 0 -5.08 0))\n'
            '    (symbol "EL817_1_1"\n'
            "      (pin passive line (at -7.62 2.54 0) (length 2.54)"
            ' (name "A") (number "1"))\n'
            "      (pin passive line (at -7.62 -2.54 0) (length 2.54)"
            ' (name "K") (number "2"))\n'
            "      (pin passive line (at 7.62 -2.54 180) (length 2.54)"
            ' (name "E") (number "3"))\n'
            "      (pin passive line (at 7.62 2.54 180) (length 2.54)"
            ' (name "C") (number "4"))\n'
            "    )\n"
            "  )\n"
            ")\n"
        ),
        encoding="utf-8",
    )


@pytest.fixture
def isolator_project(tmp_path: Path, fake_cli: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Project + symbol library configured for direct get_pin_positions calls.

    Uses environment variables consumed by ``KiCadMCPConfig`` rather than
    poking at the cached singleton — the ``reset_globals`` autouse fixture
    in ``tests/conftest.py`` already clears the cache before this test runs
    and the env vars below.
    """
    _ = fake_cli  # ensure the kicad-cli env var is set
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "demo.kicad_pro").write_text('{"meta": {"version": 1}}', encoding="utf-8")

    symbols_dir = tmp_path / "symbols"
    symbols_dir.mkdir()
    _write_optoisolator_lib(symbols_dir)

    monkeypatch.setenv("KICAD_MCP_PROJECT_DIR", str(project_dir))
    monkeypatch.setenv("KICAD_MCP_SYMBOL_LIBRARY_DIR", str(symbols_dir))
    monkeypatch.setenv("KICAD_MCP_WORKSPACE_ROOT", str(tmp_path))

    return project_dir


def test_pin_positions_use_single_y_flip_rot0(isolator_project: Path) -> None:
    """At rot=0 a lib-y pin must flip exactly once (sym_y - lib_y).

    With the buggy double-flip, pin 1 (lib y=+2.54) would have been
    reported at schematic y=102.54 instead of the correct 97.46. This
    test pins the correct value to fail-loud on regression.
    """
    from kicad_mcp.tools.schematic import get_pin_positions

    pins = get_pin_positions(
        library="Isolator",
        symbol_name="EL817",
        sym_x=100.0,
        sym_y=100.0,
        rotation=0,
        unit=1,
    )

    # Top-side pins (lib y > 0) project to schematic y < sym_y.
    assert pins["1"] == (92.38, 97.46), (
        f"Pin 1 at lib (-7.62, +2.54) must map to (92.38, 97.46); "
        f"got {pins['1']}. Buggy double-flip would yield (92.38, 102.54)."
    )
    assert pins["4"] == (107.62, 97.46), (
        f"Pin 4 at lib (+7.62, +2.54) must map to (107.62, 97.46); got {pins['4']}."
    )
    # Bottom-side pins (lib y < 0) project to schematic y > sym_y.
    assert pins["2"] == (92.38, 102.54), (
        f"Pin 2 at lib (-7.62, -2.54) must map to (92.38, 102.54); got {pins['2']}."
    )
    assert pins["3"] == (107.62, 102.54), (
        f"Pin 3 at lib (+7.62, -2.54) must map to (107.62, 102.54); got {pins['3']}."
    )

    # Top and bottom pins must not collide in schematic y.
    assert pins["1"][1] != pins["2"][1]
    assert pins["1"][1] < pins["2"][1], (
        "Pin 1 (lib top, y=+2.54) must be ABOVE Pin 2 (lib bottom, y=-2.54) "
        "in schematic frame (y-DOWN). The buggy double-flip swapped them."
    )


def test_pin_positions_rotation_90(isolator_project: Path) -> None:
    """Rotation must apply to the raw lib (x, y), not (x, -y).

    rotate_point(-7.62, 2.54, 90) = (-2.54, -7.62), so pin 1 lands at
    (sym_x - 2.54, sym_y - (-7.62)) = (97.46, 107.62).

    The buggy code did rotate_point(-7.62, -2.54, 90) = (2.54, -7.62),
    which would produce (102.54, 107.62) — different x.
    """
    from kicad_mcp.tools.schematic import get_pin_positions

    pins = get_pin_positions(
        library="Isolator",
        symbol_name="EL817",
        sym_x=100.0,
        sym_y=100.0,
        rotation=90,
        unit=1,
    )

    assert pins["1"] == (97.46, 107.62), (
        f"Pin 1 at lib (-7.62, +2.54) rot=90 must map to (97.46, 107.62); "
        f"got {pins['1']}. Buggy code would yield (102.54, 107.62)."
    )
    assert pins["2"] == (102.54, 107.62), (
        f"Pin 2 at lib (-7.62, -2.54) rot=90 must map to (102.54, 107.62); got {pins['2']}."
    )


def test_pin_positions_rotation_270(isolator_project: Path) -> None:
    """rot=270 path coverage.

    rotate_point(-7.62, 2.54, 270) = (2.54, 7.62), so pin 1 lands at
    (sym_x + 2.54, sym_y - 7.62) = (102.54, 92.38).

    The buggy code did rotate_point(-7.62, -2.54, 270) = (-2.54, 7.62),
    which would produce (97.46, 92.38) — different x.
    """
    from kicad_mcp.tools.schematic import get_pin_positions

    pins = get_pin_positions(
        library="Isolator",
        symbol_name="EL817",
        sym_x=100.0,
        sym_y=100.0,
        rotation=270,
        unit=1,
    )

    assert pins["1"] == (102.54, 92.38), (
        f"Pin 1 at lib (-7.62, +2.54) rot=270 must map to (102.54, 92.38); "
        f"got {pins['1']}. Buggy code would yield (97.46, 92.38)."
    )
    assert pins["2"] == (97.46, 92.38), (
        f"Pin 2 at lib (-7.62, -2.54) rot=270 must map to (97.46, 92.38); got {pins['2']}."
    )


def test_pin_positions_zero_y_pins_unaffected(isolator_project: Path) -> None:
    """Symbols whose pins all have lib y=0 (e.g. Device:R) are immune to the
    double-flip bug. Pin this behavior so the regression test surface stays
    honest about which cases the bug DID NOT affect.
    """
    from kicad_mcp.tools.schematic import get_pin_positions

    # Reuse the EL817 lib but flatten by rewriting via the existing fixture.
    # The simpler proof is to assert: a pin at lib y=0 at rotation=0 lands at
    # exactly sym_y. Add a transient symbol for this assertion.
    symbols_dir = isolator_project.parent / "symbols"
    (symbols_dir / "FlatDev.kicad_sym").write_text(
        (
            "(kicad_symbol_lib (version 20250316) (generator pytest)\n"
            '  (symbol "FlatR"\n'
            '    (property "Reference" "R" (id 0) (at 0 2.54 0))\n'
            '    (property "Value" "FlatR" (id 1) (at 0 -2.54 0))\n'
            "    (pin passive line (at -2.54 0 0) (length 2.54)"
            ' (name "1") (number "1"))\n'
            "    (pin passive line (at 2.54 0 180) (length 2.54)"
            ' (name "2") (number "2"))\n'
            "  )\n"
            ")\n"
        ),
        encoding="utf-8",
    )

    pins = get_pin_positions(
        library="FlatDev",
        symbol_name="FlatR",
        sym_x=50.0,
        sym_y=50.0,
        rotation=0,
        unit=1,
    )

    assert pins["1"] == (47.46, 50.0), pins
    assert pins["2"] == (52.54, 50.0), pins
