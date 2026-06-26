# Phase 24: Java Framework Packs & CLI Improvements - Context

**Gathered:** 2026-06-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Ship two new built-in framework packs — `spring` and `mockito` — and add three CLI capabilities:
an `argus upgrade` interactive regeneration command, automatic platform detection in `argus init`,
and 80% unit test coverage across all changed modules. Spring and Mockito packs are framework-layer
additions on top of the existing `java` language pack. No changes to existing pack structure or
adapter protocol.

</domain>

<decisions>
## Implementation Decisions

### Spring pack — version target
- Target Spring Boot 4.x / Spring 7 (Jakarta EE 11 era, virtual threads baseline)
- Do NOT include Spring Boot 2.x/3.x compatibility notes — pack is forward-looking

### Spring pack — module scope
- Cover the core trio: Web MVC + Data JPA + REST API design
- Out of scope: Spring Security, Spring Actuator (too deep; own packs if needed later)
- In scope: IoC container guidance, `@Component`/`@Service`/`@Repository` discipline, JPA entity patterns, `@RestController` + `@RequestMapping` REST conventions

### Spring pack — testing coverage
- Spring test slices live in the spring pack: `@SpringBootTest`, `@WebMvcTest`, `@DataJpaTest`
- This keeps the full Spring stack picture (app + test layer) in one place
- Mockito pack covers only mock mechanics — no Spring-specific test annotations

### Spring pack — overlap boundary with java language pack
- Forbidden in spring pack: null discipline, streams/optionals, checked vs unchecked exceptions
  (those live in the `java` language pack from Phase 22)
- Spring pack adds framework-layer rules that assume java pack is already active

### Spring pack — test assertion key phrase
- `@SpringBootTest` — unique annotation, stable location in instructions.md testing section
- Isolation constant: `SPRING_CONFIG` — follows `PYTHON_CONFIG`, `GO_CONFIG`, `FASTAPI_CONFIG` precedent

### Mockito pack — test runner assumption
- Target JUnit 5 and JUnit 6 (modern entry points only; JUnit 4 is end-of-life)
- `@ExtendWith(MockitoExtension.class)` is the canonical setup pattern to document

### Mockito pack — style coverage
- Include BDDMockito alongside classic style: `BDDMockito.given()` / `then()` shown as alternative
- Cover all three core mechanics: `@Mock` vs `@Spy`, argument captors, `verify()` patterns
- NOT a Spring testing pack — no `@MockBean`, `@SpyBean` (those are spring pack territory)

### Mockito pack — overlap boundary with java language pack
- Forbidden in mockito pack: language-level assertions, JUnit lifecycle annotations unrelated to mocking
- Mockito pack is test-runner framework content only

### Mockito pack — test assertion key phrase
- `ArgumentCaptor` — stable class name, unique to Mockito, lives in the argument captor section
- Isolation constant: `MOCKITO_CONFIG` — follows prior precedents

### argus upgrade — purpose and UX
- `upgrade` is the interactive developer flow: detect drift → list out-of-date files → prompt "Regenerate now? [y/N]"
- Distinct from `generate --check` (silent CI exit gate): upgrade is human-facing, check is machine-facing
- When no files are out of date: print "✓ All generated files are up to date." and exit 0
- When files differ: list file names (not inline diff), then prompt

### argus upgrade — CI mode
- Detected via `CI` environment variable (`os.environ.get("CI")`)
- In CI mode: exit non-zero if any files differ, no prompt, no interactive output
- No `--ci` flag needed — standard CI env var is sufficient and auto-applied by all major CI platforms

### argus upgrade — diff presentation
- List changed file names only (e.g., `  • CLAUDE.md`, `  • .cursor/rules/argus.md`)
- No inline diff output — generated files can be large; git diff is available if user wants details

