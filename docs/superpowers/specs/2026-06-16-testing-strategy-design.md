# Testing Strategy Pack — Design Spec

**Date:** 2026-06-16
**Status:** Approved

## Summary

Add a `testing-strategy` pack to argus that establishes which test layer to use (unit, integration,
E2E), how to choose the right test double, and when each layer runs in the commit/push/CI pipeline.
This complements the `tdd` pack (which covers unit test discipline) by answering the layer-selection
decision `tdd` deliberately omits.

## Decisions

| Question | Decision | Rationale |
|---|---|---|
| Relationship to `tdd` | Complement, not replace | `tdd` owns unit test structure and the Red/Green/Refactor cycle; this pack owns layer selection and test doubles |
| Scope | Pyramid + doubles + execution tiers | These three are inseparable: choosing the wrong layer and the wrong double both produce fragile suites; tiers enforce it at the tooling level |
| Test double guidance | Fake/Stub/Mock with when-to-use rules | Mock overuse is the most common source of brittle tests; explicit rules prevent it |
| Contract testing | Out of scope | Consumer-driven contracts (Pact) are microservices-specific; most argus users work in monoliths |
| Requires | `["tdd"]` | The pyramid sits on top of TDD unit test discipline; the pack assumes it |
| Pack format | Full pack (instructions + checklist + examples) | Consistent with existing packs; plugs into pre-commit gate |

## Pack Structure

```
argus/packs/testing-strategy/
  pack.yml
  instructions.md
  checklist.md
  examples.md
```

## `pack.yml`

```yaml
name: testing-strategy
description: Test at the right layer — unit, integration, and E2E with appropriate doubles
category: quality
requires:
  - tdd
platforms: [all]
```

## `instructions.md`

```markdown
# Testing Strategy

## Core Rule
Test at the lowest layer that gives you confidence. More unit tests than integration tests;
more integration tests than E2E tests. Inverting this pyramid produces a slow, fragile suite.

## The Test Pyramid

        /\
       /E2E\       ← few, slow, fragile — critical journeys only
      /------\
     /Integr. \    ← moderate — only at system boundaries
    /----------\
   / Unit Tests \  ← many, fast, isolated — all business logic
  /--------------\

The pyramid shape is intentional: unit tests are cheap to write and run in milliseconds;
E2E tests are expensive, slow, and occasionally flaky. Inverting it is a common mistake
that teams pay for with hours of CI time and fragile suites.

## Unit Tests

**Use for:** Business logic, algorithms, transformations, domain rules — anything that can
be tested without external dependencies.
**Characteristics:** No I/O, no network, no database. Milliseconds per test. Deterministic.
**Coverage:** 80% minimum for changed code (see `tdd` pack).
**Rule:** If it can be tested without any external dependency, test it here.

## Integration Tests

**Use for:** Code that crosses a system boundary — database queries, external API calls,
file I/O, message queues, adapter implementations.
**Characteristics:** Slower than unit tests. Uses real infrastructure or a realistic substitute
(e.g., an in-memory database, a local test container, a fake HTTP server).
**Scope is narrow:** Test the integration point itself, not every code path that reaches it.
One integration test per repository method or adapter — not one per caller.
**Rule:** If the behavior depends on a real external system, test it here, not in unit tests.

## End-to-End Tests

**Use for:** The 2–3 critical user journeys that must never break regardless of internal changes.
**Characteristics:** Slow (seconds to minutes), occasionally flaky due to timing and environment,
expensive to maintain. Tests the whole deployed system.
**Rule:** If a unit or integration test can answer the question, use that instead. E2E tests
are a last resort, not a default.
**Anti-pattern:** Testing every feature E2E. This produces a suite that takes 20+ minutes to
run and breaks on every UI or API change.

## Test Doubles

Use the simplest double that makes the test work:

| Double | What it is | When to use |
|---|---|---|
| **Fake** | A working simplified implementation | Integration tests — in-memory DB, fake HTTP server |
| **Stub** | Returns canned values, no behavior | Unit tests — when you need a value from a collaborator |
| **Mock** | Verifies that specific calls were made | Unit tests — when the interaction itself is the assertion |

**Prefer fakes and stubs over mocks.** Mocks assert on HOW code works internally — they
break when you refactor, even when behavior is correct. Fakes and stubs assert on WHAT
the code produces — they survive refactoring. See the `dependency-injection` pack for how
constructor injection makes substitution easy without patching internals.

**Never patch internals to test.** If you need to monkey-patch a private method or module
internals to write a test, that is a signal to inject the dependency instead.

## Test Execution Tiers

| When | What runs | Why |
|---|---|---|
| Before every commit | Unit tests only | Fast, isolated — no reason to skip |
| Before push | Unit tests + integration tests | Catch boundary failures before teammates see them |
| CI pipeline | Unit + integration + E2E | Hard gate — failures block merge |

## Red Flags — Stop and Correct
- E2E test written for a feature that could be covered by a unit test
- Mock asserting on an internal private method call
- Integration test covering business logic (that belongs in unit tests)
- Unit test hitting a real database or network
- Test suite takes more than 5 minutes to run locally (pyramid is inverted)
```

