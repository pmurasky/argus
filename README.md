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
✓ AGENTS.md
✓ CLAUDE.md
✓ .claude/rules/tdd.md
✓ .claude/rules/atomic-commit.md
✓ .claude/rules/solid.md
✓ .claude/skills/tdd/SKILL.md
✓ .claude/skills/atomic-commit/SKILL.md
✓ .claude/skills/solid/SKILL.md
✓ .cursor/rules/tdd.md
✓ .cursor/rules/atomic-commit.md
✓ .cursor/rules/solid.md
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
