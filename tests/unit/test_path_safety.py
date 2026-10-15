# pyright: reportPrivateUsage=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnusedImport=false
# ruff: noqa: ANN001, ANN201
from __future__ import annotations

from pathlib import Path

import pytest

from kicad_mcp.config import KiCadMCPConfig
from kicad_mcp.errors import KiCadNotRunningError, UnsafePathError, error_payload
from kicad_mcp.path_safety import assert_within
from kicad_mcp.utils.paths import relative_subpath, resolve_under

BYPASS_FLAG_NAME = ".kicad-mcp-allow-any-path"


def test_resolve_within_project_blocks_traversal(sample_project: Path) -> None:
    cfg = KiCadMCPConfig(project_dir=sample_project)

    with pytest.raises(UnsafePathError):
        cfg.resolve_within_project("../outside.txt")


def test_explicit_workspace_blocks_outside_absolute_path(tmp_path: Path, fake_cli: Path) -> None:
    workspace = tmp_path / "workspace"
    project = workspace / "project"
    outside = tmp_path / "outside.txt"
    project.mkdir(parents=True)
    outside.write_text("x", encoding="utf-8")

    cfg = KiCadMCPConfig(kicad_cli=fake_cli, workspace_root=workspace, project_dir=project)

    with pytest.raises(UnsafePathError):
        cfg.resolve_within_project(outside)


def test_output_subdir_blocks_parent_traversal(sample_project: Path) -> None:
    cfg = KiCadMCPConfig(project_dir=sample_project)

    with pytest.raises(UnsafePathError):
        cfg.ensure_output_dir("../escape")


def test_path_utils_wrapper_resolves_safe_paths(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    nested = workspace / "project" / "board.kicad_pcb"
    nested.parent.mkdir(parents=True)
    nested.write_text("(kicad_pcb)", encoding="utf-8")

    assert resolve_under(workspace, "project/board.kicad_pcb") == nested
    assert resolve_under(workspace, nested) == nested
    assert relative_subpath("exports/gerbers") == Path("exports/gerbers")


def test_error_payload_masks_domain_shape() -> None:
    payload = error_payload(RuntimeError("boom"))

    assert payload == {
        "code": "INTERNAL_ERROR",
        "message": "boom",
        "hint": "Run doctor for diagnostics and retry with corrected configuration.",
        "retryable": False,
    }


def test_relative_subpath_blocks_absolute_path(tmp_path: Path) -> None:
    with pytest.raises(UnsafePathError):
        relative_subpath(tmp_path)


def test_error_payload_preserves_domain_error() -> None:
    payload = error_payload(KiCadNotRunningError("not reachable"))

    assert payload["code"] == "KICAD_NOT_RUNNING"
    assert payload["message"] == "not reachable"
    assert payload["retryable"] is True


def test_error_payload_falls_back_to_exception_name() -> None:
    payload = error_payload(RuntimeError())

    assert payload["message"] == "RuntimeError"


# --- bypass-flag (~/.kicad-mcp-allow-any-path) regression coverage ----------
#
# ``assert_within`` opts the user out of the workspace sandbox when the
# bypass flag file exists in their home dir. The tests below pin that
# contract so a refactor cannot silently change the file name, change
# from ``.exists()`` to ``.is_file()`` without notice, or accidentally
# delete the bypass entirely (re-trapping users behind a busted MCP
# env-passthrough — the exact scenario the flag exists to escape).


def test_assert_within_allows_any_path_when_flag_file_present(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When the bypass flag is present, paths outside ``root`` are accepted."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    (fake_home / BYPASS_FLAG_NAME).write_text("", encoding="utf-8")
    monkeypatch.setattr("kicad_mcp.path_safety.Path.home", lambda: fake_home)

    root = tmp_path / "workspace"
    root.mkdir()
    outside = tmp_path / "elsewhere" / "file.txt"
    outside.parent.mkdir()
    outside.write_text("x", encoding="utf-8")

    # Must not raise — bypass file present.
    assert_within(root, outside)


def test_assert_within_rejects_outside_when_flag_file_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without the bypass flag, out-of-workspace paths must raise."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    # Explicitly ensure the flag is NOT present.
    assert not (fake_home / BYPASS_FLAG_NAME).exists()
    monkeypatch.setattr("kicad_mcp.path_safety.Path.home", lambda: fake_home)

    root = tmp_path / "workspace"
    root.mkdir()
    outside = tmp_path / "elsewhere" / "file.txt"
    outside.parent.mkdir()
    outside.write_text("x", encoding="utf-8")

    with pytest.raises(UnsafePathError):
        assert_within(root, outside)


def test_assert_within_accepts_inside_path_regardless_of_flag(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """In-workspace paths must always pass — the flag is for OUT-of-workspace."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr("kicad_mcp.path_safety.Path.home", lambda: fake_home)

    root = tmp_path / "workspace"
    nested = root / "sub" / "file.txt"
    nested.parent.mkdir(parents=True)
    nested.write_text("x", encoding="utf-8")

    # No flag, in-workspace: passes.
    assert_within(root, nested)
    # Flag added, in-workspace: still passes (early-return is harmless).
    (fake_home / BYPASS_FLAG_NAME).write_text("", encoding="utf-8")
    assert_within(root, nested)


def test_bypass_flag_uses_exists_not_is_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Pin the documented contract: the bypass check uses ``.exists()``.

    A directory named ``.kicad-mcp-allow-any-path`` (created e.g. by an
    accidental ``mkdir`` instead of ``touch``) currently also enables
    bypass. If we ever tighten this to ``.is_file()`` the change must be
    intentional — this test will fail loud so we notice.
    """
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    # Create as a directory, not a file.
    (fake_home / BYPASS_FLAG_NAME).mkdir()
    monkeypatch.setattr("kicad_mcp.path_safety.Path.home", lambda: fake_home)

    root = tmp_path / "workspace"
    root.mkdir()
    outside = tmp_path / "elsewhere"
    outside.mkdir()

    # Directory flag also activates bypass (``.exists()`` returns True).
    assert_within(root, outside)


def test_bypass_flag_filename_is_stable() -> None:
    """The flag-file name is part of the public bypass contract — pin it.

    Changing this string is a user-visible breaking change (the user has
    to ``touch`` the new filename to keep their bypass working). This
    test guards against a silent rename.
    """
    # The bypass file name documented in path_safety.assert_within().
    import kicad_mcp.path_safety as ps

    src = (Path(ps.__file__)).read_text(encoding="utf-8")
    assert BYPASS_FLAG_NAME in src, (
        f"path_safety.py no longer mentions '{BYPASS_FLAG_NAME}'; the "
        "bypass flag was renamed or removed without updating tests. "
        "If this was intentional, update BYPASS_FLAG_NAME and the user "
        "docs to match."
    )
