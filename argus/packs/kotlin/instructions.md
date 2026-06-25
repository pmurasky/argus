# Kotlin

## Null Safety
- Model absence with nullable types (`?`) and use safe calls (`?.`) for all nullable access
- Prefer `?.let { }` for null-conditional blocks over nested null checks
- Use `!!` only when provably non-null and add a comment explaining why
- Validate function entry points with `requireNotNull` / `checkNotNull` for precondition enforcement
- Explicitly guard Java-interop boundaries (platform types) with null checks before use

## Idiomatic Kotlin
- Use `data class` for DTOs and value objects instead of manual `equals`/`hashCode`
- Prefer `when` expressions over `if/else` chains for multi-branch logic
- Use destructuring declarations where they aid clarity (e.g., iterating map entries)
- Add behavior with extension functions instead of subclassing or utility classes
- Use `object` for singletons rather than static-method classes

## Coroutines
- Mark async functions `suspend` — never block a coroutine thread with blocking I/O
- Use `Flow` for streams of values instead of callbacks or observable wrappers
- Launch coroutines only within a structured scope, never `GlobalScope`
- Use `withContext(Dispatchers.IO)` for blocking I/O to avoid blocking the default dispatcher
- Cancel scopes when their work is done to prevent resource leaks

## Kotlin-over-Java Idioms
- Prefer the Kotlin collection API (`filter`, `map`, `flatMap`) over Java Streams
- Use string templates (`"$value"`) over concatenation or `String.format`
- Use scope functions purposefully with a consistent mental model: transform with `let`, configure with `apply`
- Prefer named and default parameters over overloaded constructors

## Red Flags — Stop and Correct
- `!!` used without an explanatory comment confirming it is provably non-null
- `GlobalScope.launch` used in production code
- `if/else` chain where a `when` expression fits more clearly
- Manual getter/setter class where a `data class` eliminates the boilerplate
- `String.format` where a string template reads better
- Blocking call inside a coroutine without `withContext(Dispatchers.IO)`
