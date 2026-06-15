from pathlib import Path
from argus.adapters.base import BaseAdapter, GeneratedFile, Pack, GENERATED_HEADER


class ClaudeAdapter(BaseAdapter):
    platform_id = "claude"
    display_name = "Claude Code"

    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        files = [
            self._agents_md(packs),
            self._claude_md(packs),
            *self._rules(packs),
            *self._skills(packs),
        ]
        return files

    def _claude_md(self, packs: list[Pack]) -> GeneratedFile:
        sections = [GENERATED_HEADER + "# Engineering Standards\n"]
        for pack in packs:
            sections.append(f"## {pack.name.upper()}\n\n{pack.instructions}")
            if pack.checklist:
                sections.append(pack.checklist)
            if pack.examples:
                sections.append(pack.examples)
        return GeneratedFile(path=Path("CLAUDE.md"), content="\n\n".join(sections))

    def _rules(self, packs: list[Pack]) -> list[GeneratedFile]:
        return [
            GeneratedFile(
                path=Path(f".claude/rules/{pack.name}.md"),
                content=GENERATED_HEADER + pack.instructions,
            )
            for pack in packs
        ]

    def _skills(self, packs: list[Pack]) -> list[GeneratedFile]:
        files = []
        for pack in packs:
            if pack.checklist or pack.examples:
                parts = [GENERATED_HEADER]
                if pack.checklist:
                    parts.append(pack.checklist)
                if pack.examples:
                    parts.append(pack.examples)
                files.append(GeneratedFile(
                    path=Path(f".claude/skills/{pack.name}/SKILL.md"),
                    content="\n\n".join(parts),
                ))
        return files
