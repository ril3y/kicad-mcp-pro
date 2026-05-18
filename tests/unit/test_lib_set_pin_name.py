# pyright: reportPrivateUsage=false, reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false
"""End-to-end test for the ``lib_set_pin_name`` MCP tool.

These exercise the WHOLE call path: load → mutate via sexpdata →
validate via kicad-cli → backup → atomic write. The tool is registered
under the ``library`` category in router.TOOL_CATEGORIES and the
``library`` tier group in capabilities, so we drive it the same way
the running MCP server does — via ``build_server`` + ``call_tool_text``.

When ``kicad-cli`` isn't reachable on the test machine the tests skip
gracefully so CI on Linux runners without KiCad installed still pass.
"""

from __future__ import annotations

import asyncio
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest


_FIXTURE_LIB = """\
(kicad_symbol_lib (version 20241209) (generator "test")
  (symbol "FAKE_RELAY"
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (property "Reference" "K" (at 0 16.51 0) (effects (font (size 1.27 1.27))))
    (property "Value" "FAKE_RELAY" (at 0 -17.78 0) (effects (font (size 1.27 1.27))))
    (property "Manufacturer" "FAKECO(SOMECITY)" (at 0 -25.40 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "FAKE_RELAY_0_1"
      (rectangle (start -5.08 5.08) (end 5.08 -5.08) (stroke (width 0) (type default)) (fill (type background)))
      (pin unspecified line (at -7.62 2.54 0) (length 2.54)
        (name "1" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin unspecified line (at 7.62 2.54 180) (length 2.54)
        (name "2" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
  )
)
"""


