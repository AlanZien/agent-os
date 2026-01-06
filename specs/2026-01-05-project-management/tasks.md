# Task Breakdown: Project Management

## Overview

**Feature:** Project Management - CRUD operations with card-based list view and modals
**Complexity Score:** 18 (Standard Track)
**Total Tasks:** 32 sub-tasks across 6 task groups
**Total Tests:** 56 tests (17 Critical, 23 High, 14 Medium, 2 Low)

### Execution Strategy
- **Foundation First:** Types, validations, and test setup
- **TDD Approach:** Write tests before implementation for each layer
- **Progressive Integration:** Database -> Hooks -> Components -> Pages

---

## Task List

### Foundation Layer

#### Task Group 1: Types, Validation, and Test Infrastructure
**Dependencies:** None
**Estimated Effort:** 2-3 hours
**Complexity:** Low

- [ ] 1.0 Complete foundation layer
  - [ ] 1.1 Create Project types and interfaces
    - File: `types/project.ts`
    - Define `Project` interface (id, name, description, owner_id, created_at, updated_at)
    - Define `CreateProjectInput` type (name, description)
    - Define `UpdateProjectInput` type (name?, description?)
    - Export query key constants (`PROJECTS_QUERY_KEY`)
    - Pattern reference: Use existing auth types as template
  - [ ] 1.2 Create Zod validation schemas
    - File: `lib/validations/project.ts`
    - `createProjectSchema`: name (required, max 100), description (optional, max 500)
    - `updateProjectSchema`: same rules but all optional
    - Export typed form schemas for react-hook-form integration
  - [ ] 1.3 Write validation schema tests
    - File: `__tests__/unit/validations/project.test.ts`
    - Test valid project data passes
    - Test empty name fails
    - Test name > 100 chars fails
    - Test description > 500 chars fails
    - Expected: 4-6 unit tests
  - [ ] 1.4 Set up test fixtures and mocks
    - File: `__tests__/fixtures/projects.ts` (sample project data)
    - File: `__tests__/mocks/supabase.ts` (extend existing mock)
    - Create MOCK_PROJECTS with various edge cases (long names, empty description)
    - Add mock owner data for display tests
  - [ ] 1.5 Verify foundation tests pass
    - Run: `npm run test -- __tests__/unit/validations/project.test.ts`
    - Expected: All validation tests passing
    - Confirm TypeScript compiles without errors

**Acceptance Criteria:**
- [ ] `Project` type properly typed with all fields
- [ ] Zod schemas enforce all validation rules from spec
- [ ] Unit tests cover all validation edge cases
- [ ] Test fixtures available for hook/component tests

---

### Service Layer (React Query Hooks)

#### Task Group 2: useProjects Query Hook
**Dependencies:** Task Group 1
**Estimated Effort:** 2-3 hours
**Complexity:** Medium

- [ ] 2.0 Complete useProjects hook
  - [ ] 2.1 Write useProjects tests (see test-plan.md tests 8-12)
    - File: `__tests__/integration/hooks/useProjects.test.ts`
    - Test 8: `test_useProjects_fetches_all_user_projects`
    - Test 9: `test_useProjects_returns_empty_array_when_no_projects`
    - Test 10: `test_useProjects_handles_fetch_error`
    - Test 11: `test_useProjects_respects_stale_time`
    - Test 12: `test_useProjects_query_key_pattern`
    - Use @tanstack/react-query test utils with renderHook
    - Expected: 5 tests for query behavior
  - [ ] 2.2 Implement useProjects hook
    - File: `hooks/useProjects.ts`
    - Query key: `['projects']`
    - Stale time: 30 seconds (30000ms)
    - Fetch from Supabase using browser client
    - Order by created_at desc
    - Include owner profile data via join or separate query
  - [ ] 2.3 Create QueryClientProvider wrapper
    - File: `components/providers/QueryProvider.tsx`
    - Configure default options (staleTime, retry logic)
    - Add to root layout if not present
  - [ ] 2.4 Verify useProjects tests pass
    - Run: `npm run test -- __tests__/integration/hooks/useProjects.test.ts`
    - Expected: 5/5 tests passing

**Acceptance Criteria:**
- [ ] Hook returns projects array, isLoading, error states
- [ ] Query uses correct key pattern for cache management
- [ ] Stale time configured per spec (30s)
- [ ] All 5 tests from test-plan.md pass

