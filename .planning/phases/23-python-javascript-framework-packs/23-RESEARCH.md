# Phase 23: Python & JavaScript Framework Packs - Research

**Researched:** 2026-06-25
**Domain:** Pack authoring — FastAPI framework pack, Next.js framework pack
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**FastAPI — version target**
- FastAPI 0.100+ (Pydantic v2 era)
- Rules use Pydantic v2 syntax: `model_config`, `model_validator`, `field_validator`
- No v1 compatibility shims or dual-version guidance

**FastAPI — async stance**
- Async-first: always `async def` for route handlers
- Sync `def` only for CPU-bound work that runs in a thread pool (explicit exception)
- This is a hard rule, not a guideline

**FastAPI — Pydantic scope**
- FastAPI-specific Pydantic usage only (not a general Pydantic tutorial):
  - Request/response models as the type boundary for endpoints
  - `Field()` for API-level validation (min/max, description, alias)
  - `model_config` for serialization settings (`populate_by_name`, `from_attributes`)
  - `model_validator` for cross-field validation logic
- General Pydantic patterns (settings management, discriminated unions, serialization) are out of scope

**FastAPI — router organization**
- `APIRouter` per feature/domain, assembled in a central `main.py` or `app.py`
- Each router: prefix + tags defined at router level, not endpoint level
- Standard FastAPI scaling pattern — agents must follow it

**Next.js — version target**
- Next.js 14+ App Router
- `app/` directory conventions: `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`

**Next.js — Pages Router**
- App Router only — no Pages Router content in this pack
- No migration guidance, no legacy patterns

**Next.js — React hooks discipline**
- Hooks are Client Components only — `'use client'` directive required when using hooks
- No hooks in Server Components
- `useCallback` / `useMemo` only when there is a measured performance need (not by default)

**Pack overlap boundary**
- Framework packs are additive — they never duplicate content from the parent language pack
- FastAPI pack: assumes python pack is in scope; FastAPI-specific patterns live here; generic Python idioms stay in python pack
- Next.js pack: assumes typescript pack is in scope; React/App Router-specific TypeScript patterns live here; TS fundamentals stay in typescript pack
- Content convention only, not runtime enforcement — both packs use `requires: []`

**Category & discovery**
- `category: framework` for both packs
- `requires: []` — standalone
- `platforms: [all]`

### Claude's Discretion
- Exact selection of which 15–20 rules to include per pack within each section
- Section naming and ordering within each pack
- Specific example code chosen for `examples.md`
- Key test phrases (unique strings from `instructions.md`, stable across edits)
- Whether 3 or 4 thematic sections per pack

### Deferred Ideas (OUT OF SCOPE)
- Spring and Mockito framework packs — Phase 24
- Standalone Pydantic pack (settings management, discriminated unions) — future phase
- Pages Router compatibility pack — future phase (if demand emerges)
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| FWRK-01 | User can apply `fastapi` pack for dependency injection, async patterns, Pydantic model, and router organization rules | Pack authoring pattern fully understood from phases 21–22; FastAPI domain content locked by CONTEXT.md decisions |
| FWRK-02 | User can apply `nextjs` pack for App Router, server components, React hooks discipline, and TypeScript integration rules | Pack authoring pattern fully understood from phases 21–22; Next.js domain content locked by CONTEXT.md decisions |
</phase_requirements>

---

## Summary

Phase 23 ships two framework packs: `fastapi` and `nextjs`. The implementation pattern is
identical to Phases 21 and 22 (python, typescript, go, java, kotlin packs) — create a
four-file pack directory under `argus/packs/` and add three integration tests per pack
following the `FASTAPI_CONFIG` / `NEXTJS_CONFIG` isolation constant pattern.

No infrastructure changes are needed. `loader.py` auto-discovers directories under
`argus/packs/`, so adding `argus/packs/fastapi/` and `argus/packs/nextjs/` is sufficient for
`packs list` and `packs show` to work. The generator injects content without modification.
The only new code is the pack files themselves and their integration tests.

Content decisions are fully locked by CONTEXT.md. The main authoring task is selecting
15–20 rules per pack across 3–4 sections, writing actionable `instructions.md` and
`checklist.md` content, and providing Avoid/Prefer examples in `examples.md`.

**Primary recommendation:** Copy the python pack directory structure as a template. Author
FastAPI content first (simpler domain), then Next.js. Add 3 integration tests per pack
following the KOTLIN_CONFIG precedent verbatim. No infrastructure code changes needed.

---

## Standard Stack

