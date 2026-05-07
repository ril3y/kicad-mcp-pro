# Publishing

The canonical source and release authority is
`https://github.com/oaslananka-lab/kicad-mcp-pro`. The personal repository at
`https://github.com/oaslananka/kicad-mcp-pro` is a showcase mirror only.

All CI/CD, release, registry, package-manager, signing, provenance, and
attestation workflows are owned by the organization repository. The personal
repository must not be used as a release source.

## PyPI and TestPyPI

Python package releases use `.github/workflows/release.yml` in
`oaslananka-lab/kicad-mcp-pro`. The workflow builds the Python distributions,
creates release artifacts, generates SBOM and checksum files, signs artifacts
with Sigstore, creates GitHub artifact attestations, and publishes to PyPI or
TestPyPI only when the protected `release` environment and publish inputs allow
it.

Default safe settings:

- Manual dispatch defaults to `publish=false`.
- Tag-triggered release automation is gated by `AUTO_RELEASE_PUBLISH`.
- `AUTO_RELEASE_PUBLISH=false` keeps tag-triggered releases non-publishing.
- `AUTO_RELEASE_INDEX=TestPyPI` keeps automatic test runs off production PyPI.

The release workflow uses PyPI Trusted Publishing through GitHub Actions OIDC.
Repository secrets named `PYPI_TOKEN` and `TEST_PYPI_TOKEN` should not be needed
once PyPI and TestPyPI trusted publishers are configured.

## GitHub Releases

GitHub Release artifacts are produced by `.github/workflows/release.yml` in the
organization repository. Expected release assets include:

- Python wheel and source distribution under `dist/`
- `SHA256SUMS.txt`
- `bom.json` SBOM
- Sigstore signing artifacts
- GitHub artifact attestations attached to the release workflow run

Verification guidance lives in
[Release Integrity](security/release-integrity.md).

## GHCR Container Image

Container image publishing is handled by `.github/workflows/docker-publish.yml`
in the organization repository. The image name is:

```text
ghcr.io/oaslananka-lab/kicad-mcp-pro
```

Manual workflow dispatch builds without pushing unless `publish=true`.
Version-tag pushes and approved manual runs can publish images. Provenance
attestation runs only when an image was pushed.

Use the stdio image with MCP clients:

```bash
docker run --rm -i ghcr.io/oaslananka-lab/kicad-mcp-pro:latest
```

Run streamable HTTP explicitly:

```bash
docker run --rm -p 3334:3334 ghcr.io/oaslananka-lab/kicad-mcp-pro:latest kicad-mcp-pro serve --transport http --host 0.0.0.0 --port 3334
```

DockerHub publishing is not enabled. The configured DockerHub secrets are
reserved for a future explicitly gated workflow.

## MCP Registry

`server.json` is the official MCP registry manifest because the current MCP
registry documentation points publishers at the `server.json` schema hosted by
Model Context Protocol. `mcp.json` is kept as a compatibility manifest for
clients and registries that still expect the older repository-root metadata
shape.

Both files must remain synchronized with:

- `pyproject.toml` project name and version
- Canonical repository URL
- CLI command `kicad-mcp-pro`
- PyPI package metadata
- GHCR image metadata

Validation commands:

```bash
uv run python scripts/sync_mcp_metadata.py --check
uv run python scripts/validate_mcp_manifest.py
```

Publishing is handled by `.github/workflows/mcp-registry.yml`. The workflow
validates metadata on pull requests and relevant pushes. Real publishing is
manual only, requires `publish=true`, uses the protected `release` environment,
and requires `MCP_REGISTRY_TOKEN` when a token-backed target is configured.

If an official target is selected, the workflow uses `mcp-publisher` with
GitHub OIDC. If a generic or third-party target is selected without a configured
URL, the adapter fails fast instead of pretending to publish.

## Homebrew

Homebrew tap updates are scaffolded by
`.github/workflows/homebrew-publish.yml`. The workflow is manual only.

- `publish=false` prints the generated formula diff.
- `publish=true` creates a pull request against
  `oaslananka-lab/homebrew-tap`.
- The workflow uses `PACKAGE_MANAGER_TOKEN`.
- The workflow does not push directly to the tap `main` branch.

The formula installs from the PyPI source distribution using Homebrew's Python
virtualenv helper and generated Python resources.

## Scoop

Scoop bucket updates are scaffolded by `.github/workflows/scoop-publish.yml`.
The workflow is manual only.

- `publish=false` prints the generated manifest.
- `publish=true` creates a pull request against
  `oaslananka-lab/scoop-bucket`.
- The workflow uses `PACKAGE_MANAGER_TOKEN`.
- The workflow does not push directly to the bucket `main` branch.

The manifest references the PyPI wheel for version/hash metadata and installs
the Python package into the Scoop app directory at install time.

## npm Wrapper

The repository root `package.json` is private and exists only for hooks and CI
scripts. It must not be published to npm.

The optional npm wrapper lives under `npm-wrapper/`:

```text
npm-wrapper/package.json
npm-wrapper/bin/kicad-mcp-pro.js
```

The wrapper package name is `@oaslananka/kicad-mcp-pro`. It does not install
Python dependencies during `npm install`; at runtime it executes:

```bash
uvx kicad-mcp-pro
```

No npm publish workflow is enabled yet. npm trusted publishing is available, but
the package must be configured in npm before a guarded workflow is added.

## Required Configuration

Required GitHub environment:

- `release`

Required GitHub secrets:

- `MCP_REGISTRY_TOKEN`
- `PACKAGE_MANAGER_TOKEN`
- `PERSONAL_REPO_PUSH_TOKEN`
- `NPM_TOKEN` only if npm trusted publishing is not used for a future wrapper
  publish workflow

Required GitHub variables:

- `MCP_REGISTRY_URL`
- `AUTO_RELEASE_PUBLISH`
- `AUTO_RELEASE_INDEX`

## Install Examples

Linux and macOS:

```bash
uvx kicad-mcp-pro
pipx install kicad-mcp-pro
docker run --rm -i ghcr.io/oaslananka-lab/kicad-mcp-pro:latest
```

Windows PowerShell:

```powershell
uvx kicad-mcp-pro
pipx install kicad-mcp-pro
docker run --rm -i ghcr.io/oaslananka-lab/kicad-mcp-pro:latest
```

Claude Desktop stdio example:

```json
{
  "mcpServers": {
    "kicad-mcp-pro": {
      "command": "uvx",
      "args": ["kicad-mcp-pro"]
    }
  }
}
```

The CLI can also generate client snippets:

```bash
kicad-mcp-pro mcp-config generate --client claude
kicad-mcp-pro mcp-config generate --client cursor
kicad-mcp-pro mcp-config generate --client vscode
kicad-mcp-pro mcp-config generate --client codex
```

Container stdio example:

```json
{
  "mcpServers": {
    "kicad-mcp-pro": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "ghcr.io/oaslananka-lab/kicad-mcp-pro:latest"]
    }
  }
}
```
