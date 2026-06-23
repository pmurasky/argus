from pathlib import Path

from argus.adapters.base import GENERATED_HEADER, BaseAdapter, GeneratedFile, Pack


class ClaudeAdapter(BaseAdapter):
    platform_id = "claude"
    display_name = "Claude Code"

    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        files = [
            self._agents_md(packs),
            self._claude_md(),
            *self._rules(packs),
            *self._skills(packs),
        ]
        return files

    def _claude_md(self) -> GeneratedFile:
        body = "# Engineering Standards\n\nRules are in `.claude/rules/`."
        body += " All apply to every commit.\n"
        return GeneratedFile(path=Path("CLAUDE.md"), content=GENERATED_HEADER + body)

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
                parts = [self._skill_frontmatter(pack) + GENERATED_HEADER]
                if pack.checklist:
                    parts.append(pack.checklist)
                if pack.examples:
                    parts.append(pack.examples)
                files.append(GeneratedFile(
                    path=Path(f".claude/skills/{pack.name}/SKILL.md"),
                    content="\n\n".join(parts),
                ))
        return files

    @staticmethod
    def _skill_frontmatter(pack: Pack) -> str:
        description = pack.manifest.get("description", "")
        return f"---\nname: {pack.name}\ndescription: {description}\n---\n\n"
