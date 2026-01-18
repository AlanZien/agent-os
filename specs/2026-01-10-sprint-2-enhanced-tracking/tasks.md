# Task Breakdown: Sprint 2 - Enhanced Tracking

## Overview

**Feature**: Test Management, Bug Tracking, Feature Metrics, Project Dashboard Metrics
**Total Tasks**: 47 tasks across 8 task groups
**Total Story Points**: 89
**Track**: COMPLEX (Score: 45)

### Summary by Layer
| Layer | Task Groups | Tasks | Story Points |
|-------|-------------|-------|--------------|
| Database | 2 | 10 | 16 |
| Types | 2 | 6 | 8 |
| Hooks | 2 | 10 | 16 |
| UI Components | 4 | 17 | 37 |
| Integration | 1 | 4 | 12 |
| **Total** | **8** | **47** | **89** |

---

## Task List

---

### Database Layer

#### Task Group 1: Tests Table and Migrations
**Dependencies:** None
**Parallel:** Can run in parallel with Task Group 2

- [ ] 1.0 Complete Tests database layer (8 SP)
  - [ ] 1.1 Write database tests for tests table (2 SP)
    - Implement tests 1-9 from test-plan.md "Tests Table"
    - Test table creation with required fields
    - Test feature_id foreign key constraint
    - Test status enum constraint (pending, passed, failed only)
    - Test name required constraint
    - Test cascade delete on feature
    - Test updated_at auto-update
    - Test RLS policies (authenticated, unauthenticated, other user)
    - Expected: 9 tests covering all database constraints and RLS
  - [ ] 1.2 Create tests table migration (3 SP)
    - File: `supabase/migrations/00010_create_tests_table.sql`
    - Fields: id (UUID), feature_id (FK required), name (TEXT NOT NULL), description (TEXT), status (test_status enum), created_at, updated_at
    - Create test_status enum: 'pending', 'passed', 'failed'
    - Add index on feature_id for query performance
    - Add trigger for updated_at auto-update
  - [ ] 1.3 Create RLS policies for tests table (2 SP)
    - Policy: authenticated users can SELECT tests via feature -> project ownership chain
    - Policy: authenticated users can INSERT/UPDATE/DELETE their own tests
    - Follow existing task RLS patterns
  - [ ] 1.4 Verify database layer tests pass (1 SP)
    - Run tests 1-9 from test-plan.md
    - Expected: 9/9 tests passing
    - Verify migration runs successfully

**Acceptance Criteria:**
- All 9 database tests pass
- Migration applies without errors
- RLS policies enforce proper access control
- Cascade delete works when feature is deleted

---

#### Task Group 2: Bugs Table and Migrations
**Dependencies:** None
**Parallel:** Can run in parallel with Task Group 1

- [x] 2.0 Complete Bugs database layer (8 SP)
  - [x] 2.1 Write database tests for bugs table (2 SP)
    - Implement tests 10-18 from test-plan.md "Bugs Table"
    - Test table creation with required fields
    - Test feature_id foreign key constraint
    - Test task_id optional foreign key (SET NULL on delete)
    - Test severity enum constraint (critical, high, medium, low)
    - Test priority enum constraint (urgent, high, medium, low)
    - Test status enum constraint (open, in_progress, resolved, closed, wont_fix)
    - Test title required constraint
    - Test cascade delete on feature
    - Expected: 9 tests covering all constraints
  - [x] 2.2 Create bugs table migration (3 SP)
    - File: `supabase/migrations/00011_create_bugs_table.sql`
    - Fields: id (UUID), feature_id (FK required), task_id (FK optional), title (TEXT NOT NULL), description (TEXT), severity (bug_severity), priority (bug_priority), status (bug_status), created_at, updated_at
    - Create bug_severity enum: 'critical', 'high', 'medium', 'low'
    - Create bug_priority enum: 'urgent', 'high', 'medium', 'low'
    - Create bug_status enum: 'open', 'in_progress', 'resolved', 'closed', 'wont_fix'
    - Add indexes on feature_id and task_id
    - task_id ON DELETE SET NULL
    - feature_id ON DELETE CASCADE
  - [x] 2.3 Create RLS policies for bugs table (2 SP)
    - Same pattern as tests table
    - Via feature -> project ownership chain
  - [x] 2.4 Verify database layer tests pass (1 SP)
    - Run tests 10-18 from test-plan.md
    - Expected: 9/9 tests passing

