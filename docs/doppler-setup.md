# Doppler Setup

This repository expects Doppler project `all`, config `main`.

## Manually Required GitHub Secret

Set exactly one GitHub secret manually in the organization repository:

- `DOPPLER_TOKEN`

The token must be a read-only Doppler service token scoped to project `all`, config `main`.

Set it in `oaslananka-lab/kicad-mcp-pro`. The organization repository may
inherit the secret from the organization if that is easier to maintain.

Other secret names, including `DOPPLER_GITHUB_SERVICE_TOKEN`,
`PERSONAL_REPO_PUSH_TOKEN`, and `SAFETY_API_KEY`, may be present as GitHub
Actions secrets at runtime. Prefer projecting them into GitHub by Doppler GitHub
Sync. Release publishing uses PyPI Trusted Publishing and does not require
long-lived PyPI tokens in GitHub Actions.

`CODECOV_TOKEN` is maintained as an organization-level selected GitHub secret
for coverage upload only. Do not store or fetch a Codecov API token for CI.

## Doppler GitHub Sync

In the Doppler dashboard:

1. Open project `all`, config `main`.
2. Install the GitHub integration for `oaslananka-lab`.
3. Create a sync to `oaslananka-lab/kicad-mcp-pro` repository secrets.
4. Use replace mode so GitHub remains a projection of Doppler, not a second source of truth.

## Required Secrets

The authoritative secret-name list lives in this document rather than a dotfile
so scanner exclusions do not need to hide a `.doppler/` directory.

Current expected Doppler-backed names:

- `DOPPLER_GITHUB_SERVICE_TOKEN`
- `PERSONAL_REPO_PUSH_TOKEN`
- `SAFETY_API_KEY`

Usage:

- `DOPPLER_GITHUB_SERVICE_TOKEN`: least-privilege GitHub service token for release-please PR creation when organization policy blocks `GITHUB_TOKEN` from opening pull requests.
- `PERSONAL_REPO_PUSH_TOKEN`: fine-grained token scoped only to `oaslananka/kicad-mcp-pro` for the one-way showcase mirror.
- `SAFETY_API_KEY`: optional authenticated Safety scan. It is not required for local default gates.

GitHub-only selected secret:

- `CODECOV_TOKEN`: optional Codecov coverage upload token used only by `.github/workflows/ci.yml`. Pull requests from forks receive no token and may use Codecov's public tokenless upload behavior.

Legacy local-only fallback names, not required by GitHub Actions after Trusted
Publishing migration:

- `PYPI_TOKEN`
- `TEST_PYPI_TOKEN`

No workflow or diagnostic output should print secret values.

## Verification

```bash
bash scripts/verify_doppler_secrets.sh
```

This command requires the Doppler CLI and a local login or `DOPPLER_TOKEN`.
