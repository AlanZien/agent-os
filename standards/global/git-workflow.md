# Git Workflow & Branching Strategy - AgentOS Tracker

**Version**: 2.0 | **Stack**: Next.js + Vercel | **Token-Optimized**

## Branch Strategy

### Main Branches

| Branch | Environment | Purpose | Protection Level |
|--------|-------------|---------|------------------|
| `main` | Production | Stable production code | 🔒 Protected - PR required, approvals required |
| `staging` | Staging | Pre-production testing | 🔒 Protected - PR required |
| `develop` | Development | Integration branch for features | ⚠️ Semi-protected - PR recommended |

### Supporting Branches

| Branch Pattern | Created From | Merged To | Purpose |
|----------------|--------------|-----------|---------|
| `feature/*` | `develop` | `develop` | New features |
| `bugfix/*` | `develop` | `develop` | Bug fixes |
| `hotfix/*` | `main` | `main` + `develop` | Critical production fixes |
| `release/*` | `develop` | `staging` → `main` | Release preparation |

## Workflow for Agents

### Standard Feature Development

```bash
# 1. Start from develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/spec-name

# 3. Implement feature
# ... work happens here ...

# 4. Commit changes
git add .
git commit -m "feat: implement [feature-name]

[Description of changes]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# 5. Push feature branch
git push origin feature/spec-name

# 6. Create Pull Request to develop
gh pr create --base develop --title "feat: [feature-name]" --body "..."
```

### Bug Fixes

```bash
# 1. Create bugfix branch from develop
git checkout develop
git pull origin develop
git checkout -b bugfix/issue-description

# 2. Fix bug, commit, push, PR
git commit -m "fix: resolve [bug-description]"
git push origin bugfix/issue-description
gh pr create --base develop
```

### Hotfixes (Critical Production Issues)

```bash
# 1. Create from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# 2. Fix, commit, PR to main
git commit -m "hotfix: fix critical [issue]"
git push origin hotfix/critical-issue
gh pr create --base main

# 3. Also merge back to develop
gh pr create --base develop
```

## Commit Message Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add password reset` |
| `fix` | Bug fix | `fix(api): handle null user error` |
| `docs` | Documentation | `docs(readme): update setup guide` |
| `style` | Code style (formatting) | `style: fix linting errors` |
| `refactor` | Code refactoring | `refactor(db): optimize query` |
| `test` | Add/update tests | `test(auth): add login tests` |
| `chore` | Maintenance | `chore(deps): update dependencies` |

### Examples

```bash
# Good commits
feat(auth): add email verification flow

- Add verification email template
- Create /verify-email page
- Add Supabase email confirmation

Closes #123

🤖 Generated with Claude Code
```

## Branch Protection Rules

### `main` Branch

**Required:**
- ✅ Pull request required
- ✅ At least 1 approval required
- ✅ All status checks must pass
- ✅ Linear history (squash or rebase)

**Prohibited:**
- ❌ Direct pushes
- ❌ Force pushes

### `staging` Branch

**Required:**
- ✅ Pull request required
- ✅ All status checks must pass

### `develop` Branch

**Recommended:**
- ⚠️ Pull request recommended
- ⚠️ Status checks should pass

**Allowed:**
- ✅ Direct pushes (for rapid development)

## Pre-Push Test Report

Before pushing commits, run all tests and display a structured report:

```
════════════════════════════════════════════════════════════════
📊 TEST REPORT BEFORE PUSH
════════════════════════════════════════════════════════════════

UNIT TESTS (Vitest):
  ✅ XX tests passed | ❌ X failed | ⚠️ X skipped

  By module:
    ├── lib/validations/    ✅ XX tests
    ├── lib/utils/          ✅ XX tests
    └── components/         ✅ XX tests

E2E TESTS (Playwright):
  ✅ XX tests passed | ❌ X failed

  By suite:
    ├── auth.spec.ts        ✅ XX tests
    └── dashboard.spec.ts   ✅ XX tests

════════════════════════════════════════════════════════════════
SUMMARY
════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────┐
│  TOTAL: XXX tests | ✅ XXX passed | ❌ X failed             │
│  Ready to push: ✅ YES / ❌ NO                               │
└─────────────────────────────────────────────────────────────┘
```

### Commands to Run

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# All tests with coverage
npm run test -- --coverage
```

## Agent-Specific Rules

### For implementer agent

1. ✅ ALWAYS work on feature branches
2. ✅ ALWAYS use conventional commit messages
3. ✅ ALWAYS include co-authorship footer
4. ✅ ALWAYS create PR when ready
5. ❌ NEVER force push to protected branches
6. ❌ NEVER commit directly to `main` or `staging`

### For implementation-verifier agent

1. ✅ Check that work is on correct branch
2. ✅ Verify all tests pass before PR
3. ✅ Ensure commit messages follow conventions

## Pull Request Template

```markdown
## Summary
[1-3 bullet points describing changes]

## Type of Change
- [ ] 🎉 New feature
- [ ] 🐛 Bug fix
- [ ] 📝 Documentation
- [ ] ♻️ Refactoring
- [ ] ✅ Tests

## Spec Reference
- Spec: `agent-os/specs/[spec-name]/`

## Testing
- [ ] All tests pass (`npm test`)
- [ ] E2E tests pass (`npm run test:e2e`)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project standards
- [ ] TypeScript types are correct
- [ ] No console.log statements
- [ ] Ready for review

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Quick Reference

```bash
# Start new feature
git checkout develop && git pull && git checkout -b feature/my-feature

# Commit with convention
git commit -m "feat(scope): description"

# Push and create PR
git push origin feature/my-feature
gh pr create --base develop

# Update feature branch with develop
git checkout feature/my-feature
git merge develop
```

## Related Documentation

- Environments: `@agent-os/standards/global/environments.md`
- CI/CD: `@agent-os/standards/global/ci-cd-devops.md`
- Security: `@agent-os/standards/global/security.md`

---

**Token Count**: ~600 tokens
