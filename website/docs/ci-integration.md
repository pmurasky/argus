---
id: ci-integration
title: CI Integration
sidebar_position: 7
---

# CI Integration

## Check for Drift

Use `argus generate --check` to verify that committed generated files match what Argus would produce. This catches cases where someone edits a generated file directly or adds a pack to `.argus.yml` without regenerating.

```bash
argus generate --check
```

Exit code 0 = files are current. Exit code 1 = files would change (prints which ones).

## GitHub Actions Example

Add a step to your existing CI workflow:

```yaml
# .github/workflows/ci.yml
- name: Check Argus files are up to date
  run: argus generate --check
```

Full workflow with Argus check:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: argus generate --check   # fail if generated files are stale
      - run: pytest
```

## Upgrade Check in CI

To enforce that generated files are regenerated after every `argus-standards` upgrade, use `argus upgrade` with the `CI` environment variable:

```yaml
- name: Check Argus files are current
  run: argus upgrade
  env:
    CI: 'true'
```

`argus upgrade` exits non-zero in CI mode when any generated file is stale, with no interactive prompt.

## Recommended Workflow

1. **Developer:** edits `.argus.yml` or upgrades `argus-standards`
2. **Developer:** runs `argus generate` locally and commits the updated files
3. **CI:** runs `argus generate --check` and fails the build if files are stale
4. **Developer:** sees the failure, runs `argus generate`, re-pushes
