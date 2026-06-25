# Phase 22: Go, Java & Kotlin Language Packs - Context

**Gathered:** 2026-06-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Ship three new built-in language packs — `go`, `java`, and `kotlin` — that inject
language-specific idiom, style, and discipline rules into agent instruction files. All three
packs must appear in `argus packs list`, be renderable via `argus packs show`, and inject
correct content via `argus generate`. Framework-specific rules (gin/echo for Go, Spring for
Java, Ktor/Android for Kotlin) are out of scope — packs are framework-agnostic.

</domain>

<decisions>
## Implementation Decisions

### Version targets
- Go pack targets **Go 1.21+** — covers `slices`/`maps` stdlib packages, `slog`, type
  inference improvements. Go's strong backward compatibility makes this a safe baseline.
- Java pack targets **Java 17+** — broadens reach to the most widely deployed LTS (17) while
  covering the full 17→25 arc: records (16+), sealed classes/switch expressions (17+),
  pattern matching (21+), virtual threads (21+), unnamed patterns (22+). Rules should note
  minimum Java version where a feature requires ≥17 vs ≥21.
- Kotlin pack targets **Kotlin 2.0+** — K2 compiler era; smart casts more reliable, value
  classes stable. Rules should be accurate for modern Kotlin 2.x.

### Content sections per pack

**Go — 4 sections:**
1. **Error handling** — errors-as-values idiom, `fmt.Errorf` with `%w`, `errors.Is`/`errors.As`
   for unwrapping, no `panic` for expected/recoverable conditions
2. **Interfaces and composition** — implicit interface satisfaction, small interfaces (1–2
   methods), prefer embedding/composition over struct inheritance, no interfaces-before-need
3. **Goroutines and concurrency** — goroutine leak prevention, always propagate `context.Context`,
   prefer channels for ownership transfer, `sync.Mutex` for shared state, avoid `time.Sleep`
   as synchronization
4. **Package and naming** — lowercase package names, CamelCase for exported identifiers,
   unexported lowercase, no `utils`/`helpers` packages, use `slices` and `maps` packages
   over manual index arithmetic

**Java 17+ — 4 sections:**
1. **Modern Java types** — records for immutable data carriers, sealed classes + switch
   expressions for closed type hierarchies (ADTs), `var` for local type inference where it
   improves readability, text blocks for multiline strings, unnamed patterns/variables (22+)
2. **Null discipline** — `Optional<T>` as return type for absent values, never return `null`
   from public APIs, use `Optional.orElseThrow()` over `.get()`, never use `Optional` as a
   field type or parameter type
3. **OOP discipline** — prefer composition over inheritance, make classes `final` by default,
   keep interfaces narrow (ISP), avoid god classes (>300 lines), use `record` not a mutable
   class for data-only objects
4. **Exception handling** — choose unchecked exceptions for unrecoverable conditions, checked
   for caller-recoverable conditions; never catch `Exception` broadly; no exceptions for
   control flow; always use specific exception types

**Kotlin 2.0+ — 4 sections:**
1. **Null safety** — use `?` nullable types and `?.` safe calls, prefer `?.let` for null-
   conditional blocks, use `!!` only when provably non-null (add a comment explaining why),
   `requireNotNull`/`checkNotNull` at function entry points, explicitly guard Java interop
   boundaries with null checks
2. **Idiomatic Kotlin** — `data class` for DTOs and value objects, `when` expressions over
   `if/else` chains, destructuring declarations where they aid clarity, extension functions
   to add behavior without subclassing, `object` for singletons instead of companion object
   hacks or static-method classes
3. **Coroutines** — mark async functions with `suspend`, use `Flow` for streams of values,
   always launch coroutines within a structured scope (never `GlobalScope`), use
   `withContext(Dispatchers.IO)` for blocking I/O, cancel scopes when done
