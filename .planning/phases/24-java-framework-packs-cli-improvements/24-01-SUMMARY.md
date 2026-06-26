---
phase: 24-java-framework-packs-cli-improvements
plan: "01"
subsystem: packs
tags: [spring, spring-boot, jakarta-ee, java, framework-pack, tdd]

# Dependency graph
requires:
  - phase: 22-go-java-kotlin-language-packs
    provides: java language pack (spring pack builds on java pack, requires: [java])
  - phase: 23-fastapi-nextjs-framework-packs
    provides: fastapi/nextjs pack structure and integration test patterns (mirrored for spring)
provides:
  - Spring Boot 4.x framework pack (argus/packs/spring/)
  - IoC/stereotypes, Data JPA (jakarta.persistence), REST API design, and Spring test slice rules
  - 3 integration tests covering packs list, packs show, and generate for spring
affects: [24-02, 24-03, cli-improvements, java-framework-users]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "SPRING_CONFIG isolation constant follows TYPE_SAFETY_CONFIG / FASTAPI_CONFIG precedent"
    - "Spring pack uses requires: [java] to document dependency (loader reads but does not enforce)"
    - "@SpringBootTest chosen as key test phrase — lives in Testing section, stable and unique"

key-files:
  created:
    - argus/packs/spring/pack.yml
    - argus/packs/spring/instructions.md
  modified:
    - tests/integration/test_generate.py

key-decisions:
  - "@SpringBootTest chosen as key test phrase for spring pack — lives in instructions.md Testing section, stable and unique"
  - "SPRING_CONFIG isolation constant follows FASTAPI_CONFIG and prior pack precedents"
  - "Spring pack explicitly excludes: null/Optional discipline, streams, exceptions, record rules (owned by java pack)"
  - "All content targets Spring Boot 4.x / Spring 7 / Jakarta EE 11 — no 2.x/3.x compatibility notes"

patterns-established:
  - "Spring pack: jakarta.* imports only — javax.* is forbidden and flagged in Red Flags section"
  - "Spring pack: constructor injection mandated — @Autowired on fields is a Red Flag"

requirements-completed: [FWRK-03]

# Metrics
duration: 1min
completed: "2026-06-26"
---

# Phase 24 Plan 01: Spring Framework Pack Summary

**Spring Boot 4.x framework pack with Jakarta EE 11 content covering IoC, Data JPA, REST design, and test slices — auto-discovered by existing loader, zero java-pack overlap**

## Performance

- **Duration:** 1 min
- **Started:** 2026-06-26T23:23:33Z
- **Completed:** 2026-06-26T23:24:56Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Authored `argus/packs/spring/pack.yml` with category: framework, requires: [java], platforms: [all]
- Authored `argus/packs/spring/instructions.md` with 5 sections: IoC/stereotypes, Data JPA, REST API design, Testing (Spring test slices), Red Flags
- Added 3 spring integration tests (packs list, packs show @SpringBootTest, generate injects spring.md) — RED then GREEN via TDD cycle
- Full suite: 175 passed, 94.88% coverage; mypy exits 0

## Task Commits

Each task was committed atomically:

1. **Task 1: Write 3 failing spring integration tests + SPRING_CONFIG** - `d26e64f` (test)
2. **Task 2: Author spring pack files to pass the tests** - `a3e2919` (feat)

**Plan metadata:** (docs commit — see below)

_Note: TDD tasks have separate test and feat commits per TDD cycle_

## Files Created/Modified
- `argus/packs/spring/pack.yml` - Spring pack metadata; category: framework, requires: [java]
- `argus/packs/spring/instructions.md` - Spring Boot 4.x rules: IoC, JPA, REST, test slices, Red Flags
- `tests/integration/test_generate.py` - SPRING_CONFIG constant + 3 spring integration tests appended

## Decisions Made
- `@SpringBootTest` chosen as key test phrase — stable, unique to spring pack, lives in Testing section
- `SPRING_CONFIG` isolation constant follows FASTAPI_CONFIG and prior pack precedents
- `requires: [java]` in pack.yml is documentation intent only — loader reads but does not enforce
- All spring content targets Spring Boot 4.x / Spring 7 (Jakarta EE 11, virtual threads baseline); no backward-compat notes
- Zero overlap with java pack enforced: null/Optional discipline, streams, checked/unchecked exceptions, record rules are forbidden in spring/instructions.md

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. The pre-existing coverage threshold (80%) is only satisfied when the full test suite runs together — isolated `-k spring` runs show lower coverage due to subset execution. This is expected behavior, not a new issue (tracked in STATE.md blockers).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Spring pack ships and is auto-discovered by the existing loader — no loader changes needed
- Phase 24 Plan 02 can proceed (next framework or CLI improvement pack)
- FWRK-03 requirement satisfied

---
*Phase: 24-java-framework-packs-cli-improvements*
*Completed: 2026-06-26*
