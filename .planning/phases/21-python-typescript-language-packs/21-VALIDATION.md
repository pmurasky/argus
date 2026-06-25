---
phase: 21
slug: python-typescript-language-packs
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-24
---

# Phase 21 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest tests/integration/test_generate.py -x -q` |
| **Full suite command** | `uv run pytest -x -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest tests/integration/test_generate.py -x -q`
- **After every plan wave:** Run `uv run pytest -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 21-01-01 | 01 | 1 | python-pack | integration | `uv run pytest tests/integration/test_generate.py -k python -x -q` | ❌ W0 | ⬜ pending |
| 21-01-02 | 01 | 1 | typescript-pack | integration | `uv run pytest tests/integration/test_generate.py -k typescript -x -q` | ❌ W0 | ⬜ pending |
| 21-02-01 | 02 | 2 | python-tests | integration | `uv run pytest tests/integration/test_generate.py -k python -x -q` | ❌ W0 | ⬜ pending |
| 21-02-02 | 02 | 2 | typescript-tests | integration | `uv run pytest tests/integration/test_generate.py -k typescript -x -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/integration/test_generate.py` — add PYTHON_CONFIG and TYPESCRIPT_CONFIG test stubs (3 tests each: list, show, generate)

*Existing infrastructure covers all other phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Pack content quality | python/typescript packs | Rule quality is subjective | Review pack rules against PEP 8, TSC strict mode docs |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
