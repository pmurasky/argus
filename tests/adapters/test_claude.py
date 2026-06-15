from pathlib import Path
from argus.adapters.claude import ClaudeAdapter
from argus.adapters.base import GENERATED_HEADER
from tests.adapters.conftest import stub_pack


def test_claude_generates_agents_md():
    packs = [stub_pack("tdd")]
    files = ClaudeAdapter().generate(packs)
    paths = [f.path for f in files]
    assert Path("AGENTS.md") in paths


def test_claude_generates_claude_md():
    packs = [stub_pack("tdd")]
    files = ClaudeAdapter().generate(packs)
    paths = [f.path for f in files]
    assert Path("CLAUDE.md") in paths


def test_claude_generates_rule_per_pack():
    packs = [stub_pack("tdd"), stub_pack("solid", checklist=None)]
    files = ClaudeAdapter().generate(packs)
    paths = [f.path for f in files]
    assert Path(".claude/rules/tdd.md") in paths
    assert Path(".claude/rules/solid.md") in paths


def test_claude_generates_skill_for_pack_with_checklist():
    packs = [stub_pack("tdd", checklist="## Checklist")]
    files = ClaudeAdapter().generate(packs)
    paths = [f.path for f in files]
    assert Path(".claude/skills/tdd/SKILL.md") in paths


def test_claude_skips_skill_for_pack_without_checklist_or_examples():
    packs = [stub_pack("solid", checklist=None, examples=None)]
    files = ClaudeAdapter().generate(packs)
    paths = [f.path for f in files]
    assert Path(".claude/skills/solid/SKILL.md") not in paths


def test_claude_md_includes_instructions_and_checklist():
    packs = [stub_pack("tdd", checklist="## Checklist")]
    files = ClaudeAdapter().generate(packs)
    claude_md = next(f for f in files if f.path == Path("CLAUDE.md"))
    assert "TDD instructions" in claude_md.content
    assert "## Checklist" in claude_md.content


def test_agents_md_contains_only_instructions():
    packs = [stub_pack("tdd", checklist="## Checklist")]
    files = ClaudeAdapter().generate(packs)
    agents_md = next(f for f in files if f.path == Path("AGENTS.md"))
    assert "TDD instructions" in agents_md.content
    assert "## Checklist" not in agents_md.content


def test_all_files_have_generated_header():
    packs = [stub_pack("tdd")]
    files = ClaudeAdapter().generate(packs)
    for f in files:
        assert GENERATED_HEADER in f.content, f"{f.path} missing generated header"
