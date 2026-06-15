# Argus — AI Agent Engineering Standards Layer
## Design Specification
**Date:** 2026-06-14
**Status:** Approved

---

## 1. Problem Statement

AI coding agents (Claude Code, OpenCode, Cursor, GitHub Copilot, etc.) generate functional code but lack engineering discipline. They skip TDD Red phases, produce commit blobs instead of atomic commits, violate SOLID principles, and accumulate tech debt that passes review. The problem is not the AI's capability — it is the absence of a prescribed workflow enforced before the AI starts working.

**Differentiator:** Argus is the only tool that generates all platform-specific enforcement files from a single composable config, in one CLI command, platform-agnostically. Existing tools (TDD Guard, Smithery skills, Codacy) are either single-platform or manual. Argus is neither.

---

## 2. What Argus Is

A Python CLI (`pip install argus`) that reads a project config (`.argus.yml`) and generates platform-specific instruction files for every AI coding agent in scope. The engineering standards — rules, workflows, checklists — live in composable **packs**. Platform-specific formatting is handled by **adapters**. One command generates everything.

```
argus generate
  → CLAUDE.md + .claude/rules/ + .claude/skills/   (Claude Code)
  → AGENTS.md + .opencode/commands/ + .opencode/skills/   (OpenCode)
  → AGENTS.md + .github/copilot-instructions.md   (GitHub Copilot)
  → AGENTS.md + .cursor/rules/   (Cursor)
```

---

## 3. Architecture

### 3.1 Repository Structure

```
argus/
├── argus/                        # Python package (pip-installable)
│   ├── cli.py                    # Click entry point
│   ├── loader.py                 # Two-level pack search (custom → built-in)
│   ├── generator.py              # Orchestrates adapters
│   ├── adapters/
│   │   ├── base.py               # BaseAdapter ABC + Pack + GeneratedFile dataclasses
│   │   ├── claude.py
│   │   ├── opencode.py
│   │   ├── copilot.py
│   │   └── cursor.py
│   └── packs/                    # Built-in canonical packs
│       ├── atomic-commit/
│       ├── tdd/
│       ├── solid/
│       ├── code-quality/
│       └── pre-commit/
├── tests/
│   ├── test_packs.py             # Pack schema validation
│   ├── adapters/                 # Adapter unit tests
│   └── integration/              # End-to-end generate tests
└── pyproject.toml
```

### 3.2 Design Principles Applied

| Principle | How it is applied |
|---|---|
| SRP | Packs own content. Adapters own translation. Loader owns discovery. Generator orchestrates. CLI owns UX. |
| OCP | New platform = one new adapter file, no existing code changes. New pack = one new directory. |
| LSP | Every adapter is substitutable — Generator calls only `adapter.generate(packs)`. |
| ISP | `BaseAdapter` exposes exactly one method. Adapters implement nothing they don't need. |
| DIP | Generator depends on `BaseAdapter` abstraction, never on `ClaudeAdapter` directly. |

---

## 4. Core Abstractions

### 4.1 Pack Schema

Each pack is a directory under `argus/packs/<name>/`:

```
packs/tdd/
├── pack.yml           # Manifest
├── instructions.md    # Injected into system prompt / agent context (stable, cache-friendly)
├── checklist.md       # Enforcement gate (optional — not all adapters use this)
└── examples.md        # Workflow examples (optional)
```

**`pack.yml` fields:**
```yaml
name: tdd
description: Test-driven development — tests before code, always
category: workflow          # workflow | architecture | quality | process
requires: []                # other pack names this depends on
platforms: [all]            # [all] or list of platform_ids
```

**Content design rule:** `instructions.md` must be stable and dense — it lands at a cache breakpoint in Claude Code and similar systems. It must cite the standard it derives from so the AI treats it as authoritative, not advisory. Checklists are separate because they may be invoked on demand rather than always injected.

### 4.2 Adapter Contract

