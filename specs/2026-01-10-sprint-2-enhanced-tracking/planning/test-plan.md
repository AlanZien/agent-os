# Test Plan: Sprint 2 - Enhanced Tracking

## Metadata
- **Feature**: Enhanced Tracking (Tests, Bugs, Metrics)
- **Spec**: agent-os/specs/2026-01-10-sprint-2-enhanced-tracking/spec.md
- **Requirements**: agent-os/specs/2026-01-10-sprint-2-enhanced-tracking/planning/requirements.md
- **Created**: 2026-01-10
- **Status**: Planning Complete
- **Track**: COMPLEX

## Test Summary

| Layer | Critical | High | Medium | Low | Total |
|-------|----------|------|--------|-----|-------|
| Database | 8 | 6 | 4 | 0 | 18 |
| Hooks (Unit) | 12 | 8 | 4 | 0 | 24 |
| UI Components | 10 | 14 | 8 | 2 | 34 |
| E2E | 8 | 10 | 4 | 0 | 22 |
| **Total** | **38** | **38** | **20** | **2** | **98** |

**Coverage Targets:**
- Critical paths: 100%
- High priority: 100%
- Medium priority: 80%
- Low priority: Deferred

---

## Database Layer

### Tests Table (9 tests)

#### 1. test_tests_table_creation_with_required_fields
**Priority:** Critical
**Given:**
- Database migration for `tests` table has been applied
- A valid feature exists with `id = 'feature-123'`
**When:** Insert a test with all required fields: `{ feature_id: 'feature-123', name: 'Unit test login', status: 'pending' }`
**Then:**
- Row is inserted successfully
- `id` is auto-generated (UUID)
- `created_at` and `updated_at` are auto-populated
- `description` defaults to null
**Related Requirement:** spec.md "Tests Table and Type Definitions"

#### 2. test_tests_table_feature_id_foreign_key_constraint
**Priority:** Critical
**Given:**
- Database migration for `tests` table has been applied
- No feature exists with `id = 'non-existent-feature'`
**When:** Insert a test with `{ feature_id: 'non-existent-feature', name: 'Test', status: 'pending' }`
**Then:**
- Insert fails with foreign key violation error
- No row is created
**Related Requirement:** spec.md "Tests Table - feature_id (required FK)"

#### 3. test_tests_table_status_enum_constraint
**Priority:** Critical
**Given:**
- Database migration for `tests` table has been applied
- A valid feature exists
**When:** Insert a test with invalid status: `{ feature_id: 'feature-123', name: 'Test', status: 'invalid_status' }`
**Then:**
- Insert fails with enum check constraint violation
- Only `pending`, `passed`, `failed` are accepted
**Related Requirement:** spec.md "Status enum: pending, passed, failed (3 values only)"

#### 4. test_tests_table_name_required_constraint
**Priority:** High
**Given:**
- Database migration for `tests` table has been applied
- A valid feature exists
**When:** Insert a test with null name: `{ feature_id: 'feature-123', name: null, status: 'pending' }`
**Then:**
- Insert fails with NOT NULL constraint violation
**Related Requirement:** spec.md "Tests Table - name"

#### 5. test_tests_table_cascade_delete_on_feature
**Priority:** High
**Given:**
- A feature exists with `id = 'feature-to-delete'`
- Tests exist linked to that feature
**When:** Delete the feature
**Then:**
- All tests linked to the feature are also deleted (CASCADE)
**Related Requirement:** spec.md "feature_id (required FK)"

#### 6. test_tests_table_updated_at_auto_update
**Priority:** Medium
**Given:**
- A test exists with `id = 'test-123'`
- Original `updated_at` is recorded
**When:** Update the test name
**Then:**
- `updated_at` is automatically updated to current timestamp
**Related Requirement:** spec.md "Tests Table - updated_at"

#### 7. test_tests_rls_policy_authenticated_user_can_read
**Priority:** High
**Given:**
- Tests exist for a feature belonging to a project owned by user A
- User A is authenticated
**When:** User A queries tests for that feature
**Then:**
- Tests are returned successfully
**Related Requirement:** spec.md "Add RLS policies following existing task patterns"

#### 8. test_tests_rls_policy_unauthenticated_cannot_access
**Priority:** High
**Given:**
- Tests exist in the database
- No user is authenticated
**When:** Query tests
**Then:**
- Query returns empty or access denied
**Related Requirement:** spec.md "RLS policies via feature -> project ownership chain"

