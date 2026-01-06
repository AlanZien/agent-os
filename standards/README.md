# AgentOS Tracker - Standards

Standards de développement pour AgentOS Tracker.

## Stack Technique

| Couche | Technologie |
|--------|-------------|
| **Frontend** | Next.js 14 (App Router) |
| **UI** | Tailwind CSS + shadcn/ui |
| **Backend** | Next.js API Routes |
| **Database** | Supabase (PostgreSQL) |
| **Auth** | Supabase Auth (SSR) |
| **State** | TanStack Query + Zustand |
| **Testing** | Vitest + Playwright |

## Structure des Standards

```
standards/
├── frontend/
│   ├── nextjs/
│   │   └── nextjs-patterns.md     # Next.js 14 App Router patterns
│   └── ui/
│       └── shadcn-tailwind.md     # shadcn/ui + Tailwind CSS
│
├── integrations/
│   └── supabase/
│       └── supabase-auth.md       # Supabase Auth SSR patterns
│
├── testing/
│   └── vitest-playwright.md       # Vitest + Playwright E2E
│
├── global/                        # Standards universels
│   ├── global-standards.md        # Conventions générales
│   ├── security.md                # Sécurité (OWASP, auth)
│   ├── error-handling.md          # Gestion des erreurs
│   ├── api-contracts.md           # Contrats d'API
│   ├── git-workflow.md            # Git conventions
│   └── ci-cd-devops.md            # CI/CD
│
└── migrations/                    # Guides de migration
```

## Chargement par Contexte

| Travail sur... | Standards à charger |
|----------------|---------------------|
| **Pages/Layouts** | `nextjs-patterns` + `shadcn-tailwind` |
| **API Routes** | `nextjs-patterns` + `supabase-auth` + `api-contracts` |
| **Authentification** | `supabase-auth` + `security` |
| **Composants UI** | `shadcn-tailwind` |
| **Tests unitaires** | `vitest-playwright` |
| **Tests E2E** | `vitest-playwright` |
| **Base de données** | `supabase-auth` + `security` |

## Quick Reference

### Next.js 14 Patterns

```typescript
// Server Component (default)
export default async function Page() {
  const supabase = await createClient()
  const { data } = await supabase.from('items').select('*')
  return <ItemList items={data} />
}

// Client Component (interactivity)
'use client'
export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

### Supabase Auth

```typescript
// Server-side auth check
const supabase = await createClient()
const { data: { user } } = await supabase.auth.getUser()

if (!user) redirect('/login')
```

### shadcn/ui Form

```tsx
<Form {...form}>
  <FormField name="email" render={({ field }) => (
    <FormItem>
      <FormLabel>Email</FormLabel>
      <FormControl><Input {...field} /></FormControl>
      <FormMessage />
    </FormItem>
  )} />
</Form>
```

### Testing

```typescript
// Vitest
import { describe, it, expect } from 'vitest'

describe('validation', () => {
  it('validates email format', () => {
    expect(schema.safeParse({ email: 'bad' }).success).toBe(false)
  })
})

// Playwright E2E
test('user can login', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel(/email/i).fill('test@example.com')
  await page.getByRole('button', { name: /sign in/i }).click()
  await expect(page).toHaveURL('/dashboard')
})
```

## Sources Officielles

- [Next.js 14 Documentation](https://nextjs.org/docs)
- [Supabase Auth for Next.js](https://supabase.com/docs/guides/auth/server-side/nextjs)
- [shadcn/ui](https://ui.shadcn.com)
- [Vitest](https://vitest.dev)
- [Playwright](https://playwright.dev)

---

**Version**: 2.0 (Next.js + Supabase)
**Last Updated**: 2026-01-04
