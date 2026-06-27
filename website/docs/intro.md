---
id: intro
title: Introduction
sidebar_position: 1
slug: /
---

# Argus Standards

**One command. Every AI coding agent. Consistent engineering standards.**

Argus is a Python CLI (`argus-standards`) that reads a single config file (`.argus.yml`) and generates platform-specific instruction files for every AI coding agent in your project. Engineering standards — TDD cycles, commit discipline, SOLID principles — live in composable **packs**. Platform-specific formatting is handled by **adapters**.

```bash
pip install argus-standards
argus init          # scaffold .argus.yml
argus generate      # write instruction files for every platform
```

## Why Argus?

When you work with multiple AI coding agents (Claude Code, Cursor, GitHub Copilot, OpenCode, Gemini CLI), each one reads from a different file. Without Argus, you maintain the same engineering rules in five separate places. With Argus, you maintain one config and one set of packs — Argus handles the rest.

## How It Works

1. **Packs** — composable bundles of engineering rules (TDD, SOLID, type safety, etc.)
2. **Platforms** — target agents (claude, cursor, copilot, opencode, gemini)
3. **`.argus.yml`** — your project config: which packs and platforms to use
4. **`argus generate`** — reads the config, applies packs through platform adapters, writes output files

## Supported Platforms

| Platform | Config reads from |
|----------|------------------|
| Claude Code | `CLAUDE.md`, `.claude/rules/` |
| Cursor | `.cursor/rules/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| OpenCode | `opencode.json`, `.opencode/` |
| Gemini CLI | `GEMINI.md` |

All platforms also receive `AGENTS.md` for cross-tool compatibility.

## Next Step

→ [Installation](./installation)
