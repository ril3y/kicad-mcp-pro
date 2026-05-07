# Release Process

Releases use Conventional Commits and release-please as the canonical release PR
and changelog mechanism. Release Drafter is not used.

The release-please workflow requires `DOPPLER_GITHUB_SERVICE_TOKEN`. It fails
closed when the service token is missing so release PR creation does not fall
back to `GITHUB_TOKEN` and hide token-sync drift.

## Normal Release

1. Confirm CI, Security, CodeQL, docs, and release checks are green.
2. Merge the release-please PR.
3. Confirm the release tag was created and `.github/workflows/release.yml`
   started automatically in `oaslananka-lab/kicad-mcp-pro`.
4. Approve the protected `release` environment gate when publishing is enabled.
5. Confirm PyPI/TestPyPI publish, SBOM, checksums, Sigstore signing artifacts,
   and GitHub attestations.
6. Confirm docs deploy to the organization repository `gh-pages` branch and
   `https://oaslananka-lab.github.io/kicad-mcp-pro/` Pages site.
7. Post a short GitHub Discussions announcement.

## Manual Release Workflow

Run `.github/workflows/release.yml` from `oaslananka-lab/kicad-mcp-pro`.

Inputs:

- `version`: release tag, for example `v3.0.3`.
- `index`: `TestPyPI` or `PyPI`.
- `publish`: set to `true` only for actual registry publication.
- `approval`: set to `APPROVE_RELEASE` when `publish=true`.

The workflow validates the selected index and release target, runs tests and
security checks, builds artifacts, creates SBOM output, attests artifacts, and
publishes through PyPI Trusted Publishing only when
`publish=true` and the protected environment is approved. Doppler remains the
preferred source for syncing non-PyPI secret names into GitHub, but the release
workflow does not block on unrelated Doppler entries such as Codecov or Safety.

Tag pushes matching `v*.*.*` also start the release workflow. For tag-triggered
runs, `AUTO_RELEASE_PUBLISH` controls whether publishing occurs and defaults to
`false` when the repository variable is unset. `AUTO_RELEASE_INDEX` controls the
target index and defaults to `PyPI`.

There is no separate publish workflow. Publishing must not be triggered from
pull requests, forks, local shells, or agent automation.

## Hotfix

Use `hotfix/<issue>` for urgent security, data loss, or production blocking fixes. Cherry-pick to a maintained release branch only when that branch exists and has users.

## Version Metadata

Run this before release PR review if metadata changes are manual:

```bash
npm run metadata:sync
npm run metadata:check
```

`pyproject.toml` is the source of truth for `mcp.json` and `server.json`.
