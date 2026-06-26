## Next.js Checklist

- [ ] All routes live under `app/` — no `pages/` directory present
- [ ] Each route segment is a folder with `page.tsx`; `layout.tsx` used for shared UI
- [ ] `loading.tsx` and `error.tsx` used where route-level Suspense or error boundaries are needed
- [ ] Default to Server Components; `'use client'` added only where interactivity or browser APIs are required
- [ ] `'use client'` boundary placed as low in the component tree as possible
- [ ] Every file using a hook (`useState`, `useEffect`, custom hooks) declares `'use client'`
- [ ] No hooks called inside Server Components
- [ ] `useCallback` / `useMemo` added only when a measured performance need exists, not by default
- [ ] Every component (Server and Client) has an explicit prop interface
- [ ] Route params and search params are typed from the props Next.js passes to `page.tsx`
- [ ] Server Actions declare `'use server'` and have typed arguments and return values
- [ ] No Server Component imported directly into a Client Component (use `children` composition instead)
