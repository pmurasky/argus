#!/usr/bin/env python3
"""Generate Docusaurus MDX pages from argus pack source files."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).parent.parent
PACKS_DIR = REPO_ROOT / "argus" / "packs"
OUTPUT_DIR = REPO_ROOT / "website" / "docs" / "packs"

CATEGORY_DISPLAY: dict[str, tuple[str, int]] = {
    "workflow":     ("Workflow",     1),
    "quality":      ("Code Quality", 2),
    "architecture": ("Architecture", 3),
    "language":     ("Languages",    4),
    "framework":    ("Frameworks",   5),
    "process":      ("Process",      6),
}


def _format_field(value: Any) -> str:
    """Convert a pack.yml field value to a human-readable string."""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) or "none"
    return str(value) if value else "none"


def _build_page(name: str, meta: dict[str, Any], instructions: str) -> str:
    """Return the MDX page content for a single pack."""
    title = name.replace("-", " ").title()
    description = meta.get("description", "")
    category = meta.get("category", "")
    requires = _format_field(meta.get("requires") or [])
    platforms = _format_field(meta.get("platforms", "all"))

    return f"""---
id: {name}
title: {title}
sidebar_label: {title}
custom_edit_url: null
---

# {title}

> {description}

| Field | Value |
|-------|-------|
| Category | {category} |
| Requires | {requires} |
| Platforms | {platforms} |

---

{instructions.strip()}
"""


def _write_category_json(category_dir: Path, category: str) -> None:
    """Write _category_.json for a pack category subdirectory."""
    label, position = CATEGORY_DISPLAY.get(category, (category.title(), 99))
    data = {
        "label": label,
        "position": position,
        "collapsible": True,
        "collapsed": False,
    }
    (category_dir / "_category_.json").write_text(
        json.dumps(data, indent=2) + "\n"
    )


def main() -> None:
    """Generate one MDX page per pack into website/docs/packs/{category}/."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    seen_categories: set[str] = set()
    count = 0

    for pack_dir in sorted(PACKS_DIR.iterdir()):
        if not pack_dir.is_dir():
            continue
        pack_yml = pack_dir / "pack.yml"
        instructions_md = pack_dir / "instructions.md"
        if not pack_yml.exists() or not instructions_md.exists():
            continue

        with pack_yml.open() as f:
            meta: dict[str, Any] = yaml.safe_load(f)

        name: str = meta.get("name", pack_dir.name)
        category: str = meta.get("category", "process")
        instructions: str = instructions_md.read_text()

        category_dir = OUTPUT_DIR / category
        category_dir.mkdir(exist_ok=True)

        if category not in seen_categories:
            _write_category_json(category_dir, category)
            seen_categories.add(category)

        (category_dir / f"{name}.md").write_text(
            _build_page(name, meta, instructions)
        )
        count += 1
        print(f"  ✓ packs/{category}/{name}.md")

    print(f"\nGenerated {count} pack pages across {len(seen_categories)} categories.")


if __name__ == "__main__":
    main()
