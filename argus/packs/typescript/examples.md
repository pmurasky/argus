## TypeScript Examples

### Unknown vs Any

**Avoid**
```typescript
function parse(raw: any) {
  return raw.value;
}
```

**Prefer**
```typescript
function parse(raw: unknown) {
  if (typeof raw === "object" && raw !== null && "value" in raw) {
    return (raw as { value: unknown }).value;
  }
  throw new Error("unexpected shape");
}
```

### Interface vs Type

**Avoid**
```typescript
interface Handler {
  (event: string): void;
}
type User = { id: string };
```

**Prefer**
```typescript
type Handler = (event: string) => void;
interface User {
  id: string;
}
```

### Constrained Generics

**Avoid**
```typescript
function getId<T>(item: T) {
  return item.id;
}
```

**Prefer**
```typescript
function getId<T extends { id: string }>(item: T): string {
  return item.id;
}
```

### Suppressing Errors

**Avoid**
```typescript
// @ts-ignore
widget.render();
```

**Prefer**
```typescript
// @ts-expect-error render is added by the plugin at runtime
widget.render();
```
