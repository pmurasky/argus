# Phase 20: Security Pack - Context

**Gathered:** 2026-06-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Author a new `security` pack that AI coding agents read as rules during development. The pack
injects OWASP-aligned coding discipline and input validation rules into all agent instruction
files via `argus generate`. This covers what developers control while writing code — not
infrastructure, config management, or dependency auditing.

Out of scope: broadening to other OWASP categories that are infra/ops concerns (A05 Security
Misconfiguration, A06 Vulnerable Components, A09 Logging Failures, A10 SSRF), adding language-
specific frameworks, or modifying any existing packs.

</domain>

<decisions>
## Implementation Decisions

### OWASP coverage scope
- Cover the coding-relevant subset of OWASP Top 10 (2021): A03 Injection, A02 Cryptographic
  Failures, A01 Broken Access Control, A07 Identification and Authentication Failures,
  A04 Insecure Design, A08 Software and Data Integrity Failures
- Omit infrastructure/config categories (A05, A06, A09, A10) — these don't belong in a
  code-writing rules file
- Structure with one `##` section per OWASP category, each containing 3–5 concrete rules

### Input validation
- Input validation gets its own top-level `## Input Validation` section — it's broad
  enough to deserve standalone treatment (not buried under A03 Injection)
- Rules should be concrete patterns, not principles: "Use allowlists, not blocklists",
  "Validate type, length, and format before any processing", "Reject input that doesn't
  conform — never sanitize-and-proceed", "Validate at every system boundary"
- Matches the prescriptive style of error-handling.md ("catch only at system boundaries")

### Examples content
- Secure vs. insecure side-by-side in examples.md — shows the vulnerability and the fix
  next to each other so the "why" is obvious
- Python language for all examples — consistent with the project, matches other packs
- One example per major OWASP category and one for input validation

### Red flags section
- Single flat "Red Flags — Stop and Correct" table at the end of instructions.md
- Language-agnostic patterns detectable by code review:
  - User input used in SQL query without parameterization
  - User input passed to a shell command
  - Hardcoded secret or credential in source code
  - Missing input validation before database write or external API call
  - Symmetric encryption key stored in the same codebase as the ciphertext
  - Authentication check bypassed with a flag or commented out
- Matches the style of error-handling.md and type-safety.md exactly

### Pack metadata
- `name: security`
- `category: quality` (same as error-handling, type-safety, code-quality)
- `platforms: [all]`
- No `requires:` dependencies (standalone pack)

### Claude's Discretion
- Exact wording of each rule within the per-category sections
- Number of checklist items (target: 8–12, matching other quality packs)
- Which specific Python patterns to use in examples (as long as they illustrate the rule clearly)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — PACK-01 requirement definition (OWASP Top 10 + input validation)

### Pack format
- `argus/packs/tdd/pack.yml` — pack.yml format reference (name, description, category, requires, platforms)
- `argus/packs/tdd/instructions.md` — instructions.md format gold standard
- `argus/packs/error-handling/instructions.md` — per-category section structure to replicate
- `argus/packs/error-handling/checklist.md` — checklist format and depth to match

### Test pattern
- `tests/integration/test_generate.py` — existing integration test; new security pack tests must
  follow the same 3-assertion pattern (packs list / packs show / generate injects key phrase)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tests/integration/test_generate.py` — 3-test pattern (list + show + generate) used for every
  new pack; security pack tests slot in the same file
- `argus/packs/error-handling/` — closest structural match to what security pack will look like

### Established Patterns
- All quality packs use `category: quality` in pack.yml — security pack should too
- Pack directory auto-discovered by loader: place files in `argus/packs/security/`
- Test runner is `.venv/bin/pytest` (not bare `pytest`)

### Integration Points
- New pack directory `argus/packs/security/` is auto-picked up by the pack loader — no loader
  changes needed
- Integration tests live in `tests/integration/test_generate.py` — add alongside existing tests

</code_context>

<specifics>
## Specific Ideas

- Red flags should be grep-verifiable patterns, not subjective judgements — same bar as other packs
- The instructions.md should feel like the OWASP cheat sheets distilled into agent-readable rules
- Side-by-side examples in examples.md should show the VULNERABLE code first, then the SECURE fix

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 20-security-pack*
*Context gathered: 2026-06-24*
