# GitHub Marketplace App Policy

This repository uses a small, explicit set of GitHub Apps and Marketplace
integrations. New apps must improve a concrete gate or signal without expanding
secret exposure, write permissions, or pull request noise unnecessarily.

## Approved Categories

| Category | Preferred integration | Purpose | Required posture |
| --- | --- | --- | --- |
| Dependency automation | Renovate | Dependency update PRs and dashboard | Least-privilege repo access; no auto-merge for runtime majors |
| Coverage | Codecov | Coverage status and PR diff visibility | Upload tokenless when possible; no write token in PR jobs |
| CI runtime security | StepSecurity Harden-Runner / Actions Security | Runner process, file, and network visibility | Start in audit mode before block mode |
| Supply-chain risk | Socket Security | Malicious package, install script, and typosquat detection | Advisory signal only; do not duplicate Renovate policy |
| SAST/custom rules | Semgrep | Repository-specific security and policy rules | Read-only scan jobs; no untrusted PR secret access |
| Secret monitoring | GitGuardian or native secret scanning | Secret leak detection | False-positive allowlist must be documented |
| Repository hygiene | OpenSSF Scorecard / Allstar | Branch protection, permission, and policy drift | Issue-only or read-only reporting preferred |

## Rejected Patterns

Do not install or approve apps/actions that require any of the following without
an explicit security review:

- `pull_request_target` plus untrusted checkout and write credentials.
- `workflow_run` jobs that access secrets or publish status with privileged tokens.
- Generic AI review actions that require broad API keys on pull requests.
- Duplicate scanners that comment on the same findings already covered by an
  existing app.
- Apps that require organization-wide write access when repository-scoped access
  is sufficient.

## Required App Review Checklist

Before adding a new Marketplace app or GitHub App, record:

1. Exact app name and Marketplace URL.
2. Repository or organization scope.
3. Requested permissions and why each permission is required.
4. Events/triggers used by the app.
5. Whether secrets or write tokens are exposed to untrusted pull requests.
6. Expected PR/status signal and owner responsible for triage.
7. Rollback plan if the app generates noise or unsafe behavior.

## Recommended Baseline

The recommended free/OSS-friendly baseline for this repository is:

- Renovate for dependency update PRs.
- Codecov for coverage reporting.
- StepSecurity Harden-Runner in audit mode for sensitive workflows first.
- Socket Security for malicious dependency risk.
- Semgrep for repo-specific SAST/policy rules.
- GitGuardian or GitHub native secret scanning for secret monitoring.
- OpenSSF Scorecard and optionally Allstar for repository hygiene.

Do not treat app findings as automatic merge blockers until the false-positive
rate is understood and the triage owner is documented.

## CI/CD Safety Requirements

- Prefer `pull_request` with read-only permissions for untrusted PR checks.
- Do not combine untrusted code execution with write tokens.
- Keep `permissions:` explicit in workflows.
- Pin third-party actions according to repository workflow security policy.
- Prefer `workflow_dispatch` for privileged status publishing and mirror bridge
  jobs.
- Never use `workflow_run` for token-backed status publishing.

## Operational Ownership

| Area | Owner |
| --- | --- |
| Workflow/security app findings | Repository maintainer / security owner |
| Dependency PRs | Maintainer or dependency owner |
| Coverage regressions | Change author |
| Secret findings | Security owner |
| Release and package metadata drift | Release owner |

A Marketplace app that has not produced useful signal for two release cycles
should be removed or converted to advisory-only mode.
