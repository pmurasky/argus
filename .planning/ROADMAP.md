# Roadmap: Argus — AI Agent Engineering Standards Layer

## Milestones

- ✅ **v1.0 Foundation** - Phases 1–17 (shipped 2026-06-15)
- 🚧 **v1.1 Pack Expansion** - Phases 18–24 (in progress)

## Phases

<details>
<summary>✅ v1.0 Foundation (Phases 1–17) - SHIPPED 2026-06-15</summary>

Shipped CLI (`init`, `generate`, `packs list/show`, `platforms list`, `validate`), 5 built-in
process packs, 4 platform adapters (claude, opencode, copilot, cursor), custom pack loading,
AGENTS.md generation, and PyPI publish CI workflow. Published as `argus-standards` v0.1.1.

</details>

---

### 🚧 v1.1 Pack Expansion (In Progress)

**Milestone Goal:** Expand Argus from 5 process packs and 4 platforms to 13 packs, 5 platforms,
and a smarter CLI — making Argus useful for any language or framework team.

#### Phase 18: Gemini CLI Adapter

- [x] **Phase 18: Gemini CLI Adapter** - Add `gemini` as a fifth supported platform (completed 2026-06-24)

#### Phase 19: Promoted Process Packs

- [x] **Phase 19: Promoted Process Packs** - Promote type-safety, error-handling, and documentation-standards from `.claude/rules/` to built-in packs (completed 2026-06-24)

#### Phase 20: Security Pack

- [x] **Phase 20: Security Pack** - Author new OWASP-aligned security pack (completed 2026-06-25)

#### Phase 21: Python & TypeScript Language Packs

- [x] **Phase 21: Python & TypeScript Language Packs** - Ship `python` and `typescript` language packs (completed 2026-06-25)

#### Phase 22: Go, Java & Kotlin Language Packs

- [x] **Phase 22: Go, Java & Kotlin Language Packs** - Ship `go`, `java`, and `kotlin` language packs (completed 2026-06-25)

#### Phase 23: Python & JavaScript Framework Packs

- [x] **Phase 23: Python & JavaScript Framework Packs** - Ship `fastapi` and `nextjs` framework packs (completed 2026-06-26)

#### Phase 24: Java Framework Packs & CLI Improvements

- [x] **Phase 24: Java Framework Packs & CLI Improvements** - Ship `spring` and `mockito` packs; add coverage gate, upgrade command, and platform auto-detection (completed 2026-06-26)

---

## Phase Details

### Phase 18: Gemini CLI Adapter
**Goal**: Users can target Gemini CLI as a platform, generating `GEMINI.md` alongside all other platform files in one `argus generate` run.
**Depends on**: Phase 17 (v1.0 complete)
**Requirements**: PLT-01
**Success Criteria** (what must be TRUE):
  1. User adds `gemini` to platforms in `.argus.yml` and `argus generate` writes `GEMINI.md` to the project root.
  2. `argus platforms list` includes `gemini` in its output.
  3. `GEMINI.md` content matches the pack rules configured — identical in substance to the claude adapter output for the same pack set.
  4. No existing adapter or test is modified to add this platform (adapter is a single new file).
**Plans**: 2 plans
Plans:
- [ ] 18-01-PLAN.md — TDD GeminiAdapter: failing tests then implement argus/adapters/gemini.py (AGENTS.md + GEMINI.md)
- [ ] 18-02-PLAN.md — Register entry point in pyproject.toml, add gemini to DEFAULT_PLATFORMS, reinstall, integration test

### Phase 19: Promoted Process Packs
**Goal**: The `type-safety`, `error-handling`, and `documentation-standards` packs are available as built-in Argus packs, promoting content already proven in `.claude/rules/`.
**Depends on**: Phase 18
**Requirements**: PACK-02, PACK-03, PACK-04
**Success Criteria** (what must be TRUE):
  1. User can add `type-safety` to `.argus.yml` packs and `argus generate` injects full type annotation rules into all platform files.
  2. User can add `error-handling` to `.argus.yml` packs and generated files contain exception hierarchy and catch-only-at-boundaries rules.
  3. User can add `documentation-standards` to `.argus.yml` packs and generated files contain docstring and comment discipline rules.
  4. `argus packs list` shows all three new packs.
  5. `argus packs show type-safety` (and the other two) displays the pack content.
