# Phase 21: Python & TypeScript Language Packs - Research

**Researched:** 2026-06-24
**Domain:** Pack authoring — Python idioms, TypeScript strict mode, Argus pack file format
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**type-safety overlap (Python)**
- Python pack is strictly non-type content: PEP 8 style, naming conventions, dataclasses,
  idiomatic Python (f-strings, comprehensions, context managers, pathlib, etc.)
- Zero overlap with the `type-safety` pack — annotation rules, mypy, `X | None` stay there
- No cross-reference or coupling between the two packs — they are additive, not dependent

**Content depth**
- Moderate coverage: 15–20 rules per pack, organized into 3–4 thematic sections
- Comparable density to the security pack (6 OWASP categories + input validation)
- High-signal, directly actionable rules — not a comprehensive language reference

**Content format**
- Mirror the security pack structure:
  - `instructions.md`: Category sections + Red Flags table at end
  - `checklist.md`: Checklist items matching categories
  - `examples.md`: Code examples organized by category
  - `pack.yml`: metadata with `category: language`
- Do NOT use the simpler process-pack format (no separate examples.md)

**Category & discovery**
- `category: language` in `pack.yml` for both packs
- Sets the convention for Phase 22 (go, java, kotlin) and all future language packs
- Allows `argus packs list` to group under a "Language Packs" heading

### Claude's Discretion

- Exact selection of which 15–20 rules to include per pack (within the LANG-01/LANG-02 topic areas)
- Section naming and ordering within each pack
- Specific example code chosen for `examples.md`
- Whether `requires:` in pack.yml references any other packs

### Deferred Ideas (OUT OF SCOPE)

- None — discussion stayed within phase scope
</user_constraints>

---

## Summary

Phase 21 ships two new built-in packs: `python` and `typescript`. These are content-authoring tasks
with a thin infrastructure component — the `category: language` field in `pack.yml` is new and may
require a CLI display change if `packs list` is to group by category.

The Argus pack system is fully operational: drop a directory under `argus/packs/` with the four
required files and the pack is automatically discovered. No loader changes are needed. The only
code change risk is if `packs list` needs grouping logic — currently it lists all packs flat. The
CONTEXT.md says the category "allows `argus packs list` to group under a 'Language Packs' heading"
which may or may not require a CLI change (see Open Questions).

The primary work is content: selecting 15–20 high-signal, actionable rules per pack, organizing
them into 3–4 thematic sections, writing idiomatic code examples, and authoring the checklist.
The test pattern is identical to every prior pack: three integration tests (list, show, generate)
plus an isolation config constant.

**Primary recommendation:** Follow the Phase 20 security pack plan exactly — TDD three failing
integration tests first, then author the four pack files. Do the same twice: once for `python`,
once for `typescript`.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pytest | (existing) | Test runner | Already in project; integration tests use CliRunner |
| click.testing.CliRunner | (existing) | Invoke CLI in tests | Established pattern for all pack integration tests |
| PyYAML | (existing) | Pack manifest parsing | Used by PackLoader._read for pack.yml |

No new dependencies required. Both packs are purely content files plus minor test additions.

**Version verification:** No new packages to install.

---

## Architecture Patterns

### Pack Directory Layout

Every pack must contain exactly these four files:

```
argus/packs/python/
├── pack.yml          # metadata: name, description, category, requires, platforms
├── instructions.md   # H2-sectioned rules + Red Flags table at end
├── checklist.md      # checkbox items matching instruction categories
└── examples.md       # before/after code examples per category

argus/packs/typescript/
├── pack.yml
├── instructions.md
├── checklist.md
└── examples.md
```

### Pattern 1: pack.yml for a Language Pack

New field introduced in Phase 21: `category: language`

```yaml
# argus/packs/python/pack.yml
name: python
description: PEP 8 style, idiomatic Python, dataclasses, and naming conventions
category: language
requires: []
platforms: [all]
```

```yaml
# argus/packs/typescript/pack.yml
name: typescript
description: Strict mode, interface vs type, generics discipline, and no-any rules
category: language
requires: []
platforms: [all]
```

The `requires: []` field is the correct choice (no coupling to other packs per locked decisions).

### Pattern 2: instructions.md Structure (mirror security pack)

```markdown
# Python

## PEP 8 Style
- [rule]
- [rule]

## Naming Conventions
- [rule]
- [rule]

## Idiomatic Python
- [rule]
- [rule]

## Dataclasses and Data Structures
- [rule]
- [rule]

## Red Flags — Stop and Correct
- [red flag item]
- [red flag item]
```

