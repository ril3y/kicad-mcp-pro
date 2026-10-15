"""Unit tests for ``kicad_mcp.tools.routing_rules`` helpers.

These helpers got more reuse with ``pcb_apply_manufacturer_profile`` (PR #25)
than they used to have, and a few edge branches were left unexercised. Tests
here lock the defensive behavior so future refactors don't silently swallow
errors that the manufacturer-profile tool depends on for clear messages.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kicad_mcp.config import get_config, reset_config
from kicad_mcp.tools.routing_rules import (
    _is_balanced,
    _load_rules_content,
    _rules_file_path,
    _upsert_rule,
    _write_rule,
)


def _point_config_at(project_dir: Path, project_file: Path | None = None) -> None:
    """Helper: mutate the config singleton so routing_rules helpers see this
    project_dir / project_file pair. Avoids the longer kicad_set_project tool
    dance for unit-level tests."""
    reset_config()
    cfg = get_config()
    cfg.project_dir = project_dir
    cfg.project_file = project_file


# --- _rules_file_path --------------------------------------------------------


def test_rules_file_path_without_project_raises() -> None:
    """No project_dir configured -> clean ValueError telling the caller to set one."""
    reset_config()
    with pytest.raises(ValueError, match="No project directory is configured"):
        _rules_file_path()


def test_rules_file_path_falls_back_when_no_existing_dru(tmp_path: Path) -> None:
    """If no .kicad_dru exists yet and no .kicad_pro is set, fall back to a
    canonical 'design_rules.kicad_dru' filename."""
    _point_config_at(tmp_path)
    result = _rules_file_path()
    assert result == tmp_path / "design_rules.kicad_dru"


def test_rules_file_path_uses_project_file_stem_when_no_dru(tmp_path: Path) -> None:
    """If a .kicad_pro is set but no .kicad_dru exists yet, derive the .kicad_dru
    filename from the project file stem so both files share a name."""
    pro = tmp_path / "myboard.kicad_pro"
    pro.write_text("{}", encoding="utf-8")
    _point_config_at(tmp_path, project_file=pro)
    result = _rules_file_path()
    assert result == tmp_path / "myboard.kicad_dru"


# --- _is_balanced ------------------------------------------------------------


def test_is_balanced_returns_false_on_excess_close_paren() -> None:
    """Closing without matching open must short-circuit to False."""
    assert _is_balanced('(rule "x"))') is False


def test_is_balanced_accepts_escaped_quote_inside_string() -> None:
    """A backslash-escaped quote inside a string token must not flip the
    in-string state. Lock the escape-handling branch."""
    # The inner \" stays inside the string; the closing " ends it; balanced.
    assert _is_balanced('(rule "has \\" quote") (constraint)') is True


def test_is_balanced_accepts_escaped_backslash_inside_string() -> None:
    """A backslash before something that is NOT a quote still consumes one
    char of state — covers the bare backslash branch in the escape machine."""
    assert _is_balanced('(rule "\\path\\to\\file")') is True


# --- _load_rules_content -----------------------------------------------------


def test_load_rules_content_returns_default_for_missing_file(tmp_path: Path) -> None:
    """Missing .kicad_dru is normal (first-time project) — return the empty
    (rules) sexpr stub instead of raising."""
    assert _load_rules_content(tmp_path / "absent.kicad_dru") == "(rules)\n"


def test_load_rules_content_returns_default_for_whitespace_only_file(tmp_path: Path) -> None:
    """A whitespace-only file is treated as empty and gets the stub."""
    path = tmp_path / "blank.kicad_dru"
    path.write_text("   \n\t\n", encoding="utf-8")
    assert _load_rules_content(path) == "(rules)\n"


def test_load_rules_content_refuses_unbalanced_file(tmp_path: Path) -> None:
    """An unbalanced .kicad_dru is presumed mid-write / corrupt — refuse so we
    don't compound the damage by writing more rules on top."""
    path = tmp_path / "broken.kicad_dru"
    path.write_text("(rules", encoding="utf-8")  # never closed
    with pytest.raises(ValueError, match="unbalanced parentheses"):
        _load_rules_content(path)


# --- _upsert_rule ------------------------------------------------------------


def test_upsert_rule_inserts_into_empty_rules() -> None:
    """Inserting into the empty stub produces a balanced result with the new
    rule body before the closing root paren."""
    body = '(rule "Net class Foo"\n  (condition "true")\n  (constraint clearance (min 0.20mm))\n)'
    updated = _upsert_rule("(rules)\n", "Net class Foo", body)
    assert "Net class Foo" in updated
    assert _is_balanced(updated)


def test_upsert_rule_replaces_existing_rule() -> None:
    """Idempotent re-upsert: the second call with a different body replaces
    the first, doesn't duplicate."""
    body_v1 = (
        '(rule "Net class Foo"\n  (condition "true")\n  (constraint clearance (min 0.20mm))\n)'
    )
    body_v2 = (
        '(rule "Net class Foo"\n  (condition "true")\n  (constraint clearance (min 0.30mm))\n)'
    )
    intermediate = _upsert_rule("(rules)\n", "Net class Foo", body_v1)
    final = _upsert_rule(intermediate, "Net class Foo", body_v2)
    assert final.count('(rule "Net class Foo"') == 1
    assert "0.30mm" in final
    assert "0.20mm" not in final


def test_upsert_rule_refuses_invalid_root_form() -> None:
    """If the file has no root '(rules ...)' sexpr at all, we cannot decide
    where to insert — raise so the caller surfaces it."""
    body = '(rule "Net class Foo"\n  (constraint clearance (min 0.20mm))\n)'
    with pytest.raises(ValueError, match="does not contain a root"):
        _upsert_rule("# just a comment, no parens", "Net class Foo", body)


# --- _write_rule (end-to-end on real path resolution) ------------------------


def test_write_rule_creates_file_when_missing(tmp_path: Path) -> None:
    """First-time write on a fresh project dir creates the file with the rule.

    Also exercises the full _rules_file_path -> _load_rules_content ->
    _upsert_rule -> path.write_text chain in one go.
    """
    _point_config_at(tmp_path)
    body = '(rule "Net class Bar"\n  (condition "true")\n  (constraint clearance (min 0.25mm))\n)'
    path = _write_rule("Net class Bar", body)
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Net class Bar" in content
    assert _is_balanced(content)
