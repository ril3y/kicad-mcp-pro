# Jules CI Bridge

This page is retained as a deployment-specific pointer. The current Jules
automation policy and workflow inventory live in
[Jules Automation](../automation/jules.md).

## Topology

```text
Jules workflow
  -> opens or updates PR on oaslananka-lab/kicad-mcp-pro
  -> org CI runs directly on the PR
  -> Jules CI Fixer can inspect same-repository failed workflow metadata
```

The canonical development repository is `oaslananka-lab/kicad-mcp-pro`. Do not
send Jules source work to `oaslananka/kicad-mcp-pro`; that repository receives
only mirrored `main` and version tags.

## Required configuration

Set this secret in `oaslananka-lab/kicad-mcp-pro`:

```text
JULES_API_KEY
```

## Workflows

Current Jules workflow files:

- `.github/workflows/jules-manual.yml`
- `.github/workflows/jules-ci-fixer.yml`
- `.github/workflows/jules-dependency-fixer.yml`
- `.github/workflows/jules-issue-agent.yml`

## Test sequence

1. Create a small docs-only PR through Jules.
2. Confirm the PR appears in `oaslananka-lab/kicad-mcp-pro`.
3. Confirm organization CI runs on the PR.
4. Force a harmless CI failure in a temporary branch and verify Jules CI Fixer
   can see the failed status before attempting a fix.

## Security constraints

- Never print `JULES_API_KEY`.
- Keep release publishing credentials outside Jules workflows.
- Do not run Jules from untrusted issue authors.
- Do not checkout or execute fork-origin PR code.
- CI Fixer may open or update PRs, but merge remains branch-protected and human
  reviewed.
