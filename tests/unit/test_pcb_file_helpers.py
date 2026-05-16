from __future__ import annotations

import pytest

from kicad_mcp.models.pcb import AutoPlaceBySchematicInput, StackupLayerSpec
from kicad_mcp.tools.pcb import (
    _append_to_footprint_block,
    _apply_stackup_to_board,
    _copper_layer_order,
    _impedance_context_for_layer,
    _inner_layer_graphic_block,
    _matches_layer_filter_name,
    _parse_board_footprint_blocks,
    _parse_netlist_text,
    _parse_stackup_specs_from_board_text,
    _replace_or_append_child_block,
    _strategy_board_positions,
)


def _four_layer_stackup() -> list[StackupLayerSpec]:
    return [
        StackupLayerSpec(name="F.Cu", type="signal", thickness_mm=0.035, material="Copper"),
        StackupLayerSpec(
            name="dielectric_1",
            type="dielectric",
            thickness_mm=0.2,
            material="FR4",
            epsilon_r=4.2,
            loss_tangent=0.02,
        ),
        StackupLayerSpec(name="In1.Cu", type="signal", thickness_mm=0.035, material="Copper"),
        StackupLayerSpec(
            name="dielectric_2",
            type="dielectric",
            thickness_mm=0.3,
            material="FR4",
            epsilon_r=4.0,
        ),
        StackupLayerSpec(name="In2.Cu", type="signal", thickness_mm=0.035, material="Copper"),
        StackupLayerSpec(
            name="dielectric_3",
            type="dielectric",
            thickness_mm=0.2,
            material="FR4",
            epsilon_r=4.3,
        ),
        StackupLayerSpec(name="B.Cu", type="signal", thickness_mm=0.035, material="Copper"),
    ]


def test_stackup_parser_and_impedance_context_cover_outer_and_inner_layers() -> None:
    original = "(kicad_pcb\n)"
    updated = _apply_stackup_to_board(original, _four_layer_stackup())
    parsed = _parse_stackup_specs_from_board_text(updated)

    assert parsed is not None
    assert [layer.name for layer in parsed if layer.name.endswith("_Cu")] == [
        "F_Cu",
        "In1_Cu",
        "In2_Cu",
        "B_Cu",
    ]
    assert parsed[1].loss_tangent == pytest.approx(0.02)
    outer_type, outer_height, outer_er, outer_oz = _impedance_context_for_layer(parsed, "F.Cu")
    inner_type, inner_height, inner_er, _inner_oz = _impedance_context_for_layer(parsed, "In1.Cu")

    assert outer_type == "microstrip"
    assert outer_height == pytest.approx(0.2)
    assert outer_er == pytest.approx(4.2)
    assert outer_oz > 0.9
    assert inner_type == "stripline"
    assert inner_height == pytest.approx(0.25)
    assert inner_er == pytest.approx(4.1)
    assert _parse_stackup_specs_from_board_text("(kicad_pcb)") is None
    with pytest.raises(ValueError, match="was not found"):
        _impedance_context_for_layer(parsed, "In8.Cu")
    with pytest.raises(ValueError, match="not a copper"):
        _copper_layer_order("F.SilkS")


def test_pcb_child_block_replacement_and_inner_graphic_rendering() -> None:
    parent = "(setup\n\t(pad_to_mask_clearance 0)\n)"
    replaced = _replace_or_append_child_block(
        parent,
        "pad_to_mask_clearance",
        "(pad_to_mask_clearance 0.05)",
    )
    appended = _replace_or_append_child_block("(setup\n)", "stackup", "(stackup\n)")
    footprint = '(footprint "R"\n\t(property "Reference" "R1")\n)'
    with_child = _append_to_footprint_block(footprint, "\t(fp_line (start 0 0) (end 1 0))")
    rect = _inner_layer_graphic_block("rect", "In1_Cu", 0.0, 0.0, 1.0, 1.0, "", 0.1)
    text = _inner_layer_graphic_block("text", "In2_Cu", 2.0, 3.0, 0.0, 0.0, "RF", 0.1)

    assert "(pad_to_mask_clearance 0.05)" in replaced
    assert "(stackup" in appended
    assert "fp_line" in with_child
    assert "fp_rect" in rect and 'layer "In1.Cu"' in rect
    assert 'fp_text user "RF"' in text
    with pytest.raises(ValueError, match="shape_type"):
        _inner_layer_graphic_block("arc", "In1_Cu", 0.0, 0.0, 1.0, 1.0, "", 0.1)
    with pytest.raises(ValueError, match="Could not update"):
        _append_to_footprint_block("not a block", "\t(fp_line)")


