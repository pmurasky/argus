## Documentation Standards Examples

### Correct

```python
class DataLoader:
    """Load records from built-in and custom search paths."""

def list_items(self) -> list[str]:
    """Return sorted list of all discoverable item names."""

@main.command()
def generate(...):
    """Generate platform-specific files from config."""

# YAML safe_load returns Any — typed immediately below
data: dict[str, Any] = yaml.safe_load(path.read_text())
```

### Incorrect

```python
class DataLoader:
    """DataLoader class."""          # restates the name

def list_items(self):
    """Gets the available items."""  # wrong mood, explains what

# increment the counter
i += 1                               # explains what, not why
```

### Exempt (no docstring needed)

```python
def __init__(self, project_root: Path) -> None: ...
def _load_one(self, name: str) -> Record: ...
```
