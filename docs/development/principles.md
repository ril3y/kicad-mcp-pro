# Production Principles

KiCad MCP Pro is an automation boundary between LLM agents and deterministic EDA
artifacts. The repository therefore treats reproducibility, traceability and
security as product features, not as secondary CI concerns.

## Principles

### 1. Deterministic before autonomous

Agents may propose or execute workflows, but every manufacturing-impacting output
must be reproducible from checked-in source, pinned dependencies and recorded
commands. Release exports stay behind explicit quality gates.

### 2. Supported KiCad surfaces only

Runtime code must use supported KiCad surfaces: `kicad-cli`, `kicad-python` IPC,
or explicitly documented adapters. Deprecated SWIG/`pcbnew` imports are blocked
by `npm run compat:check`.

### 3. Least privilege by default

The default transport is stdio. HTTP/streamable HTTP deployments require explicit
host, origin and bearer-token choices. Diagnostics must report only whether
secrets are configured, never their values.

### 4. Fail closed, skip intentionally

Real KiCad CLI integration tests skip only when no real CLI is discoverable.
When a CLI is configured, smoke tests must fail on broken runtime behavior.
Security, lint, type and coverage gates are not softened to make automation pass.

### 5. Trace every agent action

Agent-created PRs must include exact commands run, relevant artifact paths,
KiCad CLI version output when applicable, and a statement that no gates were
relaxed.

### 6. Separate canonical and showcase responsibilities

The organization repository owns review, history, CI/CD, publishing, signing,
and release state. The personal repository is a showcase mirror only and must
not become a second automation authority.

## Quality levels

| Level | Meaning | Required evidence |
|---|---|---|
| L1 | Code compiles and unit tests pass locally | `test:unit`, lint, typecheck |
| L2 | Cross-platform package quality | Linux/macOS/Windows CI, package build, metadata sync |
| L3 | Runtime-validated KiCad integration | Real KiCad 10 CLI smoke, failure artifacts, structured errors |
| L4 | Production-grade release integrity | release-please, version preflight, SBOM, provenance, signed artifacts |
| L5 | Agent-safe autonomous maintenance | Jules/Copilot PR loops on the organization repo, policy-enforced gates |

The target for `main` is L4. Jules/autonomous flows are L5 only when they are
observable, reversible and still gated by protected branch policy.
