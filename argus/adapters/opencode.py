import json
from pathlib import Path
from argus.adapters.base import BaseAdapter, GeneratedFile, Pack, GENERATED_HEADER


class OpenCodeAdapter(BaseAdapter):
    platform_id = "opencode"
    display_name = "OpenCode"

    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        return [
            self._agents_md(packs),
            self._opencode_json(),
            *self._skills(packs),
            *self._commands(packs),
        ]

    def _opencode_json(self) -> GeneratedFile:
        config = {"$schema": "https://opencode.ai/config.json", "instructions": "AGENTS.md"}
        return GeneratedFile(path=Path("opencode.json"), content=json.dumps(config, indent=2))

    def _skills(self, packs: list[Pack]) -> list[GeneratedFile]:
        return [
            GeneratedFile(
                path=Path(f".opencode/skills/{pack.name}/SKILL.md"),
                content=GENERATED_HEADER + pack.instructions,
            )
            for pack in packs
        ]

    def _commands(self, packs: list[Pack]) -> list[GeneratedFile]:
        return [
            GeneratedFile(
                path=Path(f".opencode/commands/{pack.name}.md"),
                content=GENERATED_HEADER + pack.checklist,
            )
            for pack in packs
            if pack.checklist
        ]
