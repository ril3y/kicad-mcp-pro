# pyright: reportUnknownLambdaType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportFunctionMemberAccess=false
# ruff: noqa: ANN401
"""Unit-level error-path coverage for ``sch_export_png``.

``sch_export_png`` was added in commit cb86438 to give the agent a quick
visual screenshot of the schematic. It calls kicad-cli to render PDF and
then rasterizes the first page with PyMuPDF. The error branches below
are easy to break silently in refactors; pin them here.

Mocking strategy mirrors the existing integration-suite fake CLI runner
in ``tests/integration/test_pcb_export_validation_surface.py`` so the
tests don't require a real kicad-cli binary.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from kicad_mcp.discovery import CliCapabilities, get_cli_capabilities
from kicad_mcp.server import build_server
from tests.conftest import call_tool_text


def _fake_cli_runner(sample_project: Path):
    """Return a fake ``subprocess.run`` that materializes a tiny PDF file."""

    def fake_run(
        cmd: list[str],
        capture_output: bool = True,
        text: bool = True,
        timeout: float = 60.0,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        _ = (capture_output, text, timeout, check)
        if "--version" in cmd:
            return subprocess.CompletedProcess(cmd, 0, stdout="KiCad 10.0.1", stderr="")

        output_path = None
        if "--output" in cmd:
            output_path = Path(cmd[cmd.index("--output") + 1])

        if "pdf" in cmd and output_path is not None:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            # Minimal PDF header so any "is this a PDF?" sniff passes.
            output_path.write_bytes(b"%PDF-1.4\n%fake\n")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    return fake_run


def _install_cli_caps(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "kicad_mcp.tools.export.get_cli_capabilities",
        lambda _cli: CliCapabilities(
            version="KiCad 10.0.1",
            gerber_command="gerber",
            drill_command="drill",
            position_command="pos",
            supports_ipc2581=True,
            supports_svg=True,
            supports_dxf=True,
            supports_step=True,
            supports_render=True,
            supports_spice_netlist=True,
        ),
    )
    get_cli_capabilities.cache_clear()


@pytest.mark.anyio
async def test_sch_export_png_pymupdf_missing(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When pymupdf is not installed, return a graceful hint, not a crash.

    The tool still runs kicad-cli to produce the PDF, so the user can
    rasterize manually. The graceful-error contract says:
      - the PDF path is mentioned (so the user can find it),
      - pymupdf is mentioned (so the user knows what's missing),
      - no exception escapes.
    """
    monkeypatch.setattr("kicad_mcp.tools.export.subprocess.run", _fake_cli_runner(sample_project))
    monkeypatch.setattr("kicad_mcp.discovery.subprocess.run", _fake_cli_runner(sample_project))
    _install_cli_caps(monkeypatch)

    # Block pymupdf import for the duration of the tool call. Using
    # sys.modules sentinel = None makes ``import pymupdf`` raise
    # ImportError without touching the real install (if any).
    monkeypatch.setitem(sys.modules, "pymupdf", None)

    server = build_server("full")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})
    text = await call_tool_text(server, "sch_export_png", {})

    assert "pymupdf" in text.lower(), f"Expected the error to mention pymupdf; got: {text!r}"
    # Successful CLI step is acknowledged, so the user knows where the PDF lives.
    assert "PDF exported" in text or "pdf" in text.lower()


@pytest.mark.anyio
async def test_sch_export_png_page_out_of_range(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Requesting a page beyond the PDF's page count must return an error,
    not crash inside pymupdf. The tool advertises ``page`` as 1-based; pin
    both the rejection AND a humane error message."""
    monkeypatch.setattr("kicad_mcp.tools.export.subprocess.run", _fake_cli_runner(sample_project))
    monkeypatch.setattr("kicad_mcp.discovery.subprocess.run", _fake_cli_runner(sample_project))
    _install_cli_caps(monkeypatch)

    # Stub pymupdf with a tiny fake document object that reports 1 page.
    class _FakePixmap:
        def save(self, path: str) -> None:  # noqa: D401 - duck-type stub
            Path(path).write_bytes(b"png")

    class _FakePage:
        def get_pixmap(self, matrix: object) -> _FakePixmap:  # noqa: D401
            _ = matrix
            return _FakePixmap()

    class _FakeDoc:
        page_count = 1

        def __init__(self) -> None:
            self.closed = False

        def __getitem__(self, idx: int) -> _FakePage:
            return _FakePage()

        def close(self) -> None:
            self.closed = True

    class _FakeMatrix:
        def __init__(self, zx: float, zy: float) -> None:
            self.zx, self.zy = zx, zy

    fake_pymupdf = type(sys)("pymupdf")
    fake_pymupdf.open = lambda _path: _FakeDoc()  # type: ignore[attr-defined]
    fake_pymupdf.Matrix = _FakeMatrix  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "pymupdf", fake_pymupdf)

    server = build_server("full")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    # Page beyond the document's range.
    text = await call_tool_text(server, "sch_export_png", {"page": 99})
    assert "out of range" in text.lower(), f"Expected an out-of-range message; got: {text!r}"
    # Confirm the real page count is surfaced so the agent can self-correct.
    assert "1" in text

    # Zero/negative pages should also be rejected (1-based contract).
    text_zero = await call_tool_text(server, "sch_export_png", {"page": 0})
    assert "out of range" in text_zero.lower()


@pytest.mark.anyio
async def test_sch_export_png_dpi_default_is_150(
    sample_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sanity check the documented default DPI.

    Calls the tool with no ``dpi`` argument and verifies the pymupdf
    Matrix is built with ``150 / 72.0`` zoom. If someone changes the
    default, this test fires so docs and behavior stay in sync.
    """
    monkeypatch.setattr("kicad_mcp.tools.export.subprocess.run", _fake_cli_runner(sample_project))
    monkeypatch.setattr("kicad_mcp.discovery.subprocess.run", _fake_cli_runner(sample_project))
    _install_cli_caps(monkeypatch)

    captured_zoom: dict[str, float] = {}

    class _FakePixmap:
        def save(self, path: str) -> None:
            Path(path).write_bytes(b"png")

    class _FakePage:
        def get_pixmap(self, matrix: object) -> _FakePixmap:
            captured_zoom["zx"] = getattr(matrix, "zx", float("nan"))
            captured_zoom["zy"] = getattr(matrix, "zy", float("nan"))
            return _FakePixmap()

    class _FakeDoc:
        page_count = 1

        def __getitem__(self, idx: int) -> _FakePage:
            _ = idx
            return _FakePage()

        def close(self) -> None:
            pass

    class _FakeMatrix:
        def __init__(self, zx: float, zy: float) -> None:
            self.zx, self.zy = zx, zy

    fake_pymupdf = type(sys)("pymupdf")
    fake_pymupdf.open = lambda _path: _FakeDoc()  # type: ignore[attr-defined]
    fake_pymupdf.Matrix = _FakeMatrix  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "pymupdf", fake_pymupdf)

    server = build_server("full")
    await call_tool_text(server, "kicad_set_project", {"project_dir": str(sample_project)})

    text = await call_tool_text(server, "sch_export_png", {})

    expected_zoom = 150 / 72.0
    assert captured_zoom.get("zx") == pytest.approx(expected_zoom), (
        f"Default DPI changed: captured zoom = {captured_zoom!r}, expected zx = {expected_zoom}. "
        "If the default was intentionally moved off 150 DPI, update this test AND the "
        "tool docstring/MEMORY note together."
    )
    assert captured_zoom.get("zy") == pytest.approx(expected_zoom)
    assert "Schematic PNG exported" in text
