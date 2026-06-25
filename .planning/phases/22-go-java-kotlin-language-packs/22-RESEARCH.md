# Phase 22: Go, Java & Kotlin Language Packs - Research

**Researched:** 2026-06-24
**Domain:** Language pack authoring — Go 1.21+, Java 17+, Kotlin 2.0+
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Version targets:**
- Go pack targets Go 1.21+ — covers `slices`/`maps` stdlib packages, `slog`, type inference improvements
- Java pack targets Java 17+ — full 17→25 arc: records (16+), sealed classes/switch expressions (17+), pattern matching (21+), virtual threads (21+), unnamed patterns (22+); rules note minimum Java version where a feature requires ≥17 vs ≥21
- Kotlin pack targets Kotlin 2.0+ — K2 compiler era; smart casts more reliable, value classes stable

**Content sections per pack (4 sections each):**

Go:
1. Error handling — errors-as-values, `fmt.Errorf` with `%w`, `errors.Is`/`errors.As`, no panic for recoverable conditions
2. Interfaces and composition — implicit satisfaction, small interfaces (1–2 methods), prefer embedding, no interfaces-before-need
3. Goroutines and concurrency — goroutine leak prevention, always propagate `context.Context`, channels for ownership transfer, `sync.Mutex` for shared state, avoid `time.Sleep` as sync
4. Package and naming — lowercase package names, CamelCase exported, unexported lowercase, no `utils`/`helpers`, use `slices` and `maps` packages

Java 17+:
1. Modern Java types — records, sealed classes + switch expressions, `var`, text blocks, unnamed patterns (22+)
2. Null discipline — `Optional<T>` as return type, never return null from public APIs, `Optional.orElseThrow()` over `.get()`, never Optional as field/parameter type
3. OOP discipline — composition over inheritance, classes final by default, narrow interfaces (ISP), avoid god classes (>300 lines), `record` not mutable class for data-only objects
4. Exception handling — unchecked for unrecoverable, checked for caller-recoverable, never catch `Exception` broadly, no exceptions for control flow, specific types

Kotlin 2.0+:
1. Null safety — `?` nullable types, `?.` safe calls, `?.let` for null-conditional blocks, `!!` only when provably non-null with comment, `requireNotNull`/`checkNotNull` at entry points, guard Java interop boundaries
2. Idiomatic Kotlin — `data class` for DTOs, `when` expressions over if/else chains, destructuring where it aids clarity, extension functions, `object` for singletons
3. Coroutines — `suspend` for async functions, `Flow` for streams, always structured scope (never GlobalScope), `withContext(Dispatchers.IO)` for blocking I/O, cancel scopes
4. Kotlin-over-Java idioms — prefer Kotlin collection API over Java Streams, string templates over concatenation, scope functions (`apply`/`let`/`run`/`also`) with consistent mental model

**Java/Kotlin relationship:** Fully independent packs — no cross-references, teams enable both if desired, no "prefer Kotlin over Java" guidance.

**Framework-agnostic rule:** No gin/echo/fiber (Go), no Spring/Jakarta EE/Quarkus (Java), no Ktor/Android/Compose (Kotlin).

**Pack metadata:** `category: language`, `requires: []`, `platforms: [all]` for all three packs.

### Claude's Discretion
- Exact selection of which 15–20 rules to include per pack within each section
- Specific example code in `examples.md` for each language
- Wording of Red Flags table entries
- Whether `checklist.md` mirrors `instructions.md` sections exactly or consolidates

### Deferred Ideas (OUT OF SCOPE)
- JVM interop pack (`jvm-interop`) covering Java↔Kotlin co-existence rules — future phase
- Framework packs for Spring (Java), Ktor/Android (Kotlin), gin/echo (Go) — Phase 23/24 scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| LANG-03 | User can apply `go` pack for Go error handling, interface design, goroutine, and package naming conventions | Pack structure established by python/typescript precedent; content sections locked in CONTEXT.md |
| LANG-04 | User can apply `java` pack for Java conventions, OOP patterns, and JVM best practices | Java 17+ target confirmed; four content sections locked in CONTEXT.md |
| LANG-05 | User can apply `kotlin` pack for Kotlin idioms, null safety, coroutines, and extension function patterns | Kotlin 2.0+ target confirmed; four content sections locked in CONTEXT.md |
</phase_requirements>

---

## Summary

Phase 22 is a pure content-authoring phase — no production code changes are needed. The pack infrastructure (loader, CLI commands, generator) is already complete and auto-discovers new packs from `argus/packs/`. The only deliverables are three new directories under `argus/packs/`: `go/`, `java/`, and `kotlin/`, each containing `pack.yml`, `instructions.md`, `checklist.md`, and `examples.md`. The test extension follows the established isolation constant pattern (`GO_CONFIG`, `JAVA_CONFIG`, `KOTLIN_CONFIG`) in `tests/integration/test_generate.py`.

