# Phase 18: Gemini CLI Adapter - Research

**Researched:** 2026-06-23
**Domain:** Python adapter pattern + Gemini CLI GEMINI.md format
**Confidence:** HIGH

---

## Summary

Phase 18 adds a fifth platform adapter to argus: `gemini`. The implementation
pattern is locked-in by the four existing adapters (claude, opencode, copilot,
cursor). The only research unknowns were (a) the exact GEMINI.md filename and
location expected by Gemini CLI, and (b) whether the format needs any special
syntax beyond standard Markdown.

Both questions have definitive answers from the official google-gemini/gemini-cli
repository docs. GEMINI.md is a plain-Markdown file placed at the project root
(or a `.gemini/` subdirectory). No frontmatter, no special sections, no schema —
just headings and bullet points. Argus's `_agents_md` / copilot-style rendering
(inline sections per pack) maps cleanly to what Gemini CLI expects.

The adapter registration mechanism (Python entry points, `pyproject.toml`) means
the new adapter is wired in by adding one line to `[project.entry-points."argus.adapters"]`
and creating `argus/adapters/gemini.py`. Zero changes to existing code required.

**Primary recommendation:** Model the `GeminiAdapter` directly on `CopilotAdapter`
— it produces a single flat Markdown file containing all pack instructions. Place
the file at `GEMINI.md` in the project root. No subdirectory files needed.

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PLT-01 | User can generate `GEMINI.md` for Gemini CLI by adding `gemini` to `.argus.yml` platforms list | GeminiAdapter implements `BaseAdapter.generate()` returning a single `GeneratedFile(path=Path("GEMINI.md"), ...)` + `AGENTS.md`; entry-point registration makes `argus platforms list` include `gemini` automatically |
</phase_requirements>

---

## Standard Stack

### Core (no new dependencies)

| Component | Detail | Why |
|-----------|--------|-----|
| `argus.adapters.base.BaseAdapter` | Existing ABC | All adapters inherit this; `generate()` contract is already defined |
| `argus.adapters.base.GENERATED_HEADER` | Existing constant | All files must carry this header — enforced by existing tests |
| `argus.adapters.base.GeneratedFile` | Existing dataclass | Return type of `generate()` |
| `argus.adapters.base.Pack` | Existing dataclass | Input type of `generate()` |
| `pyproject.toml` entry-points | `[project.entry-points."argus.adapters"]` | How `AdapterRegistry.get("gemini")` resolves the class |

No new Python packages. No new dependencies.

**Installation:** Nothing to install. Adapter is a single new file + one pyproject.toml line.

---

## Architecture Patterns

### Recommended Project Structure

```
argus/adapters/
├── base.py             # unchanged
├── claude.py           # unchanged
├── copilot.py          # unchanged
├── cursor.py           # unchanged
├── opencode.py         # unchanged
└── gemini.py           # NEW — the only file to add

tests/adapters/
├── conftest.py         # unchanged
├── test_base.py        # unchanged
├── test_claude.py      # unchanged
├── test_copilot.py     # unchanged
├── test_cursor.py      # unchanged
├── test_opencode.py    # unchanged
└── test_gemini.py      # NEW — mirrors test_copilot.py structure

pyproject.toml          # add one line under [project.entry-points."argus.adapters"]
argus/cli.py            # add "gemini" to DEFAULT_PLATFORMS list
```

### Pattern 1: Single-File Adapter (CopilotAdapter reference)

**What:** `generate()` returns two files: `AGENTS.md` (from `_agents_md()`) and
the platform-specific file (from a private method that formats pack instructions).

**When to use:** When the target platform reads one flat Markdown file. Gemini CLI
reads `GEMINI.md` at the project root — same shape as `copilot-instructions.md`.

**Example — copy this shape exactly:**

```python
# Source: argus/adapters/copilot.py (existing production code)
class CopilotAdapter(BaseAdapter):
    platform_id = "copilot"
    display_name = "GitHub Copilot"

    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        return [self._agents_md(packs), self._copilot_instructions(packs)]

    def _copilot_instructions(self, packs: list[Pack]) -> GeneratedFile:
        sections = [GENERATED_HEADER + "# Engineering Standards\n"]
        for pack in packs:
            sections.append(f"## {pack.name.upper()}\n\n{pack.instructions}")
        return GeneratedFile(
            path=Path(".github/copilot-instructions.md"),
            content="\n\n".join(sections),
        )
```

