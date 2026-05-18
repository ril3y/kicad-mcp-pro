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

from pathlib import Path
from typing import Any

import pytest

from kicad_mcp.tools.pcb import (
    _allocate_pcb_net_codes,
    _diff_pcb_against_netlist,
    _expand_kicad_lib_uri,
    _format_pcb_netlist_diff_report,
    _inject_pcb_net_table_entries,
    _parse_kicadsexpr_netlist,
    _parse_pcb_net_table,
    _run_kicad_cli_netlist_export,
    _set_pad_net_name,
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
        '    (comp (value "orphan"))\n'  # no ref
        '    (comp (ref "R1") (value "10k") (footprint "R_0603")))\n'
        "  (nets\n"
        '    (net (code "1") (name "NET_A")\n'
        '      (node (ref "R1") (pin "1"))\n'
        '      (node (pin "missing-ref"))\n'  # node missing ref
        '      (node (ref "X") )                  )))\n'  # node missing pin
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
                "9": "",  # unassigned — should be /GND_RTN
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


def test_apply_mode_writes_pad_net_rewrites_to_existing_footprints(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """The apply path must invoke ``_assign_pad_nets`` on a footprint whose
    pad-net assignments disagree with the netlist, then hand the rewritten
    block to ``_replace_board_blocks`` for atomic write. This is the
    junction-passive use case: existing footprints with stale net codes
    from a botched earlier sync get re-routed in place.
    """
    import re
    from pathlib import Path
    from types import SimpleNamespace

    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    pcb_file = project_dir / "test.kicad_pcb"
    sch_file = project_dir / "test.kicad_sch"
    output_dir = project_dir / "output"

    # Minimal .kicad_pcb with one footprint J1 whose pad 2 is currently on
    # /+12V_PWR. The netlist (synth) will say it should be /GND_RTN.
    pcb_file.write_text(
        '(kicad_pcb (version 20240108) (generator "test") (generator_version "10.0")\n'
        '\t(footprint "Test:Conn"\n'
        '\t\t(layer "F.Cu")\n'
        '\t\t(uuid "11111111-2222-3333-4444-555555555555")\n'
        "\t\t(at 50 50 0)\n"
        '\t\t(property "Reference" "J1" (at 0 -2 0) (layer "F.SilkS"))\n'
        '\t\t(property "Value" "Conn" (at 0 2 0) (layer "F.Fab"))\n'
        '\t\t(pad "1" thru_hole circle (at 0 0) (size 1.5 1.5) (drill 0.8) '
        '(layers "*.Cu" "*.Mask") (net 1 "/+12V_PWR"))\n'
        '\t\t(pad "2" thru_hole circle (at 2.54 0) (size 1.5 1.5) (drill 0.8) '
        '(layers "*.Cu" "*.Mask") (net 1 "/+12V_PWR"))\n'
        "\t)\n"
        ")\n",
        encoding="utf-8",
    )
    sch_file.write_text("(kicad_sch)\n", encoding="utf-8")
    output_dir.mkdir()

    # Synthetic netlist contents that kicad-cli would have produced
    synthetic_netlist = (
        '(export (version "E")\n'
        "\t(components\n"
        '\t\t(comp (ref "J1") (value "Conn") (footprint "Test:Conn")))\n'
        "\t(nets\n"
        '\t\t(net (code "1") (name "/+12V_PWR")\n'
        '\t\t\t(node (ref "J1") (pin "1")))\n'
        '\t\t(net (code "2") (name "/GND_RTN")\n'
        '\t\t\t(node (ref "J1") (pin "2")))))\n'
    )

    fake_cfg = SimpleNamespace(
        sch_file=sch_file,
        pcb_file=pcb_file,
        project_dir=project_dir,
        output_dir=output_dir,
        kicad_cli=Path("kicad-cli-stub"),
        cli_timeout=30,
        footprint_library_dir=None,
        ensure_output_dir=lambda subdir=None: (
            (output_dir / subdir if subdir else output_dir).resolve()
            if False
            else _ensure_subdir(output_dir, subdir)
        ),
    )

    def _ensure_subdir(base: Path, subdir: str | None) -> Path:
        target = base / subdir if subdir else base
        target.mkdir(parents=True, exist_ok=True)
        return target

    fake_cfg.ensure_output_dir = lambda subdir=None: _ensure_subdir(output_dir, subdir)

    # Stub out the kicad-cli invocation: write the synthetic netlist where
    # the tool expects it, return success.
    def fake_run(_sch: Path, out: Path) -> tuple[int, str]:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(synthetic_netlist, encoding="utf-8")
        return 0, ""

    monkeypatch.setattr("kicad_mcp.tools.pcb.get_config", lambda: fake_cfg)
    monkeypatch.setattr("kicad_mcp.tools.pcb._run_kicad_cli_netlist_export", fake_run)
    # Make pcb path resolution use our fake cfg
    monkeypatch.setattr("kicad_mcp.tools.pcb._get_pcb_file_for_sync", lambda: pcb_file)

    # Apply mode
    import asyncio

    server = build_server("full")
    result_text = asyncio.run(call_tool_text(server, "pcb_diff_from_netlist", {"apply": True}))

    assert "Headless F8 apply summary" in result_text
    assert "Existing footprints with pad-net rewrites: 1" in result_text
    assert "J1: 2->/GND_RTN" in result_text

    # The .kicad_pcb on disk should now have pad 2 on /GND_RTN — and
    # critically should NOT also retain the original /+12V_PWR clause
    # on pad 2. The pre-fix bug appended a bare-name clause alongside
    # the original integer-coded clause, producing two contradictory
    # (net ...) entries on the same pad.
    from kicad_mcp.utils.sexpr import _extract_block

    updated = pcb_file.read_text(encoding="utf-8")

    def _extract_pad(text: str, pad_number: str) -> str:
        match = re.search(rf'\(pad\s+"{re.escape(pad_number)}"', text)
        assert match is not None, f"pad {pad_number} not found in updated PCB"
        block, _ = _extract_block(text, match.start())
        return block

    pad1 = _extract_pad(updated, "1")
    pad2 = _extract_pad(updated, "2")

    # Pad 2 was rewritten: only /GND_RTN, no stale /+12V_PWR.
    assert "/GND_RTN" in pad2
    assert "/+12V_PWR" not in pad2, (
        "stale /+12V_PWR clause must be replaced, not appended-alongside"
    )
    assert pad2.count("(net ") == 1, "pad 2 must have exactly one (net ...) clause"

    # Pad 1 stays on /+12V_PWR untouched.
    assert "/+12V_PWR" in pad1
    assert "/GND_RTN" not in pad1
    assert pad1.count("(net ") == 1


def test_set_pad_net_name_replaces_integer_coded_clause_without_appending() -> None:
    """P0 repro from PR #20 audit: the pre-fix regex only matched
    ``(net "X")`` and silently appended a second clause when the real
    pad had ``(net 1 "X")``. Pin that the rewrite now produces exactly
    one (net ...) clause across all four input shapes."""
    int_coded = '(pad "1" smd circle (at 0 0) (size 1 1) (layers "F.Cu") (net 1 "/OLD"))'
    result = _set_pad_net_name(int_coded, "/NEW")
    assert result.count("(net ") == 1
    assert "/OLD" not in result
    assert '(net 1 "/NEW")' in result, "integer code must be preserved"


def test_set_pad_net_name_emits_canonical_form_when_code_supplied() -> None:
    """Apply-mode passes a freshly-allocated net_code; the rewrite must
    emit (net N "name") form so the pad references the same integer the
    top-level net table uses. Without this, pcbnew loads the pad as
    net 0 regardless of the name string (the kicad-pcb-expert P0)."""
    bare = '(pad "1" smd circle (at 0 0) (size 1 1) (layers "F.Cu") (net "/OLD"))'
    upgraded = _set_pad_net_name(bare, "/NEW", net_code=42)
    assert '(net 42 "/NEW")' in upgraded
    assert "/OLD" not in upgraded
    assert upgraded.count("(net ") == 1


def test_parse_pcb_net_table_returns_name_to_code_map_from_top_level_entries() -> None:
    """``_parse_pcb_net_table`` must extract ONLY the top-level
    ``(net N "name")`` entries; pad-level clauses (one tab deeper) must
    be ignored, otherwise pad-side stale clauses would pollute the
    allocator's "what codes are taken" view."""
    pcb_text = (
        "(kicad_pcb (version 20240108)\n"
        '\t(net 0 "")\n'
        '\t(net 1 "/+12V_PWR")\n'
        '\t(net 12 "/GND_RTN")\n'
        '\t(footprint "Test:R"\n'
        '\t\t(pad "1" smd circle (at 0 0) (size 1 1) (layers "F.Cu") (net 99 "/STALE_PAD_LEVEL"))\n'
        "\t)\n"
        ")\n"
    )
    table = _parse_pcb_net_table(pcb_text)
    assert table == {"": 0, "/+12V_PWR": 1, "/GND_RTN": 12}
    assert "/STALE_PAD_LEVEL" not in table, "pad-level (net ...) must not bleed into the table"


def test_allocate_pcb_net_codes_assigns_next_free_integer() -> None:
    """New net names get codes one past the current max; existing codes
    pass through unchanged. Allocations are sorted by name for
    deterministic diff output."""
    existing = {"": 0, "/GND": 1, "/+12V": 5}
    combined, new_entries = _allocate_pcb_net_codes(existing, {"/GND", "/SIG_A", "/SIG_B"})
    assert combined == {"": 0, "/GND": 1, "/+12V": 5, "/SIG_A": 6, "/SIG_B": 7}
    assert new_entries == [(6, "/SIG_A"), (7, "/SIG_B")]


def test_allocate_pcb_net_codes_handles_empty_existing_table() -> None:
    """Boards with zero top-level entries (e.g. fresh from
    pcb_sync_from_schematic before this fix) start the allocator at 1."""
    combined, new_entries = _allocate_pcb_net_codes({}, {"/NET_A", "/NET_B"})
    assert combined == {"/NET_A": 1, "/NET_B": 2}
    assert new_entries == [(1, "/NET_A"), (2, "/NET_B")]


def test_inject_pcb_net_table_entries_appends_after_existing_table() -> None:
    """New ``(net N "name")`` lines slot after the last existing entry —
    preserving net-table contiguity that pcbnew tooling depends on."""
    pcb_text = (
        "(kicad_pcb (version 20240108)\n"
        '\t(net 0 "")\n'
        '\t(net 1 "/EXISTING")\n'
        '\t(footprint "Test:R"\n'
        "\t)\n"
        ")\n"
    )
    updated = _inject_pcb_net_table_entries(pcb_text, [(2, "/NEW")])
    assert '(net 2 "/NEW")' in updated
    # Must appear AFTER (net 1 "/EXISTING"), BEFORE (footprint ...).
    assert updated.index('(net 2 "/NEW")') > updated.index('(net 1 "/EXISTING")')
    assert updated.index('(net 2 "/NEW")') < updated.index("(footprint")


def test_inject_pcb_net_table_entries_inserts_block_when_no_existing_table() -> None:
    """Boards with zero top-level (net ...) entries (e.g. an early-stage
    file from this fork) need the block injected right after (setup ...)
    so KiCad's loader sees nets defined before footprints reference them."""
    pcb_text = (
        "(kicad_pcb (version 20240108)\n"
        "\t(general (thickness 1.6))\n"
        "\t(setup (pad_to_mask_clearance 0))\n"
        '\t(footprint "Test:R"\n'
        "\t)\n"
        ")\n"
    )
    updated = _inject_pcb_net_table_entries(pcb_text, [(1, "/FIRST"), (2, "/SECOND")])
    assert '(net 1 "/FIRST")' in updated
    assert '(net 2 "/SECOND")' in updated
    # Both go after setup, before footprint.
    assert updated.index('(net 1 "/FIRST")') > updated.index("(setup")
    assert updated.index('(net 2 "/SECOND")') < updated.index("(footprint")


def test_expand_kicad_lib_uri_substitutes_user_vars_and_leaves_unknowns_intact(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Direct unit test for the URI expander — pinned because every
    headless library lookup runs through it. A regression that gated
    user-vars on KIPRJMOD being present would pass every other test."""
    from pathlib import Path

    monkeypatch.delenv("EASYEDA2KICAD", raising=False)
    monkeypatch.setattr(
        "kicad_mcp.tools.pcb.find_kicad_user_env_vars",
        lambda: {"EASYEDA2KICAD": "/p/external", "MY_LIBS": "/p/mylibs"},
    )

    result = _expand_kicad_lib_uri(
        "${KIPRJMOD}/${EASYEDA2KICAD}/${MY_LIBS}/${UNKNOWN}/footprint.kicad_mod",
        Path("/proj"),
    )
    # KIPRJMOD + both user vars expanded; ${UNKNOWN} survives so the
    # caller's .exists() probe will fail visibly.
    assert "/p/external" in result
    assert "/p/mylibs" in result
    assert "${UNKNOWN}" in result
    assert "${KIPRJMOD}" not in result
    assert "${EASYEDA2KICAD}" not in result


def test_expand_kicad_lib_uri_os_env_overrides_kicad_config() -> None:
    """Precedence: process env > kicad_common.json (matches KiCad GUI
    behavior per env_paths.h). A CI runner exporting a var in shell
    overrides whatever the developer's config has set locally."""
    import os
    from pathlib import Path

    os.environ["TEST_LIB_PATH_OVERRIDE_4216"] = "/from/os/env"
    try:
        result = _expand_kicad_lib_uri(
            "${TEST_LIB_PATH_OVERRIDE_4216}/foo.kicad_mod",
            Path("/proj"),
        )
        assert result == "/from/os/env/foo.kicad_mod"
    finally:
        del os.environ["TEST_LIB_PATH_OVERRIDE_4216"]


def test_run_kicad_cli_netlist_export_invokes_correct_argv(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Pin the kicad-cli command line so a typo (``kicadeeschema`` vs
    ``kicadsexpr``, missing --format flag, swapped --output) doesn't
    slip through. Test-sufficiency audit flagged this as the
    highest-risk gap: every other test stubs ``_run_kicad_cli_*`` so
    the real argv was untested."""
    import subprocess as sp
    from pathlib import Path
    from types import SimpleNamespace

    captured: list[list[str]] = []

    def fake_run(argv: list[str], **kwargs: Any) -> Any:  # noqa: ANN401
        captured.append(argv)
        # Write a minimal valid netlist so the success path is reached.
        out_idx = argv.index("--output")
        out_path = Path(argv[out_idx + 1])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text('(export (version "E"))\n', encoding="utf-8")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    # The function gates on cfg.kicad_cli.exists(); point at a real file
    # in tmp_path so the binary-availability check passes without needing
    # a real kicad-cli on the test box.
    stub_cli = tmp_path / "kicad-cli-stub"
    stub_cli.write_bytes(b"")
    monkeypatch.setattr(
        "kicad_mcp.tools.pcb.get_config",
        lambda: SimpleNamespace(
            kicad_cli=stub_cli,
            cli_timeout=30,
        ),
    )
    monkeypatch.setattr(sp, "run", fake_run)

    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)\n", encoding="utf-8")
    out = tmp_path / "out" / "netlist.net"
    code, msg = _run_kicad_cli_netlist_export(sch, out)

    assert code == 0
    assert len(captured) == 1, "first variant should succeed without fallback"
    argv = captured[0]
    assert argv[1:5] == ["sch", "export", "netlist", "--format"]
    assert "kicadsexpr" in argv
    assert "--output" in argv
    assert str(out) in argv
    assert str(sch) in argv


def test_run_kicad_cli_netlist_export_falls_back_to_input_form_on_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Older kicad-cli builds (9.0 transition) required ``--input``;
    newer ones take the positional. Without this fallback a partial-
    refresh CI environment with a stale CLI would silently fail."""
    import subprocess as sp
    from pathlib import Path
    from types import SimpleNamespace

    call_count = {"n": 0}

    def fake_run(argv: list[str], **kwargs: Any) -> Any:  # noqa: ANN401
        call_count["n"] += 1
        if call_count["n"] == 1:
            # First variant: positional input. Pretend the CLI rejects it.
            return SimpleNamespace(returncode=2, stdout="", stderr="unknown positional")
        # Second variant: --input form. Succeed and write output.
        out_idx = argv.index("--output")
        Path(argv[out_idx + 1]).parent.mkdir(parents=True, exist_ok=True)
        Path(argv[out_idx + 1]).write_text("(export)\n", encoding="utf-8")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    # The function gates on cfg.kicad_cli.exists(); point at a real file
    # in tmp_path so the binary-availability check passes without needing
    # a real kicad-cli on the test box.
    stub_cli = tmp_path / "kicad-cli-stub"
    stub_cli.write_bytes(b"")
    monkeypatch.setattr(
        "kicad_mcp.tools.pcb.get_config",
        lambda: SimpleNamespace(
            kicad_cli=stub_cli,
            cli_timeout=30,
        ),
    )
    monkeypatch.setattr(sp, "run", fake_run)

    sch = tmp_path / "demo.kicad_sch"
    sch.write_text("(kicad_sch)\n", encoding="utf-8")
    out = tmp_path / "out" / "netlist.net"
    code, _ = _run_kicad_cli_netlist_export(sch, out)

    assert code == 0
    assert call_count["n"] == 2, "second variant must be tried when first fails"


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