The content of all four sections per pack is locked by CONTEXT.md decisions — what remains to Claude's discretion is the specific rule wording, the exact 15–20 rules per section, and example code. The Python and TypeScript packs from Phase 21 are the direct structural templates: density, formatting, and file layout must match exactly. No new infrastructure, no new CLI commands, no loader changes.

**Primary recommendation:** Copy `argus/packs/python/` as scaffold for each new pack, replace all content, keep file names and YAML structure identical. Extend the integration test file with three isolation constant blocks following PYTHON_CONFIG/TYPESCRIPT_CONFIG precedents.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pytest | ≥8.x (already installed) | Integration test runner | Established project test framework |
| pyyaml | ≥6.0 (already installed) | `pack.yml` parsing | Already used by PackLoader |
| click | ≥8.1 (already installed) | CLI integration | Established project CLI framework |

No new dependencies are required. All pack content is plain Markdown and YAML.

**Test runner:** `.venv/bin/pytest` (not bare `pytest` — project convention from STATE.md)

---

## Architecture Patterns

### Pack Directory Structure (established, do not deviate)

```
argus/packs/
├── go/
│   ├── pack.yml
│   ├── instructions.md
│   ├── checklist.md
│   └── examples.md
├── java/
│   ├── pack.yml
│   ├── instructions.md
│   ├── checklist.md
│   └── examples.md
└── kotlin/
    ├── pack.yml
    ├── instructions.md
    ├── checklist.md
    └── examples.md
```

### Pattern 1: pack.yml (copy verbatim, change name/description)

```yaml
name: go
description: Go error handling, interface design, goroutine discipline, and package naming
category: language
requires: []
platforms: [all]
```

```yaml
name: java
description: Modern Java types, null discipline, OOP patterns, and exception handling
category: language
requires: []
platforms: [all]
```

```yaml
name: kotlin
description: Null safety, idiomatic Kotlin, coroutines, and Kotlin-over-Java idioms
category: language
requires: []
platforms: [all]
```

### Pattern 2: instructions.md format (Python pack as canonical template)

- H1 heading = language name (e.g., `# Go`)
- H2 headings = section names (e.g., `## Error Handling`)
- Bullet rules under each H2
- Final H2 `## Red Flags — Stop and Correct` — either bullet list (Python style) or table (TypeScript style)

**Python pack uses bullet Red Flags; TypeScript uses a table.** Either is acceptable for these packs. Use whichever is clearer per language.

### Pattern 3: checklist.md format

- H2 heading = `## [Language] Checklist`
- Checkbox bullets: `- [ ] rule`
- 8–12 items covering the most actionable rules from instructions.md
- Does not need to mirror every rule — consolidate where natural

### Pattern 4: examples.md format

- H2 heading = `## [Language] Examples`
- H3 per example = topic name
- **Avoid** block (labeled `**Avoid**`) with fenced code
- **Prefer** block (labeled `**Prefer**`) with fenced code
- 4–6 examples per pack covering the highest-value contrasts

### Pattern 5: Integration test isolation constant

```python
GO_CONFIG = """\
packs:
  - go
platforms:
  - claude
"""

def test_go_pack_appears_in_packs_list():
    """Given packs list is invoked, go appears in the output."""
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "go" in result.output

def test_go_pack_show_renders_content():
    """Given packs show go is invoked, errors.Is appears in the output."""
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "show", "go"])
    assert result.exit_code == 0
    assert "errors.Is" in result.output

def test_go_pack_generate_injects_content(tmp_path):
    """Given a go+claude config, generate writes content to .claude/rules/go.md."""
    (tmp_path / ".argus.yml").write_text(GO_CONFIG)
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "errors.Is" in (tmp_path / ".claude/rules/go.md").read_text()
```

Repeat the same three-test block for JAVA_CONFIG (key phrase: `Optional.orElseThrow`) and KOTLIN_CONFIG (key phrase: `requireNotNull`).

### Anti-Patterns to Avoid

- **Cross-referencing packs:** Each pack must be self-contained — no "see also Java pack" in Kotlin or vice versa
- **Framework content:** No gin, Spring, Ktor, Android, Compose mentions anywhere
- **Overlap with type-safety pack:** Do not include Java/Kotlin generic type annotation rules that duplicate what type-safety covers (type-safety is Python-oriented but the principle holds)
- **Version gate ambiguity for Java:** Rules using pattern matching, virtual threads (21+), or unnamed patterns (22+) MUST include a note like `(Java 21+)` or `(Java 22+)` inline

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Pack auto-discovery | Custom registry or manifest | Drop directory into `argus/packs/` | `PackLoader.available_packs()` already iterates subdirectories |
| CLI commands for new packs | New click commands | Existing `packs list`, `packs show`, `generate` | These work with any pack automatically |
| Test helpers for pack tests | Custom fixtures | Copy isolation constant + three-test block | Established pattern; no shared fixtures needed |

