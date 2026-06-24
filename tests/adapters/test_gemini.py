from pathlib import Path

from argus.adapters.gemini import GeminiAdapter
from argus.adapters.base import GENERATED_HEADER
from tests.adapters.conftest import stub_pack


def test_gemini_generates_agents_md():
    files = GeminiAdapter().generate([stub_pack("tdd")])
    assert Path("AGENTS.md") in [f.path for f in files]


def test_gemini_generates_gemini_md():
    files = GeminiAdapter().generate([stub_pack("tdd")])
    assert Path("GEMINI.md") in [f.path for f in files]


def test_gemini_generates_exactly_two_files():
    files = GeminiAdapter().generate([stub_pack("tdd"), stub_pack("solid")])
    assert len(files) == 2


def test_gemini_md_contains_pack_instructions():
    files = GeminiAdapter().generate([stub_pack("tdd")])
    gemini_md = next(f for f in files if f.path == Path("GEMINI.md"))
    assert "TDD instructions" in gemini_md.content


def test_gemini_md_does_not_contain_checklist():
    files = GeminiAdapter().generate([stub_pack("tdd", checklist="## Checklist")])
    gemini_md = next(f for f in files if f.path == Path("GEMINI.md"))
    assert "## Checklist" not in gemini_md.content


def test_all_files_have_generated_header():
    files = GeminiAdapter().generate([stub_pack("tdd")])
    for f in files:
        assert GENERATED_HEADER in f.content, f"{f.path} missing generated header"
