# Test Planning Process

You are creating a comprehensive test plan from a given spec and requirements for a new feature.

## PHASE 1: Get and read the spec.md and/or requirements document(s)

You will need ONE OR BOTH of these files to inform your test plan:
- `agent-os/specs/[this-spec]/spec.md`
- `agent-os/specs/[this-spec]/planning/requirements.md`

IF you don't have ONE OR BOTH of those files in your current conversation context, then ask user to provide direction on where you can find them by outputting the following request then wait for user's response:

```
I'll need a spec.md or requirements.md (or both) in order to build a test plan.

Please direct me to where I can find those. If you haven't created them yet, you can run /shape-spec or /write-spec first.
```

## PHASE 2: Create test-plan.md

Once you have `spec.md` AND/OR `requirements.md`, use the **test-planner** subagent to create a comprehensive test plan with detailed test specifications.

Provide the test-planner:
- `agent-os/specs/[this-spec]/spec.md` (if present)
- `agent-os/specs/[this-spec]/planning/requirements.md` (if present)
- `agent-os/specs/[this-spec]/planning/visuals/` and its contents (if present)

The test-planner will create `test-plan.md` inside the spec folder with:
- Test summary table (count by layer and priority)
- Detailed test specifications in Given-When-Then format
- Priority levels (Critical/High/Medium/Low)
- Test dependencies and execution order
- References to spec.md requirements

## PHASE 3: Inform user

Once the test-planner has created `test-plan.md` output the following to inform the user:

```
Your test plan is ready!

✅ Test plan created: `agent-os/specs/[this-spec]/test-plan.md`
   - Total tests: [X] ([Critical: X, High: X, Medium: X, Low: X])
   - Database layer: [X] tests
   - API layer: [X] tests
   - UI layer: [X] tests

NEXT STEP 👉 Run `/create-tasks` to create an implementation task list that references this test plan!
```
