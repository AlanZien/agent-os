# Process for Orchestrating a Spec's Implementation

Orchestrate parallel implementation of task groups by dedicated subagents.

**Key Principles:**
- Smart defaults reduce user interactions
- Single confirmation round instead of multiple Q&A
- Subagents have explicit retry limits and fallback strategies
- Status tracking throughout execution

---

## Phase 1: Locate tasks.md

IF you already know which spec we're working on AND that spec folder has a `tasks.md` file:
- Use it and proceed to Phase 2

OTHERWISE, request from user:
```
Please provide the path to a spec's `tasks.md` for orchestration.

If you don't have one yet, run one of these first:
/shape-spec → /write-spec → /create-tasks
```

---

## Phase 2: Generate orchestration.yml with Smart Defaults

Create `agent-os/specs/[this-spec]/orchestration.yml` with intelligent defaults based on task group analysis.

### 2.1 Available Subagents

Reference these subagent types when assigning:

| Subagent | Best For |
|----------|----------|
| `backend-specialist` | API endpoints, database, migrations, server logic |
| `frontend-specialist` | UI components, styling, client-side logic |
| `fullstack-specialist` | Features spanning frontend and backend |
| `test-specialist` | Test suites, E2E tests, test infrastructure |
| `devops-specialist` | CI/CD, deployments, infrastructure |
| `general-purpose` | Mixed or unclear scope |

### 2.2 Smart Default Assignment Rules

Analyze each task group name and description to assign defaults:

| Task Group Contains | Default Subagent | Default Standards |
|---------------------|------------------|-------------------|
| `database`, `migration`, `schema`, `DB` | `backend-specialist` | `backend/*`, `global/*` |
| `API`, `endpoint`, `route`, `middleware` | `backend-specialist` | `backend/*`, `global/*` |
| `UI`, `component`, `page`, `view`, `frontend` | `frontend-specialist` | `frontend/*`, `global/*` |
| `test`, `E2E`, `unit`, `integration` | `test-specialist` | `global/*` |
| `auth`, `security`, `middleware` | `backend-specialist` | `backend/*`, `global/*` |
| Mixed or unclear | `general-purpose` | `all` |

### 2.3 Generate orchestration.yml

Create the file with this structure:

```yaml
spec_path: agent-os/specs/[this-spec]
generated_at: [ISO timestamp]
total_task_groups: [count]

task_groups:
  - name: [task-group-name]
    claude_code_subagent: [auto-assigned based on rules]
    standards:
      - [auto-assigned based on rules]
    status: pending

  - name: [task-group-name]
    claude_code_subagent: [auto-assigned based on rules]
    standards:
      - [auto-assigned based on rules]
    status: pending

  # Repeat for each task group in tasks.md
```

---

## Phase 3: Single Confirmation Round

Present the complete orchestration plan to user for ONE confirmation:

```
## Orchestration Plan for [spec-name]

| # | Task Group | Subagent | Standards |
|---|------------|----------|-----------|
| 1 | [name] | [subagent] | [standards] |
| 2 | [name] | [subagent] | [standards] |
| 3 | [name] | [subagent] | [standards] |

### Available Standards
- `all` - Include all standards
- `global/*` - Global coding standards
- `frontend/*` - Frontend standards
- `backend/*` - Backend standards
- `[folder]/[file].md` - Specific file

### Confirm or Modify

Type `ok` to proceed with these defaults, or specify changes:
- Example: "1: fullstack-specialist, frontend/*"
- Example: "2: standards=backend/api.md, global/*"
```

**WAIT for user response.**

If user responds with `ok`, `yes`, or empty: proceed to Phase 4.

If user specifies changes: update `orchestration.yml` accordingly, then proceed.

---

## Phase 4: Execute Parallel Delegation

### 4.1 Subagent Instructions Template

For EACH task group, delegate using the Task tool with this prompt structure:

```
## Task Group: [task-group-name]

You are implementing task group "[task-group-name]" from the spec.

### Files to Read First
- Spec: `agent-os/specs/[this-spec]/spec.md`
- Tasks: `agent-os/specs/[this-spec]/tasks.md` (find your task group section)
- Test Plan: `agent-os/specs/[this-spec]/test-plan.md` (if exists)

### Standards to Follow
[Compiled list of standards files - see section 4.2]

### Implementation Rules

1. **TDD Approach**: Write tests first, then implement
2. **Checkbox Updates**: Mark tasks complete in tasks.md as you finish them
3. **One Task at a Time**: Complete each sub-task before moving to next

### CRITICAL: Retry and Fallback Strategy

**If Bash commands are blocked or fail:**
- Maximum 2 retry attempts per command
- After 2 failures, use this fallback:
  1. Document the blocker in your response
  2. Continue with implementation WITHOUT test validation
  3. Mark task as "implemented-unverified" in tasks.md
  4. Report which tests need manual execution

**If permissions are refused:**
- Do NOT retry infinitely
- Switch to write-only mode (create files without running tests)
- Document what commands need to be run manually

### Deliverables
- [ ] All sub-tasks implemented
- [ ] Tests written (even if not runnable)
- [ ] Checkboxes marked in tasks.md
- [ ] Blockers documented (if any)
```

### 4.2 Compile Standards List

For each task group, build the standards file list:

1. Read `standards` array from `orchestration.yml` for this task group
2. Apply these rules:
   - `all` → Include every file in `agent-os/standards/`
   - `folder/*` → Include all files in `agent-os/standards/folder/`
   - `folder/file.md` → Include specific file
3. De-duplicate the list
4. Format as:
   ```
   @agent-os/standards/global/coding-style.md
   @agent-os/standards/backend/api.md
   [etc.]
   ```

### 4.3 Parallel Execution

Launch subagents in PARALLEL using multiple Task tool calls in a single message:

```
[Task tool call 1: TG1 delegation]
[Task tool call 2: TG2 delegation]
[Task tool call 3: TG3 delegation]
```

**Important**: Independent task groups should run simultaneously for efficiency.

---

## Phase 5: Monitor and Report

### 5.1 Update Status in orchestration.yml

As subagents complete, update their status:

```yaml
task_groups:
  - name: [task-group-name]
    status: completed  # or: in-progress, blocked, failed
    completed_at: [ISO timestamp]
    blockers: []  # or list of blockers encountered
```

### 5.2 Final Report

Once all subagents complete, present summary:

```
## Orchestration Complete

| Task Group | Status | Blockers |
|------------|--------|----------|
| [name] | [status] | [blockers or "none"] |

### Summary
- Completed: X/Y task groups
- Blocked: Z task groups (manual intervention needed)

### Manual Steps Required
[List any tests or commands that couldn't run due to permissions]

### Next Steps
- Run `/verify-implementation` to validate
- Or run blocked tests manually: `npm test -- [test-file]`
```

---

## Quick Reference

### Execution Flow
```
Phase 1: Locate tasks.md
    ↓
Phase 2: Generate orchestration.yml (auto-defaults)
    ↓
Phase 3: Single confirmation (user approves/modifies)
    ↓
Phase 4: Parallel subagent delegation
    ↓
Phase 5: Monitor, update status, report
```

### Key Improvements from v1
- Smart defaults reduce 3 Q&A rounds to 1 confirmation
- Explicit retry limits prevent infinite loops
- Fallback strategies keep progress when blocked
- Status tracking in orchestration.yml
- Parallel execution for independent task groups
