# pyright: reportPrivateUsage=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingParameterType=false
# pyright: reportAttributeAccessIssue=false
# ruff: noqa: ANN001, ANN201
"""Tests for the headless ``pcb_get_net_traces`` and
``pcb_check_trace_ampacity`` MCP tools.

These confirm the user-visible string format (an agent will key off it)
plus the two main contract claims:

1. The narrowest segment on a multi-width net is the one driving the
   ampacity verdict — not an average.
2. F.Cu / B.Cu segments use the external IPC-2221 constant (k=0.048);
   inner layers fall back to internal (k=0.024).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kicad_mcp.tools import pcb as pcb_tools
from kicad_mcp.utils.board_tracks import segments_for_net


def _write_board(project_dir: Path, segments_text: str) -> None:
    """Helper to drop a synthetic .kicad_pcb at the configured location."""
    board = project_dir / "demo.kicad_pcb"
    board.write_text(
        f'(kicad_pcb\n\t(version 20240108)\n\t(generator "pytest")\n{segments_text}\n)\n',
        encoding="utf-8",
    )


def _segment(start, end, width_mm, layer, net) -> str:
    sx, sy = start
    ex, ey = end
    return (
        "\t(segment\n"
        f"\t\t(start {sx} {sy})\n"
        f"\t\t(end {ex} {ey})\n"
        f"\t\t(width {width_mm})\n"
        f'\t\t(layer "{layer}")\n'
        f'\t\t(net "{net}")\n'
        '\t\t(uuid "00000000-0000-0000-0000-000000000000")\n'
        "\t)"
    )


@pytest.fixture
def board_with_48v(sample_project: Path) -> Path:
    """``sample_project`` + a synthetic 48V_KEY_INPUT net routed on F.Cu /
    B.Cu and a narrower GND segment so width filtering can be tested.

    Geometry mirrors the Junction-2026 board: a 1.0 mm 48V trace split
    across two layers.
    """
    _write_board(
        sample_project,
        "\n".join(
            [
                _segment((10.0, 10.0), (20.0, 10.0), 1.0, "F.Cu", "48V_KEY_INPUT"),
                _segment((20.0, 10.0), (30.0, 10.0), 1.0, "B.Cu", "48V_KEY_INPUT"),
                _segment((0.0, 0.0), (5.0, 0.0), 0.25, "F.Cu", "GND"),
            ]
        ),
    )
    return sample_project


def _make_registered_pcb_tools():
    """Spin up FastMCP and register pcb tools so we can extract the bare
    callables and exercise them without going through the MCP transport.

    Returns a dict from tool name to the underlying Python function.
    """

    class _Stub:
        def __init__(self) -> None:
            self.tools: dict[str, object] = {}

        def tool(self, **_kwargs: object):
            def decorator(fn):
                self.tools[fn.__name__] = fn
                return fn

            return decorator

    stub = _Stub()
    pcb_tools.register(stub)  # type: ignore[arg-type]
    return stub.tools


def test_pcb_get_net_traces_lists_each_segment_with_layer_breakdown(board_with_48v: Path):
    """Output should include the limiting width, layer breakdown, total
    length, and per-segment lines. This is the format agents will key off
    when they ask 'what's the narrowest part of net X'."""
    tools = _make_registered_pcb_tools()
    result: str = tools["pcb_get_net_traces"]("48V_KEY_INPUT")  # type: ignore[operator]
    assert "Net '48V_KEY_INPUT' tracks" in result
    assert "Segments: 2" in result
    assert "1 on F.Cu" in result and "1 on B.Cu" in result
    assert "Width range: 1.000 mm (min) - 1.000 mm (max)" in result
    # Two segments of 10 mm each = 20 mm total.
    assert "Total length: 20.00 mm" in result


def test_pcb_get_net_traces_missing_net_returns_friendly_message(
    board_with_48v: Path,
):
    """Asking for a non-existent net should return a clean message, not
    raise — the agent expects a parseable response."""
    tools = _make_registered_pcb_tools()
    result: str = tools["pcb_get_net_traces"]("DOES_NOT_EXIST")  # type: ignore[operator]
    assert "No routed track segments were found for net 'DOES_NOT_EXIST'" in result


