# Azure DevOps Manual CI/CD

Azure DevOps is a manual compatibility fallback and release-support surface for
teams that mirror this repository into Azure DevOps. Automated GitHub CI/CD is
owned by the `oaslananka-lab` organization mirror, while the personal
`oaslananka` GitHub repository remains the main source repository.

## Pipeline Definition

The compatibility Azure pipeline definitions live under `.azure/pipelines/`.
The canonical CI pipeline remains `.github/workflows/ci.yml`; Azure files are
not the authoritative project CI.

It covers:

- `Validate`: `uv sync`, `ruff`, `mypy`, and `pytest` with a `--cov-fail-under=70` gate
- `Build`: `uv build` and artifact publication for the generated `dist/` output
- `Publish`: optional manual release to TestPyPI or PyPI using Azure-managed secrets

## Recommended Azure Variables

Preferred setup: store a single Doppler service token in Azure DevOps and let the pipeline fetch release secrets at runtime:

- `DOPPLER_TOKEN`

Doppler should contain:

- `PYPI_TOKEN`
- `TEST_PYPI_TOKEN`
- `SAFETY_API_KEY`

The compatibility Azure publish pipeline still supports native Azure variables
as a fallback:

- `PYPI_TOKEN`
- `TEST_PYPI_TOKEN`
- `SAFETY_API_KEY`

You can store these in a variable group if you want to share them across multiple pipelines.

## Release Model

- Automated GitHub CI/security jobs should run from `https://github.com/oaslananka-lab/kicad-mcp-pro`.
- Azure DevOps should be queued manually when you need the Azure validation or release-support path.
- Package publication should always be queued manually when you are ready to release.
- The personal GitHub repository should not run automatic CI/CD jobs.

## GitHub Workflows

The repository includes GitHub workflows that are automatic only in the
`oaslananka-lab` organization mirror and manual elsewhere:

- `.github/workflows/ci.yml`
- `.github/workflows/security.yml`
- `.github/workflows/release.yml`

Release publishing is handled by `.github/workflows/release.yml` in the org repo
through PyPI Trusted Publishing.
