# Repository Apps and External Checks

This page documents the intended GitHub App and Marketplace integration baseline
for `kicad-mcp-pro`. It is an operational checklist; installing an app still
requires repository or organization settings access.

## Current Repo-Level Baseline

The repository is expected to use the following categories of checks:

| Integration | Required | Signal |
| --- | --- | --- |
| GitHub Actions CI | Yes | Primary lint, type, test, security, build gate |
| CodeQL | Yes | GitHub native code scanning |
| Renovate | Yes | Dependency update pull requests |
| Codecov | Yes | Coverage project and patch reporting |
| Trivy | Yes | Container and dependency vulnerability checks |
| Gitleaks / secret scanning | Yes | Secret leak detection |
| OpenSSF Scorecard | Yes | Repository supply-chain posture |
| Socket Security | Recommended | Malicious dependency risk signal |
| Semgrep | Recommended | SAST and custom policy rules |
| StepSecurity Harden-Runner | Recommended | Runtime behavior visibility for sensitive workflows |
| GitGuardian | Optional | Additional secret monitoring signal |
| Mergify | Optional | Merge queue and dependency PR automation if native queue is insufficient |
| SonarQube Cloud | Optional | Quality dashboard if Semgrep/Ruff/mypy are not enough |

## App Installation Order

1. Renovate.
2. Codecov.
3. Socket Security.
4. Semgrep.
5. GitGuardian or native GitHub secret scanning policy.
6. StepSecurity Actions Security / Harden-Runner in audit mode.
7. Optional merge automation such as Mergify.

Do not install multiple tools that post duplicate comments for the same finding
unless one is configured as advisory-only.

## Renovate Policy

`renovate.json` is the source of truth for Renovate behavior. Runtime dependency
majors and core KiCad/MCP ecosystem package updates require human review through
the dependency dashboard. Low-risk GitHub Actions and development tooling minor
or patch updates may be auto-merged only after required checks pass.

## Codecov Policy

`codecov.yml` defines project and patch targets. Repository coverage thresholds
must not be lowered to merge a feature. If a tool or fixture cannot run on a
local workstation, classify it as an environment limitation and rely on CI for
the authoritative signal.

## Semgrep Policy

Semgrep should start in advisory mode with repository-specific rules for:

- no privileged `workflow_run` secret access;
- no unsafe `pull_request_target` checkout pattern;
- no `subprocess` shell execution without a reviewed wrapper;
- no deprecated KiCad `pcbnew`/SWIG usage;
- no path traversal through export tools;
- no auth token leakage through health or doctor diagnostics.

Custom rules live under `.semgrep/`.

## StepSecurity Policy

Apply Harden-Runner first to workflows that touch release, publish, package,
mirror, or token-backed status publishing paths. Start with `egress-policy:
audit`; switch to block mode only after the required network allowlist is stable.

## AI Review Policy

- GitHub Copilot automatic review may be enabled through repository rulesets.
- Gemini Code Assist may provide advisory review comments.
- Jules is not a GitHub reviewer. Use Jules sessions or PR URLs to ask Jules to
  continue a PR.
- Do not add third-party AI review actions that require broad API keys on
  untrusted pull requests.

## Required Review Ownership

Use `.github/CODEOWNERS` for path-based review ownership. Workflow, security,
release, packaging, core implementation, tests, and documentation changes should
have explicit owners. If organization teams do not exist, use the repository
maintainer account until teams are created.

## Removal Criteria

Remove or disable an external app if any of the following is true:

- it requires broader permissions than justified by its signal;
- it creates repeated duplicate findings already covered by existing tools;
- it requires unsafe workflow patterns;
- it has no owner for triage;
- it has not produced useful signal for two release cycles.
