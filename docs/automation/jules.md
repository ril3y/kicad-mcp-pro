# Jules Automation

Jules automation is configured only for the canonical repository:

```text
https://github.com/oaslananka-lab/kicad-mcp-pro
```

The personal repository at `https://github.com/oaslananka/kicad-mcp-pro` is a
showcase mirror only. Jules must not treat it as a source or release authority.

## What Jules Can Do

- Create or update fix branches and pull requests.
- Diagnose same-repository CI failures.
- Consolidate dependency maintenance into a reviewed branch.
- Work on allowlisted issue labels from trusted maintainers.
- Add focused tests and documentation for the requested fix.

## What Jules Must Not Do

Jules must not publish or trigger release artifacts:

- PyPI or TestPyPI packages
- Docker or GHCR images
- npm packages
- Homebrew formulas
- Scoop manifests
- MCP registry entries
- GitHub Releases
- SBOMs
- Sigstore bundles
- GitHub artifact attestations

Jules also must not merge PRs, modify secrets or variables, weaken CI gates, or
change release/publish workflows unless a task explicitly requires a minimal
fix there.

## Required Secret

Set this secret in `oaslananka-lab/kicad-mcp-pro`:

```text
JULES_API_KEY
```

Never print the secret. Jules workflows pass it only to the pinned Jules action.

## Workflows

### `jules-manual.yml`

Manual dispatch for maintainer-selected work:

```bash
gh workflow run jules-manual.yml --repo oaslananka-lab/kicad-mcp-pro
```

Inputs select the starting branch, task type, prompt, and context depth.

### `jules-ci-fixer.yml`

Runs from `workflow_run` only when a same-repository validation workflow fails.
It ignores fork-origin runs, personal repositories, release/publish workflows,
Jules branches, Dependabot branches, and release-please branches.

The workflow uses `workflow_run` because it needs to see completed run metadata.
It never checks out or executes the failed branch inside the privileged workflow.

### `jules-dependency-fixer.yml`

Manual dependency consolidation:

```bash
gh workflow run jules-dependency-fixer.yml --repo oaslananka-lab/kicad-mcp-pro
```

The workflow asks Jules to inspect Dependabot and dependency-alert waves, update
lockfiles, classify risk, run validation, and open a PR only when green.

### `jules-issue-agent.yml`

Runs only when issue author `oaslananka` adds one of these labels:

- `jules`
- `bug`
- `ci-fix`
- `dependency-fix`

No fork code is checked out or executed.

## Validation Required On Jules PRs

Every Jules-created PR must report these commands:

```bash
corepack npm ci
uv sync --all-extras --frozen
uv run python -m pytest tests/unit/ -q
uv run ruff format --check src/ tests/ scripts/
uv run ruff check src/ tests/ scripts/
uv run python -m mypy src/kicad_mcp/
corepack npm run workflows:lint
uv run python scripts/validate_mcp_manifest.py
```

When Docker is available:

```bash
docker build -t kicad-mcp-pro:local .
docker run --rm kicad-mcp-pro:local --help
docker run --rm kicad-mcp-pro:local health --json
```

## Auto-Merge Policy

No Jules auto-merge or auto-approve workflow is enabled. Human review remains
required. A future auto-merge workflow would need strict path, size, status, and
publish-trigger guards before being considered.

## Disable Quickly

Disable all Jules workflows:

```bash
gh workflow disable jules-manual.yml --repo oaslananka-lab/kicad-mcp-pro
gh workflow disable jules-ci-fixer.yml --repo oaslananka-lab/kicad-mcp-pro
gh workflow disable jules-dependency-fixer.yml --repo oaslananka-lab/kicad-mcp-pro
gh workflow disable jules-issue-agent.yml --repo oaslananka-lab/kicad-mcp-pro
```

Re-enable with `gh workflow enable <workflow-file> --repo
oaslananka-lab/kicad-mcp-pro`.
