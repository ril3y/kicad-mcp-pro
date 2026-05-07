"""Unit tests for low-level routing helpers in kicad_mcp.tools.routing."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from kicad_mcp.tools import routing


def _make_pad(number: str | int) -> SimpleNamespace:
    return SimpleNamespace(number=number)


def _make_footprint(reference: str, pad_numbers: list[str | int]) -> SimpleNamespace:
    """Build a fake FootprintInstance compatible with routing._find_pad."""
    return SimpleNamespace(
        reference_field=SimpleNamespace(text=SimpleNamespace(value=reference)),
        definition=SimpleNamespace(pads=[_make_pad(n) for n in pad_numbers]),
    )


def test_find_pad_returns_matching_pad_via_footprint_walk(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: _find_pad must NOT use ``pad.parent`` (kipy Pad has no such attr).

    The bug was that _find_pad iterated ``board.get_pads()`` and accessed
    ``pad.parent.reference_field`` which fails at runtime with
    ``AttributeError: 'Pad' object has no attribute 'parent'``. Fix is to
    iterate footprints first and walk ``footprint.definition.pads``.
    """
    fps = [
        _make_footprint("J1", ["1", "2", "3"]),
        _make_footprint("D1", ["1", "2", "3"]),
        _make_footprint("J_M1", list(range(1, 27))),
    ]
    monkeypatch.setattr(
        "kicad_mcp.tools.routing.get_board",
        lambda: SimpleNamespace(get_footprints=lambda: fps),
    )

    pad = routing._find_pad("D1", "2")
    assert pad is not None
    assert str(pad.number) == "2"


def test_find_pad_returns_none_when_reference_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fps = [_make_footprint("J1", ["1", "2"])]
    monkeypatch.setattr(
        "kicad_mcp.tools.routing.get_board",
        lambda: SimpleNamespace(get_footprints=lambda: fps),
    )

    assert routing._find_pad("J99", "1") is None


def test_find_pad_returns_none_when_reference_matches_but_pad_number_does_not(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fps = [_make_footprint("J1", ["1", "2"])]
    monkeypatch.setattr(
        "kicad_mcp.tools.routing.get_board",
        lambda: SimpleNamespace(get_footprints=lambda: fps),
    )

    # Once we find the matching reference, we should NOT continue searching
    # other footprints for a pad that doesn't exist on this one.
    assert routing._find_pad("J1", "99") is None


def test_find_pad_handles_int_pad_numbers_as_strings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """26-pin Amphenol footprints expose pad numbers as ints."""
    fps = [_make_footprint("J_M1", [1, 12, 14, 25, 26])]
    monkeypatch.setattr(
        "kicad_mcp.tools.routing.get_board",
        lambda: SimpleNamespace(get_footprints=lambda: fps),
    )

    pad = routing._find_pad("J_M1", "12")
    assert pad is not None
    assert str(pad.number) == "12"
