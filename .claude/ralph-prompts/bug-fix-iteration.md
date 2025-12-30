# Ralph Loop: Bug Fix Iteration

Fix failing test(s) iteratively until ALL tests pass.

## Your Role

You are in a Ralph Wiggum loop focused on fixing bugs. Your goal is to fix all failing tests by iterating until they pass, analyzing failures, and trying different approaches.

## Bug Context

**Spec:** `agent-os/specs/[SPEC_NAME]/`
**Failing test(s):** [TEST_NAMES]
**Test file(s):** [TEST_FILES]
**Bug ID (if logged in Notion):** [BUG_ID]

## Reference Documentation

**Test Specifications:**
- `agent-os/specs/[SPEC_NAME]/test-plan.md` - What the test SHOULD do

**Implementation:**
- `agent-os/specs/[SPEC_NAME]/spec.md` - Feature specification
- `agent-os/specs/[SPEC_NAME]/planning/requirements.md` - Requirements

**Standards:**
[STANDARDS_LIST]

## Bug Fix Workflow

### 1. Understand the Test
- Read the test file: [TEST_FILES]
- Read test-plan.md specification for this test
- Understand what behavior is expected
- Understand the Given-When-Then

### 2. Run the Test
```bash
[TEST_COMMAND]
```

Analyze the output:
- What assertion failed?
- What was expected vs actual?
- What line number?
- What's the error message?

### 3. Analyze Root Cause
- Where is the implementation code?
- What does the test expect?
- What is the code actually doing?
- Why is there a mismatch?

### 4. Form Hypothesis
Based on the error:
- "The test expects X but code does Y"
- "The validation is missing for Z"
- "The function signature is wrong"

### 5. Make Minimal Fix
- Fix ONLY what's needed to make this test pass
- Don't refactor other code
- Don't add extra features
- Keep it simple

### 6. Run Test Again
```bash
[TEST_COMMAND]
```

**If test PASSES:**
✅ Move to next failing test (if any)

**If test FAILS:**
❌ Analyze new error message
- Is it the same error or different?
- Did your fix help at all?
- Try different approach in next iteration

### 7. Verify No Regressions
After fixing each test, run ALL tests:
```bash
[FULL_TEST_COMMAND]
```

Ensure you didn't break previously passing tests.

## Ralph Loop Iteration Strategy

You are in a Ralph loop. Each iteration:

1. **Check what you tried before** (via git diff or file changes)
2. **Don't repeat failed approaches**
3. **Try different solution** if previous didn't work
4. **Learn from error messages** - they tell you what's wrong

### Iteration Examples:

**Iteration 1:**
- Try: Add email validation in User.__init__
- Run test: FAILS - "ValidationError not raised"
- Learn: Validation is there but not raising error

**Iteration 2:**
- Try: Actually raise ValidationError when email missing
- Run test: PASSES ✅
- Success!

### If Stuck After 3 Iterations:

If same test fails 3 times:
1. Re-read test-plan.md specification carefully
2. Check if test itself is correct
3. Look for similar working code in codebase
4. Check imports and dependencies

### If Stuck After 5 Iterations:

If still stuck after 5 iterations:
1. Consider if bug is more complex than expected
2. Check for architectural issues
3. May need to refactor implementation approach
4. Document what you've tried in code comments

## DO NOT:

❌ Skip or comment out the failing test
❌ Change the test to make it pass (unless test itself is wrong)
❌ Mark bug as fixed if test still fails
❌ Introduce new bugs while fixing this one
❌ Over-engineer the fix

## Completion Promise

Output completion promise ONLY when:

✅ ALL specified failing tests now PASS
✅ NO regressions (all other tests still pass)
✅ No new bugs introduced

When ALL criteria met:
```
<promise>BUG FIXED</promise>
```

## Current Status

**Failing tests at start:** [TEST_NAMES]

**Your mission:** Fix ALL of them iteratively.

---

**START DEBUGGING NOW**

Run the first failing test and analyze its error message.
