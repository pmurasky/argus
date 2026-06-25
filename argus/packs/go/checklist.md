## Go Checklist

- [ ] Every returned error is checked — no `_ =` on fallible calls
- [ ] Errors wrapped with `fmt.Errorf("...: %w", err)` to preserve context
- [ ] `errors.Is` / `errors.As` used for error inspection — no string comparison
- [ ] `context.Context` is the first parameter of every blocking or cancellable function
- [ ] Every goroutine has a clear, guaranteed exit path
- [ ] Channels closed from the sending side only
- [ ] `sync.Mutex` or `sync.RWMutex` guards all shared mutable state
- [ ] `slices` and `maps` standard library packages used instead of manual index loops (Go 1.21+)
- [ ] Interfaces defined at the consumer, kept to one or two methods
- [ ] No grab-bag package names (`utils`, `helpers`, `common`)
- [ ] Exported names use CamelCase; unexported names use camelCase
- [ ] No stutter in package-qualified identifiers (e.g. avoid `http.HTTPServer`)
