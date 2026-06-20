import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from argus.cli import main
from argus.adapters.base import GeneratedFile


def _write_config(tmp_path: Path):
    (tmp_path / ".argus.yml").write_text("packs: [tdd]\nplatforms: [claude]\n")


def _mock_generator(files: list[GeneratedFile]):
    mock = MagicMock()
    mock.return_value.run.return_value = files
    return mock


def test_version_flag_outputs_version():
    # Given
    from importlib.metadata import version
    runner = CliRunner()
    # When
    result = runner.invoke(main, ["--version"])
    # Then
    assert result.exit_code == 0
    assert version("argus-standards") in result.output


def test_generate_writes_files(tmp_path):
    _write_config(tmp_path)
    output_file = GeneratedFile(path=Path("CLAUDE.md"), content="# content")
    runner = CliRunner()
    with patch("argus.cli.Generator", _mock_generator([output_file])):
        result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / "CLAUDE.md").read_text() == "# content"


def test_generate_creates_parent_directories(tmp_path):
    _write_config(tmp_path)
    output_file = GeneratedFile(path=Path(".claude/rules/tdd.md"), content="# rule")
    runner = CliRunner()
    with patch("argus.cli.Generator", _mock_generator([output_file])):
        result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".claude/rules/tdd.md").exists()


def test_generate_dry_run_does_not_write(tmp_path):
    _write_config(tmp_path)
    output_file = GeneratedFile(path=Path("CLAUDE.md"), content="# content")
    runner = CliRunner()
    with patch("argus.cli.Generator", _mock_generator([output_file])):
        result = runner.invoke(main, ["generate", "--dry-run", "--project-root", str(tmp_path)])
    assert result.exit_code == 0
    assert not (tmp_path / "CLAUDE.md").exists()
    assert "would write" in result.output


def test_generate_check_exits_nonzero_when_files_differ(tmp_path):
    _write_config(tmp_path)
    (tmp_path / "CLAUDE.md").write_text("# old content")
    output_file = GeneratedFile(path=Path("CLAUDE.md"), content="# new content")
    runner = CliRunner()
    with patch("argus.cli.Generator", _mock_generator([output_file])):
        result = runner.invoke(main, ["generate", "--check", "--project-root", str(tmp_path)])
    assert result.exit_code == 1


def test_generate_check_exits_zero_when_files_match(tmp_path):
    _write_config(tmp_path)
    (tmp_path / "CLAUDE.md").write_text("# content")
    output_file = GeneratedFile(path=Path("CLAUDE.md"), content="# content")
    runner = CliRunner()
    with patch("argus.cli.Generator", _mock_generator([output_file])):
        result = runner.invoke(main, ["generate", "--check", "--project-root", str(tmp_path)])
    assert result.exit_code == 0


def test_generate_fails_gracefully_when_no_config(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 1
    assert ".argus.yml" in result.output


def test_init_creates_argus_yml(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["init", "--project-root", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".argus.yml").exists()


def test_init_yml_contains_default_packs(tmp_path):
    runner = CliRunner()
    runner.invoke(main, ["init", "--project-root", str(tmp_path)])
    import yaml
    config = yaml.safe_load((tmp_path / ".argus.yml").read_text())
    assert "tdd" in config["packs"]
    assert "atomic-commit" in config["packs"]


def test_init_does_not_overwrite_without_confirm(tmp_path):
    (tmp_path / ".argus.yml").write_text("packs: []\nplatforms: []\n")
    runner = CliRunner()
    result = runner.invoke(main, ["init", "--project-root", str(tmp_path)], input="n\n")
    assert (tmp_path / ".argus.yml").read_text() == "packs: []\nplatforms: []\n"


def test_packs_list_shows_available_packs(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "atomic-commit" in result.output
    assert "tdd" in result.output


def test_packs_show_prints_instructions(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "show", "tdd"])
    assert result.exit_code == 0
    assert "TDD" in result.output


def test_platforms_list_shows_adapters():
    from unittest.mock import MagicMock, patch
    runner = CliRunner()

    # Mock entry points
    mock_ep_claude = MagicMock()
    mock_ep_claude.name = "claude"
    mock_ep_opencode = MagicMock()
    mock_ep_opencode.name = "opencode"

    with patch("importlib.metadata.entry_points", return_value=[mock_ep_claude, mock_ep_opencode]):
        result = runner.invoke(main, ["platforms", "list"])

    assert result.exit_code == 0
    assert "claude" in result.output


def test_validate_passes_with_valid_config(tmp_path):
    from unittest.mock import MagicMock, patch
    (tmp_path / ".argus.yml").write_text(
        "packs: [tdd, atomic-commit]\nplatforms: [claude]\n"
    )
    runner = CliRunner()

    # Mock AdapterRegistry.get to return a mock adapter
    with patch("argus.cli.AdapterRegistry.get", return_value=MagicMock()):
        result = runner.invoke(main, ["validate", "--project-root", str(tmp_path)])

    assert result.exit_code == 0
    assert "All checks passed" in result.output


def test_validate_fails_with_unknown_pack(tmp_path):
    (tmp_path / ".argus.yml").write_text("packs: [nonexistent]\nplatforms: [claude]\n")
    runner = CliRunner()
    result = runner.invoke(main, ["validate", "--project-root", str(tmp_path)])
    assert result.exit_code == 1


def test_validate_fails_with_missing_config(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["validate", "--project-root", str(tmp_path)])
    assert result.exit_code == 1
