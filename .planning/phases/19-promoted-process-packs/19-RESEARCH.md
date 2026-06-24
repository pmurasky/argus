# Phase 19: Promoted Process Packs - Research

**Researched:** 2026-06-23
**Domain:** Argus pack content quality + integration test coverage
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- `type-safety` stays Python/mypy-focused; replace `mypy argus/` with `mypy .` or `mypy <your-project>/`
- Remove Argus-specific examples from `error-handling/examples.md` and `checklist.md`: replace
  `ArgusError` → `AppError` (or `ProjectError`), `PackNotFoundError` → `ResourceNotFoundError`,
  `argus/__init__.py` → `app/__init__.py`
- `error-handling/instructions.md`: replace `argus/__init__.py` with `app/__init__.py`
- `documentation-standards/examples.md`: replace `PackLoader`, `available_packs` with generic
  equivalents (`DataLoader`, `list_items` or similar)
- Add one integration test per pack, three assertions each: (1) pack appears in `argus packs list`,
  (2) `argus packs show <name>` renders pack content, (3) `argus generate` with pack produces
  output containing a key phrase from the pack's instructions
- Follow existing integration test pattern in `tests/integration/test_generate.py`
- Test runner: `.venv/bin/pytest`, not bare `pytest`
- No new pack files needed — all four files already exist per pack

### Claude's Discretion
- Exact generic class/function names used in examples (as long as clearly generic, not Argus-specific)
- Whether to add a brief note in examples explaining they use generic project names

### Deferred Ideas (OUT OF SCOPE)
- Broadening `type-safety` to TypeScript strict mode or Java generics (Phase 21)
- Adding `requires:` dependency between packs (premature, no second implementation)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PACK-02 | User can apply `type-safety` pack to enforce full type annotation discipline | Fix `mypy argus/` → `mypy .` in instructions.md and checklist.md; add integration test |
| PACK-03 | User can apply `error-handling` pack to enforce exception hierarchy and catch-only-at-boundaries rules | Generalize Argus-specific names in examples.md, checklist.md, instructions.md; add integration test |
| PACK-04 | User can apply `documentation-standards` pack to enforce docstring and comment discipline | Generalize `PackLoader`/`available_packs` in examples.md; add integration test |
</phase_requirements>

## Summary

Phase 19 is a content-fix and test-coverage phase. The three packs (`type-safety`, `error-handling`,
`documentation-standards`) already exist as fully-structured directories under `argus/packs/` with
all required files (`pack.yml`, `instructions.md`, `checklist.md`, `examples.md`). No structural
changes, new files, or code changes are needed.

The two categories of work are: (1) surgical text replacements — removing Argus project-specific
identifiers that would confuse consumers of other projects; (2) integration tests that verify
the packs are discoverable and functional through the CLI surface.

The existing `tests/integration/test_generate.py` is the only integration test file. It uses
`click.testing.CliRunner`, `tmp_path` fixtures, and inline YAML config strings. New tests follow
exactly this pattern. The existing `tests/test_packs.py` already parametrizes over `type-safety`,
`error-handling`, and `documentation-standards` for structural validation (file existence, pack.yml
schema) — it does NOT test CLI discoverability or generate output content.

**Primary recommendation:** Fix the six content locations with targeted string replacements, then
add three integration test functions (one per pack) to `tests/integration/test_generate.py`.

## Standard Stack

### Core (already installed — no new dependencies)
| Library | Version | Purpose | Notes |
|---------|---------|---------|-------|
| click.testing.CliRunner | (installed) | Invoke CLI commands in tests | Already used in all test files |
| pytest | (installed) | Test framework | Run via `.venv/bin/pytest` |

No new libraries are required. This phase involves no new production code.

## Architecture Patterns

### Recommended Project Structure
No structural changes. All work is within:
```
argus/packs/
├── type-safety/
│   ├── instructions.md   # fix: mypy argus/ → mypy .
│   └── checklist.md      # fix: mypy argus/ → mypy .
├── error-handling/
│   ├── instructions.md   # fix: argus/__init__.py → app/__init__.py
│   ├── checklist.md      # fix: ArgusError → AppError
│   └── examples.md       # fix: all Argus-specific names
└── documentation-standards/
    └── examples.md       # fix: PackLoader → DataLoader, available_packs → list_items

tests/integration/
└── test_generate.py      # add: 3 new test functions
```

