# Refactoring Pack — Design Spec

**Date:** 2026-06-16
**Status:** Approved

## Summary

Add a `refactoring` pack to argus that teaches agents when to refactor, what code smells signal the need, and how to do it safely — one change at a time, never mixing new behavior with structural improvement.

## Decisions

| Question | Decision | Rationale |
|---|---|---|
| Scope | When + smells + safe technique | The TDD pack names the Refactor phase but gives no guidance on what to do there — this fills that gap |
| Smell taxonomy | Fowler/Refactoring.guru categories (bloaters, dispensables, OO abusers, couplers) | Industry-standard, widely recognized, mechanically detectable |
| Timing rules | Rule of Three + preparatory refactoring + TDD Refactor phase | Covers all three legitimate refactoring triggers without overlapping the TDD pack |
| Requires | `["tdd"]` | Safe refactoring requires passing tests; refactoring without tests is rewriting |
| Pack format | Full pack (instructions + checklist + examples) | Consistent with existing packs; plugs into pre-commit gate |

## Pack Structure

```
argus/packs/refactoring/
  pack.yml
  instructions.md
  checklist.md
  examples.md
```

## `pack.yml`

```yaml
name: refactoring
description: Refactor safely — detect code smells, one change at a time, never break tests
category: quality
requires:
  - tdd
platforms: [all]
```

## `instructions.md`

```markdown
# Refactoring

## Core Rule
Refactoring means changing code structure without changing external behavior. Never add new
functionality in the same commit as a refactor — that is always a separate change.

## When to Refactor

**Rule of Three:** The first time you write something, just do it. The second time you do
something similar, note the duplication. The third time, refactor.

**Preparatory refactoring:** Before adding a feature, refactor the code to make the feature
easy to add. "Make the change easy, then make the easy change." — Kent Beck. The refactor
is one commit; the feature is the next.

**TDD Refactor phase:** The REFACTOR step only happens after GREEN (tests passing). Never
refactor during RED — finish making the test pass first.

**Never refactor when:**
- Tests are failing
- You are in the RED phase of TDD
- You are mid-feature (finish the feature first, then clean up)

## Code Smells — What Signals Refactoring

### Bloaters (things that grew too large)
- **Long Method** — any method over 20 lines → Extract Method
- **Large Class** — class over 300 lines → Extract Class
- **Long Parameter List** — more than 5 parameters → Introduce Parameter Object
- **Data Clumps** — same group of variables together in multiple places → Extract Class
- **Primitive Obsession** — using a `str` or `int` where a small class would be clearer → Replace Primitive with Object

### Dispensables (things that add no value)
- **Duplicate Code** — same logic in two or more places → Extract Function
- **Dead Code** — unreachable or unused code → Delete it
- **Speculative Generality** — abstractions nobody uses yet → Delete it
- **Excessive Comments** — a comment explaining what the code does signals unclear code → Rename or extract until the comment is unnecessary

### Object-Orientation Abusers
- **Switch/Match on type** — dispatching behavior based on an object's type → Strategy pattern (see design-patterns pack)
- **Refused Bequest** — subclass ignores most of what the parent provides → Rework the hierarchy

### Couplers (inappropriate dependencies)
- **Feature Envy** — a method uses another class's data more than its own → Move Method
- **Message Chains** — `a.b().c().d()` → Extract Method or Hide Delegate
- **Inappropriate Intimacy** — two classes know too much about each other's internals → Extract Class or Move Method

## How to Refactor Safely

1. **Confirm tests pass** before starting — if they don't, fix that first
2. **Make one change** — extract one method, rename one variable, move one class
3. **Run tests** after each change — if they fail, undo and reconsider
4. **Commit** when tests pass and the change is complete: `refactor: <what you improved>`
5. **Never** mix refactoring and new behavior in the same commit

## Red Flags — Stop and Correct
- Refactoring with failing tests
- Adding a new feature during a refactoring commit
- Making multiple structural changes before running tests
- Commit message contains both `feat:` and `refactor:` concerns
```

## `checklist.md`

```markdown
## Refactoring Pre-Commit Checklist

- [ ] Tests were passing before I started refactoring
- [ ] I am in the TDD REFACTOR phase (after GREEN) — not during RED
- [ ] This commit changes structure only — no new behavior added
- [ ] I made one change at a time and ran tests after each step
- [ ] All tests still pass
- [ ] Commit message is `refactor: <what you improved>`
- [ ] No code smells remain in the changed code (check: method length, duplication, parameter count)
```

## `examples.md`

````markdown
## Refactoring Examples

### Correct — Preparatory Refactoring

```python
# Step 1: refactor commit — extract method to make room for new logic
# Before
def process(self, data: dict[str, Any]) -> Result:
    validated = {k: v for k, v in data.items() if v is not None}
    if not validated:
        raise ValueError("empty")
    return Result(validated)

# After (refactor commit: "refactor: extract validation into _validate")
def process(self, data: dict[str, Any]) -> Result:
    validated = self._validate(data)
    return Result(validated)

def _validate(self, data: dict[str, Any]) -> dict[str, Any]:
    result = {k: v for k, v in data.items() if v is not None}
    if not result:
        raise ValueError("empty")
    return result

# Step 2: feature commit — add new logic cleanly to _validate
```

### Incorrect — Mixed Commit

```python
# Bad: adds a feature AND renames in the same commit
def process(self, data: dict[str, Any], strict: bool = False) -> Result:
    # renamed from old_validate; also added strict parameter
    validated = {k: v for k, v in data.items() if v is not None}
    if strict and not validated:
        raise ValueError("strict mode: empty input")
    return Result(validated)
```

### Correct — Extracting Duplicate Code

```python
# Before: same pagination logic in two methods
def list_users(self) -> list[User]:
    page, size = 1, 50
    results = []
    while True:
        batch = self._api.get("/users", page=page, size=size)
        results.extend(batch)
        if len(batch) < size:
            break
        page += 1
    return results

def list_orders(self) -> list[Order]:
    page, size = 1, 50
    results = []
    while True:
        batch = self._api.get("/orders", page=page, size=size)
        results.extend(batch)
        if len(batch) < size:
            break
        page += 1
    return results

# After: refactor commit — extract _paginate
def list_users(self) -> list[User]:
    return self._paginate("/users")

def list_orders(self) -> list[Order]:
    return self._paginate("/orders")

def _paginate(self, endpoint: str) -> list[Any]:
    page, size = 1, 50
    results = []
    while True:
        batch = self._api.get(endpoint, page=page, size=size)
        results.extend(batch)
        if len(batch) < size:
            break
        page += 1
    return results
```

### Correct — Eliminating Primitive Obsession

```python
# Before: email passed as raw string everywhere
def send_welcome(self, email: str) -> None: ...
def update_contact(self, email: str) -> None: ...

# After: refactor commit — introduce Email value object
@dataclass(frozen=True)
class Email:
    value: str
    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError(f"Invalid email: {self.value}")

def send_welcome(self, email: Email) -> None: ...
def update_contact(self, email: Email) -> None: ...
```
````

## Test Impact

`tests/test_packs.py` has a `REQUIRED_PACKS` list — `refactoring` must be added there so the existing parametrized tests cover the new pack.

## Out of Scope

- Automated refactoring tool configuration (rope, PyCharm refactoring) — tooling choice, not a rules concern
- Full Fowler refactoring catalog — the pack covers smells and safe technique; the catalog is reference material