**Acceptance Criteria:**
- All 9 database tests pass
- Migration applies without errors
- Enums properly constrain values
- task_id SET NULL works on task deletion

---

### Types Layer

#### Task Group 3: Test Types Definition
**Dependencies:** Task Groups 1 & 2 (database must exist)
**Parallel:** Can run in parallel with Task Group 4

- [x] 3.0 Complete Test types (4 SP)
  - [x] 3.1 Create types/test.ts (2 SP)
    - File: `types/test.ts`
    - Follow `types/task.ts` pattern exactly
    - Define `TEST_STATUSES = ['pending', 'passed', 'failed'] as const`
    - Define `TestStatus` type from const array
    - Define `Test` interface: id, feature_id, name, description, status, created_at, updated_at
    - Define `CreateTestInput` interface: feature_id (required), name (required), description?, status?
    - Define `UpdateTestInput` interface: name?, description?, status?
  - [x] 3.2 Create TEST_STATUS_CONFIG (1 SP)
    - pending: { label: 'Pending', color: 'text-muted-foreground', bgColor: 'bg-muted/50' }
    - passed: { label: 'Passed', color: 'text-chart-1', bgColor: 'bg-chart-1/10' }
    - failed: { label: 'Failed', color: 'text-destructive', bgColor: 'bg-destructive/10' }
  - [x] 3.3 Create TEST_QUERY_KEYS (1 SP)
    - all: ['tests'] as const
    - byFeature: (featureId: string) => ['tests', 'feature', featureId] as const
    - detail: (testId: string) => ['tests', 'detail', testId] as const

**Acceptance Criteria:**
- TypeScript compiles without errors
- Types match database schema
- Config matches design system colors
- Query keys follow existing pattern

---

#### Task Group 4: Bug Types Definition
**Dependencies:** Task Groups 1 & 2 (database must exist)
**Parallel:** Can run in parallel with Task Group 3

- [x] 4.0 Complete Bug types (4 SP)
  - [x] 4.1 Create types/bug.ts (2 SP)
    - File: `types/bug.ts`
    - Follow `types/task.ts` pattern exactly
    - Define `BUG_SEVERITIES = ['critical', 'high', 'medium', 'low'] as const`
    - Define `BUG_PRIORITIES = ['urgent', 'high', 'medium', 'low'] as const`
    - Define `BUG_STATUSES = ['open', 'in_progress', 'resolved', 'closed', 'wont_fix'] as const`
    - Define `BugSeverity`, `BugPriority`, `BugStatus` types
    - Define `Bug` interface with all fields including optional task_id
    - Define `CreateBugInput`, `UpdateBugInput` interfaces
  - [x] 4.2 Create BUG_SEVERITY_CONFIG (0.5 SP)
    - critical: { label: 'Critical', color: 'text-destructive', bgColor: 'bg-destructive/10', icon: 'AlertCircle' }
    - high: { label: 'High', color: 'text-chart-3', bgColor: 'bg-chart-3/10', icon: 'AlertTriangle' }
    - medium: { label: 'Medium', color: 'text-chart-2', bgColor: 'bg-chart-2/10', icon: 'Info' }
    - low: { label: 'Low', color: 'text-muted-foreground', bgColor: 'bg-muted/50', icon: 'MinusCircle' }
  - [x] 4.3 Create BUG_PRIORITY_CONFIG and BUG_STATUS_CONFIG (0.5 SP)
    - Priority: urgent, high, medium, low with appropriate styling
    - Status: open, in_progress, resolved, closed, wont_fix with appropriate styling
  - [x] 4.4 Create BUG_QUERY_KEYS (1 SP)
    - all: ['bugs'] as const
    - byFeature: (featureId: string) => ['bugs', 'feature', featureId] as const
    - detail: (bugId: string) => ['bugs', 'detail', bugId] as const

**Acceptance Criteria:**
- TypeScript compiles without errors
- All enums have config objects
- Icons defined for severity levels
- Query keys follow existing pattern

---

### Hooks Layer

#### Task Group 5: useTests Hook
**Dependencies:** Task Groups 1, 3 (database + types)
**Parallel:** Can run in parallel with Task Group 6

