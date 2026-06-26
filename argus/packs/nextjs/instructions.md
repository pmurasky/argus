# Next.js

## App Router Conventions
- Use the `app/` directory exclusively — App Router only, never the legacy `pages/` directory
- Map routes to folders: each route segment is a folder with a `page.tsx`
- Use `layout.tsx` for shared UI that persists across child routes (nav, providers)
- Use `loading.tsx` for route-level Suspense fallbacks and `error.tsx` for route error boundaries
- Co-locate route-specific components, but keep `page.tsx` thin and composed of smaller components
- Fetch data in Server Components with `async` components and `await` directly — no `useEffect` data fetching

## Server vs Client Components
- Default to Server Components — they render on the server and ship zero JS for that subtree
- Add the `'use client'` directive at the top of a file ONLY when it needs interactivity, state, or browser APIs
- Keep `'use client'` boundaries as low in the tree as possible to minimize client bundle size
- Never import a Server Component into a Client Component; pass it as `children` instead
- Mark server-only mutation functions with the `'use server'` directive (Server Actions)

## React Hooks Discipline
- Any file using a hook (`useState`, `useEffect`, `useRef`, custom hooks) MUST declare `'use client'`
- Never call hooks in a Server Component — Server Components do not re-render on the client
- Add `useCallback` / `useMemo` ONLY when there is a measured performance need, not by default
- Follow the rules of hooks: call them at the top level, never inside conditions or loops
- Prefer Server Components and Server Actions over client-side state where the work can run on the server

## TypeScript Integration
- Type route params and search params from the props Next.js passes to `page.tsx`
- Define explicit prop interfaces for every component (Server and Client)
- Type Server Action arguments and return values; never accept untyped `FormData` without parsing
- Use `Metadata` / `generateMetadata` typed exports for SEO instead of ad-hoc head tags
- Let async Server Components return typed data — the component is `async` and returns JSX

## Red Flags — Stop and Correct
- `pages/` directory, `getServerSideProps`, or `getStaticProps` (Pages Router — not allowed here)
- A hook used in a file that lacks the `'use client'` directive
- `'use client'` placed at the root layout, forcing the whole app into the client bundle
- Data fetched with `useEffect` in a component that could be an async Server Component
- `useCallback` / `useMemo` added speculatively without a measured performance need
- A Server Component imported into a Client Component instead of passed as `children`
