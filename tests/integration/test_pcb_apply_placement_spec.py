"""Integration tests for ``pcb_apply_placement_spec`` (PR #13).

Thin spec-driven placement tool that batches N footprint moves into a
single IPC transaction. Same Angle-wrapping semantics as
``pcb_move_footprint`` (PR #2 fix), single response listing successes
+ skipped missing references, persistence hint suffix per PR #11
convention.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from kicad_mcp.server import build_server
from tests.conftest import call_tool_text


class _OrientationFootprint:
    """Fake footprint mirroring kipy's contract: orientation setter calls
    .normalize180() on its argument (must be an Angle, not raw float)."""

    def __init__(self, ref: str) -> None:
        self.reference_field = SimpleNamespace(text=SimpleNamespace(value=ref))
        self.position = None
        self._orientation = None

    @property
    def orientation(self):  # type: ignore[no-untyped-def]
        return self._orientation

    @orientation.setter
    def orientation(self, value) -> None:  # type: ignore[no-untyped-def]
        value.normalize180()
        self._orientation = value


@pytest.mark.anyio
async def test_apply_placement_spec_moves_each_footprint_in_order(
    mock_board,
) -> None:
    """Happy path: 3 placements, all references found, all applied."""
    j1 = _OrientationFootprint("J1")
    d1 = _OrientationFootprint("D1")
    h1 = _OrientationFootprint("H1")
    mock_board.get_footprints.return_value = [j1, d1, h1]
    server = build_server("pcb")

    result = await call_tool_text(
        server,
        "pcb_apply_placement_spec",
        {
            "placements": [
                {"reference": "J1", "x_mm": 5.0, "y_mm": 25.0, "rotation_deg": 90.0},
                {"reference": "D1", "x_mm": 18.0, "y_mm": 5.0, "rotation_deg": 0.0},
                {"reference": "H1", "x_mm": 75.0, "y_mm": 25.0, "rotation_deg": 0.0},
            ],
        },
    )

    assert "Applied 3 placement(s) in one transaction." in result
    assert "J1 → (5.0, 25.0) rot=90.0" in result
    assert "D1 → (18.0, 5.0) rot=0.0" in result
    assert "H1 → (75.0, 25.0) rot=0.0" in result
    # Persistence hint per PR #11 convention.
    assert "Call pcb_save() to persist" in result
    # Rotation actually applied via the Angle wrapper (PR #2 fix).
    assert j1.orientation is not None
    assert j1.orientation.degrees == pytest.approx(90.0)
    # Single IPC transaction — one update_items call regardless of N.
    mock_board.update_items.assert_called_once()


@pytest.mark.anyio
async def test_apply_placement_spec_reports_missing_references_without_aborting(
    mock_board,
) -> None:
    """Typo'd ref ``GHOST`` doesn't exist on the board — the other 2
    placements still apply. Partial application is correct: a stray typo
    shouldn't undo work that succeeded."""
    j1 = _OrientationFootprint("J1")
    d1 = _OrientationFootprint("D1")
    mock_board.get_footprints.return_value = [j1, d1]
    server = build_server("pcb")

    result = await call_tool_text(
        server,
        "pcb_apply_placement_spec",
        {
            "placements": [
                {"reference": "J1", "x_mm": 5.0, "y_mm": 25.0},
                {"reference": "GHOST", "x_mm": 50.0, "y_mm": 50.0},
                {"reference": "D1", "x_mm": 18.0, "y_mm": 5.0},
            ],
        },
    )

    assert "Applied 2 placement(s)" in result
    assert "Skipped 1 missing reference(s): GHOST" in result
    # The two real footprints DID get placed (single IPC call covers both).
    mock_board.update_items.assert_called_once()


@pytest.mark.anyio
async def test_apply_placement_spec_all_missing_skips_update_items(
    mock_board,
) -> None:
    """If every reference is missing, the tool reports the skip list and
    does NOT issue a no-op ``update_items`` call."""
    mock_board.get_footprints.return_value = []
    server = build_server("pcb")

    result = await call_tool_text(
        server,
        "pcb_apply_placement_spec",
        {
            "placements": [
                {"reference": "GHOST_A", "x_mm": 0.0, "y_mm": 0.0},
                {"reference": "GHOST_B", "x_mm": 1.0, "y_mm": 1.0},
            ],
        },
    )

    assert "Applied 0 placement(s)" in result
    assert "Skipped 2 missing reference(s): GHOST_A, GHOST_B" in result
    mock_board.update_items.assert_not_called()


@pytest.mark.anyio
async def test_apply_placement_spec_empty_list_rejected_by_pydantic(
    mock_board,
) -> None:
    """``placements: list[...] = Field(min_length=1)`` — an empty list is a
    user error and Pydantic rejects it before the tool body runs."""
    mock_board.get_footprints.return_value = []
    server = build_server("pcb")

    result = await call_tool_text(
        server,
        "pcb_apply_placement_spec",
        {"placements": []},
    )

    # Surfaces as TOOL_EXECUTION_FAILED because Pydantic raises ValidationError.
    assert "TOOL_EXECUTION_FAILED" in result or "validation" in result.lower()
    mock_board.update_items.assert_not_called()


@pytest.mark.anyio
async def test_apply_placement_spec_default_rotation_is_zero(
    mock_board,
) -> None:
    """``rotation_deg`` defaults to 0.0 when omitted — same default as
    ``pcb_move_footprint`` for callers that only care about position."""
    j1 = _OrientationFootprint("J1")
    mock_board.get_footprints.return_value = [j1]
    server = build_server("pcb")

    await call_tool_text(
        server,
        "pcb_apply_placement_spec",
        {"placements": [{"reference": "J1", "x_mm": 10.0, "y_mm": 20.0}]},
    )

    assert j1.orientation is not None
    assert j1.orientation.degrees == pytest.approx(0.0)
