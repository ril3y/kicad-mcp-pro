# Testing Guide - kicad-mcp-pro

## Overview

kicad-mcp-pro uses **pytest** with the **uv** toolchain. Tests are organised into
three layers:

| Layer | Path | Description |
|---|---|---|
| Unit | `tests/unit/` | Pure Python, no KiCad dependency |
| Integration | `tests/integration/` | Requires kicad-cli in PATH |
| Smoke | `tests/smoke/` | End-to-end MCP protocol over stdio |

## Running Tests Locally

```bash
# Install all extras (includes test deps)
uv sync --all-extras --frozen

# Unit tests only (fast, no KiCad needed)
uv run pytest tests/unit/ -v

# Full suite (requires KiCad installed)
uv run pytest -v

# With coverage
uv run pytest --cov=kicad_mcp_pro --cov-report=term-missing
```

## CI Matrix

Tests run against Python **3.12**, **3.13**, **3.14** on
`ubuntu-latest`, `macos-latest`, `windows-latest` (9-job matrix).

## Fixtures

KiCad project fixtures live in `tests/fixtures/`. See
`docs/development/contributing-fixtures.md` for how to add new ones.
Convention: one directory per test scenario, named `<scenario>/`.

## Mutation Testing

Mutation tests run weekly via `.github/workflows/mutation.yml` using
**mutmut**. Check the Actions tab for the latest mutation score. Target
is **>= 70% survived mutations caught**.

## Mocking Strategy

- `conftest.py` root: common fixtures (temp dirs, fake KiCad stubs)
- KiCad CLI is mocked via `unittest.mock.patch` in unit tests
- Integration tests spin up a real `kicad-cli` process (Linux CI only)

## Adding a Test

1. Pick the correct layer (unit if no KiCad needed).
2. Create `tests/<layer>/test_<module>.py`.
3. Follow Arrange-Act-Assert pattern.
4. Run `uv run pytest tests/<layer>/test_<module>.py -v` locally.
5. Ensure `uv run ruff check tests/` passes.