#### 9. test_tests_rls_policy_other_user_cannot_access
**Priority:** High
**Given:**
- Tests exist for a feature belonging to project owned by user A
- User B is authenticated (different user)
**When:** User B queries those tests
**Then:**
- Query returns empty (no access to other users' tests)
**Related Requirement:** spec.md "RLS policies via feature -> project ownership chain"

---

### Bugs Table (9 tests)

#### 10. test_bugs_table_creation_with_required_fields
**Priority:** Critical
**Given:**
- Database migration for `bugs` table has been applied
- A valid feature exists with `id = 'feature-123'`
**When:** Insert a bug with required fields: `{ feature_id: 'feature-123', title: 'Login crash', severity: 'high', priority: 'urgent', status: 'open' }`
**Then:**
- Row is inserted successfully
- `id` is auto-generated (UUID)
- `created_at` and `updated_at` are auto-populated
- `task_id` and `description` default to null
**Related Requirement:** spec.md "Bugs Table and Type Definitions"

#### 11. test_bugs_table_feature_id_foreign_key_constraint
**Priority:** Critical
**Given:**
- Database migration for `bugs` table has been applied
- No feature exists with `id = 'non-existent-feature'`
**When:** Insert a bug with `{ feature_id: 'non-existent-feature', title: 'Bug', severity: 'low', priority: 'low', status: 'open' }`
**Then:**
- Insert fails with foreign key violation error
**Related Requirement:** spec.md "Bugs Table - feature_id (required FK)"

#### 12. test_bugs_table_task_id_optional_foreign_key
**Priority:** High
**Given:**
- A valid feature exists
- A valid task exists with `id = 'task-123'`
**When:** Insert a bug with optional task_id: `{ feature_id: 'feature-123', title: 'Bug', task_id: 'task-123', severity: 'medium', priority: 'medium', status: 'open' }`
**Then:**
- Row is inserted successfully with task_id linked
**Related Requirement:** spec.md "task_id (optional FK)"

#### 13. test_bugs_table_severity_enum_constraint
**Priority:** Critical
**Given:**
- Database migration for `bugs` table has been applied
- A valid feature exists
**When:** Insert a bug with invalid severity: `{ severity: 'super_critical' }`
**Then:**
- Insert fails with enum check constraint violation
- Only `critical`, `high`, `medium`, `low` are accepted
**Related Requirement:** spec.md "Severity enum: critical, high, medium, low"

#### 14. test_bugs_table_priority_enum_constraint
**Priority:** Critical
**Given:**
- Database migration for `bugs` table has been applied
- A valid feature exists
**When:** Insert a bug with invalid priority: `{ priority: 'super_urgent' }`
**Then:**
- Insert fails with enum check constraint violation
- Only `urgent`, `high`, `medium`, `low` are accepted
**Related Requirement:** spec.md "Priority enum: urgent, high, medium, low"

#### 15. test_bugs_table_status_enum_constraint
**Priority:** Critical
**Given:**
- Database migration for `bugs` table has been applied
- A valid feature exists
**When:** Insert a bug with invalid status: `{ status: 'cancelled' }`
**Then:**
- Insert fails with enum check constraint violation
- Only `open`, `in_progress`, `resolved`, `closed`, `wont_fix` are accepted
**Related Requirement:** spec.md "Status enum: open, in_progress, resolved, closed, wont_fix"

#### 16. test_bugs_table_title_required_constraint
**Priority:** High
**Given:**
- Database migration for `bugs` table has been applied
- A valid feature exists
**When:** Insert a bug with null title
**Then:**
- Insert fails with NOT NULL constraint violation
**Related Requirement:** spec.md "Bugs Table - title"

#### 17. test_bugs_table_cascade_delete_on_feature
**Priority:** High
**Given:**
- A feature exists with linked bugs
**When:** Delete the feature
**Then:**
- All bugs linked to the feature are also deleted (CASCADE)
**Related Requirement:** spec.md "feature_id (required FK)"

#### 18. test_bugs_table_task_id_nullable_on_task_delete
**Priority:** Medium
**Given:**
- A bug exists with `task_id = 'task-to-delete'`
**When:** Delete the task
**Then:**
- Bug remains but `task_id` is set to null (SET NULL behavior)
**Related Requirement:** spec.md "task_id (optional FK) - for traceability"

---

## Hooks Layer (Unit Tests)

### useTests Hook (12 tests)

#### 19. test_useTests_fetches_tests_by_feature_id
**Priority:** Critical
**Given:**
- Feature with `id = 'feature-123'` has 3 tests in database
- Component renders `useTests('feature-123')`
**When:** Hook is called
**Then:**
- Returns `{ data: [test1, test2, test3], isLoading: false, error: null }`
- Tests are fetched from Supabase `tests` table filtered by `feature_id`
**Related Requirement:** spec.md "useTests(featureId) to fetch tests by feature"

#### 20. test_useTests_returns_empty_array_when_no_tests
**Priority:** High
**Given:**
- Feature with `id = 'feature-empty'` has 0 tests
- Component renders `useTests('feature-empty')`
**When:** Hook is called
**Then:**
- Returns `{ data: [], isLoading: false, error: null }`
**Related Requirement:** spec.md "useTests(featureId)"

#### 21. test_useTests_handles_loading_state
**Priority:** Medium
**Given:**
- Component renders `useTests('feature-123')`
- Supabase request is pending
**When:** Hook is initially called
**Then:**
- Returns `{ data: undefined, isLoading: true, error: null }`
**Related Requirement:** spec.md "Follow useTasks.ts hook pattern"

#### 22. test_useTests_handles_error_state
**Priority:** High
**Given:**
- Supabase returns an error (e.g., network failure)
- Component renders `useTests('feature-123')`
**When:** Hook is called
**Then:**
- Returns `{ data: undefined, isLoading: false, error: Error }`
**Related Requirement:** spec.md "Follow useTasks.ts hook pattern"

#### 23. test_useTest_fetches_single_test_by_id
**Priority:** High
**Given:**
- Test with `id = 'test-456'` exists
- Component renders `useTest('test-456')`
**When:** Hook is called
**Then:**
- Returns single test object with all fields
**Related Requirement:** spec.md "useTest(testId) for single test retrieval"

#### 24. test_useCreateTest_creates_test_successfully
**Priority:** Critical
**Given:**
- Feature with `id = 'feature-123'` exists
- Component renders `useCreateTest()`
**When:** `mutate({ feature_id: 'feature-123', name: 'New test', status: 'pending' })` is called
**Then:**
- New test is created in database
- Query cache for `['tests', 'feature', 'feature-123']` is invalidated
- `onSuccess` callback is triggered
**Related Requirement:** spec.md "useCreateTest() mutation"

#### 25. test_useCreateTest_fails_with_validation_error
**Priority:** High
**Given:**
- Component renders `useCreateTest()`
**When:** `mutate({ feature_id: 'feature-123', name: '' })` is called (empty name)
**Then:**
- Mutation fails with validation error
- `onError` callback is triggered
**Related Requirement:** spec.md "useCreateTest()"

#### 26. test_useUpdateTest_updates_test_successfully
**Priority:** Critical
**Given:**
- Test with `id = 'test-123'` exists
- Component renders `useUpdateTest()`
**When:** `mutate({ id: 'test-123', name: 'Updated name' })` is called
**Then:**
- Test is updated in database
- Query cache is invalidated
**Related Requirement:** spec.md "useUpdateTest() mutation"

#### 27. test_useDeleteTest_deletes_test_successfully
**Priority:** Critical
**Given:**
- Test with `id = 'test-123'` exists for feature `feature-456`
- Component renders `useDeleteTest()`
**When:** `mutate({ id: 'test-123', featureId: 'feature-456' })` is called
**Then:**
- Test is deleted from database
- Query cache for feature tests is invalidated
**Related Requirement:** spec.md "useDeleteTest() mutation"

#### 28. test_useUpdateTestStatus_optimistic_update
**Priority:** Critical
**Given:**
- Test with `id = 'test-123'`, `status = 'pending'` exists
- Component renders `useUpdateTestStatus()`
**When:** `mutate({ id: 'test-123', status: 'passed', featureId: 'feature-456' })` is called
**Then:**
- UI immediately updates to show `passed` status (optimistic)
- If API fails, rolls back to `pending`
**Related Requirement:** spec.md "useUpdateTestStatus() with optimistic updates"

#### 29. test_useUpdateTestStatus_rollback_on_error
**Priority:** High
**Given:**
- Test with `id = 'test-123'`, `status = 'pending'` exists
- API will return an error
- Component renders `useUpdateTestStatus()`
**When:** `mutate({ id: 'test-123', status: 'passed', featureId: 'feature-456' })` is called
**Then:**
- UI optimistically shows `passed`
- When API fails, UI rolls back to `pending`
- Error toast is displayed
**Related Requirement:** spec.md "useUpdateTestStatus() with optimistic updates"

#### 30. test_useTests_query_keys_structure
**Priority:** Medium
**Given:**
- `TEST_QUERY_KEYS` is exported from types/test.ts
**When:** Examining the query keys
**Then:**
- `TEST_QUERY_KEYS.all` equals `['tests']`
- `TEST_QUERY_KEYS.byFeature('f1')` equals `['tests', 'feature', 'f1']`
- `TEST_QUERY_KEYS.detail('t1')` equals `['tests', 'detail', 't1']`
**Related Requirement:** spec.md "Define TEST_QUERY_KEYS for cache management"

---

### useBugs Hook (12 tests)

#### 31. test_useBugs_fetches_bugs_by_feature_id
**Priority:** Critical
**Given:**
- Feature with `id = 'feature-123'` has 2 bugs in database
- Component renders `useBugs('feature-123')`
**When:** Hook is called
**Then:**
- Returns `{ data: [bug1, bug2], isLoading: false, error: null }`
**Related Requirement:** spec.md "useBugs(featureId) to fetch bugs by feature"

#### 32. test_useBugs_returns_empty_array_when_no_bugs
**Priority:** High
**Given:**
- Feature with `id = 'feature-clean'` has 0 bugs
- Component renders `useBugs('feature-clean')`
**When:** Hook is called
**Then:**
- Returns `{ data: [], isLoading: false, error: null }`
**Related Requirement:** spec.md "useBugs(featureId)"

#### 33. test_useBugs_handles_loading_state
**Priority:** Medium
**Given:**
- Component renders `useBugs('feature-123')`
- Supabase request is pending
**When:** Hook is initially called
**Then:**
- Returns `{ data: undefined, isLoading: true, error: null }`
**Related Requirement:** spec.md "Follow useTasks.ts hook pattern"

#### 34. test_useBugs_handles_error_state
**Priority:** High
**Given:**
- Supabase returns an error
- Component renders `useBugs('feature-123')`
**When:** Hook is called
**Then:**
- Returns `{ data: undefined, isLoading: false, error: Error }`
**Related Requirement:** spec.md "Follow useTasks.ts hook pattern"

#### 35. test_useBug_fetches_single_bug_by_id
**Priority:** High
**Given:**
- Bug with `id = 'bug-789'` exists
- Component renders `useBug('bug-789')`
**When:** Hook is called
**Then:**
- Returns single bug object with all fields including optional task_id
**Related Requirement:** spec.md "useBug(bugId) for single bug retrieval"

#### 36. test_useCreateBug_creates_bug_successfully
**Priority:** Critical
**Given:**
- Feature with `id = 'feature-123'` exists
- Component renders `useCreateBug()`
**When:** `mutate({ feature_id: 'feature-123', title: 'New bug', severity: 'high', priority: 'urgent', status: 'open' })` is called
**Then:**
- New bug is created in database
- Query cache is invalidated
**Related Requirement:** spec.md "useCreateBug() mutation"

#### 37. test_useCreateBug_with_optional_task_id
**Priority:** High
**Given:**
- Feature and Task exist
- Component renders `useCreateBug()`
**When:** `mutate({ feature_id: 'feature-123', title: 'Bug', task_id: 'task-fix', severity: 'medium', priority: 'medium', status: 'open' })` is called
**Then:**
- Bug is created with task_id linked
**Related Requirement:** spec.md "task_id (optional FK)"

#### 38. test_useUpdateBug_updates_bug_successfully
**Priority:** Critical
**Given:**
- Bug with `id = 'bug-123'` exists
- Component renders `useUpdateBug()`
**When:** `mutate({ id: 'bug-123', severity: 'critical', priority: 'urgent' })` is called
**Then:**
- Bug is updated in database
- Query cache is invalidated
**Related Requirement:** spec.md "useUpdateBug() mutation"

#### 39. test_useDeleteBug_deletes_bug_successfully
**Priority:** Critical
**Given:**
- Bug with `id = 'bug-123'` exists
- Component renders `useDeleteBug()`
**When:** `mutate({ id: 'bug-123', featureId: 'feature-456' })` is called
**Then:**
- Bug is deleted from database
- Query cache is invalidated
**Related Requirement:** spec.md "useDeleteBug() mutation"

#### 40. test_useUpdateBugStatus_optimistic_update
**Priority:** Critical
**Given:**
- Bug with `id = 'bug-123'`, `status = 'open'` exists
- Component renders `useUpdateBugStatus()`
**When:** `mutate({ id: 'bug-123', status: 'in_progress', featureId: 'feature-456' })` is called
**Then:**
- UI immediately updates to show `in_progress` status
- Database is updated asynchronously
**Related Requirement:** spec.md "useUpdateBugStatus() with optimistic updates"

#### 41. test_useUpdateBugStatus_status_workflow
**Priority:** High
**Given:**
- Bug with `status = 'in_progress'` exists
- Component renders `useUpdateBugStatus()`
**When:** `mutate({ status: 'resolved' })` is called
**Then:**
- Status transitions from `in_progress` to `resolved` successfully
**Related Requirement:** spec.md "Status enum: open, in_progress, resolved, closed, wont_fix"

#### 42. test_useBugs_query_keys_structure
**Priority:** Medium
**Given:**
- `BUG_QUERY_KEYS` is exported from types/bug.ts
**When:** Examining the query keys
**Then:**
- `BUG_QUERY_KEYS.all` equals `['bugs']`
- `BUG_QUERY_KEYS.byFeature('f1')` equals `['bugs', 'feature', 'f1']`
- `BUG_QUERY_KEYS.detail('b1')` equals `['bugs', 'detail', 'b1']`
**Related Requirement:** spec.md "Define BUG_QUERY_KEYS for cache management"

---

## UI Components Layer

### TestsList Component (4 tests)

#### 43. test_TestsList_renders_tests_for_feature
**Priority:** Critical
**Given:**
- `useBugs('feature-123')` returns 3 tests
- Component `<TestsList featureId="feature-123" />` is rendered
**When:** Component mounts
**Then:**
- 3 TestCard components are rendered
- Each shows name, status badge, description preview
**Related Requirement:** spec.md "TestsList: List view of tests for a feature"

#### 44. test_TestsList_renders_empty_state
**Priority:** High
**Given:**
- `useTests('feature-empty')` returns empty array
- Component `<TestsList featureId="feature-empty" />` is rendered
**When:** Component mounts
**Then:**
- Empty state message is displayed (e.g., "No tests yet")
- Add test button is visible
**Related Requirement:** spec.md "TestsList: List view of tests"

#### 45. test_TestsList_shows_loading_skeleton
**Priority:** Medium
**Given:**
- `useTests('feature-123')` is loading (`isLoading: true`)
- Component `<TestsList featureId="feature-123" />` is rendered
**When:** Component mounts
**Then:**
- Loading skeleton is displayed
**Related Requirement:** spec.md "Follow SprintCard skeleton pattern"

#### 46. test_TestsList_shows_error_state
**Priority:** High
**Given:**
- `useTests('feature-123')` returns error
- Component `<TestsList featureId="feature-123" />` is rendered
**When:** Component mounts
**Then:**
- Error message is displayed
- Retry button may be available
**Related Requirement:** spec.md "Follow useTasks.ts hook pattern"

---

### TestCard Component (4 tests)

#### 47. test_TestCard_renders_test_details
**Priority:** High
**Given:**
- Test: `{ id: 't1', name: 'Login test', description: 'Test login flow', status: 'passed' }`
- Component `<TestCard test={test} />` is rendered
**When:** Component mounts
**Then:**
- Name "Login test" is displayed
- Description preview is shown
- Status badge shows "Passed" with green color
**Related Requirement:** spec.md "TestCard: Individual test item with status indicator"

#### 48. test_TestCard_status_badge_colors
**Priority:** High
**Given:**
- Tests with each status: `pending`, `passed`, `failed`
**When:** TestCard renders each test
**Then:**
- Pending: gray badge
- Passed: green badge
- Failed: red badge
**Related Requirement:** spec.md "TEST_STATUS_CONFIG with labels and colors"

#### 49. test_TestCard_dropdown_menu_actions
**Priority:** High
**Given:**
- Test is rendered in TestCard
- User clicks the menu button (more icon)
**When:** Dropdown opens
**Then:**
- Edit option is visible
- Delete option is visible
**Related Requirement:** spec.md "TestCard: edit/delete actions via dropdown menu"

#### 50. test_TestCard_quick_status_toggle
**Priority:** Medium
**Given:**
- Test with `status = 'pending'` is rendered
- `useUpdateTestStatus` hook is available
**When:** User clicks status badge or toggle button
**Then:**
- Status can be quickly changed (pending -> passed -> failed -> pending cycle)
**Related Requirement:** spec.md "useUpdateTestStatus() for quick status toggles"

---

### CreateTestModal Component (6 tests)

#### 51. test_CreateTestModal_renders_form_fields
**Priority:** Critical
**Given:**
- Modal `<CreateTestModal isOpen={true} featureId="feature-123" />` is rendered
**When:** Modal opens
**Then:**
- Name input field is visible (required)
- Description textarea is visible (optional)
- Status select is visible with pending/passed/failed options
- Create and Cancel buttons are visible
**Related Requirement:** spec.md "CreateTestModal: Form with name (required), description (optional), status select"

#### 52. test_CreateTestModal_validates_required_name
**Priority:** Critical
**Given:**
- CreateTestModal is open
- Name field is empty
**When:** User clicks Create button
**Then:**
- Validation error "Name is required" is displayed
- Form is not submitted
**Related Requirement:** spec.md "CreateTestModal follows CreateTaskModal pattern"

#### 53. test_CreateTestModal_submits_successfully
**Priority:** Critical
**Given:**
- CreateTestModal is open
- Name: "Unit test auth"
- Description: "Test authentication"
- Status: "pending"
**When:** User clicks Create button
**Then:**
- `useCreateTest.mutate()` is called with correct data
- Success toast "Test created successfully" is shown
- Modal closes
**Related Requirement:** spec.md "CreateTestModal with toast notifications on success/error"

#### 54. test_CreateTestModal_shows_error_toast_on_failure
**Priority:** High
**Given:**
- CreateTestModal is open
- API will return error
**When:** User fills form and clicks Create
**Then:**
- Error toast is displayed with error message
- Modal remains open
**Related Requirement:** spec.md "toast notifications on success/error"

#### 55. test_CreateTestModal_resets_form_on_open
**Priority:** Medium
**Given:**
- CreateTestModal was previously used and closed
**When:** Modal is opened again
**Then:**
- All form fields are reset to defaults
- No validation errors are shown
**Related Requirement:** spec.md "Form reset on modal open/close"

#### 56. test_CreateTestModal_cancel_closes_without_saving
**Priority:** Medium
**Given:**
- CreateTestModal is open
- User has filled some fields
**When:** User clicks Cancel button
**Then:**
- Modal closes
- No API call is made
- Form data is discarded
**Related Requirement:** spec.md "CreateTestModal follows CreateTaskModal pattern"

---

### EditTestModal Component (4 tests)

#### 57. test_EditTestModal_pre_populates_form
**Priority:** Critical
**Given:**
- Test: `{ id: 't1', name: 'Existing test', description: 'Desc', status: 'pending' }`
- Modal `<EditTestModal isOpen={true} test={test} />` is rendered
**When:** Modal opens
**Then:**
- Name field shows "Existing test"
- Description shows "Desc"
- Status select shows "Pending"
**Related Requirement:** spec.md "EditTestModal: Pre-populated form for editing"

#### 58. test_EditTestModal_updates_successfully
**Priority:** Critical
**Given:**
- EditTestModal is open with existing test
- User changes name to "Updated test name"
**When:** User clicks Save button
**Then:**
- `useUpdateTest.mutate()` is called with updated data
- Success toast is shown
- Modal closes
**Related Requirement:** spec.md "EditTestModal follows EditTaskModal pattern"

#### 59. test_EditTestModal_validates_name_not_empty
**Priority:** High
**Given:**
- EditTestModal is open
- User clears the name field
**When:** User clicks Save
**Then:**
- Validation error is displayed
- Form is not submitted
**Related Requirement:** spec.md "EditTestModal with Zod validation"

#### 60. test_EditTestModal_shows_pending_state
**Priority:** Medium
**Given:**
- EditTestModal is open
- Save button is clicked
**When:** API call is pending
**Then:**
- Save button shows loading state ("Saving...")
- Form fields are disabled
**Related Requirement:** spec.md "EditTestModal follows EditTaskModal pattern"

---

### BugsList Component (4 tests)

#### 61. test_BugsList_renders_bugs_for_feature
**Priority:** Critical
**Given:**
- `useBugs('feature-123')` returns 2 bugs
- Component `<BugsList featureId="feature-123" />` is rendered
**When:** Component mounts
**Then:**
- 2 BugCard components are rendered
**Related Requirement:** spec.md "BugsList: List view of bugs for a feature"

#### 62. test_BugsList_sorts_by_severity_then_priority
**Priority:** High
**Given:**
- Bugs: [{ severity: 'low', priority: 'low' }, { severity: 'critical', priority: 'urgent' }, { severity: 'high', priority: 'medium' }]
- Component `<BugsList featureId="feature-123" />` is rendered
**When:** Component mounts
**Then:**
- Critical bug appears first
- High severity bug appears second
- Low severity bug appears last
**Related Requirement:** spec.md "BugsList: sorted by severity then priority"

#### 63. test_BugsList_renders_empty_state
**Priority:** High
**Given:**
- `useBugs('feature-clean')` returns empty array
**When:** Component mounts
**Then:**
- Empty state message is displayed
- Add bug button is visible
**Related Requirement:** spec.md "BugsList: List view of bugs"

#### 64. test_BugsList_shows_loading_skeleton
**Priority:** Medium
**Given:**
- `useBugs('feature-123')` is loading
**When:** Component mounts
**Then:**
- Loading skeleton is displayed
**Related Requirement:** spec.md "Follow SprintCard skeleton pattern"

---

### BugCard Component (6 tests)

#### 65. test_BugCard_renders_bug_details
**Priority:** High
**Given:**
- Bug: `{ id: 'b1', title: 'Login crash', severity: 'critical', priority: 'urgent', status: 'open' }`
**When:** BugCard renders
**Then:**
- Title "Login crash" is displayed
- Severity badge shows "Critical" (red)
- Priority badge shows "Urgent"
- Status badge shows "Open"
**Related Requirement:** spec.md "BugCard: Displays title, severity badge, priority badge, status badge"

#### 66. test_BugCard_severity_badge_colors
**Priority:** High
**Given:**
- Bugs with each severity: `critical`, `high`, `medium`, `low`
**When:** BugCard renders each bug
**Then:**
- Critical: red badge
- High: orange badge
- Medium: amber badge
- Low: gray badge
**Related Requirement:** spec.md "Severity badges: critical=red, high=orange, medium=amber, low=gray"

#### 67. test_BugCard_shows_linked_task_reference
**Priority:** High
**Given:**
- Bug with `task_id = 'task-fix-123'`
- Task has title "Fix login crash"
**When:** BugCard renders
**Then:**
- Linked task reference is displayed (e.g., "Fix: Fix login crash")
**Related Requirement:** spec.md "BugCard: optional linked task reference"

#### 68. test_BugCard_no_task_reference_when_null
**Priority:** Medium
**Given:**
- Bug with `task_id = null`
**When:** BugCard renders
**Then:**
- No task reference section is shown
**Related Requirement:** spec.md "task_id (optional FK)"

#### 69. test_BugCard_dropdown_menu_actions
**Priority:** High
**Given:**
- Bug is rendered in BugCard
- User clicks menu button
**When:** Dropdown opens
**Then:**
- Edit option is visible
- Delete option is visible
**Related Requirement:** spec.md "BugCard with edit/delete actions"

#### 70. test_BugCard_priority_badge_display
**Priority:** Medium
**Given:**
- Bugs with priorities: `urgent`, `high`, `medium`, `low`
**When:** BugCard renders each bug
**Then:**
- Each priority has distinct visual style
**Related Requirement:** spec.md "Priority enum: urgent, high, medium, low"

---

### CreateBugModal Component (6 tests)

#### 71. test_CreateBugModal_renders_all_form_fields
**Priority:** Critical
**Given:**
- Modal `<CreateBugModal isOpen={true} featureId="feature-123" />` is rendered
**When:** Modal opens
**Then:**
- Title input (required)
- Description textarea
- Severity select (critical/high/medium/low)
- Priority select (urgent/high/medium/low)
- Status select (open/in_progress/resolved/closed/wont_fix)
- Task_id select (optional)
- Create and Cancel buttons
**Related Requirement:** spec.md "CreateBugModal: Form with all fields"

#### 72. test_CreateBugModal_validates_required_title
**Priority:** Critical
**Given:**
- CreateBugModal is open
- Title field is empty
**When:** User clicks Create
**Then:**
- Validation error "Title is required"
- Form not submitted
**Related Requirement:** spec.md "title (required)"

#### 73. test_CreateBugModal_submits_successfully
**Priority:** Critical
**Given:**
- CreateBugModal is open
- Title: "Crash on login"
- Severity: "critical"
- Priority: "urgent"
- Status: "open"
**When:** User clicks Create
**Then:**
- `useCreateBug.mutate()` called with correct data
- Success toast shown
- Modal closes
**Related Requirement:** spec.md "CreateBugModal with toast notifications"

#### 74. test_CreateBugModal_optional_task_select
**Priority:** High
**Given:**
- CreateBugModal is open
- Tasks exist for the feature
**When:** User opens task_id select
**Then:**
- Available tasks are shown as options
- "None" option is available
**Related Requirement:** spec.md "optional task_id select"

#### 75. test_CreateBugModal_defaults_status_to_open
**Priority:** Medium
**Given:**
- CreateBugModal is open
**When:** Modal opens
**Then:**
- Status field defaults to "open"
**Related Requirement:** spec.md "Bug status workflow: open -> ..."

#### 76. test_CreateBugModal_shows_error_on_failure
**Priority:** High
**Given:**
- CreateBugModal is open
- API will fail
**When:** User submits form
**Then:**
- Error toast is displayed
- Modal remains open
**Related Requirement:** spec.md "toast notifications on error"

---

### EditBugModal Component (4 tests)

#### 77. test_EditBugModal_pre_populates_all_fields
**Priority:** Critical
**Given:**
- Bug with all fields populated
- `<EditBugModal isOpen={true} bug={bug} />` rendered
**When:** Modal opens
**Then:**
- All fields show existing values
- Task_id select shows linked task if any
**Related Requirement:** spec.md "EditBugModal: Pre-populated form with all fields editable"

#### 78. test_EditBugModal_updates_successfully
**Priority:** Critical
**Given:**
- EditBugModal is open
- User changes severity from 'high' to 'critical'
**When:** User clicks Save
**Then:**
- `useUpdateBug.mutate()` called
- Success toast shown
- Modal closes
**Related Requirement:** spec.md "EditBugModal for editing bugs"

#### 79. test_EditBugModal_can_link_to_fix_task
**Priority:** High
**Given:**
- EditBugModal is open for bug with no task_id
- User selects a task from task_id dropdown
**When:** User clicks Save
**Then:**
- Bug is updated with new task_id
**Related Requirement:** spec.md "task_id (optional FK) for traceability"

#### 80. test_EditBugModal_can_remove_task_link
**Priority:** Medium
**Given:**
- EditBugModal is open for bug with task_id
- User selects "None" from task_id dropdown
**When:** User clicks Save
**Then:**
- Bug is updated with task_id = null
**Related Requirement:** spec.md "task_id (optional FK)"

---

### FeatureMetricsBadge Component (4 tests)

#### 81. test_FeatureMetricsBadge_displays_task_completion_percentage
**Priority:** Critical
**Given:**
- Feature has 5 tasks, 4 done
- `<FeatureMetricsBadge featureId="f1" />` rendered
**When:** Component mounts
**Then:**
- Shows "80%" with checkmark icon
**Related Requirement:** spec.md "Task completion %: (tasks with status 'done' / total tasks) * 100"

#### 82. test_FeatureMetricsBadge_displays_test_pass_rate
**Priority:** Critical
**Given:**
- Feature has 6 tests, 5 passed
- `<FeatureMetricsBadge featureId="f1" />` rendered
**When:** Component mounts
**Then:**
- Shows "5/6" with flask/beaker icon
**Related Requirement:** spec.md "Test pass rate: (tests with status 'passed' / total tests) * 100"

#### 83. test_FeatureMetricsBadge_combined_format
**Priority:** High
**Given:**
- Feature has 5 tasks (4 done) and 6 tests (5 passed)
**When:** FeatureMetricsBadge renders
**Then:**
- Display format: "80% | 5/6"
**Related Requirement:** spec.md "Format: 80% | 5/6"

#### 84. test_FeatureMetricsBadge_muted_when_no_data
**Priority:** Medium
**Given:**
- Feature has 0 tasks and 0 tests
**When:** FeatureMetricsBadge renders
**Then:**
- Badge uses muted styling
- Shows "- | -" or similar placeholder
**Related Requirement:** spec.md "Muted styling when no tasks or tests exist"

---

### FeatureMetricsDetail Component (4 tests)

#### 85. test_FeatureMetricsDetail_shows_task_progress_bar
**Priority:** Critical
**Given:**
- Feature has 10 tasks, 7 done
- `<FeatureMetricsDetail featureId="f1" />` rendered
**When:** Component mounts
**Then:**
- Progress bar shows 70% filled
- Text shows "7/10 tasks (70%)"
**Related Requirement:** spec.md "Show progress bar for task completion with count and percentage"

#### 86. test_FeatureMetricsDetail_shows_test_breakdown
**Priority:** Critical
**Given:**
- Feature has 10 tests: 6 passed, 2 failed, 2 pending
**When:** FeatureMetricsDetail renders
**Then:**
- Progress bar shows pass rate
- Breakdown: "6 passed, 2 failed, 2 pending"
**Related Requirement:** spec.md "Show progress bar for test pass rate with passed/failed/pending breakdown"

#### 87. test_FeatureMetricsDetail_shows_bug_count_by_severity
**Priority:** High
**Given:**
- Feature has bugs: 1 critical, 2 high, 3 medium, 1 low
**When:** FeatureMetricsDetail renders
**Then:**
- Shows icon + count for each severity level
- Critical: 1, High: 2, Medium: 3, Low: 1
**Related Requirement:** spec.md "Show bug count by severity (icon + count for each level)"

#### 88. test_FeatureMetricsDetail_handles_empty_state
**Priority:** Medium
**Given:**
- Feature has 0 tasks, 0 tests, 0 bugs
**When:** FeatureMetricsDetail renders
**Then:**
- Shows appropriate empty states for each section
- No progress bars (or 0%)
**Related Requirement:** spec.md "FeatureMetricsDetail component"

---

### ProjectTestsSummaryCard Component (3 tests)

#### 89. test_ProjectTestsSummaryCard_displays_test_counts
**Priority:** Critical
**Given:**
- Project has features with total 20 tests: 15 passed, 3 failed, 2 pending
- `<ProjectTestsSummaryCard projectId="p1" />` rendered
**When:** Component mounts
**Then:**
- Total: 20
- Passed: 15 (green)
- Failed: 3 (red)
- Pending: 2 (gray)
- Pass rate: 75%
**Related Requirement:** spec.md "ProjectTestsSummaryCard: total tests, passed count, failed count, pending count, overall pass rate"

#### 90. test_ProjectTestsSummaryCard_empty_state
**Priority:** High
**Given:**
- Project has 0 tests
**When:** ProjectTestsSummaryCard renders
**Then:**
- Shows "No tests" message
- Pass rate shows 0% or N/A
**Related Requirement:** spec.md "ProjectTestsSummaryCard to ProjectOverview"

#### 91. test_ProjectTestsSummaryCard_loading_state
**Priority:** Medium
**Given:**
- Data is loading
**When:** ProjectTestsSummaryCard renders
**Then:**
- Shows loading skeleton matching existing card styles
**Related Requirement:** spec.md "Maintain existing card grid layout"

---

### ProjectBugsSeverityCard Component (3 tests)

#### 92. test_ProjectBugsSeverityCard_groups_bugs_by_severity
**Priority:** Critical
**Given:**
- Project has bugs: 2 critical, 5 high, 8 medium, 3 low
- `<ProjectBugsSeverityCard projectId="p1" />` rendered
**When:** Component mounts
**Then:**
- Critical: 2 (red)
- High: 5 (orange)
- Medium: 8 (amber)
- Low: 3 (gray)
- Total open: shows aggregate
**Related Requirement:** spec.md "ProjectBugsSeverityCard: bugs grouped by severity with counts, total open bugs count"

#### 93. test_ProjectBugsSeverityCard_shows_total_open_bugs
**Priority:** High
**Given:**
- Project has 18 total bugs, 12 open (not resolved/closed/wont_fix)
**When:** ProjectBugsSeverityCard renders
**Then:**
- Shows "12 open bugs" prominently
**Related Requirement:** spec.md "total open bugs count"

#### 94. test_ProjectBugsSeverityCard_empty_state
**Priority:** Medium
**Given:**
- Project has 0 bugs
**When:** ProjectBugsSeverityCard renders
**Then:**
- Shows "No bugs" message
- May show success indicator
**Related Requirement:** spec.md "ProjectBugsSeverityCard to ProjectOverview"

---

### ProjectHealthIndicatorCard Component (2 tests)

#### 95. test_ProjectHealthIndicatorCard_healthy_status
**Priority:** High
**Given:**
- Feature completion > 80%
- Test pass rate > 90%
- 0 critical bugs open
**When:** ProjectHealthIndicatorCard renders
**Then:**
- Shows "Healthy" status with green indicator
**Related Requirement:** spec.md "Overall health indicator: healthy/warning/critical"

#### 96. test_ProjectHealthIndicatorCard_critical_status
**Priority:** High
**Given:**
- 3+ critical bugs open OR test pass rate < 50%
**When:** ProjectHealthIndicatorCard renders
**Then:**
- Shows "Critical" status with red indicator
**Related Requirement:** spec.md "combines feature completion, test pass rate, open critical bugs"

---

## E2E Tests

> **Tool:** Playwright (`e2e/*.spec.ts`)

### Test CRUD E2E (6 tests)

#### E2E-1. e2e_test_create_flow
**Priority:** Critical
**Preconditions:**
- User is authenticated
- Project and feature exist
- User is on feature detail page

**Steps:**
1. Click "Add Test" button
2. Fill name: "E2E Test Login"
3. Fill description: "Test login functionality"
4. Select status: "pending"
5. Click "Create" button
6. Verify toast "Test created successfully"
7. Verify new test appears in TestsList

**Success Criteria:**
- Test is visible in list with correct name and status
- Page does not reload (SPA behavior)

**Related User Story:** requirements.md "Create a test for a feature"

#### E2E-2. e2e_test_status_update_flow
**Priority:** Critical
**Preconditions:**
- User is authenticated
- Test exists with status "pending"

**Steps:**
1. Navigate to feature with test
2. Locate test card
3. Click status badge or use quick toggle
4. Change status to "passed"
5. Verify status badge updates immediately (optimistic)
6. Refresh page
7. Verify status persisted as "passed"

**Success Criteria:**
- Status visually updates instantly
- Status persists after refresh

**Related User Story:** requirements.md "Update test status (pending -> passed/failed)"

#### E2E-3. e2e_test_edit_flow
**Priority:** High
**Preconditions:**
- User is authenticated
- Test "Original Name" exists

**Steps:**
1. Click menu button on test card
2. Click "Edit" option
3. Verify modal opens with pre-populated data
4. Change name to "Updated Name"
5. Click "Save"
6. Verify toast "Test updated successfully"
7. Verify test card shows "Updated Name"

**Success Criteria:**
- Edit modal shows existing values
- Changes are reflected in list

**Related User Story:** requirements.md "Edit test details"

#### E2E-4. e2e_test_delete_flow
**Priority:** High
**Preconditions:**
- User is authenticated
- Test "Test to Delete" exists

**Steps:**
1. Click menu button on test card
2. Click "Delete" option
3. Verify confirmation dialog appears
4. Click "Delete" to confirm
5. Verify test removed from list
6. Verify toast "Test deleted successfully"

**Success Criteria:**
- Confirmation prevents accidental deletion
- Test no longer appears in list

**Related User Story:** requirements.md "Delete a test"

#### E2E-5. e2e_tests_list_display
**Priority:** High
**Preconditions:**
- User is authenticated
- Feature has multiple tests with various statuses

**Steps:**
1. Navigate to feature detail
2. Locate Tests section
3. Verify all tests are displayed
4. Verify each test shows name, status badge, description

**Success Criteria:**
- All tests visible
- Status badges have correct colors

**Related User Story:** requirements.md "View all tests for a feature"

#### E2E-6. e2e_tests_empty_state
**Priority:** Medium
**Preconditions:**
- User is authenticated
- Feature has no tests

**Steps:**
1. Navigate to feature detail
2. Locate Tests section
3. Verify empty state message
4. Verify "Add Test" button is visible

**Success Criteria:**
- User understands there are no tests
- Easy path to add first test

**Related User Story:** requirements.md "TestsList component"

---

### Bug CRUD E2E (8 tests)

#### E2E-7. e2e_bug_create_flow
**Priority:** Critical
**Preconditions:**
- User is authenticated
- Feature exists

**Steps:**
1. Click "Report Bug" button
2. Fill title: "Login crashes on iOS"
3. Fill description: "App crashes when..."
4. Select severity: "critical"
5. Select priority: "urgent"
6. Leave status as default "open"
7. Click "Create"
8. Verify toast and bug in list

**Success Criteria:**
- Bug appears with correct severity/priority badges
- Red severity badge for critical

**Related User Story:** requirements.md "Create a bug for a feature"

#### E2E-8. e2e_bug_create_with_task_link
**Priority:** High
**Preconditions:**
- User is authenticated
- Feature has existing tasks

**Steps:**
1. Open CreateBugModal
2. Fill required fields
3. Select a task from task_id dropdown
4. Create bug
5. Verify bug card shows linked task reference

**Success Criteria:**
- Task reference visible on bug card

**Related User Story:** requirements.md "Link bug to fix task"

#### E2E-9. e2e_bug_status_workflow
**Priority:** Critical
**Preconditions:**
- Bug exists with status "open"

**Steps:**
1. Edit bug, change status to "in_progress"
2. Save and verify
3. Edit bug, change status to "resolved"
4. Save and verify
5. Edit bug, change status to "closed"
6. Save and verify all transitions work

**Success Criteria:**
- All status transitions succeed
- Status badges update correctly

**Related User Story:** requirements.md "Update bug status through workflow"

#### E2E-10. e2e_bug_edit_severity_priority
**Priority:** High
**Preconditions:**
- Bug exists with medium severity/priority

**Steps:**
1. Open edit modal
2. Change severity to "critical"
3. Change priority to "urgent"
4. Save
5. Verify badges update

**Success Criteria:**
- Severity badge changes to red
- Priority badge shows "Urgent"

**Related User Story:** requirements.md "Edit bug details (severity, priority)"

#### E2E-11. e2e_bug_delete_flow
**Priority:** High
**Preconditions:**
- Bug exists

**Steps:**
1. Click menu on bug card
2. Click "Delete"
3. Confirm deletion
4. Verify bug removed from list

**Success Criteria:**
- Bug no longer visible
- Confirmation prevents accidents

**Related User Story:** requirements.md "Delete a bug"

#### E2E-12. e2e_bugs_list_sorted_by_severity
**Priority:** High
**Preconditions:**
- Feature has bugs with various severities

**Steps:**
1. Navigate to feature bugs list
2. Verify order: critical bugs first, then high, medium, low

**Success Criteria:**
- Critical bugs always at top
- Order is consistent

**Related User Story:** requirements.md "BugsList sorted by severity then priority"

#### E2E-13. e2e_bugs_empty_state
**Priority:** Medium
**Preconditions:**
- Feature has no bugs

**Steps:**
1. Navigate to feature detail
2. Locate Bugs section
3. Verify empty state message

**Success Criteria:**
- User understands there are no bugs
- "Report Bug" button visible

**Related User Story:** requirements.md "BugsList component"

#### E2E-14. e2e_bug_wont_fix_status
**Priority:** Medium
**Preconditions:**
- Bug exists with status "open"

**Steps:**
1. Edit bug
2. Change status to "wont_fix"
3. Save
4. Verify status badge shows "Won't Fix"

**Success Criteria:**
- Status properly displayed
- Bug remains visible in list

**Related User Story:** requirements.md "Status enum includes wont_fix"

---

### Feature Metrics E2E (4 tests)

#### E2E-15. e2e_feature_metrics_badge_display
**Priority:** Critical
**Preconditions:**
- Feature has tasks and tests with various statuses

**Steps:**
1. Navigate to features kanban/list
2. Locate feature card
3. Verify FeatureMetricsBadge is visible in footer
4. Verify format "X% | Y/Z"

**Success Criteria:**
- Badge shows task completion %
- Badge shows test pass/total

**Related User Story:** requirements.md "View feature metrics badge on card"

#### E2E-16. e2e_feature_metrics_detail_display
**Priority:** Critical
**Preconditions:**
- Feature has tasks, tests, and bugs

**Steps:**
1. Click on feature card to open detail
2. Verify FeatureMetricsDetail component visible
3. Verify task progress bar and percentage
4. Verify test breakdown (passed/failed/pending)
5. Verify bug counts by severity

**Success Criteria:**
- All metrics accurately calculated
- Visual representation clear

**Related User Story:** requirements.md "View feature metrics in detail"

#### E2E-17. e2e_feature_metrics_update_on_test_status_change
**Priority:** High
**Preconditions:**
- Feature has tests

**Steps:**
1. Note current test pass rate
2. Change a test from "pending" to "passed"
3. Verify metrics badge updates
4. Verify detail view updates

**Success Criteria:**
- Metrics reflect new test status immediately

**Related User Story:** requirements.md "Test pass rate per feature"

#### E2E-18. e2e_feature_metrics_update_on_task_completion
**Priority:** High
**Preconditions:**
- Feature has tasks

**Steps:**
1. Note current task completion %
2. Mark a task as "done"
3. Verify metrics badge updates

**Success Criteria:**
- Task completion % increases

**Related User Story:** requirements.md "Task completion percentage per feature"

---

### Project Dashboard E2E (4 tests)

#### E2E-19. e2e_project_tests_summary_card
**Priority:** Critical
**Preconditions:**
- Project has features with tests

**Steps:**
1. Navigate to project overview
2. Locate ProjectTestsSummaryCard
3. Verify total, passed, failed, pending counts
4. Verify pass rate calculation

**Success Criteria:**
- Counts aggregate across all features
- Card follows existing dashboard style

**Related User Story:** requirements.md "View project-level metrics dashboard"

#### E2E-20. e2e_project_bugs_severity_card
**Priority:** Critical
**Preconditions:**
- Project has features with bugs

**Steps:**
1. Navigate to project overview
2. Locate ProjectBugsSeverityCard
3. Verify bugs grouped by severity
4. Verify total open bugs count

**Success Criteria:**
- Severity grouping is accurate
- Open bugs count excludes resolved/closed

**Related User Story:** requirements.md "Aggregated test summary card on ProjectOverview"

#### E2E-21. e2e_project_health_indicator
**Priority:** High
**Preconditions:**
- Project has various metrics

**Steps:**
1. Navigate to project overview
2. Locate health indicator card
3. Verify status (healthy/warning/critical)
4. Verify factors shown (completion, pass rate, critical bugs)

**Success Criteria:**
- Health status reflects actual project state
- Visual indicator is clear

**Related User Story:** requirements.md "Overall project health indicator"

#### E2E-22. e2e_dashboard_layout_with_new_cards
**Priority:** Medium
**Preconditions:**
- Project exists

**Steps:**
1. Navigate to project overview
2. Verify dashboard has 4-5 cards
3. Verify responsive layout on different screen sizes

**Success Criteria:**
- New cards integrate with existing layout
- No layout breaks on mobile

**Related User Story:** requirements.md "Maintain existing card grid layout"

---

## Test Dependencies

### Execution Order Requirements

1. **Database Layer** tests must pass before Hook layer tests
   - Tables must exist before hooks can query them

2. **Hook Layer** tests must pass before UI Component tests
   - Hooks must work correctly for components to function

3. **UI Component** tests must pass before E2E tests
   - Components must render correctly for user flows to work

### Specific Dependencies

- `test_tests_table_creation` -> all other tests table tests
- `test_bugs_table_creation` -> all other bugs table tests
- `test_useTests_*` -> `test_TestsList_*`, `test_TestCard_*`
- `test_useBugs_*` -> `test_BugsList_*`, `test_BugCard_*`
- `test_FeatureMetricsBadge_*` -> `E2E-15`, `E2E-17`, `E2E-18`
- `test_ProjectTestsSummaryCard_*` -> `E2E-19`
- `test_ProjectBugsSeverityCard_*` -> `E2E-20`

---

## Test Data Requirements

### Test Database Seeds

```sql
-- Test user
INSERT INTO profiles (id, email, name) VALUES
  ('user-test-1', 'test@example.com', 'Test User');

-- Test project
INSERT INTO projects (id, name, owner_id) VALUES
  ('project-test-1', 'Test Project', 'user-test-1');

-- Test features
INSERT INTO features (id, project_id, name, phase) VALUES
  ('feature-test-1', 'project-test-1', 'Feature With Data', 'implement'),
  ('feature-test-empty', 'project-test-1', 'Empty Feature', 'raw-idea');

-- Test tasks for feature
INSERT INTO tasks (id, sprint_id, title, status) VALUES
  ('task-test-1', 'sprint-test-1', 'Task 1', 'done'),
  ('task-test-2', 'sprint-test-1', 'Task 2', 'in_progress'),
  ('task-test-3', 'sprint-test-1', 'Task 3', 'todo');
```

### Mock Data for Unit Tests

```typescript
// Test fixtures for tests
export const mockTests: Test[] = [
  { id: 't1', feature_id: 'f1', name: 'Test 1', status: 'pending', description: null },
  { id: 't2', feature_id: 'f1', name: 'Test 2', status: 'passed', description: 'Desc' },
  { id: 't3', feature_id: 'f1', name: 'Test 3', status: 'failed', description: null },
];

// Test fixtures for bugs
export const mockBugs: Bug[] = [
  { id: 'b1', feature_id: 'f1', title: 'Bug 1', severity: 'critical', priority: 'urgent', status: 'open', task_id: null },
  { id: 'b2', feature_id: 'f1', title: 'Bug 2', severity: 'high', priority: 'high', status: 'in_progress', task_id: 'task-1' },
  { id: 'b3', feature_id: 'f1', title: 'Bug 3', severity: 'medium', priority: 'medium', status: 'resolved', task_id: null },
];
```

### E2E Test Fixtures

```typescript
// e2e/fixtures/tests.ts
export const TEST_STATUSES: TestStatus[] = ['pending', 'passed', 'failed'];

export function generateTestData(): TestData {
  const timestamp = Date.now();
  return {
    name: `E2E Test ${timestamp}`,
    description: `Test created at ${new Date(timestamp).toISOString()}`,
    status: 'pending',
  };
}

// e2e/fixtures/bugs.ts
export const BUG_SEVERITIES: BugSeverity[] = ['critical', 'high', 'medium', 'low'];
export const BUG_PRIORITIES: BugPriority[] = ['urgent', 'high', 'medium', 'low'];

export function generateBugData(): BugData {
  const timestamp = Date.now();
  return {
    title: `E2E Bug ${timestamp}`,
    description: `Bug reported at ${new Date(timestamp).toISOString()}`,
    severity: 'high',
    priority: 'medium',
    status: 'open',
  };
}
```

---

## Accessibility Tests

### Keyboard Navigation (4 tests)

#### A11Y-1. test_tests_list_keyboard_navigation
**Priority:** Medium
**Given:** TestsList component rendered with tests
**When:** User navigates using Tab key
**Then:**
- Focus moves through test cards
- Each card's actions are reachable via keyboard

#### A11Y-2. test_create_test_modal_keyboard_accessible
**Priority:** Medium
**Given:** CreateTestModal is open
**When:** User uses Tab/Enter/Escape
**Then:**
- All form fields reachable via Tab
- Enter submits form
- Escape closes modal

#### A11Y-3. test_bug_card_screen_reader_labels
**Priority:** Low
**Given:** BugCard rendered
**When:** Screen reader reads card
**Then:**
- Title is read
- Severity is announced (e.g., "Severity: Critical")
- Priority is announced
- Status is announced

#### A11Y-4. test_metrics_badges_have_aria_labels
**Priority:** Low
**Given:** FeatureMetricsBadge rendered
**When:** Screen reader reads badge
**Then:**
- Full context provided (e.g., "80% tasks complete, 5 of 6 tests passed")

---

## Out of Scope

Tests explicitly NOT included in this plan:

- **Performance/load testing**: Test pass rate calculation with 1000+ tests (requires dedicated sprint)
- **Test automation execution**: Running actual test code from within the app
- **Notification testing**: Email/push notifications for test failures or bugs
- **Historical trends**: Charts showing metrics over time
- **Import/export testing**: CSV/JSON export of tests or bugs
- **Bulk operations**: Multi-select and bulk status change
- **Test attachments**: Screenshot or file uploads for tests
- **Bug comments**: Activity history on bugs
- **Kanban views for tests/bugs**: Only list views in scope
- **Filtering/search**: Advanced filtering within tests/bugs lists
- **Cross-browser compatibility**: Covered by general E2E suite

---

## Test Implementation Notes

### File Structure

```
/e2e
  /fixtures
    tests.ts          # Test data generators
    bugs.ts           # Bug data generators
  /tests              # New folder for tests E2E
    tests-crud.spec.ts
  /bugs               # New folder for bugs E2E
    bugs-crud.spec.ts
  /metrics            # New folder for metrics E2E
    feature-metrics.spec.ts
    project-metrics.spec.ts

/__tests__            # Unit tests
  /hooks
    useTests.test.ts
    useBugs.test.ts
    useFeatureMetrics.test.ts
  /components
    TestsList.test.tsx
    TestCard.test.tsx
    BugsList.test.tsx
    BugCard.test.tsx
    FeatureMetricsBadge.test.tsx
    FeatureMetricsDetail.test.tsx
    ProjectTestsSummaryCard.test.tsx
    ProjectBugsSeverityCard.test.tsx
```

### Testing Libraries

- **Unit Tests**: Vitest + React Testing Library
- **E2E Tests**: Playwright
- **Mocking**: MSW (Mock Service Worker) for API mocking
- **Database Tests**: Supabase test client with test schema

### CI/CD Integration

Tests should be run in this order:
1. Database schema validation (migrations)
2. Unit tests (hooks, utilities)
3. Component tests (React Testing Library)
4. E2E tests (Playwright)

All Critical and High priority tests must pass for deployment.
