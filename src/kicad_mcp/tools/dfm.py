"""Manufacturer-specific DFM profile tools."""

from __future__ import annotations

import json
import re
from importlib import resources
from pathlib import Path
from typing import Any, Protocol, cast

import structlog
from kipy.board_types import Track, Via
from kipy.proto.board.board_types_pb2 import BoardLayer
from mcp.server.fastmcp import FastMCP

from ..connection import KiCadConnectionError, get_board
from ..utils.sexpr import _extract_block
from ..utils.units import nm_to_mm
from .export_support import _ensure_output_dir, _get_pcb_file, _run_cli_variants
from .metadata import headless_compatible

logger = structlog.get_logger(__name__)
DEFAULT_PROFILE = ("JLCPCB", "standard")
FLOAT_PATTERN = r"-?\d+(?:\.\d+)?"


class _BoardMetricsLike(Protocol):
    """Subset of board access used by the DFM profile helpers."""

    def get_enabled_layers(self) -> list[int]:
        raise NotImplementedError

    def get_tracks(self) -> list[Track]:
        raise NotImplementedError

    def get_vias(self) -> list[Via]:
        raise NotImplementedError


def _profile_resource_name(manufacturer: str, tier: str) -> str:
    return f"{manufacturer.strip().lower()}_{tier.strip().lower()}.json"


def _available_profile_names() -> list[str]:
    profile_root = resources.files("kicad_mcp.dfm_profiles")
    return sorted(
        entry.name[:-5] for entry in profile_root.iterdir() if entry.name.endswith(".json")
    )


def _load_profile(manufacturer: str, tier: str) -> dict[str, Any]:
    resource_name = _profile_resource_name(manufacturer, tier)
    resource_root = resources.files("kicad_mcp.dfm_profiles")
    resource = resource_root / resource_name
    if not resource.is_file():
        available = ", ".join(_available_profile_names())
        raise ValueError(
            f"Unknown DFM profile '{manufacturer}/{tier}'. Available profiles: {available}"
        )
    return cast(dict[str, Any], json.loads(resource.read_text(encoding="utf-8")))


def _active_profile_path() -> Path:
    return _ensure_output_dir() / "active_dfm_profile.json"


def _write_active_profile_selection(manufacturer: str, tier: str) -> Path:
    path = _active_profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"manufacturer": manufacturer, "tier": tier}, indent=2),
        encoding="utf-8",
    )
    return path


def _selected_profile() -> dict[str, Any]:
    path = _active_profile_path()
    if path.exists():
        selection = cast(dict[str, str], json.loads(path.read_text(encoding="utf-8")))
        return _load_profile(
            selection.get("manufacturer", DEFAULT_PROFILE[0]),
            selection.get("tier", DEFAULT_PROFILE[1]),
        )
    return _load_profile(*DEFAULT_PROFILE)


def _try_get_board() -> object | None:
    try:
        return get_board()
    except (KiCadConnectionError, OSError) as exc:
        logger.debug("dfm_board_runtime_unavailable", error=str(exc))
        return None


def _board_metrics() -> dict[str, float | int | None]:
    board = _try_get_board()
    if board is None:
        return {
            "copper_layers": None,
            "min_track_width_mm": None,
            "min_via_drill_mm": None,
            "min_via_diameter_mm": None,
            "via_count": None,
        }

    board_metrics = cast(_BoardMetricsLike, board)
    layers = [
        layer for layer in board_metrics.get_enabled_layers() if "_Cu" in BoardLayer.Name(layer)
    ]
    tracks = board_metrics.get_tracks()
    vias = board_metrics.get_vias()
    return {
        "copper_layers": len(layers),
        "min_track_width_mm": min(
            (nm_to_mm(track.width) for track in tracks),
            default=None,
        ),
        "min_via_drill_mm": min(
            (nm_to_mm(via.drill_diameter) for via in vias),
            default=None,
        ),
        "min_via_diameter_mm": min(
            (nm_to_mm(via.diameter) for via in vias),
            default=None,
        ),
        "via_count": len(vias),
    }


