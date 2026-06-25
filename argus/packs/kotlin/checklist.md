## Kotlin Checklist

- [ ] Nullable types (`?`) used to model absence — no null without a nullable type
- [ ] `requireNotNull` / `checkNotNull` called at function entry points to enforce preconditions
- [ ] `!!` absent or accompanied by a comment proving non-null at that point
- [ ] `?.let { }` used for null-conditional blocks instead of nested null checks
- [ ] `data class` used for DTOs and value objects instead of manual `equals`/`hashCode`
- [ ] `when` expression used instead of `if/else` chain for multi-branch logic
- [ ] No coroutines launched in `GlobalScope` — structured scope used instead
- [ ] Blocking I/O inside coroutines wrapped in `withContext(Dispatchers.IO)`
- [ ] `Flow` used for streams of values, not callbacks
- [ ] String templates (`"$value"`) used instead of concatenation or `String.format`
- [ ] Java-interop boundaries guarded with explicit null checks before use
