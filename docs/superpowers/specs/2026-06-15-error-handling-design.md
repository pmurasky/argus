# Error Handling Pack — Design Spec

**Date:** 2026-06-15
**Status:** Approved

## Summary

Add an `error-handling` pack to argus that enforces exception design conventions and raise/catch discipline.

## Decisions

| Question | Decision | Rationale |
|---|---|---|
| Scope | Exception design + raise/return discipline | Covers naming, hierarchy, and catch rules without over-specifying logging |
| Base exception | Required — all custom exceptions must inherit from project base | Makes CLI catch-all cleaner; mechanically enforceable |
| Exception location | Close to where raised (same module) | Matches Python stdlib conventions; avoids god-module `exceptions.py` |
| Catch rules | Boundary-only + catch only what you can handle | Matches existing argus cli.py pattern; prevents silent swallowing |
| Pack format | Full pack (instructions + checklist + examples) | Consistent with existing packs; plugs into pre-commit gate |

## Pack Structure

```
argus/packs/error-handling/
  pack.yml
  instructions.md
  checklist.md
  examples.md
.claude/rules/error-handling.md
```

## `pack.yml`

```yaml
name: error-handling
description: Exception design and raise/catch discipline — base class, boundaries, no swallowing
category: quality
requires: []
platforms: [all]
```

## `instructions.md`

```markdown
# Error Handling

## Exception Design
- All custom exceptions inherit from a project-level base exception (e.g. `ArgusError`)
- Exception names end in `Error`
- Define exceptions in the module that raises them — not in a central `exceptions.py`
- Exceptions carry a human-readable message sufficient to understand the failure

## Raise vs Return
- Raise for conditions the caller cannot reasonably anticipate or recover from inline
- Return for expected outcomes the caller must handle (results, None, empty collections)
- Never use exceptions for control flow

## Catching Rules
- Catch only at system boundaries (CLI entry points, public API surfaces)
- Catch only the specific exception types you can handle — never bare `except:` or `except Exception:`
- Never swallow exceptions silently (`except ...: pass` is always wrong)
- When catching to re-raise with context, use `raise NewError(...) from original`

## Red Flags — Stop and Correct
- Custom exception inherits directly from `Exception` without a project base class
- `except:` or `except Exception:` anywhere except a top-level CLI handler
- `except ...: pass` (silent swallow)
- try/except inside a function that is not a system boundary
- Exception name does not end in `Error`
```

## `checklist.md`

```markdown
## Error Handling Checklist

- [ ] All custom exceptions inherit from the project base exception (e.g. `ArgusError`)
- [ ] Exception names end in `Error`
- [ ] Exceptions defined in the module that raises them
- [ ] No bare `except:` or `except Exception:` except at top-level CLI handlers
- [ ] No silent swallows: `except ...: pass` does not exist
- [ ] Exceptions only caught at system boundaries
- [ ] `raise X from original` used when re-raising with context
```

## `examples.md`

```markdown
## Error Handling Examples

### Correct
```python
class ArgusError(Exception): ...
class PackNotFoundError(ArgusError): ...  # inherits from base

try:
    adapter.generate(packs)
except (PackNotFoundError, UnknownPlatformError) as e:
    click.echo(f"✗ {e}", err=True)
    sys.exit(1)

raise PackNotFoundError(f'Unknown pack: "{name}"') from None
```

### Incorrect
```python
class PackNotFoundError(Exception): ...   # missing base class
except Exception as e: pass              # swallowed, too broad
except:                                  # bare except
try: ... except SomeError: pass          # silent swallow
```

### Re-raise with context
```python
except yaml.YAMLError as e:
    raise ArgusConfigError("Invalid .argus.yml") from e
```
```

## Test Impact

`tests/test_packs.py` `REQUIRED_PACKS` must include `"error-handling"`.

## Out of Scope

- Refactoring existing exceptions to inherit from `ArgusError` — that is an implementation task, not a standards pack concern
- Logging standards — varies by project; out of scope for this pack