**Plans**: 3 plans
Plans:
- [ ] 19-01-PLAN.md — type-safety: 3 integration tests + replace `mypy argus/` with `mypy .`
- [ ] 19-02-PLAN.md — error-handling: 3 integration tests + generalize Argus class names
- [ ] 19-03-PLAN.md — documentation-standards: 3 integration tests + generalize PackLoader/available_packs

### Phase 20: Security Pack
**Goal**: Users can apply an OWASP-aligned `security` pack that injects input validation and Top 10 defensive rules into every agent instruction file.
**Depends on**: Phase 19
**Requirements**: PACK-01
**Success Criteria** (what must be TRUE):
  1. User adds `security` to `.argus.yml` packs and generated files contain OWASP Top 10 guidance and input validation rules.
  2. `argus packs show security` displays the full security pack content.
  3. Security rules are specific enough to guide an AI agent (not generic platitudes — concrete rule per OWASP category).
**Plans**: 1 plan
Plans:
- [ ] 20-01-PLAN.md — TDD security pack: 3 failing integration tests, then author OWASP pack files (pack.yml, instructions.md, checklist.md, examples.md)

### Phase 21: Python & TypeScript Language Packs
**Goal**: Users working in Python or TypeScript can apply language-specific packs that inject idiomatic style, type discipline, and ecosystem conventions into agent instruction files.
**Depends on**: Phase 20
**Requirements**: LANG-01, LANG-02
**Success Criteria** (what must be TRUE):
  1. User adds `python` pack and generated files contain PEP 8 style, type hint requirements, dataclass guidance, and pythonic idiom rules.
  2. User adds `typescript` pack and generated files contain strict mode mandate, interface vs type guidance, generics usage, and no-any rules.
  3. Both packs appear in `argus packs list` under a recognizable language category.
  4. `argus packs show python` and `argus packs show typescript` each display their full content.
**Plans**: 2 plans
Plans:
- [ ] 21-01-PLAN.md — TDD python pack: 3 failing integration tests, then author pack files (PEP 8, naming, idioms, dataclasses; zero type-safety overlap)
- [ ] 21-02-PLAN.md — TDD typescript pack: 3 failing integration tests, then author pack files (strict mode, interface vs type, generics, no-any; framework-agnostic)

### Phase 22: Go, Java & Kotlin Language Packs
**Goal**: Users working in Go, Java, or Kotlin can apply language-specific packs that codify the idioms and conventions most important for AI agents to follow in each ecosystem.
**Depends on**: Phase 21
**Requirements**: LANG-03, LANG-04, LANG-05
**Success Criteria** (what must be TRUE):
  1. User adds `go` pack and generated files contain Go error handling conventions, interface design, goroutine guidance, and package naming rules.
  2. User adds `java` pack and generated files contain Java OOP conventions, common patterns, and JVM best practices.
  3. User adds `kotlin` pack and generated files contain null safety idioms, coroutine patterns, and extension function guidance.
  4. All three packs appear in `argus packs list` and respond to `argus packs show <name>`.
**Plans**: 3 plans
Plans:
- [ ] 22-01-PLAN.md — TDD go pack: 3 failing integration tests, then author pack files (error handling, interfaces/composition, goroutines, package naming; framework-agnostic)
- [ ] 22-02-PLAN.md — TDD java pack: 3 failing integration tests, then author pack files (modern Java 17+ types, null discipline, OOP, exception handling; framework-agnostic)
- [ ] 22-03-PLAN.md — TDD kotlin pack: 3 failing integration tests, then author pack files (null safety, idiomatic Kotlin, coroutines, Kotlin-over-Java idioms; framework-agnostic)

