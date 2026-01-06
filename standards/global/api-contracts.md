# API Contracts - AgentOS Tracker

**Version**: 2.0 | **Scope**: Next.js API Routes + TypeScript | **Token-Optimized**

## Purpose

Ensure type definitions between server and client code remain synchronized to prevent runtime errors from field mismatches.

## Type Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Type Flow (Next.js)                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Zod Schema (source of truth)                               │
│       │                                                     │
│       ├──> TypeScript Type (inferred)                       │
│       │                                                     │
│       ├──> API Route validation                             │
│       │                                                     │
│       └──> Client-side form validation                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Single Source of Truth

**Zod schemas** are the source of truth. Types are inferred from schemas.

```typescript
// lib/validations/item.ts
import { z } from 'zod'

export const itemSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().optional(),
  status: z.enum(['active', 'completed', 'archived']),
})

// Infer TypeScript types
export type ItemInput = z.infer<typeof itemSchema>

// Response type with additional fields
export const itemResponseSchema = itemSchema.extend({
  id: z.string().uuid(),
  user_id: z.string().uuid(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
})

export type Item = z.infer<typeof itemResponseSchema>
```

## API Route Validation

```typescript
// app/api/items/route.ts
import { NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { itemSchema } from '@/lib/validations/item'

export async function POST(request: Request) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  try {
    const body = await request.json()
    const validatedData = itemSchema.parse(body)

    const { data, error } = await supabase
      .from('items')
      .insert({ ...validatedData, user_id: user.id })
      .select()
      .single()

    if (error) throw error
    return NextResponse.json({ data }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }
    return NextResponse.json(
      { error: 'Failed to create item' },
      { status: 500 }
    )
  }
}
```

## Client-Side Validation

```typescript
// components/features/items/ItemForm.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { itemSchema, type ItemInput } from '@/lib/validations/item'

export function ItemForm({ onSubmit }: { onSubmit: (data: ItemInput) => void }) {
  const form = useForm<ItemInput>({
    resolver: zodResolver(itemSchema),
    defaultValues: {
      title: '',
      description: '',
      status: 'active',
    },
  })

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  )
}
```

## Type Mapping

| Zod Type | TypeScript Type | Supabase Column |
|----------|-----------------|-----------------|
| `z.string()` | `string` | `text` / `varchar` |
| `z.number()` | `number` | `integer` / `numeric` |
| `z.boolean()` | `boolean` | `boolean` |
| `z.string().uuid()` | `string` | `uuid` |
| `z.string().datetime()` | `string` | `timestamptz` |
| `z.enum([...])` | `union type` | `enum` or `text` |
| `z.array(z.string())` | `string[]` | `text[]` |
| `z.string().optional()` | `string \| undefined` | `nullable` |
| `z.string().nullable()` | `string \| null` | `nullable` |

## API Response Format

### Success Response

```typescript
// Standard success response
interface ApiSuccessResponse<T> {
  data: T
}

// List response with pagination
interface ApiListResponse<T> {
  data: T[]
  meta: {
    total: number
    page: number
    limit: number
    hasMore: boolean
  }
}
```

### Error Response

```typescript
interface ApiErrorResponse {
  error: string
  details?: unknown
}
```

## Shared Types Organization

```
lib/
├── validations/           # Zod schemas (source of truth)
│   ├── auth.ts           # Auth-related schemas
│   ├── item.ts           # Item schemas
│   └── user.ts           # User schemas
│
types/
├── api.ts                # API response types
├── database.ts           # Supabase-generated types
└── index.ts              # Re-exports
```

## Supabase Type Generation

Generate TypeScript types from your Supabase schema:

```bash
# Generate types from Supabase
npx supabase gen types typescript --project-id YOUR_PROJECT_ID > types/database.ts

# Or from local development
npx supabase gen types typescript --local > types/database.ts
```

## Validation Checklist

When creating new API endpoints:

- [ ] Define Zod schema in `lib/validations/`
- [ ] Infer TypeScript type with `z.infer<typeof schema>`
- [ ] Validate request body with `schema.parse(body)`
- [ ] Handle `ZodError` for validation failures
- [ ] Use same schema on client for form validation
- [ ] Generate Supabase types if schema changes

## Common Patterns

### Optional vs Nullable

```typescript
// Optional - field can be omitted
const schema = z.object({
  description: z.string().optional(), // undefined ok
})

// Nullable - field can be null
const schema = z.object({
  avatar_url: z.string().nullable(), // null ok
})

// Both - can be omitted OR null
const schema = z.object({
  bio: z.string().optional().nullable(),
})
```

### Date Handling

```typescript
// Accept ISO string, validate format
const schema = z.object({
  due_date: z.string().datetime({ message: 'Invalid date format' }),
})

// Transform to Date object
const schemaWithTransform = z.object({
  due_date: z.string().datetime().transform((val) => new Date(val)),
})
```

### Discriminated Unions

```typescript
const notificationSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('email'),
    email: z.string().email(),
  }),
  z.object({
    type: z.literal('sms'),
    phone: z.string(),
  }),
])
```

---

**Token Count**: ~600 tokens | **Critical for**: API development