### Pattern 1: Integration Test Shape (existing pattern)
**What:** Each integration test creates a `tmp_path`, writes an inline `.argus.yml`, invokes
CLI via `CliRunner`, and asserts on exit code and output content.

**When to use:** Whenever verifying end-to-end pack behavior through the CLI.

**Example (from existing `tests/integration/test_generate.py`):**
```python
# Source: tests/integration/test_generate.py

TYPE_SAFETY_CONFIG = """\
packs:
  - type-safety
platforms:
  - claude
"""

def test_type_safety_pack_appears_in_packs_list():
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "type-safety" in result.output


def test_type_safety_pack_show_renders_content():
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "show", "type-safety"])
    assert result.exit_code == 0
    assert "mypy" in result.output


def test_type_safety_pack_generate_injects_content(tmp_path):
    (tmp_path / ".argus.yml").write_text(TYPE_SAFETY_CONFIG)
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "mypy" in (tmp_path / "CLAUDE.md").read_text()
```

**Key phrase selection per pack:**
- `type-safety`: `"mypy"` — appears in instructions.md and checklist.md, survives the path fix
- `error-handling`: `"system boundaries"` — appears in instructions.md, not Argus-specific
- `documentation-standards`: `"imperative mood"` — appears in instructions.md, clearly generic

### Pattern 2: Config String Per Pack
**What:** Each pack gets its own CONFIG constant (not reusing FULL_CONFIG), isolating tests.
This follows the precedent set by GEMINI_CONFIG in test_generate.py.

**Why:** Prevents cross-contamination with other packs' content in assertions.

### Anti-Patterns to Avoid
- **Reusing FULL_CONFIG:** The existing FULL_CONFIG includes `tdd` and `atomic-commit`. Adding
  new packs to it would make the assertion "key phrase in CLAUDE.md" ambiguous about which pack
  contributed it.
- **Asserting on file path for pack content:** The `packs show` test invokes the CLI directly
  — do not read `argus/packs/type-safety/instructions.md` from disk. The CLI must work end-to-end.
- **Changing pack.yml:** The `pack.yml` files are already correct (`category: quality`, no
  `requires:`, `platforms: [all]`). Do not modify them.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CLI testing | Custom subprocess calls | `CliRunner` from `click.testing` | Already established pattern; handles exit codes, stdin/stdout capture |
| Pack discovery | Custom file scanner in tests | `argus packs list` via CLI | The test verifies the CLI works, not the underlying filesystem |

## Common Pitfalls

### Pitfall 1: `packs list` takes no `--project-root`
**What goes wrong:** `packs_list()` in `cli.py` uses `PackLoader(project_root=Path("."))` with
a hardcoded `"."`. It does NOT accept `--project-root`. Tests calling `packs list` must not pass
`--project-root`.

**Why it happens:** The list and show commands don't have a project root option — they always
show built-in packs.

**How to avoid:** For `packs list` and `packs show` tests, invoke `runner.invoke(main, ["packs",
"list"])` with no extra args. Only `generate` tests need `--project-root str(tmp_path)`.

### Pitfall 2: Key phrase must survive content edits
**What goes wrong:** If you pick a key phrase from `error-handling/examples.md` that gets changed
during the Argus-name generalization, the test will pass during RED (failing because pack isn't
fully set up) but then fail after the content fix.

**Why it happens:** Content fixes and test writing happen in sequence; a phrase in `examples.md`
can be removed.

**How to avoid:** Choose key phrases from `instructions.md` only — `instructions.md` content
is not being changed in this phase (except for `error-handling/instructions.md` which loses
`argus/__init__.py`). Use phrases that are not the strings being replaced.

**Safe key phrases:**
- `type-safety` → `"mypy"` (the tool name, not the path `mypy argus/`)
- `error-handling` → `"system boundaries"` (from Catching Rules, unchanged)
- `documentation-standards` → `"imperative mood"` (from Docstring Style, unchanged)

### Pitfall 3: Exact strings to replace in each file
**What goes wrong:** Missing an instance of an Argus-specific name in checklist.md while fixing
examples.md leaves the pack still project-specific.

**How to avoid:** Fix all instances per the exact inventory below.

**Complete replacement inventory:**

