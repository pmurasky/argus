import json

from argus.merger import JsonMerger

GENERATED = json.dumps(
    {"$schema": "https://opencode.ai/config.json", "instructions": ["AGENTS.md"]}
)


def merge(existing: str, generated: str = GENERATED) -> dict:
    result = JsonMerger().merge(existing, generated)
    assert result is not None
    return json.loads(result)


def test_preserves_unknown_top_level_keys():
    existing = json.dumps({"default_agent": "standards-build", "plugin": ["context-mode"]})
    merged = merge(existing)
    assert merged["default_agent"] == "standards-build"
    assert merged["plugin"] == ["context-mode"]


def test_updates_argus_owned_schema_key():
    existing = json.dumps({"$schema": "https://old.example/config.json"})
    merged = merge(existing)
    assert merged["$schema"] == "https://opencode.ai/config.json"


def test_deep_merges_mcp_block_preserving_foreign_servers():
    existing = json.dumps({"mcp": {"gsd": {"type": "local", "command": ["gsd"]}}})
    merged = merge(existing)
    assert merged["mcp"]["gsd"] == {"type": "local", "command": ["gsd"]}


def test_unions_instructions_with_existing_array():
    existing = json.dumps({"instructions": ["docs/AI_AGENT_WORKFLOW.md"]})
    merged = merge(existing)
    assert merged["instructions"] == ["docs/AI_AGENT_WORKFLOW.md", "AGENTS.md"]


def test_unions_instructions_with_existing_string():
    existing = json.dumps({"instructions": "CUSTOM.md"})
    merged = merge(existing)
    assert merged["instructions"] == ["CUSTOM.md", "AGENTS.md"]


def test_merge_is_idempotent():
    existing = json.dumps({"instructions": ["docs/x.md", "AGENTS.md"], "default_agent": "plan"})
    once = JsonMerger().merge(existing, GENERATED)
    assert once is not None
    twice = JsonMerger().merge(once, GENERATED)
    assert once == twice


def test_returns_none_for_invalid_json():
    assert JsonMerger().merge("{ not json", GENERATED) is None