- [x] 5.0 Complete useTests hook (8 SP)
  - [x] 5.1 Write useTests hook unit tests (3 SP)
    - Implement tests 19-30 from test-plan.md "useTests Hook"
    - Test useTests fetches by feature_id
    - Test useTests returns empty array when no tests
    - Test loading and error states
    - Test useTest fetches single test by id
    - Test useCreateTest mutation with cache invalidation
    - Test useCreateTest validation error handling
    - Test useUpdateTest mutation
    - Test useDeleteTest mutation
    - Test useUpdateTestStatus with optimistic update
    - Test useUpdateTestStatus rollback on error
    - Test query keys structure
    - Expected: 12 tests
  - [x] 5.2 Create hooks/useTests.ts (3 SP)
    - File: `hooks/useTests.ts`
    - Follow `hooks/useTasks.ts` pattern exactly
    - Implement `useTests(featureId: string)` - fetch tests by feature
    - Implement `useTest(testId: string)` - fetch single test
    - Implement `useCreateTest()` mutation with cache invalidation
    - Implement `useUpdateTest()` mutation
    - Implement `useDeleteTest()` mutation
    - Configure staleTime: 30 * 1000
    - Enable query only when featureId is truthy
  - [x] 5.3 Implement useUpdateTestStatus with optimistic updates (2 SP)
    - Optimistic update: immediately show new status
    - Rollback: restore previous status on error
    - Cache invalidation on settle
    - Follow useUpdateTaskStatus pattern from useTasks.ts
  - [x] 5.4 Verify hook tests pass (0 SP)
    - Run tests 19-30 from test-plan.md
    - Expected: 12/12 tests passing
    - **Result: 14/14 tests passing**

**Acceptance Criteria:**
- All 12 hook tests pass
- CRUD operations work correctly
- Optimistic updates provide instant feedback
- Cache invalidation keeps UI in sync

---

#### Task Group 6: useBugs Hook
**Dependencies:** Task Groups 2, 4 (database + types)
**Parallel:** Can run in parallel with Task Group 5

- [x] 6.0 Complete useBugs hook (8 SP)
  - [x] 6.1 Write useBugs hook unit tests (3 SP)
    - Implement tests 31-42 from test-plan.md "useBugs Hook"
    - Test useBugs fetches by feature_id
    - Test useBugs returns empty array when no bugs
    - Test loading and error states
    - Test useBug fetches single bug by id
    - Test useCreateBug mutation (with and without task_id)
    - Test useUpdateBug mutation
    - Test useDeleteBug mutation
    - Test useUpdateBugStatus with optimistic update
    - Test status workflow transitions
    - Test query keys structure
    - Expected: 12 tests
  - [x] 6.2 Create hooks/useBugs.ts (3 SP)
    - File: `hooks/useBugs.ts`
    - Follow `hooks/useTasks.ts` pattern exactly
    - Implement `useBugs(featureId: string)` - fetch bugs by feature
    - Implement `useBug(bugId: string)` - fetch single bug
    - Implement `useCreateBug()` mutation
    - Implement `useUpdateBug()` mutation
    - Implement `useDeleteBug()` mutation
    - Support optional task_id in create/update
  - [x] 6.3 Implement useUpdateBugStatus with optimistic updates (2 SP)
    - Same pattern as useUpdateTestStatus
    - Support all 5 status values
  - [x] 6.4 Verify hook tests pass (0 SP)
    - Run tests 31-42 from test-plan.md
    - Expected: 12/12 tests passing
    - **Result: 17/17 tests passing**

**Acceptance Criteria:**
- All 12 hook tests pass
- CRUD operations work correctly
- Optional task_id linking works
- Status workflow transitions work

---

### UI Components Layer

#### Task Group 7: Test Management UI Components
**Dependencies:** Task Groups 3, 5 (types + hooks)
**Parallel:** Can run in parallel with Task Group 8

