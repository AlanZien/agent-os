# Spec Implementation Process

Now that we have a spec and tasks list ready for implementation, we will proceed with implementation of this spec by following this multi-phase process:

PHASE 1: Determine which task group(s) from tasks.md should be implemented
PHASE 2: Delegate implementation to the implementer subagent
PHASE 3: After ALL task groups have been implemented, delegate to implementation-verifier to produce the final verification report.

Follow each of these phases and their individual workflows IN SEQUENCE:

## Multi-Phase Process

### PHASE 1: Determine which task group(s) to implement

First, check if the user has already provided instructions about which task group(s) to implement.

**If the user HAS provided instructions:** Proceed to PHASE 2 to delegate implementation of those specified task group(s) to the **implementer** subagent.

**If the user has NOT provided instructions:**

Read `agent-os/specs/[this-spec]/tasks.md` to review the available task groups, then output the following message to the user and WAIT for their response:

```
Should we proceed with implementation of all task groups in tasks.md?

If not, then please specify which task(s) to implement.
```

### PHASE 2: Delegate implementation to the implementer subagent

**First, check if test-plan.md exists:**

Check for: `agent-os/specs/[this-spec]/test-plan.md`

**If test-plan.md EXISTS, ask user about implementation mode:**

```
test-plan.md found for this spec.

Which implementation mode would you like to use?

1. Standard mode - Delegate to implementer subagent (one-shot implementation)
2. Ralph loop mode - Iterative TDD with Ralph Wiggum (auto-corrects until all tests pass)

Type 1 or 2:
```

**If test-plan.md DOES NOT exist:**

Skip the question and proceed with Standard mode only (Ralph requires test-plan.md).

---

#### Option 1: Standard Mode (Traditional Implementation)

Delegate to the **implementer** subagent to implement the specified task group(s):

Provide to the subagent:
- The specific task group(s) from `agent-os/specs/[this-spec]/tasks.md` including the parent task, all sub-tasks, and any sub-bullet points
- The path to this spec's documentation: `agent-os/specs/[this-spec]/spec.md`
- The path to this spec's requirements: `agent-os/specs/[this-spec]/planning/requirements.md`
- The path to this spec's visuals (if any): `agent-os/specs/[this-spec]/planning/visuals`

Instruct the subagent to:
1. Analyze the provided spec.md, requirements.md, and visuals (if any)
2. Analyze patterns in the codebase according to its built-in workflow
3. Implement the assigned task group according to requirements and standards
4. Update `agent-os/specs/[this-spec]/tasks.md` to mark completed tasks with `- [x]`

---

#### Option 2: Ralph Loop Mode (Iterative TDD)

**If user chose Ralph loop mode, follow these steps:**

##### Step 1: Ask for Ralph configuration

```
Ralph loop configuration:

1. Max iterations (default: 15):
2. Test command (leave empty for auto-detect):

Press Enter to use defaults, or specify values:
```

##### Step 2: Prepare Ralph prompt

Load template from: `.claude/ralph-prompts/tdd-task-group.md`

Replace these placeholders:
- `[TASK_GROUP_NAME]` → the task group name from PHASE 1
- `[SPEC_NAME]` → the spec folder name
- `[STANDARDS_LIST]` → compile list of relevant standards (see below)
- `[TEST_COMMAND_FOR_TASK_GROUP]` → test command from user or auto-detected

**Compile standards list:**
Include these standards as file references (one per line, prefixed with @):
```
@agent-os/standards/QUICK-REFERENCE.md
@agent-os/standards/testing/test-writing.md
@agent-os/standards/global-standards.md
[Add backend or frontend standards based on task type]
```

##### Step 3: Show summary

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ralph Loop - Ready to Launch
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Spec: [spec-name]
Task Group: [task-group-name]
Max Iterations: [number]
Test Command: [command]

Ralph will implement this task group using TDD:
✓ Read test-plan.md specifications
✓ Implement tests (RED-GREEN-REFACTOR)
✓ Self-correct until all tests pass
✓ Update tasks.md and sync to Notion

Ready to launch? (yes/no):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

##### Step 4: Launch Ralph loop

If user confirms, use the Skill tool to launch Ralph:

```
/ralph-loop "<prepared-prompt-from-step-2>" --completion-promise "TASK GROUP COMPLETE" --max-iterations <from-step-1>
```

Wait for Ralph to complete (outputs promise) or reach max iterations.

##### Step 5: Post-Ralph verification

After Ralph finishes, verify:
1. Check tasks.md was updated
2. Run test command to confirm all tests pass
3. Display results to user

If tests still failing after max iterations:
```
⚠️ Ralph reached max iterations with some tests still failing.

Options:
1. Run Ralph again with more iterations
2. Switch to Standard mode and fix manually
3. Review and debug the failures

Choose option:
```

### PHASE 3: Produce the final verification report

IF ALL task groups in tasks.md are marked complete with `- [x]`, then proceed with this step.  Otherwise, return to PHASE 1.

Assuming all tasks are marked complete, then delegate to the **implementation-verifier** subagent to do its implementation verification and produce its final verification report.

Provide to the subagent the following:
- The path to this spec: `agent-os/specs/[this-spec]`
Instruct the subagent to do the following:
  1. Run all of its final verifications according to its built-in workflow
  2. Produce the final verification report in `agent-os/specs/[this-spec]/verifications/final-verification.md`.
