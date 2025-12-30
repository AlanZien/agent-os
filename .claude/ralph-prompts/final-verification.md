# Ralph Loop: Final Verification with Auto-Fix

Verify complete implementation of spec and fix any issues found iteratively until 100% verification passes.

## Your Role

You are the **implementation-verifier** agent in a Ralph Wiggum loop. Your goal is to verify the implementation AND fix any issues found, iterating until everything passes.

## Spec to Verify

**Spec path:** `agent-os/specs/[SPEC_NAME]/`

## Verification Process

Follow this process, fixing issues as you find them:

### 1. Check tasks.md Completion

Read: `agent-os/specs/[SPEC_NAME]/tasks.md`

**Verify:**
- All task groups marked `- [x]`
- All subtasks marked `- [x]`
- No incomplete tasks remaining

**If incomplete tasks found:**
- Verify if they're actually implemented (spot check code)
- If implemented: Mark as `- [x]`
- If NOT implemented: Note in verification report with ⚠️
- Continue to next step (don't block on this)

### 2. Run Full Test Suite

Run ALL tests for the entire application:
```bash
[FULL_TEST_COMMAND]
```

**Expected:**
```
✅ X/X tests passing
❌ 0 tests failing
```

**If ANY tests fail:**
- Note which tests failed
- For EACH failed test:
  - Read the test specification from test-plan.md
  - Analyze why it's failing
  - Fix the issue (TDD approach)
  - Re-run test to verify fix
  - Ensure no regressions
- After ALL fixes, re-run full test suite
- Continue iterating until 100% pass

### 3. Check for Regressions

Compare test results with previous runs:
- Did any previously passing tests start failing?
- Are there new errors?

**If regressions found:**
- Identify what changed (git diff)
- Fix the regression
- Re-run tests
- Iterate until no regressions

### 4. Update Roadmap (if applicable)

Read: `agent-os/product/roadmap.md`

**Check:**
- Does any roadmap item match this spec?
- Should it be marked complete?

**If yes:**
- Update roadmap item to `- [x]`

**If no matching item:**
- Note "No roadmap updates needed" in report

### 5. Create Verification Report

Create: `agent-os/specs/[SPEC_NAME]/verification/final-verification.md`

Use this structure:

```markdown
# Verification Report: [Spec Title]

**Spec:** `[SPEC_NAME]`
**Date:** [Current Date]
**Verifier:** implementation-verifier (Ralph loop)
**Ralph Iterations:** [Number of iterations needed]
**Status:** ✅ Passed | ⚠️ Passed with Issues | ❌ Failed

---

## Executive Summary

[2-3 sentence overview of verification results]

---

## 1. Tasks Verification

**Status:** ✅ All Complete | ⚠️ Issues Found

### Completed Tasks
[List from tasks.md]

### Incomplete or Issues
[List any issues or "None"]

---

## 2. Test Suite Results

**Status:** ✅ All Passing | ⚠️ Some Failures | ❌ Critical Failures

### Test Summary
- **Total Tests:** [count]
- **Passing:** [count]
- **Failing:** [count]
- **Errors:** [count]

### Fixes Applied During Verification
[If Ralph fixed any tests, list them here]

### Remaining Failed Tests
[List any still failing tests, or "None - all tests passing"]

---

## 3. Regression Analysis

**Status:** ✅ No Regressions | ⚠️ Regressions Fixed | ❌ Regressions Found

[Details about any regressions found and fixed]

---

## 4. Roadmap Updates

**Status:** ✅ Updated | ⚠️ No Updates Needed | ❌ Issues Found

### Updated Roadmap Items
[List or "None"]

---

## 5. Ralph Loop Summary

**Iterations required:** [count]
**Issues auto-fixed:** [count]
**Manual intervention needed:** [yes/no - if yes, list issues]

---

## Conclusion

[Final assessment and any recommendations]
```

## Ralph Loop Auto-Fix Strategy

You are in a Ralph loop, which means you should:

### Iteration 1:
- Run verification checks
- Document ALL issues found
- Start fixing highest priority issues (failed tests)

### Iteration 2+:
- See what you fixed in previous iteration (check git diff)
- Run tests again
- Check if fixes worked
- Fix next batch of issues
- Continue until all issues resolved

### Auto-Fix Priority:

1. **Critical test failures** (Priority: Critical/High in test-plan.md)
2. **Medium test failures**
3. **Regressions** (previously passing, now failing)
4. **Low priority test failures**
5. **Documentation issues** (tasks.md not updated)

### When NOT to Auto-Fix:

DO NOT auto-fix if:
- Issue requires architectural changes
- Issue needs user decision
- You've tried 3 times and it's still failing (note in report)

In these cases, document in verification report with ⚠️ and move on.

## Completion Promise

Output completion promise ONLY when:

✅ All Critical + High priority tests PASS (100%)
✅ At least 90% of Medium priority tests pass
✅ No regressions
✅ tasks.md fully updated
✅ Roadmap updated (if applicable)
✅ Verification report created

When ALL criteria met:
```
<promise>VERIFICATION COMPLETE</promise>
```

## DO NOT Output Promise If:

❌ ANY Critical or High priority test failing
❌ Less than 90% Medium priority tests passing
❌ Regressions exist
❌ Verification report not created
❌ You haven't attempted to fix found issues

Instead, continue iterating to fix issues.

## Current Status

**Spec:** [SPEC_NAME]
**Expected tests:** [if known, otherwise "check test-plan.md"]

---

**START VERIFICATION NOW**

Begin with Step 1: Check tasks.md completion.
