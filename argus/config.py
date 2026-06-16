from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class ArgusConfig:
    packs: list[str]
    platforms: list[str]
    custom_packs_dir: Path | None = None

    @classmethod
    def from_file(cls, path: Path) -> "ArgusConfig":
        data = yaml.safe_load(path.read_text())
        missing = [k for k in ("packs", "platforms") if k not in data]
        if missing:
            raise ValueError(f".argus.yml is missing required keys: {', '.join(missing)}")
        return cls(
            packs=data["packs"],
            platforms=data["platforms"],
            custom_packs_dir=Path(data["custom_packs_dir"]) if "custom_packs_dir" in data else None,
        )
