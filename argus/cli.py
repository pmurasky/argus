import os
import sys
from pathlib import Path

import click
import yaml

from argus.adapters.base import GeneratedFile
from argus.config import ArgusConfig
from argus.generator import AdapterConflictError, AdapterRegistry, Generator, UnknownPlatformError
from argus.loader import PackLoader, PackNotFoundError


def _compute_changed_files(
    files: list[GeneratedFile], project_root: Path
) -> list[GeneratedFile]:
    """Return files that would change if written to project_root."""
    return [
        f for f in files
        if not (project_root / f.path).exists()
        or (project_root / f.path).read_text() != f.content
    ]


@click.group()
@click.version_option(package_name="argus-standards")
def main() -> None:
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
def generate(dry_run: bool, check: bool, project_root: Path) -> None:
    """Generate platform-specific files from .argus.yml"""
    config_path = project_root / ".argus.yml"
    if not config_path.exists():
        click.echo(
            f"✗ .argus.yml not found in {project_root}. Run `argus init` first.", err=True
        )
        sys.exit(1)

    config = ArgusConfig.from_file(config_path)
    try:
        files = Generator().run(config, project_root)
    except (PackNotFoundError, UnknownPlatformError, AdapterConflictError) as e:
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)

    if dry_run:
        for f in files:
            click.echo(f"  would write: {f.path}")
        return

    if check:
        changed = _compute_changed_files(files, project_root)
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


DEFAULT_PACKS = ["atomic-commit", "tdd", "solid", "code-quality", "pre-commit"]
DEFAULT_PLATFORMS = ["claude", "opencode", "copilot", "cursor", "gemini"]


def _detect_platforms(project_root: Path) -> list[str]:
    """Return platform IDs whose marker artifacts exist in project_root."""
    markers = {
        "claude":   lambda r: (r / ".claude").is_dir(),
        "cursor":   lambda r: (r / ".cursor").is_dir(),
        "copilot":  lambda r: (r / ".github/copilot-instructions.md").is_file(),
        "gemini":   lambda r: (r / "GEMINI.md").is_file(),
        "opencode": lambda r: (r / ".opencode").is_dir(),
    }
    return [name for name in DEFAULT_PLATFORMS if name in markers and markers[name](project_root)]


def _build_init_yaml(packs: list[str], detected: list[str]) -> str:
    """Build .argus.yml content: detected platforms active, undetected commented."""
    lines = ["packs:"]
    lines.extend(f"  - {p}" for p in packs)
    active = detected if detected else DEFAULT_PLATFORMS
    lines.append("platforms:")
    lines.extend(f"  - {p}" for p in active)
    if detected:
        for p in DEFAULT_PLATFORMS:
            if p not in detected:
                lines.append(f"  # - {p}")
    return "\n".join(lines) + "\n"


@main.command()
@click.option(
    "--project-root",
    default=".",
    type=click.Path(path_type=Path),
)
def init(project_root: Path) -> None:
    """Scaffold .argus.yml with all available packs and platforms."""
    config_path = project_root / ".argus.yml"
    if config_path.exists():
        if not click.confirm(f"{config_path} already exists. Overwrite?"):
            return
    detected = _detect_platforms(project_root)
    config_path.write_text(_build_init_yaml(DEFAULT_PACKS, detected))
    click.echo(f"✓ Written: {config_path}")
    click.echo("Edit .argus.yml to select packs and platforms, then run: argus generate")


@main.command()
@click.option(
    "--project-root",
    default=".",
    type=click.Path(path_type=Path),
)
def upgrade(project_root: Path) -> None:
    """Detect out-of-date generated files and offer to regenerate."""
    config_path = project_root / ".argus.yml"
    if not config_path.exists():
        click.echo(
            f"✗ .argus.yml not found in {project_root}. Run `argus init` first.",
            err=True,
        )
        sys.exit(1)

    config = ArgusConfig.from_file(config_path)
    try:
        files = Generator().run(config, project_root)
    except (PackNotFoundError, UnknownPlatformError, AdapterConflictError) as e:
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)

    changed = _compute_changed_files(files, project_root)

    if not changed:
        click.echo("✓ All generated files are up to date.")
        return

    for f in changed:
        click.echo(f"  • {f.path}")

    if os.environ.get("CI"):
        sys.exit(1)

    if click.confirm("Regenerate now?", default=False):
        for f in changed:
            target = project_root / f.path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f.content)
            click.echo(f"  ✓ {f.path}")


@main.group()
def packs() -> None:
    """Manage available packs."""


@packs.command("list")
def packs_list() -> None:
    """Show all available packs."""
    loader = PackLoader(project_root=Path("."))
    for name in loader.available_packs():
        click.echo(f"  {name}")


@packs.command("show")
@click.argument("name")
def packs_show(name: str) -> None:
    """Print a pack's instructions."""
    loader = PackLoader(project_root=Path("."))
    try:
        pack = loader.load([name])[0]
        click.echo(pack.instructions)
    except PackNotFoundError as e:
        click.echo(str(e), err=True)
        sys.exit(1)


@main.group()
def platforms() -> None:
    """Manage available platform adapters."""


@platforms.command("list")
def platforms_list() -> None:
    """Show all available platform adapters."""
    from importlib.metadata import entry_points
    eps = entry_points(group="argus.adapters")
    for ep in sorted(eps, key=lambda e: e.name):
        click.echo(f"  {ep.name}")


@main.command()
@click.option(
    "--project-root",
    default=".",
    type=click.Path(path_type=Path),
)
def validate(project_root: Path) -> None:
    """Validate .argus.yml and verify setup."""
    config_path = project_root / ".argus.yml"
    failed = False

    if not config_path.exists():
        click.echo(f"  ✗ .argus.yml not found in {project_root}", err=True)
        sys.exit(1)

    try:
        config = ArgusConfig.from_file(config_path)
        click.echo("  ✓ .argus.yml found and parseable")
    except Exception as e:
        click.echo(f"  ✗ .argus.yml parse error: {e}", err=True)
        sys.exit(1)

    try:
        PackLoader(project_root, config.custom_packs_dir).load(config.packs)
        click.echo(f"  ✓ Packs resolved: {', '.join(config.packs)}")
    except PackNotFoundError as e:
        click.echo(f"  ✗ {e}", err=True)
        failed = True

    try:
        for platform_id in config.platforms:
            AdapterRegistry.get(platform_id)
        click.echo(f"  ✓ Platforms resolved: {', '.join(config.platforms)}")
    except (UnknownPlatformError, AdapterConflictError) as e:
        click.echo(f"  ✗ {e}", err=True)
        failed = True

    if failed:
        sys.exit(1)

    click.echo("\n  All checks passed.")
