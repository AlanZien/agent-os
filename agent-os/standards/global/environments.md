# Environments Configuration

This document defines the development, staging, and production environments for this project. All agents and developers must understand and respect these environment boundaries.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    Environment Architecture                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Development (dev)          Staging (test)       Production │
│  ┌────────────────┐        ┌────────────────┐   ┌─────────┐ │
│  │ Local/Cloud DB │   ──>  │ Cloud Database │──>│ Cloud DB│ │
│  │ Feature testing│        │ QA & Testing   │   │ Live    │ │
│  │ Branch: develop│        │ Branch: staging│   │ main    │ │
│  └────────────────┘        └────────────────┘   └─────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Environment Definitions

### Development (dev)

**Purpose:** Active development, rapid iteration, feature testing

**Characteristics:**
- Frequent deployments (on every push to `develop`)
- Can have bugs and incomplete features
- Data can be reset/modified freely
- Used by developers daily
- Performance not critical

**Git Branch:** `develop`

**Access:**
- Developers: Full access
- Agents: Full access
- Public: No access

---

### Staging (test)

**Purpose:** Pre-production testing, QA validation, client demos

**Characteristics:**
- Deployments on PR merge to `staging`
- Should mirror production closely
- Data should be realistic but anonymized
- Used for final testing before production release
- Performance should match production

**Git Branch:** `staging`

**Access:**
- Developers: Full access
- QA Team: Full access
- Agents: Read access (for verification)
- Clients: Demo access (optional)
- Public: No access

---

### Production (prod)

**Purpose:** Live application serving real users

**Characteristics:**
- Deployments only after full testing
- Zero downtime expected
- Real user data (strict data protection)
- High performance required
- Monitored 24/7

**Git Branch:** `main`

**Access:**
- System Administrators: Full access
- Developers: Limited access (read-only)
- Agents: No direct access (only via approved PRs)
- Public: Application access only

---

## Environment Configuration

### Database Configuration

#### Option 1: Supabase (Recommended)

```bash
# Development - Supabase Project 1 OR Local
# Option A: Cloud (Recommended for team)
DATABASE_URL=postgresql://postgres:[DEV_PASSWORD]@db.[DEV_PROJECT_REF].supabase.co:5432/postgres
SUPABASE_URL=https://[DEV_PROJECT_REF].supabase.co
SUPABASE_ANON_KEY=[DEV_ANON_KEY]
SUPABASE_SERVICE_KEY=[DEV_SERVICE_KEY]

# Option B: Local (via Supabase CLI)
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=[from supabase start output]
SUPABASE_SERVICE_KEY=[from supabase start output]

# Staging - Supabase Project 2
DATABASE_URL=postgresql://postgres:[STAGING_PASSWORD]@db.[STAGING_PROJECT_REF].supabase.co:5432/postgres
SUPABASE_URL=https://[STAGING_PROJECT_REF].supabase.co
SUPABASE_ANON_KEY=[STAGING_ANON_KEY]
SUPABASE_SERVICE_KEY=[STAGING_SERVICE_KEY]

# Production - Supabase Project 3 (Pro Plan)
DATABASE_URL=postgresql://postgres:[PROD_PASSWORD]@db.[PROD_PROJECT_REF].supabase.co:5432/postgres
SUPABASE_URL=https://[PROD_PROJECT_REF].supabase.co
SUPABASE_ANON_KEY=[PROD_ANON_KEY]
SUPABASE_SERVICE_KEY=[PROD_SERVICE_KEY]
```

**Supabase Projects:**
| Environment | Project Name | Plan | Cost |
|-------------|--------------|------|------|
| Development | `[project]-dev` | Free | $0/month |
| Staging | `[project]-staging` | Free/Pro | $0-25/month |
| Production | `[project]-prod` | Pro | $25+/month |

**Notes:**
- Development can use either cloud (Free tier) or local (Supabase CLI)
- Staging should mirror production configuration
- Production requires Pro plan for production-grade features (backups, support, etc.)

---

#### Option 2: Other PostgreSQL Provider

```bash
# Development
DATABASE_URL=postgresql://user:password@dev-db-host:5432/dbname

# Staging
DATABASE_URL=postgresql://user:password@staging-db-host:5432/dbname

# Production
DATABASE_URL=postgresql://user:password@prod-db-host:5432/dbname
```

---

### API Endpoints

```bash
# Development
API_URL=http://localhost:8000
# OR for cloud dev
API_URL=https://dev-api.yourproject.com

# Staging
API_URL=https://staging-api.yourproject.com

# Production
API_URL=https://api.yourproject.com
```

---

### Frontend URLs

```bash
# Development
FRONTEND_URL=http://localhost:3000
# OR
FRONTEND_URL=https://dev.yourproject.com

# Staging
FRONTEND_URL=https://staging.yourproject.com

# Production
FRONTEND_URL=https://yourproject.com
```

