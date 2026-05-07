# Repository Autonomy

This repository is configured for a dual-owner model.

## Ownership

- `oaslananka-lab/kicad-mcp-pro` is the canonical source-of-truth and release authority.
- `oaslananka/kicad-mcp-pro` is a personal showcase mirror.

Only the organization repository accepts source changes for release. The personal
repository receives one-way mirrors of `main` and `v*.*.*` tags for public
visibility.

## CI/CD Authority

Automation runs only on `oaslananka-lab/kicad-mcp-pro`:

- CI matrix
- Security scanning
- CodeQL
- Scorecard
- release automation
- documentation deploy
- image and Docker checks

The personal showcase repository should not run required GitHub Actions. If the
mirrored workflow files appear there, repository guards skip CI/CD, release,
publishing, registry, package-manager, signing, and deployment jobs.

## Secrets

Doppler project `all`, config `main` is the secret source of truth for
organization workflows that need Doppler-backed values. Mirror writes use
`PERSONAL_REPO_PUSH_TOKEN`, scoped only to the personal showcase repository.

## Automation Boundaries

Automation does not publish releases without an explicit manual input, a
release tag trigger configured in the organization repository, and the protected
`release` environment approval where required.
