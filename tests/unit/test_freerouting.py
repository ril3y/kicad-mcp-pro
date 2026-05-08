from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from kicad_mcp.utils.freerouting import (
    FreeRoutingRunner,
    _freerouting_image_major_version,
)


def test_export_dsn_copies_existing_sibling_dsn(sample_project: Path) -> None:
    pcb_path = sample_project / "demo.kicad_pcb"
    source_dsn = sample_project / "demo.dsn"
    source_dsn.write_text("dsn", encoding="utf-8")

    runner = FreeRoutingRunner()
    staged = runner.export_dsn(pcb_path, Path("output/routing/board.dsn"))

    assert staged.exists()
    assert staged.read_text(encoding="utf-8") == "dsn"


def test_export_dsn_requires_manual_export_when_cli_lacks_specctra(sample_project: Path) -> None:
    runner = FreeRoutingRunner()

    with pytest.raises(RuntimeError) as exc_info:
        runner.export_dsn(sample_project / "demo.kicad_pcb", Path("output/routing/board.dsn"))

    assert "Export a .dsn file from KiCad's PCB Editor" in str(exc_info.value)


def test_run_freerouting_docker_builds_expected_command(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dsn_path = sample_project / "board.dsn"
    ses_path = sample_project / "board.ses"
    dsn_path.write_text("dsn", encoding="utf-8")
    observed: list[list[str]] = []

    def fake_run(cmd, capture_output, text, timeout, check):
        _ = (capture_output, text, timeout, check)
        observed.append(cmd)
        ses_path.write_text("ses", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, stdout="pass 3\n100% routed\nok", stderr="")

    monkeypatch.setattr("kicad_mcp.utils.freerouting.subprocess.run", fake_run)
    monkeypatch.setattr("kicad_mcp.utils.freerouting._docker_available", lambda _: True)

    result = FreeRoutingRunner(
        docker_image="ghcr.io/freerouting/freerouting:1.9.0",
    ).run_freerouting(
        dsn_path,
        ses_path,
        max_passes=55,
        thread_count=6,
        use_docker=True,
        net_classes_to_ignore=["GND", "PWR"],
        exclude_nets=["SHIELD"],
        drc_report_path=sample_project / "freerouting.drc.json",
    )

    assert result.returncode == 0
    assert result.routed_pct == 100.0
    assert result.total_nets == 0
    assert result.pass_count == 3
    assert result.ses_path == ses_path.resolve()
    assert observed
    assert observed[0][:3] == ["docker", "run", "--rm"]
    assert "-de" in observed[0]
    assert "-do" in observed[0]
    assert "-mt" in observed[0]
    assert "--router.max_passes=55" in observed[0]
    assert "-inc" in observed[0]
    assert "GND,PWR,SHIELD" in observed[0]
    assert "-drc" in observed[0]


def test_run_freerouting_falls_back_to_jar_when_docker_missing(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dsn_path = sample_project / "board.dsn"
    ses_path = sample_project / "board.ses"
    jar_path = sample_project / "freerouting.jar"
    dsn_path.write_text("(pcb (net A) (net B))", encoding="utf-8")
    jar_path.write_text("jar", encoding="utf-8")
    observed: list[list[str]] = []

    monkeypatch.setattr("kicad_mcp.utils.freerouting.shutil.which", lambda _: None)

    def fake_run(cmd, capture_output, text, timeout, check):
        _ = (capture_output, text, timeout, check)
        observed.append(cmd)
        ses_path.write_text("ses", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, stdout="unrouted net B", stderr="")

    monkeypatch.setattr("kicad_mcp.utils.freerouting.subprocess.run", fake_run)

    result = FreeRoutingRunner().run_freerouting(
        dsn_path,
        ses_path,
        use_docker=True,
        freerouting_jar_path=jar_path,
    )

    assert observed[0][:2] == ["java", "-jar"]
    assert result.mode == "jar"
    assert result.total_nets == 2
    assert result.unrouted_nets == ["B"]
    assert result.routed_pct == 50.0


def test_run_freerouting_jar_requires_jar_path(sample_project: Path) -> None:
    dsn_path = sample_project / "board.dsn"
    ses_path = sample_project / "board.ses"
    dsn_path.write_text("dsn", encoding="utf-8")

    with pytest.raises(RuntimeError) as exc_info:
        FreeRoutingRunner().run_freerouting(dsn_path, ses_path, use_docker=False)

    assert "FreeRouting JAR path is required" in str(exc_info.value)


@pytest.mark.parametrize(
    ("image", "expected"),
    [
        # Numbered tags — return major version.
        ("ghcr.io/freerouting/freerouting:2.1.0", 2),
        ("ghcr.io/freerouting/freerouting:2", 2),
        ("ghcr.io/freerouting/freerouting:1.9.0", 1),
        ("ghcr.io/freerouting/freerouting:v1.9.0", 1),
        ("freerouting:3.0.0-beta", 3),
        ("registry.example.com/freerouting/freerouting:1.0", 1),
        # Registry with port — must skip the host:port colon and parse the
        # final image:tag colon. ghcr-style refs with private mirrors hit
        # this shape regularly.
        ("registry.example.com:5000/freerouting/freerouting:2.0", 2),
        # Multi-digit major (forward-compat: v10 must reject too).
        ("ghcr.io/freerouting/freerouting:10.0.1", 10),
        # Ambiguous tags — must return None so detection doesn't false-positive.
        ("ghcr.io/freerouting/freerouting:latest", None),
        ("ghcr.io/freerouting/freerouting:nightly", None),
        ("ghcr.io/freerouting/freerouting", None),  # no tag
        ("ghcr.io/freerouting/freerouting@sha256:abc123", None),
    ],
)
def test_freerouting_image_major_version_parses_tag(
    image: str,
    expected: int | None,
) -> None:
    """Major-version parser must distinguish numbered tags from ambiguous ones."""
    assert _freerouting_image_major_version(image) == expected


def test_run_freerouting_rejects_v2_image_with_clear_error(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """v2.x images use an HTTP server entrypoint that ignores our CLI argv.

    Regression target: pre-detection the user got a confusing
    "100% routed" success or a silent 0-output run because the v2 docker
    container spun up its HTTP API server and never processed -de/-do.
    Now the runner refuses to launch and points at workarounds.
    """
    dsn_path = sample_project / "board.dsn"
    ses_path = sample_project / "board.ses"
    dsn_path.write_text("dsn", encoding="utf-8")

    monkeypatch.setattr("kicad_mcp.utils.freerouting._docker_available", lambda _: True)

    runner = FreeRoutingRunner(docker_image="ghcr.io/freerouting/freerouting:2.1.0")

    with pytest.raises(RuntimeError) as exc_info:
        runner.run_freerouting(dsn_path, ses_path, use_docker=True)

    msg = str(exc_info.value)
    assert "v2.x" in msg
    assert "HTTP API server" in msg
    assert "KICAD_MCP_FREEROUTING_IMAGE" in msg
    assert "KICAD_MCP_FREEROUTING_JAR" in msg


def test_run_freerouting_accepts_v1_image(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A v1.x docker image must still build the CLI command (regression guard
    that the new detection didn't accidentally reject the supported path)."""
    dsn_path = sample_project / "board.dsn"
    ses_path = sample_project / "board.ses"
    dsn_path.write_text("dsn", encoding="utf-8")
    observed: list[list[str]] = []

    def fake_run(cmd, capture_output, text, timeout, check):  # type: ignore[no-untyped-def]
        _ = (capture_output, text, timeout, check)
        observed.append(cmd)
        ses_path.write_text("ses", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, stdout="100% routed", stderr="")

    monkeypatch.setattr("kicad_mcp.utils.freerouting.subprocess.run", fake_run)
    monkeypatch.setattr("kicad_mcp.utils.freerouting._docker_available", lambda _: True)

    runner = FreeRoutingRunner(docker_image="ghcr.io/freerouting/freerouting:1.9.0")
    runner.run_freerouting(dsn_path, ses_path, use_docker=True)

    assert observed, "v1 image was unexpectedly rejected"
    assert "-de" in observed[0]


def test_run_freerouting_v2_image_falls_back_to_jar_when_configured(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """v2 image + configured JAR must transparently take the java path
    instead of refusing — the JAR is the documented v2 workaround."""
    dsn_path = sample_project / "board.dsn"
    ses_path = sample_project / "board.ses"
    jar_path = sample_project / "freerouting.jar"
    dsn_path.write_text("(pcb (net A))", encoding="utf-8")
    jar_path.write_text("jar", encoding="utf-8")
    observed: list[list[str]] = []

    def fake_run(cmd, capture_output, text, timeout, check):  # type: ignore[no-untyped-def]
        _ = (capture_output, text, timeout, check)
        observed.append(cmd)
        ses_path.write_text("ses", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, stdout="100% routed", stderr="")

    monkeypatch.setattr("kicad_mcp.utils.freerouting.subprocess.run", fake_run)
    # Docker IS available — proves the guard isn't just a docker-missing fallback.
    monkeypatch.setattr("kicad_mcp.utils.freerouting._docker_available", lambda _: True)

    runner = FreeRoutingRunner(docker_image="ghcr.io/freerouting/freerouting:2.1.0")
    result = runner.run_freerouting(
        dsn_path,
        ses_path,
        use_docker=True,
        freerouting_jar_path=jar_path,
    )

    # Must have used the java path, NOT raised.
    assert result.mode == "jar"
    assert observed[0][:2] == ["java", "-jar"]


def test_run_freerouting_accepts_ambiguous_tag(
    sample_project: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ambiguous tags (latest, nightly, no tag) must not trip the v2 guard.

    We can't tell the version from the reference, so refusing would
    block legitimate setups (e.g. private registries with custom tags).
    The detection is intentionally conservative — only refuse when the
    tag clearly says "v2+".
    """
    dsn_path = sample_project / "board.dsn"
    ses_path = sample_project / "board.ses"
    dsn_path.write_text("dsn", encoding="utf-8")
    observed: list[list[str]] = []

    def fake_run(cmd, capture_output, text, timeout, check):  # type: ignore[no-untyped-def]
        _ = (capture_output, text, timeout, check)
        observed.append(cmd)
        ses_path.write_text("ses", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, stdout="100% routed", stderr="")

    monkeypatch.setattr("kicad_mcp.utils.freerouting.subprocess.run", fake_run)
    monkeypatch.setattr("kicad_mcp.utils.freerouting._docker_available", lambda _: True)

    runner = FreeRoutingRunner(docker_image="ghcr.io/freerouting/freerouting:latest")
    runner.run_freerouting(dsn_path, ses_path, use_docker=True)

    assert observed, "ambiguous tag was unexpectedly rejected"


def test_import_ses_stages_session(sample_project: Path, tmp_path: Path) -> None:
    ses_path = tmp_path / "board.ses"
    ses_path.write_text("ses", encoding="utf-8")

    staged = FreeRoutingRunner().import_ses(sample_project / "demo.kicad_pcb", ses_path)

    assert staged.exists()
    assert staged.read_text(encoding="utf-8") == "ses"
    assert staged.parent.name == "routing"
