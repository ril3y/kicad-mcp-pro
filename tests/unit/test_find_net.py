"""Regression tests for ``kicad_mcp.tools.pcb._find_net``.

Pre-PR the helper constructed a bare ``Net()`` carrying only the requested
name — no proto code, no real linkage. Callers assigning the result to
``track.net`` / ``via.net`` / ``zone.net`` ended up with a ghost net that
didn't match any net on the board, producing silent net-mis-assignment
or stray auto-allocated nets visible later in DRC.

These tests pin the new contract: walk ``board.get_nets()`` and return
the live ``Net``; raise ``ValueError`` on a typo'd name so the failure
surfaces immediately.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest


def _patch_board(monkeypatch: pytest.MonkeyPatch, nets: list[SimpleNamespace]) -> None:
    fake_board = SimpleNamespace(get_nets=lambda: nets)
    monkeypatch.setattr("kicad_mcp.tools.pcb.get_board", lambda: fake_board)


def test_find_net_returns_the_live_board_net(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The helper must return the matching object from ``board.get_nets()``.

    Returning *that* object preserves any proto state the live net carries
    (codes, classes, flags) so downstream assignments to ``track.net`` etc.
    bind to the real net rather than a synthetic stand-in.
    """
    from kicad_mcp.tools.pcb import _find_net

    target = SimpleNamespace(name="GND_RTN", proto="<live-proto>")
    nets = [
        SimpleNamespace(name="VCC", proto="<other-proto>"),
        target,
        SimpleNamespace(name="USB_DP", proto="<another-proto>"),
    ]
    _patch_board(monkeypatch, nets)

    result = _find_net("GND_RTN")
    # MUST be the same object — not a synthetic with only the name copied.
    assert result is target
    assert result.proto == "<live-proto>"


def test_find_net_raises_when_name_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A typo'd or non-existent net must raise ``ValueError`` instead of
    silently returning a ghost net.

    Pre-fix the helper would return ``Net(name='TYPO_NET')`` and the bug
    would leak into ``track.net = ghost`` / ``zone.net = ghost`` paths,
    where it produced stray auto-nets that later confused DRC.
    """
    from kicad_mcp.tools.pcb import _find_net

    _patch_board(monkeypatch, [SimpleNamespace(name="VCC")])

    with pytest.raises(ValueError, match="was not found"):
        _find_net("TYPO_NET")


def test_find_net_raises_with_helpful_hint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Error message must point users at ``pcb_get_nets()`` for discovery."""
    from kicad_mcp.tools.pcb import _find_net

    _patch_board(monkeypatch, [SimpleNamespace(name="VCC")])

    with pytest.raises(ValueError, match="pcb_get_nets"):
        _find_net("DOESNT_EXIST")


def test_find_net_handles_empty_board(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty net list must raise, not silently fabricate."""
    from kicad_mcp.tools.pcb import _find_net

    _patch_board(monkeypatch, [])

    with pytest.raises(ValueError, match="was not found"):
        _find_net("ANY_NET")


def test_find_net_first_match_wins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If duplicate-named nets exist (rare but legal in certain edge cases),
    the helper returns the first encountered match — same convention as
    sibling ``_find_footprint_by_reference``."""
    from kicad_mcp.tools.pcb import _find_net

    first = SimpleNamespace(name="DUPE", tag="first")
    second = SimpleNamespace(name="DUPE", tag="second")
    _patch_board(monkeypatch, [first, second])

    assert _find_net("DUPE") is first


@pytest.mark.parametrize(
    "name",
    [
        # KiCad auto-allocates these for unconnected pins; they routinely
        # contain parens, slashes, and dashes. The lookup must not choke.
        "unconnected-(D6-I{slash}O2-Pad3)",
        "unconnected-(U1-Pad7)",
        "Net-(R1-Pad1)",
        # Schematic-prefixed names use leading slash.
        "/GND_RTN",
        "/USB+",
        # Case sensitivity: KiCad nets ARE case-sensitive.
        "VCC",
        "vcc",
    ],
)
def test_find_net_handles_realistic_net_names(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
) -> None:
    """Lookup must work for KiCad's real net-name shapes, not just bare alnum."""
    from kicad_mcp.tools.pcb import _find_net

    target = SimpleNamespace(name=name)
    _patch_board(monkeypatch, [SimpleNamespace(name="DECOY"), target])

    assert _find_net(name) is target


def test_find_net_is_case_sensitive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """KiCad treats VCC and vcc as distinct nets — pin that contract."""
    from kicad_mcp.tools.pcb import _find_net

    _patch_board(monkeypatch, [SimpleNamespace(name="VCC")])

    with pytest.raises(ValueError, match="was not found"):
        _find_net("vcc")
