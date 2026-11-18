from __future__ import annotations

from pathlib import Path

import pytest

from kicad_mcp.server import build_server
from kicad_mcp.utils.component_search import ComponentRecord
from tests.conftest import call_tool_text


class FakeComponentClient:
    def __init__(self) -> None:
        self.parts = {
            "C123": ComponentRecord(
                source="fake",
                lcsc_code="C123",
                mpn="LM1117-3.3",
                description="LDO regulator 3.3V 1A SOT-223",
                package="SOT-223",
                stock=5000,
                price=0.12,
                is_basic=True,
                is_preferred=True,
            ),
            "C456": ComponentRecord(
                source="fake",
                lcsc_code="C456",
                mpn="LM1117-5.0",
                description="LDO regulator 5V 1A SOT-223",
                package="SOT-223",
                stock=200,
                price=0.18,
                is_basic=False,
                is_preferred=False,
            ),
            "C789": ComponentRecord(
                source="fake",
                lcsc_code="C789",
                mpn="BAT54",
                description="Schottky diode 30V 200mA SOT-23",
                package="SOT-23",
                stock=10_000,
                price=None,
                is_basic=True,
                is_preferred=False,
            ),
            "C999": ComponentRecord(
                source="fake",
                lcsc_code="C999",
                mpn="NOMARK",
                description="Mystery IC without package data",
                package="",
                stock=25,
                price=0.05,
                is_basic=True,
                is_preferred=False,
            ),
        }

    def search(
        self,
        _keyword: str,
        *,
        package: str | None = None,
        only_basic: bool = True,
        limit: int = 20,
    ) -> list[ComponentRecord]:
        results = list(self.parts.values())
        if package:
            results = [part for part in results if part.package == package]
        if only_basic:
            results = [part for part in results if part.is_basic]
        return results[:limit]

    def get_part(self, identifier: str) -> ComponentRecord | None:
        normalized = identifier.upper()
        return self.parts.get(normalized) or next(
            (part for part in self.parts.values() if part.mpn.upper() == normalized),
            None,
        )


