# Environments Configuration - AgentOS Tracker

**Version**: 2.0 | **Stack**: Next.js + Supabase + Vercel | **Token-Optimized**

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    Environment Architecture                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Development (dev)          Staging (test)       Production  │
│  ┌────────────────┐        ┌────────────────┐   ┌─────────┐ │
│  │ Vercel Preview │   ──>  │ Vercel Preview │──>│ Vercel  │ │
│  │ Supabase Dev   │        │ Supabase Stage │   │ Prod    │ │
│  │ Branch: develop│        │ Branch: staging│   │ main    │ │
│  └────────────────┘        └────────────────┘   └─────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Environment Definitions

### Development (dev)

**Purpose:** Active development, rapid iteration, feature testing

**Characteristics:**
- Preview deploys on every push to `develop`
- Can have bugs and incomplete features
- Data can be reset/modified freely
- Performance not critical

**Git Branch:** `develop`
**Vercel:** Preview deployments
**Supabase Project:** `[project]-dev` (Free tier)

### Staging (test)

**Purpose:** Pre-production testing, QA validation

**Characteristics:**
- Deployments on PR merge to `staging`
- Should mirror production closely
- Data realistic but anonymized
- Performance should match production

**Git Branch:** `staging`
**Vercel:** Preview deployments
**Supabase Project:** `[project]-staging` (Free/Pro tier)

### Production (prod)

**Purpose:** Live application serving real users

**Characteristics:**
- Deployments only after full testing
- Zero downtime expected
- Real user data (strict data protection)
- Monitored 24/7

**Git Branch:** `main`
**Vercel:** Production deployment
**Supabase Project:** `[project]-prod` (Pro tier)

## Environment Variables

### Next.js Environment Files

```
project/
├── .env.local              # Local development (NEVER commit)
├── .env.development        # Development defaults
├── .env.production         # Production defaults
├── .env.example            # Template (safe to commit)
└── .gitignore              # Includes .env*
```

### Required Variables

```bash
# .env.local (local development)

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://[PROJECT_REF].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...  # Server-only

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Vercel Environment Variables

Configure in Vercel Dashboard per environment:

| Variable | Development | Preview | Production |
|----------|-------------|---------|------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Dev URL | Staging URL | Prod URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Dev key | Staging key | Prod key |
| `SUPABASE_SERVICE_ROLE_KEY` | Dev key | Staging key | Prod key |
| `NEXT_PUBLIC_APP_URL` | Preview URL | Preview URL | Prod URL |

### Supabase Projects

| Environment | Project Name | Plan | Cost |
|-------------|--------------|------|------|
| Development | `[project]-dev` | Free | $0/month |
| Staging | `[project]-staging` | Free | $0/month |
| Production | `[project]-prod` | Pro | $25+/month |

## Local Development Setup

### 1. Clone and Install

```bash
git clone [repo-url]
cd [project-name]
npm install
```

### 2. Environment Setup

```bash
# Copy example environment
cp .env.example .env.local

# Edit with your Supabase dev credentials
```

### 3. Supabase Local (Optional)

```bash
# Start local Supabase
npx supabase start

# Use local URLs
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=[from supabase start output]
SUPABASE_SERVICE_ROLE_KEY=[from supabase start output]
```

### 4. Run Development Server

```bash
npm run dev
# App available at http://localhost:3000
```

## Deployment Triggers

| Event | Environment | Automatic |
|-------|-------------|-----------|
| Push to `develop` | Development (Preview) | Yes |
| Push to `staging` | Staging (Preview) | Yes |
| Push to `main` | Production | Yes |
| PR to any branch | Preview | Yes |

## Database Migrations

### Development

```bash
# Create migration
npx supabase migration new [migration_name]

# Apply to local
npx supabase db push

# Reset local database
npx supabase db reset
```

### Staging & Production

```bash
# Link to Supabase project
npx supabase link --project-ref [PROJECT_REF]

# Push migrations
npx supabase db push

# Generate types
npx supabase gen types typescript --linked > types/database.ts
```

## Security Requirements

| Setting | Development | Staging | Production |
|---------|-------------|---------|------------|
| HTTPS | Optional | Required | Required |
| RLS Policies | Optional | Required | Required |
| Service Key Access | Allowed | Restricted | Restricted |
| Data Anonymization | Not required | Required | N/A (real data) |

## Monitoring per Environment

### Development
- Console logging
- Supabase Studio dashboard
- Browser DevTools

### Staging
- Vercel Analytics (preview)
- Sentry error tracking
- Log aggregation

### Production
- Vercel Analytics
- Sentry with alerting
- Supabase Dashboard
- Uptime monitoring

## Environment-Specific Behavior

### Agent Access

| Agent | Development | Staging | Production |
|-------|-------------|---------|------------|
| Direct pushes | ✅ develop only | ❌ | ❌ |
| Database access | ✅ Full | ⚠️ Read-only | ❌ |
| Deploy triggers | ✅ | ✅ via PR | ✅ via PR |

### Feature Flags

```typescript
// lib/config.ts
export const config = {
  isDev: process.env.NODE_ENV === 'development',
  isPreview: process.env.VERCEL_ENV === 'preview',
  isProd: process.env.VERCEL_ENV === 'production',
}

// Usage
if (config.isDev) {
  // Development-only code
}
```

## Cost Estimation

| Service | Development | Staging | Production |
|---------|-------------|---------|------------|
| Vercel | Free | Free | Free (hobby) / $20/month (Pro) |
| Supabase | Free | Free | $25+/month |
| **Total** | $0/month | $0/month | $25-45+/month |

## Quick Reference

### Environment Detection

```typescript
// Server-side
const env = process.env.VERCEL_ENV || 'development'

// Client-side
const isDev = process.env.NODE_ENV === 'development'
```

### Environment Verification

```bash
# Check current environment
echo $VERCEL_ENV

# Test Supabase connection
npx supabase db diff

# Verify deployment
curl https://[your-app].vercel.app/api/health
```

## Related Documentation

- Git Workflow: `@agent-os/standards/global/git-workflow.md`
- CI/CD Pipeline: `@agent-os/standards/global/ci-cd-devops.md`
- Security Standards: `@agent-os/standards/global/security.md`
- Supabase Auth: `@agent-os/standards/integrations/supabase/supabase-auth.md`

---

**Token Count**: ~700 tokens