The `GeminiAdapter` is structurally identical, with two changes:
- `platform_id = "gemini"`, `display_name = "Gemini CLI"`
- Output path: `Path("GEMINI.md")` instead of `Path(".github/copilot-instructions.md")`

### Pattern 2: Entry-Point Registration

**What:** `pyproject.toml` maps a string platform ID to the adapter class via
Python entry points. `AdapterRegistry.get("gemini")` loads the class at runtime
with zero code changes to the registry.

**Example:**

```toml
# Source: pyproject.toml [project.entry-points."argus.adapters"]
claude = "argus.adapters.claude:ClaudeAdapter"
opencode = "argus.adapters.opencode:OpenCodeAdapter"
copilot = "argus.adapters.copilot:CopilotAdapter"
cursor = "argus.adapters.cursor:CursorAdapter"
gemini = "argus.adapters.gemini:GeminiAdapter"   # ADD THIS LINE
```

After adding this line, `pip install -e .` (re-install in editable mode) is
required to register the new entry point. The test suite verifies via
`AdapterRegistry.get("gemini")` that the entry point resolves.

### Pattern 3: DEFAULT_PLATFORMS in cli.py

`argus init` scaffolds `.argus.yml` using `DEFAULT_PLATFORMS`. Add `"gemini"` to
this list so new projects include it by default.

```python
# Source: argus/cli.py
DEFAULT_PLATFORMS = ["claude", "opencode", "copilot", "cursor", "gemini"]  # add gemini
```

### Anti-Patterns to Avoid

- **Modifying BaseAdapter:** Do not change `base.py` — the contract is already
  correct. Adding methods to the base for a single adapter violates OCP.
- **Modifying existing adapters:** The phase success criteria state "no existing
  adapter or test is modified." Treat this as a hard constraint.
- **Using subdirectories for GEMINI.md:** Some community examples use `.gemini/GEMINI.md`
  but the Gemini CLI documentation is clear that `GEMINI.md` at the project root
  is the canonical location detected by default. Use `Path("GEMINI.md")`.
- **Including checklist/examples in GEMINI.md:** The copilot pattern (instructions
  only, no checklist) is correct. Gemini CLI reads GEMINI.md as a context/instruction
  file, not a checklist runner.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Adapter discovery | Custom registry dict | `importlib.metadata.entry_points` | Already implemented in `AdapterRegistry`; custom dict breaks plugin extensibility |
| Pack rendering | Custom template engine | `"\n\n".join(sections)` pattern | Four existing adapters prove this is sufficient; no template engine needed |
| File writing | Custom writer | `Generator.run()` handles writing | The generator iterates `adapter.generate()` results and writes each `GeneratedFile` |

---

## Gemini CLI GEMINI.md Format Specification

**Source:** [Official docs](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html) — HIGH confidence

### Key Facts

| Property | Value |
|----------|-------|
| Filename | `GEMINI.md` (case-sensitive) |
| Default location | Project root (same level as `.git/`) |
| Alternative location | `.gemini/GEMINI.md` (hidden, also works) |
| Format | Plain Markdown — no frontmatter, no schema |
| Special syntax | `@./path/to/file.md` for imports (NOT needed by argus) |
| Sections | Free-form — no required sections; headings organise content |
| Loading | Hierarchical: `~/.gemini/GEMINI.md` → workspace GEMINI.md → JIT from subdirs |
| CLI command | `/memory show` — displays concatenated loaded context |

### What Gemini CLI Does With GEMINI.md

The entire file content is concatenated with other loaded GEMINI.md files and
prepended to every prompt. There is no section parsing — all content is treated
as flat instruction text. This means argus's standard section-per-pack format
(H2 headings, bullet points) is a perfect fit.

### Example GEMINI.md (from official docs)