def _run_drc_report(report_name: str) -> tuple[Path, dict[str, Any] | None, str | None]:
    pcb_file = _get_pcb_file()
    out_file = _ensure_output_dir() / report_name
    code, _, stderr = _run_cli_variants(
        [
            [
                "pcb",
                "drc",
                "--output",
                str(out_file),
                "--format",
                "json",
                "--severity-all",
                "--exit-code-violations",
                str(pcb_file),
            ],
            [
                "pcb",
                "drc",
                "--input",
                str(pcb_file),
                "--output",
                str(out_file),
                "--format",
                "json",
                "--severity-all",
                "--exit-code-violations",
            ],
        ]
    )
    if not out_file.exists():
        return out_file, None, stderr if code != 0 else "DRC report was not produced."
    return out_file, cast(dict[str, Any], json.loads(out_file.read_text(encoding="utf-8"))), None


def _outline_bounds_mm(content: str) -> tuple[float, float, float, float] | None:
    xs: list[float] = []
    ys: list[float] = []
    cursor = 0
    while cursor < len(content):
        next_line = content.find("(gr_line", cursor)
        next_rect = content.find("(gr_rect", cursor)
        indices = [index for index in (next_line, next_rect) if index != -1]
        if not indices:
            break
        start = min(indices)
        block, length = _extract_block(content, start)
        if not block:
            break
        cursor = start + length
        if '(layer "Edge.Cuts")' not in block:
            continue
        match = re.search(
            rf"\(start\s+({FLOAT_PATTERN})\s+({FLOAT_PATTERN})\).*?"
            rf"\(end\s+({FLOAT_PATTERN})\s+({FLOAT_PATTERN})\)",
            block,
            re.DOTALL,
        )
        if match is None:
            continue
        xs.extend([float(match.group(1)), float(match.group(3))])
        ys.extend([float(match.group(2)), float(match.group(4))])
    if not xs or not ys:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def _board_outline_area_cm2() -> tuple[float | None, float | None, float | None]:
    pcb_text = _get_pcb_file().read_text(encoding="utf-8", errors="ignore")
    bounds = _outline_bounds_mm(pcb_text)
    if bounds is None:
        return None, None, None
    min_x_mm, min_y_mm, max_x_mm, max_y_mm = bounds
    width_mm = max_x_mm - min_x_mm
    height_mm = max_y_mm - min_y_mm
    return width_mm, height_mm, (width_mm * height_mm) / 100.0


def _format_status(status: str, message: str) -> str:
    return f"- {status}: {message}"


def _recommended_design_rules(profile: dict[str, Any]) -> dict[str, float]:
    """Map a manufacturer DFM profile onto ``pcb_set_design_rules`` arguments.

    The profile JSONs store fab-side minimums (track width, drill, annular
    ring); the design-rule writer expects board-side argument names. Bridge
    them so users can apply a manufacturer baseline without having to look
    up the schema. Derived values:

    - ``min_via_diameter_mm = min_drill_mm + 2 * min_annular_ring_mm``
      (the smallest annular-ring-clean via the fab will accept).
    - ``min_hole_to_hole_mm = max(2 * min_drill_mm, 0.25)``
      (profiles don't store this; 2x drill is a conservative industry
      default and matches JLCPCB's published spec for standard tier).

    Raises ``ValueError`` if the profile lacks a ``rules`` block — this
    catches loaders pointing at an auxiliary profile (e.g. the
    ``jlcpcb_rotations`` BOM-rotation database) that doesn't carry
    design-rule fields.
    """
    if "rules" not in profile:
        raise ValueError(
            f"Profile '{profile.get('manufacturer', '?')}/"
            f"{profile.get('tier', '?')}' has no 'rules' block — it is "
            "likely a non-design-rule auxiliary profile (e.g. a BOM "
            "rotation database). Load a profile that includes design "
            "rules (jlcpcb_standard, jlcpcb_advanced, oshpark_2layer, "
            "pcbway_standard)."
        )
    rules = cast(dict[str, float], profile["rules"])
    drill = float(rules["min_drill_mm"])
    annular = float(rules["min_annular_ring_mm"])
    return {
        "min_trace_width_mm": float(rules["min_trace_width_mm"]),
        "min_clearance_mm": float(rules["min_trace_clearance_mm"]),
        "min_via_drill_mm": drill,
        "min_via_diameter_mm": drill + 2.0 * annular,
        "min_annular_ring_mm": annular,
        "min_hole_to_hole_mm": max(2.0 * drill, 0.25),
    }


