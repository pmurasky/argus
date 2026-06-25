---
phase: 22
slug: go-java-kotlin-language-packs
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-24
---

# Phase 22 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (with pytest-cov) |
| **Config file** | `pyproject.toml` `[tool.pytest.ini_options]` |
| **Quick run command** | `.venv/bin/pytest tests/integration/test_generate.py -x -q` |
| **Full suite command** | `.venv/bin/pytest` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `.venv/bin/pytest tests/integration/test_generate.py -x -q`
- **After every plan wave:** Run `.venv/bin/pytest`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 22-01-01 | 01 | 1 | LANG-03 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k go -x` | ❌ Wave 0 | ⬜ pending |
| 22-01-02 | 01 | 1 | LANG-03 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k go -x` | ❌ Wave 0 | ⬜ pending |
| 22-01-03 | 01 | 1 | LANG-03 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k go -x` | ❌ Wave 0 | ⬜ pending |
| 22-02-01 | 02 | 1 | LANG-04 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k java -x` | ❌ Wave 0 | ⬜ pending |
| 22-02-02 | 02 | 1 | LANG-04 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k java -x` | ❌ Wave 0 | ⬜ pending |
| 22-02-03 | 02 | 1 | LANG-04 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k java -x` | ❌ Wave 0 | ⬜ pending |
| 22-03-01 | 03 | 1 | LANG-05 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k kotlin -x` | ❌ Wave 0 | ⬜ pending |
| 22-03-02 | 03 | 1 | LANG-05 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k kotlin -x` | ❌ Wave 0 | ⬜ pending |
| 22-03-03 | 03 | 1 | LANG-05 | integration | `.venv/bin/pytest tests/integration/test_generate.py -k kotlin -x` | ❌ Wave 0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/integration/test_generate.py` — add `GO_CONFIG`, `JAVA_CONFIG`, `KOTLIN_CONFIG` isolation constants and 9 test functions (3 per pack)
- [ ] `argus/packs/go/pack.yml` — does not exist
- [ ] `argus/packs/go/instructions.md` — does not exist (must contain `errors.Is` verbatim)
- [ ] `argus/packs/go/checklist.md` — does not exist
- [ ] `argus/packs/go/examples.md` — does not exist
- [ ] `argus/packs/java/pack.yml` — does not exist
- [ ] `argus/packs/java/instructions.md` — does not exist (must contain `Optional.orElseThrow` verbatim)
- [ ] `argus/packs/java/checklist.md` — does not exist
- [ ] `argus/packs/java/examples.md` — does not exist
- [ ] `argus/packs/kotlin/pack.yml` — does not exist
- [ ] `argus/packs/kotlin/instructions.md` — does not exist (must contain `requireNotNull` verbatim)
- [ ] `argus/packs/kotlin/checklist.md` — does not exist
- [ ] `argus/packs/kotlin/examples.md` — does not exist

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Rule content quality and accuracy | LANG-03/04/05 | Content correctness requires human review | Run `argus packs show go/java/kotlin` and read rules for language accuracy |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