```markdown
# Project: My TypeScript Library

## General Instructions

- When you generate new TypeScript code, follow the existing coding style.
- Ensure all new functions and classes have JSDoc comments.

## Coding Style

- Use 2 spaces for indentation.
- Always use strict equality (`===` and `!==`).
```

Argus would generate the same structure with pack names as section headings.

### Real-World Example (from google-gemini/gemini-cli's own GEMINI.md)

The gemini-cli repo's own GEMINI.md uses:
- `#` for project title
- `##` for major topic sections (Project Overview, Building and Running, Testing Conventions)
- Nested bullet lists for rules within each section
- No frontmatter, no schema, no imports

This confirms argus's `f"## {pack.name.upper()}\n\n{pack.instructions}"` pattern
produces idiomatic GEMINI.md content.

---

## Common Pitfalls

### Pitfall 1: Forgetting to reinstall after adding entry point

**What goes wrong:** `argus platforms list` does not show `gemini` even after
creating `argus/adapters/gemini.py`.

**Why it happens:** Python entry points are registered at install time, not
at import time. The entry point line in `pyproject.toml` is not "live" until
`pip install -e .` (or equivalent) is re-run.

**How to avoid:** After adding the entry-point line, run `pip install -e .`
before running tests.

**Warning signs:** `UnknownPlatformError: Unknown platform: "gemini"` during tests.

### Pitfall 2: Using `.gemini/GEMINI.md` instead of `GEMINI.md`

**What goes wrong:** The file is generated at `.gemini/GEMINI.md`, which is a
valid location Gemini CLI reads — but it is the hidden/alternative location.
The user-visible, conventional location is the project root `GEMINI.md`.

**How to avoid:** Use `Path("GEMINI.md")` as the output path. This matches
the community convention and the official quick-start examples.

### Pitfall 3: Missing `platform_id` or `display_name` class attributes

**What goes wrong:** `AdapterRegistry.get("gemini")` raises `UnknownPlatformError`
even with the entry point registered.

**Why it happens:** `AdapterRegistry` looks up entry points by `ep.name` (the
left side of the entry-point declaration). If the class attributes are wrong,
nothing breaks at registration time — but `platforms list` would show an
incorrect ID.

**How to avoid:** Set `platform_id = "gemini"` and `display_name = "Gemini CLI"`.

### Pitfall 4: Omitting AGENTS.md from generate() return

**What goes wrong:** Tests for AGENTS.md generation fail; `argus generate` does
not produce `AGENTS.md` for the gemini platform.

**Why it happens:** `_agents_md()` is inherited from `BaseAdapter` and must be
explicitly called in `generate()`. It is not automatic.

**How to avoid:** Return `[self._agents_md(packs), self._gemini_md(packs)]` —
same pattern as `CopilotAdapter`.

---

## Code Examples

### GeminiAdapter (complete implementation)

```python
# argus/adapters/gemini.py
from pathlib import Path

from argus.adapters.base import GENERATED_HEADER, BaseAdapter, GeneratedFile, Pack


class GeminiAdapter(BaseAdapter):
    """Adapter for Gemini CLI — generates GEMINI.md at the project root."""

    platform_id = "gemini"
    display_name = "Gemini CLI"

    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        """Translate packs into AGENTS.md and GEMINI.md."""
        return [self._agents_md(packs), self._gemini_md(packs)]

    def _gemini_md(self, packs: list[Pack]) -> GeneratedFile:
        """Build GEMINI.md containing all pack instructions as H2 sections."""
        sections = [GENERATED_HEADER + "# Engineering Standards\n"]
        for pack in packs:
            sections.append(f"## {pack.name.upper()}\n\n{pack.instructions}")
        return GeneratedFile(
            path=Path("GEMINI.md"),
            content="\n\n".join(sections),
        )
```

### pyproject.toml addition

```toml
[project.entry-points."argus.adapters"]
claude = "argus.adapters.claude:ClaudeAdapter"
opencode = "argus.adapters.opencode:OpenCodeAdapter"
copilot = "argus.adapters.copilot:CopilotAdapter"
cursor = "argus.adapters.cursor:CursorAdapter"
gemini = "argus.adapters.gemini:GeminiAdapter"
```

