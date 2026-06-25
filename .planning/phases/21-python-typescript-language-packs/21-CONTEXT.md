# Phase 21: Python & TypeScript Language Packs - Context

**Gathered:** 2026-06-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Ship two new built-in packs — `python` and `typescript` — that inject language-specific idiom,
style, and type-discipline rules into agent instruction files. Both packs must appear in
`argus packs list`, be renderable via `argus packs show`, and inject correct content via
`argus generate`. Creating packs for other languages (go, java, kotlin) is out of scope — those
are Phase 22.

</domain>

<decisions>
## Implementation Decisions

### type-safety overlap (Python)
- Python pack is strictly non-type content: PEP 8 style, naming conventions, dataclasses,
  idiomatic Python (f-strings, comprehensions, context managers, pathlib, etc.)
- Zero overlap with the `type-safety` pack — annotation rules, mypy, `X | None` stay there
- No cross-reference or coupling between the two packs — they are additive, not dependent

### Content depth
- Moderate coverage: 15–20 rules per pack, organized into 3–4 thematic sections
- Comparable density to the security pack (6 OWASP categories + input validation)
- High-signal, directly actionable rules — not a comprehensive language reference

### Content format
- Mirror the security pack structure:
  - `instructions.md`: Category sections + Red Flags table at end
  - `checklist.md`: Checklist items matching categories
  - `examples.md`: Code examples organized by category
  - `pack.yml`: metadata with `category: language`
- Do NOT use the simpler process-pack format (no separate examples.md)

### Category & discovery
- `category: language` in `pack.yml` for both packs
- Sets the convention for Phase 22 (go, java, kotlin) and all future language packs
- Allows `argus packs list` to group under a "Language Packs" heading

### Claude's Discretion
- Exact selection of which 15–20 rules to include per pack (within the LANG-01/LANG-02 topic areas)
- Section naming and ordering within each pack
- Specific example code chosen for `examples.md`
- Whether `requires:` in pack.yml references any other packs

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` §Language Packs — LANG-01 (python) and LANG-02 (typescript) acceptance criteria and topic areas

### Pack format reference
- `argus/packs/tdd/pack.yml` — reference for pack.yml field structure (`category:`, `requires:`)
- `argus/packs/tdd/instructions.md` — reference for instructions.md format
- `argus/packs/security/` — reference for the security pack format to mirror (instructions.md, checklist.md, examples.md)

### Roadmap success criteria
- `.planning/ROADMAP.md` §Phase 21 — success criteria that define what "done" looks like for each pack

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `argus/loader.py` — pack loader; new packs just need to land in `argus/packs/` with correct structure, no loader changes needed
- `argus/packs/security/` — complete example of the target format to mirror (instructions.md, checklist.md, examples.md, pack.yml)
- Existing test suite for pack loading — parameterized tests for list, show, generate can be extended for the two new packs

### Established Patterns
- Each pack is a directory under `argus/packs/` with: `pack.yml`, `instructions.md`, `checklist.md`, `examples.md`
- `pack.yml` has `category:` field — language packs introduce `category: language`
- Security pack used OWASP category structure; language packs will use language-topic structure (same structural pattern, different domain)

### Integration Points
- `argus packs list` — must render the new `language` category cleanly
- `argus packs show python` / `argus packs show typescript` — display full pack content
- `argus generate` — injects pack content into generated platform instruction files
- Test suite in `tests/` — extend parameterized pack tests to cover python and typescript

</code_context>

<specifics>
## Specific Ideas

- No specific requirements — open to standard approaches for content selection within the LANG-01/LANG-02 topic areas

</specifics>

<deferred>
## Deferred Ideas

- None — discussion stayed within phase scope

</deferred>

---

*Phase: 21-python-typescript-language-packs*
*Context gathered: 2026-06-24*