**Key insight:** This phase requires zero production Python code changes. All work is content authoring (Markdown + YAML) plus extending one test file.

---

## Common Pitfalls

### Pitfall 1: Key phrase not in instructions.md

**What goes wrong:** Test asserts `"errors.Is" in output` but the phrase only appears in `examples.md`, not `instructions.md`.
**Why it happens:** The `packs show` command renders the full pack content (instructions + checklist + examples), but the generate command writes only `instructions.md` to the rules file. If the key phrase is only in `examples.md`, the generate test will fail.
**How to avoid:** Ensure the test key phrase (`errors.Is`, `Optional.orElseThrow`, `requireNotNull`) appears verbatim in `instructions.md`, not only in `examples.md`.
**Warning signs:** `test_go_pack_show_renders_content` passes but `test_go_pack_generate_injects_content` fails.

### Pitfall 2: Pack directory name mismatch

**What goes wrong:** Directory named `golang/` instead of `go/` — `argus packs list` shows it but config `packs: [go]` fails to load it.
**Why it happens:** PackLoader uses the directory name as the pack name. The pack name in `pack.yml` and the directory name must both match the name used in `.argus.yml`.
**How to avoid:** Directory name = pack name in `pack.yml` = name in `packs:` list in config.

### Pitfall 3: Java version gating not annotated

**What goes wrong:** Rules for pattern matching or virtual threads written without version annotation — users on Java 17 follow rules that require Java 21.
**Why it happens:** The Java 17+ baseline covers features from 17 through 25; not all features are available at 17.
**How to avoid:** Annotate inline: `use pattern matching for switch (Java 21+)`, `use virtual threads (Java 21+)`, `use unnamed variables with `_` (Java 22+)`.

### Pitfall 4: Test file import missing

**What goes wrong:** Adding test functions to `test_generate.py` but forgetting that `CliRunner` and `main` are already imported at top of file.
**Why it happens:** The file already has all imports needed — no new imports required for the three new test blocks.
**How to avoid:** Only add isolation constants and test functions; the imports are already there.

### Pitfall 5: checklist.md or examples.md missing

**What goes wrong:** Pack loads but `packs show` output is incomplete; no checklist or examples rendered.
**Why it happens:** `_read_optional` in PackLoader silently returns None for missing files — no error raised.
**How to avoid:** All four files must exist for each pack. Verify all four files are present before running tests.

---

## Code Examples

### PackLoader path (confirmed from loader.py)

```python
# Source: argus/loader.py _read()
Pack(
    name=name,
    manifest=manifest,
    instructions=(pack_dir / "instructions.md").read_text(),
    checklist=self._read_optional(pack_dir / "checklist.md"),
    examples=self._read_optional(pack_dir / "examples.md"),
)
```

`instructions.md` is read with `.read_text()` (required). `checklist.md` and `examples.md` use `_read_optional` (returns None if missing, no error). All four files should be present to provide full pack output.

### Rule file output path (from existing test pattern)

```python
# Generated file lands at: .claude/rules/{pack_name}.md
assert "errors.Is" in (tmp_path / ".claude/rules/go.md").read_text()
assert "Optional.orElseThrow" in (tmp_path / ".claude/rules/java.md").read_text()
assert "requireNotNull" in (tmp_path / ".claude/rules/kotlin.md").read_text()
```

### Test key phrases (stable, live in instructions.md)

| Pack | Key Phrase | Section it lives in |
|------|-----------|---------------------|
| go | `errors.Is` | Error Handling |
| java | `Optional.orElseThrow` | Null Discipline |
| kotlin | `requireNotNull` | Null Safety |

All three phrases are locked by CONTEXT.md decisions — they appear in the content sections as described.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Custom pack discovery via explicit registry | Auto-discovery by directory presence | Phase 18 baseline | New packs require zero code changes |
| Per-pack CLI commands | Generic `packs list`/`packs show` | Phase 18 baseline | No CLI changes needed for Phase 22 |
| Python 2 / Go 1.11 / Java 8 | Python 3.11+, Go 1.21+, Java 17+ | Ongoing | Modern language features available for rule content |

---

## Open Questions

1. **Go Red Flags — table or bullets?**
   - What we know: Python uses bullet-list Red Flags; TypeScript uses a table; both are rendered by the same code path
   - What's unclear: No project decision on which format to use for Go/Java/Kotlin
   - Recommendation: Use the TypeScript table format for Go (Go has distinct violation/principle/fix triples that map well to columns); use bullets for Java and Kotlin which have more prose-style rules. Either works.

