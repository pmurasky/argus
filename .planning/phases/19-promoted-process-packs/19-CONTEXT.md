# Phase 19: Promoted Process Packs - Context

**Gathered:** 2026-06-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Make `type-safety`, `error-handling`, and `documentation-standards` fully functional as built-in
Argus packs — appearing in `argus packs list`, renderable via `argus packs show`, and injecting
correct content via `argus generate`. The three packs already have full directory structures and
real content; this phase fixes content quality issues and adds test coverage.

Creating new packs, adding new content categories, or broadening packs to cover other languages
are out of scope.

</domain>

<decisions>
## Implementation Decisions

### Language scope of type-safety
- Keep `type-safety` Python/mypy-focused — this is accurate and honest; other language type
  systems belong in language packs (Phase 21)
- Remove project-specific path references: `mypy argus/` → `mypy .` or `mypy <your-project>/`
  in `instructions.md` and `checklist.md`

### Content adaptation — remove Argus-specific examples
- `error-handling/examples.md` and `checklist.md` use Argus internals (`ArgusError`,
  `PackNotFoundError`, `UnknownPlatformError`, `adapter.generate(packs)`, `argus/__init__.py`)
  that are meaningless to users of other projects
- Replace with generic equivalents: `AppError` (or `ProjectError`), `ResourceNotFoundError`,
  `app/__init__.py` — same pattern, different names
- `error-handling/instructions.md` says "e.g. `argus/__init__.py`" — replace with
  "e.g. `app/__init__.py`" (generic)
- `documentation-standards/examples.md` uses `PackLoader`, `available_packs` — generalize
  to `DataLoader`, `list_items` or similar generic names

### Test coverage
- Add one integration test per pack covering three assertions each:
  1. Pack appears in `argus packs list` output
  2. `argus packs show <name>` renders the pack content
  3. `argus generate` with the pack in `.argus.yml` produces output containing a key phrase
     from that pack's instructions
- Follow the existing integration test pattern in `tests/integration/test_generate.py`
- Use `.venv/bin/pytest` as the test runner (not bare `pytest`)

### Pack completeness
- All three packs already have `instructions.md`, `checklist.md`, `examples.md`, `pack.yml`
  with real content — no new files are needed
- Work is limited to: fix content references + add tests

### Claude's Discretion
- Exact generic class/function names used in examples (as long as they are clearly generic,
  not Argus-specific)
- Whether to add a brief note in examples explaining they use generic project names

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Pack content to fix
- `argus/packs/type-safety/instructions.md` — contains `mypy argus/` path to replace
- `argus/packs/type-safety/checklist.md` — contains `mypy argus/` path to replace
- `argus/packs/error-handling/instructions.md` — contains `argus/__init__.py` reference
- `argus/packs/error-handling/checklist.md` — contains `ArgusError` as concrete example
- `argus/packs/error-handling/examples.md` — contains Argus-specific class names throughout
- `argus/packs/documentation-standards/examples.md` — contains `PackLoader`, `available_packs`

### Source of truth for content
- `.claude/rules/type-safety.md` — original source; pack should match intent but be generic
- `.claude/rules/error-handling.md` — original source
- `.claude/rules/documentation-standards.md` — original source

### Existing test pattern
- `tests/integration/test_generate.py` — existing integration test to follow as pattern
- `tests/integration/__init__.py` — test package init

### Pack format reference
- `argus/packs/tdd/pack.yml` — reference for pack.yml format (`category: workflow`, `requires:`)
- `argus/packs/tdd/instructions.md` — reference for instructions.md format

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tests/integration/test_generate.py` — existing integration tests; new pack tests should
  follow the same fixture/assertion pattern
- `argus/packs/tdd/` — gold-standard pack with all four files; use as reference for quality bar

### Established Patterns
- All packs use `category: quality` or `category: workflow` in pack.yml
- Test runner is `.venv/bin/pytest`, not bare `pytest`
- Integration tests live in `tests/integration/`

### Integration Points
- No new registration needed — packs are auto-discovered from `argus/packs/` directory
- `argus packs list` and `argus packs show` already work for any pack in the directory

</code_context>

<specifics>
## Specific Ideas

- The content fixes are surgical — change names/paths, not structure or intent
- Tests should be minimal and verify the success criteria directly (list, show, generate)
- No new pack.yml fields needed; current metadata is correct

</specifics>

<deferred>
## Deferred Ideas

- Broadening `type-safety` to cover TypeScript strict mode or Java generics — Phase 21
  (language packs) is the right home for this
- Adding a `requires:` dependency between packs (e.g., `error-handling` requires nothing,
  but could someday require `solid`) — premature; no second implementation yet

</deferred>

---

*Phase: 19-promoted-process-packs*
*Context gathered: 2026-06-23*
