import sys
from pathlib import Path
import click
from argus.config import ArgusConfig
from argus.generator import Generator


@click.group()
def main():
    """Argus — AI Agent Engineering Standards Layer"""


@main.command()
@click.option("--dry-run", is_flag=True, help="Preview files without writing")
@click.option("--check", is_flag=True, help="Exit non-zero if files would change (CI gate)")
@click.option(
    "--project-root",
    default=".",
    type=click.Path(path_type=Path),
    help="Project root directory (default: current directory)",
)
def generate(dry_run: bool, check: bool, project_root: Path):
    """Generate platform-specific files from .argus.yml"""
    config_path = project_root / ".argus.yml"
    if not config_path.exists():
        click.echo(
            f"✗ .argus.yml not found in {project_root}. Run `argus init` first.", err=True
        )
        sys.exit(1)

    config = ArgusConfig.from_file(config_path)
    files = Generator().run(config, project_root)

    if dry_run:
        for f in files:
            click.echo(f"  would write: {f.path}")
        return

    if check:
        changed = [
            f for f in files
            if not (project_root / f.path).exists()
            or (project_root / f.path).read_text() != f.content
        ]
        if changed:
            for f in changed:
                click.echo(f"  would change: {f.path}", err=True)
            sys.exit(1)
        return

    for f in files:
        target = project_root / f.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f.content)
        click.echo(f"  ✓ {f.path}")
