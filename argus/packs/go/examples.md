## Go Examples

### Error Wrapping

**Avoid**
```go
func readConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, err
    }
    return parse(data)
}
```

**Prefer**
```go
func readConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("readConfig: %w", err)
    }
    return parse(data)
}
```

### Small Consumer-Side Interface

**Avoid**
```go
// producer package defines a large interface
type Store interface {
    Save(item Item) error
    Load(id string) (Item, error)
    Delete(id string) error
    List() ([]Item, error)
}

// consumer only needs Load
func display(s Store) { item, _ := s.Load("x") }
```

**Prefer**
```go
// consumer defines exactly what it needs
type ItemLoader interface {
    Load(id string) (Item, error)
}

func display(s ItemLoader) { item, _ := s.Load("x") }
```

### Context Propagation in Goroutine

**Avoid**
```go
func fetchAll(ids []string) []Result {
    results := make([]Result, len(ids))
    for i, id := range ids {
        go func(i int, id string) {
            results[i] = fetch(id)
        }(i, id)
    }
    return results
}
```

**Prefer**
```go
func fetchAll(ctx context.Context, ids []string) ([]Result, error) {
    var wg sync.WaitGroup
    results := make([]Result, len(ids))
    for i, id := range ids {
        wg.Add(1)
        go func(i int, id string) {
            defer wg.Done()
            results[i], _ = fetch(ctx, id)
        }(i, id)
    }
    wg.Wait()
    return results, nil
}
```

### Slices Package over Index Loop

**Avoid**
```go
func contains(items []string, target string) bool {
    for i := 0; i < len(items); i++ {
        if items[i] == target {
            return true
        }
    }
    return false
}
```

**Prefer**
```go
import "slices"

func contains(items []string, target string) bool {
    return slices.Contains(items, target)
}
```
