# Git Workflow & Branching Strategy

This document defines the Git workflow and branching strategy for this project. All agents and developers must follow these conventions.

## Branch Strategy

### Main Branches

| Branch | Environment | Purpose | Protection Level |
|--------|-------------|---------|------------------|
| `main` | Production | Stable production code | 🔒 Protected - PR required, approvals required |
| `staging` | Testing/Staging | Pre-production testing | 🔒 Protected - PR required |
| `develop` | Development | Integration branch for features | ⚠️ Semi-protected - PR recommended |

### Supporting Branches

| Branch Pattern | Created From | Merged To | Purpose | Lifetime |
|----------------|--------------|-----------|---------|----------|
| `feature/*` | `develop` | `develop` | New features | Temporary |
| `bugfix/*` | `develop` | `develop` | Bug fixes | Temporary |
| `hotfix/*` | `main` | `main` + `develop` | Critical production fixes | Temporary |
| `release/*` | `develop` | `staging` → `main` | Release preparation | Temporary |

---

## Workflow for Agents

### Standard Feature Development

Agents implementing new features should follow this workflow:

```bash
# 1. Start from develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/spec-name

# 3. Implement feature (using /implement-tasks or /ralph-implement)
# ... work happens here ...

# 4. Commit changes
git add .
git commit -m "feat: implement [feature-name]

[Description of changes]

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

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

# 2. Fix bug
# ... fix happens here ...

# 3. Commit
git commit -m "fix: resolve [bug-description]"

# 4. Push and PR
git push origin bugfix/issue-description
gh pr create --base develop
```

### Hotfixes (Critical Production Issues)

```bash
# 1. Create from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# 2. Fix issue
# ... urgent fix ...

# 3. Commit
git commit -m "hotfix: fix critical [issue]"

# 4. PR to main
git push origin hotfix/critical-issue
gh pr create --base main

# 5. Also merge back to develop
gh pr create --base develop
```

---

## Environment Deployment Flow

```
feature/spec-name
    │
    ├──> PR ──> develop ──> Auto-deploy to DEV environment
    │
    └──> (after testing in dev)
         │
         ├──> PR ──> staging ──> Auto-deploy to STAGING environment
         │
         └──> (after QA approval)
              │
              └──> PR ──> main ──> Manual deploy to PRODUCTION
```

---

## Branch Protection Rules

### `main` Branch

**Required:**
- ✅ Pull request required
- ✅ At least 1 approval required
- ✅ All status checks must pass
- ✅ Conversation resolution required
- ✅ Linear history (squash or rebase)

**Prohibited:**
- ❌ Direct pushes
- ❌ Force pushes
- ❌ Branch deletion

### `staging` Branch

**Required:**
- ✅ Pull request required
- ✅ All status checks must pass

**Allowed:**
- ⚠️ Administrators can bypass

### `develop` Branch

**Recommended:**
- ⚠️ Pull request recommended (but not required)
- ⚠️ Status checks should pass

**Allowed:**
- ✅ Direct pushes (for rapid development)
- ⚠️ Force pushes (with caution)

---

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
| `style` | Code style (formatting) | `style(components): fix linting errors` |
| `refactor` | Code refactoring | `refactor(db): optimize query performance` |
| `test` | Add/update tests | `test(auth): add login tests` |
| `chore` | Maintenance | `chore(deps): update dependencies` |
| `perf` | Performance improvement | `perf(api): cache user queries` |
| `ci` | CI/CD changes | `ci(github): add deployment workflow` |

### Examples

**Good commits:**
```bash
feat(user-profile): add avatar upload functionality

- Add S3 storage integration
- Create upload endpoint
- Update user model with avatar_url

Closes #123

🤖 Generated with Claude Code
```

**Bad commits:**
```bash
# Too vague
git commit -m "updates"

# No type
git commit -m "add feature"

# No description
git commit -m "fix"
```

---

## Agent-Specific Rules

### For implementer agent

