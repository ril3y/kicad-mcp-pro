"""Integration tests for ``pcb_apply_manufacturer_profile``.

The tool is a one-shot helper that lays down both the DRC floor and a set of
recommended net classes from a bundled manufacturer profile (JLCPCB, PCBWay,
OSH Park ...). It must compose cleanly with ``pcb_set_design_rules`` /
``route_set_net_class_rules`` because it deliberately reuses their internal
helpers — so a regression here typically points at a drift in the .kicad_dru
write helpers rather than at this tool itself.
"""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

import pytest

from kicad_mcp.server import build_server
from tests.conftest import call_tool_text

NET_CLASS_NAMES: tuple[str, ...] = ("Default", "Signal", "Power", "HighCurrent")
NET_CLASS_KEYS: tuple[str, ...] = (
    "width_mm",
    "clearance_mm",
    "via_diameter_mm",
    "via_drill_mm",
)
SHIPPED_PROFILES_WITH_NET_CLASSES: tuple[tuple[str, str], ...] = (
    ("jlcpcb", "standard"),
    ("jlcpcb", "advanced"),
    ("pcbway", "standard"),
    ("oshpark", "2layer"),
)


def _dru_text(project_dir: Path) -> str:
    return (project_dir / "demo.kicad_dru").read_text(encoding="utf-8")


def _board_track_min_present(dru_text: str, mm_value: float) -> bool:
    """Return True if a board-level minimum track width constraint at ``mm_value`` is present."""
    needle = (
        f'(rule "Board minimum track width"\n'
        f"  (condition \"A.Type == 'track'\")\n"
        f"  (constraint track_width (min {mm_value:.4f}mm) (opt {mm_value:.4f}mm))\n"
        f")"
    )
    return needle in dru_text


@pytest.mark.anyio
async def test_apply_drc_and_net_classes_happy_path(
    sample_project,
    mock_kicad,
) -> None:
    """jlcpcb_standard applies a full DRC + net-class rule set."""
    server = build_server("pcb")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {"manufacturer": "JLCPCB", "tier": "standard"},
    )

    dru_text = _dru_text(sample_project)

    # Response copy
    assert "Applied profile JLCPCB / standard." in result
    assert "DRC floor:" in result
    assert "Net classes:" in result
    assert "Call pcb_save() to persist" in result  # PERSISTENCE_HINT contract

    # DRC floor — derived from jlcpcb_standard.json:
    #   min_drill 0.3 + 2*0.15 annular = 0.6 via diameter
    #   max(2*0.3, 0.25) = 0.6 hole-to-hole
    assert _board_track_min_present(dru_text, 0.127)
    assert "(constraint clearance (min 0.1270mm))" in dru_text
    assert "(constraint hole_size (min 0.3000mm))" in dru_text
    assert "(constraint via_diameter (min 0.6000mm))" in dru_text
    assert "(constraint annular_width (min 0.1500mm))" in dru_text
    assert "(constraint hole_to_hole (min 0.6000mm))" in dru_text

    # Each of the four shipped net classes must produce a (rule ...) entry.
    for nc_name in NET_CLASS_NAMES:
        assert f'(rule "Net class {nc_name}"' in dru_text, (
            f"Net class {nc_name} block missing from .kicad_dru"
        )
        assert f"A.NetClass == '{nc_name}'" in dru_text

    # Default class baseline (0.25/0.20/0.6/0.3) from jlcpcb_standard.json
    assert "(constraint track_width (min 0.2500mm) (opt 0.2500mm) (max 0.2500mm))" in dru_text
    # HighCurrent class baseline (1.0/0.5/1.0/0.5)
    assert "(constraint track_width (min 1.0000mm) (opt 1.0000mm) (max 1.0000mm))" in dru_text


@pytest.mark.anyio
async def test_apply_only_net_classes_leaves_drc_untouched(
    sample_project,
    mock_kicad,
) -> None:
    """apply_drc=False writes net-class rules but no board-level DRC floor."""
    server = build_server("pcb")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {
            "manufacturer": "jlcpcb",
            "tier": "standard",
            "apply_drc": False,
            "apply_net_classes": True,
        },
    )

    dru_text = _dru_text(sample_project)
    assert "DRC: skipped (apply_drc=False)." in result
    assert "Board minimum track width" not in dru_text
    assert "Board minimum clearance" not in dru_text
    assert "Board minimum via geometry" not in dru_text
    # All four net-class rules still landed.
    for nc_name in NET_CLASS_NAMES:
        assert f'(rule "Net class {nc_name}"' in dru_text


@pytest.mark.anyio
async def test_apply_only_drc_leaves_net_classes_untouched(
    sample_project,
    mock_kicad,
) -> None:
    """apply_net_classes=False writes DRC floor but no net-class rules."""
    server = build_server("pcb")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {
            "manufacturer": "jlcpcb",
            "tier": "standard",
            "apply_drc": True,
            "apply_net_classes": False,
        },
    )

    dru_text = _dru_text(sample_project)
    assert "Net classes: skipped (apply_net_classes=False)." in result
    assert "Board minimum track width" in dru_text
    for nc_name in NET_CLASS_NAMES:
        assert f'(rule "Net class {nc_name}"' not in dru_text


