---
id: configuration
title: Configuration
sidebar_position: 4
---

# Configuration

Argus is configured by a single file: `.argus.yml` in your project root.

## Schema

```yaml
packs:
  - tdd
  - atomic-commit
platforms:
  - claude
  - cursor
```

### `packs`

A list of pack names to include. Order does not matter.

Run `argus packs list` to see all available packs, or browse the [Packs](/packs/workflow/tdd) section of this documentation.

```yaml
packs:
  - tdd           # TDD cycle enforcement
  - atomic-commit # One logical change per commit
  - solid         # SOLID principles
  - code-quality  # Complexity + size limits
  - pre-commit    # Pre-commit gate combining all standards
```

### `platforms`

A list of platform adapter names. Each platform generates its own set of instruction files.

```yaml
platforms:
  - claude    # CLAUDE.md + .claude/rules/
  - cursor    # .cursor/rules/
  - copilot   # .github/copilot-instructions.md
  - opencode  # opencode.json + .opencode/
  - gemini    # GEMINI.md
```

See [Platforms](./platforms) for a full list of generated files per platform.

## Custom Packs

Place your own packs in `.argus/packs/{name}/` at your project root. Custom packs are discovered before built-in packs, so they override built-ins with the same name.

```
your-project/
└── .argus/
    └── packs/
        └── my-team-standards/
            ├── pack.yml
            └── instructions.md
```

`pack.yml` for a custom pack:

```yaml
name: my-team-standards
description: Internal coding conventions
category: process
requires: []
platforms: [all]
```

## Validate Without Generating

```bash
argus validate
```

Checks that `.argus.yml` references valid packs and platforms, and exits non-zero if anything is wrong. Useful as a lightweight CI check.

## Example Configs

### Minimal (Python project, Claude only)
```yaml
packs:
  - tdd
  - solid
  - python
platforms:
  - claude
```

### Full stack (TypeScript + Spring backend)
```yaml
packs:
  - tdd
  - atomic-commit
  - solid
  - code-quality
  - pre-commit
  - typescript
  - spring
  - testing-strategy
platforms:
  - claude
  - cursor
  - copilot
```
