## Next.js Examples

### Data fetching — useEffect in client vs async Server Component

**Avoid**
```tsx
'use client'

import { useState, useEffect } from 'react'

export default function ProductList() {
  const [products, setProducts] = useState([])

  useEffect(() => {
    fetch('/api/products').then(r => r.json()).then(setProducts)
  }, [])

  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>
}
```

**Prefer**
```tsx
// No 'use client' — this is a Server Component
async function getProducts() {
  const res = await fetch('https://api.example.com/products', { cache: 'force-cache' })
  return res.json()
}

export default async function ProductList() {
  const products = await getProducts()
  return <ul>{products.map((p: { id: string; name: string }) => <li key={p.id}>{p.name}</li>)}</ul>
}
```

---

### 'use client' placement — root layout vs leaf component

**Avoid**
```tsx
// app/layout.tsx
'use client'  // Forces the entire app into the client bundle

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html><body>{children}</body></html>
}
```

**Prefer**
```tsx
// app/layout.tsx — Server Component, no directive
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html><body>{children}</body></html>
}

// app/components/ThemeToggle.tsx — only this leaf needs the client
'use client'

import { useState } from 'react'

export function ThemeToggle() {
  const [dark, setDark] = useState(false)
  return <button onClick={() => setDark(d => !d)}>{dark ? 'Light' : 'Dark'}</button>
}
```

---

### Hook without 'use client' directive

**Avoid**
```tsx
// Missing 'use client' — will throw at runtime
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

**Prefer**
```tsx
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

---

### Speculative useMemo vs removing it

**Avoid**
```tsx
'use client'

import { useMemo } from 'react'

interface Props { items: string[] }

export function ItemBadge({ items }: Props) {
  // useMemo with no measured need — adds complexity, rarely helps
  const label = useMemo(() => items.join(', '), [items])
  return <span>{label}</span>
}
```

**Prefer**
```tsx
'use client'

interface Props { items: string[] }

export function ItemBadge({ items }: Props) {
  // Simple computation — no memoization needed until profiling shows a bottleneck
  const label = items.join(', ')
  return <span>{label}</span>
}
```
