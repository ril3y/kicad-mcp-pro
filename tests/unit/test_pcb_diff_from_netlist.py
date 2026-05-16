# pyright: reportPrivateUsage=false, reportUnknownLambdaType=false
# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false
"""Unit tests for the headless ``pcb_diff_from_netlist`` machinery.

The flagship piece of evidence here is the **multi-line node parser** —
the legacy ``_parse_netlist_text`` only handles the inline form
``(node (ref "X") (pin "Y"))`` and silently returns an empty map against
KiCad 10's actual tab-indented output. ``_parse_kicadsexpr_netlist``
balance-extracts each (net) and (node) block so it survives either
layout. Without this, a "headless F8" tool would happily report 'no net
changes' on every board.

The diff itself is covered by a series of synthetic
(netlist, pcb-footprints) inputs that exercise additions, removals,
footprint mismatches, and per-pad net changes in isolation.
"""

from __future__ import annotations

from typing import Any

from kicad_mcp.tools.pcb import (
    _diff_pcb_against_netlist,
    _format_pcb_netlist_diff_report,
    _parse_kicadsexpr_netlist,
)


_REAL_KICAD10_NETLIST = """\
(export (version "E")
\t(design
\t\t(source "test.kicad_sch"))
\t(components
\t\t(comp (ref "R1")
\t\t\t(value "10k")
\t\t\t(footprint "Resistor_SMD:R_0603_1608Metric"))
\t\t(comp (ref "U2")
\t\t\t(value "NE556N")
\t\t\t(footprint "Package_DIP:DIP-14_W7.62mm")))
\t(nets
\t\t(net (code "1") (name "/GND_RTN")
\t\t\t(node (ref "R1") (pin "1") (pinfunction "P1") (pintype "passive"))
\t\t\t(node (ref "U2") (pin "7") (pinfunction "GND") (pintype "power_in")))
\t\t(net (code "2") (name "/+12V_PWR")
\t\t\t(node (ref "U2") (pin "14") (pinfunction "VCC") (pintype "power_in"))
\t\t\t(node (ref "R1") (pin "2") (pinfunction "P2") (pintype "passive")))))
"""


def test_parse_kicadsexpr_netlist_handles_real_kicad10_format() -> None:
    """Pin the contract: the parser walks tab-indented multi-line node
    blocks. The legacy ``_parse_netlist_text`` regex (line-adjacent ref
    + pin) returns an empty map against this input — a regression to
    that style would silently break the diff tool."""
    components, nets = _parse_kicadsexpr_netlist(_REAL_KICAD10_NETLIST)

    assert components == {
        "R1": {"value": "10k", "footprint": "Resistor_SMD:R_0603_1608Metric"},
        "U2": {"value": "NE556N", "footprint": "Package_DIP:DIP-14_W7.62mm"},
    }
    # Sorted because dict ordering isn't a contract; the contents are.
    assert sorted(nets) == ["/+12V_PWR", "/GND_RTN"]
    assert sorted(nets["/GND_RTN"]) == [("R1", "1"), ("U2", "7")]
    assert sorted(nets["/+12V_PWR"]) == [("R1", "2"), ("U2", "14")]


def test_parse_kicadsexpr_netlist_also_handles_legacy_inline_format() -> None:
    """Backward compatibility: an older single-line form (used by the
    pre-existing test fixtures in this repo) must still parse. Locks
    that the new parser is a strict superset of the legacy one."""
    legacy = (
        "(export\n"
        "  (components\n"
        '    (comp (ref "J1") (value "Conn_01x02") (footprint "")))\n'
        "  (nets\n"
        '    (net (code "1") (name "USB_DP")\n'
        '      (node (ref "J1") (pin "A6"))\n'
        '      (node (ref "U1") (pin "12")))))\n'
    )
    components, nets = _parse_kicadsexpr_netlist(legacy)

    assert "J1" in components
    assert nets["USB_DP"] == [("J1", "A6"), ("U1", "12")]


def test_parse_kicadsexpr_netlist_skips_malformed_blocks() -> None:
    """If a (comp ...) lacks (ref ...), or a (node ...) lacks ref or pin,
    skip it silently rather than crashing. Real-world netlists from
    in-progress designs can have empty value/footprint fields, and we
    don't want the tool to fail on a half-built design."""
    text = (
        "(export\n"
        "  (components\n"
        "    (comp (value \"orphan\"))\n"  # no ref
        "    (comp (ref \"R1\") (value \"10k\") (footprint \"R_0603\")))\n"
        "  (nets\n"
        "    (net (code \"1\") (name \"NET_A\")\n"
        "      (node (ref \"R1\") (pin \"1\"))\n"
        "      (node (pin \"missing-ref\"))\n"  # node missing ref
        "      (node (ref \"X\") )                  )))\n"  # node missing pin
    )
    components, nets = _parse_kicadsexpr_netlist(text)

    assert list(components) == ["R1"]
    assert nets["NET_A"] == [("R1", "1")]


def test_diff_reports_additions_when_schematic_has_new_refs() -> None:
    nl_components = {
        "R1": {"value": "10k", "footprint": "R_0603"},
        "C1": {"value": "100nF", "footprint": "C_0603"},
    }
    pcb_footprints: dict[str, dict[str, Any]] = {
        "R1": {"name": "R_0603", "pad_nets": {"1": "/GND", "2": "/SIG"}},
    }

    diff = _diff_pcb_against_netlist(nl_components, {}, pcb_footprints)

    assert diff["additions"] == ["C1"]
    assert diff["removals"] == []


