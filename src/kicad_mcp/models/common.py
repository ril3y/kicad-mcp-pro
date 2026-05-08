"""Shared structural protocols used across KiCad tool modules."""

from __future__ import annotations

from typing import Protocol


class _PositionLike(Protocol):
    x_nm: int
    y_nm: int


class _TextValueLike(Protocol):
    value: str


class _TextFieldLike(Protocol):
    text: _TextValueLike


class _NetLike(Protocol):
    name: str


class _FootprintLike(Protocol):
    reference_field: _TextFieldLike
    value_field: _TextFieldLike
    position: object
    layer: int
    # ``FootprintInstance.definition`` exposes the underlying ``Footprint`` whose
    # ``pads`` list is the canonical way to walk a footprint's pads — kipy's
    # ``Pad`` has no ``parent`` back-reference, so consumers must reach pads via
    # this attribute. See ``_iter_board_pads_with_refs`` in tools/pcb.py.
    definition: object
    # ``FootprintAttributes`` proto wrapper (see board_types.py:1495+) carrying
    # ``do_not_populate`` / ``exclude_from_bill_of_materials`` /
    # ``exclude_from_position_files`` / ``not_in_schematic`` bool flags. Typed
    # as ``object`` because the kipy class isn't available everywhere we
    # consume the Protocol; consumers (``pcb_set_footprint_attributes``) read
    # it back as a dynamic attribute setter.
    attributes: object


class _FootprintAttributesLike(Protocol):
    """Subset of kipy's ``FootprintAttributes`` proto wrapper used by
    ``pcb_set_footprint_attributes``. Each is a settable bool — the wrapper
    writes to the underlying proto on assignment so ``update_items`` can
    ship the change back to pcbnew (PR #4 / PR #11)."""

    do_not_populate: bool
    exclude_from_bill_of_materials: bool
    exclude_from_position_files: bool
    not_in_schematic: bool


class _PadLike(Protocol):
    # NOTE: kipy's ``Pad`` class has no ``parent`` back-reference. To resolve
    # a pad's footprint, walk ``board.get_footprints()`` and inspect each
    # footprint's ``definition.pads``. Earlier revisions of this Protocol
    # declared ``parent: _FootprintLike`` which masked the real attribute
    # error and let buggy code ship; do not re-add it.
    number: str | int
    position: _PositionLike
    net: _NetLike


__all__ = [
    "_FootprintAttributesLike",
    "_FootprintLike",
    "_NetLike",
    "_PadLike",
    "_PositionLike",
    "_TextFieldLike",
    "_TextValueLike",
]
