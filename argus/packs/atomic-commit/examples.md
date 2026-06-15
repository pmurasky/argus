## Atomic Commit Examples

### Correct — one feature, three commits (TDD cycle)

```bash
git commit -m "test: add failing test for user email validation"
git commit -m "feat: implement user email validation"
git commit -m "refactor: extract email regex to named constant"
```

### Incorrect — never do this

```bash
# Bad: the word "and" signals multiple concerns
git commit -m "add user validation and fix login bug and update docs"

# Bad: mixed concerns
git commit -m "feat: add discount plus fix rounding error"
```