`type-safety/instructions.md` line 5:
- Change: `Run \`mypy argus/\` before committing`
- To: `Run \`mypy .\` (or \`mypy <your-project>/\`) before committing`

`type-safety/checklist.md` line 6:
- Change: `\`mypy argus/\` exits 0`
- To: `\`mypy .\` exits 0`

`error-handling/instructions.md` line 6:
- Change: `e.g. \`argus/__init__.py\``
- To: `e.g. \`app/__init__.py\``

`error-handling/checklist.md` line 3:
- Change: `(e.g. \`ArgusError\`)`
- To: `(e.g. \`AppError\`)`

`error-handling/examples.md` — full generalization:
- `ArgusError` → `AppError`
- `PackNotFoundError` → `ResourceNotFoundError`
- `UnknownPlatformError` → `ConfigError` (or another generic name)
- `adapter.generate(packs)` → `service.process(items)` (or similar generic call)
- `ArgusConfigError` → `AppConfigError`

`documentation-standards/examples.md`:
- `PackLoader` → `DataLoader`
- `available_packs` → `list_items`

### Pitfall 4: TDD discipline — tests must be RED before fixes
**What goes wrong:** Writing the content fix first, then the test. The test would start GREEN,
violating the TDD requirement.

**How to avoid:** For each pack, write the integration test first (it will fail or give false
positive if pack content is wrong), then make the fix. Since `packs list` and `packs show`
already work (packs are auto-discovered), the tests for those two assertions will be GREEN
immediately. The `generate` assertion is the discriminating one.