## `checklist.md`

```markdown
## Testing Strategy Pre-Commit Checklist

- [ ] New business logic is tested at the unit level — not only through integration or E2E
- [ ] Integration tests cover system boundaries only (DB, APIs, file I/O) — not business logic
- [ ] E2E tests added only for new critical user journeys, not for every new feature
- [ ] Test doubles are the simplest type that works — prefer fake/stub over mock
- [ ] No mock asserting on an internal or private method call
- [ ] No unit test hitting a real database, network, or file system
- [ ] Unit tests pass before commit; integration tests pass before push
```

## `examples.md`

````markdown
## Testing Strategy Examples

### Correct — Testing at the Right Layer

```python
# Business logic → unit test (no DB, no network)
def test_discount_applied_when_member():
    # Given
    cart = Cart(items=[Item(price=100)], membership=MembershipTier.GOLD)
    # When
    total = cart.calculate_total()
    # Then
    assert total == 90  # 10% member discount

# DB query → integration test (real or containerized DB)
def test_repository_finds_user_by_email(db_session):
    # Given
    db_session.add(User(email="a@b.com", name="Alice"))
    db_session.commit()
    repo = UserRepository(db_session)
    # When
    result = repo.find_by_email("a@b.com")
    # Then
    assert result.name == "Alice"

# Critical journey → E2E test (whole system)
def test_user_can_complete_checkout(browser):
    browser.visit("/products")
    browser.click("Add to cart")
    browser.click("Checkout")
    assert browser.find("Order confirmed")
```

### Incorrect — Wrong Layer

```python
# Bad: testing business logic through an E2E test
def test_discount_applied_when_member(browser):
    browser.login_as_gold_member()
    browser.add_item_to_cart(price=100)
    assert browser.find("Total: $90.00")  # slow, fragile, hides the logic under UI

# Bad: unit test hitting a real database
def test_find_user():
    repo = UserRepository(real_db_connection)  # breaks in CI without a running DB
    result = repo.find_by_email("a@b.com")
    assert result is not None
```

### Correct — Test Doubles

```python
# Stub: return a canned value, don't verify calls
class StubWeatherService:
    def current_temp(self, city: str) -> float:
        return 22.5

def test_forecast_formats_temperature():
    forecast = ForecastFormatter(weather=StubWeatherService())
    assert forecast.summary("London") == "London: 22.5°C"

# Fake: working in-memory implementation
class InMemoryUserRepository:
    def __init__(self) -> None:
        self._store: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._store[user.email] = user

    def find_by_email(self, email: str) -> User | None:
        return self._store.get(email)

def test_registration_saves_user():
    repo = InMemoryUserRepository()
    service = RegistrationService(users=repo)
    service.register("alice@example.com")
    assert repo.find_by_email("alice@example.com") is not None
```

### Incorrect — Mock Overuse

```python
# Bad: mock asserting on internal call — breaks on refactor
def test_registration_saves_user():
    repo = MagicMock()
    service = RegistrationService(users=repo)
    service.register("alice@example.com")
    repo.save.assert_called_once_with(User(email="alice@example.com"))
    # This test breaks if you rename the method or change the call site —
    # even if registration still works correctly end-to-end.
```
````

## Test Impact

`tests/test_packs.py` has a `REQUIRED_PACKS` list — `testing-strategy` must be added there so the
existing parametrized tests cover the new pack.

## Out of Scope

- Consumer-driven contract testing (Pact) — microservices-specific; out of scope for general use
- Property-based testing (Hypothesis) — advanced technique; belongs in a dedicated pack if needed
- Mutation testing — tooling concern; not an agent instruction topic
- Performance / load testing — separate discipline
