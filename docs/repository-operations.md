# Repository Operations

## Repositories

- Canonical source-of-truth: `oaslananka-lab/kicad-mcp-pro`
- Personal showcase mirror: `oaslananka/kicad-mcp-pro`

The organization repository is the only source repository for CI/CD, release,
publishing, registry updates, package-manager updates, signing, SBOM generation,
and artifact attestations. The personal repository is a showcase mirror only.
If repository state differs, the organization repository wins.

## Showcase Mirror

The organization repository mirrors only `main` and version tags to the personal
showcase repository with `.github/workflows/mirror-personal.yml`.

Direction:

- `oaslananka-lab/kicad-mcp-pro` `main` branch to `oaslananka/kicad-mcp-pro` `main`
- `v*.*.*` tags from organization to personal showcase

The mirror does not sync pull request branches, release-please branches,
workflow run state, issues, or GitHub Releases. The mirror workflow uses
`PERSONAL_REPO_PUSH_TOKEN`, which must be scoped only to the personal showcase
repository. It does not use the default `GITHUB_TOKEN` for cross-repo writes.

## Actions Policy

Keep Actions enabled anywhere branch protection depends on them. Use least
privilege workflow permissions and protected environments rather than disabling
normal validation.

## Jules Automation

Jules may create or update fix branches and PRs in the organization repository
only. It must not publish releases, packages, registry entries, SBOMs, Sigstore
bundles, or attestations, and it must not merge PRs.

See [Jules Automation](automation/jules.md) for the workflow inventory,
security guards, required `JULES_API_KEY` secret, and disable commands.

## Manual Mirror

Review the mirror plan without writing to the personal repository:

```bash
gh workflow run mirror-personal.yml --repo oaslananka-lab/kicad-mcp-pro \
  -f dry_run=true \
  -f ref_scope=main-and-tags
```

Mirror after reviewing the plan:

```bash
gh workflow run mirror-personal.yml --repo oaslananka-lab/kicad-mcp-pro \
  -f dry_run=false \
  -f force_mirror=false \
  -f ref_scope=main-and-tags
```

The workflow refuses force updates unless `force_mirror=true`,
`approval=MIRROR_CANONICAL_TO_PERSONAL`, and a manual `workflow_dispatch` run are
used. Divergent tags should be recovered one tag at a time with `tag_name`.

See [Personal Showcase Mirror](automation/mirror-personal.md) for stale tag
recovery.

## Release Control Plane

The release control plane is manual-only and read-first:

- `scripts/release-state.mjs` reports release state, blockers, and the next safe
  command.
- `.github/workflows/release-controller.yml` dispatches the existing guarded
  release and mirror workflows only after state checks.
- `.github/workflows/actions-maintenance.yml` lists and classifies failed runs,
  reports stale deployments/tags, and can rerun infra-only failures when
  explicitly requested.

References:

- [Release controller](automation/release-controller.md)
- [Release state machine](release-state-machine.md)
- [Failure classifier](automation/failure-classifier.md)
- [Review thread gate](automation/review-thread-gate.md)

## Mirror Recovery

1. Confirm `PERSONAL_REPO_PUSH_TOKEN` exists in the organization repository and
   has access only to `oaslananka/kicad-mcp-pro`.
2. Run `.github/workflows/mirror-personal.yml` manually with `dry_run=true`.
3. Review `git log --oneline personal/main..HEAD` in the job log.
4. Re-run with `dry_run=false` after CI is green on the organization repository.

## Pending: OIDC Trusted Publishing

The current release pipeline publishes with `pypa/gh-action-pypi-publish` and
GitHub Actions OIDC. Long-lived PyPI tokens (`PYPI_TOKEN`, `TEST_PYPI_TOKEN`)
are not required by `.github/workflows/release.yml`.

Migration path:
1. Configure a trusted publisher in the PyPI project settings pointing to
   `oaslananka-lab/kicad-mcp-pro`, workflow `release.yml`, environment `release`.
2. Configure the matching trusted publisher in TestPyPI with the same owner,
   repository, workflow, and environment.
3. Keep `id-token: write` on the release workflow so PyPI can mint short-lived
   publish credentials during the protected `release` environment run.
4. Remove any remaining `PYPI_TOKEN` and `TEST_PYPI_TOKEN` secrets from the org
   repo after TestPyPI and PyPI trusted publishers are confirmed.

Blocked by: requires PyPI and TestPyPI account owner action to configure the
trusted publishers.

## Branch Cleanup

Review planned cleanup actions:

```bash
bash scripts/repo-cleanup.sh
```

Apply after reviewing the dry run:

```bash
bash scripts/repo-cleanup.sh --apply
```

The monthly `Branch hygiene report` workflow is report-only. It opens or updates an issue and does not delete branches.

## Auto-Delete Merged PR Branches

Recommended one-time setting on the organization repository:

```bash
gh api -X PATCH /repos/oaslananka-lab/kicad-mcp-pro -f delete_branch_on_merge=true
```
