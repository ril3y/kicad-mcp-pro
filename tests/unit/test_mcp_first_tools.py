"""Tools that replace one-off scripts: symbol pins, grouped checks, reload."""

from __future__ import annotations

from pathlib import Path

import pytest

from kicad_mcp.server import build_server
from kicad_mcp.tools import dev, validation
from kicad_mcp.utils import symbol_library
from tests.conftest import call_tool_text

LIBRARY = """(kicad_symbol_lib
\t(symbol "BASE"
\t\t(property "Description" "Base part")
\t\t(property "Footprint" "Lib:SOIC")
\t\t(symbol "BASE_1_1"
\t\t\t(pin power_in line
\t\t\t\t(at 0 5.08 270)
\t\t\t\t(length 2.54)
\t\t\t\t(name "VCC")
\t\t\t\t(number "8")
\t\t\t)
\t\t\t(pin input line
\t\t\t\t(at -5.08 0 0)
\t\t\t\t(length 2.54)
\t\t\t\t(hide yes)
\t\t\t\t(name "DI")
\t\t\t\t(number "4")
\t\t\t)
\t\t)
\t)
\t(symbol "MIDDLE"
\t\t(extends "BASE")
\t\t(property "Description" "Middle part")
\t)
\t(symbol "LEAF"
\t\t(extends "MIDDLE")
\t\t(property "Datasheet" "https://example.com/leaf.pdf")
\t)
)
"""


def test_base_chain_follows_every_link() -> None:
    assert symbol_library.base_chain(LIBRARY, "LEAF") == ["LEAF", "MIDDLE", "BASE"]
    assert symbol_library.base_chain(LIBRARY, "BASE") == ["BASE"]
    with pytest.raises(KeyError):
        symbol_library.base_chain(LIBRARY, "MISSING")


def test_symbol_pins_are_sorted_and_flag_hidden_pins() -> None:
    pins = symbol_library.symbol_pins(symbol_library.symbol_block(LIBRARY, "BASE") or "")
    assert [(pin["number"], pin["name"], pin["type"], pin["hidden"]) for pin in pins] == [
        ("4", "DI", "input", True),
        ("8", "VCC", "power_in", False),
    ]


@pytest.mark.anyio
async def test_symbol_info_and_derive_reach_the_base_symbol(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("kicad_mcp.tools.library._read_symbol_file", lambda library: LIBRARY)
    server = build_server("full")

    info = await call_tool_text(
        server, "lib_get_symbol_info", {"library": "Stock", "symbol_name": "LEAF"}
    )
    made = await call_tool_text(
        server,
        "lib_derive_part",
        {"base_library": "Stock", "base_symbol": "LEAF", "name": "MY_PART", "library": "Parts"},
    )
    mine = await call_tool_text(
        server, "lib_get_symbol_info", {"library": "Parts", "symbol_name": "MY_PART"}
    )

    assert "Derived from: MIDDLE -> BASE (base symbol: BASE)" in info
    assert "- Description: Middle part" in info
    assert "4 DI (input, hidden)" in info
    assert "base symbol BASE" in made
    assert "8 VCC (power_in)" in mine
    assert "- Description: Middle part" in mine
    assert "- Datasheet: https://example.com/leaf.pdf" in mine


def _entry(kind: str, severity: str, *items: str) -> dict[str, object]:
    return {
        "type": kind,
        "severity": severity,
        "description": f"about {kind}",
        "items": [{"description": text} for text in items],
    }


@pytest.mark.anyio
async def test_grouped_checks_show_items_and_filter_by_reference(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    drc: dict[str, object] = {
        "violations": [
            _entry("clearance", "error", "Pad 1 [GND] of C1 on F.Cu", "Track [VIN] on F.Cu"),
            _entry("silk_overlap", "warning", "Footprint R10"),
            _entry("silk_overlap", "warning", "Footprint R1"),
        ],
        "unconnected_items": [
            _entry("unconnected_items", "error", "Pad 2 [GND] of C1 on F.Cu", "Pad 9 of U2 on F.Cu")
        ],
    }
    erc: dict[str, object] = {
        "sheets": [
            {
                "path": "/Power/",
                "violations": [_entry("pin_not_driven", "error", "Symbol U1 Pin 4")],
            }
        ]
    }
    monkeypatch.setattr(validation, "_run_drc_report", lambda name: (Path("d.json"), drc, None))
    monkeypatch.setattr(validation, "_run_erc_report", lambda name: (Path("e.json"), erc, None))
    server = build_server("full")

    board = await call_tool_text(server, "run_drc", {"references": ["C1", "R1"]})
    schematic = await call_tool_text(server, "run_erc", {"group": True})
    flat = await call_tool_text(server, "run_drc", {})

    assert "Limited to C1, R1: 2 violation(s), 1 unrouted connection(s)." in board
    assert "[error] clearance x1" in board
    assert "Footprint R10" not in board  # R1 must not match R10
    assert "Pad 2 [GND] of C1 on F.Cu <-> Pad 9 of U2 on F.Cu" in board
    assert "[error] pin_not_driven x1: about pin_not_driven" in schematic
    assert "/Power/: Symbol U1 Pin 4" in schematic
    assert "- [error] about clearance" in flat


@pytest.mark.anyio
async def test_dev_tools_are_off_by_default(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("KICAD_MCP_DEV_TOOLS", raising=False)
    assert not dev.enabled()
    plain = build_server("full")
    assert not dev.TOOL_NAMES & {tool.name for tool in await plain.list_tools()}


_RELOAD_SCRIPT = """
import asyncio
from kicad_mcp.server import build_server

async def main():
    server = build_server("full")
    names = {tool.name for tool in await server.list_tools()}
    assert {"dev_reload_tools", "dev_call_tool"} <= names, "dev tools missing"
    def text(result):
        content = result[0] if isinstance(result, tuple) else result
        return " ".join(getattr(item, "text", "") for item in content)

    reloaded = text(await server.call_tool("dev_reload_tools", {}))
    assert "Reloaded." in reloaded, reloaded
    assert {tool.name for tool in await server.list_tools()} == names, "tool set changed"
    through = text(await server.call_tool(
        "dev_call_tool", {"name": "kicad_get_project_info", "arguments": {}}
    ))
    assert "Current project configuration" in through, through
    print("RELOAD-OK")

asyncio.run(main())
"""


def test_dev_tools_reload_and_call_in_a_fresh_process(tmp_path: Path) -> None:
    """Run in a subprocess: a reload swaps the server's modules, which must not leak
    into the other tests of this run."""
    import os
    import subprocess
    import sys

    env = {**os.environ, "KICAD_MCP_DEV_TOOLS": "1", "KICAD_MCP_PROJECT_DIR": str(tmp_path)}
    env.pop("KICAD_MCP_HEADLESS", None)
    done = subprocess.run(  # noqa: S603 - fixed argv
        [sys.executable, "-c", _RELOAD_SCRIPT],
        capture_output=True,
        text=True,
        timeout=180,
        env=env,
        check=False,
    )
    assert "RELOAD-OK" in done.stdout, done.stdout[-600:] + done.stderr[-1200:]