- [x] 7.0 Complete Test Management UI (18 SP)
  - [x] 7.1 Write TestsList component tests (1 SP)
    - Implement tests 43-46 from test-plan.md "TestsList Component"
    - Test renders tests for feature
    - Test empty state
    - Test loading skeleton
    - Test error state
    - Expected: 4 tests
  - [x] 7.2 Create TestsList component (2 SP)
    - File: `components/features/test-management/TestsList.tsx`
    - Props: featureId, onTestClick?
    - Use useTests(featureId) hook
    - Render TestCard for each test
    - Show empty state with "Add Test" button
    - Show loading skeleton (follow SprintCardSkeleton pattern)
    - Show error state with retry option
  - [x] 7.3 Write TestCard component tests (1 SP)
    - Implement tests 47-50 from test-plan.md "TestCard Component"
    - Test renders test details (name, description, status)
    - Test status badge colors (pending=gray, passed=green, failed=red)
    - Test dropdown menu actions (Edit, Delete)
    - Test quick status toggle
    - Expected: 4 tests
  - [x] 7.4 Create TestCard component (2 SP)
    - File: `components/features/test-management/TestCard.tsx`
    - Props: test, onEdit?, onDelete?, onStatusChange?
    - Display name, description preview (line-clamp-2)
    - Display status badge with TEST_STATUS_CONFIG colors
    - Dropdown menu with Edit and Delete actions
    - Optional quick status toggle button
  - [x] 7.5 Write CreateTestModal component tests (2 SP)
    - Implement tests 51-56 from test-plan.md "CreateTestModal Component"
    - Test form fields render (name, description, status)
    - Test name validation (required)
    - Test successful submission
    - Test error toast on failure
    - Test form reset on open
    - Test cancel closes without saving
    - Expected: 6 tests
  - [x] 7.6 Create CreateTestModal component (3 SP)
    - File: `components/features/test-management/CreateTestModal.tsx`
    - Follow CreateTaskModal.tsx pattern exactly
    - Props: isOpen, onClose, featureId
    - Form fields: name (required), description (optional), status (select with 3 options)
    - Use react-hook-form with Zod validation
    - Use useCreateTest mutation
    - Toast on success/error
    - Reset form on open/close
  - [x] 7.7 Write EditTestModal component tests (1 SP)
    - Implement tests 57-60 from test-plan.md "EditTestModal Component"
    - Test pre-populates form with test data
    - Test successful update
    - Test validation on empty name
    - Test pending/loading state
    - Expected: 4 tests
  - [x] 7.8 Create EditTestModal component (3 SP)
    - File: `components/features/test-management/EditTestModal.tsx`
    - Follow EditTaskModal.tsx pattern exactly
    - Props: isOpen, onClose, test
    - Pre-populate form with test data
    - Use useUpdateTest mutation
    - Toast on success/error
    - Show loading state during save
  - [x] 7.9 Create DeleteTestConfirmation component (1 SP)
    - File: `components/features/test-management/DeleteTestConfirmation.tsx`
    - Follow DeleteTaskConfirmation pattern
    - Confirm before delete
    - Use useDeleteTest mutation
  - [x] 7.10 Create test-management index.ts (0.5 SP)
    - Export all components
  - [x] 7.11 Verify Test UI component tests pass (0.5 SP)
    - Run tests 43-60 from test-plan.md
    - Expected: 18/18 tests passing

**Acceptance Criteria:**
- All 18 UI component tests pass
- Components follow existing patterns
- Forms validate correctly
- Modals work as expected
- Toast notifications appear on success/error

---

#### Task Group 8: Bug Management UI Components
**Dependencies:** Task Groups 4, 6 (types + hooks)
**Parallel:** Can run in parallel with Task Group 7

