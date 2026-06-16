# Production-Ready Codebase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix 8 failing integration tests, align exception hierarchy with project standards, add dev tooling, and enforce quality via GitHub Actions CI.

**Architecture:** Four sequential phases — (1) fix the entry-points installation bug blocking integration tests, (2) add `ArgusError` base and update all custom exceptions, (3) add mypy/ruff/pytest-cov tooling and fix violations, (4) add GitHub Actions CI that gates every merge. Each phase leaves the test suite green before the next begins.

**Tech Stack:** Python 3.11+, pytest, mypy, ruff, pytest-cov, GitHub Actions

---

## Task 1: Fix integration tests (entry-points not registered)

**Root cause:** `AdapterRegistry.get()` in `argus/generator.py` uses `importlib.metadata.entry_points(group="argus.adapters")` to discover adapters. This returns an empty list unless the package is installed via `pip install -e .` in the active Python environment. The 120 passing tests import adapters directly and never touch the registry. The 8 integration tests invoke the CLI end-to-end, which goes through the registry, finds nothing, and raises `UnknownPlatformError`.

**The RED tests already exist** — the 8 failing integration tests are the RED state. No new tests to write.

**Files:**
- No production code changes needed
- Modify: `README.md` — add dev setup section

- [ ] **Step 1: Confirm root cause**

```bash
python3 -m pytest tests/integration/test_generate.py::test_generate_produces_claude_files -v -s 2>&1 | grep "Available platforms"
```

Expected output: `Available platforms: ` (empty string — confirms entry_points not registered)

- [ ] **Step 2: Install the package in the active Python environment**

```bash
pip3 install -e .
```

Expected: `Successfully installed argus-standards-0.1.0`

- [ ] **Step 3: Run integration tests to confirm GREEN**

```bash
python3 -m pytest tests/integration/ -v 2>&1 | tail -15
```

Expected: `8 passed`

- [ ] **Step 4: Run full suite to confirm 128/128**

```bash
python3 -m pytest tests/ -v 2>&1 | tail -5
```

Expected: `128 passed in X.XXs`

- [ ] **Step 5: Add dev setup section to README.md**

If README.md doesn't exist, create it. Otherwise append this section:

```markdown
## Development Setup

```bash
# Install in editable mode — required for integration tests (registers entry points)
pip install -e .

# Run the full test suite
pytest
```
```

- [ ] **Step 6: Commit**

```bash
git add README.md
git commit -m "docs: document pip install -e . requirement for integration tests"
```

---

## Task 2: Add ArgusError base exception

**Problem:** `PackNotFoundError` (`loader.py`), `UnknownPlatformError`, and `AdapterConflictError` (`generator.py`) inherit directly from `Exception`, violating the project error-handling rule that all custom exceptions must inherit from a project-level base in `argus/__init__.py`.

**Files:**
- Modify: `argus/__init__.py` — add `ArgusError`
- Modify: `argus/loader.py` — `PackNotFoundError` inherits `ArgusError`
- Modify: `argus/generator.py` — `UnknownPlatformError`, `AdapterConflictError` inherit `ArgusError`
- Create: `tests/test_exceptions.py` — hierarchy assertions

- [ ] **Step 1: Write the failing tests**

Create `tests/test_exceptions.py`:

```python
from argus import ArgusError
from argus.loader import PackNotFoundError
from argus.generator import UnknownPlatformError, AdapterConflictError


def test_pack_not_found_error_is_argus_error():
    assert issubclass(PackNotFoundError, ArgusError)


def test_unknown_platform_error_is_argus_error():
    assert issubclass(UnknownPlatformError, ArgusError)


def test_adapter_conflict_error_is_argus_error():
    assert issubclass(AdapterConflictError, ArgusError)
```

- [ ] **Step 2: Run to confirm RED**

```bash
python3 -m pytest tests/test_exceptions.py -v 2>&1
```

Expected: `3 failed` — `ImportError: cannot import name 'ArgusError' from 'argus'`

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_exceptions.py
git commit -m "test: add failing tests for ArgusError exception hierarchy"
```

- [ ] **Step 4: Add ArgusError to argus/__init__.py**

The file is currently empty. Replace it with:

```python
class ArgusError(Exception):
    """Base exception for all Argus errors."""
```

- [ ] **Step 5: Update PackNotFoundError in argus/loader.py**

Change the top of `argus/loader.py` from:

```python
from pathlib import Path
import yaml
from argus.adapters.base import Pack


class PackNotFoundError(Exception):
    pass
```

To:

```python
from pathlib import Path
import yaml
from argus import ArgusError
from argus.adapters.base import Pack


class PackNotFoundError(ArgusError):
    """Raised when a requested pack cannot be found on the search path."""
```

- [ ] **Step 6: Update generator.py exceptions**

Change the top of `argus/generator.py` from:

```python
from importlib.metadata import entry_points
from pathlib import Path
from argus.adapters.base import BaseAdapter, GeneratedFile
from argus.config import ArgusConfig
from argus.loader import PackLoader


class AdapterConflictError(Exception):
    pass


class UnknownPlatformError(Exception):
    pass
