## Unreleased

### Fix

- **lint**: split long string in _claude_md to stay under 100 chars

### Refactor

- **claude**: slim CLAUDE.md to a rules pointer instead of inlining pack content

## v0.1.1 (2026-06-20)

### Feat

- **cli**: add --version flag

### Fix

- **test**: make version assertion version-agnostic

## v0.1.0 (2026-06-20)

### Feat

- **exceptions**: add ArgusError project base exception
- add testing-strategy pack checklist and examples
- add testing-strategy pack
- add refactoring pack checklist and examples
- add refactoring pack
- add dependency-injection and design-patterns packs
- add documentation-standards pack checklist and examples
- add documentation-standards pack
- add error-handling pack checklist and examples
- add error-handling pack
- add type-safety pack checklist and examples
- add type-safety pack
- add Skills 2.0 frontmatter to claude adapter skill files
- add init, packs, platforms, and validate CLI commands
- add generate command with --dry-run and --check
- add Copilot and Cursor adapters
- add OpenCode adapter
- add Claude Code adapter
- add pre-commit orchestrating pack — all 5 packs complete
- add code-quality pack with NIST-backed thresholds
- add solid pack
- add tdd pack
- add atomic-commit pack and pack schema tests
- add AdapterRegistry and Generator with deduplication
- add PackLoader with two-level search path
- add ArgusConfig with YAML loading
- add core data models Pack, GeneratedFile, BaseAdapter

### Fix

- **ci**: add types-PyYAML dev dependency to satisfy mypy import-untyped check
- **lint**: resolve ruff violations
- **types**: resolve mypy violations
- **generator**: UnknownPlatformError and AdapterConflictError inherit ArgusError
- **loader**: PackNotFoundError inherits ArgusError
- align checklist item with two-tier exception location rule
- clarify base exception location and system boundary in error-handling pack
- error handling in generate command and ArgusConfig validation
