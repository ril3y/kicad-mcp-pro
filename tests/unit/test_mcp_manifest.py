from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_validator() -> object:
    script = ROOT / "scripts" / "validate_mcp_manifest.py"
    spec = importlib.util.spec_from_file_location("validate_mcp_manifest", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checked_mcp_manifest_is_valid() -> None:
    module = _load_validator()
    manifest = module.validate_manifest_file(ROOT / "mcp.json")

    assert manifest["name"] == "io.github.oaslananka-lab/kicad-mcp-pro"
    assert manifest["repository"]["url"] == "https://github.com/oaslananka-lab/kicad-mcp-pro"
    assert manifest["mcp"]["command"] == "kicad-mcp-pro"


def test_validator_rejects_missing_command(tmp_path: Path) -> None:
    module = _load_validator()
    manifest = json.loads((ROOT / "mcp.json").read_text(encoding="utf-8"))
    manifest["mcp"].pop("command")
    for package in manifest["packages"]:
        package.pop("command", None)
    path = tmp_path / "mcp.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    errors = module.validate_manifest(module.load_manifest(path))

    assert "manifest must define mcp.command or a package command." in errors


def test_validator_rejects_duplicate_packages(tmp_path: Path) -> None:
    module = _load_validator()
    manifest = json.loads((ROOT / "mcp.json").read_text(encoding="utf-8"))
    manifest["packages"].append(dict(manifest["packages"][0]))
    path = tmp_path / "mcp.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    errors = module.validate_manifest(module.load_manifest(path))

    assert any("duplicates package pypi/kicad-mcp-pro" in error for error in errors)


def test_validator_rejects_unsupported_transport() -> None:
    module = _load_validator()
    manifest = json.loads((ROOT / "mcp.json").read_text(encoding="utf-8"))
    manifest["packages"][0]["transport"]["type"] = "websocket"

    errors = module.validate_manifest(manifest)

    assert "packages[0] uses unsupported transport 'websocket'." in errors
