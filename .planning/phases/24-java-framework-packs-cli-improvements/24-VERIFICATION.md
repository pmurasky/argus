---
phase: 24-java-framework-packs-cli-improvements
verified: 2026-06-26T00:00:00Z
status: passed
score: 6/6 must-haves verified
gaps: []
human_verification:
  - test: "Run `argus upgrade` in a terminal with a stale generated file"
    expected: "Prompt appears listing stale file names; file is written after confirming 'y'"
    why_human: "Interactive prompt flow and real file write cannot be fully verified via CliRunner alone"
---

# Phase 24: Java Framework Packs & CLI Improvements Verification Report

**Phase Goal:** Ship two Java framework packs (spring, mockito) and two CLI capabilities (upgrade drift detection, init platform auto-detection)
**Verified:** 2026-06-26
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| #  | Truth                                                                                    | Status     | Evidence                                                                     |
|----|------------------------------------------------------------------------------------------|------------|------------------------------------------------------------------------------|
| 1  | User adds `spring` to .argus.yml packs and generate injects Spring Boot 4.x content     | VERIFIED   | test_spring_pack_generate_injects_content passes; spring.md written to .claude/rules/ |
| 2  | `argus packs list` includes spring                                                       | VERIFIED   | test_spring_pack_appears_in_packs_list passes; pack.yml has name: spring     |
| 3  | `argus packs show spring` displays Spring content including @SpringBootTest              | VERIFIED   | test_spring_pack_show_renders_content passes; instructions.md contains @SpringBootTest |
| 4  | User adds `mockito` to .argus.yml packs and generate injects Mockito content             | VERIFIED   | test_mockito_pack_generate_injects_content passes; mockito.md written to .claude/rules/ |
| 5  | `argus packs list` includes mockito                                                      | VERIFIED   | test_mockito_pack_appears_in_packs_list passes; pack.yml has name: mockito   |
| 6  | `argus packs show mockito` displays content including ArgumentCaptor                     | VERIFIED   | test_mockito_pack_show_renders_content passes; instructions.md contains ArgumentCaptor |
| 7  | `argus upgrade` prints success and exits 0 when generated files are current              | VERIFIED   | test_upgrade_exits_zero_when_files_current passes; "up to date" message confirmed |
| 8  | `argus upgrade` lists out-of-date file names and prompts to regenerate when files differ | VERIFIED   | test_upgrade_lists_changed_file_names + test_upgrade_prompts_and_writes_when_confirmed pass |
| 9  | `argus upgrade` exits non-zero with no prompt when CI env var is set and files differ    | VERIFIED   | test_upgrade_exits_nonzero_in_ci_when_files_differ passes; env={"CI": "true"} tested |
| 10 | `argus init` pre-selects detected platforms (uncommented) and comments out undetected    | VERIFIED   | test_init_detects_claude_platform, test_init_comments_undetected_platforms pass |
| 11 | `argus init` falls back to all-platforms-uncommented when nothing is detected            | VERIFIED   | test_init_fallback_when_no_platforms_detected passes; "# -" not in output asserted |
| 12 | All changed code in phase 24 reaches 80% coverage                                       | VERIFIED   | Full suite: 94.67% coverage, 189 tests pass, --cov-fail-under=80 exits 0    |

**Score:** 12/12 truths verified

### Required Artifacts

| Artifact                                | Expected                                                 | Status     | Details                                                       |
|-----------------------------------------|----------------------------------------------------------|------------|---------------------------------------------------------------|
| `argus/packs/spring/pack.yml`           | Spring pack metadata, category: framework                | VERIFIED   | name: spring, category: framework, requires: [java], platforms: [all] |
| `argus/packs/spring/instructions.md`   | Spring Boot 4.x IoC/JPA/REST/test-slice rules            | VERIFIED   | @SpringBootTest, @WebMvcTest, @DataJpaTest, @RestController, jakarta.persistence present; no javax overlap |
| `argus/packs/mockito/pack.yml`          | Mockito pack metadata, category: framework               | VERIFIED   | name: mockito, category: framework, requires: [java], platforms: [all] |
| `argus/packs/mockito/instructions.md`  | Mockito 5.x mock mechanics: @Mock vs @Spy, ArgumentCaptor, BDDMockito | VERIFIED | ArgumentCaptor, @ExtendWith(MockitoExtension.class), @Spy, BDDMockito all present; no @MockBean/@SpyBean |
| `argus/cli.py`                          | upgrade command, _compute_changed_files, _detect_platforms, _build_init_yaml, init wiring | VERIFIED | All four functions present and wired; import os present; generate --check uses _compute_changed_files |
| `tests/integration/test_generate.py`  | 3 spring + 3 mockito integration tests + config constants | VERIFIED   | SPRING_CONFIG, MOCKITO_CONFIG, all 6 test functions present and substantive |
| `tests/test_cli.py`                     | 6 upgrade unit tests + 5 init detection unit tests        | VERIFIED   | All 11 test functions present with full Given/When/Then assertions |

