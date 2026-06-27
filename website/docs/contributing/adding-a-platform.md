---
id: adding-a-platform
title: Adding a Platform Adapter
sidebar_position: 2
---

# Adding a Platform Adapter

A platform adapter controls how pack content is written for a specific AI coding agent. Each adapter is a Python class that implements the `BaseAdapter` protocol.

## File Location

Create `argus/adapters/{platform_name}.py`. Existing adapters to reference:
- `argus/adapters/claude.py` — writes per-pack rule files under `.claude/rules/`
- `argus/adapters/cursor.py` — writes per-pack rule files under `.cursor/rules/`
- `argus/adapters/copilot.py` — concatenates packs into a single file

## `BaseAdapter` Interface

From `argus/adapters/base.py`:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

@dataclass
class GeneratedFile:
    path: Path
    content: str

class BaseAdapter(Protocol):
    def generate(
        self,
        packs: list[str],
        pack_contents: dict[str, str],
        project_root: Path,
    ) -> list[GeneratedFile]: ...
```

Return a list of `GeneratedFile` objects. The generator writes them to disk.

## Minimal Adapter Example

```python
"""MyPlatform adapter — writes combined rules to myplatform-rules.md."""

from pathlib import Path

from argus.adapters.base import BaseAdapter, GeneratedFile


class MyPlatformAdapter(BaseAdapter):
    """Generate rules file for MyPlatform."""

    def generate(
        self,
        packs: list[str],
        pack_contents: dict[str, str],
        project_root: Path,
    ) -> list[GeneratedFile]:
        """Return a single combined rules file."""
        sections = [f"# {name}\n\n{content}" for name, content in pack_contents.items()]
        return [
            GeneratedFile(
                path=Path("myplatform-rules.md"),
                content="\n\n---\n\n".join(sections) + "\n",
            )
        ]
```

## Register the Adapter

Add an entry point in `pyproject.toml` under `[project.entry-points."argus.adapters"]`:

```toml
[project.entry-points."argus.adapters"]
myplatform = "argus.adapters.myplatform:MyPlatformAdapter"
```

Re-install the package for the entry point to take effect:

```bash
pip install -e .
argus platforms list  # should now include 'myplatform'
```

## Detection Marker (for `argus init`)

To make `argus init` auto-detect your platform, add a marker in `argus/cli.py` inside `_detect_platforms()`:

```python
"myplatform": lambda r: (r / "myplatform-config.json").is_file(),
```

## Writing Tests

Add tests in `tests/adapters/test_myplatform.py`:

```python
from pathlib import Path
from argus.adapters.myplatform import MyPlatformAdapter


def test_generate_returns_combined_file():
    adapter = MyPlatformAdapter()
    result = adapter.generate(
        packs=["tdd"],
        pack_contents={"tdd": "# TDD\n\nUse TDD."},
        project_root=Path("/tmp"),
    )
    assert len(result) == 1
    assert result[0].path == Path("myplatform-rules.md")
    assert "TDD" in result[0].content
```

Run: `.venv/bin/pytest tests/adapters/test_myplatform.py -q`

## Submitting

1. Create `argus/adapters/{name}.py` implementing `BaseAdapter`
2. Register the entry point in `pyproject.toml`
3. Add detection marker in `_detect_platforms()` if applicable
4. Write adapter unit tests + integration tests (RED → GREEN)
5. Run: `.venv/bin/pytest tests/ -q` and `mypy argus/`
6. Open a pull request
