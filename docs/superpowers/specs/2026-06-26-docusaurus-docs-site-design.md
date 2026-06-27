# Docusaurus Documentation Site — Design Spec

**Date:** 2026-06-26
**Project:** argus-standards
**Status:** Approved

---

## Overview

Add a Docusaurus documentation site inside the `argus-standards` repo (`website/` folder), deployed to GitHub Pages at `https://pmurasky.github.io/argus/`. The site serves both end users (installing and using Argus) and contributors (adding packs and platform adapters). Pack reference pages are auto-generated from source — never hand-maintained.

---

## Site Structure

```
website/
├── docusaurus.config.ts
├── sidebars.ts
├── package.json
├── static/
│   └── img/                   # Logo, favicon
├── src/
│   └── css/
│       └── custom.css         # Detroit Lions color theme
└── docs/
    ├── intro.md
    ├── installation.md
    ├── quick-start.md
    ├── upgrade.md
    ├── configuration.md
    ├── platforms.md
    ├── ci-integration.md
    ├── contributing/
    │   ├── adding-a-pack.md
    │   └── adding-a-platform.md
    └── packs/                 # AUTO-GENERATED — gitignored
        ├── _category_.json
        └── {name}.md × 22
```

`website/docs/packs/` is listed in `.gitignore`. It is regenerated at build time by `scripts/gen-pack-docs.py`.

---

## Navigation

**Navbar:** `Docs` | `Packs` | `GitHub` (external)

**Sidebar order:**
1. Introduction
2. Installation
3. Quick Start
4. Configuration (`.argus.yml` reference)
5. Upgrade (`argus upgrade`)
6. Platforms
7. CI Integration
8. Packs *(auto-generated, grouped by category)*
   - Process (tdd, atomic-commit, solid, code-quality, pre-commit, error-handling, type-safety, documentation-standards, dependency-injection, design-patterns, refactoring, testing-strategy, security)
   - Languages (python, typescript, go, java, kotlin)
   - Frameworks (fastapi, nextjs, spring, mockito)
9. Contributing
   - Adding a Pack
   - Adding a Platform Adapter

---

## Detroit Lions Color Theme

| Role | Color | Hex |
|------|-------|-----|
| Primary (links, active nav, buttons) | Honolulu Blue | `#0076B6` |
| Primary dark (hover) | Deep Blue | `#005A8E` |
| Primary darker (pressed) | Navy | `#004470` |
| Accent / highlight | Silver | `#B0B7BC` |
| Background | White | `#FFFFFF` |
| Dark mode background | Near-black | `#1A1A1A` |
| Dark mode primary | Bright Blue | `#1A9FE0` |

**Applied to:**
- Navbar: `#0076B6` background, white text
- Active sidebar item: `#0076B6`
- Code block header: `#000000` with white text
- Buttons / CTAs: `#0076B6` → hover `#005A8E`
- Footer: `#000000` background, white text, blue links
- Admonition "tip" accent: `#B0B7BC`

Implemented via `src/css/custom.css` overriding Docusaurus's `--ifm-color-primary-*` CSS custom properties.

---

## Pack Page Generation

**Script:** `scripts/gen-pack-docs.py`

Invoked automatically as part of `npm run build` (via `scripts.prebuild` in `package.json`).

**Algorithm:**
1. Walk `argus/packs/*/`
2. For each pack, read `pack.yml` (name, description, category, requires, platforms) and `instructions.md`
3. Write `website/docs/packs/{name}.md`:

```markdown
---
id: {name}
title: {Name}
sidebar_label: {Name}
---

# {Name}

> {description}

| Field | Value |
|-------|-------|
| Category | {category} |
| Requires | {requires or "none"} |
| Platforms | {platforms} |

---

{full instructions.md content verbatim}
```

4. Write `website/docs/packs/_category_.json` grouping packs under "Packs"

**Sidebar sub-grouping** (via `_category_.json` + frontmatter `custom_edit_url: null`):
- Process packs (category: process)
- Language packs (category: language)
- Framework packs (category: framework)

---

## GitHub Pages Deployment

**File:** `.github/workflows/deploy-docs.yml`
**Trigger:** Push to `main`

**Steps:**
1. Checkout repo
2. Set up Python 3.11, install `argus-standards` in dev mode
3. Run `python scripts/gen-pack-docs.py`
4. Set up Node 20, `cd website && npm ci`
5. `npm run build` (which also re-runs the gen script via `prebuild`)
6. Deploy `website/build/` to `gh-pages` branch via `peaceiris/actions-gh-pages`

**GitHub repo setting required:** Pages source → `gh-pages` branch, `/ (root)` folder.

---

## Content Outline

| Page | Key Content |
|------|-------------|
| `intro.md` | What Argus is, one-command generate, supported platforms, link to Quick Start |
| `installation.md` | `pip install argus-standards`, Python 3.11+ requirement, verify with `argus --version` |
| `quick-start.md` | `argus init` → edit `.argus.yml` → `argus generate`, show example output files |
| `configuration.md` | Full `.argus.yml` schema, `packs` list, `platforms` list, custom packs path |
| `upgrade.md` | `argus upgrade` command, interactive mode, CI mode (`CI=true` env var) |
| `platforms.md` | Table of platforms + files generated per platform, including AGENTS.md |
| `ci-integration.md` | `argus generate --check` in GitHub Actions, `argus upgrade` in CI |
| `adding-a-pack.md` | `pack.yml` schema, `instructions.md` conventions, testing with `packs show` |
| `adding-a-platform.md` | Adapter protocol/ABC, entry-point registration in `pyproject.toml`, writing tests |

---

## Constraints

- Docusaurus 3.x (latest stable)
- Node 20 LTS
- No versioning — single latest docs
- `website/docs/packs/` must be gitignored (generated at build time)
- Script must be idempotent — safe to run multiple times
- Site URL base: `/argus/` (GitHub Pages project site, not user/org site)