---

#### Task Group 3: Mutation Hooks (Create, Update, Delete)
**Dependencies:** Task Group 2
**Estimated Effort:** 3-4 hours
**Complexity:** Medium-High

- [ ] 3.0 Complete mutation hooks
  - [ ] 3.1 Write useCreateProject tests (see test-plan.md tests 13-15)
    - File: `__tests__/integration/hooks/useCreateProject.test.ts`
    - Test 13: `test_useCreateProject_creates_project_successfully`
    - Test 14: `test_useCreateProject_handles_validation_error`
    - Test 15: `test_useCreateProject_handles_server_error`
    - Verify query invalidation after success
    - Expected: 3 tests
  - [ ] 3.2 Implement useCreateProject hook
    - File: `hooks/useCreateProject.ts`
    - Insert into projects table
    - Auto-assign owner_id from authenticated user
    - Invalidate `['projects']` query on success
    - Return created project data
  - [ ] 3.3 Write useUpdateProject tests (see test-plan.md tests 16-17)
    - File: `__tests__/integration/hooks/useUpdateProject.test.ts`
    - Test 16: `test_useUpdateProject_updates_project_successfully`
    - Test 17: `test_useUpdateProject_performs_optimistic_update`
    - Verify optimistic update and rollback behavior
    - Expected: 2 tests
  - [ ] 3.4 Implement useUpdateProject hook
    - File: `hooks/useUpdateProject.ts`
    - Update by project ID
    - Implement optimistic update pattern
    - Rollback on error
    - Invalidate queries on success
  - [ ] 3.5 Write useDeleteProject tests (see test-plan.md tests 18-19)
    - File: `__tests__/integration/hooks/useDeleteProject.test.ts`
    - Test 18: `test_useDeleteProject_deletes_project_successfully`
    - Test 19: `test_useDeleteProject_handles_not_found_error`
    - Expected: 2 tests
  - [ ] 3.6 Implement useDeleteProject hook
    - File: `hooks/useDeleteProject.ts`
    - Hard delete from projects table
    - Invalidate `['projects']` query on success
    - Handle not found gracefully
  - [ ] 3.7 Create hooks barrel export
    - File: `hooks/projects/index.ts`
    - Export all project-related hooks
  - [ ] 3.8 Verify all mutation hook tests pass
    - Run: `npm run test -- __tests__/integration/hooks/`
    - Expected: 12/12 tests passing (5 query + 7 mutation)

**Acceptance Criteria:**
- [ ] Create mutation inserts project with owner_id
- [ ] Update mutation performs optimistic updates
- [ ] Delete mutation hard-deletes project
- [ ] All mutations invalidate project list query
- [ ] All 7 mutation tests pass

---

### UI Components Layer

#### Task Group 4: Core UI Components
**Dependencies:** Task Group 3
**Estimated Effort:** 4-5 hours
**Complexity:** Medium

