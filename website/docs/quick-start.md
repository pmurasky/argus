---
id: quick-start
title: Quick Start
sidebar_position: 3
---

# Quick Start

Get from zero to generated files in under two minutes.

## Step 1: Initialize

Run in your project root:

```bash
argus init
```

This creates `.argus.yml` and detects which platforms are already installed (e.g., if `.claude/` exists, `claude` is pre-selected).

Example output:
```
✓ Written: .argus.yml
Edit .argus.yml to select packs and platforms, then run: argus generate
```

## Step 2: Edit `.argus.yml`

Open `.argus.yml` and choose your packs and platforms:

```yaml
packs:
  - tdd
  - atomic-commit
  - solid
  - code-quality
  - pre-commit
platforms:
  - claude
  - cursor
```

See [Packs](/packs/workflow/tdd) for the full list of available packs and [Platforms](./platforms) for available platforms.

## Step 3: Generate

```bash
argus generate
```

Argus reads `.argus.yml`, applies each pack through the platform adapters, and writes the output files.

Example output for `claude` + `cursor` platforms:
```
Writing CLAUDE.md
Writing .claude/rules/tdd.md
Writing .claude/rules/atomic-commit.md
Writing .claude/rules/solid.md
Writing .claude/rules/code-quality.md
Writing .claude/rules/pre-commit.md
Writing .cursor/rules/tdd.md
Writing .cursor/rules/atomic-commit.md
...
Writing AGENTS.md
```

## Step 4: Commit the output files

The generated files should be committed to your repository so every contributor and every agent gets the same rules:

```bash
git add CLAUDE.md .claude/ .cursor/ AGENTS.md
git commit -m "chore: add Argus engineering standards"
```

## What's Next

- Run `argus packs list` to see all available packs
- Run `argus packs show tdd` to preview what a pack injects
- Run `argus generate --dry-run` to preview output without writing files
- See [CI Integration](./ci-integration) to enforce freshness in CI
