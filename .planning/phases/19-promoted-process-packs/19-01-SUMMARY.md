---
phase: 19-promoted-process-packs
plan: 01
subsystem: testing
tags: [type-safety, mypy, integration-tests, packs, cli]

# Dependency graph
requires:
  - phase: 18-gemini-cli-adapter
    provides: integration test isolation pattern (local config constant per test group)
provides:
  - Three integration tests for type-safety pack (packs list / packs show / generate)
  - Generic mypy invocation in type-safety pack content (no Argus-specific paths)
affects: [20-promoted-process-packs, PACK-02]

# Tech tracking
tech-stack:
  added: []
  patterns: [TYPE_SAFETY_CONFIG local constant mirrors GEMINI_CONFIG isolation pattern for pack-specific integration tests]

key-files:
  created: []
  modified:
    - tests/integration/test_generate.py
    - argus/packs/type-safety/instructions.md
    - argus/packs/type-safety/checklist.md

key-decisions:
  - "TYPE_SAFETY_CONFIG constant used as an isolated config (not added to FULL_CONFIG) — mirrors GEMINI_CONFIG precedent from 18-02"
  - "mypy . chosen as the generic replacement over mypy <package>/ — simpler and more universally applicable"

patterns-established:
  - "Pack-specific integration tests use a dedicated local config constant, never FULL_CONFIG"

requirements-completed: [PACK-02]

# Metrics
duration: 5min
completed: 2026-06-24
---

# Phase 19 Plan 01: type-safety Pack Integration Tests and Generic Path Fix Summary

**Three integration tests proving type-safety pack is discoverable, renderable, and injectable via generate; Argus-specific `mypy argus/` path removed from pack content**

## Performance

- **Duration:** 5 min
- **Started:** 2026-06-24T01:47:30Z
- **Completed:** 2026-06-24T01:48:39Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Added `test_type_safety_pack_appears_in_packs_list`, `test_type_safety_pack_show_renders_content`, and `test_type_safety_pack_generate_injects_content` to the integration test suite
- Replaced `mypy argus/` with `mypy .` (or `mypy <your-project>/`) in `instructions.md` and `` `mypy .` exits 0 `` in `checklist.md`
- Full 142-test suite passes with no regressions

## Task Commits

Each task was committed atomically:

1. **Task 1: Add three integration tests for the type-safety pack** - `b8d49d9` (test)
2. **Task 2: Replace Argus-specific mypy path in type-safety content** - `724c020` (fix)

**Plan metadata:** (docs commit follows)

## Files Created/Modified

- `tests/integration/test_generate.py` - Added TYPE_SAFETY_CONFIG constant and three test functions
- `argus/packs/type-safety/instructions.md` - `mypy argus/` replaced with `mypy .` (or `mypy <your-project>/`)
- `argus/packs/type-safety/checklist.md` - `` `mypy argus/` `` replaced with `` `mypy .` ``

## Decisions Made

- TYPE_SAFETY_CONFIG constant used as an isolated config (not added to FULL_CONFIG) — mirrors GEMINI_CONFIG precedent from 18-02
- `mypy .` chosen as the generic replacement over `mypy <package>/` — simpler and more universally applicable

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. The three new integration tests passed immediately because the type-safety pack already existed and was fully functional — the tests verified existing behavior and then remained green after the content fix in Task 2.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- PACK-02 verified end-to-end through the CLI
- type-safety pack is now generic and usable in any project
- Ready for 19-02 (next pack promotion in the phase)

---
*Phase: 19-promoted-process-packs*
*Completed: 2026-06-24*