- [ ] 4.0 Complete core UI components
  - [ ] 4.1 Write ProjectCard tests (see test-plan.md tests 27-33)
    - File: `__tests__/integration/components/ProjectCard.test.tsx`
    - Test 27: `test_ProjectCard_renders_project_name_truncated`
    - Test 28: `test_ProjectCard_renders_description_truncated`
    - Test 29: `test_ProjectCard_renders_owner_name`
    - Test 30: `test_ProjectCard_renders_relative_date`
    - Test 31: `test_ProjectCard_navigates_to_detail_page_on_click`
    - Test 32: `test_ProjectCard_shows_hover_effect` (Low priority - optional)
    - Test 33: `test_ProjectCard_context_menu_opens_on_click`
    - Expected: 6-7 tests
  - [ ] 4.2 Implement ProjectCard component
    - File: `components/features/projects/ProjectCard.tsx`
    - Display name (H4, line-clamp-1)
    - Display description (line-clamp-2)
    - Display owner name or email fallback
    - Display relative date (use date-fns or similar)
    - Clickable card navigates to `/projects/[id]`
    - Three-dot context menu with Edit/Delete options
    - Hover effect: border-strong transition
  - [ ] 4.3 Write CreateProjectModal tests (see test-plan.md tests 34-40)
    - File: `__tests__/integration/components/CreateProjectModal.test.tsx`
    - Test 34: `test_CreateProjectModal_renders_form_fields`
    - Test 35: `test_CreateProjectModal_validates_name_required`
    - Test 36: `test_CreateProjectModal_validates_name_max_length`
    - Test 37: `test_CreateProjectModal_validates_description_max_length`
    - Test 38: `test_CreateProjectModal_shows_loading_state_on_submit`
    - Test 39: `test_CreateProjectModal_closes_on_successful_create`
    - Test 40: `test_CreateProjectModal_cancel_button_closes_modal`
    - Expected: 7 tests
  - [ ] 4.4 Implement CreateProjectModal component
    - File: `components/features/projects/CreateProjectModal.tsx`
    - Use Dialog from shadcn/ui
    - Form with react-hook-form + zod resolver
    - Name input (required indicator, 100 char max)
    - Description textarea (optional, 500 char max)
    - Create button with loading state
    - Cancel button closes modal
    - Toast notification on success/error
  - [ ] 4.5 Write EditProjectModal tests (see test-plan.md tests 41-45)
    - File: `__tests__/integration/components/EditProjectModal.test.tsx`
    - Test 41: `test_EditProjectModal_pre_populates_existing_data`
    - Test 42: `test_EditProjectModal_validates_same_as_create`
    - Test 43: `test_EditProjectModal_shows_success_toast_on_save`
    - Test 44: `test_EditProjectModal_shows_error_toast_on_failure`
    - Test 45: `test_EditProjectModal_cancel_discards_changes`
    - Expected: 5 tests
  - [ ] 4.6 Implement EditProjectModal component
    - File: `components/features/projects/EditProjectModal.tsx`
    - Same form structure as CreateProjectModal
    - Pre-populate with existing project data
    - "Save" button instead of "Create"
    - Use useUpdateProject mutation
    - Display appropriate toasts
  - [ ] 4.7 Write DeleteConfirmationDialog tests (see test-plan.md tests 46-50)
    - File: `__tests__/integration/components/DeleteConfirmationDialog.test.tsx`
    - Test 46: `test_DeleteDialog_displays_project_name`
    - Test 47: `test_DeleteDialog_shows_destructive_button`
    - Test 48: `test_DeleteDialog_confirms_deletion_on_delete_click`
    - Test 49: `test_DeleteDialog_cancel_button_closes_without_delete`
    - Test 50: `test_DeleteDialog_click_outside_closes_dialog` (Low priority)
    - Expected: 4-5 tests
  - [ ] 4.8 Implement DeleteConfirmationDialog component
    - File: `components/features/projects/DeleteConfirmationDialog.tsx`
    - Use AlertDialog from shadcn/ui
    - Display project name in message
    - Warning text about permanent deletion
    - Destructive "Delete" button (red variant)
    - Cancel button (secondary)
    - Call useDeleteProject on confirm
  - [ ] 4.9 Create components barrel export
    - File: `components/features/projects/index.ts`
    - Export all project components
  - [ ] 4.10 Verify all component tests pass
    - Run: `npm run test -- __tests__/integration/components/`
    - Expected: 23-25/25 tests passing (can skip Low priority tests)

**Acceptance Criteria:**
- [ ] ProjectCard displays all required information
- [ ] ProjectCard has working navigation and context menu
- [ ] CreateProjectModal validates and submits correctly
- [ ] EditProjectModal pre-populates and updates correctly
- [ ] DeleteConfirmationDialog confirms before deletion
- [ ] All modals show appropriate loading/error states
- [ ] All Critical/High priority component tests pass

---

### Page Integration Layer

#### Task Group 5: Projects List Page and Detail Page
**Dependencies:** Task Group 4
**Estimated Effort:** 3-4 hours
**Complexity:** Medium

