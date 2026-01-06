# Security Standards - AgentOS Tracker

**Version**: 2.0 | **Scope**: Next.js + Supabase | **Token-Optimized**

## OWASP Top 10 Mitigation

### 1. Broken Access Control

```typescript
// API Route - Verify ownership before deletion
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Verify ownership before deletion
  const { data: item } = await supabase
    .from('items')
    .select('user_id')
    .eq('id', params.id)
    .single()

  if (item?.user_id !== user.id) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
  }

  await supabase.from('items').delete().eq('id', params.id)
  return NextResponse.json({ status: 'deleted' })
}
```

### 2. Cryptographic Failures

```typescript
// Password hashing with bcrypt
import bcrypt from 'bcryptjs'

export function hashPassword(password: string): string {
  return bcrypt.hashSync(password, 10)
}

export function verifyPassword(plain: string, hashed: string): boolean {
  return bcrypt.compareSync(plain, hashed)
}

// NEVER store plain passwords
// NEVER use weak algorithms (MD5, SHA1)
// ALWAYS use bcrypt, argon2, or scrypt
```

### 3. Injection (SQL, NoSQL, Command)

```typescript
// ✅ SAFE - Supabase uses parameterized queries
const { data } = await supabase
  .from('items')
  .select('*')
  .eq('user_id', userId)

// ❌ DANGEROUS - Never do string interpolation
const query = `SELECT * FROM items WHERE user_id = '${userId}'`

// Input validation with Zod
import { z } from 'zod'

export const itemSchema = z.object({
  title: z.string()
    .min(1)
    .max(200)
    .refine(
      (val) => !['<', '>', ';', '--'].some(char => val.includes(char)),
      'Invalid characters in title'
    ),
})
```

### 4. Insecure Design

```typescript
// Rate limiting in middleware
// Note: For production, use Vercel's rate limiting or upstash/ratelimit

import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, '1 m'), // 5 requests per minute
})

// In API route
const ip = request.headers.get('x-forwarded-for') ?? 'unknown'
const { success } = await ratelimit.limit(ip)

if (!success) {
  return NextResponse.json(
    { error: 'Too many requests' },
    { status: 429 }
  )
}
```

### 5. Security Misconfiguration

```typescript
// next.config.js - Security headers
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin'
  }
]

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ]
  },
}
```

### 6. Vulnerable Components

```bash
# Regular dependency updates
npm outdated
npm audit

# Fix vulnerabilities
npm audit fix

# Pin versions in production
# package.json - use exact versions
"dependencies": {
  "next": "14.0.4",  # Not "^14.0.4"
}
```

### 7. Authentication Failures

```typescript
// Supabase handles JWT automatically
// Key security: ALWAYS use getUser() server-side

// ✅ CORRECT - Validates JWT signature
const { data: { user } } = await supabase.auth.getUser()

// ❌ INCORRECT - Can be spoofed
const { data: { session } } = await supabase.auth.getSession()

// Session configuration in Supabase Dashboard:
// - Access token expiry: 1 hour (default)
// - Refresh token expiry: 7-30 days
// - Enable "Secure email change" and "Secure password change"
```

### 8. Data Integrity Failures

```typescript
// File upload validation
import { NextResponse } from 'next/server'

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']
const MAX_SIZE = 5 * 1024 * 1024 // 5MB

export async function POST(request: Request) {
  const formData = await request.formData()
  const file = formData.get('file') as File | null

  if (!file) {
    return NextResponse.json({ error: 'No file' }, { status: 400 })
  }

  // Check file size
  if (file.size > MAX_SIZE) {
    return NextResponse.json({ error: 'File too large' }, { status: 400 })
  }

  // Verify actual file type
  if (!ALLOWED_TYPES.includes(file.type)) {
    return NextResponse.json({ error: 'Invalid file type' }, { status: 400 })
  }

  // Upload to Supabase Storage
  const supabase = await createClient()
  const { data, error } = await supabase.storage
    .from('uploads')
    .upload(`${Date.now()}-${file.name}`, file)

  if (error) throw error
  return NextResponse.json({ data })
}
```

### 9. Logging & Monitoring

```typescript
// Secure logging - NEVER log sensitive data

// ✅ GOOD - Log security events
console.warn(`Failed login attempt for: ${email}`)
console.info(`User ${userId} accessed resource`)

// ❌ BAD - Never log sensitive data
console.info(`Password: ${password}`)  // NEVER
console.debug(`JWT: ${token}`)         // NEVER

// Use structured logging for production
// Consider: pino, winston, or Vercel's built-in logging
```

### 10. Server-Side Request Forgery (SSRF)

```typescript
// URL validation for external requests
const ALLOWED_DOMAINS = ['api.trusted-service.com']

export async function fetchExternalData(url: string) {
  const parsed = new URL(url)

  // Validate domain
  if (!ALLOWED_DOMAINS.includes(parsed.hostname)) {
    throw new Error('Untrusted domain')
  }

  // Prevent internal network access
  if (
    parsed.hostname === 'localhost' ||
    parsed.hostname === '127.0.0.1' ||
    parsed.hostname.startsWith('192.168.')
  ) {
    throw new Error('Invalid URL')
  }

  const response = await fetch(url, { signal: AbortSignal.timeout(5000) })
  return response.json()
}
```

## Environment Variables & Secrets

```bash
# .env.local (NEVER commit)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...  # Server-only

# .env.example (commit this as template)
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

```typescript
// Validate environment at startup
if (!process.env.NEXT_PUBLIC_SUPABASE_URL) {
  throw new Error('Missing NEXT_PUBLIC_SUPABASE_URL')
}
```

## Row Level Security (Supabase)

```sql
-- Enable RLS on all tables
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Users can only see their own items
CREATE POLICY "Users can view own items"
  ON items FOR SELECT
  USING (auth.uid() = user_id);

-- Users can only update their own items
CREATE POLICY "Users can update own items"
  ON items FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can only delete their own items
CREATE POLICY "Users can delete own items"
  ON items FOR DELETE
  USING (auth.uid() = user_id);

-- Users can insert items for themselves
CREATE POLICY "Users can insert own items"
  ON items FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

## Security Checklist

### Server-Side (API Routes)
- [ ] Use `getUser()` not `getSession()` for auth
- [ ] Validate all input with Zod
- [ ] Check ownership before mutations
- [ ] Rate limit sensitive endpoints
- [ ] Return generic error messages
- [ ] Log security events (not sensitive data)
- [ ] Enable RLS on all Supabase tables

### Client-Side
- [ ] No secrets in client code
- [ ] HTTPS only (automatic on Vercel)
- [ ] Validate input before submission
- [ ] Handle auth errors gracefully
- [ ] Clear sensitive data on logout

### Infrastructure
- [ ] Security headers configured
- [ ] Dependencies updated monthly
- [ ] npm audit run before releases
- [ ] Environment variables secured
- [ ] Supabase RLS enabled

---

**Token Count**: ~1000 tokens
