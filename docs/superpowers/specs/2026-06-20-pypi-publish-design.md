# PyPI Publish Design

**Date:** 2026-06-20
**Status:** Approved

## Goal

Publish `argus-standards` to PyPI so users can install it with `pip install argus-standards`. Releases are triggered by pushing a `v*.*.*` git tag and published automatically via GitHub Actions using OIDC trusted publishing (no secrets required).

---

## 1. `pyproject.toml` Metadata Additions

Add to the `[project]` table:

```toml
authors = [{name = "Peter Murasky Jr", email = "peter.murasky@gmail.com"}]
license = {text = "MIT"}
readme = "README.md"
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Quality Assurance",
]
```

Add a new `[project.urls]` table:

```toml
[project.urls]
Homepage = "https://github.com/pmurasky/argus"
Repository = "https://github.com/pmurasky/argus"
Issues = "https://github.com/pmurasky/argus/issues"
```

---

## 2. README.md Content

The README is the PyPI landing page. Structure:

1. **Badge row** — PyPI version badge, Python version badge, MIT license badge
2. **One-line hook** — "Argus injects engineering discipline into AI coding agents via platform-specific instruction files generated from composable standards packs."
3. **Install** — `pip install argus-standards`
4. **Quick start** — minimal `.argus.yml` + `argus generate` showing output files created
5. **Commands table** — `init`, `generate` (with `--dry-run`, `--check`), `packs list`, `packs show`, `platforms list`, `validate`
6. **Packs table** — name + one-line description for all available packs
7. **Platforms table** — platform name + file(s) generated
8. **License** — "MIT © Peter Murasky Jr"

---

## 3. GitHub Actions Publish Workflow

**File:** `.github/workflows/publish.yml`
**Trigger:** `push` to tags matching `v*.*.*`

### Jobs

**`test`**
- Checks out code, sets up Python 3.11, installs with `pip install -e ".[dev]"`
- Runs `pytest`, `mypy argus/`, `ruff check argus/`

**`publish-testpypi`**
- `needs: test`
- Builds with `hatch build`
- Uses `pypa/gh-action-pypi-publish@release/v1` with `repository-url: https://test.pypi.org/legacy/`
- Requires `permissions: id-token: write`

**`publish-pypi`**
- `needs: publish-testpypi`
- Same action, default repository (real PyPI)
- Requires `permissions: id-token: write`

### Environment Names
- TestPyPI job uses environment `testpypi`
- PyPI job uses environment `pypi`

These environment names must match what is registered on PyPI as the trusted publisher.

---

## 4. One-Time PyPI Setup (Manual Steps)

These steps are performed once by the maintainer in the browser — not automated.

### TestPyPI Trusted Publisher
1. Create account at https://test.pypi.org (if needed)
2. Go to Account Settings → Publishing → Add a new pending publisher
3. Fill in:
   - PyPI project name: `argus-standards`
   - Owner: `pmurasky`
   - Repository: `argus`
   - Workflow filename: `publish.yml`
   - Environment name: `testpypi`

### PyPI Trusted Publisher
1. Create account at https://pypi.org (if needed)
2. Same flow: Account Settings → Publishing → Add a new pending publisher
3. Fill in:
   - PyPI project name: `argus-standards`
   - Owner: `pmurasky`
   - Repository: `argus`
   - Workflow filename: `publish.yml`
   - Environment name: `pypi`

### GitHub Environments
Create two environments in the repo (Settings → Environments):
- `testpypi` — no protection rules needed
- `pypi` — optionally add "Required reviewers" for extra safety on production deploys

---

## 5. Release Process

Once setup is complete, releasing is:

```bash
# Bump version in pyproject.toml (e.g., 0.1.0 → 0.1.1)
# Commit: chore(release): bump version to 0.1.1
git tag v0.1.1
git push origin v0.1.1
```

GitHub Actions runs automatically:
1. Tests gate the build
2. Package uploads to TestPyPI
3. Package uploads to real PyPI

---

## 6. Out of Scope

- CHANGELOG.md (deferred to V1.1)
- Version bump automation via `hatch version` (deferred to V1.1)
- `pip install` from TestPyPI verification step (manual check by maintainer)
