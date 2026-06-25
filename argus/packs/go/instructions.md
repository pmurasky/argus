# Go

## Error Handling
- Return errors as values — do not panic for recoverable conditions
- Wrap errors with context using `fmt.Errorf("...: %w", err)`
- Unwrap and inspect errors with `errors.Is` and `errors.As`
- Check every returned error — never assign to `_` on a fallible call
- Reserve `panic` only for unrecoverable programmer bugs (invariant violations)
- Place the error return as the last return value in every function signature

## Interfaces and Composition
- Define interfaces at the consumer, not the producer
- Keep interfaces small — one or two methods is the target
- Rely on implicit interface satisfaction; do not declare `implements`
- Prefer struct embedding and composition over inheritance hierarchies
- Do not create an interface before a second implementation exists ("accept interfaces, return structs")
- Name single-method interfaces with the method name plus `-er` suffix (e.g. `Reader`, `Writer`)

## Goroutines and Concurrency
- Every goroutine must have a clear, guaranteed exit path — prevent goroutine leaks
- Propagate `context.Context` as the first parameter to every function that may block or be cancelled
- Use channels to transfer ownership of data between goroutines
- Use `sync.Mutex` or `sync.RWMutex` to guard shared mutable state
- Never use `time.Sleep` for synchronization — use channels or `sync.WaitGroup`
- Close channels from the sending side only; closing from the receiver causes panics

## Package and Naming
- Use lowercase, single-word package names — no underscores, no mixed case
- Exported identifiers use CamelCase; unexported identifiers use camelCase
- Avoid grab-bag package names: `utils`, `helpers`, `common`, `misc` are always wrong
- Use the `slices` and `maps` standard library packages (Go 1.21+) instead of manual index arithmetic
- Name package contents so they read well at the call site — avoid stutter like `http.HTTPServer`
- Group related functionality into focused packages; a package should have one clear responsibility

## Red Flags — Stop and Correct

| Violation | Fix |
|---|---|
| Ignored error return (`_ =` on a fallible call) | Handle or wrap the error |
| `panic` used for a recoverable condition | Return an `error` value |
| Interface defined with only one implementation | Delete it; use the concrete type |
| `time.Sleep` used to coordinate goroutines | Use a channel or `sync.WaitGroup` |
| `utils` / `helpers` / `common` package name | Name the package for its domain |
| Error not wrapped with `%w` when re-raised | Use `fmt.Errorf("context: %w", err)` |
| Context not propagated through a blocking function | Add `ctx context.Context` as first parameter |
