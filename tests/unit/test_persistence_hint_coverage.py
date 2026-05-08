"""Static coverage check for the PR #11 persistence-hint sweep.

Every IPC-mutating tool in ``src/kicad_mcp/tools/pcb.py`` must reference
``_PERSISTENCE_HINT`` in its body so its success response tells the
caller to follow up with ``pcb_save()``. This test scans the production
file's text to confirm each named tool's def block contains the
constant — catches regressions where a refactor accidentally drops the
hint from one tool while leaving the others intact.

Pre-fix behavior was that mutating tools silently lost their changes if
pcbnew closed without saving. PR #10 added the hint to one tool
(``pcb_set_footprint_attributes``); PR #11 swept it across the rest and
hoisted the constant to ``connection.py`` so sibling modules
(``routing.py``, ``power_integrity.py``) can import it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from kicad_mcp.connection import PERSISTENCE_HINT

# Tools that mutate pcbnew's in-memory board over IPC and never write to
# the .kicad_pcb file themselves. Each must call _PERSISTENCE_HINT in its
# success path. ``pcb_save`` is intentionally excluded (it IS the save).
# File-based tools (e.g. pcb_set_design_rules → .kicad_dru, pcb_block_place
# → _transactional_board_write) are also excluded; their persistence is
# different and out of this PR's scope.
_IPC_MUTATING_TOOLS = [
    "pcb_refill_zones",
    "pcb_add_track",
    "pcb_add_tracks_bulk",
    "pcb_add_via",
    "pcb_add_blind_via",
    "pcb_add_microvia",
    "pcb_add_segment",
    "pcb_add_circle",
    "pcb_add_rectangle",
    "pcb_set_board_outline",
    "pcb_add_text",
    "pcb_delete_items",
    "pcb_move_footprint",
    "pcb_set_footprint_layer",
    "pcb_set_footprint_attributes",
    "pcb_add_zone",
    "pcb_set_keepout_zone",
    "pcb_add_teardrops",
]


def _pcb_module_text() -> str:
    src_path = (
        Path(__file__).resolve().parent.parent.parent / "src" / "kicad_mcp" / "tools" / "pcb.py"
    )
    return src_path.read_text(encoding="utf-8")


def _function_body(source: str, name: str) -> str:
    """Return the text of the named function's body up to the next ``def``
    (peer or ``@mcp.tool()``) so the static check is scoped to one tool."""
    # Anchor on ``def <name>(`` then capture until the next decorator or
    # function def at the same indentation. Tools live inside ``register``
    # so their indentation is one level deeper, but we don't need to be
    # precise — we just need the next ``def `` token at any indent.
    pattern = re.compile(
        rf"def {re.escape(name)}\b.*?(?=\n\s*@mcp\.tool|\n\s*def |\Z)",
        re.DOTALL,
    )
    match = pattern.search(source)
    if match is None:
        raise AssertionError(
            f"could not locate function ``{name}`` in pcb.py — has it been "
            "renamed or moved? Update _IPC_MUTATING_TOOLS."
        )
    return match.group(0)


def test_persistence_hint_constant_is_defined() -> None:
    """The ``PERSISTENCE_HINT`` constant must exist in ``connection.py``.

    Lives there (not in any single tool module) so siblings like
    ``routing.py`` and ``power_integrity.py`` can import it without
    crossing tool-package boundaries — see PR #11's E-audit fix.
    """
    src = (
        Path(__file__).resolve().parent.parent.parent / "src" / "kicad_mcp" / "connection.py"
    ).read_text(encoding="utf-8")
    assert re.search(r"^PERSISTENCE_HINT\s*=", src, re.MULTILINE), (
        "PERSISTENCE_HINT module-level constant is missing from connection.py"
    )


def test_persistence_hint_value_matches_import() -> None:
    """The text in ``connection.py`` must equal what's imported at runtime.
    Catches a refactor that splits the constant into two divergent strings."""
    src = (
        Path(__file__).resolve().parent.parent.parent / "src" / "kicad_mcp" / "connection.py"
    ).read_text(encoding="utf-8")
    match = re.search(
        r'PERSISTENCE_HINT\s*=\s*\(\s*"([^"]+)"\s*\n\s*"([^"]+)"\s*\)',
        src,
    )
    assert match is not None, "could not parse PERSISTENCE_HINT in connection.py"
    assembled = match.group(1) + match.group(2)
    assert assembled == PERSISTENCE_HINT


def test_persistence_hint_starts_with_call_pcb_save() -> None:
    """Lock the wording prefix so the assertion in integration tests
    (``'Call pcb_save() to persist' in result``) keeps matching after
    any future tweak. Mutation against the wording trips this AND every
    integration assertion in one shot."""
    assert PERSISTENCE_HINT.startswith("Call pcb_save() to persist"), (
        f"hint should lead with 'Call pcb_save() to persist'; got: {PERSISTENCE_HINT!r}"
    )


@pytest.mark.parametrize("tool_name", _IPC_MUTATING_TOOLS)
def test_ipc_mutator_references_persistence_hint(tool_name: str) -> None:
    """Every IPC mutator's body must reference ``_PERSISTENCE_HINT`` so its
    success response carries the persistence reminder. A regression that
    drops the suffix from any one tool fails this test for that tool."""
    src = _pcb_module_text()
    body = _function_body(src, tool_name)
    assert "_PERSISTENCE_HINT" in body, (
        f"{tool_name} success path must reference _PERSISTENCE_HINT — "
        f"if this tool no longer mutates the IPC board, remove it from "
        "_IPC_MUTATING_TOOLS in this test file."
    )


# Module-level helpers (NOT MCP tools) that legitimately use the hint.
# These functions mutate the IPC board too but live outside ``register()``;
# the parametrize doesn't claim them. Listing them here keeps the
# orphaned-uses guard accurate without forcing them into the MCP tool set.
_NON_TOOL_HINT_USERS = ["run_auto_refill_zones"]

# Sibling modules (outside ``tools/pcb.py``) that also expose IPC-mutating
# MCP tools and import ``PERSISTENCE_HINT`` from ``connection.py``.
# Each entry is (module_path_relative_to_src, expected_tool_names).
_SIBLING_MODULE_TOOLS: list[tuple[str, list[str]]] = [
    (
        "kicad_mcp/tools/routing.py",
        ["route_single_track", "route_from_pad_to_pad"],
    ),
    (
        "kicad_mcp/tools/power_integrity.py",
        ["pdn_generate_power_plane"],
    ),
]


def _module_text(rel_path: str) -> str:
    return (Path(__file__).resolve().parent.parent.parent / "src" / rel_path).read_text(
        encoding="utf-8"
    )


@pytest.mark.parametrize(
    ("rel_path", "tool_name"),
    [(rel_path, tool) for rel_path, tools in _SIBLING_MODULE_TOOLS for tool in tools],
)
def test_sibling_module_ipc_mutator_uses_persistence_hint(rel_path: str, tool_name: str) -> None:
    """Cross-module sweep guard. ``routing.py`` and ``power_integrity.py``
    each have IPC mutators that must carry the hint just like the
    ``pcb.py`` set, since they share the same data-loss class. Catches
    the gap Audit E found in PR #11: routing's pad-to-pad calls were
    missing the hint when the constant lived in ``pcb.py``."""
    src = _module_text(rel_path)
    body = _function_body(src, tool_name)
    assert "PERSISTENCE_HINT" in body, (
        f"{tool_name} (in {rel_path}) must reference PERSISTENCE_HINT"
    )


def test_no_unexpected_orphaned_persistence_hint_uses() -> None:
    """If someone adds a new IPC-mutating MCP tool, they must update
    _IPC_MUTATING_TOOLS. This guard counts the use sites in ``pcb.py`` and
    fails if a use appears that neither the tool list NOR the explicit
    non-tool allow-list claims, so the test list stays in sync with the
    source."""
    src = _pcb_module_text()
    references = [
        line
        for line in src.splitlines()
        if "_PERSISTENCE_HINT" in line
        and not re.match(r"^_PERSISTENCE_HINT\s*=", line)
        and not line.strip().startswith("#")
        # Skip the import line + its multi-line continuation. PR #11
        # imports the constant from connection.py rather than declaring
        # it locally, so the import shouldn't count as a use.
        and not line.strip().startswith("from")
        and "PERSISTENCE_HINT as _PERSISTENCE_HINT" not in line
    ]
    expected = len(_IPC_MUTATING_TOOLS) + len(_NON_TOOL_HINT_USERS)
    assert len(references) == expected, (
        f"expected exactly {expected} references to _PERSISTENCE_HINT "
        f"({len(_IPC_MUTATING_TOOLS)} MCP tools + "
        f"{len(_NON_TOOL_HINT_USERS)} module helpers), found "
        f"{len(references)}. If a new tool was added, update "
        "_IPC_MUTATING_TOOLS or _NON_TOOL_HINT_USERS. Lines:\n" + "\n".join(references)
    )
