## Type Safety Examples

### Correct
```python
def load(self, pack_names: list[str]) -> list[Pack]: ...
def from_file(cls, path: Path) -> "ArgusConfig": ...
custom_packs_dir: Path | None = None
```

### Incorrect
```python
def load(self, pack_names): ...           # missing annotations
def get(cls, platform_id: str): ...       # missing return type
Optional[Path]                            # use Path | None
List[str]                                 # use list[str]
```

### Correct boundary usage
```python
data: dict[str, Any] = yaml.safe_load(path.read_text())
packs: list[str] = data["packs"]         # typed immediately after
```