- [x] 8.0 Complete Bug Management UI (19 SP)
  - [x] 8.1 Write BugsList component tests (1 SP)
    - Implement tests 61-64 from test-plan.md "BugsList Component"
    - Test renders bugs for feature
    - Test sorting by severity then priority (critical first)
    - Test empty state
    - Test loading skeleton
    - Expected: 4 tests
  - [x] 8.2 Create BugsList component (3 SP)
    - File: `components/features/bug-management/BugsList.tsx`
    - Props: featureId, onBugClick?
    - Use useBugs(featureId) hook
    - Sort bugs: critical > high > medium > low, then by priority
    - Render BugCard for each bug
    - Show empty state with "Report Bug" button
    - Show loading skeleton
  - [x] 8.3 Write BugCard component tests (2 SP)
    - Implement tests 65-70 from test-plan.md "BugCard Component"
    - Test renders bug details (title, severity, priority, status)
    - Test severity badge colors (critical=red, high=orange, medium=amber, low=gray)
    - Test shows linked task reference when task_id exists
    - Test hides task reference when task_id is null
    - Test dropdown menu actions
    - Test priority badge display
    - Expected: 6 tests
  - [x] 8.4 Create BugCard component (3 SP)
    - File: `components/features/bug-management/BugCard.tsx`
    - Props: bug, onEdit?, onDelete?, linkedTask?
    - Display title, description preview
    - Display severity badge with BUG_SEVERITY_CONFIG
    - Display priority badge with BUG_PRIORITY_CONFIG
    - Display status badge with BUG_STATUS_CONFIG
    - Show linked task reference if task_id exists (needs task fetch or pass as prop)
    - Dropdown menu with Edit and Delete actions
  - [x] 8.5 Write CreateBugModal component tests (2 SP)
    - Implement tests 71-76 from test-plan.md "CreateBugModal Component"
    - Test all form fields render
    - Test title validation (required)
    - Test successful submission
    - Test optional task_id select shows available tasks
    - Test status defaults to 'open'
    - Test error toast on failure
    - Expected: 6 tests
  - [x] 8.6 Create CreateBugModal component (3 SP)
    - File: `components/features/bug-management/CreateBugModal.tsx`
    - Follow CreateTaskModal.tsx pattern
    - Props: isOpen, onClose, featureId, availableTasks?
    - Form fields: title (required), description, severity (select), priority (select), status (select), task_id (optional select)
    - Default status to 'open'
    - Use react-hook-form with Zod validation
    - Use useCreateBug mutation
    - Toast on success/error
  - [x] 8.7 Write EditBugModal component tests (1 SP)
    - Implement tests 77-80 from test-plan.md "EditBugModal Component"
    - Test pre-populates all fields
    - Test successful update
    - Test can link to fix task
    - Test can remove task link (set to None)
    - Expected: 4 tests
  - [x] 8.8 Create EditBugModal component (3 SP)
    - File: `components/features/bug-management/EditBugModal.tsx`
    - Follow EditTaskModal.tsx pattern
    - Props: isOpen, onClose, bug, availableTasks?
    - All fields editable including task_id (can set to null with "None" option)
    - Use useUpdateBug mutation
    - Toast on success/error
  - [x] 8.9 Create DeleteBugConfirmation component (0.5 SP)
    - Follow DeleteTaskConfirmation pattern
  - [x] 8.10 Create bug-management index.ts (0.5 SP)
    - Export all components
  - [x] 8.11 Verify Bug UI component tests pass (0 SP)
    - Run tests 61-80 from test-plan.md
    - Expected: 20/20 tests passing

**Acceptance Criteria:**
- All 20 UI component tests pass
- Sorting by severity/priority works
- All form fields work correctly
- Task linking/unlinking works
- Status workflow respected

---

### Feature Metrics Layer

#### Task Group 9: Feature Metrics Components
**Dependencies:** Task Groups 5, 6 (useTests, useBugs hooks)

- [ ] 9.0 Complete Feature Metrics components (12 SP)
  - [ ] 9.1 Create useFeatureMetrics hook (2 SP)
    - File: `hooks/useFeatureMetrics.ts`
    - Props: featureId
    - Fetch tasks (via existing hook), tests, bugs for feature
    - Calculate task completion %: (done / total) * 100
    - Calculate test pass rate: (passed / total) * 100
    - Calculate bug counts by severity
    - Return: { taskCompletion, testPassRate, passedTests, totalTests, bugsBySeverity, isLoading }
  - [ ] 9.2 Write FeatureMetricsBadge component tests (1 SP)
    - Implement tests 81-84 from test-plan.md "FeatureMetricsBadge Component"
    - Test displays task completion percentage
    - Test displays test pass rate (X/Y format)
    - Test combined format "80% | 5/6"
    - Test muted styling when no data
    - Expected: 4 tests
  - [ ] 9.3 Create FeatureMetricsBadge component (2 SP)
    - File: `components/features/feature-management/FeatureMetricsBadge.tsx`
    - Props: featureId OR { taskCompletion, passedTests, totalTests }
    - Format: "80% | 5/6" with checkmark and flask icons
    - Muted styling when no tasks/tests exist (show "- | -")
    - Compact design for card footer
  - [ ] 9.4 Write FeatureMetricsDetail component tests (1 SP)
    - Implement tests 85-88 from test-plan.md "FeatureMetricsDetail Component"
    - Test shows task progress bar with count and percentage
    - Test shows test breakdown (passed/failed/pending)
    - Test shows bug count by severity
    - Test handles empty state
    - Expected: 4 tests
  - [ ] 9.5 Create FeatureMetricsDetail component (3 SP)
    - File: `components/features/feature-management/FeatureMetricsDetail.tsx`
    - Props: featureId
    - Task progress: progress bar + "7/10 tasks (70%)"
    - Test breakdown: progress bar + "6 passed, 2 failed, 2 pending"
    - Bug counts: icon + count for each severity level
    - Handle empty states gracefully
  - [ ] 9.6 Integrate FeatureMetricsBadge into FeatureCard (2 SP)
    - Modify existing FeatureCard component
    - Add FeatureMetricsBadge in footer area
    - Only show when feature has tasks or tests
  - [ ] 9.7 Integrate FeatureMetricsDetail into FeatureDetailPanel (1 SP)
    - Modify existing FeatureDetailPanel component
    - Add FeatureMetricsDetail section
    - Show after description, before actions
  - [ ] 9.8 Verify Feature Metrics tests pass (0 SP)
    - Run tests 81-88 from test-plan.md
    - Expected: 8/8 tests passing