### argus init — platform detection markers
Strict filesystem markers (only detect if the platform's actual config artifact exists):
- `.cursor/` directory → `cursor`
- `.github/copilot-instructions.md` file → `copilot`
- `GEMINI.md` file → `gemini`
- `.claude/` directory → `claude`
- `.opencode/` directory → `opencode`

### argus init — YAML output when platforms detected
- Detected platforms listed first (active, uncommented)
- Undetected platforms listed below, commented out with `# ` prefix
- User can uncomment to activate additional platforms — no information lost

### argus init — fallback when nothing detected
- Fall back to current behavior: all platforms listed uncommented, no detection output message
- Silent fallback — consistent with current `argus init` experience

### Claude's Discretion
- Exact wording of `argus upgrade` prompt text and output formatting
- Spring pack IoC container section structure and ordering
- Mockito pack BDDMockito example code style
- Whether `pack.yml` for spring and mockito includes a `requires:` field pointing to the java pack

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` §Framework Packs — FWRK-03 (spring pack), FWRK-04 (mockito pack)
- `.planning/REQUIREMENTS.md` §CLI & Core — CLI-01 (80% coverage), CLI-02 (upgrade command), CLI-03 (init detection)
- `.planning/ROADMAP.md` — Phase 24 success criteria (5 criteria)

### Pack format reference
- `argus/packs/fastapi/pack.yml` — framework pack metadata template (category: framework)
- `argus/packs/fastapi/instructions.md` — framework pack instructions template
- `argus/packs/java/instructions.md` — java language pack (defines what spring/mockito must NOT duplicate)

### Test pattern
- `tests/integration/test_generate.py` — isolation config constant pattern (`SPRING_CONFIG`,
  `MOCKITO_CONFIG`) + 3-assertion test (packs list / packs show / generate injects key phrase);
  must follow the same pattern as `PYTHON_CONFIG`, `GO_CONFIG`, `FASTAPI_CONFIG` etc.

### CLI reference
- `argus/cli.py` — existing `init` command (lines ~77-86), `generate --check` flag — upgrade must
  be a new `@main.command()` alongside generate/init; init detection modifies the `init` command body

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `argus/packs/fastapi/` — complete working framework pack to copy and adapt for spring and mockito
- `argus/packs/java/` — existing java language pack; read to enforce overlap boundary (no duplication)
- `argus/loader.py` — auto-discovers packs from `argus/packs/`; no changes needed for new packs
- `tests/integration/test_generate.py` — extend with `SPRING_CONFIG` and `MOCKITO_CONFIG` isolation
  constants following prior precedents
- `argus/cli.py:68` — `DEFAULT_PLATFORMS` list; init currently writes all platforms unconditionally

### Established Patterns
- `generate --check` flag (cli.py ~line 20): CI gate pattern — upgrade is the interactive counterpart
- Isolation config constants: `{"packs": ["X"], "platforms": ["claude"]}` — use `SPRING_CONFIG` / `MOCKITO_CONFIG`
- Pack discovery is automatic — adding `argus/packs/spring/` and `argus/packs/mockito/` is sufficient

### Integration Points
- `argus init` writes `.argus.yml` via `yaml.dump()` — detection logic precedes the dump call
- New `argus upgrade` is a new `@main.command()` that calls the generator internally, compares output,
  checks `os.environ.get("CI")`, and conditionally prompts

</code_context>

<specifics>
## Specific Ideas

- Spring Boot 4.x target is intentional and forward-looking — do not add "also works with Boot 3.x" hedging
- JUnit 5 + JUnit 6 both mentioned in Mockito pack (not just JUnit 5)
- `argus upgrade` should feel like a polished developer tool: clear "N files out of date" → list → prompt flow
- Detected platforms appearing first in `.argus.yml` with undetected ones commented — gives the user
  a clear signal of what was auto-selected vs what they might want to add

</specifics>

<deferred>
## Deferred Ideas

- Spring Security pack — deep domain, could be its own phase if demand emerges
- Spring Actuator coverage — deferred; production observability pack could follow
- `argus init` interactive wizard (interactive platform selection prompt) — scope creep for this phase
- `--ci` flag for `argus upgrade` — env var alone is sufficient; revisit only if users request it

</deferred>

---

*Phase: 24-java-framework-packs-cli-improvements*
*Context gathered: 2026-06-26*
