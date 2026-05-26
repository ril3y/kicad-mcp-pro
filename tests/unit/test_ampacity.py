# pyright: reportPrivateUsage=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingParameterType=false
# ruff: noqa: ANN001, ANN201
"""Unit tests for the IPC-2221 ampacity math helpers.

These pin numerical values against IPC-2221's reference formula at fixed
inputs so a refactor of the constants or rounding cannot silently shift
the recommended fuse sizes downstream tools emit.
"""

from __future__ import annotations

import pytest

from kicad_mcp.utils.ampacity import (
    STANDARD_FUSE_RATINGS_A,
    copper_oz_to_thickness_mm,
    ipc2221_current_capacity_a,
    ipc2221_required_width_mm,
    recommended_fuse_rating_a,
)


def test_external_capacity_matches_reference_value():
    """1 mm wide, 1 oz copper, external, ΔT 20°C ≈ 3.23 A per IPC-2221
    using our 0.034798 mm/oz copper-thickness constant.

    Pinning the exact value protects against silent regressions: if either
    the k constant (0.048) or the copper-thickness constant moves, fuse
    recommendations across the codebase shift.
    """
    capacity = ipc2221_current_capacity_a(
        1.0,
        copper_oz_to_thickness_mm(1.0),
        external=True,
        max_temp_rise_c=20.0,
    )
    assert capacity == pytest.approx(3.23, abs=0.02)


def test_internal_is_half_external_k_so_lower_capacity():
    """Internal-layer k (0.024) is half external k (0.048), so for identical
    geometry the internal capacity is half the external capacity."""
    args = dict(
        width_mm=1.0,
        copper_thickness_mm_value=copper_oz_to_thickness_mm(1.0),
        max_temp_rise_c=20.0,
    )
    external = ipc2221_current_capacity_a(**args, external=True)
    internal = ipc2221_current_capacity_a(**args, external=False)
    assert internal == pytest.approx(external / 2.0, rel=1e-9)


def test_zero_or_negative_inputs_return_zero():
    """Width / thickness / ΔT must all be positive; otherwise the formula
    has no physical meaning. Guard against div-by-zero in calling code by
    returning 0.0 explicitly."""
    cu = copper_oz_to_thickness_mm(1.0)
    assert ipc2221_current_capacity_a(0.0, cu, external=True, max_temp_rise_c=20.0) == 0.0
    assert ipc2221_current_capacity_a(1.0, 0.0, external=True, max_temp_rise_c=20.0) == 0.0
    assert ipc2221_current_capacity_a(1.0, cu, external=True, max_temp_rise_c=0.0) == 0.0
    assert ipc2221_current_capacity_a(-0.1, cu, external=True, max_temp_rise_c=20.0) == 0.0


def test_required_width_inverts_capacity():
    """Solving for the width that exactly carries ``capacity_a`` should
    return the original width within rounding tolerance."""
    cu = copper_oz_to_thickness_mm(1.0)
    width = 0.75
    capacity = ipc2221_current_capacity_a(width, cu, external=True, max_temp_rise_c=20.0)
    recovered = ipc2221_required_width_mm(capacity, cu, external=True, max_temp_rise_c=20.0)
    assert recovered == pytest.approx(width, rel=1e-6)


def test_required_width_zero_for_invalid_inputs():
    """``ipc2221_required_width_mm`` must return 0.0 (not NaN / negative)
    when handed nonsense inputs — callers compare against the routed width
    and need a stable sentinel."""
    cu = copper_oz_to_thickness_mm(1.0)
    assert ipc2221_required_width_mm(0.0, cu, external=True, max_temp_rise_c=20.0) == 0.0
    assert ipc2221_required_width_mm(1.0, 0.0, external=True, max_temp_rise_c=20.0) == 0.0
    assert ipc2221_required_width_mm(1.0, cu, external=True, max_temp_rise_c=0.0) == 0.0


def test_recommended_fuse_rounds_down_to_standard_size():
    """A 3.23 A trace × 0.7 safety → 2.26 A target → rounds down to 2 A.
    Pinning the boundary value matters because moving the safety factor
    or the standard fuse-rating list could land on 1 A instead."""
    assert recommended_fuse_rating_a(3.23) == pytest.approx(2.0)


def test_recommended_fuse_returns_zero_when_trace_too_narrow():
    """A 0.5 A trace × 0.7 = 0.35 A — below the smallest stocked rating
    (0.5 A) — so no fuse is recommended."""
    assert recommended_fuse_rating_a(0.5) == 0.0


def test_recommended_fuse_honors_safety_factor():
    """Override the safety factor — 100% means fuse = trace capacity rounded
    down. For a 10 A trace that's the 10 A blade fuse."""
    assert recommended_fuse_rating_a(10.0, safety_factor=1.0) == pytest.approx(10.0)


def test_standard_fuse_ratings_are_monotonic_and_documented():
    """Pin the published fuse-rating list — changing this list is a
    user-visible change to fuse recommendations and must be intentional."""
    assert STANDARD_FUSE_RATINGS_A == (
        0.5,
        1.0,
        2.0,
        3.0,
        5.0,
        7.5,
        10.0,
        15.0,
        20.0,
        25.0,
        30.0,
    )
    # And sorted ascending — `recommended_fuse_rating_a` depends on max()
    # picking the largest qualifying rating.
    assert list(STANDARD_FUSE_RATINGS_A) == sorted(STANDARD_FUSE_RATINGS_A)


def test_copper_oz_to_thickness_mm_matches_classic_constant():
    """1 oz copper ≈ 34.8 μm finished thickness — pin the value so any
    refactor of the underlying util keeps this contract."""
    assert copper_oz_to_thickness_mm(1.0) == pytest.approx(0.034798, abs=1e-6)
    assert copper_oz_to_thickness_mm(2.0) == pytest.approx(0.069596, abs=1e-6)