### Core (pack authoring — no new dependencies)
| Component | Version | Purpose |
|-----------|---------|---------|
| `argus/packs/<name>/pack.yml` | n/a | Pack manifest: name, category, requires, platforms |
| `argus/packs/<name>/instructions.md` | n/a | Rules injected into platform instruction files |
| `argus/packs/<name>/checklist.md` | n/a | Pre-commit checklist items |
| `argus/packs/<name>/examples.md` | n/a | Avoid/Prefer side-by-side code examples |

No new Python packages are required. All infrastructure already exists.

**Installation:** None required.

---

## Architecture Patterns

### Pack Directory Structure (established, non-negotiable)
```
argus/packs/
├── fastapi/
│   ├── pack.yml
│   ├── instructions.md
│   ├── checklist.md
│   └── examples.md
└── nextjs/
    ├── pack.yml
    ├── instructions.md
    ├── checklist.md
    └── examples.md
```

### Pattern 1: pack.yml manifest
**What:** YAML manifest consumed by `PackLoader._read()`. The `category` field is rendered
as-is in `packs list` — "framework" is a new value but the loader renders any string, so
no loader change is needed.

```yaml
# argus/packs/fastapi/pack.yml
name: fastapi
description: Async-first routing, Pydantic v2 models, and dependency injection patterns
category: framework
requires: []
platforms: [all]
```

```yaml
# argus/packs/nextjs/pack.yml
name: nextjs
description: App Router conventions, server components, and React hooks discipline
category: framework
requires: []
platforms: [all]
```

### Pattern 2: instructions.md content structure
**What:** Markdown with H2 sections, each containing 4–6 bullet rules. Exactly matches
the python and kotlin packs in density and format. Ends with a "Red Flags — Stop and Correct"
section, which is the established closer for all language/framework packs.

**FastAPI sections (locked topics from FWRK-01):**
1. Async Patterns — route handlers always `async def`, sync only for CPU-bound work
2. Pydantic Models — request/response models, `Field()`, `model_config`, `model_validator`
3. Dependency Injection — `Depends()`, injectable services, testability pattern
4. Router Organization — `APIRouter` per domain, prefix+tags at router level, assembled in main

**Next.js sections (locked topics from FWRK-02):**
1. App Router Conventions — `app/` directory, `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`
2. Server vs Client Components — default to Server Components, `'use client'` only when needed
3. React Hooks Discipline — hooks require `'use client'`, no premature `useCallback`/`useMemo`
4. TypeScript Integration — route param types, component prop interfaces, `use server`/`use client` directives

### Pattern 3: Integration test structure (the mandatory 3-test set)
**What:** Three tests per pack, following the exact same structure as all prior packs.
Isolation constant named `FASTAPI_CONFIG` / `NEXTJS_CONFIG` — not added to `FULL_CONFIG`.
Key phrase is a unique string from `instructions.md` that is stable across future edits.

```python
# Source: tests/integration/test_generate.py — existing pattern, replicated verbatim

FASTAPI_CONFIG = """\
packs:
  - fastapi
platforms:
  - claude
"""

def test_fastapi_pack_appears_in_packs_list():
    """Given packs list is invoked, fastapi appears in the output."""
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "fastapi" in result.output


def test_fastapi_pack_show_renders_content():
    """Given packs show fastapi is invoked, <key_phrase> appears in the output."""
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "show", "fastapi"])
    assert result.exit_code == 0
    assert "<key_phrase>" in result.output


def test_fastapi_pack_generate_injects_content(tmp_path):
    """Given a fastapi+claude config, generate writes content to .claude/rules/fastapi.md."""
    (tmp_path / ".argus.yml").write_text(FASTAPI_CONFIG)
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "<key_phrase>" in (tmp_path / ".claude/rules/fastapi.md").read_text()
```

**Key phrase selection rule (from STATE.md decisions):** Pick a unique string from
`instructions.md` that is stable and unlikely to change. Suggested anchors:
- FastAPI: `APIRouter` — appears in Router Organization section, framework-unique, stable
- Next.js: `use client` — appears in both Server/Client and Hooks sections, framework-unique, stable

### Anti-Patterns to Avoid
- **Duplicate language pack content:** Never repeat python pack rules (PEP 8, pathlib, f-strings)
  in the FastAPI pack. Never repeat typescript pack rules (strict mode, no-any) in the Next.js pack.
- **General Pydantic tutorial content:** `BaseSettings`, discriminated unions, custom serializers
  are out of scope per CONTEXT.md — keep only FastAPI endpoint model patterns.
- **Pages Router content:** Any `pages/`, `getServerSideProps`, `getStaticProps` references are
  forbidden in the Next.js pack per CONTEXT.md.
