# Phase 20: Security Pack - Research

**Researched:** 2026-06-24
**Domain:** OWASP-aligned security rules pack for AI coding agents
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**OWASP coverage scope:**
- Cover the coding-relevant subset of OWASP Top 10 (2021): A03 Injection, A02 Cryptographic Failures, A01 Broken Access Control, A07 Identification and Authentication Failures, A04 Insecure Design, A08 Software and Data Integrity Failures
- Omit infrastructure/config categories (A05, A06, A09, A10) — these don't belong in a code-writing rules file
- Structure with one `##` section per OWASP category, each containing 3–5 concrete rules

**Input validation:**
- Input validation gets its own top-level `## Input Validation` section — it's broad enough to deserve standalone treatment (not buried under A03 Injection)
- Rules must be concrete patterns, not principles: "Use allowlists, not blocklists", "Validate type, length, and format before any processing", "Reject input that doesn't conform — never sanitize-and-proceed", "Validate at every system boundary"
- Matches the prescriptive style of error-handling.md ("catch only at system boundaries")

**Examples content:**
- Secure vs. insecure side-by-side in examples.md — shows the vulnerability and the fix next to each other so the "why" is obvious
- Python language for all examples — consistent with the project, matches other packs
- One example per major OWASP category and one for input validation

**Red flags section:**
- Single flat "Red Flags — Stop and Correct" table at the end of instructions.md
- Language-agnostic patterns detectable by code review:
  - User input used in SQL query without parameterization
  - User input passed to a shell command
  - Hardcoded secret or credential in source code
  - Missing input validation before database write or external API call
  - Symmetric encryption key stored in the same codebase as the ciphertext
  - Authentication check bypassed with a flag or commented out
- Matches the style of error-handling.md and type-safety.md exactly

**Pack metadata:**
- `name: security`
- `category: quality` (same as error-handling, type-safety, code-quality)
- `platforms: [all]`
- No `requires:` dependencies (standalone pack)

### Claude's Discretion
- Exact wording of each rule within the per-category sections
- Number of checklist items (target: 8–12, matching other quality packs)
- Which specific Python patterns to use in examples (as long as they illustrate the rule clearly)

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

---

## Summary

This phase authors a new `security` pack — four files in `argus/packs/security/` — that follows the exact same structure as the `error-handling` and `documentation-standards` packs. The pack is auto-discovered by the existing loader; no loader or CLI changes are required. The only moving parts are: the four pack files, three new integration tests in the existing `tests/integration/test_generate.py`, and a TDD cycle that keeps tests red before implementation.

The OWASP Top 10 has a 2025 edition in addition to the 2021 edition. The user's CONTEXT.md locks the 2021 numbering (A01–A08 as specified). The ranking shifts between 2021 and 2025 (e.g., Injection drops from #3 to #5; Insecure Design drops from #4 to #6) are irrelevant here because the phase is constrained to the 2021 list. The substance of each category's coding rules is stable across both editions — the content that belongs in agent instructions has not changed.

The security pack is entirely content work plus tests. There is no new Python code to write beyond the pack files themselves. The implementation risk is low: the loader, generator, and all CLI commands are already working correctly for quality-category packs.

**Primary recommendation:** Author four files (`pack.yml`, `instructions.md`, `checklist.md`, `examples.md`) under `argus/packs/security/`, following `error-handling/` as the structural gold standard. Write the three integration tests first (TDD: they will fail until the pack directory exists), then create the pack files.

---

## Standard Stack

### Core
| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| Pack directory convention | N/A | `argus/packs/security/` — auto-discovered by loader | All packs use this; no loader changes needed |
| `pack.yml` | N/A | Pack metadata: name, description, category, requires, platforms | Required by loader; format identical to `error-handling/pack.yml` |
| `instructions.md` | N/A | Agent-readable rules, one `##` section per OWASP category | Format defined by `error-handling/instructions.md` |
| `checklist.md` | N/A | Flat `- [ ]` checklist, 8–12 items | Format defined by `error-handling/checklist.md` |
| `examples.md` | N/A | Side-by-side vulnerable/secure Python code blocks | Format defined by `error-handling/examples.md` |

### Testing
| Component | Details | Purpose |
|-----------|---------|---------|
| `tests/integration/test_generate.py` | Existing file — append new tests | 3-test pattern: list / show / generate |
| `.venv/bin/pytest` | Not bare `pytest` | Correct test runner for this project |
| `SECURITY_CONFIG` constant | Isolated config (follows `TYPE_SAFETY_CONFIG` precedent) | Prevents cross-test pollution |