def _kicad_cli_available() -> Path | None:
    candidates = [
        Path(r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"),
        Path("/usr/bin/kicad-cli"),
        Path("/usr/local/bin/kicad-cli"),
    ]
    for c in candidates:
        if c.exists():
            return c
    found = shutil.which("kicad-cli")
    return Path(found) if found else None


_CLI = _kicad_cli_available()
needs_cli = pytest.mark.skipif(_CLI is None, reason="kicad-cli not installed on this machine")


def _setup(tmp_path: Path, monkeypatch) -> tuple[Path, SimpleNamespace]:
    """Write the fixture lib and return (path, fake_cfg)."""
    lib = tmp_path / "fake.kicad_sym"
    lib.write_text(_FIXTURE_LIB, encoding="utf-8")
    fake_cfg = SimpleNamespace(
        symbol_library_dir=tmp_path,
        footprint_library_dir=tmp_path,
        project_dir=None,
        kicad_cli=_CLI if _CLI else Path("kicad-cli-stub"),
        max_items_per_response=50,
    )
    monkeypatch.setattr("kicad_mcp.tools.library.get_config", lambda: fake_cfg)
    return lib, fake_cfg


@needs_cli
def test_lib_set_pin_name_renames_pin_and_persists_change(
    tmp_path: Path, monkeypatch
) -> None:
    """Full path: rename pin "1" to "Coil1" via the MCP tool, confirm
    the rename landed on disk AND that the file still parses cleanly
    via kicad-cli (so the next person to open it doesn't see a broken
    library). This is the bug the tool was built to prevent."""
    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    lib, _ = _setup(tmp_path, monkeypatch)
    server = build_server("agent_full")
    result = asyncio.run(
        call_tool_text(
            server,
            "lib_set_pin_name",
            {
                "symbol_name": "FAKE_RELAY",
                "pin_number": "1",
                "new_name": "Coil1",
                "library_path": str(lib),
            },
        )
    )

    assert "Renamed pin 1" in result
    assert "Coil1" in result
    # Backup file exists
    backup = lib.with_suffix(lib.suffix + ".bak-pre-rename")
    assert backup.exists()
    # The live file has the new name
    new_text = lib.read_text(encoding="utf-8")
    assert '(name "Coil1"' in new_text
    # The previous "1" name was on pin 1 — confirm it's gone for that pin
    # (pin 2's name is still "2", separately).
    # Easiest check: count occurrences of (name "1" — must be 0.
    assert new_text.count('(name "1"') == 0


@needs_cli
def test_lib_set_pin_name_dry_run_validates_without_writing(
    tmp_path: Path, monkeypatch
) -> None:
    """dry_run=True must validate (kicad-cli must accept the rewrite)
    but NOT touch the live file. Used by callers that want to confirm
    a rename would succeed before committing to it."""
    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    lib, _ = _setup(tmp_path, monkeypatch)
    original = lib.read_text(encoding="utf-8")
    result = asyncio.run(
        call_tool_text(
            build_server("agent_full"),
            "lib_set_pin_name",
            {
                "symbol_name": "FAKE_RELAY",
                "pin_number": "1",
                "new_name": "Coil1",
                "library_path": str(lib),
                "dry_run": True,
            },
        )
    )

    assert "dry-run OK" in result
    # Original file unchanged
    assert lib.read_text(encoding="utf-8") == original
    # No backup created in dry-run mode
    backup = lib.with_suffix(lib.suffix + ".bak-pre-rename")
    assert not backup.exists()


def test_lib_set_pin_name_reports_when_symbol_missing(
    tmp_path: Path, monkeypatch
) -> None:
    """Looking up a non-existent symbol should fail cleanly with a
    pointer at the cause — NOT mangle the file."""
    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    lib, _ = _setup(tmp_path, monkeypatch)
    original = lib.read_text(encoding="utf-8")

    result = asyncio.run(
        call_tool_text(
            build_server("agent_full"),
            "lib_set_pin_name",
            {
                "symbol_name": "DOES_NOT_EXIST",
                "pin_number": "1",
                "new_name": "X",
                "library_path": str(lib),
            },
        )
    )

    assert "not found" in result.lower()
    assert lib.read_text(encoding="utf-8") == original


def test_lib_set_pin_name_reports_when_pin_missing(
    tmp_path: Path, monkeypatch
) -> None:
    """Same shape — pin number missing must NOT cause a write."""
    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    lib, _ = _setup(tmp_path, monkeypatch)
    original = lib.read_text(encoding="utf-8")

    result = asyncio.run(
        call_tool_text(
            build_server("agent_full"),
            "lib_set_pin_name",
            {
                "symbol_name": "FAKE_RELAY",
                "pin_number": "99",
                "new_name": "X",
                "library_path": str(lib),
            },
        )
    )

    assert "not found" in result.lower()
    assert "datasheet" in result.lower()  # tool nudges user to verify
    assert lib.read_text(encoding="utf-8") == original


@needs_cli
def test_lib_set_pin_name_noop_when_name_already_set(
    tmp_path: Path, monkeypatch
) -> None:
    """Renaming a pin to its existing name should be a no-op (no write,
    no backup, clear "No change" message). Without this guard repeated
    automation runs would needlessly churn the file."""
    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    lib, _ = _setup(tmp_path, monkeypatch)

    result = asyncio.run(
        call_tool_text(
            build_server("agent_full"),
            "lib_set_pin_name",
            {
                "symbol_name": "FAKE_RELAY",
                "pin_number": "1",
                "new_name": "1",
                "library_path": str(lib),
            },
        )
    )

    assert "No change" in result
    backup = lib.with_suffix(lib.suffix + ".bak-pre-rename")
    assert not backup.exists()


@needs_cli
def test_lib_set_pin_name_also_sets_pin_type_when_requested(
    tmp_path: Path, monkeypatch
) -> None:
    """The optional ``new_type`` parameter retypes a pin (unspecified ->
    passive, etc.). This is part of the rename flow because turning a
    relay's "unspecified" pins into "passive" matches what KiCad's own
    Symbol Editor would do."""
    from kicad_mcp.server import build_server
    from tests.conftest import call_tool_text

    lib, _ = _setup(tmp_path, monkeypatch)
    result = asyncio.run(
        call_tool_text(
            build_server("agent_full"),
            "lib_set_pin_name",
            {
                "symbol_name": "FAKE_RELAY",
                "pin_number": "1",
                "new_name": "Coil1",
                "library_path": str(lib),
                "new_type": "passive",
            },
        )
    )

    assert "Renamed pin 1" in result
    assert "passive" in result
    text = lib.read_text(encoding="utf-8")
    # The pin block whose name is now Coil1 should also be type=passive.
    # Spot-check by searching for "passive" appearing near "Coil1".
    coil1_idx = text.find('(name "Coil1"')
    assert coil1_idx > 0
    # The (pin <type> ...) opener is at some earlier index
    pin_open = text.rfind("(pin ", 0, coil1_idx)
    assert pin_open > 0
    pin_header = text[pin_open : pin_open + 30]
    assert "passive" in pin_header