- [ ] 5.0 Complete page integration
  - [ ] 5.1 Write ProjectListPage tests (see test-plan.md tests 20-26)
    - File: `__tests__/integration/components/ProjectListPage.test.tsx`
    - Test 20: `test_ProjectListPage_renders_page_header_with_title`
    - Test 21: `test_ProjectListPage_renders_skeleton_while_loading`
    - Test 22: `test_ProjectListPage_renders_project_grid_with_data`
    - Test 23: `test_ProjectListPage_renders_empty_state`
    - Test 24: `test_ProjectListPage_renders_error_state`
    - Test 25: `test_ProjectListPage_retry_button_refetches_data`
    - Test 26: `test_ProjectListPage_new_project_button_opens_modal`
    - Expected: 7 tests
  - [ ] 5.2 Implement ProjectListPage client component
    - File: `components/features/projects/ProjectListPage.tsx`
    - Page header with "Projects" title and "New Project" button
    - Use useProjects hook for data
    - Loading state: skeleton grid (3-6 skeleton cards)
    - Empty state: illustration + "No projects yet" + CTA button
    - Error state: error message + retry button
    - Grid layout: 1 col mobile, 2 cols tablet, 3 cols desktop
    - Gap: 16px (gap-4)
    - Render ProjectCard for each project
  - [ ] 5.3 Update projects page.tsx
    - File: `app/(dashboard)/projects/page.tsx`
    - Import and render ProjectListPage
    - Server-side initial data fetch (optional for SSR hydration)
    - Ensure layout wraps with QueryProvider if not global
  - [ ] 5.4 Write ProjectDetailPage tests (see test-plan.md tests 51-53)
    - File: `__tests__/integration/components/ProjectDetailPage.test.tsx`
    - Test 51: `test_ProjectDetailPage_displays_project_info`
    - Test 52: `test_ProjectDetailPage_shows_breadcrumb_navigation`
    - Test 53: `test_ProjectDetailPage_handles_not_found`
    - Expected: 3 tests
  - [ ] 5.5 Create project detail page (placeholder)
    - File: `app/(dashboard)/projects/[id]/page.tsx`
    - Fetch single project by ID
    - Display project name (H1) and description
    - Breadcrumb: "Projects > [Project Name]"
    - Placeholder content for future specs/tasks section
    - Handle 404 if project not found
  - [ ] 5.6 Verify page integration tests pass
    - Run: `npm run test -- __tests__/integration/components/ProjectListPage.test.tsx __tests__/integration/components/ProjectDetailPage.test.tsx`
    - Expected: 10/10 tests passing

**Acceptance Criteria:**
- [ ] Projects page displays grid of project cards
- [ ] Page handles loading, empty, and error states
- [ ] New Project button opens create modal
- [ ] Project detail page shows project info with breadcrumb
- [ ] Navigation between list and detail works correctly
- [ ] All 10 page tests pass

---

### E2E and Final Validation Layer

#### Task Group 6: E2E Tests and Final Validation
**Dependencies:** Task Group 5
**Estimated Effort:** 3-4 hours
**Complexity:** Medium-High

- [ ] 6.0 Complete E2E tests and validation
  - [ ] 6.1 Set up E2E test fixtures
    - File: `e2e/fixtures/projects.ts`
    - Extend auth fixture with project seeding
    - Create test projects in database before tests
    - Clean up test projects after tests
    - Ensure isolated test environment
  - [ ] 6.2 Write E2E tests (see test-plan.md tests 54-62)
    - File: `e2e/dashboard/projects.spec.ts`
    - Test 54: `test_e2e_user_can_view_projects_list` (Critical)
    - Test 55: `test_e2e_user_can_create_new_project` (Critical)
    - Test 56: `test_e2e_user_can_edit_existing_project` (Critical)
    - Test 57: `test_e2e_user_can_delete_project` (High)
    - Test 58: `test_e2e_user_can_navigate_to_project_detail` (High)
    - Test 59: `test_e2e_create_modal_validates_empty_name` (High)
    - Test 60: `test_e2e_empty_state_shows_when_no_projects` (High)
    - Test 61: `test_e2e_cancel_button_closes_modal_without_saving` (Medium)
    - Test 62: `test_e2e_responsive_grid_layout` (Medium)
    - Expected: 9 E2E tests
  - [ ] 6.3 Run full E2E test suite
    - Command: `npm run test:e2e -- e2e/dashboard/projects.spec.ts`
    - Expected: 9/9 E2E tests passing
    - Verify on multiple browsers if configured (Chromium minimum)
  - [ ] 6.4 Run complete test validation
    - Run ALL unit tests: `npm run test:run`
    - Run ALL E2E tests: `npm run test:e2e`
    - Verify test counts match test-plan.md
    - Expected totals:
      - Database/RLS: 7 tests (if applicable)
      - Service/Query: 12 tests
      - UI Components: 28 tests
      - E2E: 9 tests
      - Total: ~56 tests
  - [ ] 6.5 Generate test coverage report
    - Command: `npm run test:coverage`
    - Target: 80%+ line coverage for new code
    - Document any gaps
  - [ ] 6.6 Final acceptance validation
    - Manual smoke test of all user flows
    - Verify responsive layout (mobile/tablet/desktop)
    - Confirm toast notifications display correctly
    - Validate optimistic updates work smoothly
    - Check all form validations are user-friendly