When implementing features:
1. ✅ ALWAYS work on feature branches (never directly on `develop`, `staging`, or `main`)
2. ✅ ALWAYS use conventional commit messages
3. ✅ ALWAYS include co-authorship footer for Claude Code
4. ✅ ALWAYS create PR when ready (use `gh pr create`)
5. ❌ NEVER force push to protected branches
6. ❌ NEVER commit directly to `main` or `staging`

### For implementation-verifier agent

When verifying implementations:
1. ✅ Check that work is on correct branch (feature/*)
2. ✅ Verify all tests pass before PR
3. ✅ Ensure commit messages follow conventions
4. ⚠️ Can suggest improvements before PR creation

### For ralph-wiggum loops

Ralph iterations should:
1. ✅ Work on the current feature branch
2. ✅ Make incremental commits during iterations
3. ✅ Squash commits before final PR (optional)
4. ✅ Include iteration summary in PR description

---

## Pull Request Template

When creating PRs, use this template:

```markdown
## Description
[Brief description of changes]

## Type of Change
- [ ] 🎉 New feature (feat)
- [ ] 🐛 Bug fix (fix)
- [ ] 📝 Documentation (docs)
- [ ] ♻️ Refactoring (refactor)
- [ ] ✅ Tests (test)

## Spec Reference
- Spec: `agent-os/specs/[spec-name]/`
- Tasks: Link to tasks.md section

## Testing
- [ ] All tests pass (`npm test` / `pytest`)
- [ ] Manual testing completed
- [ ] No regressions found

## Checklist
- [ ] Code follows project standards
- [ ] Commit messages follow conventions
- [ ] Documentation updated (if needed)
- [ ] Tests added/updated (if needed)
- [ ] Ready for review

## Screenshots (if applicable)
[Add screenshots for UI changes]

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Release Process

### Creating a Release

```bash
# 1. Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# 2. Update version numbers, changelog
# ... version bump ...

# 3. Commit
git commit -m "chore(release): prepare v1.2.0"

# 4. PR to staging for final testing
git push origin release/v1.2.0
gh pr create --base staging --title "Release v1.2.0"

# 5. After staging approval, PR to main
gh pr create --base main --title "Release v1.2.0"

# 6. Tag the release
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# 7. Merge release branch back to develop
git checkout develop
git merge release/v1.2.0
git push origin develop

# 8. Delete release branch
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

---

## Git Hooks Integration

This project may use Git hooks for automation. Agents should respect these hooks:

### Pre-commit Hook
- Runs linting
- Runs formatting
- Runs quick tests
- **Do not skip** with `--no-verify` unless explicitly instructed

### Pre-push Hook
- Runs full test suite
- Checks branch name format
- **Can be skipped** for WIP pushes with `--no-verify`

### Commit-msg Hook
- Validates commit message format
- Ensures conventional commits
- **Do not skip**

---

## Troubleshooting

### Agent tried to push to protected branch

**Error:**
```
remote: error: GH006: Protected branch update failed
```

**Solution:**
Agent should:
1. Create feature branch instead
2. Push to feature branch
3. Create PR to target branch

### Commit message rejected

**Error:**
```
commit-msg hook: Invalid commit message format
```

**Solution:**
Use conventional commit format:
```bash
git commit --amend -m "feat(scope): proper message"
```

### Merge conflicts

If agent encounters merge conflicts:
1. **Do not resolve automatically** - ask user
2. Provide conflict details
3. Suggest resolution strategy
4. Let user decide

---

## Best Practices Summary

### ✅ DO:
- Work on feature branches
- Use conventional commits
- Create PRs for all merges to protected branches
- Keep commits atomic and meaningful
- Write descriptive PR descriptions
- Reference issues/specs in commits
- Tag releases properly

### ❌ DON'T:
- Push directly to `main` or `staging`
- Use force push on shared branches
- Skip Git hooks without reason
- Write vague commit messages
- Merge without PR review (on protected branches)
- Leave unfinished features on `develop`
- Commit secrets or credentials

---

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
# OR
git rebase develop

# Squash commits before merging
git rebase -i develop
```

---

## Related Documentation

- Environments: `@agent-os/standards/global/environments.md`
- CI/CD: `@agent-os/standards/global/ci-cd-devops.md`
- Security: `@agent-os/standards/global/security.md`
