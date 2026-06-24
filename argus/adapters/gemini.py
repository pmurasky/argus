from pathlib import Path

from argus.adapters.base import GENERATED_HEADER, BaseAdapter, GeneratedFile, Pack


class GeminiAdapter(BaseAdapter):
    """Adapter for Gemini CLI — generates GEMINI.md at the project root."""

    platform_id = "gemini"
    display_name = "Gemini CLI"

    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        """Translate packs into AGENTS.md and GEMINI.md."""
        return [self._agents_md(packs), self._gemini_md(packs)]

    def _gemini_md(self, packs: list[Pack]) -> GeneratedFile:
        """Build GEMINI.md containing all pack instructions as H2 sections."""
        sections = [GENERATED_HEADER + "# Engineering Standards\n"]
        for pack in packs:
            sections.append(f"## {pack.name.upper()}\n\n{pack.instructions}")
        return GeneratedFile(
            path=Path("GEMINI.md"),
            content="\n\n".join(sections),
        )
