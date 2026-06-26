---
phase: 23
slug: python-javascript-framework-packs
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-25
---

# Phase 23 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `.venv/bin/pytest tests/integration/test_generate.py -x -q` |
| **Full suite command** | `.venv/bin/pytest -x -q` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `.venv/bin/pytest tests/integration/test_generate.py -x -q`
- **After every plan wave:** Run `.venv/bin/pytest -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 23-01-01 | 01 | 1 | FWRK-01 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k fastapi -x -q` | ❌ W0 | ⬜ pending |
| 23-01-02 | 01 | 1 | FWRK-01 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k fastapi -x -q` | ❌ W0 | ⬜ pending |
| 23-02-01 | 02 | 2 | FWRK-02 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k nextjs -x -q` | ❌ W0 | ⬜ pending |
| 23-02-02 | 02 | 2 | FWRK-02 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k nextjs -x -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/integration/test_generate.py` — add `FASTAPI_CONFIG` and `NEXTJS_CONFIG` isolation constants + 3-assertion tests (packs list / packs show / generate key phrase) following PYTHON_CONFIG precedent

*Existing pytest infrastructure covers all phase requirements — no new fixtures or installs needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `argus packs list` renders "framework" category label cleanly | FWRK-01, FWRK-02 | Visual output check | Run `argus packs list` and confirm `fastapi` and `nextjs` appear under a `framework` group |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
