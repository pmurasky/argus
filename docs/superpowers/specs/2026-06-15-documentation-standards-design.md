# Documentation Standards Pack — Design Spec

**Date:** 2026-06-15
**Status:** Approved

## Summary

Add a `documentation-standards` pack to argus that enforces docstrings on public API surfaces and Click CLI commands, with a comment discipline rule.

## Decisions

| Question | Decision | Rationale |
|---|---|---|
| Scope | Public API docstrings + comment discipline | Two real failure modes: missing discoverability docs and noise comments |
| Docstring format | One-line summary only | Type annotations cover parameter types; small codebase; low friction |
| Public definition | Conventional Python public + Click commands | Click commands are user-facing but don't follow `_` convention |
| Comment rule | WHY only, never WHAT | Matches system prompt guidance; pairs with self-documenting code from naming/types |
| Pack format | Full pack (instructions + checklist + examples) | Consistent with existing packs; plugs into pre-commit gate |

## Pack Structure

```
argus/packs/documentation-standards/
  pack.yml
  instructions.md
  checklist.md
  examples.md
.claude/rules/documentation-standards.md
```

## `pack.yml`

```yaml
name: documentation-standards
description: Docstrings on public API and CLI commands; comments only for non-obvious WHY
category: quality
requires: []
platforms: [all]
```

## `instructions.md`

```markdown
# Documentation Standards

## Docstring Requirements
- All public classes must have a one-line docstring describing their purpose
- All public methods and functions must have a one-line docstring
- All Click CLI commands must have a one-line docstring (used by `--help`)
- `__init__` methods are exempt — document the class instead
- Private methods (prefixed `_`) are exempt

## Docstring Style
- One sentence, imperative mood: "Load packs from the search path." not "Loads packs..."
- No restating the function name: `def load():` → not "Load the load."
- Fits on one line — if you need more, the function probably does too much

## Comment Discipline
- Write comments only when the WHY is non-obvious: a hidden constraint, a workaround,
  a subtle invariant, or behaviour that would surprise a reader
- Never explain WHAT the code does — well-named identifiers already do that
- Never reference the current task, ticket, or caller in a comment

## Red Flags — Stop and Correct
- Public class, method, or CLI command with no docstring
- Docstring that restates the function name or explains what the code does
- Comment that says what the code does rather than why
- Multi-line docstring on a function under 10 lines
```

## `checklist.md`

```markdown
## Documentation Standards Checklist

- [ ] Every public class has a one-line docstring
- [ ] Every public method and function has a one-line docstring
- [ ] Every Click CLI command has a one-line docstring
- [ ] `__init__` and private (`_`) methods are not documented (exempt)
- [ ] Docstrings use imperative mood ("Return" not "Returns")
- [ ] No docstring restates the function name or describes what the code does
- [ ] Inline comments explain WHY only — not WHAT
- [ ] No multi-line docstrings on functions under 10 lines
```

## `examples.md`

```markdown
## Documentation Standards Examples

### Correct
```python
class PackLoader:
    """Load packs from built-in and custom search paths."""

def available_packs(self) -> list[str]:
    """Return sorted list of all discoverable pack names."""

@main.command()
def generate(...):
    """Generate platform-specific files from .argus.yml"""

# YAML safe_load returns Any — typed immediately below
data: dict[str, Any] = yaml.safe_load(path.read_text())
```

### Incorrect
```python
class PackLoader:
    """PackLoader class."""          # restates the name

def available_packs(self):
    """Gets the available packs."""  # wrong mood, explains what

# increment the counter
i += 1                               # explains what, not why
```

### Exempt (no docstring needed)
```python
def __init__(self, project_root: Path) -> None: ...
def _load_one(self, name: str) -> Pack: ...
```
```

## Test Impact

`tests/test_packs.py` `REQUIRED_PACKS` must include `"documentation-standards"`.

## Out of Scope

- Automated docstring linting (`pydocstyle`, `interrogate`) — tooling setup, not a standards pack concern
- README or changelog requirements — project-level, not enforceable per-commit
