# PyPI Publish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish `argus-standards` to PyPI with a tag-triggered GitHub Actions workflow using OIDC trusted publishing.

**Architecture:** Three file changes (pyproject.toml metadata, README.md content, publish workflow), plus one-time manual PyPI/TestPyPI trusted publisher registration. No new Python code — this is entirely configuration and content.

**Tech Stack:** hatchling (build), pypa/gh-action-pypi-publish (upload), GitHub Actions OIDC (auth)

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `pyproject.toml` | Modify | Add authors, license, readme, classifiers, [project.urls] |
| `README.md` | Overwrite | Full content for PyPI landing page |
| `.github/workflows/publish.yml` | Create | Tag-triggered publish to TestPyPI then PyPI |

---

## Task 1: Add PyPI Metadata to pyproject.toml

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add metadata fields to [project]**

Open `pyproject.toml` and add the following lines immediately after the `description` line:

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

- [ ] **Step 2: Add [project.urls] section**

Add this new section after `[project.optional-dependencies]`:

```toml
[project.urls]
Homepage = "https://github.com/pmurasky/argus"
Repository = "https://github.com/pmurasky/argus"
Issues = "https://github.com/pmurasky/argus/issues"
```

- [ ] **Step 3: Verify the build succeeds**

```bash
cd /media/peter/Linux_AppData/AIProjects/argus
pip install hatch --quiet
hatch build
```

Expected: `dist/argus_standards-0.1.0-py3-none-any.whl` and `dist/argus_standards-0.1.0.tar.gz` created with no errors.

- [ ] **Step 4: Inspect the wheel metadata**

```bash
python3 -c "
import zipfile, sys
whl = sorted(__import__('pathlib').Path('dist').glob('*.whl'))[0]
with zipfile.ZipFile(whl) as z:
    meta = [f for f in z.namelist() if f.endswith('METADATA')][0]
    print(z.read(meta).decode())
" | head -40
```

Expected: `Author-email`, `Classifier`, `Project-URL`, and `License` lines all present.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml
git commit -m "chore(pyproject): add PyPI publication metadata"
```

---

## Task 2: Write README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Overwrite README.md with full content**

Replace the entire contents of `README.md` with:

```markdown
# argus-standards

