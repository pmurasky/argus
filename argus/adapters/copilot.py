from pathlib import Path

from argus.adapters.base import GENERATED_HEADER, BaseAdapter, GeneratedFile, Pack


class CopilotAdapter(BaseAdapter):
    platform_id = "copilot"
    display_name = "GitHub Copilot"

    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        return [self._agents_md(packs), self._copilot_instructions(packs)]

    def _copilot_instructions(self, packs: list[Pack]) -> GeneratedFile:
        sections = [GENERATED_HEADER + "# Engineering Standards\n"]
        for pack in packs:
            sections.append(f"## {pack.name.upper()}\n\n{pack.instructions}")
        return GeneratedFile(
            path=Path(".github/copilot-instructions.md"),
            content="\n\n".join(sections),
        )
