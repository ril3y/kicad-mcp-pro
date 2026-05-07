# Release Controller

`release-controller.yml` is a manual-only control plane for the release sequence
in the canonical repository, `oaslananka-lab/kicad-mcp-pro`. It never publishes
directly. It inspects state with `scripts/release-state.mjs` and then dispatches
the existing guarded workflows when the requested operation is safe.

The personal repository, `oaslananka/kicad-mcp-pro`, is a showcase mirror only.
It is never a release authority.

## Modes

- `dry-run`: dispatches `release.yml` with `publish=false` against TestPyPI
  settings. This builds, signs, attests, and stages release artifacts without
  uploading to a package index.
- `testpypi`: dispatches `release.yml` with `publish=true` and
  `index=TestPyPI`. It requires `approval=APPROVE_RELEASE`; the release workflow
  still uses the protected `release` environment.
- `pypi`: dispatches `release.yml` with `publish=true` and `index=PyPI`. It
  requires `approval=APPROVE_RELEASE`, `allow_pypi=true`, and an observed
  TestPyPI publication state.
- `mirror`: dispatches `mirror-personal.yml` without force after PyPI
  publication is observed.
- `full-safe`: runs the dry-run first, then dispatches TestPyPI only when
  approval is present. It stops before PyPI unless the PyPI approval guards are
  also present and TestPyPI is already observed as published.

## Production PyPI Gate

Production PyPI remains human-gated because it is irreversible for a given
version. The controller requires all of the following before it can dispatch the
PyPI publish path:

- release-state reports no blockers;
- TestPyPI already contains the exact version;
- `allow_pypi=true`;
- `approval=APPROVE_RELEASE`;
- the downstream `release.yml` run passes the protected `release` environment.

The controller does not bypass environment approval and does not add or use
long-lived PyPI tokens.

## Example Commands

Inspect state locally:

```bash
node scripts/release-state.mjs --version v3.2.1
```

Dispatch a release dry run:

```bash
gh workflow run release-controller.yml \
  --repo oaslananka-lab/kicad-mcp-pro \
  -f mode=dry-run \
  -f version=v3.2.1
```

Dispatch TestPyPI after reviewing the dry run:

```bash
gh workflow run release-controller.yml \
  --repo oaslananka-lab/kicad-mcp-pro \
  -f mode=testpypi \
  -f version=v3.2.1 \
  -f approval=APPROVE_RELEASE
```

Dispatch PyPI only after TestPyPI smoke succeeds:

```bash
gh workflow run release-controller.yml \
  --repo oaslananka-lab/kicad-mcp-pro \
  -f mode=pypi \
  -f version=v3.2.1 \
  -f allow_pypi=true \
  -f approval=APPROVE_RELEASE
```

No publish workflow was triggered while this automation was implemented.
