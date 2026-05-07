"""Layer mapping helpers across KiCad versions."""

from __future__ import annotations

from typing import Final, cast

from kipy.proto.board.board_types_pb2 import BoardLayer

_INNER_COPPER_LAYERS: Final[tuple[str, ...]] = tuple(f"In{index}_Cu" for index in range(1, 31))

CANONICAL_LAYER_NAMES: Final[tuple[str, ...]] = (
    "F_Cu",
    *_INNER_COPPER_LAYERS,
    "B_Cu",
    "F_SilkS",
    "B_SilkS",
    "F_Mask",
    "B_Mask",
    "F_Fab",
    "B_Fab",
    "F_CrtYd",
    "B_CrtYd",
    "Edge_Cuts",
    "Dwgs_User",
    "Cmts_User",
    "Eco1_User",
    "Eco2_User",
)

_LAYER_ATTRS: Final[dict[str, str]] = {
    "F_Cu": "BL_F_Cu",
    **{name: f"BL_{name}" for name in _INNER_COPPER_LAYERS},
    "B_Cu": "BL_B_Cu",
    "F_SilkS": "BL_F_SilkS",
    "B_SilkS": "BL_B_SilkS",
    "F_Mask": "BL_F_Mask",
    "B_Mask": "BL_B_Mask",
    "F_Fab": "BL_F_Fab",
    "B_Fab": "BL_B_Fab",
    "F_CrtYd": "BL_F_CrtYd",
    "B_CrtYd": "BL_B_CrtYd",
    "Edge_Cuts": "BL_Edge_Cuts",
    "Dwgs_User": "BL_Dwgs_User",
    "Cmts_User": "BL_Cmts_User",
    "Eco1_User": "BL_Eco1_User",
    "Eco2_User": "BL_Eco2_User",
}

# KiCad 7+ "friendly" layer names. KiCad's UI surfaces ``F.Silkscreen``
# while the canonical S-expression token remains ``F.SilkS``. Users (and
# kicad-cli output) routinely mix these forms — accept both shapes plus
# the underscore variants we use as canonical keys.
_FRIENDLY_ALIASES: Final[dict[str, str]] = {
    "F.Silkscreen": "F_SilkS",
    "B.Silkscreen": "B_SilkS",
    "F.Courtyard": "F_CrtYd",
    "B.Courtyard": "B_CrtYd",
    "User.Drawings": "Dwgs_User",
    "User.Comments": "Cmts_User",
    "User.Eco1": "Eco1_User",
    "User.Eco2": "Eco2_User",
}

_ALIASES: Final[dict[str, str]] = {
    "F.Cu": "F_Cu",
    "B.Cu": "B_Cu",
    **{f"In{index}.Cu": f"In{index}_Cu" for index in range(1, 31)},
    "Edge.Cuts": "Edge_Cuts",
    "F.SilkS": "F_SilkS",
    "B.SilkS": "B_SilkS",
    "F.Mask": "F_Mask",
    "B.Mask": "B_Mask",
    "F.Fab": "F_Fab",
    "B.Fab": "B_Fab",
    "F.CrtYd": "F_CrtYd",
    "B.CrtYd": "B_CrtYd",
    "Dwgs.User": "Dwgs_User",
    "Cmts.User": "Cmts_User",
    "Eco1.User": "Eco1_User",
    "Eco2.User": "Eco2_User",
    **_FRIENDLY_ALIASES,
    # Underscore form mirrors of the friendly names — users who normalize
    # ``F.Silkscreen`` → ``F_Silkscreen`` should resolve too.
    **{name.replace(".", "_"): canonical for name, canonical in _FRIENDLY_ALIASES.items()},
}


def resolve_layer_name(layer_name: str) -> str:
    """Resolve user-supplied layer names to canonical KiCad names."""
    normalized = _ALIASES.get(layer_name, layer_name)
    if normalized not in _LAYER_ATTRS:
        choices = ", ".join(CANONICAL_LAYER_NAMES)
        raise ValueError(f"Unknown layer '{layer_name}'. Expected one of: {choices}")
    return normalized


def resolve_layer(layer_name: str) -> BoardLayer.ValueType:
    """Resolve a canonical layer name to a KiCad board layer enum value."""
    canonical = resolve_layer_name(layer_name)
    return cast(BoardLayer.ValueType, getattr(BoardLayer, _LAYER_ATTRS[canonical]))
