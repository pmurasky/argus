---
phase: 20
slug: security-pack
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-24
---

# Phase 20 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (existing) |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `.venv/bin/pytest tests/integration/test_generate.py -x` |
| **Full suite command** | `.venv/bin/pytest` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `.venv/bin/pytest tests/integration/test_generate.py -x`
- **After every plan wave:** Run `.venv/bin/pytest`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 20-01-01 | 01 | 0 | PACK-01 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_security_pack_appears_in_packs_list -x` | ❌ W0 | ⬜ pending |
| 20-01-02 | 01 | 0 | PACK-01 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_security_pack_show_renders_content -x` | ❌ W0 | ⬜ pending |
| 20-01-03 | 01 | 0 | PACK-01 | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_security_pack_generate_injects_content -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/integration/test_generate.py` — append three new test functions (list, show, generate assertions for security pack)

*No new framework install required — pytest and click.testing are already present.*

---

## Manual-Only Verifications

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