```python
# argus/adapters/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Pack:
    name: str
    manifest: dict
    instructions: str
    checklist: str | None
    examples: str | None

@dataclass
class GeneratedFile:
    path: Path      # relative to project root
    content: str

class BaseAdapter(ABC):
    platform_id: str      # "claude", "opencode", "copilot", "cursor"
    display_name: str

    @abstractmethod
    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        """Translate packs into one or more platform-specific files."""
        ...
```

Adapters are folder-level generators — they return a list of `GeneratedFile`, not a single file. The Claude adapter generates `CLAUDE.md` plus files under `.claude/`. Every adapter also generates `AGENTS.md` as a universal baseline (now an open standard adopted by 30+ tools).

### 4.3 Pack Loader

Two-level search path — project-local packs override built-in packs by name:

```
1. <custom_packs_dir>   (from .argus.yml, default: .argus/packs/)
2. argus/packs/         (built-in, shipped with the pip package)
```

```python
# argus/loader.py
class PackLoader:
    def __init__(self, project_root: Path, custom_packs_dir: Path | None):
        self.search_path = [
            custom_packs_dir or project_root / ".argus/packs",
            importlib.resources.files("argus") / "packs",
        ]

    def load(self, pack_names: list[str]) -> list[Pack]:
        # Resolves each name against search_path in order
        ...
```

This mirrors Ansible's role path resolution — a well-proven pattern for override behavior.

### 4.4 Generator

```python
# argus/generator.py
class Generator:
    def run(self, config: ArgusConfig, project_root: Path) -> list[GeneratedFile]:
        packs = PackLoader(project_root, config.custom_packs_dir).load(config.packs)
        results = []
        for platform_id in config.platforms:
            adapter = AdapterRegistry.get(platform_id)
            results.extend(adapter.generate(packs))
        return results
```

`AdapterRegistry` discovers adapters via Python entry points — the same mechanism used by pytest plugins and Flask extensions. Third-party packages can register new adapters (`argus-adapter-devin`, `argus-adapter-windsurf`) without touching argus core.

**Collision policy:** If two packages register the same `platform_id`, `argus generate` fails with an explicit error naming both packages. Never silently last-one-wins.

### 4.5 Generated File Headers

Every generated file begins with:

```
# Generated by argus. Run `argus generate` to update. Do not edit manually.
```

---

## 5. Project Config

`.argus.yml` in the consuming project root:

```yaml
packs:
  - tdd
  - atomic-commit
  - solid
  - code-quality
  - pre-commit
platforms:
  - claude
  - opencode
  - copilot
  - cursor
custom_packs_dir: .argus/packs/   # optional: project-local custom packs
```

Versioning model: always-latest. `pip install --upgrade argus` is the update path. No pinning in V1.

---

## 6. V1 Pack Catalog

Five packs ship in V1. Each is grounded in a cited industry standard.

### `atomic-commit`
**Category:** workflow
**Covers:** atomic commit discipline + conventional commits format (folded in — users want both or neither)
**Authority:** Wikipedia atomic commit definition; conventionalcommits.org open spec; Smithery atomic-commit skill ecosystem precedent
**Key rule:** "If your commit message requires the word 'also', that is a second commit."
**Conventional format:** `type(scope): description` — `feat`, `fix`, `test`, `refactor`, `docs`, `chore`

### `tdd`
**Category:** workflow
**Requires:** `atomic-commit`
**Authority:** TDD Guard (production enforcement tool); extensive AI-agent TDD literature (2025–2026)
**Key rule:** "An agent must never write or modify production code before there exists at least one failing test."
**Cycle:** STOP → RED → GREEN → COMMIT → REFACTOR → COMMIT
**Coverage threshold:** 80% unit test coverage minimum; 100% for critical paths. Integration/E2E tests do not count toward coverage.

