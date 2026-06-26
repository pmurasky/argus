# Phase 24: Java Framework Packs & CLI Improvements - Research

**Researched:** 2026-06-26
**Domain:** Pack authoring (Spring/Mockito), CLI command extension, filesystem detection
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Spring pack — version target**
- Target Spring Boot 4.x / Spring 7 (Jakarta EE 11 era, virtual threads baseline)
- Do NOT include Spring Boot 2.x/3.x compatibility notes — pack is forward-looking

**Spring pack — module scope**
- Cover the core trio: Web MVC + Data JPA + REST API design
- Out of scope: Spring Security, Spring Actuator
- In scope: IoC container guidance, `@Component`/`@Service`/`@Repository` discipline, JPA entity patterns, `@RestController` + `@RequestMapping` REST conventions

**Spring pack — testing coverage**
- Spring test slices live in the spring pack: `@SpringBootTest`, `@WebMvcTest`, `@DataJpaTest`
- Mockito pack covers only mock mechanics — no Spring-specific test annotations

**Spring pack — overlap boundary with java language pack**
- Forbidden in spring pack: null discipline, streams/optionals, checked vs unchecked exceptions
- Spring pack adds framework-layer rules that assume java pack is already active

**Spring pack — test assertion key phrase**
- `@SpringBootTest` — unique annotation, stable location in instructions.md testing section
- Isolation constant: `SPRING_CONFIG`

**Mockito pack — test runner assumption**
- Target JUnit 5 and JUnit 6 (modern entry points only; JUnit 4 is end-of-life)
- `@ExtendWith(MockitoExtension.class)` is the canonical setup pattern to document

**Mockito pack — style coverage**
- Include BDDMockito alongside classic style
- Cover all three core mechanics: `@Mock` vs `@Spy`, argument captors, `verify()` patterns
- NOT a Spring testing pack — no `@MockBean`, `@SpyBean`

**Mockito pack — overlap boundary with java language pack**
- Forbidden in mockito pack: language-level assertions, JUnit lifecycle annotations unrelated to mocking

**Mockito pack — test assertion key phrase**
- `ArgumentCaptor` — stable class name, unique to Mockito, lives in the argument captor section
- Isolation constant: `MOCKITO_CONFIG`

**argus upgrade — purpose and UX**
- `upgrade` is the interactive developer flow: detect drift → list out-of-date files → prompt "Regenerate now? [y/N]"
- Distinct from `generate --check` (silent CI exit gate)
- When no files are out of date: print "All generated files are up to date." and exit 0
- When files differ: list file names only, then prompt

**argus upgrade — CI mode**
- Detected via `CI` environment variable (`os.environ.get("CI")`)
- In CI mode: exit non-zero if any files differ, no prompt, no interactive output
- No `--ci` flag needed

**argus upgrade — diff presentation**
- List changed file names only (bullet list)
- No inline diff output

**argus init — platform detection markers**
- `.cursor/` directory → `cursor`
- `.github/copilot-instructions.md` file → `copilot`
- `GEMINI.md` file → `gemini`
- `.claude/` directory → `claude`
- `.opencode/` directory → `opencode`

**argus init — YAML output when platforms detected**
- Detected platforms listed first (active, uncommented)
- Undetected platforms listed below, commented out with `# ` prefix

**argus init — fallback when nothing detected**
- Fall back to current behavior: all platforms listed uncommented, no detection output message

### Claude's Discretion
- Exact wording of `argus upgrade` prompt text and output formatting
- Spring pack IoC container section structure and ordering
- Mockito pack BDDMockito example code style
- Whether `pack.yml` for spring and mockito includes a `requires:` field pointing to the java pack

### Deferred Ideas (OUT OF SCOPE)
- Spring Security pack
- Spring Actuator coverage
- `argus init` interactive wizard
- `--ci` flag for `argus upgrade`
</user_constraints>

---

## Summary

Phase 24 has three distinct work streams that share no technical risk:

1. **Two new framework packs** (`spring`, `mockito`) — pure content authoring following the established `argus/packs/fastapi/` template. The filesystem layout, loader auto-discovery, and integration test pattern are fully mechanical and low-risk. The only authoring decisions are content scope (locked) and whether to add a `requires:` field (Claude's discretion).

2. **`argus upgrade` command** — a new `@main.command()` in `argus/cli.py` that reuses the `generate` command's file-diff logic. The key behavioral split is: interactive (human) mode prompts; CI mode (env var `CI`) exits non-zero silently. Click's `CliRunner` can test both paths cleanly.

3. **`argus init` platform detection** — a filesystem marker scan that runs before `yaml.dump()` in the existing `init` command. The YAML output shape (detected first uncommented, undetected commented) requires custom YAML serialization since `yaml.dump()` does not support inline comments natively.

**Primary recommendation:** Implement in three atomic waves: (1) spring pack, (2) mockito pack, (3) upgrade + init detection. Each wave can be planned and committed independently.

---

## Standard Stack

### Core (all already present in project)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| click | installed | CLI commands, prompts, env var reading | Already used; `click.confirm()` handles interactive prompt; `CliRunner` handles test isolation |
| PyYAML | installed | YAML read/write for `.argus.yml` | Already used in `argus/cli.py` and `argus/config.py` |
| pytest | installed | Test framework | Project standard; `.venv/bin/pytest` confirmed |
| pytest-cov | installed | Coverage measurement | Confirmed working — 94.54% reported on unit tests |

### No New Dependencies Needed
All required libraries are already installed. This phase adds no new packages.

---

## Architecture Patterns

### Recommended Project Structure (new files only)
```
argus/packs/
├── spring/
│   ├── pack.yml          # category: framework, requires: []
│   └── instructions.md   # Spring Boot 4.x / Spring 7 content
└── mockito/
    ├── pack.yml          # category: framework, requires: []
    └── instructions.md   # Mockito 5.x content

tests/integration/
└── test_generate.py      # Extend — add SPRING_CONFIG and MOCKITO_CONFIG blocks

tests/
└── test_cli.py           # Extend — add upgrade and init detection tests
```

### Pattern 1: Pack File Layout (established, fully mechanical)
**What:** Two files per pack — `pack.yml` for metadata, `instructions.md` for content.
**When to use:** Every new pack.
**Example:**
```yaml
# argus/packs/spring/pack.yml
name: spring
description: Spring Boot 4.x IoC container, JPA patterns, and REST API design
category: framework
requires: []
platforms: [all]
```

The `requires:` field is available in `pack.yml` (per the fastapi template which has `requires: []`) but currently unused by the loader. If `requires:` is populated with `[java]`, the loader ignores it silently — it is documentation only unless the loader is extended. **Recommendation:** Include `requires: [java]` as documentation intent; do not extend the loader to enforce it (out of scope).

### Pattern 2: Integration Test Isolation Constants (established, mechanical)
**What:** Each pack gets its own `XXX_CONFIG` string constant for test isolation. Three tests per pack following existing pattern.
**When to use:** Every new pack integration test block.
**Example:**
```python
SPRING_CONFIG = """\
packs:
  - spring
platforms:
  - claude
"""

def test_spring_pack_appears_in_packs_list():
    """Given packs list is invoked, spring appears in the output."""
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "spring" in result.output

def test_spring_pack_show_renders_content():
    """Given packs show spring is invoked, @SpringBootTest appears in the output."""
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "show", "spring"])
    assert result.exit_code == 0
    assert "@SpringBootTest" in result.output

def test_spring_pack_generate_injects_content(tmp_path):
    """Given a spring+claude config, generate writes content to .claude/rules/spring.md."""
    (tmp_path / ".argus.yml").write_text(SPRING_CONFIG)
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "@SpringBootTest" in (tmp_path / ".claude/rules/spring.md").read_text()
```

### Pattern 3: `argus upgrade` Command
**What:** New `@main.command()` that computes the same file diff as `generate --check`, then branches on CI env var.
**When to use:** Interactive developer experience; CI-safe (same behavior as `--check` when `CI` is set).
**Example structure:**
```python
@main.command()
@click.option("--project-root", default=".", type=click.Path(path_type=Path))
def upgrade(project_root: Path) -> None:
    """Detect out-of-date generated files and offer to regenerate."""
    # 1. Load config, run generator to get expected files
    # 2. Compute changed list (same logic as generate --check)
    # 3. If no changes: print success, exit 0
    # 4. If CI env var set: list changed files to stderr, sys.exit(1)
    # 5. Interactive: list changed files, click.confirm("Regenerate now?"), write if yes
```

Key: The file-diff logic in `generate --check` (lines 49-57 of cli.py) is not extracted into a helper — it is inlined. For `upgrade`, extract it to a private helper `_compute_changed_files(files, project_root)` to avoid duplication.

### Pattern 4: `argus init` Platform Detection
**What:** Scan `project_root` for marker files/directories before writing `.argus.yml`.
**When to use:** Within the existing `init` command body, before the `yaml.dump()` call.

The challenge: `yaml.dump()` does not emit inline comments. The required output format — detected platforms uncommented, undetected commented — requires manual YAML construction (string building), not `yaml.dump()`.

**Example approach:**
```python
def _detect_platforms(project_root: Path) -> list[str]:
    """Return platform IDs whose marker artifacts exist in project_root."""
    markers = {
        "claude":   lambda r: (r / ".claude").is_dir(),
        "cursor":   lambda r: (r / ".cursor").is_dir(),
        "copilot":  lambda r: (r / ".github/copilot-instructions.md").is_file(),
        "gemini":   lambda r: (r / "GEMINI.md").is_file(),
        "opencode": lambda r: (r / ".opencode").is_dir(),
    }
    return [name for name, check in markers.items() if check(project_root)]

def _build_init_yaml(packs: list[str], detected: list[str], all_platforms: list[str]) -> str:
    """Build .argus.yml content with detected platforms active, others commented."""
    lines = ["packs:"]
    for p in packs:
        lines.append(f"  - {p}")
    lines.append("platforms:")
    for p in detected:
        lines.append(f"  - {p}")
    for p in all_platforms:
        if p not in detected:
            lines.append(f"  # - {p}")
    return "\n".join(lines) + "\n"
```

**Fallback (nothing detected):** `detected` is empty → all platforms added uncommented → same behavior as current `yaml.dump(config)` output.

### Anti-Patterns to Avoid
- **Modifying `generate --check` to share code with `upgrade` inline:** Extract the diff logic first into a private function, then both commands call it.
- **Using `yaml.dump()` for the commented-platform YAML:** `yaml.dump()` strips comments. Build the init YAML as a string when detection is active.
- **Asserting on Spring-specific annotations in Mockito pack tests:** Key phrases must be strictly pack-specific. `ArgumentCaptor` for mockito; `@SpringBootTest` for spring.
- **Adding Spring Security or `@MockBean` content:** Out of scope per locked decisions.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Interactive y/N prompt in upgrade | Custom input() loop | `click.confirm("Regenerate now?", default=False)` | Handles TTY detection, default, Ctrl-C; integrates with CliRunner for tests |
| Reading CI environment variable | `os.environ["CI"]` with KeyError risk | `os.environ.get("CI")` | Returns None (falsy) when unset; no exception |
| Testing upgrade in CI mode | Complex subprocess | `CliRunner.invoke()` with `env={"CI": "true"}` | Click's test runner passes env dict per invocation |
| Pack auto-discovery | Manual pack registration | Drop files in `argus/packs/spring/` and `argus/packs/mockito/` | `argus/loader.py` auto-discovers all subdirectories |

---

## Common Pitfalls

### Pitfall 1: YAML Comments Stripped by PyYAML
**What goes wrong:** Developer writes `yaml.dump(config)` for init output, commented-out platforms disappear.
**Why it happens:** YAML spec allows comments; PyYAML's dump does not preserve or emit them.
**How to avoid:** Build the `.argus.yml` string manually for the detection path. The fallback (nothing detected) can still use `yaml.dump()` since all platforms are active and no comments needed.
**Warning signs:** Integration test for commented platforms fails because the file contains no `# -` lines.

### Pitfall 2: Spring Content Duplicating java Pack
**What goes wrong:** Spring pack instructions.md contains null discipline, Optional rules, or exception handling guidance already in the java pack.
**Why it happens:** Natural tendency to make the pack "complete."
**How to avoid:** Read `argus/packs/java/instructions.md` before drafting spring content. Forbidden topics per CONTEXT.md: null discipline, streams/optionals, checked vs unchecked exceptions.
**Warning signs:** Text search for "Optional", "null", "checked exception" in spring/instructions.md returns results.

### Pitfall 3: Mockito Pack Including Spring Test Annotations
**What goes wrong:** `@MockBean`, `@SpyBean` appear in mockito pack (they are Spring-Mockito integration, not pure Mockito).
**Why it happens:** They use Mockito internally and are commonly taught alongside it.
**How to avoid:** Mockito pack scope = mock mechanics only. Spring-specific test annotations live in spring pack. Check mockito/instructions.md for any `@MockBean` or `@SpyBean` text.
**Warning signs:** Text search for "MockBean" or "SpyBean" in mockito/instructions.md returns results.

### Pitfall 4: `upgrade` Not Handling Missing `.argus.yml`
**What goes wrong:** `upgrade` with no config crashes with unhandled exception instead of clean error message.
**Why it happens:** Copy-pasting generate logic without the early-exit guard.
**How to avoid:** Include the `if not config_path.exists()` guard (same as generate command, cli.py lines 30-33).
**Warning signs:** `test_upgrade_fails_gracefully_when_no_config` fails.

### Pitfall 5: Platform Detection Order in YAML Output
**What goes wrong:** Detected platforms appear after commented ones, or in arbitrary dict order.
**Why it happens:** Using a set for detection results loses insertion order.
**How to avoid:** Use `list` (not `set`) to accumulate detected platforms; iterate `DEFAULT_PLATFORMS` in fixed order to produce the commented section. This ensures deterministic output.

### Pitfall 6: Coverage Gate Already Met
**What goes wrong:** CLI-01 (80% coverage) is already satisfied at 94.54% on unit tests. No special "coverage gate" feature needs to be built — the gate is the existing `--cov-fail-under=80` in pytest config.
**Why it matters:** Do not build a coverage reporting command or CI artifact. The requirement is "all changed code in this phase reaches 80% coverage," not "build a coverage gate feature." Satisfy it by writing tests for every new function added in phase 24.

---

## Code Examples

### Upgrade Command Structure (unit-testable)
```python
# argus/cli.py — add after existing generate command

def _compute_changed_files(
    files: list[GeneratedFile], project_root: Path
) -> list[GeneratedFile]:
    """Return files that would change if written to project_root."""
    return [
        f for f in files
        if not (project_root / f.path).exists()
        or (project_root / f.path).read_text() != f.content
    ]


@main.command()
@click.option("--project-root", default=".", type=click.Path(path_type=Path))
def upgrade(project_root: Path) -> None:
    """Detect out-of-date generated files and offer to regenerate."""
    config_path = project_root / ".argus.yml"
    if not config_path.exists():
        click.echo(f"✗ .argus.yml not found in {project_root}. Run `argus init` first.", err=True)
        sys.exit(1)

    config = ArgusConfig.from_file(config_path)
    try:
        files = Generator().run(config, project_root)
    except (PackNotFoundError, UnknownPlatformError, AdapterConflictError) as e:
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)

    changed = _compute_changed_files(files, project_root)

    if not changed:
        click.echo("All generated files are up to date.")
        return

    for f in changed:
        click.echo(f"  • {f.path}")

    if os.environ.get("CI"):
        sys.exit(1)

    if click.confirm("Regenerate now?", default=False):
        for f in changed:
            target = project_root / f.path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f.content)
            click.echo(f"  ✓ {f.path}")
```

Note: `import os` must be added to `argus/cli.py` imports.

### Test: upgrade CI mode
```python
def test_upgrade_exits_nonzero_in_ci_when_files_differ(tmp_path):
    # Given
    _write_config(tmp_path)
    (tmp_path / "CLAUDE.md").write_text("# stale")
    output_file = GeneratedFile(path=Path("CLAUDE.md"), content="# fresh")
    runner = CliRunner()
    # When
    with patch("argus.cli.Generator", _mock_generator([output_file])):
        result = runner.invoke(main, ["upgrade", "--project-root", str(tmp_path)], env={"CI": "true"})
    # Then
    assert result.exit_code == 1
```

### Test: upgrade interactive mode prompts and writes
```python
def test_upgrade_prompts_and_writes_when_confirmed(tmp_path):
    # Given
    _write_config(tmp_path)
    output_file = GeneratedFile(path=Path("CLAUDE.md"), content="# fresh")
    runner = CliRunner()
    # When
    with patch("argus.cli.Generator", _mock_generator([output_file])):
        result = runner.invoke(
            main, ["upgrade", "--project-root", str(tmp_path)],
            input="y\n", env={}
        )
    # Then
    assert result.exit_code == 0
    assert (tmp_path / "CLAUDE.md").read_text() == "# fresh"
```

### Test: init detection
```python
def test_init_detects_claude_platform(tmp_path):
    # Given — .claude/ directory exists
    (tmp_path / ".claude").mkdir()
    runner = CliRunner()
    # When
    result = runner.invoke(main, ["init", "--project-root", str(tmp_path)])
    # Then
    content = (tmp_path / ".argus.yml").read_text()
    assert "- claude" in content          # detected, uncommented
    assert "# - cursor" in content        # not detected, commented
```

---

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| Spring Boot 2.x/3.x (javax.*) | Spring Boot 4.x / Spring 7 (jakarta.*) | All import statements use `jakarta.*` not `javax.*` in pack examples |
| JUnit 4 `@RunWith(MockitoJUnitRunner.class)` | JUnit 5/6 `@ExtendWith(MockitoExtension.class)` | Mockito pack documents only JUnit 5+ setup; JUnit 4 is end-of-life |
| Mockito 4.x | Mockito 5.x | Mockito 5 dropped JUnit 4 runner; aligns with JUnit 5/6 assumption |

**Deprecated/outdated — do not include in packs:**
- `@RunWith`: JUnit 4 runner; replaced by `@ExtendWith`
- `javax.*` imports: replaced by `jakarta.*` in Spring 7+
- Spring Boot 2.x `@SpringBootApplication` on `src/main/resources/` class path conventions: packaging changed in Boot 4.x
- Mockito `when().thenReturn()` is NOT deprecated — still valid classic style; include alongside BDDMockito

---

## Open Questions

1. **`requires: [java]` enforcement**
   - What we know: `pack.yml` has a `requires:` field; loader (`argus/loader.py`) reads it but does not enforce ordering or validation.
   - What's unclear: Whether adding `requires: [java]` to spring/pack.yml causes any runtime behavior.
   - Recommendation: Add `requires: [java]` as documentation intent. Verify the loader does not fail on a non-empty `requires:` list by inspecting `loader.py` load() method. If it ignores the field, the value is documentation-only and safe.

2. **`_compute_changed_files` extraction**
   - What we know: The diff logic currently exists inline in generate (cli.py lines 49-57). Extracting it creates a private function.
   - What's unclear: Whether the private function should live in `cli.py` or be moved to `generator.py`.
   - Recommendation: Keep it in `cli.py` as a module-level private function — it is CLI presentation logic, not generator logic.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (installed in .venv) |
| Config file | pyproject.toml (or setup.cfg — existing project configuration) |
| Quick run command | `.venv/bin/pytest tests/ --ignore=tests/integration -q` |
| Full suite command | `.venv/bin/pytest tests/ -q` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FWRK-03 | spring pack in packs list | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_spring_pack_appears_in_packs_list` | ❌ Wave 1 |
| FWRK-03 | spring pack show renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_spring_pack_show_renders_content` | ❌ Wave 1 |
| FWRK-03 | spring pack generate injects content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_spring_pack_generate_injects_content` | ❌ Wave 1 |
| FWRK-04 | mockito pack in packs list | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_mockito_pack_appears_in_packs_list` | ❌ Wave 2 |
| FWRK-04 | mockito pack show renders content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_mockito_pack_show_renders_content` | ❌ Wave 2 |
| FWRK-04 | mockito pack generate injects content | integration | `.venv/bin/pytest tests/integration/test_generate.py::test_mockito_pack_generate_injects_content` | ❌ Wave 2 |
| CLI-02 | upgrade exits 0 when files current | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_exits_zero_when_files_current` | ❌ Wave 3 |
| CLI-02 | upgrade lists changed files | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_lists_changed_file_names` | ❌ Wave 3 |
| CLI-02 | upgrade CI mode exits nonzero | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_exits_nonzero_in_ci_when_files_differ` | ❌ Wave 3 |
| CLI-02 | upgrade interactive prompts and writes | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_prompts_and_writes_when_confirmed` | ❌ Wave 3 |
| CLI-02 | upgrade interactive declines leaves files | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_does_not_write_when_declined` | ❌ Wave 3 |
| CLI-02 | upgrade fails gracefully with no config | unit | `.venv/bin/pytest tests/test_cli.py::test_upgrade_fails_gracefully_when_no_config` | ❌ Wave 3 |
| CLI-03 | init detects claude platform | unit | `.venv/bin/pytest tests/test_cli.py::test_init_detects_claude_platform` | ❌ Wave 3 |
| CLI-03 | init detects cursor platform | unit | `.venv/bin/pytest tests/test_cli.py::test_init_detects_cursor_platform` | ❌ Wave 3 |
| CLI-03 | init detects copilot platform | unit | `.venv/bin/pytest tests/test_cli.py::test_init_detects_copilot_platform` | ❌ Wave 3 |
| CLI-03 | init comments undetected platforms | unit | `.venv/bin/pytest tests/test_cli.py::test_init_comments_undetected_platforms` | ❌ Wave 3 |
| CLI-03 | init fallback when nothing detected | unit | `.venv/bin/pytest tests/test_cli.py::test_init_fallback_when_no_platforms_detected` | ❌ Wave 3 |
| CLI-01 | 80% coverage on changed modules | coverage | `.venv/bin/pytest tests/ --cov=argus --cov-fail-under=80` | ✅ existing |

### Sampling Rate
- **Per task commit:** `.venv/bin/pytest tests/ --ignore=tests/integration -q`
- **Per wave merge:** `.venv/bin/pytest tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
None — existing test infrastructure covers all phase requirements. No new framework installs or conftest files needed. All new tests extend existing files (`tests/integration/test_generate.py`, `tests/test_cli.py`).

---

## Sources

### Primary (HIGH confidence)
- Direct code inspection: `argus/cli.py` — complete CLI command structure
- Direct code inspection: `argus/packs/fastapi/pack.yml`, `argus/packs/fastapi/instructions.md` — pack template
- Direct code inspection: `argus/packs/java/instructions.md` — overlap boundary enforcement
- Direct code inspection: `tests/integration/test_generate.py` — 3-assertion integration test pattern (9 prior pack examples)
- Direct code inspection: `tests/test_cli.py` — unit test patterns with `patch("argus.cli.Generator")`
- Direct code inspection: `.planning/phases/24-java-framework-packs-cli-improvements/24-CONTEXT.md` — all locked decisions

### Secondary (MEDIUM confidence)
- Click documentation: `click.confirm()` API, `CliRunner(env=...)` parameter for env injection
- PyYAML behavior: dump() strips comments (well-established library behavior)

### Tertiary (LOW confidence — not needed; all research derived from codebase)
None required.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries are already installed and in use; no new dependencies
- Architecture patterns: HIGH — derived directly from 9 prior pack implementations and existing CLI code
- Pitfalls: HIGH — derived from codebase inspection and locked CONTEXT.md decisions
- Pack content (Spring/Mockito): MEDIUM — domain knowledge of Spring Boot 4.x/Spring 7 APIs (forward-looking; Spring Boot 4 not yet GA as of knowledge cutoff, but decisions are locked)

**Research date:** 2026-06-26
**Valid until:** 2026-07-26 (stable domain; pack content is authoritative by decision)