[![PyPI version](https://img.shields.io/pypi/v/argus-standards)](https://pypi.org/project/argus-standards/)
[![Python 3.11+](https://img.shields.io/pypi/pyversions/argus-standards)](https://pypi.org/project/argus-standards/)
[![License: MIT](https://img.shields.io/github/license/pmurasky/argus)](LICENSE)

Argus injects engineering discipline into AI coding agents via platform-specific instruction files generated from composable standards packs.

AI coding agents skip TDD, produce commit blobs, and violate SOLID by default. Argus fixes this by generating the right system prompt files for your platform — one command, any combination of standards.

## Install

```bash
pip install argus-standards
```

## Quick Start

**1. Create `.argus.yml` in your project root:**

```yaml
packs:
  - tdd
  - atomic-commit
  - solid
```

**2. Generate platform files:**

```bash
argus generate
```

Argus writes instruction files for every supported platform it detects in your project. For example, with Claude Code and Cursor present:

```
✓ Wrote AGENTS.md
✓ Wrote CLAUDE.md
✓ Wrote .claude/rules/tdd.md
✓ Wrote .claude/rules/atomic-commit.md
✓ Wrote .claude/rules/solid.md
✓ Wrote .claude/skills/tdd/SKILL.md
✓ Wrote .claude/skills/atomic-commit/SKILL.md
✓ Wrote .claude/skills/solid/SKILL.md
✓ Wrote .cursor/rules/tdd.md
✓ Wrote .cursor/rules/atomic-commit.md
✓ Wrote .cursor/rules/solid.md
```

## Commands

| Command | Description |
|---|---|
| `argus init` | Create a starter `.argus.yml` in the current directory |
| `argus generate` | Generate platform files from `.argus.yml` |
| `argus generate --dry-run` | Preview files that would be written without writing them |
| `argus generate --check` | Exit non-zero if generated output differs from disk (for CI) |
| `argus packs list` | List all available packs |
| `argus packs show <name>` | Show the full content of a pack |
| `argus platforms list` | List all supported platforms |
| `argus validate` | Validate `.argus.yml` without generating files |

## Packs

Packs are composable engineering standards. Include only the ones your project needs.

| Pack | Description |
|---|---|
| `tdd` | Test-driven development — RED → GREEN → COMMIT → REFACTOR cycle |
| `atomic-commit` | One logical change per commit, conventional commit format |
| `solid` | SOLID principles with mechanically detectable violation checklist |
| `code-quality` | Cyclomatic complexity ≤ 10, method ≤ 20 lines, class ≤ 300 lines |
| `pre-commit` | Non-negotiable pre-commit gate combining all active standards |
| `error-handling` | Exception hierarchy, raise vs return rules, catching at boundaries |
| `type-safety` | Full annotation coverage, mypy-clean, no Any in signatures |
| `documentation-standards` | Docstrings on public API, imperative mood, no what-comments |
| `dependency-injection` | Constructor injection, depend on abstractions, single composition root |
| `design-patterns` | Strategy/Factory/Observer patterns to eliminate type-dispatch |
| `refactoring` | Safe refactoring cycles, code smell catalog, preparatory refactoring |
| `testing-strategy` | Test pyramid, test doubles guide, right layer for each test type |

## Platforms

| Platform | Files Generated |
|---|---|
| Claude Code (`claude`) | `CLAUDE.md`, `.claude/rules/{pack}.md`, `.claude/skills/{pack}/SKILL.md` |
| Cursor (`cursor`) | `.cursor/rules/{pack}.md` |
| GitHub Copilot (`copilot`) | `.github/copilot-instructions.md` |
| OpenCode (`opencode`) | `opencode.json`, `.opencode/skills/{pack}/SKILL.md`, `.opencode/commands/{pack}.md` |

All platforms also receive `AGENTS.md` (OpenAI Codex / general agents).

## Development Setup

```bash
git clone https://github.com/pmurasky/argus.git
cd argus
pip install -e ".[dev]"
pytest
```

## License

MIT © Peter Murasky Jr
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: write README for PyPI landing page"
```

---

## Task 3: Create GitHub Actions Publish Workflow

**Files:**
- Create: `.github/workflows/publish.yml`

- [ ] **Step 1: Create publish.yml**

Create `.github/workflows/publish.yml` with this content:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*.*.*"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Run tests
        run: pytest
      - name: Type check
        run: mypy argus/
      - name: Lint
        run: ruff check argus/

  publish-testpypi:
    needs: test
    runs-on: ubuntu-latest
    environment: testpypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Build package
        run: |
          pip install hatch
          hatch build
      - name: Publish to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/

  publish-pypi:
    needs: publish-testpypi
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Build package
        run: |
          pip install hatch
          hatch build
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

- [ ] **Step 2: Validate YAML syntax**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/publish.yml'))"
```

Expected: no output (valid YAML, no exception).

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/publish.yml
git commit -m "ci: add tag-triggered PyPI publish workflow"
```

---

## Task 4: One-Time PyPI Setup (Manual — Not Automated)

These steps are performed once in the browser. No code changes required.

- [ ] **Step 1: Create GitHub Environments**

Go to https://github.com/pmurasky/argus/settings/environments and create two environments:
- `testpypi` — no protection rules needed
- `pypi` — optionally add yourself as a required reviewer

- [ ] **Step 2: Register Trusted Publisher on TestPyPI**

1. Go to https://test.pypi.org — create an account if needed
2. Navigate to: Account Settings → Publishing → Add a new pending publisher
3. Fill in:
   - **PyPI project name:** `argus-standards`
   - **Owner:** `pmurasky`
   - **Repository name:** `argus`
   - **Workflow filename:** `publish.yml`
   - **Environment name:** `testpypi`
4. Click Add

- [ ] **Step 3: Register Trusted Publisher on PyPI**

1. Go to https://pypi.org — create an account if needed
2. Navigate to: Account Settings → Publishing → Add a new pending publisher
3. Fill in:
   - **PyPI project name:** `argus-standards`
   - **Owner:** `pmurasky`
   - **Repository name:** `argus`
   - **Workflow filename:** `publish.yml`
   - **Environment name:** `pypi`
4. Click Add

- [ ] **Step 4: Tag and release**

```bash
git push origin main
git tag v0.1.0
git push origin v0.1.0
```

Watch the Actions tab at https://github.com/pmurasky/argus/actions — the three jobs should run in sequence: `test` → `publish-testpypi` → `publish-pypi`.

- [ ] **Step 5: Verify the PyPI listing**

Visit https://pypi.org/project/argus-standards/ and confirm:
- Description renders from README.md
- Version shows `0.1.0`
- Classifiers, license, and links are all present

Test the install in a clean environment:
```bash
pip install argus-standards
argus --version
argus packs list
```
