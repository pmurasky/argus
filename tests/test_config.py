import pytest
from pathlib import Path
from argus.config import ArgusConfig


def test_config_loads_packs_and_platforms(tmp_path):
    (tmp_path / ".argus.yml").write_text(
        "packs:\n  - tdd\n  - solid\nplatforms:\n  - claude\n"
    )
    config = ArgusConfig.from_file(tmp_path / ".argus.yml")
    assert config.packs == ["tdd", "solid"]
    assert config.platforms == ["claude"]


def test_config_custom_packs_dir_is_none_when_absent(tmp_path):
    (tmp_path / ".argus.yml").write_text("packs: [tdd]\nplatforms: [claude]\n")
    config = ArgusConfig.from_file(tmp_path / ".argus.yml")
    assert config.custom_packs_dir is None


def test_config_loads_custom_packs_dir(tmp_path):
    (tmp_path / ".argus.yml").write_text(
        "packs: [tdd]\nplatforms: [claude]\ncustom_packs_dir: .argus/packs\n"
    )
    config = ArgusConfig.from_file(tmp_path / ".argus.yml")
    assert config.custom_packs_dir == Path(".argus/packs")


def test_config_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        ArgusConfig.from_file(tmp_path / "nonexistent.yml")
