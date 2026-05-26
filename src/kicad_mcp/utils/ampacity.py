"""IPC-2221 trace ampacity helpers.

Pure-math utilities for sizing PCB traces and fuses against expected
current loads. No KiCad IPC dependency — safe to call from headless
tools that only read a ``.kicad_pcb`` file from disk.

Formula (IPC-2221 §6.2):

    I = k * (ΔT)^0.44 * (A)^0.725

where:
    I = max continuous current in amps
    ΔT = allowed temperature rise above ambient in °C
    A = cross-sectional area in mil²
    k = 0.048 for external (outer-layer) traces
    k = 0.024 for internal (inner-layer) traces
"""

from __future__ import annotations

from .impedance import copper_thickness_mm
from .units import mm_to_mil

_EXTERNAL_K = 0.048
_INTERNAL_K = 0.024

# Standard automotive blade-fuse ratings. Used for `recommended_fuse_rating_a`
# to round down to the next-lower stocked size. Larger values can be added
# later if needed.
STANDARD_FUSE_RATINGS_A: tuple[float, ...] = (
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


def ipc2221_current_capacity_a(
    width_mm: float,
    copper_thickness_mm_value: float,
    *,
    external: bool,
    max_temp_rise_c: float,
) -> float:
    """IPC-2221 max-continuous-current for a PCB trace.

    ``width_mm`` is the conductor width. ``copper_thickness_mm_value`` is the
    finished-copper thickness (e.g. ``copper_thickness_mm(1.0)`` for 1 oz).
    ``external`` selects between outer-layer and inner-layer k constants.
    ``max_temp_rise_c`` is the allowed copper-vs-ambient ΔT in °C.
    """
    if width_mm <= 0 or copper_thickness_mm_value <= 0 or max_temp_rise_c <= 0:
        return 0.0
    area_mil_sq = mm_to_mil(width_mm) * mm_to_mil(copper_thickness_mm_value)
    k = _EXTERNAL_K if external else _INTERNAL_K
    return float(k * (max_temp_rise_c**0.44) * (area_mil_sq**0.725))


def ipc2221_required_width_mm(
    expected_current_a: float,
    copper_thickness_mm_value: float,
    *,
    external: bool,
    max_temp_rise_c: float,
) -> float:
    """Inverse of :func:`ipc2221_current_capacity_a` — return width needed
    to carry ``expected_current_a`` at the given ΔT."""
    if expected_current_a <= 0 or copper_thickness_mm_value <= 0 or max_temp_rise_c <= 0:
        return 0.0
    k = _EXTERNAL_K if external else _INTERNAL_K
    area_mil_sq = (expected_current_a / (k * (max_temp_rise_c**0.44))) ** (1.0 / 0.725)
    return float(area_mil_sq / mm_to_mil(copper_thickness_mm_value) * 0.0254)


def recommended_fuse_rating_a(
    trace_capacity_a: float,
    *,
    safety_factor: float = 0.7,
) -> float:
    """Round trace capacity × safety factor down to the next-lower stocked
    blade-fuse rating.

    ``safety_factor`` is the fraction of trace capacity the fuse must blow
    below. 0.7 is the rule of thumb for automotive harnesses — a 10 A trace
    paired with a 7 A fuse.

    Returns ``0.0`` if no standard rating fits (trace too narrow for any
    common fuse).
    """
    target = trace_capacity_a * safety_factor
    eligible = [rating for rating in STANDARD_FUSE_RATINGS_A if rating <= target]
    if not eligible:
        return 0.0
    return float(max(eligible))


def copper_oz_to_thickness_mm(copper_oz: float) -> float:
    """Convenience re-export so callers don't have to reach into ``impedance``."""
    return copper_thickness_mm(copper_oz)


__all__ = [
    "STANDARD_FUSE_RATINGS_A",
    "copper_oz_to_thickness_mm",
    "ipc2221_current_capacity_a",
    "ipc2221_required_width_mm",
    "recommended_fuse_rating_a",
]
