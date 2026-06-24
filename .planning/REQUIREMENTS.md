# Requirements: Argus — AI Agent Engineering Standards Layer

**Defined:** 2026-06-23
**Milestone:** v1.1
**Core Value:** One command, one config, all AI coding platforms — engineering discipline injected everywhere agents run.

## v1.1 Requirements

### Platform Adapters

- [ ] **PLT-01**: User can generate `GEMINI.md` for Gemini CLI by adding `gemini` to `.argus.yml` platforms

### Process Packs

- [ ] **PACK-01**: User can apply `security` pack to inject OWASP Top 10 and input validation rules into all agent instruction files
- [ ] **PACK-02**: User can apply `type-safety` pack to enforce full type annotation discipline (promoted from `.claude/rules/type-safety.md`)
- [ ] **PACK-03**: User can apply `error-handling` pack to enforce exception hierarchy and catch-only-at-boundaries rules (promoted from `.claude/rules/error-handling.md`)
- [ ] **PACK-04**: User can apply `documentation-standards` pack to enforce docstring and comment discipline (promoted from `.claude/rules/documentation-standards.md`)

### Language Packs

- [ ] **LANG-01**: User can apply `python` pack for PEP 8, type hint, dataclass, and pythonic idiom rules
- [ ] **LANG-02**: User can apply `typescript` pack for strict mode, interface vs type, generics, and no-any rules
- [ ] **LANG-03**: User can apply `go` pack for Go error handling, interface design, goroutine, and package naming conventions
- [ ] **LANG-04**: User can apply `java` pack for Java conventions, OOP patterns, and JVM best practices
- [ ] **LANG-05**: User can apply `kotlin` pack for Kotlin idioms, null safety, coroutines, and extension function patterns

### Framework Packs

- [ ] **FWRK-01**: User can apply `fastapi` pack for dependency injection, async patterns, Pydantic model, and router organization rules
- [ ] **FWRK-02**: User can apply `nextjs` pack for App Router, server components, React hooks discipline, and TypeScript integration rules
- [ ] **FWRK-03**: User can apply `spring` pack for Spring/Spring Boot conventions, IoC container, JPA patterns, and REST API design
- [ ] **FWRK-04**: User can apply `mockito` pack for Java mock discipline, `@Mock` vs `@Spy`, argument captors, and verify patterns

### CLI & Core

- [ ] **CLI-01**: All changed code reaches 80% unit test coverage (project's own stated standard)
- [ ] **CLI-02**: `argus upgrade` command detects out-of-date generated files and offers to regenerate them
- [ ] **CLI-03**: `argus init` detects installed platforms from project files (`.cursor/`, `.github/`, `.windsurf/`, etc.) and pre-selects them

## Future Requirements

### Additional Platforms

- **PLT-02**: Windsurf adapter (`.windsurf/rules/*.md`)
- **PLT-03**: Zed adapter (thin wrapper — Zed reads AGENTS.md natively)
- **PLT-04**: Aider adapter (`.aider.conf.yml` conventions)
- **PLT-05**: JetBrains Junie adapter

### Additional Packs

- **PACK-05**: `refactoring` pack (code smells, safe refactoring steps)
- **PACK-06**: `design-patterns` pack (Strategy, Factory, Observer, Adapter)
- **PACK-07**: `dependency-injection` pack (constructor injection, abstract interfaces)
- **PACK-08**: `testing-strategy` pack (test pyramid, doubles, integration vs unit)
- **LANG-06**: `rust` pack
- **LANG-07**: `csharp` pack
- **FWRK-05**: Django / Flask pack
- **FWRK-06**: Vue.js pack

### Ecosystem

- **ECO-01**: Pack registry / community sharing (GitHub-based, discoverable)
- **ECO-02**: Skills.sh distribution integration
- **ECO-03**: `argus pack new <name>` scaffold command

## Out of Scope

| Feature | Reason |
|---------|--------|
| GUI / web interface | CLI-first; adds complexity without addressing core problem |
| AI-assisted pack generation | Distraction from core delivery for v1.x |
| Pack versioning / pinning | YAGNI until pack content stabilizes |
| Pack authoring wizard | Text editor sufficient |
| Real-time watch mode | `--check` in CI covers the use case |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PLT-01      | TBD   | Pending |
| PACK-01     | TBD   | Pending |
| PACK-02     | TBD   | Pending |
| PACK-03     | TBD   | Pending |
| PACK-04     | TBD   | Pending |
| LANG-01     | TBD   | Pending |
| LANG-02     | TBD   | Pending |
| LANG-03     | TBD   | Pending |
| LANG-04     | TBD   | Pending |
| LANG-05     | TBD   | Pending |
| FWRK-01     | TBD   | Pending |
| FWRK-02     | TBD   | Pending |
| FWRK-03     | TBD   | Pending |
| FWRK-04     | TBD   | Pending |
| CLI-01      | TBD   | Pending |
| CLI-02      | TBD   | Pending |
| CLI-03      | TBD   | Pending |

**Coverage:**
- v1.1 requirements: 17 total
- Mapped to phases: 0 (pending roadmap)
- Unmapped: 17 ⚠️

---
*Requirements defined: 2026-06-23*
*Last updated: 2026-06-23 — initial definition*
