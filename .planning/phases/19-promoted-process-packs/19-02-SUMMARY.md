---
phase: 19-promoted-process-packs
plan: "02"
subsystem: packs
tags: [integration-tests, error-handling, content-generalization, pack-promotion]
dependency_graph:
  requires: [19-01]
  provides: [PACK-03]
  affects: [tests/integration/test_generate.py, argus/packs/error-handling/]
tech_stack:
  added: []
  patterns: [TYPE_SAFETY_CONFIG pattern extended to ERROR_HANDLING_CONFIG]
key_files:
  created: []
  modified:
    - tests/integration/test_generate.py
    - argus/packs/error-handling/instructions.md
    - argus/packs/error-handling/checklist.md
    - argus/packs/error-handling/examples.md
decisions:
  - ERROR_HANDLING_CONFIG constant follows the established TYPE_SAFETY_CONFIG isolation pattern
  - Key phrase "system boundaries" chosen because it lives in Catching Rules (not changed by generalization)
  - examples.md replaced wholesale with AppError/ResourceNotFoundError/AppConfigError generic names
metrics:
  duration: "1 min"
  completed_date: "2026-06-24"
  tasks_completed: 2
  files_modified: 4
---

# Phase 19 Plan 02: Error-Handling Pack Integration Tests and Generalization Summary

**One-liner:** Integration tests for error-handling pack CLI (packs list/show/generate) plus generic AppError/ResourceNotFoundError names replacing all Argus-specific class names.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Add three integration tests for the error-handling pack | d60e6bd | tests/integration/test_generate.py |
| 2 | Generalize Argus-specific names in error-handling content | a867400 | argus/packs/error-handling/{instructions,checklist,examples}.md |

## What Was Built

### Task 1 — Integration Tests

Appended `ERROR_HANDLING_CONFIG` constant and three test functions to `tests/integration/test_generate.py`:

- `test_error_handling_pack_appears_in_packs_list` — verifies `argus packs list` exits 0 and includes "error-handling"
- `test_error_handling_pack_show_renders_content` — verifies `argus packs show error-handling` exits 0 and includes "system boundaries"
- `test_error_handling_pack_generate_injects_content` — verifies `argus generate` writes `.claude/rules/error-handling.md` containing "system boundaries"

### Task 2 — Content Generalization

Made surgical replacements in three pack files:

- `instructions.md`: `ArgusError` → `AppError`, `argus/__init__.py` → `app/__init__.py`
- `checklist.md`: `ArgusError` → `AppError`
- `examples.md`: Full rewrite replacing `ArgusError`/`PackNotFoundError`/`UnknownPlatformError`/`ArgusConfigError`/`adapter.generate(packs)`/`.argus.yml` with generic `AppError`/`ResourceNotFoundError`/`AppConfigError`/`service.process(items)`

## Verification Results

- `pytest tests/integration/test_generate.py -k error_handling -x --no-cov` — 3 passed
- `grep -rE "ArgusError|PackNotFoundError|UnknownPlatformError|ArgusConfigError|adapter\.generate|\.argus\.yml" argus/packs/error-handling/` — no matches (clean)
- `pytest --no-cov -q` — 145 passed (no regressions)

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED

- `tests/integration/test_generate.py` contains `ERROR_HANDLING_CONFIG`, all three test functions, and `.claude/rules/error-handling.md` reference
- `argus/packs/error-handling/examples.md` contains `class AppError` and `class ResourceNotFoundError(AppError)`
- `argus/packs/error-handling/instructions.md` contains `app/__init__.py` and `system boundaries`
- `argus/packs/error-handling/checklist.md` contains `AppError`
- Commits d60e6bd and a867400 exist in git log
