## Python Checklist

- [ ] f-strings used for interpolation — no .format() or % strings
- [ ] All resource management uses a with statement — no manual .close() calls
- [ ] pathlib.Path used for filesystem paths — no os.path string building
- [ ] enumerate()/zip() used instead of manual index arithmetic
- [ ] is None / is not None used for None comparison
- [ ] snake_case for functions and variables; PascalCase for classes
- [ ] UPPER_SNAKE_CASE for module-level constants
- [ ] @dataclass used for structured records instead of bare dicts
- [ ] @dataclass(frozen=True) used for immutable value objects
- [ ] No builtins shadowed (list, id, type, dict)