### No installation required
All dependencies are already present. This phase creates text files and appends tests to an existing file.

---

## Architecture Patterns

### Recommended Pack Structure
```
argus/packs/security/
├── pack.yml         # metadata: name, category, platforms
├── instructions.md  # rules: one H2 per OWASP category + Input Validation + Red Flags
├── checklist.md     # 8–12 checkbox items
└── examples.md      # side-by-side vulnerable/secure Python examples
```

### Pattern 1: Pack File Format (from error-handling reference)

**pack.yml:**
```yaml
name: security
description: OWASP Top 10 coding rules — injection, cryptography, access control, and input validation
category: quality
requires: []
platforms: [all]
```

**instructions.md section structure:**
```markdown
# Security

## Input Validation
- Use allowlists, not blocklists — define what is permitted, reject everything else
- Validate type, length, and format before any processing
- Reject input that does not conform — never sanitize-and-proceed
- Validate at every system boundary, including internal service calls

## A03 Injection
- Use parameterized queries or prepared statements for all database access
- Never pass user input to shell commands; use subprocess with argument lists, not shell=True
- Treat all external input as untrusted regardless of source (user, API, file, environment)

## A02 Cryptographic Failures
- Never store secrets or credentials in source code or version control
- Use a well-established library (e.g. cryptography, bcrypt) — never hand-roll crypto primitives
- Prefer asymmetric or hash-based solutions over symmetric encryption for secrets at rest
- Store encryption keys separately from the data they protect

## A01 Broken Access Control
- Enforce authorization on every request at the server side — never trust client-supplied roles or IDs
- Use deny-by-default: grant minimum permissions required, not broad access trimmed down
- Validate that the authenticated user owns the resource being accessed before returning it

## A07 Identification and Authentication Failures
- Never hardcode credentials, tokens, or API keys — use environment variables or a secrets manager
- Hash passwords with a slow algorithm (bcrypt, argon2) before storage — never store plaintext or MD5/SHA-1
- Expire and rotate session tokens; invalidate them on logout

## A04 Insecure Design
- Model threat scenarios at design time — identify trust boundaries and adversarial inputs before writing code
- Never implement security controls as optional flags or commented-out blocks
- Separate concerns: authentication, authorization, and business logic belong in distinct layers

## A08 Software and Data Integrity Failures
- Verify the integrity of external data (deserialised objects, uploaded files) before processing
- Never deserialize data from untrusted sources without schema validation
- Treat deserialization of user-supplied pickle, YAML with arbitrary tags, or XML as high-risk

## Red Flags — Stop and Correct
- User input used in SQL query without parameterization
- User input passed to a shell command (especially shell=True)
- Hardcoded secret, credential, or API key in source code
- Missing input validation before database write or external API call
- Symmetric encryption key stored in the same codebase as the ciphertext
- Authentication check bypassed with a flag or commented out
```

### Pattern 2: Integration Test Structure (3-assertion pattern)

```python
# Source: tests/integration/test_generate.py — existing pattern for type-safety, error-handling, docs-standards

SECURITY_CONFIG = """\
packs:
  - security
platforms:
  - claude
"""


def test_security_pack_appears_in_packs_list():
    """Given packs list is invoked, security appears in the output."""
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "security" in result.output


def test_security_pack_show_renders_content():
    """Given packs show security is invoked, key phrase appears in the output."""
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "show", "security"])
    assert result.exit_code == 0
    assert "parameterized" in result.output


def test_security_pack_generate_injects_content(tmp_path):
    """Given a security+claude config, generate writes content to .claude/rules/security.md."""
    (tmp_path / ".argus.yml").write_text(SECURITY_CONFIG)
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "parameterized" in (tmp_path / ".claude/rules/security.md").read_text()
```

**Key phrase selection:** "parameterized" (from "parameterized queries") — this word is distinctive, appears in instructions.md (not only in examples.md, so it survives future edits), and is a core signal of injection prevention. This follows the precedent set by "system boundaries" (error-handling) and "imperative mood" (documentation-standards).

### Pattern 3: Checklist Format

