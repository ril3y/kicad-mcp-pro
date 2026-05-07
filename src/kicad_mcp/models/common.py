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
    "_FootprintLike",
    "_NetLike",
    "_PadLike",
    "_PositionLike",
    "_TextFieldLike",
    "_TextValueLike",
]
