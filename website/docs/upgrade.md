---
id: upgrade
title: Upgrade
sidebar_position: 5
---

# Upgrade

## Upgrade the Package

```bash
pip install --upgrade argus-standards
```

## Detect Out-of-Date Files

After upgrading, your generated files (`.claude/rules/`, `AGENTS.md`, etc.) may differ from what the new version would generate. Use `argus upgrade` to check:

```bash
argus upgrade
```

If files are current:
```
✓ All generated files are up to date.
```

If files are stale, Argus lists the affected files and offers to regenerate:
```
  • .claude/rules/tdd.md
  • .claude/rules/solid.md
  • AGENTS.md

Regenerate now? [y/N]:
```

Type `y` to regenerate all stale files. Type `n` (or press Enter) to skip.

## CI Mode

In CI environments (where `CI=true` is set), `argus upgrade` exits non-zero immediately when files are stale — no prompt. Use this to enforce freshness:

```yaml
# .github/workflows/ci.yml
- run: argus upgrade
  env:
    CI: 'true'
```

This fails the CI run if anyone commits without regenerating after a pack or platform change. See [CI Integration](./ci-integration) for the full workflow.

## When to Run `argus upgrade`

- After `pip install --upgrade argus-standards`
- After adding a new pack or platform to `.argus.yml`
- After modifying a custom pack in `.argus/packs/`
