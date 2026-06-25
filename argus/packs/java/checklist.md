## Java Checklist

- [ ] `record` used for immutable data carriers instead of mutable classes with getters/setters
- [ ] No `null` returned from a public API — `Optional<T>` used for absent values
- [ ] `Optional.orElseThrow()` used instead of `Optional.get()`
- [ ] `Optional` not used as a field type or method parameter type
- [ ] `Objects.requireNonNull` used to validate constructor and method arguments
- [ ] Classes are `final` by default; extension contracts documented explicitly
- [ ] Composition preferred over inheritance; interfaces preferred over abstract classes
- [ ] Interfaces are narrow — one focused responsibility each
- [ ] No broad `catch (Exception e)` — only specific, recoverable exception types caught
- [ ] Exceptions not used for control flow — `Optional` or result type used instead
- [ ] Original cause preserved when rethrowing: `throw new XError(msg, cause)`
- [ ] `List.of()` / `Map.of()` / `Set.of()` used for immutable collections
