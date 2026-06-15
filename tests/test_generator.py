import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from argus.adapters.base import GeneratedFile, Pack
from argus.config import ArgusConfig
from argus.generator import Generator, AdapterConflictError, UnknownPlatformError


def _make_config(tmp_path: Path, packs=None, platforms=None):
    packs = packs or ["tdd"]
    platforms = platforms or ["claude"]
    cfg_text = f"packs: {packs}\nplatforms: {platforms}\n"
    (tmp_path / ".argus.yml").write_text(cfg_text)
    return ArgusConfig.from_file(tmp_path / ".argus.yml")


def _stub_pack(name="tdd") -> Pack:
    return Pack(name=name, manifest={}, instructions="# instructions", checklist=None, examples=None)


def test_generator_calls_adapter_for_each_platform(tmp_path):
    config = _make_config(tmp_path, platforms=["claude", "opencode"])
    mock_adapter = MagicMock()
    mock_adapter.generate.return_value = [GeneratedFile(path=Path("AGENTS.md"), content="x")]

    with patch("argus.generator.AdapterRegistry.get", return_value=mock_adapter), \
         patch("argus.generator.PackLoader") as mock_loader:
        mock_loader.return_value.load.return_value = [_stub_pack()]
        files = Generator().run(config, tmp_path)

    assert mock_adapter.generate.call_count == 2


def test_generator_deduplicates_identical_paths(tmp_path):
    config = _make_config(tmp_path, platforms=["claude", "opencode"])
    agents_file = GeneratedFile(path=Path("AGENTS.md"), content="same content")
    mock_adapter = MagicMock()
    mock_adapter.generate.return_value = [agents_file]

    with patch("argus.generator.AdapterRegistry.get", return_value=mock_adapter), \
         patch("argus.generator.PackLoader") as mock_loader:
        mock_loader.return_value.load.return_value = [_stub_pack()]
        files = Generator().run(config, tmp_path)

    paths = [f.path for f in files]
    assert paths.count(Path("AGENTS.md")) == 1


def test_adapter_registry_raises_on_unknown_platform():
    with pytest.raises(UnknownPlatformError) as exc_info:
        from argus.generator import AdapterRegistry
        AdapterRegistry.get("nonexistent-platform")
    assert "nonexistent-platform" in str(exc_info.value)
    assert "Available platforms" in str(exc_info.value)