def _dfm_check_lines(
    profile: dict[str, Any],
    *,
    heading: str | None = None,
) -> list[str]:
    rules = cast(dict[str, float | int], profile["rules"])
    metrics = _board_metrics()
    _, report, error = _run_drc_report("dfm_profile_check.json")
    violations = cast(list[dict[str, Any]], report.get("violations", [])) if report else []
    unconnected = cast(list[dict[str, Any]], report.get("unconnected_items", [])) if report else []
    courtyard = (
        cast(list[dict[str, Any]], report.get("items_not_passing_courtyard", [])) if report else []
    )
    silk = [entry for entry in violations if "silk" in str(entry.get("description", "")).lower()]

    lines = [
        heading or "DFM profile check:",
        f"- Profile: {profile['manufacturer']} / {profile['tier']}",
    ]
    checks_run = 0

    copper_layers = metrics["copper_layers"]
    if copper_layers is None:
        lines.append(
            _format_status(
                "WARN",
                "Copper layer count unavailable without an active board.",
            )
        )
    else:
        checks_run += 1
        status = "PASS" if copper_layers <= int(rules["max_layers"]) else "FAIL"
        lines.append(
            _format_status(
                status,
                f"Copper layers {copper_layers} <= max {int(rules['max_layers'])}",
            )
        )

    min_track_width_mm = metrics["min_track_width_mm"]
    if min_track_width_mm is None:
        lines.append(
            _format_status(
                "WARN",
                "Minimum track width unavailable without an active board.",
            )
        )
    else:
        checks_run += 1
        status = "PASS" if min_track_width_mm >= float(rules["min_trace_width_mm"]) else "FAIL"
        lines.append(
            _format_status(
                status,
                f"Minimum track width {min_track_width_mm:.3f} mm "
                f">= {float(rules['min_trace_width_mm']):.3f} mm",
            )
        )

    min_via_drill_mm = metrics["min_via_drill_mm"]
    if min_via_drill_mm is None:
        lines.append(
            _format_status(
                "WARN",
                "Minimum via drill unavailable without an active board.",
            )
        )
    else:
        checks_run += 1
        status = "PASS" if min_via_drill_mm >= float(rules["min_drill_mm"]) else "FAIL"
        lines.append(
            _format_status(
                status,
                f"Minimum via drill {min_via_drill_mm:.3f} mm "
                f">= {float(rules['min_drill_mm']):.3f} mm",
            )
        )

    if report is None:
        lines.append(_format_status("WARN", f"DRC report unavailable ({error})."))
    else:
        checks_run += 3
        lines.append(
            _format_status(
                "PASS" if not violations else "FAIL",
                f"DRC violations: {len(violations)}",
            )
        )
        lines.append(
            _format_status(
                "PASS" if not unconnected else "FAIL",
                f"Unconnected items: {len(unconnected)}",
            )
        )
        lines.append(
            _format_status(
                "PASS" if not courtyard else "WARN",
                f"Courtyard issues: {len(courtyard)}",
            )
        )
        lines.append(
            _format_status(
                "PASS" if not silk else "WARN",
                f"Silk overlap hints: {len(silk)}",
            )
        )
        checks_run += 1

    lines.append(
        _format_status(
            "WARN",
            "Manual review: annular ring, copper-to-edge, and silkscreen text size "
            f"against {profile['manufacturer']} {profile['tier']} fab notes.",
        )
    )
    lines.insert(2, f"- Checks run: {checks_run}")
    return lines


def _cost_lines(
    profile: dict[str, Any],
    quantity: int,
) -> list[str]:
    pricing = cast(dict[str, float], profile["pricing"])
    width_mm, height_mm, area_cm2 = _board_outline_area_cm2()
    metrics = _board_metrics()
    copper_layers = int(metrics["copper_layers"] or 2)
    via_count = int(metrics["via_count"] or 0)
    if area_cm2 is None:
        area_cm2 = 25.0

    layer_multiplier = 1.0 + (max(copper_layers - 2, 0) * float(pricing["extra_layer_multiplier"]))
    setup_cost = float(pricing["setup_usd"])
    area_cost = quantity * area_cm2 * float(pricing["per_sq_cm_usd"]) * layer_multiplier
    drill_cost = quantity * via_count * float(pricing["per_drill_usd"])
    total_cost = setup_cost + area_cost + drill_cost

    lines = [
        "Manufacturing cost estimate:",
        f"- Profile: {profile['manufacturer']} / {profile['tier']}",
        f"- Quantity: {quantity}",
    ]
    if width_mm is not None and height_mm is not None:
        lines.append(f"- Board size: {width_mm:.2f} x {height_mm:.2f} mm")
    else:
        lines.append("- Board size: unavailable, using a conservative 25.00 cm^2 estimate")
    lines.extend(
        [
            f"- Board area: {area_cm2:.2f} cm^2",
            f"- Copper layers: {copper_layers}",
            f"- Via count estimate: {via_count}",
            f"- Setup: ${setup_cost:.2f}",
            f"- Area cost: ${area_cost:.2f}",
            f"- Drill cost: ${drill_cost:.2f}",
            f"- Total: ${total_cost:.2f}",
        ]
    )
    return lines