```

To:

```python
from importlib.metadata import entry_points
from pathlib import Path
from argus import ArgusError
from argus.adapters.base import BaseAdapter, GeneratedFile
from argus.config import ArgusConfig
from argus.loader import PackLoader


class AdapterConflictError(ArgusError):
    """Raised when multiple adapters register the same platform id."""


class UnknownPlatformError(ArgusError):
    """Raised when a requested platform has no registered adapter."""
```

- [ ] **Step 7: Run tests to confirm GREEN**

```bash
python3 -m pytest tests/test_exceptions.py tests/ -v 2>&1 | tail -5
```

Expected: `131 passed` (128 + 3 new)

- [ ] **Step 8: Commit implementations (one per file)**

```bash
git add argus/__init__.py
git commit -m "feat(exceptions): add ArgusError project base exception"

git add argus/loader.py
git commit -m "fix(loader): PackNotFoundError inherits ArgusError"

git add argus/generator.py
git commit -m "fix(generator): UnknownPlatformError and AdapterConflictError inherit ArgusError"
```

---

## Task 3: Add dev tooling config to pyproject.toml

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add dev dependencies and tool config to pyproject.toml**

Add the following sections. Insert `[project.optional-dependencies]` immediately after the existing `[project]` block. Append the tool sections at the end of the file.

```toml
[project.optional-dependencies]
dev = [
    "mypy>=1.0",
    "ruff>=0.4",
    "pytest-cov>=4.0",
]
```

```toml
[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]

[tool.coverage.run]
source = ["argus"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

Also update the existing `[tool.pytest.ini_options]` section:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=argus --cov-report=term-missing"
```

- [ ] **Step 2: Install dev dependencies**

```bash
pip3 install -e ".[dev]"
```

Expected: installs mypy, ruff, pytest-cov

- [ ] **Step 3: Commit pyproject.toml**

```bash
git add pyproject.toml
git commit -m "chore: add mypy, ruff, pytest-cov dev dependencies and tool config"
```

---

## Task 4: Fix mypy violations

**Files:**
- Modify: `argus/adapters/base.py` (known: `manifest: dict` needs `dict[str, Any]`)
- Modify: any other file mypy flags

- [ ] **Step 1: Run mypy and capture all violations**

```bash
python3 -m mypy argus/ 2>&1
```

Note every file and error code reported.

- [ ] **Step 2: Fix argus/adapters/base.py — manifest type**

In `argus/adapters/base.py`, the `Pack` dataclass has `manifest: dict` which mypy flags as a missing type parameter. Change:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
```

To:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
```

And change the `Pack` field:

```python
    manifest: dict
```

To:

```python
    manifest: dict[str, Any]
```

- [ ] **Step 3: Fix any additional mypy violations reported in Step 1**

For each remaining error, apply the minimal fix:
- Missing return type → add `-> ReturnType`
- `Optional[X]` → change to `X | None`
- `List[X]` / `Dict[X, Y]` → change to `list[X]` / `dict[X, Y]`
- `Any` in a signature → type it properly

- [ ] **Step 4: Run mypy until it exits 0**

```bash
python3 -m mypy argus/ 2>&1
```

Expected: `Success: no issues found in N source files`

- [ ] **Step 5: Run full test suite to confirm nothing broke**

```bash
python3 -m pytest tests/ 2>&1 | tail -5
```

Expected: all tests pass

- [ ] **Step 6: Commit**

```bash
git add argus/
git commit -m "fix(types): resolve mypy violations — annotate manifest and missing return types"
```

---

## Task 5: Fix ruff violations

**Files:**
- Modify: any `argus/` files that ruff flags

- [ ] **Step 1: Run ruff and capture violations**

```bash
python3 -m ruff check argus/ 2>&1
```

- [ ] **Step 2: Auto-fix safe violations**

```bash
python3 -m ruff check argus/ --fix 2>&1
```

- [ ] **Step 3: Manually fix any remaining violations**

Remaining violations after `--fix` typically need manual attention (e.g., unused imports that are part of re-exports). Fix each one.

- [ ] **Step 4: Run ruff to confirm clean**

```bash
python3 -m ruff check argus/ 2>&1
```

Expected: exits 0 with no output

- [ ] **Step 5: Run full test suite to confirm nothing broke**

```bash
python3 -m pytest tests/ 2>&1 | tail -5
```

Expected: all tests pass

- [ ] **Step 6: Commit (only if there were actual violations)**

```bash
git add argus/
git commit -m "fix(lint): resolve ruff violations"
```

If ruff exits clean with no changes, skip this commit.

---

## Task 6: Add GitHub Actions CI workflow

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create the workflows directory**

```bash
mkdir -p .github/workflows
```

- [ ] **Step 2: Create .github/workflows/ci.yml**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: pytest

  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: ruff check argus/

  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: mypy argus/
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow for test, lint, and typecheck"
```

- [ ] **Step 4: Push and verify CI runs**

```bash
git push origin main
```

Open the repository on GitHub → Actions tab. Confirm all three jobs (Test, Lint, Type Check) complete green.
