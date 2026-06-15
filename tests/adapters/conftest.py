import pytest
from argus.adapters.base import Pack


def stub_pack(
    name: str,
    checklist: str | None = "## Checklist\n\n- [ ] item",
    examples: str | None = None,
) -> Pack:
    return Pack(
        name=name,
        manifest={"name": name, "category": "workflow", "requires": [], "platforms": ["all"]},
        instructions=f"# {name.upper()} instructions\n\nCore rule for {name}.",
        checklist=checklist,
        examples=examples,
    )
