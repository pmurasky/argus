# Argus — AI Agent Engineering Standards Layer

## What This Is

A Python CLI (`pip install argus-standards`) that reads a project config (`.argus.yml`) and generates platform-specific instruction files for every AI coding agent in scope. Engineering standards — rules, workflows, checklists — live in composable **packs**. Platform-specific formatting is handled by **adapters**. One command generates everything.

## Core Value

One command, one config, all AI coding platforms — engineering discipline injected everywhere agents run.

## Requirements

### Validated

<!-- Shipped in v1.0 and confirmed working. -->

- ✓ User can define packs and platforms in `.argus.yml` — v1.0
- ✓ `argus generate` writes platform-specific files for all selected platforms — v1.0
- ✓ `argus generate --dry-run` previews files without writing — v1.0
- ✓ `argus generate --check` exits non-zero if output differs from disk (CI use) — v1.0
- ✓ `argus init` scaffolds a starter `.argus.yml` — v1.0
- ✓ `argus packs list/show` lets user discover available packs — v1.0
- ✓ `argus platforms list` lists supported platforms — v1.0
- ✓ `argus validate` validates config without generating — v1.0
- ✓ Custom packs loadable from `.argus/packs/` (project-local override) — v1.0
- ✓ 5 built-in packs: atomic-commit, tdd, solid, code-quality, pre-commit — v1.0
- ✓ 4 platform adapters: claude, opencode, copilot, cursor — v1.0

### Active

<!-- Current milestone scope — v1.1 -->

- PLT-01: User can generate GEMINI.md for Gemini CLI by adding `gemini` to `.argus.yml` platforms — Validated in Phase 18: Gemini CLI Adapter
- PACK-02: type-safety pack discoverable, renderable, injectable, no Argus-specific paths — Validated in Phase 19: Promoted Process Packs
- PACK-03: error-handling pack discoverable, renderable, injectable, no Argus-specific class names — Validated in Phase 19: Promoted Process Packs
- PACK-04: documentation-standards pack discoverable, renderable, injectable, no Argus-specific names — Validated in Phase 19: Promoted Process Packs
- PACK-01: security pack discoverable, renderable, injectable — OWASP Top 10 (2021) categories A01/A02/A03/A04/A07/A08 + Input Validation — Validated in Phase 20: Security Pack
- LANG-01: python language pack discoverable, renderable, injectable — pathlib idioms, zero mypy overlap — Validated in Phase 21: Python & TypeScript Language Packs
- LANG-02: typescript language pack discoverable, renderable, injectable — strict mode, noImplicitAny, no framework coupling — Validated in Phase 21: Python & TypeScript Language Packs
- LANG-03: go language pack discoverable, renderable, injectable — errors.Is/As, interface composition, goroutines, package naming — Validated in Phase 22: Go, Java & Kotlin Language Packs
- LANG-04: java language pack discoverable, renderable, injectable — modern types, Optional.orElseThrow, OOP patterns, exceptions — Validated in Phase 22: Go, Java & Kotlin Language Packs
- LANG-05: kotlin language pack discoverable, renderable, injectable — requireNotNull, coroutines, idiomatic Kotlin, K-over-Java idioms — Validated in Phase 22: Go, Java & Kotlin Language Packs
- FWRK-01: fastapi framework pack discoverable, renderable, injectable — async-first, Pydantic v2, DI patterns, APIRouter organization — Validated in Phase 23: Python & JavaScript Framework Packs
- FWRK-02: nextjs framework pack discoverable, renderable, injectable — App Router, server/client components, hooks discipline, TS integration — Validated in Phase 23: Python & JavaScript Framework Packs

### Out of Scope

| Feature | Reason |
|---------|--------|
| GUI / web interface | CLI-first; a GUI adds complexity without addressing the core problem |
| Pack authoring wizard | Text editor is sufficient; YAGNI until users request it |
| AI-assisted pack generation | Out of scope for v1.x; distraction from core delivery |

## Context

- **Ecosystem shift (2026):** AGENTS.md is now stewarded by the Linux Foundation, read natively by 28+ tools and in 60,000+ repos. AGENTS.md has become the primary cross-tool standard.
- **Platform gap:** Windsurf (`.windsurf/rules/*.md`), Zed (reads AGENTS.md natively), Aider, and JetBrains Junie are not yet supported. Gemini CLI (`GEMINI.md`) added in Phase 18.
- **Pack gap:** `awesome-cursorrules` has 163+ community rules. Argus has 5 process packs. Language/framework/security packs are the biggest unmet demand.
- **Skills.sh (Jan 2026):** npm-style skill package manager working across Claude Code, Codex CLI, Cursor — potential distribution channel for packs.
- **Architecture:** Clean SOLID design. New platform = one adapter file, no existing code changes. New pack = one new directory.
- **Test coverage:** 172 tests pass; coverage at 94.88% (above 80% threshold).
- **Version:** 0.1.1. PyPI CI workflow wired (tag-triggered publish).
- **Always run tests with `.venv/bin/pytest`** — system python3 doesn't have argus-standards installed.

## Constraints

- **Python**: 3.11+ — broad compatibility, modern type syntax
- **Zero mandatory dependencies beyond click + pyyaml** — keeps install lightweight
- **Pack format stays backward-compatible** — existing `.argus.yml` files must keep working
- **SOLID / TDD / type-safety rules** — enforced on every commit (see `.claude/rules/`)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Composable packs (not monolithic rules file) | Lets teams pick and mix standards; easier to maintain individually | ✓ Good |
| Platform adapters as strategy pattern | New platform = one file, zero existing changes | ✓ Good |
| Two-level pack search (custom → built-in) | Project-local overrides without forking | ✓ Good |
| AGENTS.md generated for all platforms | Cross-tool baseline everyone can read | ✓ Good |
| hatchling build backend | Modern, fast, zero config | ✓ Good |

---
*Last updated: 2026-06-26 — Phase 23 complete (FastAPI & Next.js Framework Packs); 172 tests passing at 94.88% coverage*