---

### Authentication & Security

```bash
# Development
JWT_SECRET=dev-secret-key-change-me-in-production
SESSION_SECRET=dev-session-secret
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Staging
JWT_SECRET=[STAGING_JWT_SECRET_32_CHARS_MIN]
SESSION_SECRET=[STAGING_SESSION_SECRET]
ALLOWED_ORIGINS=https://staging.yourproject.com,https://staging-api.yourproject.com

# Production
JWT_SECRET=[PROD_JWT_SECRET_64_CHARS_RECOMMENDED]
SESSION_SECRET=[PROD_SESSION_SECRET]
ALLOWED_ORIGINS=https://yourproject.com,https://api.yourproject.com
```

**Security Requirements:**
| Setting | Development | Staging | Production |
|---------|-------------|---------|------------|
| JWT Secret Length | 32+ chars | 32+ chars | 64+ chars |
| Rotation | Never | Quarterly | Monthly |
| Storage | .env file | Secrets manager | Secrets manager |
| HTTPS Required | No | Yes | Yes |

---

### Third-Party Services

#### Notion Integration

```bash
# Development
NOTION_API_KEY=[DEV_NOTION_KEY]
NOTION_DATABASE_ID=[DEV_DATABASE_ID]

# Staging
NOTION_API_KEY=[STAGING_NOTION_KEY]
NOTION_DATABASE_ID=[STAGING_DATABASE_ID]

# Production
NOTION_API_KEY=[PROD_NOTION_KEY]
NOTION_DATABASE_ID=[PROD_DATABASE_ID]
```

#### Email Service (Example: SendGrid)

```bash
# Development
SENDGRID_API_KEY=[DEV_KEY]
FROM_EMAIL=dev@yourproject.com

# Staging
SENDGRID_API_KEY=[STAGING_KEY]
FROM_EMAIL=staging@yourproject.com

# Production
SENDGRID_API_KEY=[PROD_KEY]
FROM_EMAIL=noreply@yourproject.com
```

#### File Storage (Example: S3/Supabase Storage)

```bash
# Development
STORAGE_BUCKET=dev-uploads
STORAGE_URL=https://[DEV_PROJECT].supabase.co/storage/v1

# Staging
STORAGE_BUCKET=staging-uploads
STORAGE_URL=https://[STAGING_PROJECT].supabase.co/storage/v1

# Production
STORAGE_BUCKET=prod-uploads
STORAGE_URL=https://[PROD_PROJECT].supabase.co/storage/v1
```

---

## Environment Variables Management

### File Structure

```
project/
├── .env.dev                  # Development config
├── .env.staging              # Staging config
├── .env.prod                 # Production config (NEVER commit)
├── .env.example              # Template (safe to commit)
└── .gitignore                # Includes .env.*
```

### .gitignore Configuration

```bash
# Environment files
.env
.env.*
.env.local
.env.development.local
.env.test.local
.env.production.local

# Except example
!.env.example
```

### Loading Environment Variables

#### Backend (Python/FastAPI)

```python
# config.py
import os
from dotenv import load_dotenv

# Load environment-specific .env file
env = os.getenv("ENV", "dev")
load_dotenv(f".env.{env}")

DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
```

#### Frontend (React/React Native)

```javascript
// config.js
const env = process.env.REACT_APP_ENV || 'dev';

const config = {
  dev: {
    apiUrl: process.env.REACT_APP_DEV_API_URL,
    supabaseUrl: process.env.REACT_APP_DEV_SUPABASE_URL,
  },
  staging: {
    apiUrl: process.env.REACT_APP_STAGING_API_URL,
    supabaseUrl: process.env.REACT_APP_STAGING_SUPABASE_URL,
  },
  prod: {
    apiUrl: process.env.REACT_APP_PROD_API_URL,
    supabaseUrl: process.env.REACT_APP_PROD_SUPABASE_URL,
  },
};

export default config[env];
```

---

## Deployment Strategy

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml (example)

on:
  push:
    branches:
      - develop    # Triggers dev deployment
      - staging    # Triggers staging deployment
  pull_request:
    branches:
      - main       # Requires approval before prod deployment

jobs:
  deploy-dev:
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Development
        run: ./scripts/deploy.sh dev
        env:
          DATABASE_URL: ${{ secrets.DEV_DATABASE_URL }}

  deploy-staging:
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Staging
        run: ./scripts/deploy.sh staging
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

  deploy-prod:
    if: github.event.pull_request.merged == true && github.base_ref == 'main'
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Production
        run: ./scripts/deploy.sh prod
        env:
          DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
