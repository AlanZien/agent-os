# Ralph Wiggum Implementation for agent-os

Use Ralph Wiggum iterative loops to implement a task group with automatic TDD self-correction until all tests pass.

## What is This Command?

This command launches a Ralph loop that:
1. Reads your task group and test specifications
2. Implements tests in TDD style (RED → GREEN → REFACTOR)
3. Self-corrects based on test failures
4. Iterates until ALL tests pass
5. Updates tasks.md and syncs to Notion

Perfect for well-defined task groups with clear test specifications.

## Usage

```
/ralph-implement
```

The command will guide you through the setup interactively.

---

## Process

### STEP 1: Locate Spec and Task Group

**First, ask user:**

```
Which spec are you working on?

Available specs in agent-os/specs/:
[List all spec folders found]

Enter spec name:
```

**Then, read tasks.md:**

Read: `agent-os/specs/[user-provided-spec]/tasks.md`

**Then, ask user:**

```
Which task group should Ralph implement?

Available task groups in tasks.md:
1. [Task Group 1 Name]
2. [Task Group 2 Name]
3. [Task Group 3 Name]

Enter task group number or name:
```

---

### STEP 2: Verify Prerequisites

Before launching Ralph, verify:

**Check 1: test-plan.md exists**
```bash
ls agent-os/specs/[spec-name]/test-plan.md
```

If NOT exists:
```
⚠️ Warning: test-plan.md not found for this spec.

Ralph works best with TDD workflow which requires test-plan.md.

Options:
1. Run /plan-tests first to create test-plan.md (Recommended)
2. Continue anyway (Ralph will implement without test guidance - not recommended)

Choose option:
```

**Check 2: Task group has tests in test-plan.md**

If test-plan.md exists:
- Read test-plan.md
- Find tests associated with this task group
- Count them

If NO tests found:
```
⚠️ Warning: No tests found in test-plan.md for task group "[task-group-name]".

Ralph needs tests to iterate on. Without tests, Ralph cannot verify success.

Options:
1. Add tests to test-plan.md for this task group first (Recommended)
2. Use /implement-tasks instead (standard implementation without Ralph)

Choose option:
```

**Check 3: Standards available**

Check if standards exist in `agent-os/standards/`

---

### STEP 3: Load All Standards

**Standards are automatically included for all implementations** (same as implementer agent):

```
# Product-Level References
@agent-os/product/design-system.md

# Feature-Level Test Specifications
@agent-os/specs/[spec-name]/test-plan.md

# Quick Reference & Bootstrap
@agent-os/standards/QUICK-REFERENCE.md
@agent-os/standards/PROJECT-BOOTSTRAP.md

# Core Standards
@agent-os/standards/backend/BACKEND-FASTAPI.md
@agent-os/standards/backend/DATABASE-SUPABASE.md
@agent-os/standards/backend/backend-patterns.md
@agent-os/standards/frontend/MOBILE-REACT-NATIVE.md
@agent-os/standards/frontend/frontend-patterns.md
@agent-os/standards/global-standards.md

# Security, DevOps & Testing
@agent-os/standards/global/security.md
@agent-os/standards/global/ci-cd-devops.md
@agent-os/standards/testing/test-writing.md
```

**Note:** All standards are included to ensure comprehensive coverage, especially critical patterns like core service abstractions (cache, logging, monitoring, payment).

---

### STEP 4: Configure Ralph Loop

**Ask user:**

```
Ralph loop configuration:

1. Max iterations: [default: 15]
   (How many times Ralph should iterate before stopping)

2. Test command: [default: auto-detect from project]
   (Command to run tests, e.g., pytest, npm test)

Press Enter to use defaults, or specify custom values:
```

**Auto-detect test command** if not provided:
- Check for `pytest.ini`, `pyproject.toml` → `pytest`
- Check for `package.json` with test script → `npm test`
- Check for `go.mod` → `go test ./...`
- Otherwise, ask user to specify

---

### STEP 5: Prepare Ralph Prompt

Load the template from `.claude/ralph-prompts/tdd-task-group.md`

**Replace these placeholders:**
- `[TASK_GROUP_NAME]` → actual task group name from tasks.md
- `[SPEC_NAME]` → spec folder name
- `[STANDARDS_LIST]` → complete standards list from Step 3 (all standards)
- `[TEST_COMMAND_FOR_TASK_GROUP]` → test command from Step 4

**Resulting prompt structure:**
```markdown
# Ralph Loop: TDD Task Group Implementation

Implement task group "Database Layer" from agent-os/specs/user-auth/tasks.md...

## Required Documentation
- agent-os/specs/user-auth/spec.md
- agent-os/specs/user-auth/test-plan.md
...

## Standards to follow:
# Product-Level References
@agent-os/product/design-system.md

# Core Standards
@agent-os/standards/backend/BACKEND-FASTAPI.md
@agent-os/standards/backend/DATABASE-SUPABASE.md
@agent-os/standards/backend/backend-patterns.md
@agent-os/standards/frontend/MOBILE-REACT-NATIVE.md
@agent-os/standards/frontend/frontend-patterns.md
@agent-os/standards/global-standards.md

# Security, DevOps & Testing
@agent-os/standards/global/security.md
@agent-os/standards/global/ci-cd-devops.md
@agent-os/standards/testing/test-writing.md

[Rest of template...]
```

