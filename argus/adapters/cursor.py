from pathlib import Path

from argus.adapters.base import GENERATED_HEADER, BaseAdapter, GeneratedFile, Pack


class CursorAdapter(BaseAdapter):
    platform_id = "cursor"
    display_name = "Cursor"

    def generate(self, packs: list[Pack]) -> list[GeneratedFile]:
        return [self._agents_md(packs), *self._rules(packs)]

    def _rules(self, packs: list[Pack]) -> list[GeneratedFile]:
        return [
            GeneratedFile(
                path=Path(f".cursor/rules/{pack.name}.md"),
                content=GENERATED_HEADER + pack.instructions,
            )
            for pack in packs
        ]
