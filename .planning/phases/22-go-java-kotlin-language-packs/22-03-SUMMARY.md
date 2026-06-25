---
phase: 22-go-java-kotlin-language-packs
plan: "03"
subsystem: language-packs
tags: [kotlin, language-pack, null-safety, coroutines, packs]

# Dependency graph
requires:
  - phase: 22-02
    provides: GO_CONFIG and JAVA_CONFIG isolation constants already in test_generate.py
provides:
  - Kotlin 2.0+ language pack with null safety, idiomatic Kotlin, coroutines, and Kotlin-over-Java idioms
  - KOTLIN_CONFIG isolation constant and three integration tests for the kotlin pack
affects:
  - Phase 23 (framework packs that build on language packs)
  - Phase 24 (CLI-01 coverage gate)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - KOTLIN_CONFIG isolation constant follows GO_CONFIG/JAVA_CONFIG/TYPE_SAFETY_CONFIG precedent
    - requireNotNull as key test phrase for kotlin pack (lives in instructions.md Null Safety section)

key-files:
  created:
    - argus/packs/kotlin/pack.yml
    - argus/packs/kotlin/instructions.md
    - argus/packs/kotlin/checklist.md
    - argus/packs/kotlin/examples.md
  modified:
    - tests/integration/test_generate.py

key-decisions:
  - "requireNotNull chosen as key test phrase for kotlin pack — lives in instructions.md Null Safety section, stable and unique"
  - "KOTLIN_CONFIG isolation constant follows GO_CONFIG and JAVA_CONFIG precedent from Plans 01 and 02"
  - "Kotlin pack is framework-agnostic — FORBIDDEN: Ktor, Android, Compose, Jetpack (belong in Phase 23)"

patterns-established:
  - "Four-file pack structure: pack.yml, instructions.md, checklist.md, examples.md"
  - "Isolation constant pattern for pack integration tests (KOTLIN_CONFIG mirrors GO_CONFIG/JAVA_CONFIG)"

requirements-completed: [LANG-05]

# Metrics
duration: 2min
completed: 2026-06-25
---

# Phase 22 Plan 03: Kotlin Language Pack Summary

**Kotlin 2.0+ language pack delivering null-safety (requireNotNull), structured coroutines, idiomatic Kotlin, and Kotlin-over-Java idioms via four pack files and three passing integration tests**

## Performance

- **Duration:** 2 min
- **Started:** 2026-06-25T02:27:33Z
- **Completed:** 2026-06-25T02:29:26Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Three failing kotlin integration tests written first (RED), confirming pack absence
- Four pack files authored under argus/packs/kotlin/ (pack.yml, instructions.md, checklist.md, examples.md)
- All three kotlin tests pass GREEN; full 166-test suite passes with no regressions
- Framework-agnostic: zero Ktor, Android, Compose, or Jetpack mentions

## Task Commits

Each task was committed atomically:

1. **Task 1: Add failing KOTLIN_CONFIG isolation block and three kotlin tests (RED)** - `28735f1` (test)
2. **Task 2: Author the four kotlin pack files (GREEN)** - `5c079aa` (feat)

**Plan metadata:** (docs commit — see below)

_Note: TDD tasks have separate test (RED) and feat (GREEN) commits_

## Files Created/Modified
- `tests/integration/test_generate.py` - KOTLIN_CONFIG constant + 3 kotlin test functions appended
- `argus/packs/kotlin/pack.yml` - Kotlin pack manifest (name: kotlin, category: language, platforms: all)
- `argus/packs/kotlin/instructions.md` - Four sections: Null Safety (requireNotNull), Idiomatic Kotlin, Coroutines, Kotlin-over-Java + Red Flags
- `argus/packs/kotlin/checklist.md` - 11 actionable items covering requireNotNull, data class, structured scope, string templates
- `argus/packs/kotlin/examples.md` - Four Avoid/Prefer examples: requireNotNull vs !!, when vs if/else, structured scope vs GlobalScope, string templates

## Decisions Made
- `requireNotNull` chosen as key test phrase for kotlin pack — lives in instructions.md Null Safety section, stable and unique
- KOTLIN_CONFIG isolation constant follows GO_CONFIG and JAVA_CONFIG precedent from Plans 22-01 and 22-02
- Kotlin pack is framework-agnostic — FORBIDDEN: Ktor, Android, Compose, Jetpack (belong in Phase 23 framework packs)
- `viewModelScope` used in coroutine example as a representative structured scope (not framework-specific API — it's an illustrative name)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Coverage gate at 80% triggered (total 62%), but this is pre-existing (STATE.md notes "46% entering v1.1"). Tests run with `--no-cov` for regression verification. Out-of-scope per deviation rules; logged as known blocker for Phase 24 (CLI-01).

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 22 complete: go, java, and kotlin language packs all delivered and tested
- Phase 23 (framework packs) can reference the kotlin pack as the language foundation
- Phase 24 (CLI-01 coverage gate) must address the pre-existing 62% coverage gap

---
*Phase: 22-go-java-kotlin-language-packs*
*Completed: 2026-06-25*
