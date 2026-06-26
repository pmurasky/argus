# Phase 23: Python & JavaScript Framework Packs - Context

**Gathered:** 2026-06-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Ship two new built-in framework packs — `fastapi` and `nextjs` — that inject framework-specific
rules into agent instruction files. Both packs must appear in `argus packs list`, be renderable
via `argus packs show`, and inject correct content via `argus generate`. Spring and Mockito
framework packs are out of scope — those are Phase 24.

</domain>

<decisions>
## Implementation Decisions

### FastAPI — version target
- FastAPI 0.100+ (Pydantic v2 era)
- Rules use Pydantic v2 syntax: `model_config`, `model_validator`, `field_validator`
- No v1 compatibility shims or dual-version guidance

### FastAPI — async stance
- **Async-first**: always `async def` for route handlers
- Sync `def` only for CPU-bound work that runs in a thread pool (explicit exception)
- This is a hard rule, not a guideline

### FastAPI — Pydantic scope
- FastAPI-specific Pydantic usage only (not a general Pydantic tutorial):
  - Request/response models as the type boundary for endpoints
  - `Field()` for API-level validation (min/max, description, alias)
  - `model_config` for serialization settings (`populate_by_name`, `from_attributes`)
  - `model_validator` for cross-field validation logic
- General Pydantic patterns (settings management, discriminated unions, serialization) are
  out of scope — belong in a potential future standalone pydantic pack

### FastAPI — router organization
- `APIRouter` per feature/domain, assembled in a central `main.py` or `app.py`
- Each router: prefix + tags defined at router level, not endpoint level
- Standard FastAPI scaling pattern — agents must follow it, not inline all routes in main.py

### Next.js — version target
- Next.js 14+ App Router
- `app/` directory conventions: `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`

### Next.js — Pages Router
- **App Router only** — no Pages Router content in this pack
- No migration guidance, no legacy patterns

### Next.js — React hooks discipline
- Hooks are Client Components only — `'use client'` directive required when using hooks
- No hooks in Server Components
- `useCallback` / `useMemo` only when there is a measured performance need (not by default)

### Pack overlap boundary
- Framework packs are **additive** — they never duplicate content from the parent language pack
- FastAPI pack: assumes python pack is in scope; FastAPI-specific application of Python patterns
  (e.g., `async for` in streaming endpoints) lives here; generic Python idioms stay in python pack
- Next.js pack: assumes typescript pack is in scope; React/App Router-specific TypeScript patterns
  (component types, `use server`/`use client` directives, route param typing) live here; TS
  fundamentals (generics, strict mode, no-any) stay in typescript pack
- This is a content convention, not runtime enforcement — both packs use `requires: []`

### Category & discovery
- `category: framework` for both packs — parallel to `category: language`
- Sets the convention for Phase 24 (spring, mockito) and future framework packs
- `requires: []` — no runtime dependency declaration (matches all prior pack precedents)

### Pack metadata (follows Phase 21/22 precedent)
- `category: framework` for both packs
- `requires: []` — standalone
- `platforms: [all]`

### Claude's Discretion
- Exact selection of which 15–20 rules to include per pack within each section
- Section naming and ordering within each pack
- Specific example code chosen for `examples.md`
- Key test phrases (unique strings from `instructions.md`, stable across edits)
- Whether 3 or 4 thematic sections per pack

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` §Framework Packs — FWRK-01 (fastapi) and FWRK-02 (nextjs)
  acceptance criteria and topic areas

### Pack format reference (framework pack template)
- `argus/packs/python/` — direct structural template (pack.yml, instructions.md, checklist.md,
  examples.md); language pack format is the target format for framework packs too
- `argus/packs/typescript/` — second reference for pack density and format
- `argus/packs/security/` — reference for examples.md with secure/insecure side-by-side format

### Test pattern
- `tests/integration/test_generate.py` — isolation config constant pattern (FASTAPI_CONFIG,
  NEXTJS_CONFIG) + 3-assertion test (packs list / packs show / generate injects key phrase);
  must follow the same pattern as PYTHON_CONFIG / TYPESCRIPT_CONFIG / GO_CONFIG etc.

### Roadmap success criteria
- `.planning/ROADMAP.md` §Phase 23 — success criteria that define "done" for each pack

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `argus/packs/python/` — complete working language pack to copy and adapt; only content
  changes needed, structure is identical
- `argus/packs/typescript/` — second working pack to confirm structure is stable
- `argus/loader.py` — auto-discovers packs from `argus/packs/`; no changes needed for new packs
- `tests/integration/test_generate.py` — extend with FASTAPI_CONFIG and NEXTJS_CONFIG isolation
  constants following PYTHON_CONFIG, TYPESCRIPT_CONFIG, GO_CONFIG precedents

### Established Patterns
- Each pack: `pack.yml` + `instructions.md` + `checklist.md` + `examples.md`
- `pack.yml`: `category: framework`, `requires: []`, `platforms: [all]`
- Test key phrase: pick a unique string from `instructions.md` that is stable and unlikely
  to change (e.g., `APIRouter` for FastAPI, `use client` for Next.js — Claude decides)
- Test runner: `.venv/bin/pytest` (not bare `pytest`)

### Integration Points
- `argus packs list` — new packs appear automatically; `framework` category is new but the
  loader renders any category label, so no code change expected
- `argus packs show fastapi` / `show nextjs` — no code changes needed
- `argus generate` — injects pack content; no generator changes needed

</code_context>

<specifics>
## Specific Ideas

- No specific requirements — open to standard approaches for rule content within the FWRK-01/
  FWRK-02 topic areas

</specifics>

<deferred>
## Deferred Ideas

- Spring and Mockito framework packs — Phase 24
- Standalone Pydantic pack (settings management, discriminated unions) — future phase
- Pages Router compatibility pack — future phase (if demand emerges)

</deferred>

---

*Phase: 23-python-javascript-framework-packs*
*Context gathered: 2026-06-25*
