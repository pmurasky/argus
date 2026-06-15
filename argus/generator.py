from importlib.metadata import entry_points
from pathlib import Path
from argus.adapters.base import BaseAdapter, GeneratedFile
from argus.config import ArgusConfig
from argus.loader import PackLoader


class AdapterConflictError(Exception):
    pass


class UnknownPlatformError(Exception):
    pass


class AdapterRegistry:
    @classmethod
    def get(cls, platform_id: str) -> BaseAdapter:
        eps = entry_points(group="argus.adapters")
        matching = [ep for ep in eps if ep.name == platform_id]

        if len(matching) > 1:
            sources = [ep.value for ep in matching]
            raise AdapterConflictError(
                f'Adapter conflict: platform "{platform_id}" registered by:\n'
                + "\n".join(f"    {s}" for s in sources)
                + "\nUninstall one before running generate."
            )

        if not matching:
            available = sorted({ep.name for ep in eps})
            raise UnknownPlatformError(
                f'Unknown platform: "{platform_id}"\n'
                f"  Available platforms: {', '.join(available)}"
            )

        return matching[0].load()()


class Generator:
    def run(self, config: ArgusConfig, project_root: Path) -> list[GeneratedFile]:
        packs = PackLoader(project_root, config.custom_packs_dir).load(config.packs)
        seen: dict[Path, GeneratedFile] = {}
        for platform_id in config.platforms:
            adapter = AdapterRegistry.get(platform_id)
            for f in adapter.generate(packs):
                seen[f.path] = f
        return list(seen.values())