---

### STEP 6: Show Summary and Confirm

**Display summary:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ralph Wiggum Implementation - Ready to Launch
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Spec: user-auth
Task Group: Database Layer
Tests: 8 tests from test-plan.md
Max Iterations: 15
Test Command: pytest backend/tests/

Standards included: ALL (comprehensive coverage)
✓ Backend patterns (FastAPI, Supabase, core abstractions)
✓ Frontend patterns (React Native)
✓ Global standards (security, testing, ci-cd)
✓ Product design system

Ralph will:
1. Read test specifications from test-plan.md
2. Implement each test using TDD (RED-GREEN-REFACTOR)
3. Self-correct based on test failures
4. Iterate until all 8 tests pass
5. Update tasks.md and sync to Notion
6. Output <promise>TASK GROUP COMPLETE</promise>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to launch Ralph loop?
Type 'yes' to continue, or 'no' to cancel:
```

---

### STEP 7: Launch Ralph Loop

**If user confirms, launch:**

Use the Skill tool to launch Ralph:

```
/ralph-loop "<prepared-prompt-from-step-5>" --completion-promise "TASK GROUP COMPLETE" --max-iterations <from-step-4>
```

**Monitor Ralph's progress:**

Ralph will iterate, and you'll see each iteration's output. Wait for:
- Ralph to complete (outputs promise)
- OR max iterations reached
- OR user cancels with /cancel-ralph

---

### STEP 8: Post-Ralph Summary

**After Ralph finishes (success or max iterations), display:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ralph Loop Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iterations used: X / <max-iterations>
Status: [COMPLETE / MAX ITERATIONS REACHED / CANCELLED]

Final verification:
```

**Run verification:**
1. Check if tasks.md was updated
2. Run test command one final time
3. Display test results

```
Tasks updated: ✅ Yes / ❌ No
Notion synced: ✅ Yes / ❌ No

Test Results:
✅ 8/8 tests passing
❌ 0 tests failing

[If all tests pass:]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task group "Database Layer" successfully implemented!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If some tests fail:]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Ralph reached max iterations with some tests still failing.

Failed tests:
- test_password_validation
- test_email_uniqueness

Options:
1. Run Ralph again with more iterations: /ralph-implement
2. Fix manually and use standard implementation
3. Review and debug the failures

Choose option:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## When to Use This Command

**✅ Use /ralph-implement when:**
- Task group has clear test specifications in test-plan.md
- You want TDD implementation with self-correction
- Task is well-defined with binary success criteria (tests pass/fail)
- You want hands-off iterative development

**❌ Don't use /ralph-implement when:**
- No test-plan.md exists (run /plan-tests first)
- Task requires design decisions or user input
- Success criteria are subjective ("make it look nice")
- You prefer manual control over implementation

---

## Troubleshooting

**Problem: Ralph keeps failing same test**
- Check if test specification in test-plan.md is clear
- Verify test command is correct
- Increase max iterations
- Or switch to manual implementation

**Problem: Ralph outputs promise but tests still fail**
- This shouldn't happen (bug in Ralph logic)
- Manually verify tests: run test command
- If tests fail, don't trust the promise - investigate

**Problem: Ralph modifies wrong files**
- Review standards - they guide Ralph's implementation
- Check if task group description in tasks.md is clear
- Provide more specific requirements in spec.md

**Problem: Max iterations reached**
- Task might be too complex for single Ralph loop
- Break into smaller task groups
- Or increase max iterations and try again
- Or switch to manual implementation

---

## Examples

### Example 1: Simple backend task group
```
/ralph-implement

> Which spec? user-auth
> Which task group? Database Layer
> Standards? 1 (All standards)
> Max iterations? 15
> Test command? pytest backend/tests/

[Ralph runs and implements 8 tests successfully]
✅ Task group complete!
```

### Example 2: Frontend task group with custom standards
```
/ralph-implement

> Which spec? dashboard-ui
> Which task group? User Profile Component
> Standards? 4 (Custom)
> Specify: frontend/*, global/security.md
> Max iterations? 20
> Test command? npm test

[Ralph runs and implements tests]
✅ Task group complete!
```

---

## Related Commands

- `/plan-tests` - Create test-plan.md before using Ralph
- `/implement-tasks` - Standard implementation without Ralph
- `/cancel-ralph` - Cancel active Ralph loop
- `ralph-wiggum:help` - Learn more about Ralph technique
