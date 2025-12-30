# Ralph Wiggum Prompts for agent-os

This directory contains Ralph Wiggum prompt templates for iterative TDD implementation in the agent-os workflow.

## What is Ralph Wiggum?

Ralph Wiggum is an iterative development technique where the same prompt is fed to Claude repeatedly. Claude sees its own previous work in files and git history, enabling self-correction until task completion.

**Key principle:** Deterministic iteration with clear completion criteria.

## Available Prompts

### 1. `tdd-task-group.md`
**Purpose:** Implement a complete task group using TRUE TDD workflow

**When to use:**
- Implementing a task group from tasks.md
- test-plan.md exists with test specifications
- Want automated RED-GREEN-REFACTOR cycles
- Want self-correction until all tests pass

**Completion promise:** `TASK GROUP COMPLETE`

**Used by:** `/ralph-implement` command

---

### 2. `bug-fix-iteration.md`
**Purpose:** Fix failing tests iteratively

**When to use:**
- One or more tests are failing
- Need iterative debugging approach
- Want automatic retry with different approaches
- Bug logged in Notion needs fixing

**Completion promise:** `BUG FIXED`

**Manual usage:**
```bash
# Edit bug-fix-iteration.md to replace placeholders:
# [SPEC_NAME], [TEST_NAMES], [TEST_FILES], etc.

/ralph-loop "$(cat .claude/ralph-prompts/bug-fix-iteration.md)" --completion-promise "BUG FIXED" --max-iterations 10
```

---

### 3. `final-verification.md`
**Purpose:** Verify implementation and auto-fix any issues found

**When to use:**
- All task groups supposedly complete
- Want comprehensive verification
- Want auto-fix of any failures found
- Ready for final sign-off

**Completion promise:** `VERIFICATION COMPLETE`

**Manual usage:**
```bash
# Edit final-verification.md to replace placeholders:
# [SPEC_NAME], [FULL_TEST_COMMAND], etc.

/ralph-loop "$(cat .claude/ralph-prompts/final-verification.md)" --completion-promise "VERIFICATION COMPLETE" --max-iterations 5
```

---

## How Prompts Work

### Template Structure

Each prompt contains **placeholders** that get replaced with actual values:

```markdown
Implement task group "[TASK_GROUP_NAME]" from agent-os/specs/[SPEC_NAME]/tasks.md

Standards to follow:
[STANDARDS_LIST]
```

### Placeholder Replacements

Common placeholders across prompts:

| Placeholder | Replaced With | Example |
|------------|---------------|---------|
| `[SPEC_NAME]` | Spec folder name | `user-auth` |
| `[TASK_GROUP_NAME]` | Task group from tasks.md | `Database Layer` |
| `[STANDARDS_LIST]` | List of standards to follow | `@agent-os/standards/backend/BACKEND-FASTAPI.md` |
| `[TEST_COMMAND]` | Command to run tests | `pytest backend/tests/` |
| `[TEST_NAMES]` | Names of specific tests | `test_user_creation_requires_email` |
| `[TEST_FILES]` | Paths to test files | `backend/tests/models/test_user.py` |

### Automatic Replacement

The `/ralph-implement` command handles replacements automatically.

For manual usage, use `sed`:

```bash
cat .claude/ralph-prompts/tdd-task-group.md | \
  sed 's/\[SPEC_NAME\]/user-auth/g' | \
  sed 's/\[TASK_GROUP_NAME\]/Database Layer/g' | \
  sed 's/\[TEST_COMMAND_FOR_TASK_GROUP\]/pytest backend\/tests\/models/g'
```

---

## Usage Patterns

### Pattern 1: Standard TDD Implementation (Recommended)

Use the command - it handles everything:

```bash
/ralph-implement
```

Interactive prompts will guide you through:
1. Select spec
2. Select task group
3. Choose standards
4. Configure iterations
5. Launch Ralph automatically

---

### Pattern 2: Manual Bug Fix

When a specific test is failing:

```bash
# 1. Edit bug-fix-iteration.md manually
# Replace [SPEC_NAME], [TEST_NAMES], [TEST_FILES]

# 2. Launch Ralph manually
/ralph-loop "$(cat .claude/ralph-prompts/bug-fix-iteration.md)" \
  --completion-promise "BUG FIXED" \
  --max-iterations 10
```

---

### Pattern 3: Final Verification with Auto-Fix

After all implementation complete:

```bash
# 1. Edit final-verification.md manually
# Replace [SPEC_NAME], [FULL_TEST_COMMAND]

# 2. Launch Ralph manually
/ralph-loop "$(cat .claude/ralph-prompts/final-verification.md)" \
  --completion-promise "VERIFICATION COMPLETE" \
  --max-iterations 5
```

---

## Customizing Prompts

### For Your Project

You can customize these templates for your specific needs:

**1. Change test commands:**
```markdown
# Instead of generic [TEST_COMMAND]
pytest backend/tests/models/  # Specific to your structure
```

**2. Add project-specific instructions:**
```markdown
## Project-Specific Notes

- Always use Supabase client from `app/db.py`
- Follow naming convention: `test_<model>_<behavior>`
- Use factories from `tests/factories.py`
```

**3. Adjust completion criteria:**
```markdown
# Be more strict
✅ All tests PASS (including integration tests)
✅ Code coverage > 90%
✅ No linting errors

# Or more lenient
✅ All Critical tests PASS
✅ 80% of High priority tests PASS
```

### Creating New Prompts

To create a new Ralph prompt for a specific use case:

