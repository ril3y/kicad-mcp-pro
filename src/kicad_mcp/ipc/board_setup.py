"""Board stackup, enabled layers and design-rule constraints through KiCad's API.

These use KiCad's own commands on the open board (GUI or headless server), not
text edits of the ``.kicad_pcb`` file.
"""

from __future__ import annotations

from typing import Any

from ._master_client import ApiError, MasterKiCadClient

# Fabricator stackups. Thicknesses in mm, top to bottom, copper and dielectric
# alternating; the dielectric entries are (thickness, relative permittivity, material).
STACKUP_PRESETS: dict[str, dict[str, Any]] = {
    "jlcpcb-4-7628": {
        "description": "JLCPCB JLC04161H-7628, 4 layers, 1.6 mm, 1 oz outer / 0.5 oz inner",
        "copper_mm": [0.035, 0.0152, 0.0152, 0.035],
        "dielectrics": [
            (0.2104, 4.4, "7628 prepreg"),
            (1.065, 4.6, "FR-4 core"),
            (0.2104, 4.4, "7628 prepreg"),
        ],
    },
    "jlcpcb-2": {
        "description": "JLCPCB 2 layers, 1.6 mm, 1 oz",
        "copper_mm": [0.035, 0.035],
        "dielectrics": [(1.5, 4.6, "FR-4 core")],
    },
}

# Minimum constraints in mm. Conservative values inside the limits the fabricator
# publishes for the board type; a tighter design needs the fabricator's current table.
RULE_PRESETS: dict[str, dict[str, Any]] = {
    "jlcpcb-multilayer": {
        "description": "JLCPCB 4-6 layer boards, 1 oz, conservative",
        "min_clearance": 0.127,
        "min_track_width": 0.127,
        "min_connection_width": 0.127,
        "min_via_annular_width": 0.13,
        "min_via_size": 0.45,
        "min_through_drill": 0.2,
        "copper_edge_clearance": 0.3,
        "hole_clearance": 0.2,
        "hole_to_hole_min": 0.25,
        "min_silk_text_height": 0.8,
        "min_silk_text_thickness": 0.15,
    },
    "jlcpcb-2-layer": {
        "description": "JLCPCB 1-2 layer boards, 1 oz, conservative",
        "min_clearance": 0.127,
        "min_track_width": 0.127,
        "min_connection_width": 0.127,
        "min_via_annular_width": 0.15,
        "min_via_size": 0.6,
        "min_through_drill": 0.3,
        "copper_edge_clearance": 0.3,
        "hole_clearance": 0.2,
        "hole_to_hole_min": 0.25,
        "min_silk_text_height": 0.8,
        "min_silk_text_thickness": 0.15,
    },
}


def _nm(mm: float) -> int:
    return int(round(mm * 1_000_000))


def _board_document(client: MasterKiCadClient) -> Any:  # noqa: ANN401
    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        GetOpenDocuments,
        GetOpenDocumentsResponse,
    )
    from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType

    request = GetOpenDocuments()
    request.type = DocumentType.DOCTYPE_PCB
    documents = list(client.send(request, GetOpenDocumentsResponse).documents)
    if not documents:
        raise RuntimeError("No board is open in KiCad.")
    return documents[0]