```

### Deployment Triggers

| Event | Branch | Environment | Approval | Automatic |
|-------|--------|-------------|----------|-----------|
| Push to `develop` | develop | Development | No | Yes |
| PR merged to `staging` | staging | Staging | No | Yes |
| PR merged to `main` | main | Production | Yes | After approval |

---

## Database Migrations

### Migration Strategy

**Development:**
```bash
# Create and test migrations freely
supabase migration new add_user_avatar
# OR
alembic revision --autogenerate -m "add user avatar"

# Apply immediately
supabase db push
# OR
alembic upgrade head
```

**Staging:**
```bash
# Test migrations from develop
git checkout staging
git merge develop

# Apply migrations
supabase db push
# OR
alembic upgrade head

# Verify data integrity
npm run test:integration
```

**Production:**
```bash
# Apply migrations with backup
pg_dump [prod_db] > backup_$(date +%Y%m%d).sql

# Apply migration
supabase db push
# OR
alembic upgrade head

# Verify
npm run test:smoke
```

### Migration Checklist

Before applying migrations to production:
- [ ] Tested in development
- [ ] Tested in staging with production-like data
- [ ] Backup created
- [ ] Rollback plan ready
- [ ] All tests pass
- [ ] Team notified
- [ ] Maintenance window scheduled (if needed)

---

## Testing Requirements per Environment

### Development

**Required:**
- ✅ Unit tests pass
- ✅ No linting errors

**Optional:**
- Integration tests
- End-to-end tests

### Staging

**Required:**
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ Critical E2E tests pass
- ✅ No security vulnerabilities (high/critical)
- ✅ Performance benchmarks met

**Optional:**
- Manual QA testing
- User acceptance testing (UAT)

### Production

**Required:**
- ✅ All staging tests passed
- ✅ Security scan passed (zero high/critical vulnerabilities)
- ✅ Performance tests passed
- ✅ Load testing completed
- ✅ Smoke tests passed post-deployment

---

## Monitoring & Logging

### Development

**Logging:**
- Console logging (verbose)
- Local log files
- No external logging service required

**Monitoring:**
- Local development tools
- Browser DevTools
- Database GUI (Supabase Studio, pgAdmin)

### Staging

**Logging:**
- Structured logging (JSON)
- Log aggregation (e.g., Logtail, CloudWatch)
- Retention: 7 days

**Monitoring:**
- Application Performance Monitoring (APM)
- Error tracking (e.g., Sentry)
- Uptime monitoring

### Production

**Logging:**
- Structured logging (JSON)
- Log aggregation with search/alerts
- Retention: 30 days (or per compliance requirements)

**Monitoring:**
- APM with detailed metrics
- Error tracking with alerting
- Uptime monitoring with SMS/email alerts
- Performance monitoring
- Database monitoring
- Cost monitoring

**Alerting:**
- Critical errors → Immediate SMS/Slack
- High CPU/Memory → Email
- Downtime → SMS + Slack + Email

---

## Environment-Specific Agent Behavior

### Agents in Development

**Allowed:**
- ✅ Direct pushes to `develop` (with caution)
- ✅ Experimental features
- ✅ Database resets
- ✅ Verbose logging

**Not Allowed:**
- ❌ Pushing to `staging` or `main`

### Agents in Staging

**Allowed:**
- ✅ Read database data (for verification)
- ✅ Run tests
- ✅ Create verification reports

**Not Allowed:**
- ❌ Modifying data directly
- ❌ Deploying without PR
- ❌ Skipping tests

### Agents in Production

**Allowed:**
- ✅ Read-only access (for debugging)
- ✅ Creating PRs for hotfixes

**Not Allowed:**
- ❌ Direct database access
- ❌ Direct deployments
- ❌ Skipping any checks
- ❌ Force pushes

---

## Cost Estimation

### Supabase Costs (Example)

| Environment | Plan | Database | Storage | Cost/Month |
|-------------|------|----------|---------|------------|
| Development | Free | 500MB | 1GB | $0 |
| Staging | Free/Pro | 8GB | 100GB | $0-25 |
| Production | Pro | 8GB+ | 100GB+ | $25+ |

**Total during development:** ~$0/month
**Total with staging:** ~$0-25/month
**Total in production:** ~$25-100/month (scales with usage)

---

## Quick Reference

### Environment Selection

```bash
# Set environment for current session
export ENV=dev       # Development
export ENV=staging   # Staging
export ENV=prod      # Production

# Run with specific environment
ENV=dev npm start
ENV=staging npm test
ENV=prod npm run build
```

### Environment Verification

```bash
# Check which environment you're in
echo $ENV

# Verify database connection
psql $DATABASE_URL -c "SELECT current_database();"

# Verify API connectivity
curl $API_URL/health
```

---

## Related Documentation

- Git Workflow: `@agent-os/standards/global/git-workflow.md`
- CI/CD Pipeline: `@agent-os/standards/global/ci-cd-devops.md`
- Security Standards: `@agent-os/standards/global/security.md`
- Database Standards: `@agent-os/standards/backend/DATABASE-SUPABASE.md`