### test_gemini.py (complete test file)

```python
# tests/adapters/test_gemini.py
from pathlib import Path
from argus.adapters.gemini import GeminiAdapter
from argus.adapters.base import GENERATED_HEADER
from tests.adapters.conftest import stub_pack


def test_gemini_generates_agents_md():
    files = GeminiAdapter().generate([stub_pack("tdd")])
    assert Path("AGENTS.md") in [f.path for f in files]


def test_gemini_generates_gemini_md():
    files = GeminiAdapter().generate([stub_pack("tdd")])
    assert Path("GEMINI.md") in [f.path for f in files]


def test_gemini_generates_exactly_two_files():
    files = GeminiAdapter().generate([stub_pack("tdd"), stub_pack("solid")])
    assert len(files) == 2


def test_gemini_md_contains_pack_instructions():
    files = GeminiAdapter().generate([stub_pack("tdd")])
    gemini_md = next(f for f in files if f.path == Path("GEMINI.md"))
    assert "TDD instructions" in gemini_md.content


def test_gemini_md_does_not_contain_checklist():
    files = GeminiAdapter().generate([stub_pack("tdd", checklist="## Checklist")])
    gemini_md = next(f for f in files if f.path == Path("GEMINI.md"))
    assert "## Checklist" not in gemini_md.content


def test_all_files_have_generated_header():
    files = GeminiAdapter().generate([stub_pack("tdd")])
    for f in files:
        assert GENERATED_HEADER in f.content, f"{f.path} missing generated header"
```

---

## Adapter Registration Architecture

The full registration flow (no code changes required to existing modules):

```
pyproject.toml
  └─ [project.entry-points."argus.adapters"]
       gemini = "argus.adapters.gemini:GeminiAdapter"
                          │
                          ▼ (pip install -e .)
argus.generator.AdapterRegistry.get("gemini")
  └─ importlib.metadata.entry_points(group="argus.adapters")
       │  filters ep.name == "gemini"
       └─ ep.load()()  →  GeminiAdapter()
                               │
                               ▼
                     generator.run() calls .generate(packs)
                               │
                               ▼
                     [GeneratedFile("AGENTS.md", ...), GeneratedFile("GEMINI.md", ...)]
```