```markdown
# my-custom-prompt.md

# Ralph Loop: [Your Use Case]

[Your specific instructions...]

## Completion Promise

Output ONLY when:
✅ [Criteria 1]
✅ [Criteria 2]

When met:
<promise>MY CUSTOM COMPLETE</promise>
```

Then use:
```bash
/ralph-loop "$(cat .claude/ralph-prompts/my-custom-prompt.md)" \
  --completion-promise "MY CUSTOM COMPLETE" \
  --max-iterations 10
```

---

## Best Practices

### ✅ DO:

- **Use clear completion promises** - Ralph needs to know when to stop
- **Specify test commands explicitly** - Don't rely on auto-detection
- **Include relevant standards** - Guide Ralph's implementation
- **Set reasonable max iterations** - 15-20 for complex tasks, 5-10 for simple
- **Test prompts on small task groups first** - Validate before large tasks

### ❌ DON'T:

- **Use vague success criteria** - "Make it better" won't work
- **Mix planning and execution** - Ralph executes, doesn't plan
- **Set too few iterations** - Give Ralph room to iterate
- **Skip test-plan.md** - TDD needs test specifications
- **Use for exploratory work** - Ralph needs clear goals

---

## Iteration Limits Guide

Choose max iterations based on task complexity:

| Task Type | Max Iterations | Reasoning |
|-----------|----------------|-----------|
| Small bug fix (1-2 tests) | 5-10 | Usually fixable quickly |
| Medium task group (3-8 tests) | 15-20 | Multiple RED-GREEN cycles |
| Large task group (9+ tests) | 20-30 | Many tests to implement |
| Final verification | 5-10 | Should mostly pass already |
| Complex refactoring | 10-15 | May need several attempts |

If Ralph reaches max iterations:
1. Check if task is too complex (break it down)
2. Check if prompt is clear enough
3. Check if test specifications are correct
4. Increase iterations and try again
5. Or switch to manual implementation

---

## Troubleshooting

### Ralph keeps hitting max iterations

**Possible causes:**
- Task too complex → Break into smaller task groups
- Test specifications unclear → Improve test-plan.md
- Missing standards → Add relevant standards
- Tests themselves are buggy → Fix test-plan.md specs

**Solutions:**
- Increase max iterations
- Simplify task group (fewer tests)
- Make test-plan.md specs more explicit (Given-When-Then)
- Verify tests manually first

### Ralph outputs promise but tests fail

**This shouldn't happen** - it's a bug in the prompt logic.

**Solutions:**
- Check prompt's completion criteria
- Make criteria MORE strict
- Add explicit test verification before promise
- Report issue (prompt needs fixing)

### Ralph modifies wrong files

**Possible causes:**
- Task description in tasks.md is vague
- Standards don't match task domain
- Prompt lacks file path guidance

**Solutions:**
- Make task description more specific in tasks.md
- Include only relevant standards
- Add file path hints to prompt

---

## Integration with agent-os Workflow

```
Standard agent-os workflow:

/shape-spec
    ↓
/write-spec
    ↓
/plan-tests  ← Creates test-plan.md (REQUIRED for Ralph)
    ↓
/create-tasks ← Creates tasks.md with task groups
    ↓
/ralph-implement  ← Ralph uses prompts from this directory
    ↓
[Ralph iterates using tdd-task-group.md]
    ↓
✅ Task group complete
```

---

## Examples

### Example 1: Implementing user authentication

```bash
# After /plan-tests and /create-tasks

/ralph-implement

> Spec: user-auth
> Task Group: Database Layer
> Standards: All
> Max iterations: 15
> Test command: pytest backend/tests/models

# Ralph uses tdd-task-group.md template
# Implements 8 tests from test-plan.md
# Iterates until all pass
# Outputs: <promise>TASK GROUP COMPLETE</promise>
```

### Example 2: Fixing a failing test

```bash
# Test test_password_validation is failing

# Manually edit bug-fix-iteration.md:
# [TEST_NAMES] → test_password_validation
# [TEST_FILES] → backend/tests/models/test_user.py
# [SPEC_NAME] → user-auth

/ralph-loop "$(cat .claude/ralph-prompts/bug-fix-iteration.md)" \
  --completion-promise "BUG FIXED" \
  --max-iterations 10
```

### Example 3: Final verification

```bash
# All tasks supposedly done, run verification

# Edit final-verification.md:
# [SPEC_NAME] → user-auth
# [FULL_TEST_COMMAND] → pytest

/ralph-loop "$(cat .claude/ralph-prompts/final-verification.md)" \
  --completion-promise "VERIFICATION COMPLETE" \
  --max-iterations 5

# Ralph verifies, fixes any issues, creates report
```

---

## Quick Reference

| Command | Prompt Used | When to Use |
|---------|-------------|-------------|
| `/ralph-implement` | `tdd-task-group.md` | Implement task group with TDD |
| Manual bug fix | `bug-fix-iteration.md` | Fix specific failing tests |
| Final verification | `final-verification.md` | Verify + auto-fix at end |

---

## Next Steps

1. **Try /ralph-implement** - Use the command for your first Ralph implementation
2. **Review generated code** - See how Ralph implements TDD cycles
3. **Adjust prompts** - Customize templates for your project
4. **Create custom prompts** - For specific recurring tasks
5. **Share learnings** - Document what works for your team

---

For more about Ralph Wiggum technique:
- Original article: https://ghuntley.com/ralph/
- Help command: `/ralph-wiggum:help`