### Phase 23: Python & JavaScript Framework Packs
**Goal**: Users building FastAPI APIs or Next.js applications can apply framework packs that give AI agents precise, actionable rules for those ecosystems.
**Depends on**: Phase 22
**Requirements**: FWRK-01, FWRK-02
**Success Criteria** (what must be TRUE):
  1. User adds `fastapi` pack and generated files contain dependency injection patterns, async/await discipline, Pydantic model guidance, and router organization rules.
  2. User adds `nextjs` pack and generated files contain App Router conventions, server component vs client component guidance, React hooks discipline, and TypeScript integration rules.
  3. Both packs appear in `argus packs list` and respond to `argus packs show <name>`.
**Plans**: 2 plans
Plans:
- [ ] 23-01-PLAN.md — TDD fastapi pack: 3 failing integration tests, then author pack files (async patterns, Pydantic v2 models, dependency injection, APIRouter organization; additive to python pack)
- [ ] 23-02-PLAN.md — TDD nextjs pack: 3 failing integration tests, then author pack files (App Router conventions, server vs client components, hooks discipline, TS integration; additive to typescript pack)

### Phase 24: Java Framework Packs & CLI Improvements
**Goal**: Users on Java/Spring stacks can apply Spring and Mockito packs; the CLI gains a coverage gate, an upgrade command, and automatic platform detection during `argus init`.
**Depends on**: Phase 23
**Requirements**: FWRK-03, FWRK-04, CLI-01, CLI-02, CLI-03
**Success Criteria** (what must be TRUE):
  1. User adds `spring` pack and generated files contain Spring Boot conventions, IoC container guidance, JPA patterns, and REST API design rules.
  2. User adds `mockito` pack and generated files contain mock discipline rules: `@Mock` vs `@Spy`, argument captors, and verify patterns.
  3. Running the test suite after all v1.1 changes achieves 80% unit test coverage on all changed modules (project's stated standard).
  4. `argus upgrade` detects when generated files are out of date and offers to regenerate them; exits non-zero in CI mode when files differ.
  5. `argus init` on a project with `.cursor/` or `.github/copilot-instructions.md` present automatically pre-selects those platforms in the scaffolded `.argus.yml`.
**Plans**: 3 plans
Plans:
- [ ] 24-01-PLAN.md — TDD spring pack: 3 failing integration tests, then author pack files (IoC/stereotypes, Data JPA, REST design, Spring test slices; Spring Boot 4.x/jakarta, additive to java pack)
- [ ] 24-02-PLAN.md — TDD mockito pack: 3 failing integration tests, then author pack files (@Mock vs @Spy, ArgumentCaptor, verify patterns, BDDMockito; JUnit 5/6, mock-mechanics only)
- [ ] 24-03-PLAN.md — TDD CLI improvements: argus upgrade command (CLI-02) + init platform detection (CLI-03) + 80% coverage gate (CLI-01)

---

## Progress

**Execution Order:**
Phases execute in numeric order: 18 → 19 → 20 → 21 → 22 → 23 → 24

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1–17. Foundation | v1.0 | — | Complete | 2026-06-15 |
| 18. Gemini CLI Adapter | 2/2 | Complete    | 2026-06-24 | - |
| 19. Promoted Process Packs | 3/3 | Complete    | 2026-06-24 | - |
| 20. Security Pack | 1/1 | Complete    | 2026-06-25 | - |
| 21. Python & TypeScript Language Packs | 2/2 | Complete    | 2026-06-25 | - |
| 22. Go, Java & Kotlin Language Packs | 3/3 | Complete    | 2026-06-25 | - |
| 23. Python & JavaScript Framework Packs | 2/2 | Complete    | 2026-06-26 | - |
| 24. Java Framework Packs & CLI Improvements | 3/3 | Complete    | 2026-06-26 | - |
