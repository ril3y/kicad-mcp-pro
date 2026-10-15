# pyright: reportPrivateUsage=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingParameterType=false
# ruff: noqa: ANN001, ANN201
"""Unit tests for the headless ``.kicad_pcb`` segment parser.

Targets two real-world syntaxes:
- KiCad 10.99: ``(net "name")`` baked into each segment
- KiCad 9.x legacy: ``(net N)`` reference + a top-level ``(net N "name")`` table
"""

from __future__ import annotations

from kicad_mcp.utils.board_tracks import (
    TrackSegment,
    parse_board_segments,
    segments_for_net,
)

_KICAD_10_99_FIXTURE = """
(kicad_pcb
\t(version 20240108)
\t(generator "pytest")
\t(segment
\t\t(start 10.0 10.0)
\t\t(end 20.0 10.0)
\t\t(width 0.25)
\t\t(layer "F.Cu")
\t\t(net "VCC")
\t\t(uuid "aaa")
\t)
\t(segment
\t\t(start 20.0 10.0)
\t\t(end 30.0 10.0)
\t\t(width 0.50)
\t\t(layer "B.Cu")
\t\t(net "VCC")
\t\t(uuid "bbb")
\t)
\t(segment
\t\t(start 0.0 0.0)
\t\t(end 5.0 0.0)
\t\t(width 0.20)
\t\t(layer "F.Cu")
\t\t(net "GND")
\t\t(uuid "ccc")
\t)
)
"""

_KICAD_9_LEGACY_FIXTURE = """
(kicad_pcb
\t(version 20221218)
\t(generator pcbnew)
\t(net 1 "VCC")
\t(net 2 "GND")
\t(segment (start 0 0) (end 10 0) (width 0.25) (layer "F.Cu") (net 1) (tstamp 1))
\t(segment (start 0 5) (end 10 5) (width 0.50) (layer "B.Cu") (net 2) (tstamp 2))
)
"""


def test_parse_kicad_10_99_segments():
    """KiCad 10.99 syntax: net name is inlined into each segment."""
    segs = parse_board_segments(_KICAD_10_99_FIXTURE)
    assert len(segs) == 3

    vcc = [s for s in segs if s.net_name == "VCC"]
    assert len(vcc) == 2
    assert {s.width_mm for s in vcc} == {0.25, 0.50}
    assert {s.layer for s in vcc} == {"F.Cu", "B.Cu"}

    # The 0.25-wide F.Cu VCC segment is 10 mm long; length_mm uses
    # Euclidean distance so this is a stable property pin.
    first = next(s for s in vcc if s.width_mm == 0.25)
    assert first.length_mm == 10.0


def test_parse_kicad_9_legacy_segments():
    """KiCad 9.x legacy: segments reference a (net N) code that resolves
    against the top-level (net N "name") declarations."""
    segs = parse_board_segments(_KICAD_9_LEGACY_FIXTURE)
    assert len(segs) == 2
    names = {s.net_name for s in segs}
    assert names == {"VCC", "GND"}


def test_segments_for_net_case_sensitive_by_default():
    """Net names ARE case-sensitive in KiCad. Match the convention; tests
    asking for ``vcc`` shouldn't find ``VCC`` unless they opt in."""
    case_match = segments_for_net(_KICAD_10_99_FIXTURE, "VCC")
    case_miss = segments_for_net(_KICAD_10_99_FIXTURE, "vcc")
    assert len(case_match) == 2
    assert case_miss == []


def test_segments_for_net_case_insensitive_opt_in():
    """``case_sensitive=False`` for ergonomic CLI / agent use."""
    segs = segments_for_net(_KICAD_10_99_FIXTURE, "vcc", case_sensitive=False)
    assert len(segs) == 2


def test_unknown_net_returns_empty_list():
    """No segments + no exception — let callers render the "no tracks
    found" message."""
    assert segments_for_net(_KICAD_10_99_FIXTURE, "DOES_NOT_EXIST") == []


def test_malformed_segment_block_is_skipped_silently():
    """Older KiCad versions occasionally emit segments missing one field.
    We skip them rather than crash so a single bad segment doesn't break
    an otherwise-good net analysis."""
    fixture = """
    (kicad_pcb
        (segment (start 0 0) (end 5 0) (width 0.25) (layer "F.Cu") (net "VCC") (uuid "ok"))
        (segment (start 0 0) (width 0.25) (layer "F.Cu") (net "VCC") (uuid "missing-end"))
    )
    """
    segs = parse_board_segments(fixture)
    assert len(segs) == 1
    assert segs[0].length_mm == 5.0


def test_length_mm_uses_euclidean_distance():
    """Pythagorean check — for a 3-4-5 triangle segment, length is 5 mm."""
    seg = TrackSegment(
        start_mm=(0.0, 0.0),
        end_mm=(3.0, 4.0),
        width_mm=0.25,
        layer="F.Cu",
        net_name="X",
    )
    assert seg.length_mm == 5.0


def test_segment_without_any_net_marker_is_dropped():
    """A segment with neither ``(net N)`` code nor ``(net "name")`` text
    has nothing to attach to — drop it from the result rather than
    inventing an empty net name (which would silently merge with the
    "" net used by unrouted board content)."""
    fixture = """
    (kicad_pcb
        (segment (start 0 0) (end 5 0) (width 0.25) (layer "F.Cu") (uuid "no-net"))
    )
    """
    assert parse_board_segments(fixture) == []
