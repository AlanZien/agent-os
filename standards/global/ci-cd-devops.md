# CI/CD & DevOps Standards - AgentOS Tracker

**Version**: 2.0 | **Stack**: GitHub Actions + Vercel | **Token-Optimized**

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Deployment Flow                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Push to develop  ──> Preview Deploy (Vercel)               │
│  Push to staging  ──> Staging Deploy (Vercel)               │
│  Push to main     ──> Production Deploy (Vercel)            │
│                                                             │
│  Supabase: Separate projects per environment                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## GitHub Actions Workflows

### Main CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main, staging, develop]
  pull_request:
    branches: [main, staging]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run TypeScript check
        run: npx tsc --noEmit

      - name: Run ESLint
        run: npm run lint

      - name: Run unit tests
        run: npm run test
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.TEST_SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.TEST_SUPABASE_ANON_KEY }}

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json

  e2e:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.TEST_SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.TEST_SUPABASE_ANON_KEY }}

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

### Security Scan

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --audit-level=moderate

      - name: Run TruffleHog (secrets scan)
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: main
          head: HEAD

      - name: Run Snyk (dependencies)
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## Vercel Configuration

### vercel.json

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "regions": ["cdg1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-DNS-Prefetch-Control", "value": "on" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "origin-when-cross-origin" }
      ]
    }
  ]
}
```

### Environment Variables (Vercel)

| Variable | Development | Preview | Production |
|----------|-------------|---------|------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Dev project | Staging project | Prod project |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Dev key | Staging key | Prod key |
| `SUPABASE_SERVICE_ROLE_KEY` | Dev key | Staging key | Prod key |

## Environment Strategy

| Environment | Git Branch | Vercel | Purpose |
|-------------|------------|--------|---------|
| **Development** | `develop` | Preview | Active development |
| **Staging** | `staging` | Preview | Pre-production testing |
| **Production** | `main` | Production | Live application |

**See full details:** `@agent-os/standards/global/environments.md`

## GitHub Secrets Configuration

### Required Secrets

```bash
# Supabase (per environment)
TEST_SUPABASE_URL          # For CI tests
TEST_SUPABASE_ANON_KEY     # For CI tests

# Security scanning
SNYK_TOKEN                 # Snyk dependency scanning

# Coverage reporting
CODECOV_TOKEN              # Code coverage uploads
```

### Vercel Environment Variables

Configure directly in Vercel Dashboard:
- Project Settings > Environment Variables
- Set different values per environment (Production, Preview, Development)

## Database Migrations

### Supabase Migrations

```bash
# Create new migration
npx supabase migration new add_user_avatar

# Apply locally
npx supabase db push

# Apply to production (via dashboard or CLI)
npx supabase db push --linked
```

### CI Migration Check

```yaml
# Add to CI workflow
- name: Check migrations
  run: |
    npx supabase db diff --linked
    if [ $? -ne 0 ]; then
      echo "Warning: Database schema has uncommitted changes"
    fi
```

## Monitoring & Logging

### Vercel Analytics

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
```

### Error Tracking (Sentry)

```typescript
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./sentry.server.config')
  }

  if (process.env.NEXT_RUNTIME === 'edge') {
    await import('./sentry.edge.config')
  }
}
```

```typescript
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.VERCEL_ENV || 'development',
  tracesSampleRate: 0.1,
})
```

### Structured Logging

```typescript
// lib/logger.ts
type LogLevel = 'info' | 'warn' | 'error'

interface LogEntry {
  level: LogLevel
  message: string
  timestamp: string
  [key: string]: unknown
}

export function log(level: LogLevel, message: string, data?: Record<string, unknown>) {
  const entry: LogEntry = {
    level,
    message,
    timestamp: new Date().toISOString(),
    ...data,
  }

  if (process.env.NODE_ENV === 'production') {
    console[level](JSON.stringify(entry))
  } else {
    console[level](message, data)
  }
}
```

## Best Practices Checklist

### CI/CD
- [ ] Tests run on every PR
- [ ] TypeScript check passes
- [ ] ESLint check passes
- [ ] E2E tests run before merge
- [ ] Security scans weekly
- [ ] Preview deploys for PRs
- [ ] Manual approval for production (optional)

### Vercel
- [ ] Environment variables per environment
- [ ] Security headers configured
- [ ] Analytics enabled
- [ ] Speed Insights enabled
- [ ] Region configured (CDG for Europe)

### Monitoring
- [ ] Error tracking with Sentry
- [ ] Structured logging
- [ ] Performance monitoring
- [ ] Uptime monitoring

### Database
- [ ] Migrations versioned
- [ ] Backup strategy defined
- [ ] RLS policies tested

---

**Token Count**: ~800 tokens | **Reusable for**: All Next.js + Vercel projects
