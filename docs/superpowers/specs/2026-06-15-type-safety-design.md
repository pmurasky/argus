# Type Safety Pack — Design Spec

**Date:** 2026-06-15
**Status:** Approved

## Summary

Add a `type-safety` pack to argus that enforces Python type annotations on all functions and methods, with mypy as the enforcement tool.

## Decisions

| Question | Decision | Rationale |
|---|---|---|
| Annotation scope | All functions (public + private) | Full traceability; mypy default behaviour |
| Type checker | mypy | De facto standard; concrete pre-commit command |
| `Any` policy | Permitted at YAML/JSON/CLI boundaries only; never in signatures | YAML payloads are genuinely unstructured; forcing TypedDict everywhere is over-engineering |
| Pack format | Full pack (instructions + checklist + examples) | Consistent with existing packs; plugs into pre-commit gate |

## Pack Structure

```
argus/packs/type-safety/
  pack.yml
  instructions.md
  checklist.md
  examples.md
.claude/rules/type-safety.md
```

## `pack.yml`

```yaml
name: type-safety
description: Python type annotations — all functions annotated, mypy clean
category: quality
requires: []
platforms: [all]
```

## `instructions.md`

```markdown
# Type Safety

## Core Rule
Every function and method must have fully annotated parameters and return type.
Run `mypy argus/` before committing — it must exit 0.

## Annotation Requirements
- All parameters annotated — no bare untyped arguments
- All return types explicit — including `-> None`
- Use `X | None` syntax (not `Optional[X]`)
- Use built-in generics: `list[str]`, `dict[str, int]` (not `List`, `Dict` from `typing`)

## `Any` Policy
`Any` is permitted **only at external data boundaries** (YAML, JSON, CLI input).
Assign the unstructured value to a typed local variable as soon as its shape is known.
`Any` in function signatures is never permitted.

## Red Flags — Stop and Correct
- Unannotated function parameter or return type
- `Any` in a function signature
- `Optional[X]` instead of `X | None`
- `List`, `Dict`, `Tuple` imported from `typing` (use built-ins)
- mypy exits non-zero
```

## `checklist.md`

```markdown
- [ ] Every function parameter has a type annotation
- [ ] Every function has an explicit return type (including `-> None`)
- [ ] `X | None` used instead of `Optional[X]`
- [ ] Built-in generics used: `list[str]` not `List[str]`
- [ ] `Any` appears only at YAML/JSON/CLI boundaries, never in function signatures
- [ ] `mypy argus/` exits 0
```

## `examples.md`

```markdown
## Correct
def load(self, pack_names: list[str]) -> list[Pack]: ...
def from_file(cls, path: Path) -> "ArgusConfig": ...
custom_packs_dir: Path | None = None

## Incorrect
def load(self, pack_names): ...           # missing annotations
def get(cls, platform_id: str):  ...      # missing return type
Optional[Path]                            # use Path | None
List[str]                                 # use list[str]

## Correct boundary usage
data: dict[str, Any] = yaml.safe_load(path.read_text())
packs: list[str] = data["packs"]         # typed immediately after
```

## Test Impact

`tests/test_packs.py` has a `REQUIRED_PACKS` list — `type-safety` must be added there so the existing parametrized tests cover the new pack.

## Out of Scope

- mypy configuration (`mypy.ini` / `pyproject.toml`) — tooling setup, not a rules pack concern
- Third-party stub packages (`types-PyYAML` etc.) — project-level setup decision
