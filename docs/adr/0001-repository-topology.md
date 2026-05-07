# ADR-0001: Repository Topology

**Status:** Accepted
**Date:** 2026-05-04
**Deciders:** @oaslananka

## Context

The project uses two repos:

- `oaslananka-lab/kicad-mcp-pro` - canonical source of truth and release authority.
- `oaslananka/kicad-mcp-pro` - personal showcase mirror.

The topology keeps public showcase visibility separate from the repository that
owns CI/CD, release, registry, package-manager, and signing authority.

## Decision

Maintain the dual-repo topology with the organization repository as canonical.
The organization repository contains all source changes and runs CI, security
scanning, release automation, docs deploy, publishing workflows, SBOM generation,
Sigstore signing, and artifact attestations.

Normal contributors open PRs against `oaslananka-lab/kicad-mcp-pro`. The
personal repository receives only one-way mirrors of `main` and version tags.

## Consequences

- Contributors need to understand that the organization repository owns code review and automation.
- Public health indicators must point at the organization repository workflows.
- The `docs/autonomy.md` document must accurately describe this boundary.
- Any future maintainer must have access to both repos.

## Verification

A new contributor can determine the topology from this ADR, `docs/autonomy.md`, and `docs/deployment/repository-topology.md` within 5 minutes.