@pytest.mark.anyio
async def test_library_symbol_footprint_and_generator_surface(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = build_server("full")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    libs = await call_tool_text(server, "lib_list_libraries", {})
    symbols = await call_tool_text(server, "lib_search_symbols", {"query": "resistor"})
    missing_symbol = await call_tool_text(
        server,
        "lib_get_symbol_info",
        {"library": "Missing", "symbol_name": "R"},
    )
    symbol_info = await call_tool_text(
        server,
        "lib_get_symbol_info",
        {"library": "Device", "symbol_name": "R"},
    )
    footprints = await call_tool_text(server, "lib_search_footprints", {"query": "0805"})
    footprint_list = await call_tool_text(
        server,
        "lib_list_footprints",
        {"library": "Resistor_SMD"},
    )
    footprint_info = await call_tool_text(
        server,
        "lib_get_footprint_info",
        {"library": "Resistor_SMD", "footprint": "R_0805"},
    )
    model = await call_tool_text(
        server,
        "lib_get_footprint_3d_model",
        {"library": "Resistor_SMD", "footprint": "R_0805"},
    )
    missing_model = await call_tool_text(
        server,
        "lib_get_footprint_3d_model",
        {"library": "Resistor_SMD", "footprint": "missing"},
    )
    datasheet = await call_tool_text(
        server,
        "lib_get_datasheet_url",
        {"library": "Device", "symbol_name": "R"},
    )
    custom = await call_tool_text(
        server,
        "lib_create_custom_symbol",
        {"name": "My IC", "pins": [{"number": "1", "name": "IN"}]},
    )
    footprint_gen = await call_tool_text(
        server,
        "lib_generate_footprint_ipc7351",
        {"package": "0805", "density": "B", "output_path": "generated/R.kicad_mod"},
    )
    footprint_bad_density = await call_tool_text(
        server,
        "lib_generate_footprint_ipc7351",
        {"package": "0805", "density": "Z"},
    )
    symbol_bad_pin = await call_tool_text(
        server,
        "lib_generate_symbol_from_pintable",
        {"name": "Broken", "pins": [{"name": "NO_NUMBER"}]},
    )
    symbol_gen = await call_tool_text(
        server,
        "lib_generate_symbol_from_pintable",
        {
            "name": "Generated IC",
            "pins": [{"number": "1", "name": "GPIO", "side": "right"}],
            "output_path": "generated/generated.kicad_sym",
        },
    )

    monkeypatch.setattr("kicad_mcp.tools.library.update_symbol_property", lambda *_args: None)
    assigned = await call_tool_text(
        server,
        "lib_assign_footprint",
        {"reference": "R1", "library": "Resistor_SMD", "footprint": "R_0805"},
    )
    lcsc = await call_tool_text(
        server,
        "lib_assign_lcsc_to_symbol",
        {"reference": "R1", "lcsc_code": "lcsc-c123"},
    )

    assert "Symbol libraries" in libs
    assert "Device:R" in symbols
    assert "was not found" in missing_symbol
    assert "Symbol: Device:R" in symbol_info
    assert "Pins: 2" in symbol_info
    assert "Resistor_SMD:R_0805" in footprints
    assert "R_0805" in footprint_list
    assert "Footprint: Resistor_SMD:R_0805" in footprint_info
    assert "R_0805.wrl" in model
    assert "was not found" in missing_model
    assert "https://example.com/r.pdf" in datasheet
    assert "Created custom symbol" in custom
    assert "Footprint saved" in footprint_gen
    assert "Invalid density" in footprint_bad_density
    assert "Invalid pin specification" in symbol_bad_pin
    assert "Symbol saved" in symbol_gen
    assert "Assigned footprint" in assigned
    assert "C123" in lcsc


@pytest.mark.anyio
async def test_library_live_component_surface(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = build_server("full")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})
    monkeypatch.setattr(
        "kicad_mcp.tools.library._component_search_client",
        lambda _src: FakeComponentClient(),
    )
    monkeypatch.setattr("kicad_mcp.tools.library.update_symbol_property", lambda *_args: None)
    monkeypatch.setattr(
        "kicad_mcp.tools.library._schematic_component_rows",
        lambda: [
            {
                "reference": "U1",
                "value": "LM1117-3.3",
                "footprint": "Package_TO_SOT_SMD:SOT-223",
                "lib_id": "Regulator_Linear:LM1117",
                "lcsc": "C123",
            },
            {
                "reference": "D1",
                "value": "BAT54",
                "footprint": "Package_TO_SOT_SMD:SOT-23",
                "lib_id": "Diode:BAT54",
                "lcsc": "",
            },
        ],
    )

    search = await call_tool_text(
        server,
        "lib_search_components",
        {"keyword": "LDO", "source": "jlcsearch", "sort_by": "stock"},
    )
    below_stock = await call_tool_text(
        server,
        "lib_search_components",
        {"keyword": "LDO", "source": "jlcsearch", "min_stock": 1_000_000},
    )
    details = await call_tool_text(
        server,
        "lib_get_component_details",
        {"lcsc_code_or_mpn": "C123"},
    )
    missing = await call_tool_text(
        server,
        "lib_get_component_details",
        {"lcsc_code_or_mpn": "missing"},
    )
    bom = await call_tool_text(server, "lib_get_bom_with_pricing", {"quantity": 3})
    bad_qty = await call_tool_text(server, "lib_get_bom_with_pricing", {"quantity": 0})
    stock = await call_tool_text(server, "lib_check_stock_availability", {"refs": ["U1", "D1"]})
    no_refs = await call_tool_text(server, "lib_check_stock_availability", {"refs": []})
    alternatives = await call_tool_text(
        server,
        "lib_find_alternative_parts",
        {"lcsc_code": "C123", "tolerance_percent": 100.0},
    )
    no_base = await call_tool_text(
        server,
        "lib_find_alternative_parts",
        {"lcsc_code": "missing"},
    )
    recommend = await call_tool_text(
        server,
        "lib_recommend_part",
        {"category": "LDO", "requirements": {"current_a": 1.0}, "only_basic": False},
    )
    bind = await call_tool_text(
        server,
        "lib_bind_part_to_symbol",
        {"sym_ref": "U1", "lcsc_code_or_mpn": "C123"},
    )

    assert "Live component matches" in search
    assert "C123" in search
    assert "below min_stock=1000000" in below_stock
    assert "Matches exist" in below_stock
    assert "Component details" in details
    assert "LM1117-3.3" in details
    assert "No component details" in missing
    assert "Live BOM with pricing" in bom
    assert "Estimated total" in bom
    assert "D1" in bom
    assert "value-only matching disabled" in bom
    assert "Quantity must be at least 1" in bad_qty
    assert "Stock availability" in stock
    assert "U1: C123" in stock
    assert "D1: unresolved" in stock
    assert "No references were supplied" in no_refs
    assert "Alternative parts for C123" in alternatives
    assert "No base component details" in no_base
    assert "Part recommendations" in recommend
    assert "Bound 'C123' to U1" in bind


