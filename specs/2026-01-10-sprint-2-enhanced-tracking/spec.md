# Specification: Sprint 2 - Enhanced Tracking

## Goal

Extend AgentOS-Tracker with test management, bug tracking, and feature-level metrics to provide comprehensive visibility into feature quality and project health.

## User Stories

- As a developer, I want to track tests per feature so that I can monitor test coverage and pass rates
- As a project manager, I want to log and track bugs with severity/priority so that I can prioritize fixes effectively
- As a team member, I want to see feature progress metrics at a glance so that I can quickly assess feature health

## Specific Requirements

**Tests Table and Type Definitions**
- Create `tests` table in Supabase with fields: `id`, `feature_id` (required FK), `name`, `description`, `status`, `created_at`, `updated_at`
- Status enum: `pending`, `passed`, `failed` (3 values only)
- Create `types/test.ts` following `types/task.ts` pattern with `Test`, `CreateTestInput`, `UpdateTestInput` interfaces
- Define `TEST_STATUSES` constant array and `TestStatus` type
- Create `TEST_STATUS_CONFIG` with labels and colors (pending=gray, passed=green, failed=red)
- Add RLS policies following existing task patterns via feature -> project ownership chain

**Bugs Table and Type Definitions**
- Create `bugs` table with fields: `id`, `feature_id` (required FK), `task_id` (optional FK), `title`, `description`, `severity`, `priority`, `status`, `created_at`, `updated_at`
- Severity enum: `critical`, `high`, `medium`, `low`
- Priority enum: `urgent`, `high`, `medium`, `low`
- Status enum: `open`, `in_progress`, `resolved`, `closed`, `wont_fix`
- Create `types/bug.ts` with `Bug`, `CreateBugInput`, `UpdateBugInput` interfaces
- Define `BUG_SEVERITIES`, `BUG_PRIORITIES`, `BUG_STATUSES` constant arrays
- Create config objects with labels, colors, and icons for each enum

**useTests Hook**
- Follow `useTasks.ts` hook pattern with React Query
- Implement `useTests(featureId)` to fetch tests by feature
- Implement `useTest(testId)` for single test retrieval
- Implement `useCreateTest()`, `useUpdateTest()`, `useDeleteTest()` mutations
- Implement `useUpdateTestStatus()` with optimistic updates for quick status toggles
- Define `TEST_QUERY_KEYS` for cache management

**useBugs Hook**
- Follow `useTasks.ts` hook pattern with React Query
- Implement `useBugs(featureId)` to fetch bugs by feature
- Implement `useBug(bugId)` for single bug retrieval
- Implement `useCreateBug()`, `useUpdateBug()`, `useDeleteBug()` mutations
- Implement `useUpdateBugStatus()` with optimistic updates
- Define `BUG_QUERY_KEYS` for cache management

**Test Management UI Components**
- `TestsList`: List view of tests for a feature, displays name, status badge, description preview
- `TestCard`: Individual test item with status indicator, edit/delete actions via dropdown menu
- `CreateTestModal`: Form with name (required), description (optional), status select; follows CreateTaskModal pattern
- `EditTestModal`: Pre-populated form for editing existing tests; follows EditTaskModal pattern
- All modals use Dialog, react-hook-form with Zod validation, toast notifications on success/error

**Bug Management UI Components**
- `BugsList`: List view of bugs for a feature, sorted by severity then priority
- `BugCard`: Displays title, severity badge, priority badge, status badge, optional linked task reference
- `CreateBugModal`: Form with title (required), description, severity select, priority select, status select, optional task_id select
- `EditBugModal`: Pre-populated form for editing bugs with all fields editable
- Severity badges use design system colors: critical=red, high=orange, medium=amber, low=gray

**Feature Metrics Calculation**
- Task completion %: `(tasks with status 'done' / total tasks) * 100` per feature
- Test pass rate: `(tests with status 'passed' / total tests) * 100` per feature
- Create `useFeatureMetrics(featureId)` hook that fetches tasks and tests, returns calculated metrics
- Alternatively, extend `useFeatures` to include metrics in a single query with joins

**Feature Metrics Display - Compact Badge**
- Create `FeatureMetricsBadge` component for Kanban/List cards
- Format: "80% | 5/6" where 80% = task completion, 5/6 = passed/total tests
- Use checkmark icon for tasks, flask/beaker icon for tests
- Muted styling when no tasks or tests exist
- Add badge to existing `FeatureCard` component in the footer area

**Feature Metrics Display - Detail View**
- Create `FeatureMetricsDetail` component for feature detail modal/panel
- Show progress bar for task completion with count and percentage
- Show progress bar for test pass rate with passed/failed/pending breakdown
- Show bug count by severity (icon + count for each level)
- Integrate into existing `FeatureDetailPanel` component

**Project-Level Dashboard Integration**
- Add `ProjectTestsSummaryCard` to ProjectOverview: total tests, passed count, failed count, pending count, overall pass rate
- Add `ProjectBugsSeverityCard` to ProjectOverview: bugs grouped by severity with counts, total open bugs count
- Add overall health indicator card: combines feature completion, test pass rate, open critical bugs into a simple status (healthy/warning/critical)
- Maintain existing card grid layout (expand from 3 to 4-5 cards or use 2 rows)

## Visual Design

No visual mockups provided. Follow existing design patterns:
- Use design-system.md color palette for status/severity badges
- Follow SprintCard component structure for metrics display
- Follow CreateTaskModal pattern for form modals
- Maintain dark theme consistency with card backgrounds (#171717) and borders (#2E2E2E)

## Existing Code to Leverage

**hooks/useTasks.ts**
- Complete CRUD hook pattern with React Query mutations
- Optimistic update implementation in useUpdateTaskStatus
- Query key factory pattern with TASK_QUERY_KEYS
- Stale time configuration and query enabling pattern
- Use as direct template for useTests.ts and useBugs.ts

**types/task.ts**
- Status and priority const arrays with type derivation
- Status/priority config objects with label, color, bgColor/icon
- CreateInput and UpdateInput interface patterns
- Query keys object structure
- Use as template for types/test.ts and types/bug.ts

**components/features/task-management/CreateTaskModal.tsx**
- Dialog component structure with Header, Content, Footer
- react-hook-form with Zod schema validation pattern
- Select components for status/priority fields
- Toast notifications on mutation success/error
- Form reset on modal open/close
- Use as template for Create/Edit modals for tests and bugs

**components/features/sprint-management/SprintCard.tsx**
- Metrics display with progress bars and percentages
- Badge component usage for status display
- Compact layout with multiple metrics in footer
- Skeleton component pattern for loading states
- Use progress bar pattern for FeatureMetricsBadge and FeatureMetricsDetail

**components/features/projects/ProjectOverview.tsx**
- Dashboard card grid layout with 3 columns
- Loading skeleton pattern for dashboard
- Metrics calculation from hook data
- Card structure with icon, label, value, and optional action
- Extend with new test/bug summary cards following same structure

## Out of Scope

- Test automation or execution (running tests automatically from the app)
- Notifications (email, push, or in-app notifications for test/bug changes)
- Historical trends or time-series metrics (charts showing progress over time)
- Bug assignment to users (bugs are not assignable, only linked to features/tasks)
- Import/export functionality (CSV, JSON export of tests or bugs)
- Bulk operations on tests or bugs (multi-select, bulk status change)
- Test attachments or screenshots
- Bug comments or activity history
- Kanban board views for tests or bugs (list view only in this sprint)
- Filtering or search within tests/bugs lists (basic list display only)
