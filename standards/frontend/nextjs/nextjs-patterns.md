# Next.js 14 Standards

> **Source:** [Next.js Official Documentation](https://nextjs.org/docs) (App Router)

## Overview

Standards et patterns pour Next.js 14 avec App Router, TypeScript et Server Components.

## Structure des dossiers

```
app/
├── (auth)/                    # Route group pour pages auth (pas de layout dashboard)
│   ├── login/page.tsx
│   ├── signup/page.tsx
│   └── layout.tsx             # Auth-specific layout
├── (dashboard)/               # Route group pour pages protégées
│   ├── page.tsx               # Dashboard home
│   └── layout.tsx             # Dashboard layout avec sidebar
├── api/                       # API Routes
│   └── auth/
│       ├── login/route.ts
│       └── signup/route.ts
├── layout.tsx                 # Root layout
├── page.tsx                   # Landing page
└── globals.css

components/
├── ui/                        # shadcn/ui components
├── features/                  # Feature-specific components
│   └── auth/
│       ├── LoginForm.tsx
│       └── SignupForm.tsx
└── providers/                 # Context providers
    └── QueryProvider.tsx

lib/
├── supabase/                  # Supabase clients
│   ├── client.ts              # Browser client
│   ├── server.ts              # Server client
│   └── middleware.ts          # Middleware helpers
├── validations/               # Zod schemas
└── utils.ts                   # Utility functions

hooks/                         # Custom React hooks
types/                         # TypeScript types
```

## App Router Conventions

### Page Components

```typescript
// app/(dashboard)/projects/page.tsx
import { createClient } from '@/lib/supabase/server'

// Metadata
export const metadata = {
  title: 'Projects | AgentOS Tracker',
  description: 'Manage your projects'
}

// Server Component par défaut
export default async function ProjectsPage() {
  const supabase = await createClient()
  const { data: projects } = await supabase
    .from('projects')
    .select('*')
    .order('created_at', { ascending: false })

  return (
    <div>
      <h1>Projects</h1>
      <ProjectList projects={projects} />
    </div>
  )
}
```

### Layout Components

```typescript
// app/(dashboard)/layout.tsx
import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import { Sidebar } from '@/components/features/dashboard/Sidebar'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="flex h-screen">
      <Sidebar user={user} />
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  )
}
```

### Loading States

```typescript
// app/(dashboard)/projects/loading.tsx
import { Skeleton } from '@/components/ui/skeleton'

export default function ProjectsLoading() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-48" />
      <Skeleton className="h-64 w-full" />
    </div>
  )
}
```

### Error Handling

```typescript
// app/(dashboard)/projects/error.tsx
'use client'

export default function ProjectsError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <h2 className="text-lg font-semibold text-red-500">
        Something went wrong
      </h2>
      <p className="text-muted-foreground">{error.message}</p>
      <button onClick={reset} className="mt-4">
        Try again
      </button>
    </div>
  )
}
```

## API Routes

### Route Handlers

```typescript
// app/api/projects/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { projectSchema } from '@/lib/validations/project'
import { z } from 'zod'

// GET /api/projects
export async function GET(request: NextRequest) {
  try {
    const supabase = await createClient()
    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const { data, error } = await supabase
      .from('projects')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error

    return NextResponse.json({ data })
  } catch (error) {
    console.error('GET /api/projects error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// POST /api/projects
export async function POST(request: NextRequest) {
  try {
    const supabase = await createClient()
    const { data: { user } } = await supabase.auth.getUser()

    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const body = await request.json()
    const validatedData = projectSchema.parse(body)

    const { data, error } = await supabase
      .from('projects')
      .insert({ ...validatedData, user_id: user.id })
      .select()
      .single()

    if (error) throw error

    return NextResponse.json({ data }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation error', details: error.errors },
        { status: 400 }
      )
    }
    console.error('POST /api/projects error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### Dynamic Routes

```typescript
// app/api/projects/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params
  // ...
}
```

## Server vs Client Components

### Server Components (default)

- Fetch data directly
- Access backend resources
- Keep sensitive information
- No useState, useEffect, event handlers

```typescript
// Server Component
async function ServerComponent() {
  const data = await fetchData() // Direct fetch
  return <div>{data}</div>
}
```

### Client Components

- Interactivity (onClick, onChange, etc.)
- useState, useEffect, useContext
- Browser APIs
- Custom hooks with state

```typescript
// Client Component
'use client'

import { useState } from 'react'

export function ClientComponent() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

### Pattern: Server Component with Client Islands

```typescript
// Server Component (page)
import { ClientForm } from './ClientForm'

export default async function Page() {
  const initialData = await fetchData()

  return (
    <div>
      <h1>Server rendered title</h1>
      <ClientForm initialData={initialData} /> {/* Client island */}
    </div>
  )
}
```

## Middleware

```typescript
// middleware.ts
import { NextResponse, type NextRequest } from 'next/server'
import { updateSession } from '@/lib/supabase/middleware'

export async function middleware(request: NextRequest) {
  return await updateSession(request)
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

## Data Fetching Patterns

### Server Component Fetching

```typescript
// Parallel fetching
async function Page() {
  const [projects, tasks] = await Promise.all([
    fetchProjects(),
    fetchTasks()
  ])
  return <Dashboard projects={projects} tasks={tasks} />
}
```

### TanStack Query for Client Components

```typescript
'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

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

export function useCreateProject() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: CreateProjectInput) => {
      const res = await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!res.ok) throw new Error('Failed to create')
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
    }
  })
}
```

## TypeScript Conventions

### Prop Types

```typescript
// Prefer interface for component props
interface ButtonProps {
  variant?: 'default' | 'destructive' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
}

// Use type for unions/intersections
type Status = 'pending' | 'in_progress' | 'done'
```

### Server Action Types

```typescript
// lib/actions/project.ts
'use server'

import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1),
  description: z.string().optional()
})

export async function createProject(formData: FormData) {
  const validatedFields = schema.safeParse({
    name: formData.get('name'),
    description: formData.get('description')
  })

  if (!validatedFields.success) {
    return { error: 'Invalid fields' }
  }

  // Create project...

  revalidatePath('/projects')
  return { success: true }
}
```

## Performance Best Practices

1. **Use Server Components** by default
2. **Minimize client JavaScript** with selective 'use client'
3. **Parallel data fetching** with Promise.all
4. **Dynamic imports** for heavy components:
   ```typescript
   const HeavyChart = dynamic(() => import('./HeavyChart'), {
     loading: () => <Skeleton />
   })
   ```
5. **Image optimization** with next/image
6. **Route prefetching** with Link component

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx

# Server-only (no NEXT_PUBLIC_ prefix)
SUPABASE_SERVICE_ROLE_KEY=xxx
```

Access:
- Client: `process.env.NEXT_PUBLIC_*`
- Server: `process.env.*`
