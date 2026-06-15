## Documentation Standards Examples

### Correct

```python
class PackLoader:
    """Load packs from built-in and custom search paths."""

def available_packs(self) -> list[str]:
    """Return sorted list of all discoverable pack names."""

@main.command()
def generate(...):
    """Generate platform-specific files from .argus.yml"""

# YAML safe_load returns Any — typed immediately below
data: dict[str, Any] = yaml.safe_load(path.read_text())
```

### Incorrect

```python
class PackLoader:
    """PackLoader class."""          # restates the name

def available_packs(self):
    """Gets the available packs."""  # wrong mood, explains what

# increment the counter
i += 1                               # explains what, not why
```

### Exempt (no docstring needed)

```python
def __init__(self, project_root: Path) -> None: ...
def _load_one(self, name: str) -> Pack: ...
```