**Acceptance Criteria:**
- All 8 metrics tests pass
- Badge displays correctly on feature cards
- Detail view shows comprehensive breakdown
- Empty states handled gracefully

---

### Project Dashboard Layer

#### Task Group 10: Project Dashboard Metrics
**Dependencies:** Task Groups 5, 6, 9 (hooks + feature metrics)

- [ ] 10.0 Complete Project Dashboard integration (12 SP)
  - [ ] 10.1 Create useProjectMetrics hook (2 SP)
    - File: `hooks/useProjectMetrics.ts`
    - Props: projectId
    - Aggregate tests across all features: total, passed, failed, pending
    - Aggregate bugs across all features: count by severity, total open
    - Calculate overall pass rate
    - Calculate project health status (healthy/warning/critical)
  - [ ] 10.2 Write ProjectTestsSummaryCard tests (1 SP)
    - Implement tests 89-91 from test-plan.md "ProjectTestsSummaryCard"
    - Test displays test counts (total, passed, failed, pending, pass rate)
    - Test empty state
    - Test loading state
    - Expected: 3 tests
  - [ ] 10.3 Create ProjectTestsSummaryCard component (2 SP)
    - File: `components/features/projects/ProjectTestsSummaryCard.tsx`
    - Follow existing ProjectOverview card structure
    - Display: Total tests, Passed (green), Failed (red), Pending (gray), Pass rate %
    - Icon: Flask or TestTube icon
    - Match existing card styling
  - [ ] 10.4 Write ProjectBugsSeverityCard tests (1 SP)
    - Implement tests 92-94 from test-plan.md "ProjectBugsSeverityCard"
    - Test groups bugs by severity
    - Test shows total open bugs count
    - Test empty state
    - Expected: 3 tests
  - [ ] 10.5 Create ProjectBugsSeverityCard component (2 SP)
    - File: `components/features/projects/ProjectBugsSeverityCard.tsx`
    - Display: Bugs grouped by severity with counts
    - Show total open bugs prominently
    - Use severity colors (red, orange, amber, gray)
    - Icon: Bug icon
  - [ ] 10.6 Write ProjectHealthIndicatorCard tests (1 SP)
    - Implement tests 95-96 from test-plan.md "ProjectHealthIndicatorCard"
    - Test healthy status (>80% completion, >90% pass rate, 0 critical bugs)
    - Test critical status (3+ critical bugs OR <50% pass rate)
    - Expected: 2 tests
  - [ ] 10.7 Create ProjectHealthIndicatorCard component (2 SP)
    - File: `components/features/projects/ProjectHealthIndicatorCard.tsx`
    - Calculate health: healthy (green), warning (amber), critical (red)
    - Logic:
      - Critical: 3+ critical bugs open OR test pass rate < 50%
      - Warning: 1-2 critical bugs OR pass rate 50-89%
      - Healthy: 0 critical bugs AND pass rate >= 90%
    - Display status with icon and color
  - [ ] 10.8 Integrate new cards into ProjectOverview (1 SP)
    - Modify `components/features/projects/ProjectOverview.tsx`
    - Expand grid from 3 to 5 columns (or 2 rows)
    - Add ProjectTestsSummaryCard
    - Add ProjectBugsSeverityCard
    - Add ProjectHealthIndicatorCard
    - Maintain responsive layout
  - [ ] 10.9 Verify Project Dashboard tests pass (0 SP)
    - Run tests 89-96 from test-plan.md
    - Expected: 8/8 tests passing

**Acceptance Criteria:**
- All 8 dashboard tests pass
- New cards integrate seamlessly
- Responsive layout works on mobile
- Health indicator accurately reflects project state

---

