---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Pack Expansion
status: unknown
stopped_at: Completed 24-02-PLAN.md
last_updated: "2026-06-26T23:28:54.029Z"
progress:
  total_phases: 7
  completed_phases: 6
  total_plans: 16
  completed_plans: 15
---

# Project State

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-06-23)

**Core value:** One command, one config, all AI coding platforms — engineering discipline injected everywhere agents run.
**Current focus:** Phase 24 — java-framework-packs-cli-improvements

## Current Position

Phase: 24 (java-framework-packs-cli-improvements) — EXECUTING
Plan: 1 of 3

## Performance Metrics

**Velocity:**

- Total plans completed: 1 (v1.1)
- Average duration: 2 min
- Total execution time: 2 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 18 (Gemini CLI Adapter) | 1/2 | 2 min | 2 min |

**Recent Trend:** 2 min/plan

*Updated after each plan completion*
| Phase 18-gemini-cli-adapter P02 | 2 | 2 tasks | 3 files |
| Phase 19 P02 | 1 min | 2 tasks | 4 files |
| Phase 19 P03 | 5 | 2 tasks | 2 files |
| Phase 20-security-pack P01 | 5 | 2 tasks | 5 files |
| Phase 21-python-typescript-language-packs P01 | 5 min | 2 tasks | 5 files |
| Phase 21-python-typescript-language-packs P02 | 5 | 2 tasks | 5 files |
| Phase 22-go-java-kotlin-language-packs P01 | 2 | 2 tasks | 5 files |
| Phase 22 P02 | 2 min | 2 tasks | 5 files |
| Phase 22-go-java-kotlin-language-packs P03 | 2 | 2 tasks | 5 files |
| Phase 23 P01 | 5 | 2 tasks | 5 files |
| Phase 23 P02 | 3 | 2 tasks | 5 files |
| Phase 24-java-framework-packs-cli-improvements P01 | 1 | 2 tasks | 3 files |
| Phase 24 P02 | 4 | 2 tasks | 3 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Roadmap: PACK-02/03/04 grouped as one phase (content from existing `.claude/rules/` — promotion, not net-new authoring)
- Roadmap: CLI-01 (coverage gate) placed last (Phase 24) so coverage is measured after all pack/adapter work lands
- Roadmap: Security pack (PACK-01) gets its own phase — new content requiring research; higher risk than promotions
- 18-01: GeminiAdapter._gemini_md mirrors CopilotAdapter._copilot_instructions — same H2 pattern, GEMINI.md output path
- 18-01: No existing file modified — GeminiAdapter is a single new file per phase hard constraint
- [Phase 18-gemini-cli-adapter]: 18-02: GEMINI_CONFIG local constant used in test to isolate from FULL_CONFIG shared by other integration tests
- [Phase 18-gemini-cli-adapter]: 18-02: uv pip install -e . used for reinstall (project uses uv toolchain, pip not present in .venv)
- [Phase 19-promoted-process-packs]: 19-01: TYPE_SAFETY_CONFIG constant used as isolated config (not added to FULL_CONFIG) — mirrors GEMINI_CONFIG precedent
- [Phase 19-promoted-process-packs]: 19-01: mypy . chosen as generic replacement for mypy argus/ in type-safety pack content
- [Phase 19]: 19-02: ERROR_HANDLING_CONFIG constant follows TYPE_SAFETY_CONFIG isolation pattern
- [Phase 19]: 19-02: 'system boundaries' chosen as key phrase for tests (survives generalization)
- [Phase 19]: 'imperative mood' chosen as key phrase for documentation-standards tests — lives in instructions.md, not examples.md, so survives Task 2 edit
- [Phase 19]: DOCUMENTATION_STANDARDS_CONFIG follows isolation pattern from Plans 01 and 02
- [Phase 20-security-pack]: parameterized chosen as key test phrase for security pack — lives in instructions.md (A03 Injection), survives future content edits
- [Phase 20-security-pack]: SECURITY_CONFIG isolation constant follows TYPE_SAFETY_CONFIG and prior pack precedents
- [Phase 21-python-typescript-language-packs]: pathlib chosen as key test phrase for python pack — lives in instructions.md (Idiomatic Python section), stable and unique
- [Phase 21-python-typescript-language-packs]: PYTHON_CONFIG isolation constant follows TYPE_SAFETY_CONFIG and prior pack precedents
- [Phase 21-python-typescript-language-packs]: Zero overlap with type-safety pack enforced — FORBIDDEN in python pack: mypy, Optional, type annotations
- [Phase 21-python-typescript-language-packs]: noImplicitAny chosen as key test phrase for typescript pack — lives in instructions.md Strict Mode section, stable and unique
- [Phase 21-python-typescript-language-packs]: TYPESCRIPT_CONFIG isolation constant follows TYPE_SAFETY_CONFIG and prior pack precedents
- [Phase 21-python-typescript-language-packs]: TypeScript pack is framework-agnostic — FORBIDDEN: React, JSX, Next.js, Vue (belong in Phase 23)
- [Phase 22-go-java-kotlin-language-packs]: errors.Is chosen as key test phrase for go pack — lives in instructions.md Error Handling section, stable and unique
- [Phase 22-go-java-kotlin-language-packs]: GO_CONFIG isolation constant follows TYPE_SAFETY_CONFIG and prior pack precedents
- [Phase 22-go-java-kotlin-language-packs]: Go pack is framework-agnostic — FORBIDDEN: gin, echo, fiber (belong in Phase 23 framework packs)
- [Phase 22]: Optional.orElseThrow chosen as key test phrase for java pack — lives in instructions.md Null Discipline section, stable and unique
- [Phase 22]: JAVA_CONFIG isolation constant follows GO_CONFIG and prior pack precedents
- [Phase 22]: Java pack is framework-agnostic — FORBIDDEN: Spring, Jakarta EE, Quarkus, Hibernate
- [Phase 22]: requireNotNull chosen as key test phrase for kotlin pack — lives in instructions.md Null Safety section, stable and unique
- [Phase 22]: KOTLIN_CONFIG isolation constant follows GO_CONFIG and JAVA_CONFIG precedent from Plans 22-01 and 22-02
- [Phase 22]: Kotlin pack is framework-agnostic — FORBIDDEN: Ktor, Android, Compose, Jetpack (belong in Phase 23 framework packs)
- [Phase 23]: APIRouter chosen as key test phrase for fastapi pack — lives in instructions.md Router Organization section, stable and unique
- [Phase 23]: FASTAPI_CONFIG isolation constant follows KOTLIN_CONFIG and prior pack precedents
- [Phase 23]: use client chosen as key test phrase for nextjs pack — lives in instructions.md, stable and unique
- [Phase 23]: NEXTJS_CONFIG isolation constant follows FASTAPI_CONFIG and prior pack precedents
- [Phase 24-java-framework-packs-cli-improvements]: @SpringBootTest chosen as key test phrase for spring pack — lives in instructions.md Testing section, stable and unique
- [Phase 24-java-framework-packs-cli-improvements]: SPRING_CONFIG isolation constant follows FASTAPI_CONFIG and prior pack precedents
- [Phase 24-java-framework-packs-cli-improvements]: Spring pack: All content targets Spring Boot 4.x / Spring 7 (Jakarta EE 11) — no 2.x/3.x compatibility notes, zero java-pack overlap
- [Phase 24]: ArgumentCaptor chosen as key test phrase for mockito pack — lives in instructions.md Argument Captors section, stable and unique
- [Phase 24]: MOCKITO_CONFIG isolation constant follows SPRING_CONFIG and prior pack precedents
- [Phase 24]: Mockito pack: mock-mechanics only — FORBIDDEN: @MockBean, @SpyBean (Spring), @RunWith (JUnit 4)

### Pending Todos

None yet.

### Blockers/Concerns

- Test coverage at 46% entering v1.1 — CLI-01 (Phase 24) must reach 80% on all changed code, but the gap is large; watch for scope creep if backfilling old code
- `.venv/bin/pytest` is the correct test runner (not bare `pytest`)

## Session Continuity

Last session: 2026-06-26T23:28:54.027Z
Stopped at: Completed 24-02-PLAN.md
Resume file: None