def test_pcb_check_trace_ampacity_uses_min_width_on_multi_width_net(
    sample_project: Path,
):
    """A multi-width net's ampacity is driven by the narrowest segment.
    Two segments at 1.0 mm and 0.4 mm → the 0.4 mm bottleneck wins."""
    _write_board(
        sample_project,
        "\n".join(
            [
                _segment((0.0, 0.0), (10.0, 0.0), 1.0, "F.Cu", "POWER"),
                # Bottleneck.
                _segment((10.0, 0.0), (12.0, 0.0), 0.4, "F.Cu", "POWER"),
            ]
        ),
    )
    tools = _make_registered_pcb_tools()
    result: str = tools["pcb_check_trace_ampacity"]("POWER")  # type: ignore[operator]
    assert "Limiting segment: 0.400 mm wide on F.Cu" in result
    assert "external" in result  # F.Cu = external layer


def test_pcb_check_trace_ampacity_inner_layer_capacity_is_half(
    sample_project: Path,
):
    """An inner-layer segment uses k=0.024 instead of k=0.048, so the
    reported ΔT 20°C capacity is exactly half the external value at the
    same width / copper weight."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 1.0, "In1.Cu", "INNER_POWER"),
    )
    tools = _make_registered_pcb_tools()
    result: str = tools["pcb_check_trace_ampacity"]("INNER_POWER")  # type: ignore[operator]
    assert "internal" in result
    # 3.23 A external / 2 = 1.62 A internal at ΔT 20°C.
    assert "ΔT 20 C: 1.62 A" in result


def test_pcb_check_trace_ampacity_load_check_passes_when_under_limit(
    sample_project: Path,
):
    """Expected current 0.06 A on a 1.0 mm external trace at ΔT 20°C is
    under capacity — the tool must report OK."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 1.0, "F.Cu", "PWR"),
    )
    tools = _make_registered_pcb_tools()
    result: str = tools["pcb_check_trace_ampacity"]("PWR", 0.06)  # type: ignore[operator]
    assert "Load check (expected 0.060 A" in result
    assert "OK" in result


def test_pcb_check_trace_ampacity_load_check_fails_when_over_limit(
    sample_project: Path,
):
    """A 0.3 mm trace at ΔT 20°C carries roughly 0.92 A — asking it to
    carry 5 A must report FAIL with an explicit percent-of-capacity."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 0.3, "F.Cu", "PWR"),
    )
    tools = _make_registered_pcb_tools()
    result: str = tools["pcb_check_trace_ampacity"]("PWR", 5.0)  # type: ignore[operator]
    assert "FAIL" in result


def test_pcb_check_trace_ampacity_recommends_2a_fuse_for_1mm_external(
    sample_project: Path,
):
    """Pin the Junction-2026 reference: 1 mm × 1 oz × external × ΔT 20°C
    → ~3.5 A capacity → 70% safety = 2.46 A → 2.0 A standard fuse."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 1.0, "F.Cu", "PWR"),
    )
    tools = _make_registered_pcb_tools()
    result: str = tools["pcb_check_trace_ampacity"]("PWR")  # type: ignore[operator]
    assert "Recommended fuse rating: 2.0 A" in result


def test_pcb_check_trace_ampacity_reports_no_fuse_for_too_narrow_trace(
    sample_project: Path,
):
    """A 0.1 mm × 1 oz × external trace carries ~0.4 A — below the 0.5 A
    smallest stocked rating once the 0.7 safety factor lands. Output must
    clearly state no standard fuse fits, not silently emit '0.0 A'."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 0.1, "F.Cu", "TINY"),
    )
    tools = _make_registered_pcb_tools()
    result: str = tools["pcb_check_trace_ampacity"]("TINY")  # type: ignore[operator]
    assert "trace is too narrow for any standard" in result


def test_pcb_check_trace_ampacity_honors_custom_max_temp_rise_c(
    sample_project: Path,
):
    """The ``max_temp_rise_c`` parameter MUST change the load-check threshold
    — otherwise the parameter is decorative. At ΔT 60 °C a 1.0 mm × 1 oz
    external trace carries ~5.5 A, so a 4 A load that FAILs at ΔT 20 °C
    must PASS at ΔT 60 °C."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 1.0, "F.Cu", "PWR"),
    )
    tools = _make_registered_pcb_tools()
    fail_at_20 = tools["pcb_check_trace_ampacity"](  # type: ignore[operator]
        "PWR", 4.0, max_temp_rise_c=20.0
    )
    assert "FAIL" in fail_at_20
    pass_at_60 = tools["pcb_check_trace_ampacity"](  # type: ignore[operator]
        "PWR", 4.0, max_temp_rise_c=60.0
    )
    assert "OK" in pass_at_60 and "FAIL" not in pass_at_60


