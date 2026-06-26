---
phase: 23-python-javascript-framework-packs
plan: "02"
subsystem: packs
tags: [nextjs, framework-pack, app-router, tdd]
dependency_graph:
  requires: [23-01]
  provides: [nextjs-pack]
  affects: [argus/packs/nextjs/]
tech_stack:
  added: []
  patterns: [isolation-config-constant, tdd-red-green]
key_files:
  created:
    - argus/packs/nextjs/pack.yml
    - argus/packs/nextjs/instructions.md
    - argus/packs/nextjs/checklist.md
    - argus/packs/nextjs/examples.md
  modified:
    - tests/integration/test_generate.py
decisions:
  - "use client chosen as key test phrase for nextjs pack — lives in instructions.md Server vs Client Components section, stable and unique"
  - "NEXTJS_CONFIG isolation constant follows FASTAPI_CONFIG and prior pack precedents"
  - "nextjs pack is App Router only — FORBIDDEN: pages/, getServerSideProps, getStaticProps (Pages Router)"
  - "nextjs pack has zero overlap with typescript pack — FORBIDDEN: noImplicitAny, strict mode, no-any"
metrics:
  duration: "3 min"
  completed: "2026-06-26"
  tasks_completed: 2
  files_changed: 5
---

# Phase 23 Plan 02: Next.js Framework Pack Summary

**One-liner:** Next.js App Router framework pack with server/client component rules, hooks discipline, and TypeScript integration using `'use client'` as the key integration test phrase.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Add NEXTJS_CONFIG and 3 failing tests (RED) | 75c8b4d | tests/integration/test_generate.py |
| 2 | Author nextjs pack files (GREEN) | abfd465 | argus/packs/nextjs/{pack.yml,instructions.md,checklist.md,examples.md} |

## What Was Built

- `argus/packs/nextjs/pack.yml` — pack manifest with `category: framework`
- `argus/packs/nextjs/instructions.md` — 4 content sections (App Router Conventions, Server vs Client Components, React Hooks Discipline, TypeScript Integration) + Red Flags closer; contains `'use client'` directive as key phrase
- `argus/packs/nextjs/checklist.md` — 12 pre-commit checkbox items covering routes, component defaults, hook discipline, TypeScript
- `argus/packs/nextjs/examples.md` — 4 Avoid/Prefer blocks: data fetching, `'use client'` placement, hook directive, speculative useMemo
- 3 integration tests in `tests/integration/test_generate.py` following the FASTAPI_CONFIG pattern

## Verification

- `.venv/bin/pytest tests/integration/test_generate.py -k nextjs -x -q` — 3 passed
- `.venv/bin/pytest -x -q` — 172 passed, full suite green

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED

- `argus/packs/nextjs/pack.yml` — FOUND
- `argus/packs/nextjs/instructions.md` — FOUND (contains `use client`, 5 H2 sections, no forbidden strings)
- `argus/packs/nextjs/checklist.md` — FOUND (12 `- [ ]` items)
- `argus/packs/nextjs/examples.md` — FOUND (contains `**Prefer**` and `**Avoid**`)
- Commit 75c8b4d — RED tests
- Commit abfd465 — GREEN pack files