- **Adding packs to REQUIRED_PACKS or VALID_CATEGORIES in test_packs.py:** The existing
  `test_packs.py` validates only the original process packs with `VALID_CATEGORIES =
  {"workflow", "architecture", "quality", "process"}`. Language and framework packs are NOT
  in `REQUIRED_PACKS` and are NOT validated there. Do not modify `test_packs.py` — the
  integration test suite in `test_generate.py` is the correct validation surface.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---------|-------------|-------------|
| Pack discovery | Custom registry, config entries | Drop directory into `argus/packs/` — `PackLoader.available_packs()` discovers it |
| Category rendering | Category enum, validation | `category: framework` string in pack.yml — loader passes it through as-is |
| Test isolation | Shared config mutation | Isolated `FASTAPI_CONFIG` constant — exactly like `KOTLIN_CONFIG`, `GO_CONFIG` |
| Framework content | Write from scratch | Check CONTEXT.md — content decisions are pre-made; execution is authoring, not design |

---

## Common Pitfalls

### Pitfall 1: Modifying test_packs.py VALID_CATEGORIES
**What goes wrong:** Developer sees `VALID_CATEGORIES = {"workflow", "architecture", "quality", "process"}` and adds `"framework"` and `"language"` to it, then adds new packs to `REQUIRED_PACKS`.
**Why it happens:** `test_packs.py` looks like the canonical pack test, but it only covers original process packs.
**How to avoid:** Add tests ONLY to `tests/integration/test_generate.py` following the 3-test per pack pattern. Never modify `REQUIRED_PACKS` or `VALID_CATEGORIES` in `test_packs.py`.
**Warning signs:** PR touches `tests/test_packs.py` — that file should not change in Phase 23.

### Pitfall 2: Duplicating parent language pack content
**What goes wrong:** FastAPI pack repeats "use f-strings" or "use pathlib" from the python pack. Next.js pack repeats "noImplicitAny" from the typescript pack.
**Why it happens:** The rules feel relevant and the author is unsure what belongs where.
**How to avoid:** Before writing any rule, ask "Does this belong in the python/typescript pack?" If yes, omit it. FastAPI pack = FastAPI-specific application of Python; Next.js pack = App Router-specific application of TypeScript.
**Warning signs:** Instructions.md contains mypy, PEP 8, f-strings, pathlib (FastAPI) or noImplicitAny, strict mode, generics basics (Next.js).

### Pitfall 3: Wrong test runner
**What goes wrong:** Tests invoked with bare `pytest` instead of `.venv/bin/pytest`.
**Why it happens:** Developer habit.
**How to avoid:** Always use `.venv/bin/pytest` as noted in STATE.md.
**Warning signs:** `pytest: command not found` or tests running against wrong environment.

### Pitfall 4: Key phrase appears in checklist.md or examples.md but not instructions.md
**What goes wrong:** Test asserts on key phrase in `packs show` output, which renders `instructions.md`. If phrase only appears in checklist or examples, the show test fails.
**Why it happens:** Author puts the distinctive term only in checklist or examples.
**How to avoid:** Confirm key phrase appears verbatim in `instructions.md`. The `packs show` command renders `pack.instructions` only (from `loader._read()` — `instructions.md`).
**Warning signs:** `test_fastapi_pack_show_renders_content` fails even though the pack directory exists.

### Pitfall 5: Scope creep into Pydantic general patterns
**What goes wrong:** FastAPI pack includes `BaseSettings` for config, custom serializers, or discriminated unions.
**Why it happens:** These are real FastAPI-adjacent patterns.
**How to avoid:** Per CONTEXT.md decisions — any Pydantic pattern not directly tied to request/response model typing or endpoint validation is out of scope for this pack.

---

## Code Examples

### FastAPI — correct pack.yml
```yaml
name: fastapi
description: Async-first routing, Pydantic v2 models, and dependency injection patterns
category: framework
requires: []
platforms: [all]
```

### Next.js — correct pack.yml
```yaml
name: nextjs
description: App Router conventions, server components, and React hooks discipline
category: framework
requires: []
platforms: [all]
```

### Integration test isolation constant (FastAPI)
```python
FASTAPI_CONFIG = """\
packs:
  - fastapi
platforms:
  - claude
"""
```

### Integration test isolation constant (Next.js)
```python
NEXTJS_CONFIG = """\
packs:
  - nextjs
platforms:
  - claude
"""
```

### How packs show renders content (loader.py reference)
```python
# argus/cli.py packs_show command — renders pack.instructions (instructions.md only)
pack = loader.load([name])[0]
click.echo(pack.instructions)
# Key phrase MUST be in instructions.md, not checklist.md or examples.md
```

---

## State of the Art