### `solid`
**Category:** architecture
**Authority:** Industry-standard SOLID literature; violation patterns are mechanically detectable
**Violation quick-reference (the core of this pack's instructions):**

| Violation | Principle | Fix |
|---|---|---|
| God class (300+ lines, 10+ methods) | SRP | Extract focused classes |
| `switch`/`match` on type | OCP | Strategy pattern or polymorphism |
| Subclass throws `UnsupportedOperationException` | LSP | Rework abstraction hierarchy |
| Interface with stub methods | ISP | Split into focused interfaces |
| `new ConcreteClass()` inside a class | DIP | Constructor injection with interface |
| Method name contains "And" | SRP | Split into separate methods |
| Class imports 10+ packages | SRP | Extract responsibilities |

### `code-quality`
**Category:** quality
**Authority:** NIST cyclomatic complexity standard (≤10); NASA mandate (<10 for mission-critical); industry size metrics
**Key metrics:**
- Cyclomatic complexity ≤ 10 per method (NIST; NASA mandates < 10 for mission-critical software)
- Method length ≤ 20 lines (excluding blank lines and comments)
- Class length ≤ 300 lines (class body only; imports/package declarations excluded)
- Maximum 5 parameters per method (use parameter objects beyond this)
- No duplicated code (DRY)

### `pre-commit`
**Category:** process
**Requires:** `tdd`, `atomic-commit`, `solid`, `code-quality`
**Role:** Orchestrating gate — references all other packs and provides the unified pre-commit checklist. This is the pack that ties enforcement together. Without it, individual packs don't reinforce each other.

---

## 7. V1 Platform Adapters

Four adapters ship in V1. All generate `AGENTS.md` as universal baseline.

| Adapter | `platform_id` | Generates |
|---|---|---|
| Claude Code | `claude` | `AGENTS.md`, `CLAUDE.md`, `.claude/rules/`, `.claude/skills/` |
| OpenCode | `opencode` | `AGENTS.md`, `opencode.json`, `.opencode/commands/`, `.opencode/skills/` |
| GitHub Copilot | `copilot` | `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/` |
| Cursor | `cursor` | `AGENTS.md`, `.cursor/rules/` |

**Pack file usage per adapter:**

| Adapter | `instructions.md` | `checklist.md` | `examples.md` |
|---|---|---|---|
| `claude` | ✓ | ✓ | ✓ |
| `opencode` | ✓ | ✓ | — |
| `copilot` | ✓ | — | — |
| `cursor` | ✓ | — | — |

Copilot and Cursor receive instructions only — injecting checklists into passive always-on context creates noise. Claude Code and OpenCode have interactive agent loops that can act on checklists.

**Deferred to V2:** `windsurf`, `aider`, `cline`. Language packs (Java, Kotlin, Python, TypeScript, Go) deferred — require language detection logic not in V1 scope.

---

## 8. CLI Surface

```
argus init                     # Interactive: scaffold .argus.yml in current directory
argus generate                 # Read .argus.yml → write all platform files
argus generate --dry-run       # Preview output without writing any files
argus generate --check         # Exit non-zero if any file would change (CI gate)
argus packs list               # Show all available packs with descriptions
argus packs show <name>        # Print a pack's instructions.md to stdout
argus platforms list           # Show all available platform adapters
argus validate                 # Verify .argus.yml: packs exist, platforms exist, no conflicts
```

Built with `click` — the standard for Python CLIs (Flask, Black, Poetry, dbt all use it).

### CI Integration

```yaml
# .github/workflows/standards.yml
- name: Verify argus standards are up to date
  run: argus generate --check
```

This enforces "generated files must be committed and current" — the same pattern as `prettier --check` and `black --check`.

---

## 9. Error Handling

Three categories, each handled explicitly:

**User errors** — fail fast, specific actionable message, no stack trace:
```
✗ Unknown pack: "tdd-enforcement"
  Available packs: atomic-commit, tdd, solid, code-quality, pre-commit
  Did you mean: tdd?
```

**Generation errors** — report exactly what failed, stop immediately:
```
✗ Failed to write .github/copilot-instructions.md
  Permission denied — check directory permissions and try again.
```

**Adapter collisions** — hard error, never silent:
```
✗ Adapter conflict: platform "claude" registered by both:
    argus (built-in)
    argus-adapter-claude-enterprise==1.2.0
  Uninstall one before running generate.
```

All failures exit with a non-zero code. `--check` mode exits non-zero if any file would change.

---

## 10. Testing Strategy

Three layers matching the three things that can break independently:

**Pack schema tests** — validate every pack has required files in correct format. Runs on every `packs/` change. No adapters involved, very fast.

**Adapter unit tests** — given stub `Pack` objects, assert correct files with correct paths and content structure. No filesystem writes, fully isolated. Verifies the `BaseAdapter` contract is satisfied.

**Integration tests** — run `argus generate` against a real `tmp_path`, assert output files exist and contain expected pack content. No mocking of the filesystem. This catches adapter + loader + CLI wiring failures. Mocking the filesystem here would repeat the exact mistake TDD Guard's critics identified: tests that pass but don't reflect real behavior.

---

## 11. Scope Boundaries

**In V1:**
- 5 core packs (`atomic-commit`, `tdd`, `solid`, `code-quality`, `pre-commit`)
- 4 platform adapters (`claude`, `opencode`, `copilot`, `cursor`)
- Full CLI surface (`init`, `generate`, `generate --dry-run`, `generate --check`, `packs list`, `packs show`, `platforms list`, `validate`)
- Entry point adapter discovery (ecosystem-ready from day one)
- Two-level pack search path (built-in + project-local custom override)
- Generated file headers
- Adapter collision detection (hard error)
- Three-layer test suite

**Explicitly out of V1:**
- Language packs (Java, Kotlin, Python, TypeScript, Go) — require language detection
- Remote pack registry — V2
- `windsurf`, `aider`, `cline` adapters — V2
- Pack-level rule configuration (ESLint-style) — V2
- Version pinning — always-latest in V1
- Git hooks installation — not argus's job (use pre-commit or husky)
- Running linters or static analysis — not argus's job
- Validating that the AI actually followed the standards — argus injects rules; the agent enforces them

---

## 12. Relationship to engineering-standards Project

The existing `engineering-standards` project (`/media/peter/Linux_AppData/AIProjects/engineering-standards`) is the inspiration and source of domain knowledge for argus packs. Pack content in argus is independently authored, informed by but not copied from engineering-standards. The engineering-standards project's distribution manifest (`standards-package.json`) and platform directories (`.claude/`, `.opencode/`, `.cursor/`) validate that the adapter model is implementable — they are a hand-coded proof of concept that argus automates.

The two projects remain independent in V1. Migration of engineering-standards consumers to argus is a future decision.

---

## 13. Key Design Decisions Log

| Decision | Rationale |
|---|---|
| Python CLI over Node or Rust | Widest contributor base for dev tooling; `click` ecosystem; installable via `pip` alongside existing dev tools |
| Always-latest (no pinning) | Reduces config complexity in V1; pinning is a V2 concern once the pack schema stabilizes |
| EditorConfig-style distribution | Canonical source in repo + CLI generator; standards travel with the project; proven pattern |
| Composable packs approach | Platform-agnostic content, platform-specific delivery; maps to mental model users already have from Superpowers |
| `atomic-commit` over `microcommit` | Industry-standard Wikipedia term; Smithery uses it; ecosystem consistency matters |
| `conventional-commits` folded into `atomic-commit` | Users want both or neither; separate packs for tightly coupled concerns creates unnecessary config friction |
| `AGENTS.md` as universal baseline | Open standard adopted by 30+ tools (Anthropic, late 2025); every adapter generates it |
| Entry point adapter discovery | Same mechanism as pytest plugins; enables community `argus-adapter-*` packages without touching core |
| Hard error on adapter collision | Silent last-one-wins is a maintenance hazard; explicit error forces deliberate resolution |
| No filesystem mocking in integration tests | Avoids the trap TDD Guard critics identified — tests that pass but don't reflect real filesystem behavior |
