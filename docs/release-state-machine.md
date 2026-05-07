# Release State Machine

`scripts/release-state.mjs` reports the current release state and the next safe
command for `kicad-mcp-pro`. It is read-only and can be used locally or inside
`release-controller.yml`.

## States

- `no-release`: no release tag or release PR state is visible.
- `release-pr-open`: a release-please PR appears to be open.
- `release-pr-merged`: reserved for a future state that can observe the merge
  before the tag appears.
- `tag-created`: the version tag exists locally or on the canonical repository.
- `dry-run-success`: a successful release dry run or draft GitHub Release is
  visible.
- `testpypi-published`: the exact version exists on TestPyPI.
- `pypi-published`: the exact version exists on PyPI.
- `mirror-synced`: PyPI is published and the personal showcase mirror has the
  current main/tag state.
- `complete`: PyPI is published, GitHub Release is published, and the personal
  showcase mirror is synced.
- `blocked`: a release blocker was found.

## Blockers

The script reports blockers for conditions such as:

- metadata version drift across `pyproject.toml`, `mcp.json`, and `server.json`;
- missing canonical version tag;
- PyPI package visible without a matching GitHub Release;
- personal showcase tag divergence.

The controller stops when blockers exist.

## TestPyPI to PyPI Flow

The safe release sequence is:

1. Merge the release-please PR after CI is green.
2. Confirm the version tag exists.
3. Run `release-controller.yml` in `dry-run` mode.
4. Run `release-controller.yml` in `testpypi` mode with
   `approval=APPROVE_RELEASE`.
5. Verify TestPyPI smoke install.
6. Run `release-controller.yml` in `pypi` mode with `allow_pypi=true` and
   `approval=APPROVE_RELEASE`.
7. Mirror the personal showcase repository after the package release succeeds.

Production PyPI requires explicit approval because published files for a version
cannot be replaced safely.

## Old Failed Deployments

Failed deployments in the GitHub `release` environment are historical records.
Do not treat an old failed deployment as the current release state. Use the
latest relevant `release.yml` run, the GitHub Release for the tag, and package
index visibility for the exact version.

`actions-maintenance.yml` can list recent deployments, but it never deletes or
rewrites deployment history.
