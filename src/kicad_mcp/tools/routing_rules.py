"""Shared helpers for KiCad design-rules file edits."""

from __future__ import annotations

from pathlib import Path

from ..config import get_config
from ..utils.sexpr import _extract_block, _sexpr_string


def _rules_file_path() -> Path:
    cfg = get_config()
    if cfg.project_dir is None:
        raise ValueError(
            "No project directory is configured. Call kicad_set_project() "
            "before editing routing rules."
        )

    existing = sorted(cfg.project_dir.glob("*.kicad_dru"))
    if existing:
        return existing[0]

    if cfg.project_file is not None:
        return cfg.project_dir / f"{cfg.project_file.stem}.kicad_dru"
    return cfg.project_dir / "design_rules.kicad_dru"


def _is_balanced(content: str) -> bool:
    depth = 0
    in_string = False
    escaped = False
    for char in content:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not in_string


def _load_rules_content(path: Path) -> str:
    if not path.exists():
        return "(rules)\n"
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return "(rules)\n"
    if not _is_balanced(content):
        raise ValueError(
            "Refusing to write an invalid design rules file with unbalanced parentheses."
        )
    return content


def _upsert_rule(content: str, rule_name: str, rule_body: str) -> str:
    search = f"(rule {_sexpr_string(rule_name)}"
    index = content.find(search)
    if index >= 0:
        block, consumed = _extract_block(content, index)
        if not block or consumed == 0:
            raise ValueError(f"Could not replace existing rule block for {rule_name}.")
        updated = content[:index] + rule_body + content[index + consumed :]
    else:
        stripped = content.rstrip()
        insert_at = stripped.rfind(")")
        if insert_at < 0:
            raise ValueError("The design rules file does not contain a root '(rules ...)' form.")
        prefix = stripped[:insert_at].rstrip()
        suffix = stripped[insert_at:]
        updated = f"{prefix}\n{rule_body}\n{suffix}\n"
    if not _is_balanced(updated):
        raise ValueError(f"Refusing to write invalid design rules after updating {rule_name}.")
    return updated


def _write_rule(rule_name: str, rule_body: str) -> Path:
    path = _rules_file_path()
    content = _load_rules_content(path)
    updated = _upsert_rule(content, rule_name, rule_body)
    path.write_text(updated, encoding="utf-8")
    return path


def _mm(value: float) -> str:
    return f"{value:.4f}mm"


def _net_class_rule_body(
    net_class: str,
    width_mm: float,
    clearance_mm: float,
    via_diameter_mm: float,
    via_drill_mm: float,
) -> tuple[str, str]:
    track_width_constraint = (
        f"  (constraint track_width (min {_mm(width_mm)}) "
        f"(opt {_mm(width_mm)}) (max {_mm(width_mm)}))"
    )
    via_diameter_constraint = (
        f"  (constraint via_diameter (min {_mm(via_diameter_mm)}) "
        f"(opt {_mm(via_diameter_mm)}) (max {_mm(via_diameter_mm)}))"
    )
    via_drill_constraint = (
        f"  (constraint via_drill (min {_mm(via_drill_mm)}) "
        f"(opt {_mm(via_drill_mm)}) (max {_mm(via_drill_mm)}))"
    )
    name = f"Net class {net_class}"
    body = "\n".join(
        [
            f"(rule {_sexpr_string(name)}",
            f"  (condition \"A.NetClass == '{net_class}'\")",
            track_width_constraint,
            f"  (constraint clearance (min {_mm(clearance_mm)}))",
            via_diameter_constraint,
            via_drill_constraint,
            ")",
        ]
    )
    return name, body
