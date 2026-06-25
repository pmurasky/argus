# TypeScript

## Strict Mode
- Enable "strict": true in tsconfig.json — never disable individual strict flags
- Keep noImplicitAny on — every value must have a known or explicitly declared type
- Enable noUncheckedIndexedAccess so array and object index access is treated as possibly undefined
- Enable exactOptionalPropertyTypes to stop undefined leaking into optional properties

## Interface vs Type
- Use interface for object shapes that may be extended (public contracts, API payloads)
- Use type for unions, intersections, mapped types, and aliases to primitives
- Use a type alias with a function signature for function types — not an interface
- Prefer interface for public API shapes; declaration merging is a deliberate benefit

## Generics
- Name single-purpose type parameters T, K, V; use descriptive names (TItem, TKey) for complex ones
- Constrain a generic with extends whenever the body relies on a specific shape
- Never leave a generic unbounded when the function reads properties off it — constrain it
- Use unknown as the safe fallback in generic positions instead of any

## No-Any Discipline
- Never use any — use unknown for unknown values and narrow with type guards
- Never write `as any`; if a cast is unavoidable use `as unknown as T` with a justifying comment
- Never use @ts-ignore — use @ts-expect-error with an explanation
- Avoid Object, Function, and {} as types — they are too broad; declare the specific shape

## Red Flags — Stop and Correct

| Red Flag | Violation | Fix |
|----------|-----------|-----|
| `any` appearing anywhere a real type could be declared | No-Any Discipline | Replace with `unknown` and narrow |
| `as any` cast instead of `as unknown as T` with a reason | No-Any Discipline | Add cast chain and justifying comment |
| `@ts-ignore` suppressing an error | No-Any Discipline | Replace with `@ts-expect-error` and explanation |
| Individual strict flags disabled in tsconfig.json | Strict Mode | Remove the override and fix the underlying issue |
| `interface` used to alias a union or a primitive | Interface vs Type | Use `type` instead |
| Unbounded generic `<T>` whose body accesses properties of T | Generics | Add `extends` constraint |
