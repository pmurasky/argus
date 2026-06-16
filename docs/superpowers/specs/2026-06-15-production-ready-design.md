# Production-Ready Codebase Design

**Date:** 2026-06-15
**Scope:** Fix failing tests, align exception hierarchy, add dev tooling, add GitHub Actions CI

---

## Goal

Bring the Argus codebase to production quality: all tests green, standards violations resolved, dev tooling enforced, and a GitHub Actions CI pipeline that gates every merge.

---

## Section 1: Bug Fix — Failing Integration Tests

**Problem:** 8 integration tests in `tests/integration/test_generate.py` all fail. Every test uses a config with all 4 platforms (`claude`, `opencode`, `copilot`, `cursor`). The most likely root cause is one or more adapters raising an exception during `generate`, causing the CLI to exit with code 1 before any files are written.

**Approach:**
1. Run the first failing test with full output to identify the actual error.
2. Locate the broken adapter(s) or write path in the CLI.
3. Fix until all 128 tests pass. No suppression, no test adjustments.

**Constraints:**
- If the bug is in the CLI write loop (e.g., missing `parent.mkdir(parents=True, exist_ok=True)`), one fix covers all 8.
- If the bug is in a specific adapter, each broken adapter gets its own fix commit following the TDD cycle (RED already exists — go straight to GREEN then COMMIT).
- All existing passing tests must remain green throughout.

---

## Section 2: Exception Hierarchy

**Problem:** `PackNotFoundError` (`loader.py`), `UnknownPlatformError`, and `AdapterConflictError` (`generator.py`) inherit directly from `Exception`, violating the project error-handling rule that all custom exceptions must inherit from a project-level base.

**Fix:**
- Add `class ArgusError(Exception): ...` to `argus/__init__.py`.
- Update `PackNotFoundError` in `loader.py` to inherit from `ArgusError`.
- Update `UnknownPlatformError` and `AdapterConflictError` in `generator.py` to inherit from `ArgusError`.

**No behavior changes.** Catch sites in `cli.py` already use specific subtypes and remain unchanged.

**Commit strategy:** One atomic commit per file changed (`fix(exceptions): ...`).

---

## Section 3: Dev Tooling

All configuration added to `pyproject.toml`. No new files.

### Optional dependencies

```toml
[project.optional-dependencies]
dev = [
    "mypy>=1.0",
    "ruff>=0.4",
    "pytest-cov>=4.0",
]
```

Install with: `pip install -e ".[dev]"`

### mypy

```toml
[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
```

Run: `mypy argus/` — must exit 0 before CI is added. Full `strict = true` is deferred; these flags enforce annotation completeness without triggering third-party stub issues.

### ruff

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]
```

Run: `ruff check argus/` — must exit 0 before CI is added.

### coverage

```toml
[tool.coverage.run]
source = ["argus"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

### pytest (update existing section)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=argus --cov-report=term-missing"
```

**Order of operations:** Add tooling config, then run mypy and ruff and fix all violations before adding CI — so the pipeline starts clean.

---

## Section 4: GitHub Actions CI

Single workflow file: `.github/workflows/ci.yml`

**Triggers:** `push` and `pull_request` targeting `main`.

**Jobs** (run in parallel, all on `ubuntu-latest`, Python 3.11):

| Job | Command | Fails if |
|-----|---------|----------|
| `test` | `pytest` | Any test fails or coverage < 80% |
| `lint` | `ruff check argus/` | Any lint error |
| `typecheck` | `mypy argus/` | Any type error |

All three jobs must pass for a PR to merge.

---

## Execution Order

1. Fix integration tests (bug fix) — get to 128/128 passing
2. Fix exception hierarchy — align with standards
3. Add dev tooling to pyproject.toml — configure mypy, ruff, coverage
4. Fix any mypy/ruff violations surfaced by new tooling
5. Add GitHub Actions CI workflow

Each step is independently committable and verifiable before the next begins.
