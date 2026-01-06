# Global Standards - AgentOS Tracker

**Version**: 2.0 | **Applies to**: All code | **Token-Optimized**

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14 (App Router) + TypeScript |
| **UI** | Tailwind CSS + shadcn/ui |
| **Database** | Supabase (PostgreSQL) |
| **Auth** | Supabase Auth (SSR) |
| **State** | TanStack Query (server) + Zustand (client) |
| **Testing** | Vitest + Playwright |
| **Deployment** | Vercel |

## Naming Conventions

### TypeScript

```typescript
// Variables & functions: camelCase
const userId = "123"
function getItemById(itemId: string): Item {}

// Components & Types: PascalCase
export function ItemCard({ item }: ItemCardProps) {}
interface ItemCardProps {
  item: Item
}

// Constants: UPPER_SNAKE_CASE
const MAX_FILE_SIZE = 5_000_000
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL

// Files:
// - Components: PascalCase (ItemCard.tsx)
// - Utils/hooks: camelCase (useAuth.ts, apiClient.ts)
// - Pages: lowercase with dashes (page.tsx in folders)
```

## Code Style

### Clean Functions

```typescript
// ✅ GOOD - Small, focused, single responsibility
export function hashPassword(password: string): string {
  return bcrypt.hashSync(password, 10)
}

export function verifyPassword(plain: string, hashed: string): boolean {
  return bcrypt.compareSync(plain, hashed)
}

// ❌ BAD - Too many responsibilities
export function handleUserAuthentication(email: string, password: string) {
  // Validates, hashes, creates user, sends email, logs in
  // 100 lines of mixed logic
}
```

### DRY Principle

```typescript
// ✅ GOOD - Reusable hook with TanStack Query
export function useProjects() {
  return useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const res = await fetch('/api/projects')
      if (!res.ok) throw new Error('Failed to fetch')
      return res.json()
    }
  })
}

// Usage in any component
const { data: projects, isLoading } = useProjects()

// ❌ BAD - Duplicated fetch logic in every component
```

### Remove Dead Code

```typescript
// ✅ GOOD - Clean, only what's needed
import { createClient } from '@/lib/supabase/server'

export async function getItems(userId: string) {
  const supabase = await createClient()
  const { data } = await supabase
    .from('items')
    .select('*')
    .eq('user_id', userId)
  return data
}

// ❌ BAD - Commented code, unused imports
// import { oldClient } from '@/lib/old'  // Old implementation
// import { format } from 'date-fns'  // Unused
```

## Code Comments

### When to Comment

```typescript
// ✅ GOOD - Explain WHY, not WHAT
export function ItemCard({ item }: ItemCardProps) {
  // Use React.memo to prevent re-renders when parent updates
  // but item data hasn't changed
  return useMemo(() => (
    <Card>
      <CardTitle>{item.title}</CardTitle>
    </Card>
  ), [item.id])
}

// ❌ BAD - Obvious comments
// Loop through items
items.forEach(item => {
  // Print item title
  console.log(item.title)
})
```

### Self-Documenting Code

```typescript
// ✅ GOOD - Code explains itself
function isItemOwner(item: Item, userId: string): boolean {
  return item.userId === userId
}

if (isItemOwner(item, currentUser.id)) {
  await deleteItem(item.id)
}

// ❌ BAD - Needs comment to understand
// Check if user can delete (is owner)
if (item.userId === currentUser.id) {
  await deleteItem(item.id)
}
```

## Error Handling

### User-Friendly Messages

```typescript
// ✅ GOOD - Clear, actionable (API Route)
export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validatedData = schema.parse(body)
    // ... create item
    return NextResponse.json({ data }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid data. Please check all required fields.' },
        { status: 400 }
      )
    }
    console.error('Failed to create item:', error)
    return NextResponse.json(
      { error: 'Unable to create item. Please try again.' },
      { status: 500 }
    )
  }
}

// ❌ BAD - Exposes technical details
catch (error) {
  return NextResponse.json({ error: error.message }, { status: 500 })
}
```

### Graceful Degradation

```typescript
// ✅ GOOD - Continue with cached data on error
export function useItems() {
  return useQuery({
    queryKey: ['items'],
    queryFn: fetchItems,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
    // Keep previous data while refetching
    placeholderData: keepPreviousData,
  })
}
```

## Input Validation

### Server-Side First (Zod)

```typescript
// ✅ GOOD - Validate on server with Zod
import { z } from 'zod'

export const itemSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().optional(),
})

export type ItemInput = z.infer<typeof itemSchema>

// In API Route
const validatedData = itemSchema.parse(body)
```

### Client-Side for UX

```typescript
// ✅ GOOD - Immediate feedback with React Hook Form + Zod
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

export function ItemForm() {
  const form = useForm<ItemInput>({
    resolver: zodResolver(itemSchema),
  })

  // Form validation happens automatically
}
```

## Version Control

### Commit Messages

```bash
# ✅ GOOD - Clear, descriptive
git commit -m "Add item search with pagination

- Implement /api/items/search with query parameter
- Add pagination (default 20, max 100)
- Include tests for search functionality"

# ❌ BAD - Vague
git commit -m "fix stuff"
git commit -m "updates"
```

### Branch Naming

```bash
# ✅ GOOD - Type/scope/description
feature/item-search
bugfix/login-token-expiry
hotfix/critical-security-patch

# ❌ BAD
my-changes
test
branch-1
```

## Project Structure

```
app/
├── (auth)/                  # Auth route group
│   ├── login/page.tsx
│   ├── signup/page.tsx
│   └── layout.tsx
├── (dashboard)/             # Protected route group
│   ├── page.tsx
│   ├── projects/page.tsx
│   └── layout.tsx
├── api/                     # API Routes
│   └── auth/
│       └── login/route.ts
├── layout.tsx               # Root layout
└── page.tsx                 # Landing page

components/
├── ui/                      # shadcn/ui components
├── features/                # Feature-specific
│   └── auth/
│       └── LoginForm.tsx
└── providers/               # Context providers

lib/
├── supabase/                # Supabase clients
│   ├── client.ts
│   ├── server.ts
│   └── middleware.ts
├── validations/             # Zod schemas
└── utils.ts

hooks/                       # Custom hooks
types/                       # TypeScript types
```

## Best Practices

1. **Naming**: Descriptive names, consistent conventions
2. **Functions**: Small, focused, single responsibility
3. **Comments**: Explain WHY, not WHAT. Code should be self-documenting
4. **Errors**: User-friendly messages, fail fast, graceful degradation
5. **Validation**: Server-side required, client-side for UX
6. **Dead Code**: Delete it, don't comment it out
7. **DRY**: Extract common logic into reusable hooks
8. **Version Control**: Clear commits, feature branches
9. **Structure**: Consistent, predictable organization
10. **No Secrets**: Use environment variables, never commit keys

---

**Token Count**: ~900 tokens