| Prior Phase | Established Pattern | Applies to Phase 23 |
|-------------|--------------------|--------------------|
| Phase 21 (python, typescript) | `category: language`, `requires: []`, isolation config constant | Use `category: framework` instead; all other patterns identical |
| Phase 22 (go, java, kotlin) | 3 tests per pack in `test_generate.py`, key phrase from `instructions.md` | Replicate verbatim |
| Phase 20 (security) | Avoid/Prefer side-by-side examples.md format | Use for FastAPI and Next.js examples |
| All packs | Red Flags section closes `instructions.md` | Mandatory for both packs |

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (detected: `pytest.ini` not present, configured via pyproject.toml coverage) |
| Config file | `pyproject.toml` (coverage threshold 80%) |
| Quick run command | `.venv/bin/pytest tests/integration/test_generate.py -x` |
| Full suite command | `.venv/bin/pytest` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FWRK-01 | fastapi pack appears in packs list | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_fastapi_pack_appears_in_packs_list -x` | ❌ Wave 0 |
| FWRK-01 | fastapi pack show renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_fastapi_pack_show_renders_content -x` | ❌ Wave 0 |
| FWRK-01 | fastapi generate injects content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_fastapi_pack_generate_injects_content -x` | ❌ Wave 0 |
| FWRK-02 | nextjs pack appears in packs list | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_nextjs_pack_appears_in_packs_list -x` | ❌ Wave 0 |
| FWRK-02 | nextjs pack show renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_nextjs_pack_show_renders_content -x` | ❌ Wave 0 |
| FWRK-02 | nextjs generate injects content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_nextjs_pack_generate_injects_content -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `.venv/bin/pytest tests/integration/test_generate.py -x`
- **Per wave merge:** `.venv/bin/pytest`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] 6 new test functions in `tests/integration/test_generate.py` — covers FWRK-01 and FWRK-02
- [ ] `argus/packs/fastapi/` directory with 4 files — covers FWRK-01
- [ ] `argus/packs/nextjs/` directory with 4 files — covers FWRK-02

*(No new test infrastructure needed — existing `test_generate.py` and conftest are sufficient)*

---

## Open Questions

1. **Key phrase selection for fastapi pack**
   - What we know: Must be a unique string in `instructions.md`, stable across edits
   - Recommendation: `APIRouter` — framework-unique, appears in Router Organization section, not a Python keyword, not in any other existing pack
   - Claude's discretion to confirm or choose another from the authored content

2. **Key phrase selection for nextjs pack**
   - What we know: Same constraints as FastAPI
   - Recommendation: `use client` — App Router specific, will appear in both Server/Client and Hooks sections, unmistakable
   - Claude's discretion to confirm or choose another from the authored content

3. **Number of sections per pack**
   - What we know: CONTEXT.md gives Claude discretion on 3 or 4 sections; FWRK-01 lists 4 topic areas; FWRK-02 lists 4 topic areas
   - Recommendation: 4 sections per pack — aligns with requirement topic areas, matches python/kotlin density

---

## Sources

### Primary (HIGH confidence)
- Direct codebase inspection: `argus/packs/python/`, `argus/packs/kotlin/`, `argus/packs/typescript/` — pack structure verified
- Direct codebase inspection: `tests/integration/test_generate.py` — test pattern verified (KOTLIN_CONFIG, GO_CONFIG, etc.)
- Direct codebase inspection: `argus/loader.py` — auto-discovery confirmed, no code changes needed
- Direct codebase inspection: `argus/cli.py` — `packs show` renders `instructions` field only; `packs list` uses `available_packs()` which discovers directories
- Direct codebase inspection: `tests/test_packs.py` — confirmed `VALID_CATEGORIES` does not include `framework`; `REQUIRED_PACKS` does not include language or framework packs; no modification needed
- `.planning/phases/23-python-javascript-framework-packs/23-CONTEXT.md` — all content decisions locked

### Secondary (MEDIUM confidence)
- `.planning/STATE.md` accumulated decisions — key phrase selection pattern from phases 20–22
- `.planning/ROADMAP.md` Phase 23 success criteria — 3 acceptance criteria verified

---

## Metadata

**Confidence breakdown:**
- Implementation pattern: HIGH — identical to 5 prior packs, all infrastructure verified
- Pack content scope (FastAPI): HIGH — locked by CONTEXT.md decisions
- Pack content scope (Next.js): HIGH — locked by CONTEXT.md decisions
- Key phrase candidates: MEDIUM — Claude's discretion, recommendations provided but not locked
- test_packs.py non-modification: HIGH — verified REQUIRED_PACKS excludes all post-Phase-20 packs

**Research date:** 2026-06-25
**Valid until:** 2026-07-25 (pack authoring is stable infrastructure — no fast-moving dependencies)