```markdown
## Security Checklist

- [ ] All database queries use parameterized statements — no string interpolation
- [ ] No user input passed to shell commands; subprocess called with argument list, not shell=True
- [ ] No hardcoded secrets, credentials, or API keys in source code
- [ ] All input validated at system boundaries (type, length, format) before processing
- [ ] Allowlist validation used — input rejected if it doesn't match expected pattern
- [ ] Passwords hashed with bcrypt or argon2 before storage
- [ ] Encryption keys stored separately from the data they protect
- [ ] Authorization checked server-side on every request — no client-supplied role trust
- [ ] Session tokens expire and are invalidated on logout
- [ ] External data (deserialised objects, uploads) validated against a schema before use
```

### Pattern 4: Examples Format (side-by-side, vulnerable first)

```markdown
## Security Examples

### Injection — SQL

**Vulnerable**
```python
query = f"SELECT * FROM users WHERE name = '{user_input}'"
db.execute(query)
```

**Secure**
```python
db.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```

### Injection — Shell

**Vulnerable**
```python
subprocess.run(f"convert {filename} output.png", shell=True)
```

**Secure**
```python
subprocess.run(["convert", filename, "output.png"])
```

### Cryptographic Failures

**Vulnerable**
```python
SECRET_KEY = "my-hardcoded-key"
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**Secure**
```python
SECRET_KEY = os.environ["SECRET_KEY"]
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Input Validation

**Vulnerable**
```python
def create_user(data: dict) -> None:
    db.insert("users", data)  # no validation
```

**Secure**
```python
def create_user(data: dict) -> None:
    if not isinstance(data.get("email"), str) or len(data["email"]) > 254:
        raise ValidationError("Invalid email")
    if not EMAIL_RE.match(data["email"]):
        raise ValidationError("Invalid email format")
    db.insert("users", data)
```
```

### Anti-Patterns to Avoid

- **Sanitize-and-proceed:** Stripping dangerous characters and using the cleaned input in a query. Use parameterization instead — sanitization is always incomplete.
- **Client-side-only validation:** Relying on frontend validation. Always re-validate at the server boundary.
- **Denylist validation:** Blocking known-bad patterns (e.g., `'; DROP TABLE`). Allowlists are the correct approach.
- **Commenting out auth:** `# if not user.is_admin: raise Forbidden()` left in production path.
- **Key/secret co-location:** Storing encryption key and encrypted data in the same file or table.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Password hashing | Custom MD5/SHA-1 hash | `bcrypt` or `argon2-cffi` | MD5/SHA-1 are fast — attackers can brute-force; slow algorithms are mandatory |
| Symmetric encryption | XOR cipher, custom AES mode | `cryptography` library (`Fernet`) | Subtle mistakes in IV reuse, padding oracles invalidate hand-rolled crypto |
| Token generation | `random` module | `secrets` module | `random` is not cryptographically secure |
| Input schema validation | Manual length/type checks in every function | `pydantic` or `marshmallow` | Consistent, tested, composable — not reimplemented per endpoint |

**Key insight:** Cryptography is the domain where custom implementations consistently fail silently. The pack rules should direct agents away from hand-rolling any cryptographic primitive.

---

## Common Pitfalls

### Pitfall 1: `shell=True` in subprocess calls
**What goes wrong:** `subprocess.run(cmd, shell=True)` where `cmd` includes user input allows command injection.
**Why it happens:** Shell-string convenience; developers treat the command as a template.
**How to avoid:** Always use a list: `subprocess.run(["convert", filename, "output.png"])`.
**Warning signs:** Any `shell=True` with a variable in the command string.

### Pitfall 2: f-string SQL queries
**What goes wrong:** `f"SELECT * FROM users WHERE id = {user_id}"` — direct interpolation bypasses the DB driver's parameterization.
**Why it happens:** F-strings are the natural Python string tool; the danger is non-obvious.
**How to avoid:** Use `?` or `%s` placeholders (depending on driver) and pass values as a tuple.
**Warning signs:** Any `f"SELECT` or `"SELECT ... " + variable`.

### Pitfall 3: Hardcoded secrets surfaced by git history
**What goes wrong:** A secret committed even once persists in git history even after removal.
**Why it happens:** Developer plans to "replace it before merging" but forgets, or rotates it later without cleaning history.
**How to avoid:** Never commit a secret value; load from `os.environ` from day one. The Red Flag rule enforces this.
**Warning signs:** Any string literal matching the shape of a token, key, or password (length, entropy).

