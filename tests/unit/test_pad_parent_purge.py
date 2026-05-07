"""Regression tests for the pad.parent purge.

kipy's ``Pad`` class has no ``parent`` back-reference. Several tools used
``pad.parent.reference_field.text.value`` to resolve a pad's footprint ref;
they crashed at runtime. The fix walks ``board.get_footprints()`` and pairs
each pad with its footprint's reference designator via the shared helper
``kicad_mcp.tools.pcb._iter_board_pads_with_refs``.

These tests use :class:`SimpleNamespace` fakes that intentionally lack a
``parent`` attribute. They invoke the **real** production helper rather
than re-implementing the iteration in the test body — a regression that
re-introduces ``pad.parent`` will fail the suite with ``AttributeError``.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest


def _make_pad(
    number: str | int,
    *,
    x_nm: int = 0,
    y_nm: int = 0,
    net_name: str = "",
    size_x_nm: int = 1_000_000,
    size_y_nm: int = 1_000_000,
    pad_id: str | None = None,
) -> SimpleNamespace:
    """Build a fake Pad without a ``parent`` attribute (mirrors kipy's API)."""
    return SimpleNamespace(
        number=number,
        position=SimpleNamespace(x_nm=x_nm, y_nm=y_nm),
        net=SimpleNamespace(name=net_name),
        size=SimpleNamespace(x_nm=size_x_nm, y_nm=size_y_nm),
        id=pad_id,
    )


def _make_footprint(reference: str, pads: list[SimpleNamespace]) -> SimpleNamespace:
    """Fake FootprintInstance: ``reference_field`` + ``definition.pads``."""
    return SimpleNamespace(
        reference_field=SimpleNamespace(text=SimpleNamespace(value=reference)),
        definition=SimpleNamespace(pads=pads),
    )


def _patch_board_pcb(monkeypatch: pytest.MonkeyPatch, fps: list[SimpleNamespace]) -> None:
    """Monkeypatch ``kicad_mcp.tools.pcb.get_board`` with a fake board."""
    fake_board = SimpleNamespace(get_footprints=lambda: fps)
    monkeypatch.setattr("kicad_mcp.tools.pcb.get_board", lambda: fake_board)


# ---------- pcb._iter_board_pads_with_refs (the shared helper) ----------


def test_iter_board_pads_with_refs_pairs_each_pad_with_footprint_ref(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The helper that all 3 pcb.py call sites use must produce (pad, ref) pairs.

    Regression target: the original implementations called
    ``pad.parent.reference_field.text.value``; this test's fake Pads have
    no ``parent`` attribute, so any regression triggers ``AttributeError``.
    """
    from kicad_mcp.tools.pcb import _iter_board_pads_with_refs

    fps = [
        _make_footprint("J1", [_make_pad("1"), _make_pad("2")]),
        _make_footprint("D1", [_make_pad("1")]),
    ]
    _patch_board_pcb(monkeypatch, fps)

    pairs = _iter_board_pads_with_refs()

    assert len(pairs) == 3
    refs = {ref for _, ref in pairs}
    assert refs == {"J1", "D1"}
    # Critically: no pair's pad has a `parent` attribute.
    assert all(not hasattr(pad, "parent") for pad, _ in pairs)


def test_iter_board_pads_handles_empty_board(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty board ⇒ empty list, no exceptions."""
    from kicad_mcp.tools.pcb import _iter_board_pads_with_refs

    _patch_board_pcb(monkeypatch, [])
    assert _iter_board_pads_with_refs() == []


def test_iter_board_pads_handles_footprint_without_definition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Footprints lacking ``definition`` are skipped (older kipy / fakes)."""
    from kicad_mcp.tools.pcb import _iter_board_pads_with_refs

    legit = _make_footprint("J1", [_make_pad("1")])
    no_def = SimpleNamespace(
        reference_field=SimpleNamespace(text=SimpleNamespace(value="GHOST")),
    )  # no `definition`
    _patch_board_pcb(monkeypatch, [legit, no_def])

    pairs = _iter_board_pads_with_refs()
    refs = {ref for _, ref in pairs}
    assert refs == {"J1"}  # GHOST silently skipped, J1 still surfaces


def test_iter_board_pads_handles_footprint_with_empty_pads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Footprints with empty ``definition.pads`` contribute nothing, no errors."""
    from kicad_mcp.tools.pcb import _iter_board_pads_with_refs

    fps = [
        _make_footprint("EMPTY", []),
        _make_footprint("J1", [_make_pad("1")]),
    ]
    _patch_board_pcb(monkeypatch, fps)

    pairs = _iter_board_pads_with_refs()
    assert [ref for _, ref in pairs] == ["J1"]


# ---------- signal_integrity._find_power_anchor ----------


def test_find_power_anchor_walks_footprints_without_pad_parent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """_find_power_anchor must locate the IC's power pin via footprint walk.

    Regression: original used ``_footprint_reference(pad.parent)`` which
    raises AttributeError on real kipy Pad objects.
    """
    from kicad_mcp.tools import signal_integrity as si

    fps = [
        _make_footprint("U7", [
            _make_pad("1", x_nm=4_000_000, y_nm=8_000_000, net_name="VCC"),
            _make_pad("2", x_nm=4_080_000, y_nm=8_000_000, net_name="GND"),
        ]),
        _make_footprint("C5", [
            _make_pad("1", x_nm=10_000_000, y_nm=10_000_000, net_name="VCC"),
        ]),
    ]
    monkeypatch.setattr(si, "_board_footprints", lambda: fps)

    x_mm, y_mm = si._find_power_anchor("U7", "1")
    assert x_mm == pytest.approx(4.0)
    assert y_mm == pytest.approx(8.0)


def test_find_power_anchor_falls_back_to_footprint_centroid_when_pin_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When the named pin doesn't exist on the IC, return the footprint position."""
    from kicad_mcp.tools import signal_integrity as si

    fp = SimpleNamespace(
        reference_field=SimpleNamespace(text=SimpleNamespace(value="U99")),
        definition=SimpleNamespace(pads=[_make_pad("1")]),
        position=SimpleNamespace(x_nm=12_000_000, y_nm=15_000_000),
    )
    monkeypatch.setattr(si, "_board_footprints", lambda: [fp])

    x_mm, y_mm = si._find_power_anchor("U99", "999")  # pin doesn't exist
    assert x_mm == pytest.approx(12.0)
    assert y_mm == pytest.approx(15.0)


def test_find_power_anchor_raises_when_footprint_missing_entirely(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If the refdes isn't on the board at all, the helper raises ValueError."""
    from kicad_mcp.tools import signal_integrity as si

    monkeypatch.setattr(si, "_board_footprints", lambda: [])
    with pytest.raises(ValueError, match="was not found"):
        si._find_power_anchor("UMissing", "1")


def test_find_power_anchor_handles_int_pad_numbers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Some footprints (e.g. 26-pin Amphenol) expose pad numbers as int."""
    from kicad_mcp.tools import signal_integrity as si

    fps = [
        _make_footprint(
            "J_M1",
            [_make_pad(7, x_nm=20_000_000, y_nm=5_000_000, net_name="VCC")],
        ),
    ]
    monkeypatch.setattr(si, "_board_footprints", lambda: fps)

    x_mm, y_mm = si._find_power_anchor("J_M1", "7")
    assert x_mm == pytest.approx(20.0)
    assert y_mm == pytest.approx(5.0)


# ---------- _PadLike Protocol ----------


def test_padlike_protocol_does_not_declare_parent() -> None:
    """The _PadLike Protocol must not advertise a ``parent`` attribute.

    The ``parent`` declaration was a lie about kipy's actual API and led
    every consumer to write the buggy access pattern. Removing it forces
    Pyright to flag any future regressions.
    """
    from kicad_mcp.models.common import _PadLike

    assert "parent" not in _PadLike.__annotations__, (
        "_PadLike must not declare 'parent' — kipy's Pad has no such attr. "
        "Walk board.get_footprints() and inspect fp.definition.pads instead."
    )
