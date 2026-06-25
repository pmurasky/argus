## TypeScript Checklist

- [ ] "strict": true set in tsconfig.json — no individual strict flag disabled
- [ ] noImplicitAny enabled — no implicit any anywhere
- [ ] noUncheckedIndexedAccess enabled for index safety
- [ ] No any in the codebase — unknown used and narrowed with type guards
- [ ] No `as any` casts — `as unknown as T` with a comment where unavoidable
- [ ] @ts-expect-error used instead of @ts-ignore
- [ ] interface used for object shapes; type used for unions and aliases
- [ ] Function types declared with a type alias, not an interface
- [ ] Generics constrained with extends when the body needs a shape
- [ ] No Object, Function, or {} used as a type