4. **Kotlin-over-Java idioms** — prefer Kotlin collection API (`filter`, `map`, `flatMap`)
   over Java Streams, use string templates over concatenation or `String.format`, use scope
   functions (`apply`, `let`, `run`, `also`) purposefully with a consistent mental model
   (transform → use `let`, configure → use `apply`)

### Java/Kotlin relationship
- **Fully independent** — each pack is self-contained with no cross-references between them.
  Matches the Python/TypeScript precedent from Phase 21.
- Teams using both languages enable both packs; rules stack additively.
- No "prefer Kotlin over Java" guidance in either pack.

### Framework-agnostic rule
- Go pack: no gin, echo, fiber, or framework-specific rules
- Java pack: no Spring, Jakarta EE, or Quarkus-specific rules
- Kotlin pack: no Ktor, Android, or Compose-specific rules
- Follows the TypeScript precedent (no React/Vue/Next.js) from Phase 21

### Pack metadata (follows Phase 21 precedent)
- `category: language` for all three packs
- `requires: []` — standalone, no inter-pack dependencies
- `platforms: [all]`

### Claude's Discretion
- Exact selection of which 15–20 rules to include per pack within each section
- Specific example code in `examples.md` for each language
- Wording of Red Flags table entries
- Whether `checklist.md` mirrors `instructions.md` sections exactly or consolidates

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` §Language Packs — LANG-03 (go), LANG-04 (java), LANG-05
  (kotlin) acceptance criteria and topic areas

### Pack format reference (language pack template)
- `argus/packs/python/` — direct template for language pack structure (pack.yml, instructions.md,
  checklist.md, examples.md); content uses `category: language`
- `argus/packs/typescript/` — second reference for language pack format and density
- `argus/packs/security/` — reference for examples.md with secure/insecure side-by-side format

### Test pattern
- `tests/integration/test_generate.py` — isolation config constant pattern (GO_CONFIG,
  JAVA_CONFIG, KOTLIN_CONFIG) + 3-assertion test (packs list / packs show / generate injects
  key phrase); must follow the same pattern as PYTHON_CONFIG / TYPESCRIPT_CONFIG

### Roadmap success criteria
- `.planning/ROADMAP.md` §Phase 22 — success criteria that define "done" for each pack

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `argus/packs/python/` — complete working language pack to copy and adapt; no structural
  changes needed, only content replacement
- `argus/packs/typescript/` — second working language pack; confirms the pattern is stable
- `argus/loader.py` — auto-discovers packs from `argus/packs/`; no changes needed for new packs
- `tests/integration/test_generate.py` — extend with GO_CONFIG, JAVA_CONFIG, KOTLIN_CONFIG
  isolation constants following PYTHON_CONFIG and TYPESCRIPT_CONFIG precedents

### Established Patterns
- Each language pack: `pack.yml` + `instructions.md` + `checklist.md` + `examples.md`
- `pack.yml`: `category: language`, `requires: []`, `platforms: [all]`
- Test key phrase: pick a unique string from `instructions.md` that won't change (e.g.,
  `errors.Is` for Go, `Optional.orElseThrow` for Java, `requireNotNull` for Kotlin)
- Test runner: `.venv/bin/pytest` (not bare `pytest`)

### Integration Points
- `argus packs list` — new packs appear automatically; `language` category already established
- `argus packs show go` / `show java` / `show kotlin` — no code changes needed
- `argus generate` — injects pack content; no generator changes needed

</code_context>

<specifics>
## Specific Ideas

- No specific requirements — open to standard approaches for rule content selection within
  the LANG-03/LANG-04/LANG-05 topic areas

</specifics>

<deferred>
## Deferred Ideas

- JVM interop pack (`jvm-interop`) covering Java↔Kotlin co-existence rules — future phase
- Framework packs for Spring (Java), Ktor/Android (Kotlin), gin/echo (Go) — Phase 23/24 scope

</deferred>

---

*Phase: 22-go-java-kotlin-language-packs*
*Context gathered: 2026-06-24*
