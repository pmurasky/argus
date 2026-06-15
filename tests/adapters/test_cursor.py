from pathlib import Path
from argus.adapters.cursor import CursorAdapter
from tests.adapters.conftest import stub_pack


def test_cursor_generates_agents_md():
    files = CursorAdapter().generate([stub_pack("tdd")])
    assert Path("AGENTS.md") in [f.path for f in files]


def test_cursor_generates_rule_per_pack():
    files = CursorAdapter().generate([stub_pack("tdd"), stub_pack("solid")])
    paths = [f.path for f in files]
    assert Path(".cursor/rules/tdd.md") in paths
    assert Path(".cursor/rules/solid.md") in paths


def test_cursor_rules_contain_only_instructions():
    files = CursorAdapter().generate([stub_pack("tdd", checklist="## Checklist")])
    rule = next(f for f in files if f.path == Path(".cursor/rules/tdd.md"))
    assert "TDD instructions" in rule.content
    assert "## Checklist" not in rule.content