**Practical sequence per pack:**
1. Write all three assertions for the pack as a single test or three tests
2. Confirm the `generate` assertion is GREEN (the pack content already injects into CLAUDE.md)
3. The content-fix commits are not TDD cycles — they are refactor commits (behavior from
   the user's perspective is: "examples now use generic names")

**Note:** Since packs already work end-to-end (they're auto-discovered), all three assertions
will likely be GREEN from the start. The integration tests are verification, not behavior
specification. This is acceptable — CONTEXT.md states "Work is limited to: fix content
references + add tests."

## Code Examples

### Integration test structure for each pack

```python
# Source: based on tests/integration/test_generate.py pattern

from click.testing import CliRunner
from argus.cli import main

TYPE_SAFETY_CONFIG = """\
packs:
  - type-safety
platforms:
  - claude
"""

ERROR_HANDLING_CONFIG = """\
packs:
  - error-handling
platforms:
  - claude
"""

DOCUMENTATION_STANDARDS_CONFIG = """\
packs:
  - documentation-standards
platforms:
  - claude
"""


def test_type_safety_pack_appears_in_packs_list():
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "type-safety" in result.output


def test_type_safety_pack_show_renders_content():
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "show", "type-safety"])
    assert result.exit_code == 0
    assert "mypy" in result.output


def test_type_safety_pack_generate_injects_content(tmp_path):
    (tmp_path / ".argus.yml").write_text(TYPE_SAFETY_CONFIG)
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "mypy" in (tmp_path / "CLAUDE.md").read_text()


# ... repeat pattern for error-handling (key: "system boundaries")
# ... repeat pattern for documentation-standards (key: "imperative mood")
```

### Generalized error-handling/examples.md (replacement content)

```python
# Correct
class AppError(Exception): ...
class ResourceNotFoundError(AppError): ...  # inherits from base

try:
    service.process(items)
except (ResourceNotFoundError, ConfigError) as e:
    click.echo(f"✗ {e}", err=True)
    sys.exit(1)

raise ResourceNotFoundError(f'Unknown resource: "{name}"') from None

# Incorrect
class ResourceNotFoundError(Exception): ...   # missing base class
except Exception as e: pass                   # swallowed, too broad
except:                                       # bare except
try: ... except SomeError: pass               # silent swallow

# Re-raise with context
except yaml.YAMLError as e:
    raise AppConfigError("Invalid config.yml") from e
```

### Generalized documentation-standards/examples.md (replacement content)

```python
# Correct
class DataLoader:
    """Load records from built-in and custom search paths."""

def list_items(self) -> list[str]:
    """Return sorted list of all discoverable item names."""

@main.command()
def generate(...):
    """Generate platform-specific files from config.yml"""

# YAML safe_load returns Any — typed immediately below
data: dict[str, Any] = yaml.safe_load(path.read_text())

# Incorrect
class DataLoader:
    """DataLoader class."""          # restates the name

def list_items(self):
    """Gets the available items."""  # wrong mood, explains what

# increment the counter
i += 1                               # explains what, not why

# Exempt (no docstring needed)
def __init__(self, project_root: Path) -> None: ...
def _load_one(self, name: str) -> Record: ...
```

## State of the Art

| Old State | Current State | Impact |
|-----------|--------------|--------|
| Packs contain Argus project names | Packs use generic project names | Packs usable in any project context |
| No integration tests for promoted packs | 3 tests × 3 assertions = 9 assertions | PACK-02/03/04 verified end-to-end |

## Open Questions

1. **Should the `generate` assertion check `CLAUDE.md` content or a rules file?**
   - What we know: `test_generated_files_have_header` checks `CLAUDE.md`; `test_generate_produces_claude_files` checks `.claude/rules/tdd.md`
   - What's unclear: Claude adapter may put pack content in `.claude/rules/<pack-name>.md`, not in `CLAUDE.md` directly
   - Recommendation: Assert on `CLAUDE.md` first (it points to rules dir). If the key phrase doesn't appear there, check `(tmp_path / ".claude/rules/type-safety.md").read_text()`. Review the existing test `test_generated_files_have_header` to confirm where content lands — it only checks for "Generated by argus" in CLAUDE.md, suggesting pack instruction content goes to the rules files, not CLAUDE.md.
   - **Safe approach:** Assert on the rules file: `(tmp_path / ".claude/rules/type-safety.md").read_text()` contains `"mypy"`.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing) |
| Config file | `pyproject.toml` or implicit |
| Quick run command | `.venv/bin/pytest tests/integration/test_generate.py -x` |
| Full suite command | `.venv/bin/pytest` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PACK-02 | `type-safety` pack appears in `packs list` | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_type_safety_pack_appears_in_packs_list -x` | ❌ Wave 0 |
| PACK-02 | `packs show type-safety` renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_type_safety_pack_show_renders_content -x` | ❌ Wave 0 |
| PACK-02 | `generate` with type-safety pack injects content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_type_safety_pack_generate_injects_content -x` | ❌ Wave 0 |
| PACK-03 | `error-handling` pack appears in `packs list` | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_error_handling_pack_appears_in_packs_list -x` | ❌ Wave 0 |
| PACK-03 | `packs show error-handling` renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_error_handling_pack_show_renders_content -x` | ❌ Wave 0 |
| PACK-03 | `generate` with error-handling pack injects content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_error_handling_pack_generate_injects_content -x` | ❌ Wave 0 |
| PACK-04 | `documentation-standards` pack appears in `packs list` | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_documentation_standards_pack_appears_in_packs_list -x` | ❌ Wave 0 |
| PACK-04 | `packs show documentation-standards` renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_documentation_standards_pack_show_renders_content -x` | ❌ Wave 0 |
| PACK-04 | `generate` with documentation-standards pack injects content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_documentation_standards_pack_generate_injects_content -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `.venv/bin/pytest tests/integration/test_generate.py -x`
- **Per wave merge:** `.venv/bin/pytest`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] 9 new test functions in `tests/integration/test_generate.py` — covers PACK-02, PACK-03, PACK-04
- [ ] No new framework install needed — pytest already present

## Sources

### Primary (HIGH confidence)
- Direct code read: `tests/integration/test_generate.py` — existing integration test pattern
- Direct code read: `argus/cli.py` — `packs list` has no `--project-root`; `packs show` takes name arg
- Direct code read: `argus/loader.py` — auto-discovery from `argus/packs/` directory
- Direct code read: all six pack content files — exact strings that need changing

### Secondary (MEDIUM confidence)
- Direct code read: `tests/test_packs.py` — confirms structural tests already pass for three packs; integration tests are the gap
- Direct code read: `tests/test_cli.py` — confirms `packs list` / `packs show` test pattern used in unit tests

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new dependencies; all libraries already in project
- Architecture: HIGH — directly read existing test files and pack structure
- Pitfalls: HIGH — drawn from direct code inspection of CLI and test patterns
- Content replacements: HIGH — read actual file content, identified exact strings

**Research date:** 2026-06-23
**Valid until:** Until pack content or CLI interface changes (stable)