def set_stackup(preset: str, client: MasterKiCadClient | None = None) -> list[str]:
    """Enable the preset's copper layers and write its thicknesses and materials.

    Returns one description line per stackup layer as KiCad reports it afterwards.
    """
    from kicad_mcp._master_proto.mp.board import board_commands_pb2 as commands
    from kicad_mcp._master_proto.mp.board import board_pb2, board_types_pb2

    if preset not in STACKUP_PRESETS:
        raise ValueError(f"Unknown stackup {preset!r}. Known: {', '.join(STACKUP_PRESETS)}.")
    spec = STACKUP_PRESETS[preset]
    copper: list[float] = spec["copper_mm"]
    dielectrics: list[tuple[float, float, str]] = spec["dielectrics"]
    client = client or MasterKiCadClient()
    document = _board_document(client)

    get_layers = commands.GetBoardEnabledLayers()
    get_layers.board.CopyFrom(document)
    enabled = client.send(get_layers, commands.BoardEnabledLayersResponse)
    inner = [getattr(board_types_pb2, f"BL_In{index}_Cu") for index in range(1, len(copper) - 1)]
    all_inner = {
        value for name, value in board_types_pb2.BoardLayer.items() if name.startswith("BL_In")
    }
    layers = [layer for layer in enabled.layers if layer not in all_inner] + inner
    set_layers = commands.SetBoardEnabledLayers()
    set_layers.board.CopyFrom(document)
    set_layers.copper_layer_count = len(copper)
    set_layers.layers.extend(layers)
    client.send(set_layers, commands.BoardEnabledLayersResponse)

    get_stackup = commands.GetBoardStackup()
    get_stackup.board.CopyFrom(document)
    stackup = client.send(get_stackup, commands.BoardStackupResponse).stackup
    copper_seen = 0
    dielectric_seen = 0
    for layer in stackup.layers:
        if layer.type == board_pb2.BSLT_COPPER:
            if copper_seen < len(copper):
                layer.thickness.value_nm = _nm(copper[copper_seen])
            copper_seen += 1
        elif layer.type == board_pb2.BSLT_DIELECTRIC:
            if dielectric_seen < len(dielectrics):
                thickness, epsilon, material = dielectrics[dielectric_seen]
                layer.thickness.value_nm = _nm(thickness)
                layer.material_name = material
                if not layer.dielectric.layer:
                    layer.dielectric.layer.add()
                for sub in layer.dielectric.layer:
                    sub.thickness.value_nm = _nm(thickness / len(layer.dielectric.layer))
                    sub.epsilon_r = epsilon
                    sub.material_name = material
                is_core = "core" in material.casefold()
                layer.dielectric.type = board_pb2.BSDT_CORE if is_core else board_pb2.BSDT_PREPREG
            dielectric_seen += 1
    if copper_seen != len(copper) or dielectric_seen != len(dielectrics):
        raise RuntimeError(
            f"KiCad reports {copper_seen} copper and {dielectric_seen} dielectric layers; "
            f"the preset has {len(copper)} and {len(dielectrics)}."
        )
    update = commands.UpdateBoardStackup()
    update.board.CopyFrom(document)
    update.stackup.CopyFrom(stackup)
    thickness_note = ""
    try:
        client.send(update, commands.BoardStackupResponse)
    except ApiError as exc:
        if "no handler" not in str(exc).casefold():
            raise
        # Some KiCad 11 builds declare UpdateBoardStackup but do not serve it. The copper
        # layers are enabled either way; thicknesses then stay at KiCad's defaults.
        thickness_note = (
            "note: this KiCad build cannot write layer thicknesses over its API; the layers "
            "are enabled but thicknesses and materials below are KiCad's defaults, not the "
            "preset's. Set them in Board Setup > Physical Stackup before ordering."
        )

    after = client.send(get_stackup, commands.BoardStackupResponse).stackup
    lines: list[str] = []
    total = 0.0
    for layer in after.layers:
        kind = board_pb2.BoardStackupLayerType.Name(layer.type).removeprefix("BSLT_").lower()
        if kind not in {"copper", "dielectric"}:
            continue
        thickness = layer.thickness.value_nm / 1e6
        total += thickness
        name = board_types_pb2.BoardLayer.Name(layer.layer).removeprefix("BL_")
        detail = name if kind == "copper" else layer.material_name
        if kind == "dielectric" and layer.dielectric.layer:
            detail += f", er {layer.dielectric.layer[0].epsilon_r:g}"
        lines.append(f"{kind}: {detail}, {thickness:.4f} mm")
    lines.append(f"total: {total:.3f} mm")
    if thickness_note:
        lines.append(thickness_note)
    return lines


def set_rules(preset: str, client: MasterKiCadClient | None = None) -> list[str]:
    """Write the preset's minimum constraints into the board setup; return what was set."""
    from kicad_mcp._master_proto.mp.board import board_commands_pb2 as commands

    if preset not in RULE_PRESETS:
        raise ValueError(f"Unknown rule set {preset!r}. Known: {', '.join(RULE_PRESETS)}.")
    spec = {key: value for key, value in RULE_PRESETS[preset].items() if key != "description"}
    client = client or MasterKiCadClient()
    document = _board_document(client)

    get_rules = commands.GetBoardDesignRules()
    get_rules.board.CopyFrom(document)
    rules = client.send(get_rules, commands.BoardDesignRulesResponse).rules
    for key, value in spec.items():
        getattr(rules.constraints, key).value_nm = _nm(float(value))
    set_request = commands.SetBoardDesignRules()
    set_request.board.CopyFrom(document)
    set_request.rules.CopyFrom(rules)
    client.send(set_request, commands.BoardDesignRulesResponse)

    after = client.send(get_rules, commands.BoardDesignRulesResponse).rules.constraints
    return [f"{key}: {getattr(after, key).value_nm / 1e6:g} mm" for key in spec]