### Pattern 3: Integration Test Structure (established pattern)

```python
# Source: tests/integration/test_generate.py — existing pattern for every pack

PYTHON_CONFIG = """\
packs:
  - python
platforms:
  - claude
"""

def test_python_pack_appears_in_packs_list():
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "python" in result.output

def test_python_pack_show_renders_content():
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "show", "python"])
    assert result.exit_code == 0
    assert "<key_phrase>" in result.output  # phrase from instructions.md

def test_python_pack_generate_injects_content(tmp_path):
    (tmp_path / ".argus.yml").write_text(PYTHON_CONFIG)
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "<key_phrase>" in (tmp_path / ".claude/rules/python.md").read_text()
```

Key phrase selection rule (from STATE.md decisions): choose a phrase that lives in
`instructions.md` (not `examples.md`) and is specific enough to survive future content edits.
Prior examples: "mypy", "system boundaries", "imperative mood", "parameterized".

### Anti-Patterns to Avoid

- **Using `examples.md` key phrase in tests:** The test asserts against `instructions.md` content (via `packs show`); `examples.md` is not rendered by `packs show`. Use a phrase from `instructions.md`.
- **Adding `requires:` dependencies:** Locked decision: no coupling between packs.
- **Type annotation rules in python pack:** Locked decision: `X | None`, `mypy`, annotation rules stay in `type-safety` pack.
- **Using the `category: quality` or `category: workflow` values:** Both new packs use `category: language`.
- **Modifying loader.py or cli.py for basic discovery:** The loader already auto-discovers all pack directories — no loader changes needed to add new packs.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Pack discovery | Custom registration/registry code | Drop directory into `argus/packs/` | PackLoader.available_packs() iterates `argus/packs/` automatically |
| Test isolation | Shared FULL_CONFIG | Dedicated `PYTHON_CONFIG` / `TYPESCRIPT_CONFIG` constants | Follows established isolation pattern; prevents config coupling between test groups |
| Category grouping (if needed) | New data structure or separate config | `manifest["category"]` already loaded into Pack.manifest dict | The `category` field is in pack.yml and loaded into `Pack.manifest["category"]` via PyYAML |

**Key insight:** The Argus pack system is content-driven. Infrastructure already handles everything;
the primary deliverable is well-authored, high-signal content in the four pack files.

---

## Common Pitfalls

### Pitfall 1: Key Phrase in examples.md Rather Than instructions.md

**What goes wrong:** Test for `packs show python` asserts on a string that only appears in
`examples.md`. The `packs_show` command renders `pack.instructions` (instructions.md only), so
the test passes `packs show` but would fail if examples.md were the only location for the phrase.
**Why it happens:** Tester picks a code example (e.g., `f"Hello {name}"`) as the key phrase.
**How to avoid:** Always choose a key phrase that appears verbatim in `instructions.md`.
**Warning signs:** Test passes `packs show` but the asserted phrase doesn't appear in instructions.md.

### Pitfall 2: Python Rules Overlapping with type-safety Pack

**What goes wrong:** Python pack includes rules about type annotations, `mypy`, `X | None`, or
`Optional[X]`. This creates duplicate guidance when a user applies both packs.
**Why it happens:** Type hints feel like "idiomatic Python" but are already owned by `type-safety`.
**How to avoid:** Locked decision: python pack covers PEP 8 style, naming, idioms, dataclasses —
zero annotation rules. When in doubt, if it mentions `mypy` or `: type`, it belongs in type-safety.
**Warning signs:** Any rule mentioning `mypy`, `Optional`, `-> None`, `X | None`, or `typing`.

### Pitfall 3: TypeScript Rules Duplicating Future Framework Content

**What goes wrong:** TypeScript pack includes Next.js or React-specific rules that belong in
the `nextjs` framework pack (Phase 23). The TypeScript pack must be framework-agnostic.
**Why it happens:** TypeScript is commonly used with React; temptation to include JSX/component rules.
**How to avoid:** TypeScript pack covers language-level rules only: strict mode, `interface` vs
`type`, generics, `noImplicitAny`, `unknown` vs `any`, utility types. No framework imports.
**Warning signs:** Any rule mentioning React, JSX, Next.js, Vue, or specific npm packages.

### Pitfall 4: `category: language` Field Breaks packs list Without CLI Change

