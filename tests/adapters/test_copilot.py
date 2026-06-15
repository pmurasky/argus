from pathlib import Path
from argus.adapters.copilot import CopilotAdapter
from argus.adapters.base import GENERATED_HEADER
from tests.adapters.conftest import stub_pack


def test_copilot_generates_agents_md():
    files = CopilotAdapter().generate([stub_pack("tdd")])
    assert Path("AGENTS.md") in [f.path for f in files]


def test_copilot_generates_copilot_instructions():
    files = CopilotAdapter().generate([stub_pack("tdd")])
    assert Path(".github/copilot-instructions.md") in [f.path for f in files]


def test_copilot_instructions_contains_only_instructions_no_checklist():
    files = CopilotAdapter().generate([stub_pack("tdd", checklist="## Checklist")])
    copilot_md = next(f for f in files if f.path == Path(".github/copilot-instructions.md"))
    assert "TDD instructions" in copilot_md.content
    assert "## Checklist" not in copilot_md.content


def test_copilot_generates_exactly_two_files():
    files = CopilotAdapter().generate([stub_pack("tdd"), stub_pack("solid")])
    assert len(files) == 2