### Key Link Verification

| From                                  | To                                              | Via                                               | Status   | Details                                                     |
|---------------------------------------|-------------------------------------------------|---------------------------------------------------|----------|-------------------------------------------------------------|
| tests/integration/test_generate.py   | argus/packs/spring/instructions.md             | generate writes .claude/rules/spring.md, asserts @SpringBootTest | WIRED | test asserts (tmp_path / ".claude/rules/spring.md").read_text() contains "@SpringBootTest" |
| tests/integration/test_generate.py   | argus/packs/mockito/instructions.md            | generate writes .claude/rules/mockito.md, asserts ArgumentCaptor | WIRED | test asserts (tmp_path / ".claude/rules/mockito.md").read_text() contains "ArgumentCaptor" |
| argus/cli.py upgrade                  | _compute_changed_files + os.environ.get("CI") + click.confirm | diff then branch on CI env var vs interactive prompt | WIRED | cli.py line 147: changed = _compute_changed_files; line 156: os.environ.get("CI"); line 159: click.confirm |
| argus/cli.py init                     | _detect_platforms + _build_init_yaml           | scan markers before writing .argus.yml            | WIRED    | cli.py lines 118-119: detected = _detect_platforms(project_root); config_path.write_text(_build_init_yaml(DEFAULT_PACKS, detected)) |

### Requirements Coverage

| Requirement | Source Plan | Description                                                                 | Status    | Evidence                                                                |
|-------------|-------------|-----------------------------------------------------------------------------|-----------|-------------------------------------------------------------------------|
| FWRK-03     | 24-01-PLAN  | User can apply `spring` pack for Spring/Spring Boot conventions              | SATISFIED | spring pack exists, 3 integration tests pass, packs list/show/generate all work |
| FWRK-04     | 24-02-PLAN  | User can apply `mockito` pack for Java mock discipline                       | SATISFIED | mockito pack exists, 3 integration tests pass, packs list/show/generate all work |
| CLI-01      | 24-03-PLAN  | All changed code reaches 80% unit test coverage                              | SATISFIED | 94.67% total coverage, --cov-fail-under=80 passes across 189 tests      |
| CLI-02      | 24-03-PLAN  | `argus upgrade` detects out-of-date generated files and offers to regenerate | SATISFIED | upgrade command present with 6 passing unit tests covering all branches  |
| CLI-03      | 24-03-PLAN  | `argus init` detects installed platforms from project files                  | SATISFIED | _detect_platforms + _build_init_yaml implemented, 5 passing unit tests   |

No orphaned requirements — all 5 IDs claimed in plan frontmatter match REQUIREMENTS.md Phase 24 entries and are fully implemented.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| argus/packs/spring/instructions.md | 12, 35 | `javax.` appears in "never use" examples | Info | Intentional negative examples in instructions; plan acceptance criteria note these are instructional references, not actual javax imports in production code |

No blockers found. The two `javax.` occurrences are explicit "never use" warnings in the pack content — exactly what the rules demand.

### Human Verification Required

#### 1. Interactive upgrade prompt flow

**Test:** In a project with a stale generated file, run `argus upgrade` from the terminal (not via CliRunner). Answer "y" when prompted.
**Expected:** Lists stale file names, prompts "Regenerate now?", writes the updated file on confirmation, prints confirmation per file.
**Why human:** CliRunner mixes stdout/stderr and simulates input — real terminal behavior for interactive prompts (cursor, clear-to-end-of-line, ANSI) cannot be verified programmatically.

### Gaps Summary

No gaps. All phase-24 deliverables are present, substantive, wired, and tested.

- spring pack: fully authored with Jakarta-only content, no java-pack overlap, 3 integration tests pass
- mockito pack: fully authored with mock-mechanics-only content, no Spring annotation overlap, 3 integration tests pass
- upgrade command: all 5 behavioral branches implemented and covered by 6 unit tests
- init platform detection: _detect_platforms + _build_init_yaml wired into init command, 5 unit tests cover all detection paths and fallback
- Coverage gate: 94.67% across all 189 tests, mypy exits 0

---

_Verified: 2026-06-26_
_Verifier: Claude (gsd-verifier)_
