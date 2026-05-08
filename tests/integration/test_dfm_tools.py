from __future__ import annotations

from types import SimpleNamespace

import pytest
from kipy.proto.board.board_types_pb2 import BoardLayer

from kicad_mcp.server import build_server
from tests.conftest import call_tool_text


@pytest.mark.anyio
async def test_dfm_profile_load_run_and_cost(
    sample_project,
    mock_board,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_board.get_enabled_layers.return_value = [BoardLayer.BL_F_Cu, BoardLayer.BL_B_Cu]
    mock_board.get_tracks.return_value = [SimpleNamespace(width=200_000)]
    mock_board.get_vias.return_value = [SimpleNamespace(drill_diameter=300_000, diameter=600_000)]
    (sample_project / "demo.kicad_pcb").write_text(
        "\n".join(
            [
                "(kicad_pcb",
                "\t(version 20250216)",
                '\t(generator "pytest")',
                (
                    "\t(gr_rect (start 0 0) (end 50 40) "
                    "(stroke (width 0.05) (type solid)) "
                    '(fill no) (layer "Edge.Cuts"))'
                ),
                ")",
                "",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "kicad_mcp.tools.dfm._run_drc_report",
        lambda _report_name: (
            sample_project / "output" / "dfm_profile_check.json",
            {
                "violations": [],
                "unconnected_items": [],
                "items_not_passing_courtyard": [],
            },
            None,
        ),
    )
    server = build_server("manufacturing")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    loaded = await call_tool_text(
        server,
        "dfm_load_manufacturer_profile",
        {"manufacturer": "JLCPCB", "tier": "standard"},
    )
    report = await call_tool_text(server, "dfm_run_manufacturer_check", {})
    cost = await call_tool_text(
        server,
        "dfm_calculate_manufacturing_cost",
        {"quantity": 10, "manufacturer": "JLCPCB", "tier": "standard"},
    )

    assert "Active profile: JLCPCB / standard" in loaded
    assert "Profile: JLCPCB / standard" in report
    assert "PASS: Minimum track width 0.200 mm >= 0.127 mm" in report
    assert "PASS: Minimum via drill 0.300 mm >= 0.300 mm" in report
    assert "Manufacturing cost estimate:" in cost
    assert "Board size: 50.00 x 40.00 mm" in cost
    assert "Quantity: 10" in cost


@pytest.mark.anyio
async def test_legacy_dfm_validation_uses_profile_backend(
    sample_project,
    mock_board,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_board.get_enabled_layers.return_value = [BoardLayer.BL_F_Cu, BoardLayer.BL_B_Cu]
    mock_board.get_tracks.return_value = [SimpleNamespace(width=150_000)]
    mock_board.get_vias.return_value = [SimpleNamespace(drill_diameter=350_000, diameter=700_000)]
    monkeypatch.setattr(
        "kicad_mcp.tools.dfm._run_drc_report",
        lambda _report_name: (
            sample_project / "output" / "dfm_profile_check.json",
            {
                "violations": [{"severity": "warning", "description": "Silk overlap"}],
                "unconnected_items": [],
                "items_not_passing_courtyard": [],
            },
            None,
        ),
    )
    server = build_server("manufacturing")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    jlcpcb = await call_tool_text(server, "check_design_for_manufacture", {"jlcpcb": True})
    generic = await call_tool_text(server, "check_design_for_manufacture", {"jlcpcb": False})

    assert "DFM check (JLCPCB profile):" in jlcpcb
    assert "Profile: JLCPCB / standard" in jlcpcb
    assert "DFM check (generic profile):" in generic
    assert "Profile: PCBWay / standard" in generic


@pytest.mark.anyio
async def test_dfm_get_recommended_design_rules_uses_active_profile(
    sample_project,
) -> None:
    """The recommended-rules tool reads the active profile by default and
    emits a copy-paste-able ``pcb_set_design_rules(...)`` call so the LLM
    can apply manufacturer baselines without looking up schema."""
    server = build_server("dfm")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    await call_tool_text(
        server,
        "dfm_load_manufacturer_profile",
        {"manufacturer": "JLCPCB", "tier": "standard"},
    )
    result = await call_tool_text(server, "dfm_get_recommended_design_rules", {})

    # Profile baseline values (from jlcpcb_standard.json):
    #   min_trace_width_mm = 0.127, min_trace_clearance_mm = 0.127,
    #   min_drill_mm = 0.3, min_annular_ring_mm = 0.15
    # Derived:
    #   min_via_diameter_mm = 0.3 + 2*0.15 = 0.6
    #   min_hole_to_hole_mm = max(2*0.3, 0.25) = 0.6
    assert "Profile: JLCPCB / standard" in result
    assert "min_trace_width_mm: 0.127" in result
    assert "min_clearance_mm: 0.127" in result
    assert "min_via_drill_mm: 0.300" in result
    assert "min_via_diameter_mm: 0.600" in result
    assert "min_annular_ring_mm: 0.150" in result
    assert "min_hole_to_hole_mm: 0.600" in result
    # Apply-snippet contract: must contain a complete, copy-paste-able
    # kwarg block — full kwarg + closing paren — so a regression that
    # drops a kwarg or breaks formatting is caught.
    assert "pcb_set_design_rules(min_trace_width_mm=0.127" in result
    assert "min_hole_to_hole_mm=0.600)" in result


@pytest.mark.anyio
async def test_dfm_get_recommended_design_rules_explicit_profile(
    sample_project,
) -> None:
    """Passing manufacturer + tier overrides the active profile selection."""
    server = build_server("dfm")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "dfm_get_recommended_design_rules",
        {"manufacturer": "PCBWay", "tier": "standard"},
    )

    assert "Profile: PCBWay / standard" in result
    assert "pcb_set_design_rules(" in result


@pytest.mark.anyio
async def test_dfm_get_recommended_design_rules_rejects_rules_less_profile(
    sample_project,
) -> None:
    """``jlcpcb_rotations`` is an auxiliary BOM database, not a design-rule
    profile. Loading it then asking for recommended rules must surface a
    clear ValueError, not an unhandled KeyError on ``profile['rules']``."""
    server = build_server("dfm")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "dfm_get_recommended_design_rules",
        {"manufacturer": "jlcpcb", "tier": "rotations"},
    )

    assert "no 'rules' block" in result, (
        f"Expected friendly 'no rules block' guidance, got: {result!r}"
    )


def test_recommended_design_rules_clamps_hole_to_hole_for_tiny_drills() -> None:
    """The ``max(2*drill, 0.25)`` clamp must apply when the profile's drill
    is small enough that 2x falls below the 0.25 mm industry floor.

    None of the bundled profiles trigger this branch (smallest drill is 0.2),
    so we synthesize a profile inline to lock the clamp behavior. A
    regression that drops the clamp would silently emit
    ``min_hole_to_hole_mm = 0.20`` for a profile with drill=0.1.
    """
    from kicad_mcp.tools.dfm import _recommended_design_rules

    profile = {
        "manufacturer": "Test",
        "tier": "ultratiny",
        "rules": {
            "min_trace_width_mm": 0.05,
            "min_trace_clearance_mm": 0.05,
            "min_drill_mm": 0.1,  # 2x = 0.2, below the 0.25 floor
            "min_annular_ring_mm": 0.05,
        },
    }

    rules = _recommended_design_rules(profile)
    assert rules["min_hole_to_hole_mm"] == 0.25
    assert rules["min_via_drill_mm"] == 0.1
    assert rules["min_via_diameter_mm"] == pytest.approx(0.2)


@pytest.mark.anyio
async def test_dfm_get_recommended_design_rules_partial_args_rejected(
    sample_project,
) -> None:
    """Passing only one of manufacturer / tier is ambiguous — must raise.

    Asserts on the stable error-message substring (``Pass both``) rather
    than the harness-specific wrapping so the contract isn't tied to how
    FastMCP happens to surface ValueError today.
    """
    server = build_server("dfm")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "dfm_get_recommended_design_rules",
        {"manufacturer": "JLCPCB"},
    )

    assert "Pass both" in result, (
        f"Expected the 'Pass both' guidance in the partial-args error, got: {result!r}"
    )
