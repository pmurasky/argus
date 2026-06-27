---
id: platforms
title: Platforms
sidebar_position: 6
---

# Platforms

A platform adapter controls which files get written and in what format. List the platforms you use in `.argus.yml`.

## Supported Platforms

| Platform | Key | Files Generated |
|----------|-----|-----------------|
| Claude Code | `claude` | `CLAUDE.md`, `.claude/rules/{pack}.md` |
| Cursor | `cursor` | `.cursor/rules/{pack}.md` |
| GitHub Copilot | `copilot` | `.github/copilot-instructions.md` |
| OpenCode | `opencode` | `opencode.json`, `.opencode/commands/{pack}.md` |
| Gemini CLI | `gemini` | `GEMINI.md` |

All platforms also receive `AGENTS.md` — the cross-tool baseline that OpenAI Codex and other tools read.

## Platform Details

### Claude Code (`claude`)

Generates:
- `CLAUDE.md` — top-level instructions Claude Code reads on startup
- `.claude/rules/{pack}.md` — one file per pack, auto-loaded by Claude Code

### Cursor (`cursor`)

Generates:
- `.cursor/rules/{pack}.md` — Cursor rule files, one per pack

### GitHub Copilot (`copilot`)

Generates:
- `.github/copilot-instructions.md` — single combined file (Copilot reads one file)

### OpenCode (`opencode`)

Generates:
- `opencode.json` — OpenCode configuration
- `.opencode/commands/{pack}.md` — one command file per pack

### Gemini CLI (`gemini`)

Generates:
- `GEMINI.md` — top-level instructions for Gemini CLI

## Checking Available Platforms

```bash
argus platforms list
```

## Detecting Installed Platforms

`argus init` detects which platforms are already active in your project and pre-selects them:

| Marker | Detected Platform |
|--------|------------------|
| `.claude/` directory | `claude` |
| `.cursor/` directory | `cursor` |
| `.github/copilot-instructions.md` | `copilot` |
| `.opencode/` directory | `opencode` |
| `GEMINI.md` file | `gemini` |

Undetected platforms appear commented out in `.argus.yml` for easy activation later.
