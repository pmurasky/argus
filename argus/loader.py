from pathlib import Path
import yaml
from argus import ArgusError
from argus.adapters.base import Pack


class PackNotFoundError(ArgusError):
    """Raised when a requested pack cannot be found on the search path."""


class PackLoader:
    def __init__(
        self,
        project_root: Path,
        custom_packs_dir: Path | None = None,
        builtin_packs_dir: Path | None = None,
    ):
        if builtin_packs_dir is None:
            import importlib.resources
            builtin_packs_dir = Path(str(importlib.resources.files("argus") / "packs"))

        self._search_path: list[Path] = []
        candidate_custom = custom_packs_dir or project_root / ".argus/packs"
        if candidate_custom.exists():
            self._search_path.append(candidate_custom)
        self._search_path.append(builtin_packs_dir)

    def load(self, pack_names: list[str]) -> list[Pack]:
        return [self._load_one(name) for name in pack_names]

    def available_packs(self) -> list[str]:
        found: set[str] = set()
        for base in self._search_path:
            if base.exists():
                found.update(p.name for p in base.iterdir() if p.is_dir())
        return sorted(found)

    def _load_one(self, name: str) -> Pack:
        for base in self._search_path:
            pack_dir = base / name
            if pack_dir.exists():
                return self._read(pack_dir, name)
        available = ", ".join(self.available_packs()) or "(none)"
        raise PackNotFoundError(
            f'Unknown pack: "{name}"\n  Available packs: {available}\n'
            f'  Did you mean one of the above?'
        )

    def _read(self, pack_dir: Path, name: str) -> Pack:
        manifest = yaml.safe_load((pack_dir / "pack.yml").read_text())
        return Pack(
            name=name,
            manifest=manifest,
            instructions=(pack_dir / "instructions.md").read_text(),
            checklist=self._read_optional(pack_dir / "checklist.md"),
            examples=self._read_optional(pack_dir / "examples.md"),
        )

    @staticmethod
    def _read_optional(path: Path) -> str | None:
        return path.read_text() if path.exists() else None
