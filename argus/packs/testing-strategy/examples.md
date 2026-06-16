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
    assert browser.find("Total: $90.00")  # slow, fragile, hides the logic under the UI

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
    # Given
    forecast = ForecastFormatter(weather=StubWeatherService())
    # When
    result = forecast.summary("London")
    # Then
    assert result == "London: 22.5°C"

# Fake: working in-memory implementation
class InMemoryUserRepository:
    def __init__(self) -> None:
        self._store: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._store[user.email] = user

    def find_by_email(self, email: str) -> User | None:
        return self._store.get(email)

def test_registration_saves_user():
    # Given
    repo = InMemoryUserRepository()
    service = RegistrationService(users=repo)
    # When
    service.register("alice@example.com")
    # Then
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
    # This test breaks if you rename the method or change the call site,
    # even if registration still works correctly end-to-end.
```
