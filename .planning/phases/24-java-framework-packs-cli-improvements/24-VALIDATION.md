---
phase: 24
slug: java-framework-packs-cli-improvements
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-26
---

# Phase 24 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (installed in .venv) |
| **Config file** | pyproject.toml |
| **Quick run command** | `.venv/bin/pytest tests/ --ignore=tests/integration -q` |
| **Full suite command** | `.venv/bin/pytest tests/ -q` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `.venv/bin/pytest tests/ --ignore=tests/integration -q`
- **After every plan wave:** Run `.venv/bin/pytest tests/ -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 24-01-01 | 01 | 1 | FWRK-03 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_spring_pack_appears_in_packs_list` | ❌ Wave 1 | ⬜ pending |
| 24-01-02 | 01 | 1 | FWRK-03 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_spring_pack_show_renders_content` | ❌ Wave 1 | ⬜ pending |
| 24-01-03 | 01 | 1 | FWRK-03 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_spring_pack_generate_injects_content` | ❌ Wave 1 | ⬜ pending |
| 24-02-01 | 02 | 2 | FWRK-04 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_mockito_pack_appears_in_packs_list` | ❌ Wave 2 | ⬜ pending |
| 24-02-02 | 02 | 2 | FWRK-04 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_mockito_pack_show_renders_content` | ❌ Wave 2 | ⬜ pending |
| 24-02-03 | 02 | 2 | FWRK-04 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_mockito_pack_generate_injects_content` | ❌ Wave 2 | ⬜ pending |
| 24-03-01 | 03 | 3 | CLI-02 | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_exits_zero_when_files_current` | ❌ Wave 3 | ⬜ pending |
| 24-03-02 | 03 | 3 | CLI-02 | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_lists_changed_file_names` | ❌ Wave 3 | ⬜ pending |
| 24-03-03 | 03 | 3 | CLI-02 | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_exits_nonzero_in_ci_when_files_differ` | ❌ Wave 3 | ⬜ pending |
| 24-03-04 | 03 | 3 | CLI-02 | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_prompts_and_writes_when_confirmed` | ❌ Wave 3 | ⬜ pending |
| 24-03-05 | 03 | 3 | CLI-02 | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_does_not_write_when_declined` | ❌ Wave 3 | ⬜ pending |
| 24-03-06 | 03 | 3 | CLI-02 | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_fails_gracefully_when_no_config` | ❌ Wave 3 | ⬜ pending |
| 24-03-07 | 03 | 3 | CLI-03 | unit | `.venv/bin/pytest tests/test_cli.py::test_init_detects_claude_platform` | ❌ Wave 3 | ⬜ pending |
| 24-03-08 | 03 | 3 | CLI-03 | unit | `.venv/bin/pytest tests/test_cli.py::test_init_detects_cursor_platform` | ❌ Wave 3 | ⬜ pending |
| 24-03-09 | 03 | 3 | CLI-03 | unit | `.venv/bin/pytest tests/test_cli.py::test_init_detects_copilot_platform` | ❌ Wave 3 | ⬜ pending |
| 24-03-10 | 03 | 3 | CLI-03 | unit | `.venv/bin/pytest tests/test_cli.py::test_init_comments_undetected_platforms` | ❌ Wave 3 | ⬜ pending |
| 24-03-11 | 03 | 3 | CLI-03 | unit | `.venv/bin/pytest tests/test_cli.py::test_init_fallback_when_no_platforms_detected` | ❌ Wave 3 | ⬜ pending |
| 24-03-12 | 03 | 3 | CLI-01 | coverage | `.venv/bin/pytest tests/ --cov=argus --cov-fail-under=80` | ✅ existing | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No new framework installs or conftest files needed.

*All new tests extend existing files (`tests/integration/test_generate.py`, `tests/test_cli.py`).*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `argus upgrade` interactive prompt UX | CLI-02 | TTY interaction not fully captured by CliRunner | Run `argus upgrade` in a real terminal with a stale generated file; verify prompt appears and file is written on "y" |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
