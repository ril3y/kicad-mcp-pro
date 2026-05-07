from __future__ import annotations

import pytest
from kipy.proto.board.board_types_pb2 import BoardLayer

from kicad_mcp.utils.layers import resolve_layer, resolve_layer_name


def test_layer_alias_resolution() -> None:
    assert resolve_layer_name("F.Cu") == "F_Cu"
    assert resolve_layer_name("In30.Cu") == "In30_Cu"


def test_resolve_layer_returns_board_layer_value() -> None:
    layer = resolve_layer("F.Cu")
    inner = resolve_layer("In30.Cu")

    assert isinstance(layer, int)
    assert layer == BoardLayer.BL_F_Cu
    assert inner == BoardLayer.Value("BL_In30_Cu")


def test_resolve_layer_rejects_unknown_layer() -> None:
    try:
        resolve_layer("Not.A.Layer")
    except ValueError as exc:
        assert "Unknown layer" in str(exc)
    else:
        raise AssertionError("resolve_layer() should reject invalid layers")


@pytest.mark.parametrize(
    ("input_name", "canonical"),
    [
        # KiCad 7+ "friendly" names — surface in pcbnew UI and kicad-cli output.
        ("F.Silkscreen", "F_SilkS"),
        ("B.Silkscreen", "B_SilkS"),
        ("F.Courtyard", "F_CrtYd"),
        ("B.Courtyard", "B_CrtYd"),
        ("User.Drawings", "Dwgs_User"),
        ("User.Comments", "Cmts_User"),
        ("User.Eco1", "Eco1_User"),
        ("User.Eco2", "Eco2_User"),
        # Underscore-form variants (users who already normalized the dot).
        ("F_Silkscreen", "F_SilkS"),
        ("B_Silkscreen", "B_SilkS"),
        ("F_Courtyard", "F_CrtYd"),
        ("B_Courtyard", "B_CrtYd"),
        ("User_Drawings", "Dwgs_User"),
        ("User_Comments", "Cmts_User"),
        ("User_Eco1", "Eco1_User"),
        ("User_Eco2", "Eco2_User"),
    ],
)
def test_resolve_friendly_layer_aliases(input_name: str, canonical: str) -> None:
    """KiCad 7+ surfaces ``F.Silkscreen`` etc. but the S-expr keeps ``F.SilkS``.

    Regression target: the junction-passive build hit
    ``Unknown layer 'F_Silkscreen'`` because only the legacy abbreviated
    forms were aliased. Users expect to pass either form interchangeably.
    """
    assert resolve_layer_name(input_name) == canonical
    # And the BoardLayer enum lookup must round-trip too.
    assert resolve_layer(input_name) == BoardLayer.Value(f"BL_{canonical}")


def test_resolve_layer_is_case_sensitive() -> None:
    """Lock the case-sensitive contract.

    KiCad's UI and ``kicad-cli`` output preserve case, so we deliberately
    don't fuzzy-match. If someone later adds case-insensitive matching
    they should update this test along with the design decision.
    """
    with pytest.raises(ValueError, match="Unknown layer"):
        resolve_layer_name("f.silkscreen")
    with pytest.raises(ValueError, match="Unknown layer"):
        resolve_layer_name("F.SILKSCREEN")