@pytest.mark.anyio
async def test_dry_run_writes_nothing(
    sample_project,
    mock_kicad,
) -> None:
    """dry_run=True must NOT modify the .kicad_dru file."""
    server = build_server("pcb")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    dru_path = sample_project / "demo.kicad_dru"
    before = dru_path.read_text(encoding="utf-8")

    result = await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {
            "manufacturer": "jlcpcb",
            "tier": "standard",
            "dry_run": True,
        },
    )

    after = dru_path.read_text(encoding="utf-8")
    assert before == after, "dry_run modified the .kicad_dru file"
    assert "DRY RUN" in result
    assert "No files were written." in result
    # The response must still telegraph every value that WOULD be written so the
    # user can compare/approve.
    assert "Min trace width: 0.127 mm" in result
    assert "Min clearance: 0.127 mm" in result
    assert "Min via drill: 0.300 mm" in result
    assert "Min via diameter: 0.600 mm" in result
    assert "Min annular ring: 0.150 mm" in result
    assert "Min hole-to-hole: 0.600 mm" in result
    for nc_name in NET_CLASS_NAMES:
        assert nc_name in result


@pytest.mark.anyio
async def test_unknown_manufacturer_lists_available_profiles(
    sample_project,
    mock_kicad,
) -> None:
    server = build_server("pcb")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {"manufacturer": "nope_unknown", "tier": "standard"},
    )

    assert "Unknown manufacturer profile" in result
    assert "Available profiles" in result
    # At least one bundled profile must be enumerated so the user can pick one.
    assert "jlcpcb_standard" in result


@pytest.mark.anyio
async def test_unknown_tier_is_clear_error(
    sample_project,
    mock_kicad,
) -> None:
    server = build_server("pcb")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {"manufacturer": "jlcpcb", "tier": "ultra_unobtanium"},
    )

    assert "Unknown manufacturer profile" in result
    # Sanity: the lookup name embeds tier explicitly.
    assert "jlcpcb/ultra_unobtanium" in result or "ultra_unobtanium" in result


@pytest.mark.anyio
async def test_profile_without_net_classes_block_graceful(
    sample_project,
    mock_kicad,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A profile missing the net_classes block applies DRC and surfaces a clear note."""
    # Drop a custom profile file into a temporary copy of the dfm_profiles
    # directory and point importlib.resources at it via monkeypatching the
    # ``files`` lookup. Easier: ship a tier name that maps to a real bundled
    # profile that we KNOW is rules-only, the existing ``jlcpcb_rotations``.
    server = build_server("pcb")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    result = await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {"manufacturer": "jlcpcb", "tier": "rotations"},
    )

    dru_text = _dru_text(sample_project)
    # jlcpcb_rotations has no 'rules' nor 'net_classes' blocks — both must
    # be skipped with explicit messaging and the .kicad_dru is unchanged.
    assert "NOT applied" in result
    assert "no 'rules' block" in result
    assert "no 'net_classes' block" in result
    assert "Board minimum track width" not in dru_text
    assert '(rule "Net class Default"' not in dru_text


@pytest.mark.anyio
async def test_double_apply_is_idempotent(
    sample_project,
    mock_kicad,
) -> None:
    """Calling the tool twice with identical args must not duplicate rules."""
    server = build_server("pcb")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {"manufacturer": "jlcpcb", "tier": "standard"},
    )
    await call_tool_text(
        server,
        "pcb_apply_manufacturer_profile",
        {"manufacturer": "jlcpcb", "tier": "standard"},
    )

    dru_text = _dru_text(sample_project)
    # Each declared block must appear exactly once, regardless of how many
    # times the tool was invoked.
    for rule_name in (
        "Board minimum track width",
        "Board minimum clearance",
        "Board minimum via geometry",
        "Net class Default",
        "Net class Signal",
        "Net class Power",
        "Net class HighCurrent",
    ):
        occurrences = dru_text.count(f'(rule "{rule_name}"')
        assert occurrences == 1, (
            f"Rule '{rule_name}' appeared {occurrences} times in .kicad_dru — "
            "the upsert helper is not idempotent."
        )


# --- Unit-style: lock the shape of every shipped profile's net_classes ------


@pytest.mark.parametrize("manufacturer,tier", SHIPPED_PROFILES_WITH_NET_CLASSES)
def test_shipped_profile_has_expected_net_class_shape(
    manufacturer: str,
    tier: str,
) -> None:
    """Every shipped design-rule profile must declare the four canonical net classes.

    Catches future drift where a profile gets a partial update (e.g. only
    Default/Signal). A 4-key contract is the cheap insurance.
    """
    profile_root = resources.files("kicad_mcp.dfm_profiles")
    resource = profile_root / f"{manufacturer}_{tier}.json"
    assert resource.is_file(), f"Missing profile file: {resource}"

    profile = json.loads(resource.read_text(encoding="utf-8"))
    assert "net_classes" in profile, (
        f"Profile {manufacturer}/{tier} is missing the 'net_classes' block."
    )
    net_classes = profile["net_classes"]
    assert set(net_classes.keys()) == set(NET_CLASS_NAMES), (
        f"Profile {manufacturer}/{tier} has net classes {sorted(net_classes.keys())}, "
        f"expected {sorted(NET_CLASS_NAMES)}."
    )
    for nc_name, nc_config in net_classes.items():
        for key in NET_CLASS_KEYS:
            assert key in nc_config, (
                f"Profile {manufacturer}/{tier} net class '{nc_name}' missing required key '{key}'."
            )
            assert isinstance(nc_config[key], int | float), (
                f"Profile {manufacturer}/{tier} net class '{nc_name}' "
                f"key '{key}' must be numeric, got {type(nc_config[key]).__name__}."
            )
            assert nc_config[key] > 0, (
                f"Profile {manufacturer}/{tier} net class '{nc_name}' "
                f"key '{key}' must be > 0, got {nc_config[key]}."
            )
