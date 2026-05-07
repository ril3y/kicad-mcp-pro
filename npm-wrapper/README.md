# @oaslananka/kicad-mcp-pro

This package is a thin npm wrapper for the Python package `kicad-mcp-pro`.

It does not install Python dependencies during `npm install`. At runtime, the
wrapper executes:

```bash
uvx kicad-mcp-pro
```

Install `uv` first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then run:

```bash
npx @oaslananka/kicad-mcp-pro --help
npx @oaslananka/kicad-mcp-pro health --json
```

The canonical repository and release authority is
`https://github.com/oaslananka-lab/kicad-mcp-pro`. The personal repository at
`https://github.com/oaslananka/kicad-mcp-pro` is a showcase mirror.
