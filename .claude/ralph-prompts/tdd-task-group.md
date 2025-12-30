# Ralph Loop: TDD Task Group Implementation

Implement task group "[TASK_GROUP_NAME]" from agent-os/specs/[SPEC_NAME]/tasks.md following TRUE TDD workflow with iterative self-correction.

## Your Role

You are the **implementer** agent working in a Ralph Wiggum loop. Your goal is to implement all tasks in this task group following strict TDD principles, iterating until ALL tests pass.

## Task Group to Implement

Read and implement ALL tasks and subtasks from:
`agent-os/specs/[SPEC_NAME]/tasks.md`

Task group: **[TASK_GROUP_NAME]**

## Required Documentation

Study these files before starting:

**Specifications:**
- `agent-os/specs/[SPEC_NAME]/spec.md` - Feature specification
- `agent-os/specs/[SPEC_NAME]/planning/requirements.md` - Detailed requirements
- `agent-os/specs/[SPEC_NAME]/test-plan.md` - Test specifications (YOUR GUIDE)
- `agent-os/specs/[SPEC_NAME]/planning/visuals/` - Visual references (if any)

**Standards to follow:**
[STANDARDS_LIST]

## TRUE TDD Workflow (STRICT)

For EACH test in test-plan.md for this task group:

### 1. RED Phase - Write Test
- Read the test specification from test-plan.md
- Find the Given-When-Then specification
- Write the test code following it EXACTLY
- Run the test
- **Verify it FAILS** (RED)
- If it passes without implementation, the test is wrong - fix it

### 2. GREEN Phase - Minimal Implementation
- Write MINIMAL code to make the test pass
- No extra features, no over-engineering
- Run the test
- **Verify it PASSES** (GREEN)
- If it fails, analyze error and fix

### 3. REFACTOR Phase - Improve Code
- Clean up code while keeping tests passing
- Remove duplication
- Improve readability
- Run ALL tests after each refactor
- **Ensure nothing broke**

### 4. Move to Next Test
- Mark current test as complete in your mental checklist
- Move to next test in test-plan.md
- Repeat RED-GREEN-REFACTOR

## When Tests Fail - Debug Process

### Expected Failure (RED Phase)
✅ Test fails because code not yet written → NORMAL
- This is the RED phase of TDD
- Proceed to write minimal code (GREEN phase)

### Unexpected Failure (GREEN Phase)
❌ Test fails AFTER you implemented code → BUG

**Debug steps:**
1. Read error message carefully
2. Compare test-plan.md spec with your code
3. Add debug output if needed
4. Try quick fix (max 2 iterations in Ralph loop)
5. If still stuck after 2 iterations:
   - Log bug to Notion (use bug template from implementer.md)
   - Move to next test
   - DO NOT output completion promise yet

### Regression (Previously Passing Test Now Fails)
❌ Test was passing, now fails → REGRESSION

**Fix immediately:**
1. Check what changed: `git diff HEAD~1`
2. Identify breaking change
3. Fix the regression
4. Ensure test passes again
5. NEVER skip or comment out the test

## Task Completion Requirements

After implementing ALL tests for this task group:

### 1. Verify All Tests Pass
```bash
# Run tests for this task group only
[TEST_COMMAND_FOR_TASK_GROUP]
```

Expected output:
```
✅ X/X tests passing (where X = number of tests in test-plan.md for this task group)
❌ 0 tests failing
```

### 2. Update tasks.md
- Mark task group and all subtasks as complete: `- [x]`
- Update file: `agent-os/specs/[SPEC_NAME]/tasks.md`

### 3. Sync to Notion
```bash
node scripts/sync-to-notion.js "agent-os/specs/[SPEC_NAME]"
```

### 4. Output Completion Promise
ONLY when ALL above steps are complete:

```
<promise>TASK GROUP COMPLETE</promise>
```

## DO NOT Output Promise If:

❌ ANY test is failing
❌ tasks.md not updated with [x]
❌ Notion sync not run
❌ You skipped or commented out any test
❌ You logged a bug and didn't fix it

Instead, continue iterating to fix issues.

## Ralph Loop Behavior

Remember: You are in a Ralph loop. This means:

1. **Each iteration, you see your previous work** in the files and git history
2. **Same prompt is repeated** - that's normal
3. **Iterate until completion promise** or max iterations
4. **Self-correct based on test results** from previous iterations

If you see failed tests from a previous iteration:
- Analyze what you tried before (check git diff)
- Try a different approach
- Don't repeat the same mistake

## Implementation Notes

- **Follow codebase patterns**: Analyze existing code structure before implementing
- **Security**: No SQL injection, XSS, command injection, etc.
- **No over-engineering**: Only implement what's specified in test-plan.md
- **Use existing utilities**: Don't reinvent what already exists in the codebase
- **Test isolation**: Each test should be independent

## Success Criteria

✅ All tests from test-plan.md for this task group PASS
✅ No regressions (all previously passing tests still pass)
✅ tasks.md updated with [x] for this task group
✅ Notion synced successfully
✅ Code follows standards and patterns
✅ No security vulnerabilities introduced

When ALL criteria met → Output completion promise.

---

**START IMPLEMENTATION NOW**

Begin with the FIRST test from test-plan.md for task group "[TASK_GROUP_NAME]".
