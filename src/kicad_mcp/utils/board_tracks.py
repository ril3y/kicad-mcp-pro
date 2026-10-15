"""Headless parser for ``(segment ...)`` blocks in a ``.kicad_pcb`` file.

Lets read-only tools answer "what tracks does net X have, and what's the
narrowest one" without needing a live IPC connection or pcbnew running.
Handles both the legacy ``(net N "name")`` and the KiCad 10.99 ``(net "name")``
segment-net syntaxes.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterator
from dataclasses import dataclass

from .sexpr import _extract_block as extract_block  # noqa: PLC2701

_FLOAT = r"-?\d+(?:\.\d+)?"
_START_RE = re.compile(rf"\(start\s+({_FLOAT})\s+({_FLOAT})\)")
_END_RE = re.compile(rf"\(end\s+({_FLOAT})\s+({_FLOAT})\)")
_WIDTH_RE = re.compile(rf"\(width\s+({_FLOAT})\)")
_LAYER_RE = re.compile(r'\(layer\s+"([^"]+)"\)')
# KiCad 10.99 inlines the net name into segments; legacy boards use the
# pre-declared (net N "name") table and reference the integer code.
_NET_NAME_RE = re.compile(r'\(net\s+"([^"]+)"\)')
_NET_CODE_RE = re.compile(r"\(net\s+(\d+)\)")
# Top-level `(net N "name")` declarations used in legacy boards.
_NET_DECL_RE = re.compile(r'\(net\s+(\d+)\s+"((?:\\.|[^"\\])*)"\)')


@dataclass(frozen=True)
class TrackSegment:
    """A single ``(segment ...)`` block lifted from a ``.kicad_pcb`` file.

    All coordinates and widths are in millimeters.
    """

    start_mm: tuple[float, float]
    end_mm: tuple[float, float]
    width_mm: float
    layer: str
    net_name: str

    @property
    def length_mm(self) -> float:
        return math.hypot(
            self.end_mm[0] - self.start_mm[0],
            self.end_mm[1] - self.start_mm[1],
        )


def _net_code_table(content: str) -> dict[int, str]:
    """Build a ``code -> name`` map from legacy ``(net N "name")`` decls."""
    return {int(m.group(1)): m.group(2) for m in _NET_DECL_RE.finditer(content)}


def _iter_segment_blocks(content: str) -> Iterator[str]:
    cursor = 0
    while cursor < len(content):
        position = content.find("(segment", cursor)
        if position < 0:
            return
        block, length = extract_block(content, position)
        if not block:
            return
        yield block
        cursor = position + length


def parse_board_segments(content: str) -> list[TrackSegment]:
    """Extract every ``(segment ...)`` block from a ``.kicad_pcb`` file.

    Malformed segments (missing required fields) are skipped silently rather
    than raising — board files written by older KiCad versions sometimes have
    odd shapes, and the goal here is best-effort enumeration.
    """
    net_codes = _net_code_table(content)
    segments: list[TrackSegment] = []
    for block in _iter_segment_blocks(content):
        start_m = _START_RE.search(block)
        end_m = _END_RE.search(block)
        width_m = _WIDTH_RE.search(block)
        layer_m = _LAYER_RE.search(block)
        if not (start_m and end_m and width_m and layer_m):
            continue

        net_name_m = _NET_NAME_RE.search(block)
        if net_name_m is not None:
            net_name = net_name_m.group(1)
        else:
            code_m = _NET_CODE_RE.search(block)
            if code_m is None:
                continue
            net_name = net_codes.get(int(code_m.group(1)), "")

        segments.append(
            TrackSegment(
                start_mm=(float(start_m.group(1)), float(start_m.group(2))),
                end_mm=(float(end_m.group(1)), float(end_m.group(2))),
                width_mm=float(width_m.group(1)),
                layer=layer_m.group(1),
                net_name=net_name,
            )
        )
    return segments


def segments_for_net(
    content: str,
    net_name: str,
    *,
    case_sensitive: bool = True,
) -> list[TrackSegment]:
    """Filter ``parse_board_segments`` by net name."""
    target = net_name if case_sensitive else net_name.casefold()
    return [
        seg
        for seg in parse_board_segments(content)
        if (seg.net_name if case_sensitive else seg.net_name.casefold()) == target
    ]


__all__ = [
    "TrackSegment",
    "parse_board_segments",
    "segments_for_net",
]
