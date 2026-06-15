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
