from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run_node(*args: str) -> subprocess.CompletedProcess[str]:
    node = shutil.which("node")
    assert node is not None
    return subprocess.run(
        [node, *args],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def test_release_state_offline_outputs_required_schema() -> None:
    result = _run_node("scripts/release-state.mjs", "--offline", "--json")

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert {
        "current_state",
        "version",
        "tag",
        "github_release",
        "testpypi",
        "pypi",
        "mirror",
        "blockers",
        "next_safe_command",
        "safe_to_publish",
    }.issubset(payload)
    assert payload["tag"] == f"v{payload['version']}"
    assert isinstance(payload["safe_to_publish"], bool)


def test_failure_classifier_detects_non_python_pypi_asset() -> None:
    result = _run_node(
        "scripts/classify-gh-failure.mjs",
        "--json",
        "--text",
        "InvalidDistribution: SHA256SUMS.txt is not a valid distribution",
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["classification"] == "non-python-asset-uploaded-to-pypi"
    assert payload["publish_must_stop"] is True
    assert payload["auto_fix_allowed"] is True


def test_failure_classifier_detects_personal_mirror_tag_clobber() -> None:
    result = _run_node(
        "scripts/classify-gh-failure.mjs",
        "--json",
        "--text",
        "! [rejected] v3.2.0 -> v3.2.0 (would clobber existing tag)",
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["classification"] == "personal-mirror-tag-clobber"
    assert payload["publish_must_stop"] is False
    assert payload["human_approval_required"] is True


def test_review_thread_gate_blocks_current_human_thread(tmp_path: Path) -> None:
    fixture = tmp_path / "pull-request.json"
    json_out = tmp_path / "summary.json"
    markdown_out = tmp_path / "summary.md"
    fixture.write_text(
        json.dumps(
            {
                "id": "PR_kw",
                "url": "https://github.com/oaslananka-lab/kicad-mcp-pro/pull/1",
                "isDraft": False,
                "reviewThreads": {
                    "nodes": [
                        {
                            "id": "PRRT_human",
                            "isResolved": False,
                            "isOutdated": False,
                            "path": "src/example.py",
                            "line": 10,
                            "originalLine": 10,
                            "diffSide": "RIGHT",
                            "comments": {
                                "nodes": [
                                    {
                                        "author": {"login": "oaslananka"},
                                        "body": "Please add a regression test.",
                                        "url": "https://github.com/example/thread",
                                        "createdAt": "2026-05-07T00:00:00Z",
                                        "updatedAt": "2026-05-07T00:00:00Z",
                                    }
                                ]
                            },
                        },
                        {
                            "id": "PRRT_bot_info",
                            "isResolved": False,
                            "isOutdated": False,
                            "path": "README.md",
                            "line": 1,
                            "originalLine": 1,
                            "diffSide": "RIGHT",
                            "comments": {
                                "nodes": [
                                    {
                                        "author": {"login": "github-actions[bot]"},
                                        "body": "Informational summary only.",
                                        "url": "https://github.com/example/bot",
                                        "createdAt": "2026-05-07T00:00:00Z",
                                        "updatedAt": "2026-05-07T00:00:00Z",
                                    }
                                ]
                            },
                        },
                    ]
                },
            }
        ),
        encoding="utf-8",
    )

    result = _run_node(
        "scripts/check-review-threads.mjs",
        "--fixture",
        str(fixture),
        "--repo",
        "oaslananka-lab/kicad-mcp-pro",
        "--pr",
        "1",
        "--json-out",
        str(json_out),
        "--markdown-out",
        str(markdown_out),
        "--fail-on-blocked",
    )

    assert result.returncode == 1
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    assert payload["blocked"] is True
    assert payload["counts"]["blocking"] == 1
    assert payload["blocking_threads"][0]["reason"] == "human-review"
    assert "Review Thread Gate" in markdown_out.read_text(encoding="utf-8")