def test_netlist_parser_and_non_cluster_placement_strategies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    netlist = """
    (export
      (nets
        (net (code "1") (name "USB_DP")
          (node (ref "J1") (pin "A6"))
          (node (ref "U1") (pin "12")))
        (net (code "2") (name "GND")
          (node (ref "J1") (pin "A1")))))
    """
    components = [
        {"reference": "U2", "footprint": "Resistor_SMD:R_0805"},
        {"reference": "U1", "footprint": "Resistor_SMD:R_0805"},
        {"reference": "J1", "footprint": "Connector_Generic:Conn_01x02"},
    ]
    linear_payload = AutoPlaceBySchematicInput(
        strategy="linear",
        origin_x_mm=10.0,
        origin_y_mm=20.0,
        grid_mm=1.0,
    )
    star_payload = AutoPlaceBySchematicInput(
        strategy="star",
        origin_x_mm=50.0,
        origin_y_mm=40.0,
        grid_mm=1.0,
    )
    monkeypatch.setattr(
        "kicad_mcp.tools.pcb._footprint_size_from_assignment",
        lambda _assignment: (2.0, 1.0),
    )

    linear = _strategy_board_positions(components, linear_payload, [])
    star = _strategy_board_positions(components, star_payload, [])

    assert _parse_netlist_text(netlist)[("J1", "A6")] == "USB_DP"
    assert list(linear) == ["J1", "U1", "U2"]
    assert linear["J1"][0] <= linear["U1"][0] <= linear["U2"][0]
    assert star["J1"] == (50.0, 40.0)
    assert star["U1"] != star["U2"]


def test_matches_layer_filter_name_handles_alias_forms() -> None:
    # The headless variant of the layer filter takes a layer NAME string
    # (as parsed from a .kicad_pcb block) rather than an integer enum, so
    # it has to normalise alias forms ('F.Cu' / 'F_Cu' / 'F-Cu') before
    # comparing. An empty filter matches everything; mismatched layers
    # filter out.
    assert _matches_layer_filter_name("F.Cu", "") is True
    assert _matches_layer_filter_name("F.Cu", "F_Cu") is True
    assert _matches_layer_filter_name("F.Cu", "F.Cu") is True
    assert _matches_layer_filter_name("F.Cu", "B_Cu") is False
    assert _matches_layer_filter_name("In1.Cu", "In1_Cu") is True


def test_pad_net_clause_regex_matches_both_kicad_format_versions() -> None:
    # The headless ``pcb_get_pads`` path uses this regex to extract the net
    # name from a pad block. Active KiCad 10 boards may contain EITHER
    # format depending on when the project was first written; the wire
    # harness production board uses the legacy form, the junction-passive
    # board uses the new form. The regex must handle both.
    import re

    net_pat = re.compile(r"\(net\s+(?:\d+\s+)?\"([^\"]+)\"\)")

    new_form = '(pad "1" smd rect (at 0 0) (size 1 1) (net "/GND_RTN"))'
    legacy_form = '(pad "1" smd rect (at 0 0) (size 1 1) (net 12 "/SIGNAL"))'
    no_net = '(pad "1" smd rect (at 0 0) (size 1 1))'

    new_match = net_pat.search(new_form)
    legacy_match = net_pat.search(legacy_form)
    assert new_match is not None and new_match.group(1) == "/GND_RTN"
    assert legacy_match is not None and legacy_match.group(1) == "/SIGNAL"
    assert net_pat.search(no_net) is None


def test_parse_board_footprint_blocks_extracts_pads_with_both_net_formats() -> None:
    # Validates that the block-capture parser preserves both net-clause
    # forms verbatim so the downstream pad-net regex can run against them.
    board_text = "\n".join(
        [
            "(kicad_pcb",
            "\t(version 20250216)",
            '\t(generator "pytest")',
            '\t(footprint "Resistor_SMD:R_0805"',
            '\t\t(layer "F.Cu")',
            '\t\t(uuid "1111")',
            "\t\t(at 10 20 0)",
            '\t\t(property "Reference" "R1"',
            "\t\t\t(at 0 -1.5 0)",
            "\t\t)",
            '\t\t(property "Value" "10k"',
            "\t\t\t(at 0 1.5 0)",
            "\t\t)",
            '\t\t(pad "1" smd rect (at -0.7 0) (size 1 1)',
            '\t\t\t(layers "F.Cu" "F.Mask" "F.Paste")',
            '\t\t\t(net "/GND")',
            "\t\t)",
            '\t\t(pad "2" smd rect (at 0.7 0) (size 1 1)',
            '\t\t\t(layers "F.Cu" "F.Mask" "F.Paste")',
            '\t\t\t(net 12 "/SIGNAL")',
            "\t\t)",
            "\t)",
            ")",
            "",
        ]
    )

    parsed = _parse_board_footprint_blocks(board_text)
    assert "R1" in parsed
    block = str(parsed["R1"]["block"])
    # Both net clauses survive intact in the captured block — the pad-net
    # regex used by pcb_get_pads must match either form to populate the
    # net column when reading older boards.
    assert '(net "/GND")' in block
    assert '(net 12 "/SIGNAL")' in block
    assert parsed["R1"]["value"] == "10k"
    assert parsed["R1"]["layer_name"] == "F.Cu"
