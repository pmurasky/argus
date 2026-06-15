## TDD Example: Implementing a discount method

### Step 1 — RED (write the test first)

```python
def test_apply_discount_reduces_price_by_percentage():
    # Given
    product = Product(price=100.0)
    # When
    discounted = product.apply_discount(20)
    # Then
    assert discounted == 80.0
```

Run: `pytest tests/test_product.py::test_apply_discount_reduces_price_by_percentage -v`
**Expected: FAIL** — `AttributeError: 'Product' object has no attribute 'apply_discount'`

### Step 2 — GREEN (minimum code to pass)

```python
def apply_discount(self, percentage: float) -> float:
    return self.price * (1 - percentage / 100)
```

Run: `pytest tests/test_product.py::test_apply_discount_reduces_price_by_percentage -v`
**Expected: PASS**

Commit: `git commit -m "feat: implement apply_discount method"`

### Step 3 — REFACTOR (improve without changing behaviour)

```python
def apply_discount(self, percentage: float) -> float:
    discount_multiplier = 1 - percentage / 100
    return self.price * discount_multiplier
```

Run: `pytest tests/test_product.py -v`
**Expected: PASS** — all tests still green

Commit: `git commit -m "refactor: extract discount_multiplier for clarity"`