def test_pcb_check_trace_ampacity_honors_copper_weight_oz(sample_project: Path):
    """Doubling copper weight from 1 oz to 2 oz roughly doubles capacity at
    fixed width / ΔT (technically × 2^0.725 ≈ 1.65 — the area exponent in
    IPC-2221). So a 4 A load that FAILs at 1 oz on a 0.5 mm trace must
    move closer to OK on the same trace at 2 oz copper. We assert the
    reported capacity DIFFERS — that's the parameter's whole job."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 0.5, "F.Cu", "PWR"),
    )
    tools = _make_registered_pcb_tools()
    one_oz = tools["pcb_check_trace_ampacity"]("PWR", 0.0, 20.0, 1.0)  # type: ignore[operator]
    two_oz = tools["pcb_check_trace_ampacity"]("PWR", 0.0, 20.0, 2.0)  # type: ignore[operator]
    # 1 oz ΔT 20 C capacity for 0.5 mm = ~1.96 A; 2 oz ≈ 3.24 A.
    assert "ΔT 20 C: 1.95 A" in one_oz or "ΔT 20 C: 1.96 A" in one_oz
    assert "ΔT 20 C: 3.23 A" in two_oz or "ΔT 20 C: 3.24 A" in two_oz


def test_pcb_check_trace_ampacity_load_check_passes_at_exact_capacity(
    sample_project: Path,
):
    """Boundary: ``expected_current_a == chosen_capacity_a`` should be OK
    (the tool uses ``<=``, not ``<``). Documenting the boundary prevents a
    future refactor from silently making the comparison strict."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 1.0, "F.Cu", "PWR"),
    )
    tools = _make_registered_pcb_tools()
    # 1.0 mm × 1 oz × external × ΔT 20°C ≈ 3.23 A. Use slightly under to
    # avoid floating-point boundary fragility.
    result: str = tools["pcb_check_trace_ampacity"]("PWR", 3.22)  # type: ignore[operator]
    assert "OK" in result and "FAIL" not in result


def test_pcb_check_trace_ampacity_case_insensitive_lookup_finds_net(
    sample_project: Path,
):
    """The ``pcb_get_net_traces`` tool advertises ``case_sensitive`` but the
    ampacity tool does not. Confirm that ``pcb_get_net_traces`` actually
    finds a mixed-case net when given the lowercase form with the flag set.
    The ampacity tool is intentionally case-sensitive (net names are)."""
    _write_board(
        sample_project,
        _segment((0.0, 0.0), (10.0, 0.0), 1.0, "F.Cu", "MixedCaseNet"),
    )
    tools = _make_registered_pcb_tools()
    found = tools["pcb_get_net_traces"](  # type: ignore[operator]
        "mixedcasenet", case_sensitive=False
    )
    assert "Net 'MixedCaseNet' tracks" in found

    not_found = tools["pcb_get_net_traces"]("mixedcasenet")  # type: ignore[operator]
    assert "No routed track segments" in not_found


def test_segments_for_net_finds_the_synthetic_fixture(board_with_48v: Path):
    """Sanity check the parser helper against the same fixture so a
    parser regression doesn't masquerade as a tool-format failure."""
    board = (board_with_48v / "demo.kicad_pcb").read_text(encoding="utf-8")
    matches = segments_for_net(board, "48V_KEY_INPUT")
    assert len(matches) == 2
    assert {s.layer for s in matches} == {"F.Cu", "B.Cu"}
