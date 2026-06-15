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