def register(mcp: FastMCP) -> None:
    """Register DFM tools."""

    @mcp.tool()
    @headless_compatible
    def dfm_load_manufacturer_profile(
        manufacturer: str = "JLCPCB",
        tier: str = "standard",
    ) -> str:
        """Load a bundled manufacturer DFM profile for subsequent checks."""
        profile = _load_profile(manufacturer, tier)
        state_path = _write_active_profile_selection(
            str(profile["manufacturer"]),
            str(profile["tier"]),
        )
        return "\n".join(
            [
                "DFM profile loaded.",
                f"- Active profile: {profile['manufacturer']} / {profile['tier']}",
                f"- State file: {state_path}",
            ]
        )

    @mcp.tool()
    @headless_compatible
    def dfm_run_manufacturer_check() -> str:
        """Run a manufacturer-aware DFM review using the active bundled profile."""
        profile = _selected_profile()
        return "\n".join(_dfm_check_lines(profile))

    @mcp.tool()
    @headless_compatible
    def dfm_get_recommended_design_rules(
        manufacturer: str | None = None,
        tier: str | None = None,
    ) -> str:
        """Show the manufacturer's recommended ``pcb_set_design_rules`` values.

        Reads the active profile (or the explicit ``manufacturer`` / ``tier``
        if provided) and emits the six float arguments ``pcb_set_design_rules``
        accepts, derived from the profile's fab minimums. The output is
        formatted so an LLM client can copy-paste the arg block straight into
        a ``pcb_set_design_rules`` call without looking up schema.
        """
        if manufacturer is not None and tier is not None:
            profile = _load_profile(manufacturer, tier)
        elif manufacturer is None and tier is None:
            profile = _selected_profile()
        else:
            raise ValueError(
                "Pass both 'manufacturer' and 'tier' or neither (to use the "
                "active profile saved by dfm_load_manufacturer_profile)."
            )

        rules = _recommended_design_rules(profile)
        lines = [
            "Recommended pcb_set_design_rules arguments:",
            f"- Profile: {profile['manufacturer']} / {profile['tier']}",
            f"- min_trace_width_mm: {rules['min_trace_width_mm']:.3f}",
            f"- min_clearance_mm: {rules['min_clearance_mm']:.3f}",
            f"- min_via_drill_mm: {rules['min_via_drill_mm']:.3f}",
            f"- min_via_diameter_mm: {rules['min_via_diameter_mm']:.3f}",
            f"- min_annular_ring_mm: {rules['min_annular_ring_mm']:.3f}",
            f"- min_hole_to_hole_mm: {rules['min_hole_to_hole_mm']:.3f}",
            "",
            "Apply with:",
            "  pcb_set_design_rules("
            f"min_trace_width_mm={rules['min_trace_width_mm']:.3f}, "
            f"min_clearance_mm={rules['min_clearance_mm']:.3f}, "
            f"min_via_drill_mm={rules['min_via_drill_mm']:.3f}, "
            f"min_via_diameter_mm={rules['min_via_diameter_mm']:.3f}, "
            f"min_annular_ring_mm={rules['min_annular_ring_mm']:.3f}, "
            f"min_hole_to_hole_mm={rules['min_hole_to_hole_mm']:.3f})",
        ]
        return "\n".join(lines)

    @mcp.tool()
    @headless_compatible
    def dfm_calculate_manufacturing_cost(
        quantity: int = 10,
        manufacturer: str = "JLCPCB",
        tier: str = "standard",
    ) -> str:
        """Estimate fabrication cost from board area, layers, and via count."""
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        profile = _load_profile(manufacturer, tier)
        return "\n".join(_cost_lines(profile, quantity))