**What goes wrong:** Current `packs_list` command simply calls `loader.available_packs()` and
prints each name. A new `category` field in pack.yml has no effect on this output — packs just
appear alphabetically alongside all other packs.
**Why it happens:** The CONTEXT.md says the category "allows grouping under a Language Packs
heading" — this may be aspirational for a future phase rather than a Phase 21 requirement.
**How to avoid:** Check the Phase 21 success criteria (ROADMAP.md §Phase 21): criteria 3 says
"both packs appear in `argus packs list` under a recognizable language category." If the planner
interprets this as requiring CLI grouping, a CLI change is needed. If "recognizable" means the
name alone is sufficient, no CLI change is needed.
**Warning signs:** If the test for criteria 3 asserts on category grouping output (e.g., "Language
Packs"), a CLI change is required; if it only asserts `"python" in result.output`, no change is
needed.

---

## Code Examples

### pack.yml — Language Pack (verified against existing packs)

```yaml
# Source: argus/packs/security/pack.yml and argus/packs/tdd/pack.yml
name: python
description: PEP 8 style, idiomatic Python, dataclasses, and naming conventions
category: language
requires: []
platforms: [all]
```

### Suggested Python Pack Content Sections

Based on LANG-01 acceptance criteria and the locked non-type scope:

**Section 1 — PEP 8 Style**
- 4-space indentation; no tabs
- Lines max 88 characters (Black default) or 79 (PEP 8 strict)
- Two blank lines between top-level definitions; one between methods
- Imports grouped: stdlib, third-party, local — each group separated by blank line

**Section 2 — Naming Conventions**
- `snake_case` for variables, functions, modules; `PascalCase` for classes
- `UPPER_SNAKE_CASE` for module-level constants
- Single leading underscore `_name` for internal; double `__name` for name-mangled
- Avoid single-letter names except loop indices; avoid shadowing builtins (`list`, `id`, `type`)

**Section 3 — Idiomatic Python**
- Prefer f-strings over `.format()` or `%` interpolation
- Use list/dict/set comprehensions over explicit loops for simple transforms
- Use `with` statement (context manager) for all resource management (files, locks, connections)
- Use `pathlib.Path` instead of `os.path` for filesystem operations
- Use `enumerate()` and `zip()` instead of manual index arithmetic
- Prefer `is None` / `is not None` over `== None` / `!= None`

**Section 4 — Dataclasses and Data Structures**
- Use `@dataclass` for plain data containers; prefer over raw dicts for structured data
- Use `@dataclass(frozen=True)` for immutable value objects
- Use `namedtuple` or `@dataclass` over positional tuples with semantic meaning
- Use `dict` for dynamic key-value maps; `@dataclass` for fixed-schema objects

### Suggested TypeScript Pack Content Sections

Based on LANG-02 acceptance criteria:

**Section 1 — Strict Mode**
- Always enable `"strict": true` in tsconfig.json — never disable individual strict flags
- Enable `"noUncheckedIndexedAccess"` for array and object index safety
- Enable `"exactOptionalPropertyTypes"` to prevent assigning `undefined` to optional props

**Section 2 — Interface vs Type**
- Use `interface` for object shapes that may be extended (classes, API contracts, props)
- Use `type` for unions, intersections, mapped types, and aliases to primitives
- Never use `interface` for function types — use `type` with a function signature
- Prefer `interface` over `type` for public API shapes (declaration merging is a benefit)

**Section 3 — Generics**
- Name type parameters `T`, `K`, `V` for single-purpose; use descriptive names (`TItem`, `TKey`) for complex generics
- Constrain generics with `extends` when the implementation requires a specific shape
- Avoid unbounded `<T>` when the function body needs properties of `T` — always constrain
- Use `unknown` as the safe top type instead of `any` in generic fallbacks

**Section 4 — No-Any Discipline**
- Never use `any` — use `unknown` for values of unknown type and narrow with type guards
- Never use `as any` casts — use `as unknown as T` with a comment justifying the cast
- Never use `@ts-ignore` — use `@ts-expect-error` with an explanation comment
- Avoid `Object`, `Function`, `{}` as types — they are too broad; use specific shapes

### checklist.md Structure (verified against security pack)

```markdown
## Python Checklist

- [ ] f-strings used for string interpolation — no .format() or % strings
- [ ] All resource management uses with statement — no manual .close() calls
- [ ] pathlib.Path used for filesystem operations — no os.path calls
- [ ] ...
```

---

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| `category: quality` / `category: workflow` | `category: language` | New category value; all future language packs follow this |
| Manual `os.path` in Python | `pathlib.Path` | PEP 428, Python 3.4+; idiomatic since 3.6+ |
| TypeScript `any` as escape hatch | `unknown` + type narrowing | TypeScript 3.0+; `unknown` is the safe alternative |
| `interface` for everything in TS | `interface` for shapes, `type` for unions/aliases | Community consensus; TypeScript team guidance |

---

## Open Questions

1. **Does `packs list` need grouping by category in Phase 21?**
   - What we know: ROADMAP success criteria 3 says "both packs appear in `argus packs list` under a recognizable language category." Current `packs_list` in cli.py prints names flat with no category grouping.
   - What's unclear: Whether "recognizable language category" means the CLI must show a "Language Packs" heading, or whether having a `category: language` field in pack.yml is sufficient metadata for a future phase.
   - Recommendation: The planner should decide whether to include a CLI grouping task. If yes, add a task to modify `packs_list` to group by `manifest["category"]`. If no, add a note that criteria 3 is satisfied by the pack name alone being visible. Looking at the Phase 20 precedent (security pack had no grouping requirement), no CLI change was needed then — likely the same here.

2. **Key phrase selection for TypeScript pack test**
   - What we know: The test for `packs show typescript` needs a phrase from `instructions.md` that is stable and specific.
   - Recommendation: `"strict"` is the highest-signal candidate (appears in "strict mode" section, unlikely to be removed). Could also use `"noImplicitAny"` or `"unknown"`. Planner should pick one and lock it.

3. **Key phrase selection for Python pack test**
   - Recommendation: `"f-string"` or `"pathlib"` are both specific and stable candidates from `instructions.md`. `"PEP 8"` is also a safe choice as it will appear in the H1 or a section header.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (existing) |
| Config file | pyproject.toml (`[tool.pytest.ini_options]`) |
| Quick run command | `.venv/bin/pytest tests/integration/test_generate.py -x` |
| Full suite command | `.venv/bin/pytest` |

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| LANG-01 | `python` pack appears in `packs list` | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_python_pack_appears_in_packs_list -x` | No — Wave 0 |
| LANG-01 | `packs show python` renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_python_pack_show_renders_content -x` | No — Wave 0 |
| LANG-01 | `generate` injects python pack content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_python_pack_generate_injects_content -x` | No — Wave 0 |
| LANG-02 | `typescript` pack appears in `packs list` | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_typescript_pack_appears_in_packs_list -x` | No — Wave 0 |
| LANG-02 | `packs show typescript` renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_typescript_pack_show_renders_content -x` | No — Wave 0 |
| LANG-02 | `generate` injects typescript pack content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_typescript_pack_generate_injects_content -x` | No — Wave 0 |

### Sampling Rate

- **Per task commit:** `.venv/bin/pytest tests/integration/test_generate.py -x`
- **Per wave merge:** `.venv/bin/pytest`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] 6 new test functions in `tests/integration/test_generate.py` — covers LANG-01 and LANG-02 (add to existing file, not a new file)
- [ ] `PYTHON_CONFIG` and `TYPESCRIPT_CONFIG` constants in `tests/integration/test_generate.py`