`argus platforms list` uses the same `entry_points(group="argus.adapters")` call,
so the new platform appears automatically once the entry point is registered.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (via `.venv/bin/pytest`) |
| Config file | `pyproject.toml` `[tool.pytest.ini_options]` |
| Quick run command | `.venv/bin/pytest tests/adapters/test_gemini.py -x` |
| Full suite command | `.venv/bin/pytest` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| PLT-01 | `GeminiAdapter.generate()` returns `GEMINI.md` at project root | unit | `.venv/bin/pytest tests/adapters/test_gemini.py -x` | ❌ Wave 0 |
| PLT-01 | `GEMINI.md` content contains pack instructions (not checklist) | unit | `.venv/bin/pytest tests/adapters/test_gemini.py::test_gemini_md_contains_pack_instructions -x` | ❌ Wave 0 |
| PLT-01 | `AGENTS.md` is also generated | unit | `.venv/bin/pytest tests/adapters/test_gemini.py::test_gemini_generates_agents_md -x` | ❌ Wave 0 |
| PLT-01 | `argus platforms list` includes `gemini` | integration | `.venv/bin/pytest tests/integration/ -x` | check existing |
| PLT-01 | All generated files have `GENERATED_HEADER` | unit | `.venv/bin/pytest tests/adapters/test_gemini.py::test_all_files_have_generated_header -x` | ❌ Wave 0 |
| PLT-01 | mypy clean on new adapter file | type-check | `.venv/bin/python -m mypy argus/adapters/gemini.py` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** `.venv/bin/pytest tests/adapters/test_gemini.py -x`
- **Per wave merge:** `.venv/bin/pytest`
- **Phase gate:** Full suite green + mypy clean before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/adapters/test_gemini.py` — covers PLT-01 (6 unit tests shown above)
- [ ] `argus/adapters/gemini.py` — the production file itself
- [ ] `pyproject.toml` entry-point line — required before entry-point tests pass
- [ ] Re-run `pip install -e .` after adding entry point

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Register adapters in a hardcoded dict | Python entry points (`importlib.metadata`) | v1.0 (Phase 17) | New adapters are a single file + one pyproject.toml line; no registry code changes |
| Single instruction file per platform | Per-platform output shape | v1.0 | Some adapters (claude) produce many files; copilot/gemini produce one |

**No deprecated patterns** relevant to this phase.

---

## Open Questions

1. **Should `argus init` include `gemini` in `DEFAULT_PLATFORMS`?**
   - What we know: `DEFAULT_PLATFORMS` in `cli.py` currently lists all 4 adapters.
   - What's unclear: Adding gemini to default means all new `argus init` users get GEMINI.md scaffolded even if they don't use Gemini CLI.
   - Recommendation: Add it. The existing pattern is "include all known platforms" in the default scaffold. Consistency beats cleverness. User can remove it from `.argus.yml` if unwanted.

2. **Integration test coverage for `argus platforms list` output?**
   - What we know: `tests/integration/test_generate.py` exists but was not fully read.
   - What's unclear: Whether the integration tests verify the `platforms list` command output.
   - Recommendation: Check `tests/integration/test_generate.py` during implementation. If `platforms list` isn't integration-tested, add one test case.

---

## GitHub Examples

Real-world GEMINI.md files found:

- [google-gemini/gemini-cli GEMINI.md](https://github.com/google-gemini/gemini-cli/blob/main/GEMINI.md) — The project's own GEMINI.md; uses `#` title, `##` sections (Project Overview, Building and Running, Testing Conventions), nested bullet lists. No frontmatter.
- [amitkmaraj/gemini-cli-gemini-markdown-files](https://github.com/amitkmaraj/gemini-cli-gemini-markdown-files) — Community collection of GEMINI.md templates. Senior Engineering example: uses `##` sections with emoji headers for Persona, Workflow, Coding Standards, Git, Debugging.
- [Official example in docs](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html) — Minimal TypeScript project example: `# Project: My TypeScript Library`, then `## General Instructions`, `## Coding Style`.

**Pattern confirmed:** All real GEMINI.md files are flat Markdown with H1 title + H2 sections. No frontmatter, no schema, no imports required. Argus's rendering pattern is idiomatic.

---

## Sources

### Primary (HIGH confidence)
- [google-gemini/gemini-cli docs/cli/gemini-md.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md) — official spec: filename, location, hierarchy, imports, customization
- [google-gemini/gemini-cli GEMINI.md](https://github.com/google-gemini/gemini-cli/blob/main/GEMINI.md) — reference implementation from the project itself
- `argus/adapters/base.py`, `argus/adapters/copilot.py`, `argus/adapters/claude.py` — existing adapter contract and reference implementations (read directly)
- `pyproject.toml` — entry-point registration pattern (read directly)

### Secondary (MEDIUM confidence)
- [google-gemini.github.io official docs](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html) — mirrors GitHub docs content; confirms hierarchy loading behavior
- [geminicli.com/docs/cli/gemini-md](https://geminicli.com/docs/cli/gemini-md/) — third-party docs site, consistent with official

### Tertiary (LOW confidence)
- [amitkmaraj/gemini-cli-gemini-markdown-files](https://github.com/amitkmaraj/gemini-cli-gemini-markdown-files) — community examples, not official; useful for confirming real-world conventions
- [Medium: Practical Gemini CLI Instruction Following](https://medium.com/google-cloud/practical-gemini-cli-instruction-following-gemini-md-hierarchy-part-1-3ba241ac5496) — tutorial, consistent with official docs

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all existing code read directly; no new libraries
- Architecture: HIGH — CopilotAdapter is a working, tested 1:1 analogue
- GEMINI.md format: HIGH — verified from official google-gemini/gemini-cli repo
- Pitfalls: HIGH — entry-point registration pitfall is a known Python pattern; others verified from existing codebase

**Research date:** 2026-06-23
**Valid until:** 2026-09-23 (stable — GEMINI.md format is unlikely to change; entry-point pattern is stable Python)