def test_diff_reports_removals_when_pcb_has_orphan_footprints() -> None:
    nl_components = {"R1": {"value": "", "footprint": ""}}
    pcb_footprints: dict[str, dict[str, Any]] = {
        "R1": {"name": "R_0603", "pad_nets": {}},
        "R_OLD": {"name": "R_0805", "pad_nets": {}},
        "C_OLD": {"name": "C_0805", "pad_nets": {}},
    }

    diff = _diff_pcb_against_netlist(nl_components, {}, pcb_footprints)

    assert diff["removals"] == ["C_OLD", "R_OLD"]


def test_diff_reports_footprint_mismatches_for_shared_refs() -> None:
    nl_components = {"R1": {"value": "10k", "footprint": "Resistor_SMD:R_0603"}}
    pcb_footprints: dict[str, dict[str, Any]] = {
        "R1": {"name": "Resistor_THT:R_Axial", "pad_nets": {}},
    }

    diff = _diff_pcb_against_netlist(nl_components, {}, pcb_footprints)

    assert diff["footprint_mismatches"] == [
        ("R1", "Resistor_THT:R_Axial", "Resistor_SMD:R_0603"),
    ]
    # No add/remove since the ref exists on both sides.
    assert diff["additions"] == []
    assert diff["removals"] == []


def test_diff_reports_net_changes_when_pad_assignments_differ() -> None:
    """Repro of the junction-passive case: existing PCB has stale
    /+12V_PWR on ground pins; the schematic netlist correctly puts them
    on /GND_RTN. The diff must surface those re-routes so apply-mode can
    fix the board without an F8 dance through pcbnew."""
    nl_components = {"J1": {"value": "Conn", "footprint": "Pin_Header_01x09"}}
    nl_nets = {
        "/GND_RTN": [("J1", "2"), ("J1", "9")],
        "/+12V_PWR": [("J1", "1")],
    }
    pcb_footprints: dict[str, dict[str, Any]] = {
        "J1": {
            "name": "Pin_Header_01x09",
            "pad_nets": {
                "1": "/+12V_PWR",  # already correct
                "2": "/+12V_PWR",  # stale — should be /GND_RTN
                "9": "",           # unassigned — should be /GND_RTN
            },
        },
    }

    diff = _diff_pcb_against_netlist(nl_components, nl_nets, pcb_footprints)

    assert diff["net_changes"] == [
        ("J1", "2", "/+12V_PWR", "/GND_RTN"),
        ("J1", "9", "", "/GND_RTN"),
    ]


def test_diff_does_not_emit_net_change_when_assignments_already_match() -> None:
    """Sanity: if every pad already has the right net, the diff is empty.
    Pins this so a future "I'll always re-emit pad nets" refactor doesn't
    cause unnecessary file churn on a clean board."""
    nl_components = {"R1": {"value": "10k", "footprint": "R_0603"}}
    nl_nets = {"/SIG": [("R1", "1")], "/GND": [("R1", "2")]}
    pcb_footprints: dict[str, dict[str, Any]] = {
        "R1": {"name": "R_0603", "pad_nets": {"1": "/SIG", "2": "/GND"}},
    }

    diff = _diff_pcb_against_netlist(nl_components, nl_nets, pcb_footprints)

    assert diff["net_changes"] == []


def test_diff_ignores_net_changes_for_refs_not_on_pcb() -> None:
    """A schematic component that's not on the PCB yet appears as an
    addition — its pad-net assignments don't generate spurious
    'net_changes' entries pointing at empty PCB-side state."""
    nl_components = {"NEW_R": {"value": "10k", "footprint": "R_0603"}}
    nl_nets = {"/SIG": [("NEW_R", "1"), ("NEW_R", "2")]}
    pcb_footprints: dict[str, dict[str, Any]] = {}

    diff = _diff_pcb_against_netlist(nl_components, nl_nets, pcb_footprints)

    assert diff["additions"] == ["NEW_R"]
    assert diff["net_changes"] == []


def test_format_diff_report_caps_long_sections_with_summary() -> None:
    """The report goes back to the agent over MCP; a giant board would
    bloat the context window. Sections are capped at 30/40 lines with
    an 'and N more' trailer. This locks that contract."""
    nl_components = {f"R{i}": {"value": "10k", "footprint": "R_0603"} for i in range(100)}
    diff = {
        "additions": sorted(nl_components),
        "removals": [],
        "footprint_mismatches": [],
        "net_changes": [(f"R{i}", "1", "/old", "/new") for i in range(60)],
    }

    report = _format_pcb_netlist_diff_report(diff, nl_components)

    assert "Add to PCB: 100 footprint(s)" in report
    assert "and 70 more" in report  # 100 - 30 cap
    assert "Net changes on existing pads: 60" in report
    assert "and 20 more" in report  # 60 - 40 cap
    assert "+ R0" in report  # first one rendered
    # R99 should NOT be rendered (over the cap); R29 (sorted as 'R29') should be
    assert "+ R29" in report