@pytest.mark.anyio
async def test_library_live_component_edge_cases(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = build_server("full")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})
    monkeypatch.setattr(
        "kicad_mcp.tools.library._component_search_client",
        lambda _src: FakeComponentClient(),
    )

    updates: list[tuple[str, str, str]] = []

    def record_update(reference: str, field: str, value: str) -> None:
        updates.append((reference, field, value))

    monkeypatch.setattr("kicad_mcp.tools.library.update_symbol_property", record_update)

    no_match = await call_tool_text(
        server,
        "lib_recommend_part",
        {
            "category": "LDO",
            "requirements": {
                "voltage_v": {"min": 100.0, "max": 120.0},
                "capacitance_nf": 100.0,
                "frequency_khz": "ignored-text",
            },
        },
    )
    sot23_recommend = await call_tool_text(
        server,
        "lib_recommend_part",
        {
            "category": "diode",
            "requirements": {"current_a": 0.2},
            "package": "SOT-23",
        },
    )
    no_part = await call_tool_text(
        server,
        "lib_bind_part_to_symbol",
        {"sym_ref": "U1", "lcsc_code_or_mpn": "missing"},
    )
    no_package = await call_tool_text(
        server,
        "lib_bind_part_to_symbol",
        {"sym_ref": "U2", "lcsc_code_or_mpn": "C999"},
    )
    no_auto_footprint = await call_tool_text(
        server,
        "lib_bind_part_to_symbol",
        {"sym_ref": "U3", "lcsc_code_or_mpn": "C123", "auto_assign_footprint": False},
    )

    def fail_update(_reference: str, _field: str, _value: str) -> None:
        raise RuntimeError("schematic locked")

    monkeypatch.setattr("kicad_mcp.tools.library.update_symbol_property", fail_update)
    update_failed = await call_tool_text(
        server,
        "lib_bind_part_to_symbol",
        {"sym_ref": "U4", "lcsc_code_or_mpn": "C123"},
    )

    assert "No matching parts found" in no_match
    assert "BAT54" in sot23_recommend
    assert "No part found" in no_part
    assert "package info unavailable" in no_package
    assert "Footprint hint" not in no_auto_footprint
    assert "Could not update schematic properties" in update_failed
    assert ("U2", "LCSC", "C999") in updates


@pytest.mark.anyio
async def test_project_library_tools_make_parts_kicad_can_find(sample_project: Path) -> None:
    server = build_server("full")

    footprint = await call_tool_text(
        server,
        "lib_generate_footprint_from_pads",
        {
            "name": "ODD-2",
            "pads": [
                {"number": 1, "x_mm": -0.8, "y_mm": -0.7, "w_mm": 0.75, "h_mm": 0.225},
                {"number": 1, "x_mm": -0.65, "y_mm": -0.9, "w_mm": 0.4, "h_mm": 0.575},
                {"number": 2, "x_mm": 0.9, "y_mm": 0.25, "w_mm": 0.6, "h_mm": 0.25},
            ],
            "body_w_mm": 2.0,
            "body_h_mm": 2.0,
            "library": "Parts",
        },
    )
    bad_footprint = await call_tool_text(
        server,
        "lib_generate_footprint_from_pads",
        {
            "name": "BAD",
            "pads": [{"number": 1, "x_mm": 0, "y_mm": 0}],
            "body_w_mm": 2.0,
            "body_h_mm": 2.0,
            "library": "Parts",
        },
    )
    symbol = await call_tool_text(
        server,
        "lib_generate_symbol_from_pintable",
        {
            "name": "ODD",
            "pins": [{"number": "1", "name": "IN"}, {"number": "2", "name": "OUT"}],
            "footprint_hint": "Parts:ODD-2",
            "library": "Parts",
        },
    )

    assert "Footprint Parts:ODD-2 saved" in footprint
    assert "Pad numbers: 1, 2 (3 rectangles" in footprint
    assert "Footprint generation failed" in bad_footprint
    assert "Symbol Parts:ODD saved" in symbol
    assert (sample_project / "libs" / "Parts.pretty" / "ODD-2.kicad_mod").exists()
    assert not (sample_project / "libs" / "Parts.pretty" / "BAD.kicad_mod").exists()
    assert '(symbol "ODD"' in (sample_project / "libs" / "Parts.kicad_sym").read_text("utf-8")
    assert '(name "Parts")' in (sample_project / "sym-lib-table").read_text("utf-8")
    assert '(name "Parts")' in (sample_project / "fp-lib-table").read_text("utf-8")
