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

    only = await call_tool_text(server, "run_drc", {"types": ["silk_overlap"]})
    assert "silk_overlap x2" in only and "Footprint R10" in only
    assert "clearance x1" not in only and "Unrouted connections" not in only


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
    # A second reload must still reach the server the client talks to, not the copy
    # built by the first reload.
    import sys
    reloaded = text(await server.call_tool("dev_reload_tools", {}))
    assert "Reloaded." in reloaded, reloaded
    live_fn = server._tool_manager._tools["sch_draw"].fn
    current = sys.modules["kicad_mcp.tools.schematic"]
    assert live_fn.__globals__ is current.__dict__, "second reload left stale tools in place"
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


@pytest.mark.anyio
async def test_lib_set_pin_types_sets_many_and_refuses_bad_input(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    library = sample_project / "parts.kicad_sym"
    library.write_text(LIBRARY, encoding="utf-8")
    monkeypatch.setattr(
        "kicad_mcp.tools.library.validate_via_kicad_cli", lambda text, cli, **kw: (True, "")
    )
    server = build_server("full")
    args = {"symbol_name": "BASE", "library_path": str(library)}

    bad_type = await call_tool_text(
        server, "lib_set_pin_types", {**args, "pin_types": {"4": "sideways"}}
    )
    bad_pin = await call_tool_text(
        server, "lib_set_pin_types", {**args, "pin_types": {"9": "input"}}
    )
    done = await call_tool_text(
        server, "lib_set_pin_types", {**args, "pin_types": {"4": "output", "8": "power_in"}}
    )

    assert "Unknown pin type(s): sideways" in bad_type
    assert "No such pin(s) on 'BASE': 9" in bad_pin
    assert "Set the type of 1 pin(s)" in done
    pins = symbol_library.symbol_pins(
        symbol_library.symbol_block(library.read_text(encoding="utf-8"), "BASE") or ""
    )
    assert [(pin["number"], pin["type"]) for pin in pins] == [("4", "output"), ("8", "power_in")]


class _Point:
    def __init__(self, x_mm: float, y_mm: float) -> None:
        self.x, self.y = int(x_mm * 1e6), int(y_mm * 1e6)


class _Thing:
    def __init__(self, ident: str, *points: tuple[float, float]) -> None:
        self.id = ident
        self.start = self.position = _Point(*points[0])
        self.end = _Point(*points[-1])


@pytest.mark.anyio
async def test_block_tools_take_only_what_lies_inside(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """pcb_move_block and pcb_delete_block_copper act on a rectangle of layout."""
    from contextlib import contextmanager

    from kicad_mcp.tools import pcb

    class Board:
        def __init__(self) -> None:
            self.updated: list[object] = []
            self.removed: list[object] = []
            self.footprints = [_Thing("fp-in", (60, 60)), _Thing("fp-out", (110, 80))]
            self.tracks = [_Thing("t-in", (56, 56), (62, 56)), _Thing("t-half", (62, 56), (90, 56))]
            self.vias = [_Thing("v-in", (58, 58))]

        def get_footprints(self) -> list[_Thing]:
            return self.footprints

        def get_tracks(self) -> list[_Thing]:
            return self.tracks

        def get_vias(self) -> list[_Thing]:
            return self.vias

        def get_zones(self) -> list[_Thing]:
            return []

        def update_items(self, items: list[object]) -> None:
            self.updated = list(items)

        def remove_items_by_id(self, ids: list[object]) -> None:
            self.removed = list(ids)

    board = Board()

    @contextmanager
    def transaction():  # noqa: ANN202
        yield board

    monkeypatch.setattr(pcb, "get_board", lambda: board)
    monkeypatch.setattr(pcb, "board_transaction", transaction)
    server = build_server("full")
    box = {"x1_mm": 54, "y1_mm": 54, "x2_mm": 72, "y2_mm": 71}

    moved = await call_tool_text(server, "pcb_move_block", {**box, "dx_mm": 50, "dy_mm": 40})
    assert "Moved 1 footprints, 1 tracks, 1 vias, 0 zones" in moved
    assert {item.id for item in board.updated} == {"fp-in", "t-in", "v-in"}

    class _Field:
        def __init__(self, value: str) -> None:
            self.text = type("T", (), {"value": value})()

    board.footprints[0].reference_field = _Field("U5")
    board.footprints[1].reference_field = _Field("R1")
    gone = await call_tool_text(server, "pcb_delete_footprints", {"references": ["U5", "X9"]})
    assert "Deleted U5. Not on the board: X9." in gone
    assert board.removed == ["fp-in"]

    box = {"x1_mm": 104, "y1_mm": 94, "x2_mm": 122, "y2_mm": 111}
    deleted = await call_tool_text(server, "pcb_delete_block_copper", box)
    assert "Deleted 1 tracks, 1 vias, 0 zones" in deleted
    assert set(board.removed) == {"t-in", "v-in"}


def test_only_parentless_headless_servers_count_as_orphans() -> None:
    from kicad_mcp.ipc import headless

    listing = """
  100     1 /K/kicad-cli api-server --socket /tmp/kmcp-old1/board.sock /p/a.kicad_pcb
  101   900 /K/kicad-cli api-server --socket /tmp/kmcp-live/board.sock /p/a.kicad_pcb
  102     1 /K/kicad /p/a.kicad_pro
  103     1 /usr/bin/python other --socket /tmp/kmcp-x/board.sock
"""
    expected = Path("/tmp/kmcp-old1")  # noqa: S108 - a path in test text, nothing is created
    assert headless.orphaned_servers(listing) == [(100, expected)]


@pytest.mark.anyio
async def test_lib_number_footprint_pads_numbers_only_the_unnumbered(sample_project: Path) -> None:
    folder = sample_project / "libs" / "Parts.pretty"
    folder.mkdir(parents=True)
    footprint = folder / "QFN.kicad_mod"
    footprint.write_text(
        '(footprint "QFN" (pad "" thru_hole circle (at 0 0)) (pad "37" smd rect (at 0 0)))',
        encoding="utf-8",
    )
    server = build_server("full")
    args = {"library": "Parts", "footprint": "QFN", "number": "37"}

    first = await call_tool_text(server, "lib_number_footprint_pads", args)
    again = await call_tool_text(server, "lib_number_footprint_pads", args)

    assert "Numbered 1 pad(s)" in first
    assert footprint.read_text(encoding="utf-8").count('(pad "37"') == 2
    assert "no unnumbered pads" in again


def test_parse_ses_gives_tracks_and_vias_in_board_millimetres() -> None:
    from kicad_mcp.utils.freerouting import parse_ses

    ses = """(session board.ses (base_design board.dsn)
      (routes (resolution um 10)
        (library_out (padstack "Via[0-3]_600:300_um"))
        (network_out
          (net "/LED_EN"
            (wire (path F.Cu 2000 1040000 -850000 1060000 -850000 1060000 -870000))
            (via "Via[0-3]_600:300_um" 1060000 -870000))
          (net GND (wire (path B.Cu 5000 0 0 10000 0))))))"""
    tracks, vias = parse_ses(ses)

    assert tracks[0] == {
        "net": "/LED_EN", "layer": "F.Cu", "width": 0.2,
        "x1": 104.0, "y1": 85.0, "x2": 106.0, "y2": 85.0,
    }  # fmt: skip
    assert (tracks[1]["x2"], tracks[1]["y2"]) == (106.0, 87.0)
    assert tracks[2]["net"] == "GND" and tracks[2]["width"] == 0.5
    assert vias == [{"net": "/LED_EN", "x": 106.0, "y": 87.0, "diameter": 0.6, "drill": 0.3}]
