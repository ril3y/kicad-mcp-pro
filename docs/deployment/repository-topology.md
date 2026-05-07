# Repository and CI/CD Topology

This project uses two GitHub repositories with different responsibilities:

- Canonical source and release authority: `https://github.com/oaslananka-lab/kicad-mcp-pro`
- Personal showcase mirror: `https://github.com/oaslananka/kicad-mcp-pro`

The organization repository owns code review, issues, security reporting,
release automation, package publishing, registry metadata, signing, SBOM output,
and artifact attestations. The personal repository is a read-only showcase
mirror for consumers.

## Trigger Policy

| Surface | Role | Trigger policy |
|---|---|---|
| GitHub org (`oaslananka-lab`) | Canonical source and CI/CD owner | CI and security run on `push`/`pull_request`; publish remains guarded |
| GitHub personal (`oaslananka`) | Showcase mirror | No required Actions; mirrored `main` and `v*.*.*` tags only |
| Azure DevOps | Manual fallback and release support | Manual only |
| GitLab | Manual fallback mirror | Manual only |

Because the same workflow files are mirrored to both GitHub repositories, push
events may appear in the personal repository UI. CI/CD, publishing, registry,
signing, package-manager, and release jobs are guarded with
`github.repository == 'oaslananka-lab/kicad-mcp-pro'`, so they do not execute
outside the organization repository.

## Recommended Remotes

Use explicit remotes so source pushes go to the canonical organization
repository. Treat the personal repository as a mirror target only.

```bash
git remote add github-org git@github.com:oaslananka-lab/kicad-mcp-pro.git
git remote add showcase git@github.com:oaslananka/kicad-mcp-pro.git
git remote add azure git@ssh.dev.azure.com:v3/oaslananka/open-source/kicad-mcp-pro
```

If a GitLab mirror is used, add it as a separate manual remote:

```bash
git remote add gitlab <gitlab-repository-url>
```

## Publishing

PyPI, TestPyPI, GHCR, MCP registry, Homebrew, Scoop, npm wrapper, GitHub
Releases, SBOM, provenance, signing, and attestations are emitted only from the
organization GitHub repository.

## Doppler Secrets

The recommended secret model is to store only `DOPPLER_TOKEN` in CI/CD systems and keep the actual release secrets in Doppler:

- PyPI Trusted Publishing configuration for workflow `release.yml` and
  environment `release`
- `SAFETY_API_KEY`
- `NPM_TOKEN`
- `OVSX_PAT`
- `VSCE_PAT`

GitHub organization workflows, Azure DevOps, and GitLab all use the same pattern: install the Doppler CLI, then execute sensitive commands through `doppler run -- ...` so Doppler injects secrets as environment variables at runtime.

Minimum setup:

- GitHub org repository secret: `DOPPLER_TOKEN`
- GitHub org repository secrets: `DOPPLER_PROJECT=all`, `DOPPLER_CONFIG=main`
- Azure DevOps secret variable or variable group entry: `DOPPLER_TOKEN`
- Azure DevOps variables: `DOPPLER_PROJECT=all`, `DOPPLER_CONFIG=main`
- GitLab CI/CD variable: `DOPPLER_TOKEN`
- GitLab CI/CD variables: `DOPPLER_PROJECT=all`, `DOPPLER_CONFIG=main`

Keep old native secrets such as `PYPI_TOKEN` and `TEST_PYPI_TOKEN` only for
local fallback publishing outside GitHub Actions. The canonical release workflow
uses OIDC Trusted Publishing.
