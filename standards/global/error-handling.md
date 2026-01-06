# Error & Blocking Management - AgentOS Tracker

**Version**: 2.0 | **Applies to**: All agents | **Token-Optimized**

## Overview

This document defines how agents should handle errors, blocking situations, and escalation to ensure visibility and proper tracking.

## Error Categories

| Category | Description | Action |
|----------|-------------|--------|
| **Recoverable** | Temporary issues (network, timeout) | Retry up to 3 times, then escalate |
| **Fixable** | Code/config errors agent can fix | Attempt fix, verify, continue |
| **Blocking** | Cannot proceed without help | Log + alert user |
| **Critical** | Security/data integrity at risk | Stop immediately + alert user |

## Blocking Detection

An agent is **blocked** when ANY of these conditions are met:

1. **Time threshold exceeded**: Spent >30 minutes on single issue without progress
2. **Retry exhausted**: Same error after 3 fix attempts
3. **Missing dependency**: Required file/service/credential unavailable
4. **Ambiguous requirements**: Spec contradicts itself or is unclear
5. **Permission denied**: Cannot access required resource
6. **External service down**: Third-party API/service unavailable

## Escalation Protocol

### Step 1: Detect Blocking Condition

```
IF (time_on_issue > 30 minutes) OR
   (fix_attempts >= 3) OR
   (missing_critical_dependency) OR
   (ambiguous_requirements)
THEN → BLOCKED
```

### Step 2: Alert User

Output a clear alert:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 BLOCKED - Need Human Input
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: {brief description}
Spec: {spec-path}
Time spent: {X} minutes
Attempts: {N}

What I tried:
1. {attempt 1}
2. {attempt 2}
3. {attempt 3}

Error:
{error message}

Options:
1. Provide guidance to continue
2. Skip this task for now
3. Modify requirements

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 3: Wait for User Response

**DO NOT** continue with other tasks until user responds with one of:
- Guidance to resolve the issue
- Permission to skip
- Modified requirements

## Error Handling in Code

### API Routes

```typescript
// app/api/items/route.ts
import { NextResponse } from 'next/server'
import { z } from 'zod'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validatedData = schema.parse(body)

    // ... process data

    return NextResponse.json({ data }, { status: 201 })
  } catch (error) {
    // Validation errors
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid data. Please check all required fields.' },
        { status: 400 }
      )
    }

    // Log error for debugging (not sensitive data)
    console.error('Failed to create item:', error)

    // User-friendly message
    return NextResponse.json(
      { error: 'Unable to create item. Please try again.' },
      { status: 500 }
    )
  }
}
```

### Client Components

```typescript
// components/features/items/ItemForm.tsx
'use client'

import { toast } from 'sonner'

async function handleSubmit(data: ItemInput) {
  try {
    const response = await fetch('/api/items', {
      method: 'POST',
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Something went wrong')
    }

    toast.success('Item created successfully')
  } catch (error) {
    toast.error(error instanceof Error ? error.message : 'Failed to create item')
  }
}
```

### TanStack Query Error Handling

```typescript
// hooks/useItems.ts
import { useQuery, useMutation } from '@tanstack/react-query'
import { toast } from 'sonner'

export function useCreateItem() {
  return useMutation({
    mutationFn: createItem,
    onError: (error) => {
      toast.error(error.message || 'Failed to create item')
    },
    onSuccess: () => {
      toast.success('Item created')
    },
  })
}
```

## Error Messages

### User-Facing Messages

| Situation | Message |
|-----------|---------|
| Validation error | "Please check the highlighted fields" |
| Network error | "Connection lost. Please check your internet" |
| Auth error | "Please sign in to continue" |
| Not found | "This item doesn't exist or was deleted" |
| Server error | "Something went wrong. Please try again" |
| Rate limit | "Too many requests. Please wait a moment" |

### Never Expose

- ❌ Database connection strings
- ❌ Stack traces
- ❌ Internal error codes
- ❌ SQL errors
- ❌ Environment variable names

## Integration Points

This error handling applies to ALL agents:

| Agent | When to Apply |
|-------|---------------|
| `spec-shaper` | Requirements unclear after follow-up questions |
| `spec-writer` | Cannot determine technical approach |
| `task-list-creator` | Dependencies cannot be resolved |
| `implementer` | Code/test failures after 30 min |
| `implementation-verifier` | Cannot run verification steps |

## Best Practices

1. **Be specific**: Include exact error messages, not summaries
2. **Show attempts**: Document what was tried before escalating
3. **Provide options**: Give user actionable choices
4. **Don't loop**: If blocked, stop and wait - don't retry indefinitely
5. **Context is key**: Include spec path, task being worked on, and relevant code
6. **Graceful degradation**: Keep UI functional even when errors occur
7. **Log appropriately**: Log errors server-side, show friendly messages client-side

---

**Token Count**: ~500 tokens
