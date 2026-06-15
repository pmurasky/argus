## Dependency Injection Examples

### Correct

```python
from typing import Protocol

class PackRepository(Protocol):
    def find(self, name: str) -> Pack: ...

class PackLoader:
    """Load packs using an injected repository."""

    def __init__(self, repository: PackRepository) -> None:
        self._repository = repository

    def load(self, name: str) -> Pack:
        """Return a pack by name from the repository."""
        return self._repository.find(name)
```

```python
# Composition root — only place that wires concrete types
def main() -> None:
    repo = FileSystemPackRepository(root=Path("packs"))
    loader = PackLoader(repository=repo)
    cli(loader=loader)
```

### Incorrect

```python
class PackLoader:
    def __init__(self) -> None:
        self._repository = FileSystemPackRepository()  # concrete, internal

    def load(self, name: str) -> Pack:
        return self._repository.find(name)
```

```python
# Infrastructure import in domain module
from argus.infrastructure.fs_repo import FileSystemPackRepository  # wrong layer
```

### Testable with injection

```python
class FakeRepository:
    def find(self, name: str) -> Pack:
        return Pack(name=name, content="# stub")

def test_loader_returns_pack_by_name():
    # Given
    loader = PackLoader(repository=FakeRepository())
    # When
    result = loader.load("tdd")
    # Then
    assert result.name == "tdd"
```