### E2E Testing Layer

#### Task Group 11: End-to-End Tests
**Dependencies:** All previous task groups (full feature implementation)

- [x] 11.0 Complete E2E test suite (8 SP)
  - [x] 11.1 Create E2E test fixtures (1 SP)
    - File: `e2e/fixtures/tests.ts`
    - File: `e2e/fixtures/bugs.ts`
    - Test data generators with timestamps
    - Status arrays for iteration
  - [x] 11.2 Write Test CRUD E2E tests (2 SP)
    - Implement E2E tests 1-6 from test-plan.md "Test CRUD E2E"
    - File: `e2e/tests/tests-crud.spec.ts`
    - Test create flow
    - Test status update flow (optimistic update verification)
    - Test edit flow
    - Test delete flow
    - Test list display
    - Test empty state
    - Expected: 6 E2E tests
  - [x] 11.3 Write Bug CRUD E2E tests (2 SP)
    - Implement E2E tests 7-14 from test-plan.md "Bug CRUD E2E"
    - File: `e2e/bugs/bugs-crud.spec.ts`
    - Test create flow
    - Test create with task link
    - Test status workflow (open -> in_progress -> resolved -> closed)
    - Test edit severity/priority
    - Test delete flow
    - Test sorted by severity
    - Test empty state
    - Test wont_fix status
    - Expected: 8 E2E tests
  - [x] 11.4 Write Feature Metrics E2E tests (1.5 SP)
    - Implement E2E tests 15-18 from test-plan.md "Feature Metrics E2E"
    - File: `e2e/metrics/feature-metrics.spec.ts`
    - Test badge display on feature cards
    - Test detail display in feature panel
    - Test metrics update on test status change
    - Test metrics update on task completion
    - Expected: 4 E2E tests
  - [x] 11.5 Write Project Dashboard E2E tests (1.5 SP)
    - Implement E2E tests 19-22 from test-plan.md "Project Dashboard E2E"
    - File: `e2e/metrics/project-metrics.spec.ts`
    - Test tests summary card
    - Test bugs severity card
    - Test health indicator
    - Test dashboard layout with new cards
    - Expected: 4 E2E tests (+ 1 integration test)
  - [ ] 11.6 Run full E2E suite and fix issues (0 SP)
    - Run all E2E tests
    - Expected: 22/22 E2E tests passing
    - Fix any integration issues discovered

**Acceptance Criteria:**
- All 22 E2E tests pass
- Tests cover full user workflows
- Optimistic updates verified
- Dashboard integration verified

---

### Final Validation

#### Task Group 12: Final Test Validation
**Dependencies:** All previous task groups

- [ ] 12.0 Validate all tests from test-plan.md (3 SP)
  - [ ] 12.1 Run complete test validation (1 SP)
    - Run ALL tests from test-plan.md across all layers
    - Database: 18 tests
    - Hooks: 24 tests
    - UI Components: 34 tests
    - E2E: 22 tests
    - Expected: 98/98 tests passing (or as specified in test-plan.md)
  - [ ] 12.2 Review test coverage report (1 SP)
    - Verify all Critical priority tests implemented (100% required)
    - Verify all High priority tests implemented (100% required)
    - Check Medium priority tests (80% target)
    - Document any Low priority tests deferred
  - [ ] 12.3 Address any failing tests (0.5 SP)
    - Debug and fix any tests that fail
    - Ensure all Given-When-Then assertions pass
    - Do NOT skip or comment out failing tests
  - [ ] 12.4 Generate final test report (0.5 SP)
    - Document test counts: Planned vs Implemented vs Passing
    - List any Medium/Low priority tests deferred
    - Confirm feature is ready for deployment

**Acceptance Criteria:**
- 100% of Critical and High priority tests pass (76 tests)
- At least 80% of Medium priority tests pass (16 of 20)
- Test report confirms full test coverage
- Zero failing tests remain

---

## Execution Order

### Phase 1: Foundation (Parallelizable)
1. **Task Group 1**: Tests Table (Database) - 8 SP
2. **Task Group 2**: Bugs Table (Database) - 8 SP

### Phase 2: Type Definitions (Parallelizable, after Phase 1)
3. **Task Group 3**: Test Types - 4 SP
4. **Task Group 4**: Bug Types - 4 SP

### Phase 3: Hooks (Parallelizable, after Phase 2)
5. **Task Group 5**: useTests Hook - 8 SP
6. **Task Group 6**: useBugs Hook - 8 SP

