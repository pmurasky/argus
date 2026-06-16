## Testing Strategy Pre-Commit Checklist

- [ ] New business logic is tested at the unit level — not only through integration or E2E
- [ ] Integration tests cover system boundaries only (DB, APIs, file I/O) — not business logic
- [ ] E2E tests added only for new critical user journeys, not for every new feature
- [ ] Test doubles are the simplest type that works — prefer fake/stub over mock
- [ ] No mock asserting on an internal or private method call
- [ ] No unit test hitting a real database, network, or file system
- [ ] Unit tests pass before commit; integration tests pass before push