2. **Checklist — mirror sections or consolidate?**
   - What we know: CONTEXT.md marks this as Claude's discretion
   - What's unclear: Whether a Java checklist should have 4 sections matching instructions.md or be a flat list
   - Recommendation: Use a flat list (8–12 items) as Python and TypeScript checklists do — flat is more scannable during review

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (with pytest-cov) |
| Config file | `pyproject.toml` `[tool.pytest.ini_options]` |
| Quick run command | `.venv/bin/pytest tests/integration/test_generate.py -x -q` |
| Full suite command | `.venv/bin/pytest` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| LANG-03 | `go` appears in `packs list` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k go -x` | ❌ Wave 0 |
| LANG-03 | `packs show go` renders `errors.Is` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k go -x` | ❌ Wave 0 |
| LANG-03 | `generate` injects `errors.Is` to `.claude/rules/go.md` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k go -x` | ❌ Wave 0 |
| LANG-04 | `java` appears in `packs list` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k java -x` | ❌ Wave 0 |
| LANG-04 | `packs show java` renders `Optional.orElseThrow` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k java -x` | ❌ Wave 0 |
| LANG-04 | `generate` injects `Optional.orElseThrow` to `.claude/rules/java.md` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k java -x` | ❌ Wave 0 |
| LANG-05 | `kotlin` appears in `packs list` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k kotlin -x` | ❌ Wave 0 |
| LANG-05 | `packs show kotlin` renders `requireNotNull` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k kotlin -x` | ❌ Wave 0 |
| LANG-05 | `generate` injects `requireNotNull` to `.claude/rules/kotlin.md` | integration | `.venv/bin/pytest tests/integration/test_generate.py -k kotlin -x` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `.venv/bin/pytest tests/integration/test_generate.py -x -q`
- **Per wave merge:** `.venv/bin/pytest`
- **Phase gate:** Full suite green (coverage ≥80% on changed code) before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/integration/test_generate.py` — add `GO_CONFIG`, `JAVA_CONFIG`, `KOTLIN_CONFIG` isolation constants and nine test functions (3 per pack); file exists but lacks these blocks
- [ ] `argus/packs/go/pack.yml` — does not exist
- [ ] `argus/packs/go/instructions.md` — does not exist
- [ ] `argus/packs/go/checklist.md` — does not exist
- [ ] `argus/packs/go/examples.md` — does not exist
- [ ] `argus/packs/java/pack.yml` — does not exist
- [ ] `argus/packs/java/instructions.md` — does not exist
- [ ] `argus/packs/java/checklist.md` — does not exist
- [ ] `argus/packs/java/examples.md` — does not exist
- [ ] `argus/packs/kotlin/pack.yml` — does not exist
- [ ] `argus/packs/kotlin/instructions.md` — does not exist
- [ ] `argus/packs/kotlin/checklist.md` — does not exist
- [ ] `argus/packs/kotlin/examples.md` — does not exist

---

## Sources

### Primary (HIGH confidence)

- `argus/packs/python/` — direct structural template; all four files inspected
- `argus/packs/typescript/` — second structural template; all four files inspected
- `argus/loader.py` — confirmed auto-discovery mechanism; no code changes required
- `tests/integration/test_generate.py` — confirmed isolation constant pattern and three-test block structure
- `pyproject.toml` — confirmed test runner, coverage config, coverage threshold (80%)
- `.planning/phases/22-go-java-kotlin-language-packs/22-CONTEXT.md` — locked decisions for all three packs

### Secondary (MEDIUM confidence)

- Go 1.21 release notes — `slices`/`maps` packages, `slog` confirmed as standard library additions (Go's backward compatibility guarantee makes 1.21+ a stable baseline)
- Java 17 LTS widely deployed; Java 21 LTS adds pattern matching and virtual threads; Java 22 adds unnamed patterns — confirmed against public Java release schedule
- Kotlin 2.0 K2 compiler stabilized smart casts and value classes — confirmed from Kotlin official blog timeline

### Tertiary (LOW confidence — not needed, content is locked)

- N/A — content sections are fully specified in CONTEXT.md; no ecosystem survey required

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new dependencies; existing infrastructure confirmed by code inspection
- Architecture: HIGH — templates inspected directly from codebase, patterns verified across 6 prior packs
- Pitfalls: HIGH — derived from direct inspection of loader.py and prior integration test patterns
- Content accuracy: MEDIUM — Go/Java/Kotlin idioms are drawn from established community standards; specific rule wording is at Claude's discretion

**Research date:** 2026-06-24
**Valid until:** 2026-12-24 (stable — pack infrastructure is mature, language versions are LTS)