*(No new test files needed — extend the existing `test_generate.py` per established pattern)*

---

## Sources

### Primary (HIGH confidence)

- Direct file read: `argus/packs/security/` — exact format to mirror (instructions.md, checklist.md, examples.md, pack.yml)
- Direct file read: `argus/packs/tdd/pack.yml` — pack.yml field structure reference
- Direct file read: `argus/loader.py` — confirms auto-discovery, no loader changes needed
- Direct file read: `argus/cli.py` — confirms current packs_list behavior (flat list, no grouping)
- Direct file read: `tests/integration/test_generate.py` — exact test pattern for all 6 new tests
- Direct file read: `argus/adapters/base.py` — confirms `packs_show` renders `pack.instructions` only

### Secondary (MEDIUM confidence)

- `.planning/ROADMAP.md` §Phase 21 — success criteria; interpreted "recognizable language category" as probably not requiring grouping CLI change
- `.planning/STATE.md` — key phrase selection rule and isolation constant pattern

### Tertiary (LOW confidence)

- None

---

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — no new dependencies; all existing infrastructure verified by direct file reads
- Architecture: HIGH — pack format directly observed in security pack; test pattern directly observed in test_generate.py
- Pitfalls: HIGH — derived from locked decisions in CONTEXT.md and observed code behavior
- Content recommendations: MEDIUM — Python/TypeScript idiom selection is well-established community practice but not verified against a live authoritative source

**Research date:** 2026-06-24
**Valid until:** 2026-07-24 (stable domain; pack format won't change within v1.1)
