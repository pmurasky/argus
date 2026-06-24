---
phase: 18
slug: gemini-cli-adapter
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-23
---

# Phase 18 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | pyproject.toml |
| **Quick run command** | `pytest tests/adapters/test_gemini.py -v` |
| **Full suite command** | `pytest tests/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/adapters/test_gemini.py -v`
- **After every plan wave:** Run `pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 18-01-01 | 01 | 1 | PLT-01 | unit | `pytest tests/adapters/test_gemini.py -v` | ❌ W0 | ⬜ pending |
| 18-01-02 | 01 | 1 | PLT-01 | unit | `pytest tests/adapters/test_gemini.py -v` | ❌ W0 | ⬜ pending |
| 18-01-03 | 01 | 1 | PLT-01 | unit | `pytest tests/adapters/test_gemini.py -v` | ❌ W0 | ⬜ pending |
| 18-01-04 | 01 | 2 | PLT-01 | integration | `pytest tests/ -v` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/adapters/test_gemini.py` — stubs for PLT-01 (six unit tests mirroring test_copilot.py pattern)

*Existing pytest infrastructure covers all other phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `argus platforms list` shows `gemini` | PLT-01 | CLI output verification | Run `argus platforms list` after `pip install -e .` and confirm `gemini` appears |
| `argus generate` with `platforms: [gemini]` in `.argus.yml` creates `GEMINI.md` at project root | PLT-01 | File system output | Create test project, run generate, confirm `GEMINI.md` exists at root |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