### Phase 4: UI Components (Parallelizable, after Phase 3)
7. **Task Group 7**: Test Management UI - 18 SP
8. **Task Group 8**: Bug Management UI - 19 SP

### Phase 5: Metrics & Integration (Sequential, after Phase 4)
9. **Task Group 9**: Feature Metrics - 12 SP
10. **Task Group 10**: Project Dashboard - 12 SP

### Phase 6: E2E & Validation (Sequential, after Phase 5)
11. **Task Group 11**: E2E Tests - 8 SP
12. **Task Group 12**: Final Validation - 3 SP

---

## File Summary

### New Files to Create

**Database Migrations:**
- `supabase/migrations/00010_create_tests_table.sql`
- `supabase/migrations/00011_create_bugs_table.sql`

**Types:**
- `types/test.ts`
- `types/bug.ts`

**Hooks:**
- `hooks/useTests.ts`
- `hooks/useBugs.ts`
- `hooks/useFeatureMetrics.ts`
- `hooks/useProjectMetrics.ts`

**Test Management Components:**
- `components/features/test-management/TestsList.tsx`
- `components/features/test-management/TestCard.tsx`
- `components/features/test-management/CreateTestModal.tsx`
- `components/features/test-management/EditTestModal.tsx`
- `components/features/test-management/DeleteTestConfirmation.tsx`
- `components/features/test-management/index.ts`

**Bug Management Components:**
- `components/features/bug-management/BugsList.tsx`
- `components/features/bug-management/BugCard.tsx`
- `components/features/bug-management/CreateBugModal.tsx`
- `components/features/bug-management/EditBugModal.tsx`
- `components/features/bug-management/DeleteBugConfirmation.tsx`
- `components/features/bug-management/index.ts`

**Feature Metrics Components:**
- `components/features/feature-management/FeatureMetricsBadge.tsx`
- `components/features/feature-management/FeatureMetricsDetail.tsx`

**Project Dashboard Components:**
- `components/features/projects/ProjectTestsSummaryCard.tsx`
- `components/features/projects/ProjectBugsSeverityCard.tsx`
- `components/features/projects/ProjectHealthIndicatorCard.tsx`

**E2E Test Files:**
- `e2e/fixtures/tests.ts`
- `e2e/fixtures/bugs.ts`
- `e2e/tests/tests-crud.spec.ts`
- `e2e/bugs/bugs-crud.spec.ts`
- `e2e/metrics/feature-metrics.spec.ts`
- `e2e/metrics/project-metrics.spec.ts`

**Unit Test Files:**
- `__tests__/hooks/useTests.test.ts`
- `__tests__/hooks/useBugs.test.ts`
- `__tests__/components/TestsList.test.tsx`
- `__tests__/components/TestCard.test.tsx`
- `__tests__/components/BugsList.test.tsx`
- `__tests__/components/BugCard.test.tsx`
- `__tests__/components/FeatureMetricsBadge.test.tsx`
- `__tests__/components/FeatureMetricsDetail.test.tsx`
- `__tests__/components/ProjectTestsSummaryCard.test.tsx`
- `__tests__/components/ProjectBugsSeverityCard.test.tsx`

### Existing Files to Modify

- `components/features/feature-management/FeatureCard.tsx` - Add FeatureMetricsBadge
- `components/features/feature-management/FeatureDetailPanel.tsx` - Add FeatureMetricsDetail
- `components/features/projects/ProjectOverview.tsx` - Add new dashboard cards

---

## Risk Assessment

### High Risk Items
1. **RLS Policies**: Complex ownership chain (tests -> features -> projects) may have edge cases
2. **Optimistic Updates**: Rollback logic must handle all error scenarios
3. **Dashboard Performance**: Aggregating metrics across all features may be slow for large projects

### Mitigation Strategies
1. Thorough RLS testing with different user contexts
2. Comprehensive error state testing for optimistic updates
3. Consider adding database views or functions for dashboard aggregations

---

## Definition of Done

- [ ] All database migrations applied successfully
- [ ] All TypeScript types compile without errors
- [ ] All 98 tests from test-plan.md pass (or documented exceptions)
- [ ] All components render correctly in dev environment
- [ ] Feature metrics display on feature cards
- [ ] Project dashboard shows new metrics cards
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] No console errors or warnings
- [ ] Code reviewed and approved
- [ ] Documentation updated if needed
