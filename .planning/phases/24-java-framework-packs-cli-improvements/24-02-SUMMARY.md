---
phase: 24-java-framework-packs-cli-improvements
plan: 02
subsystem: testing
tags: [mockito, java, mocking, junit5, bdd, tdd]

# Dependency graph
requires:
  - phase: 24-01
    provides: spring pack pattern (same test file, sequential ownership)
provides:
  - Mockito 5.x framework pack with mock-mechanics-only content
  - 3 integration tests for mockito pack (list, show, generate)
  - ArgumentCaptor, @Mock vs @Spy, verify patterns, BDDMockito coverage
affects: [24-03, future-java-framework-packs]

# Tech tracking
tech-stack:
  added: []
  patterns: [MOCKITO_CONFIG isolation constant follows prior pack precedents]

key-files:
  created:
    - argus/packs/mockito/pack.yml
    - argus/packs/mockito/instructions.md
  modified:
    - tests/integration/test_generate.py

key-decisions:
  - "ArgumentCaptor chosen as key test phrase for mockito pack — lives in instructions.md Argument Captors section, stable and unique"
  - "MOCKITO_CONFIG isolation constant follows SPRING_CONFIG and prior pack precedents"
  - "Mockito pack: mock-mechanics only — FORBIDDEN: @MockBean, @SpyBean (Spring), @RunWith (JUnit 4)"

patterns-established:
  - "Mockito pack scope: @ExtendWith(MockitoExtension.class) for JUnit 5/6, never JUnit 4 @RunWith"
  - "No Spring test annotation overlap: @MockBean/@SpyBean belong to spring pack only"

requirements-completed: [FWRK-04]

# Metrics
duration: 4min
completed: 2026-06-26
---

# Phase 24 Plan 02: Mockito Framework Pack Summary

**Mockito 5.x framework pack with @Mock vs @Spy, ArgumentCaptor, verify patterns, and BDDMockito — mock-mechanics only, zero Spring test annotation overlap**

## Performance

- **Duration:** 4 min
- **Started:** 2026-06-26T23:30:00Z
- **Completed:** 2026-06-26T23:34:00Z
- **Tasks:** 2 (TDD: RED + GREEN)
- **Files modified:** 3

## Accomplishments
- Authored Mockito 5.x framework pack with 5 H2 sections: Setup, @Mock vs @Spy, Argument Captors, Verify Patterns, Classic and BDD Style
- 3 integration tests (list, show, generate) all pass; full suite 178 passing at 94.88% coverage
- Zero Spring test annotation overlap enforced (@MockBean, @SpyBean absent from mockito/instructions.md)

## Task Commits

Each task was committed atomically:

1. **Task 1: Write 3 failing mockito integration tests + MOCKITO_CONFIG** - `db01a1d` (test)
2. **Task 2: Author mockito pack files to pass the tests** - `19c72fa` (feat)

## Files Created/Modified
- `argus/packs/mockito/pack.yml` - Pack metadata: category framework, requires java, platforms all
- `argus/packs/mockito/instructions.md` - Mockito 5.x mock-mechanics content with ArgumentCaptor, BDDMockito, Red Flags
- `tests/integration/test_generate.py` - MOCKITO_CONFIG constant + 3 integration tests appended

## Decisions Made
- ArgumentCaptor chosen as key test phrase — unique, stable, lives in Argument Captors section
- MOCKITO_CONFIG isolation constant follows prior pack precedents (TYPE_SAFETY_CONFIG, SPRING_CONFIG, etc.)
- Pack scope strictly mock-mechanics: no @MockBean/@SpyBean (Spring pack), no JUnit lifecycle annotations, no JUnit 4

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Mockito pack auto-discovered, `argus packs list` includes mockito, `argus packs show mockito` renders ArgumentCaptor content
- Ready for Plan 24-03 (CLI improvements)
- Full suite green at 94.88% coverage

---
*Phase: 24-java-framework-packs-cli-improvements*
*Completed: 2026-06-26*