### Pitfall 4: Authorization checked only at the route level
**What goes wrong:** Route-level auth guard bypassed by direct service/repository calls elsewhere in the codebase.
**Why it happens:** Auth check placed at the HTTP handler and assumed to be the only entry point.
**How to avoid:** Enforce authorization in the service layer, not only at the boundary layer.
**Warning signs:** Service methods that accept a user ID without verifying ownership.

### Pitfall 5: Overly broad deserialization
**What goes wrong:** `pickle.loads(user_data)` or `yaml.load(data)` (without `Loader=yaml.SafeLoader`) executes arbitrary code.
**Why it happens:** Convenience of full object reconstruction from bytes/YAML.
**How to avoid:** Use `yaml.safe_load()`. Never `pickle.loads()` on untrusted data. Validate schema explicitly.
**Warning signs:** `yaml.load(`, `pickle.loads(`, `eval(` with external input.

---

## OWASP 2021 vs 2025 — Relevance to This Phase

The CONTEXT.md locks the 2021 numbering. The 2025 edition reorganized rankings (Injection drops to #5; Insecure Design drops to #6) and renamed two categories, but the **coding rules content** for all six locked categories is substantively unchanged. The phase should use 2021 category IDs (A01–A08) as specified. The pack does not need to mention edition year — rules are stated without reference to OWASP numbering in the final text (consistent with how error-handling.md doesn't cite RFC numbers).

| 2021 ID | 2021 Name | 2025 Status | Content change for coding rules |
|---------|-----------|-------------|--------------------------------|
| A01 | Broken Access Control | Still #1 | None — SSRF merged in, but SSRF is out of scope |
| A02 | Cryptographic Failures | Now #4 | None |
| A03 | Injection | Now #5 | None |
| A04 | Insecure Design | Now #6 | None |
| A07 | Authentication Failures | Now #7 | None |
| A08 | Software/Data Integrity | Now #8 | None |

**Confidence:** HIGH — verified against owasp.org/Top10/2021/ and owasp.org/Top10/2025/.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing) |
| Config file | `pyproject.toml` (or none — inferred from project root) |
| Quick run command | `.venv/bin/pytest tests/integration/test_generate.py -x` |
| Full suite command | `.venv/bin/pytest` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PACK-01 | `security` appears in `packs list` output | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_security_pack_appears_in_packs_list -x` | Wave 0 (new) |
| PACK-01 | `packs show security` renders instructions content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_security_pack_show_renders_content -x` | Wave 0 (new) |
| PACK-01 | `generate` injects security rules into `.claude/rules/security.md` | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_security_pack_generate_injects_content -x` | Wave 0 (new) |

### Sampling Rate
- **Per task commit:** `.venv/bin/pytest tests/integration/test_generate.py -x`
- **Per wave merge:** `.venv/bin/pytest`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] Three new test functions appended to `tests/integration/test_generate.py` — covers PACK-01 (all three assertions)
- [ ] `argus/packs/security/` directory and four files — these are the production artifacts that make the tests green

*(No new framework install required — pytest and click.testing are already present)*

---

## Sources

### Primary (HIGH confidence)
- `argus/packs/error-handling/` — structural gold standard for instructions.md, checklist.md, examples.md, pack.yml
- `argus/packs/type-safety/pack.yml` — confirms `category: quality`, `requires: []` pattern
- `tests/integration/test_generate.py` — 3-assertion test pattern, isolated CONFIG constant pattern, correct test runner path
- [OWASP Top 10:2021](https://owasp.org/Top10/2021/) — category definitions and scope
- [OWASP A01:2021 Broken Access Control](https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/)
- [OWASP A02:2021 Cryptographic Failures](https://owasp.org/Top10/2021/A02_2021-Cryptographic_Failures/)
- [OWASP A03:2021 Injection](https://owasp.org/Top10/2021/A03_2021-Injection/)

### Secondary (MEDIUM confidence)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) — allowlist vs blocklist guidance, server-side requirement
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/) — confirmed 2021 content is still accurate; ranking changes don't affect rule content

### Tertiary (LOW confidence — not needed, content is locked)
- None required; all implementation decisions are locked in CONTEXT.md

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — pack format verified from existing packs in the codebase
- Architecture: HIGH — test pattern and file structure directly observed from existing source
- Pitfalls: HIGH — OWASP cheat sheets and standard Python security guidance
- OWASP content: HIGH — verified against official owasp.org documentation

**Research date:** 2026-06-24
**Valid until:** 2026-12-24 (OWASP Top 10 updates ~every 3–4 years; pack format stable)
