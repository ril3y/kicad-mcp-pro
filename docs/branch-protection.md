# Branch Protection

Rulesets are stored as code in `.github/rulesets/main.json`.

Create in the canonical organization repository:

```bash
gh api -X POST /repos/oaslananka-lab/kicad-mcp-pro/rulesets --input .github/rulesets/main.json
```

If the ruleset already exists, use the ruleset id:

```bash
gh api /repos/oaslananka-lab/kicad-mcp-pro/rulesets
gh api -X PUT /repos/oaslananka-lab/kicad-mcp-pro/rulesets/<id> --input .github/rulesets/main.json
```

The personal showcase mirror should not carry independent branch-protection
requirements that conflict with the organization repository. It receives
`main` and version tags from the guarded mirror workflow.

The current organization policy requires pull requests, one review, code owner
review, signed commits, and non-fast-forward protection.

`required_status_checks` is empty in the committed JSON by default. After the
organization workflows have run at least once, add the actual check names that
GitHub reports for this repository.
