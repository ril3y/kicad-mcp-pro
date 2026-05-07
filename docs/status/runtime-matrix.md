# Runtime Matrix

This matrix describes the supported runtime surface for KiCad MCP Pro.

## Python

| Python | Status | Notes |
|---|---|---|
| 3.12 | Tested | Primary package and Docker runtime. |
| 3.13 | Tested | Covered by CI for pure Python behavior. |
| 3.14 | Preview | Used by selected signing/tooling paths; runtime support is best effort until Python 3.14 is stable in downstream tooling. |

## Operating Systems

| Platform | Status | Notes |
|---|---|---|
| Linux | Tested | Primary CI and container platform. |
| macOS | Tested | Homebrew workflow generation runs on macOS. |
| Windows | Tested | PowerShell, path handling, and CLI smoke tests run in CI. |

## KiCad Availability

| KiCad CLI | Status | Behavior |
|---|---|---|
| Present | Full | CLI-backed exports, validation, and diagnostics can run. |
| Missing | Degraded | `health --json` and most metadata/config commands still work. IPC-dependent tools report unavailable state instead of crashing. |

## Transports

| Transport | Status | Invocation |
|---|---|---|
| stdio | Default | `uvx kicad-mcp-pro` or `docker run --rm -i ghcr.io/oaslananka-lab/kicad-mcp-pro:latest` |
| streamable-http | Supported | `kicad-mcp-pro serve --transport http --host 0.0.0.0 --port 3334` |

HTTP mode should be bound only on trusted networks unless authentication,
network policy, and CORS are configured.

## MCP Clients

| Client | Status | Notes |
|---|---|---|
| Claude Desktop | Supported | Use stdio with `uvx kicad-mcp-pro`. |
| Cursor | Supported | Use stdio with absolute project paths when setting project environment variables. |
| VS Code MCP | Supported | Use stdio with a `servers` configuration entry. |
| Codex | Supported | Use stdio configuration for local agent workflows. |
| Claude Code | Supported | Use stdio configuration; see the integration guide. |

## Containers

The default container image does not bundle KiCad. It is suitable for stdio MCP
usage, metadata commands, and host-mounted or externally configured KiCad CLI
paths. Install KiCad on the host or use a dedicated CI image when full CLI export
coverage is required inside the container.
