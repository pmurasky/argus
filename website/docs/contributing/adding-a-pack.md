---
id: adding-a-pack
title: Adding a Pack
sidebar_position: 1
---

# Adding a Pack

A pack is a directory in `argus/packs/` containing two files: `pack.yml` (metadata) and `instructions.md` (the content injected into agent instruction files).

## Directory Structure

```
argus/packs/my-new-pack/
├── pack.yml
└── instructions.md
```

## `pack.yml` Schema

```yaml
name: my-new-pack
description: One-line description of what this pack enforces
category: quality        # workflow | quality | architecture | language | framework | process
requires: []             # list of pack names this pack depends on (documentation only)
platforms: [all]         # [all] or a specific list like [claude, cursor]
```

All fields are required. `requires` is documentation intent — the loader does not enforce dependencies at runtime.

## `instructions.md` Conventions

The content of `instructions.md` is injected verbatim into the platform-specific instruction file. Write rules in the imperative mood, organized under H2 sections.

```markdown
# My New Pack

> One-sentence summary of the pack's purpose.

## Core Rule

State the single most important rule here.

## Rule Category 1

- Rule one: specific, actionable, imperative
- Rule two: specific, actionable, imperative
- Rule three: avoid being vague

## Red Flags — Stop and Correct

- Pattern that should never appear in code
- Another anti-pattern to avoid
```

### Writing Good Rules

- **Imperative mood:** "Use constructor injection" not "Constructor injection should be used"
- **Specific:** "Method must be ≤ 20 lines" not "Keep methods short"
- **Actionable:** The developer should know exactly what to do or avoid
- **No overlap:** Check existing packs — don't duplicate rules that belong in another pack

## Testing Your Pack

After creating the files, verify the pack is discoverable:

```bash
argus packs list | grep my-new-pack
```

Preview the content that would be injected:

```bash
argus packs show my-new-pack
```

## Writing Tests

Add integration tests for your pack in `tests/integration/test_generate.py`, following the existing pattern:

```python
MY_PACK_CONFIG = """\
packs:
  - my-new-pack
platforms:
  - claude
"""


def test_my_new_pack_appears_in_packs_list():
    runner = CliRunner()
    result = runner.invoke(main, ["packs", "list"])
    assert result.exit_code == 0
    assert "my-new-pack" in result.output


def test_my_new_pack_generate_injects_content(tmp_path):
    (tmp_path / ".argus.yml").write_text(MY_PACK_CONFIG)
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "--project-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "KEY_PHRASE_FROM_INSTRUCTIONS" in (
        tmp_path / ".claude/rules/my-new-pack.md"
    ).read_text()
```

Run: `.venv/bin/pytest tests/integration/test_generate.py -k my-new-pack -q`

## Submitting

1. Create your pack directory and files
2. Write the integration tests (RED → GREEN TDD cycle)
3. Run the full test suite: `.venv/bin/pytest tests/ -q`
4. Run type check: `mypy argus/`
5. Open a pull request
