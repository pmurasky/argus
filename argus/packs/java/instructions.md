# Java

## Modern Java Types
- Use `record` for immutable data carriers instead of mutable classes with getters/setters
- Use sealed classes with switch expressions for closed type hierarchies and ADTs
- Use `var` for local type inference where it improves readability; never use `var` for fields
- Use text blocks for multiline strings instead of string concatenation
- Use pattern matching for switch (Java 21+); use unnamed patterns with `_` (Java 22+)
- Prefer `List.of()`, `Map.of()`, and `Set.of()` for immutable collections

## Null Discipline
- Return `Optional<T>` for values that may be absent; never return `null` from a public API
- Use `Optional.orElseThrow()` rather than `Optional.get()` — never call `.get()` without a presence check
- Never use `Optional` as a field type or method parameter type
- Use `Objects.requireNonNull` to validate constructor and method arguments
- Annotate nullable parameters and return types with `@Nullable` where a null contract exists
- Prefer empty collections over `null` for absent collection results

## OOP Discipline
- Prefer composition over inheritance; favor interfaces over abstract classes
- Make classes `final` by default; document extension contracts explicitly when a class is non-final
- Keep interfaces narrow — one focused responsibility per interface (Interface Segregation)
- Avoid god classes (>300 lines); extract focused collaborator classes by responsibility
- Use a `record` instead of a mutable class for data-only objects without behavior

## Exception Handling
- Use unchecked exceptions for unrecoverable conditions; use checked exceptions for caller-recoverable conditions
- Never catch `Exception` or `Throwable` broadly; catch only the specific types you can handle
- Never use exceptions for control flow; return `Optional` or a result type instead
- Always throw the most specific exception type available
- Preserve the original cause when rethrowing: `throw new DomainError(msg, cause)`

## Red Flags — Stop and Correct
- `null` returned from a public method where `Optional<T>` fits
- `Optional.get()` called without a prior `isPresent()` check
- `catch (Exception e)` or `catch (Throwable t)` outside a top-level boundary handler
- Mutable data class with getters/setters where a `record` fits
- Non-final class with no documented extension contract
- `Optional` used as a field type or method parameter