**Acceptance Criteria:**
- [ ] All 9 E2E tests pass
- [ ] 100% of Critical priority tests pass (17 tests)
- [ ] 100% of High priority tests pass (23 tests)
- [ ] At least 80% of Medium priority tests pass (14 tests)
- [ ] No failing tests in CI
- [ ] Feature is ready for deployment

---

## Execution Order Summary

| Order | Task Group | Focus | Tests | Effort |
|-------|-----------|-------|-------|--------|
| 1 | Foundation | Types, Validation, Fixtures | 4-6 | 2-3h |
| 2 | useProjects | Query Hook | 5 | 2-3h |
| 3 | Mutations | Create/Update/Delete Hooks | 7 | 3-4h |
| 4 | Components | Cards, Modals, Dialogs | 23-25 | 4-5h |
| 5 | Pages | List Page, Detail Page | 10 | 3-4h |
| 6 | E2E | End-to-End Flows | 9 | 3-4h |

**Total Estimated Effort:** 17-23 hours

---

## Test Reference Quick Guide

### By Layer (from test-plan.md)

| Layer | Test IDs | File Location |
|-------|----------|---------------|
| RLS | 1-7 | `__tests__/rls/projects.rls.test.ts` |
| Hooks | 8-19 | `__tests__/integration/hooks/use*.test.ts` |
| Components | 20-53 | `__tests__/integration/components/*.test.tsx` |
| E2E | 54-62 | `e2e/dashboard/projects.spec.ts` |

### By Priority

| Priority | Count | Required Pass Rate |
|----------|-------|-------------------|
| Critical | 17 | 100% |
| High | 23 | 100% |
| Medium | 14 | 80% |
| Low | 2 | Deferred |

---

## Files to Create/Modify

### New Files
```
types/project.ts
lib/validations/project.ts
hooks/useProjects.ts
hooks/useCreateProject.ts
hooks/useUpdateProject.ts
hooks/useDeleteProject.ts
hooks/projects/index.ts
components/providers/QueryProvider.tsx
components/features/projects/ProjectCard.tsx
components/features/projects/CreateProjectModal.tsx
components/features/projects/EditProjectModal.tsx
components/features/projects/DeleteConfirmationDialog.tsx
components/features/projects/ProjectListPage.tsx
components/features/projects/index.ts
app/(dashboard)/projects/[id]/page.tsx
__tests__/unit/validations/project.test.ts
__tests__/integration/hooks/useProjects.test.ts
__tests__/integration/hooks/useCreateProject.test.ts
__tests__/integration/hooks/useUpdateProject.test.ts
__tests__/integration/hooks/useDeleteProject.test.ts
__tests__/integration/components/ProjectCard.test.tsx
__tests__/integration/components/CreateProjectModal.test.tsx
__tests__/integration/components/EditProjectModal.test.tsx
__tests__/integration/components/DeleteConfirmationDialog.test.tsx
__tests__/integration/components/ProjectListPage.test.tsx
__tests__/integration/components/ProjectDetailPage.test.tsx
__tests__/fixtures/projects.ts
e2e/dashboard/projects.spec.ts
e2e/fixtures/projects.ts
```

### Modified Files
```
app/(dashboard)/projects/page.tsx
__tests__/mocks/supabase.ts (extend)
app/layout.tsx (add QueryProvider if not present)
```

---

## Notes

1. **RLS Tests (1-7):** These require a Supabase test instance. If not available in local dev, they can be run in CI with proper test database setup.

2. **Optimistic Updates:** Task 3.4 implements optimistic updates for edit. This is a more advanced React Query pattern - reference the official TanStack docs if needed.

3. **Relative Dates:** Use `date-fns` library (`formatDistanceToNow`) for "2 days ago" style dates. Install if not present.

4. **shadcn/ui Components:** Dialog and AlertDialog components needed. Run `npx shadcn@latest add dialog alert-dialog` if not installed.

5. **Toast Notifications:** Ensure sonner or toast component is configured. Reference existing toast pattern in codebase.
