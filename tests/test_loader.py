import pytest
from pathlib import Path
from argus.loader import PackLoader, PackNotFoundError


def _make_pack(base: Path, name: str, has_checklist: bool = True, has_examples: bool = False):
    pack_dir = base / name
    pack_dir.mkdir(parents=True)
    (pack_dir / "pack.yml").write_text(
        f"name: {name}\ncategory: workflow\nrequires: []\nplatforms: [all]\n"
    )
    (pack_dir / "instructions.md").write_text(f"# {name} instructions")
    if has_checklist:
        (pack_dir / "checklist.md").write_text(f"## {name} checklist")
    if has_examples:
        (pack_dir / "examples.md").write_text(f"## {name} examples")


def test_loader_finds_pack_in_builtin_path(tmp_path):
    builtin = tmp_path / "builtin"
    _make_pack(builtin, "tdd")
    loader = PackLoader(project_root=tmp_path, builtin_packs_dir=builtin)
    packs = loader.load(["tdd"])
    assert packs[0].name == "tdd"
    assert packs[0].instructions == "# tdd instructions"


def test_loader_reads_optional_checklist(tmp_path):
    builtin = tmp_path / "builtin"
    _make_pack(builtin, "tdd", has_checklist=True)
    loader = PackLoader(project_root=tmp_path, builtin_packs_dir=builtin)
    pack = loader.load(["tdd"])[0]
    assert pack.checklist == "## tdd checklist"


def test_loader_checklist_is_none_when_absent(tmp_path):
    builtin = tmp_path / "builtin"
    _make_pack(builtin, "tdd", has_checklist=False)
    loader = PackLoader(project_root=tmp_path, builtin_packs_dir=builtin)
    pack = loader.load(["tdd"])[0]
    assert pack.checklist is None


def test_loader_examples_is_none_when_absent(tmp_path):
    builtin = tmp_path / "builtin"
    _make_pack(builtin, "tdd", has_examples=False)
    loader = PackLoader(project_root=tmp_path, builtin_packs_dir=builtin)
    pack = loader.load(["tdd"])[0]
    assert pack.examples is None


def test_loader_reads_examples_when_present(tmp_path):
    builtin = tmp_path / "builtin"
    _make_pack(builtin, "tdd", has_examples=True)
    loader = PackLoader(project_root=tmp_path, builtin_packs_dir=builtin)
    pack = loader.load(["tdd"])[0]
    assert pack.examples == "## tdd examples"


def test_loader_raises_on_unknown_pack(tmp_path):
    builtin = tmp_path / "builtin"
    builtin.mkdir()
    loader = PackLoader(project_root=tmp_path, builtin_packs_dir=builtin)
    with pytest.raises(PackNotFoundError) as exc_info:
        loader.load(["nonexistent"])
    assert "nonexistent" in str(exc_info.value)
    assert "Available packs" in str(exc_info.value)


def test_custom_pack_overrides_builtin(tmp_path):
    builtin = tmp_path / "builtin"
    _make_pack(builtin, "tdd")
    (builtin / "tdd" / "instructions.md").write_text("# builtin tdd")

    custom = tmp_path / ".argus" / "packs"
    _make_pack(custom, "tdd")
    (custom / "tdd" / "instructions.md").write_text("# custom tdd")

    loader = PackLoader(project_root=tmp_path, custom_packs_dir=custom, builtin_packs_dir=builtin)
    pack = loader.load(["tdd"])[0]
    assert pack.instructions == "# custom tdd"


def test_available_packs_lists_builtin(tmp_path):
    builtin = tmp_path / "builtin"
    _make_pack(builtin, "tdd")
    _make_pack(builtin, "solid")
    loader = PackLoader(project_root=tmp_path, builtin_packs_dir=builtin)
    available = loader.available_packs()
    assert "tdd" in available
    assert "solid" in available
