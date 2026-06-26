---
phase: 24-java-framework-packs-cli-improvements
plan: "03"
subsystem: cli
tags: [upgrade, init, platform-detection, drift-detection, coverage]
dependency_graph:
  requires: [24-01, 24-02]
  provides: [CLI-02, CLI-03, CLI-01]
  affects: [argus/cli.py, tests/test_cli.py]
tech_stack:
  added: []
  patterns: [strategy-via-dict, helper-extraction]
key_files:
  created: []
  modified:
    - argus/cli.py
    - tests/test_cli.py
decisions:
  - "_compute_changed_files extracted as shared helper so generate --check and upgrade stay DRY"
  - "upgrade uses sys.exit(1) in CI mode (env var CI) — no interactive prompt when CI is set"
  - "_build_init_yaml produces flat key:/indented-list YAML (not yaml.dump) for deterministic order with comments"
  - "_detect_platforms iterates DEFAULT_PLATFORMS (not dict keys) to preserve order"
metrics:
  duration: "8 min"
  completed: "2026-06-26"
  tasks_completed: 2
  files_modified: 2
---

# Phase 24 Plan 03: CLI Improvements (upgrade + init detection) Summary

**One-liner:** `argus upgrade` drift detection with CI/interactive modes + `argus init` platform auto-detection via filesystem markers, 94.67% coverage.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 RED | Add failing upgrade tests | 7995385 | tests/test_cli.py |
| 1 GREEN | Add upgrade command for drift detection | f4da980 | argus/cli.py |
| 2 RED | Add failing init platform detection tests | 6b440d5 | tests/test_cli.py |
| 2 GREEN | Detect installed platforms in argus init | 6a671b3 | argus/cli.py |

## What Was Built

### `argus upgrade` command (CLI-02)

- Computes drifted files by comparing generated content to disk
- Lists out-of-date file names (one per line)
- In CI mode (`CI` env var set): exits non-zero silently when files differ
- In interactive mode: prompts with `Regenerate now?`, writes on confirmation
- Exits 0 with "up to date" message when all files are current
- Fails gracefully with exit 1 when `.argus.yml` is missing

### `_compute_changed_files` helper

- Extracted from the existing `generate --check` inline comprehension
- Shared by both `generate --check` and `upgrade` — eliminates duplication
- Returns `list[GeneratedFile]` of files missing or differing from disk

### `argus init` platform detection (CLI-03)

- `_detect_platforms(project_root)`: checks five filesystem markers:
  - `.claude/` directory → claude
  - `.cursor/` directory → cursor
  - `.github/copilot-instructions.md` file → copilot
  - `GEMINI.md` file → gemini
  - `.opencode/` directory → opencode
- `_build_init_yaml(packs, detected)`: builds YAML with detected platforms active and undetected commented as `# - <name>`
- Silent fallback: when no markers detected, all platforms written uncommented

### Coverage gate (CLI-01)

- Full test suite: 189 tests pass at 94.67% coverage
- `--cov-fail-under=80` gate exits 0

## Tests Written

**Upgrade tests (6):**
- `test_upgrade_exits_zero_when_files_current`
- `test_upgrade_lists_changed_file_names`
- `test_upgrade_exits_nonzero_in_ci_when_files_differ`
- `test_upgrade_prompts_and_writes_when_confirmed`
- `test_upgrade_does_not_write_when_declined`
- `test_upgrade_fails_gracefully_when_no_config`

**Init detection tests (5):**
- `test_init_detects_claude_platform`
- `test_init_detects_cursor_platform`
- `test_init_detects_copilot_platform`
- `test_init_comments_undetected_platforms`
- `test_init_fallback_when_no_platforms_detected`

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED

Files exist:
- argus/cli.py: FOUND
- tests/test_cli.py: FOUND

Commits exist:
- 7995385: FOUND (RED upgrade tests)
- f4da980: FOUND (GREEN upgrade command)
- 6b440d5: FOUND (RED init detection tests)
- 6a671b3: FOUND (GREEN init detection)

All acceptance criteria verified:
- argus/cli.py contains `import os`: YES
- argus/cli.py contains `def _compute_changed_files(`: YES
- argus/cli.py contains `def upgrade(`: YES
- argus/cli.py contains `os.environ.get("CI")`: YES
- argus/cli.py contains `click.confirm("Regenerate now?"`: YES
- argus/cli.py generate --check uses `_compute_changed_files(`: YES
- argus/cli.py contains `def _detect_platforms(`: YES
- argus/cli.py contains `def _build_init_yaml(`: YES
- All 11 new tests PASS: YES
- mypy exits 0: YES
- Coverage gate (80%) passes: YES (94.67%)
