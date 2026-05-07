# Personal Showcase Mirror

The canonical repository is:

```text
https://github.com/oaslananka-lab/kicad-mcp-pro
```

The personal showcase mirror is:

```text
https://github.com/oaslananka/kicad-mcp-pro
```

The personal repository is advisory and public-facing only. It is not a source
of truth for releases, package publishing, signing, registry updates, SBOMs, or
artifact attestations.

## What Mirrors

`mirror-personal.yml` mirrors only:

- `main`;
- `v*.*.*` tags.

It does not mirror pull request branches, release-please branches, issues,
workflow state, or GitHub Releases.

## Safe Default Behavior

Default automatic mode:

- fast-forwards personal `main` when safe;
- pushes missing version tags;
- refuses to clobber divergent tags;
- refuses non-fast-forward branch recovery unless explicitly approved.

Mirror failure must not invalidate a package release. A stale personal tag is a
showcase divergence, not a PyPI/TestPyPI build failure.

## Stale Tag Recovery

When the workflow reports:

```text
Personal showcase tag divergence detected.
```

review the canonical and personal refs first. If the organization repository is
confirmed canonical, run a manual recovery for the single tag:

```bash
gh workflow run mirror-personal.yml \
  --repo oaslananka-lab/kicad-mcp-pro \
  -f dry_run=false \
  -f force_mirror=true \
  -f ref_scope=tags \
  -f tag_name=v3.2.0 \
  -f approval=MIRROR_CANONICAL_TO_PERSONAL
```

The workflow uses `--force-with-lease` for manual force recovery and requires
the approval string. Do not run broad force updates for all tags.

No mirror force operation was triggered while this automation was implemented.
