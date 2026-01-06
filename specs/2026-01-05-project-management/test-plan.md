# Test Plan: Project Management

## Metadata
- **Feature**: Project Management - CRUD operations with card-based list view and modals
- **Spec**: agent-os/specs/2026-01-05-project-management/spec.md
- **Requirements**: agent-os/specs/2026-01-05-project-management/planning/requirements.md
- **Created**: 2026-01-06
- **Status**: Planning Complete

## Test Summary

| Layer | Critical | High | Medium | Low | Total |
|-------|----------|------|--------|-----|-------|
| Database/RLS | 4 | 2 | 1 | 0 | 7 |
| Service/Query | 4 | 5 | 3 | 0 | 12 |
| UI Components | 6 | 12 | 8 | 2 | 28 |
| E2E | 3 | 4 | 2 | 0 | 9 |
| **Total** | **17** | **23** | **14** | **2** | **56** |

**Coverage Targets:**
- Critical paths: 100%
- High priority: 100%
- Medium priority: 80%
- Low priority: Deferred

---

## Database/RLS Layer

### RLS Policy Tests (7 tests)

#### 1. test_rls_user_can_read_own_projects
**Priority:** Critical
**Given:**
- User A is authenticated with user_id = "user-a-123"
- User A owns 3 projects in the database
- User B owns 2 projects in the database
**When:** User A queries `SELECT * FROM projects`
**Then:**
- Only 3 projects are returned (User A's projects)
- None of User B's projects are visible
**Related Requirement:** spec.md "API Integration > RLS policies handle authorization"

#### 2. test_rls_user_can_create_project_with_own_id
**Priority:** Critical
**Given:**
- User A is authenticated with user_id = "user-a-123"
- Request body: `{ name: "New Project", owner_id: "user-a-123" }`
**When:** User A executes `INSERT INTO projects`
**Then:**
- Project is created successfully
- owner_id matches authenticated user
**Related Requirement:** spec.md "API Integration > RLS policies handle authorization"

#### 3. test_rls_user_cannot_create_project_for_other_user
**Priority:** Critical
**Given:**
- User A is authenticated with user_id = "user-a-123"
- Request body: `{ name: "Malicious Project", owner_id: "user-b-456" }`
**When:** User A attempts `INSERT INTO projects`
**Then:**
- Insert is rejected by RLS policy
- Error message indicates permission denied
**Related Requirement:** spec.md "API Integration > RLS policies handle authorization"

#### 4. test_rls_user_can_update_own_project
**Priority:** Critical
**Given:**
- User A owns project with id = "proj-123"
- Update payload: `{ name: "Updated Name" }`
**When:** User A executes `UPDATE projects WHERE id = 'proj-123'`
**Then:**
- Project is updated successfully
- updated_at timestamp is refreshed
**Related Requirement:** spec.md "Edit Project Modal"

#### 5. test_rls_user_cannot_update_other_users_project
**Priority:** High
**Given:**
- User B owns project with id = "proj-456"
- User A is authenticated
**When:** User A attempts `UPDATE projects WHERE id = 'proj-456'`
**Then:**
- Update fails silently (0 rows affected)
- Project remains unchanged
**Related Requirement:** spec.md "API Integration > RLS policies handle authorization"

#### 6. test_rls_user_can_delete_own_project
**Priority:** High
**Given:**
- User A owns project with id = "proj-123"
**When:** User A executes `DELETE FROM projects WHERE id = 'proj-123'`
**Then:**
- Project is permanently deleted
- No orphaned data remains
**Related Requirement:** spec.md "Delete Project Confirmation > Hard delete"

#### 7. test_rls_unauthenticated_user_cannot_access_projects
**Priority:** Medium
**Given:**
- No authentication token provided
- Projects exist in database
**When:** Anonymous user queries `SELECT * FROM projects`
**Then:**
- Query returns empty result or error
- No project data is exposed
**Related Requirement:** spec.md "API Integration > RLS policies handle authorization"

---

## Service/Query Layer (React Query Hooks)

### useProjects Hook (5 tests)

#### 8. test_useProjects_fetches_all_user_projects
**Priority:** Critical
**Given:**
- User is authenticated
- User owns 5 projects in database
- Supabase client is properly configured
**When:** `useProjects()` hook is called
**Then:**
- `data` contains array of 5 projects
- `isLoading` transitions from true to false
- `error` is null
**Related Requirement:** spec.md "Project List Page > Display projects"

#### 9. test_useProjects_returns_empty_array_when_no_projects
**Priority:** High
**Given:**
- User is authenticated
- User has no projects
**When:** `useProjects()` hook is called
**Then:**
- `data` is empty array `[]`
- `isLoading` is false
- `error` is null
**Related Requirement:** spec.md "Project List Page > Empty state"

#### 10. test_useProjects_handles_fetch_error
**Priority:** High
**Given:**
- User is authenticated
- Supabase returns error (network failure, timeout)
**When:** `useProjects()` hook is called
**Then:**
- `data` is undefined
- `isLoading` is false
- `error` contains error object with message
**Related Requirement:** spec.md "Project List Page > Error state"

#### 11. test_useProjects_respects_stale_time
**Priority:** Medium
**Given:**
- User fetched projects 15 seconds ago
- Stale time configured to 30 seconds
**When:** Component remounts
**Then:**
- Cached data is returned immediately
- No new fetch request is made
**Related Requirement:** spec.md "Data Fetching > Configure stale time of 30 seconds"

#### 12. test_useProjects_query_key_pattern
**Priority:** Medium
**Given:**
- React Query DevTools available
**When:** `useProjects()` hook is called
**Then:**
- Query is registered with key `['projects']`
**Related Requirement:** spec.md "Data Fetching > Query key pattern"

### useCreateProject Mutation (3 tests)

#### 13. test_useCreateProject_creates_project_successfully
**Priority:** Critical
**Given:**
- User is authenticated
- Valid project data: `{ name: "Test Project", description: "Description" }`
**When:** `mutate({ name, description })` is called
**Then:**
- `isSuccess` becomes true
- New project is returned in `data`
- Projects list query is invalidated (refetched)
**Related Requirement:** spec.md "Create Project Modal > Close modal and refresh list"

#### 14. test_useCreateProject_handles_validation_error
**Priority:** High
**Given:**
- User is authenticated
- Invalid data: `{ name: "", description: "..." }` (empty name)
**When:** `mutate()` is called
**Then:**
- `isError` becomes true
- `error` contains validation message
- No project is created
**Related Requirement:** spec.md "Create Project Modal > Form validation"

#### 15. test_useCreateProject_handles_server_error
**Priority:** High
**Given:**
- User is authenticated
- Valid data provided
- Supabase returns 500 error
**When:** `mutate()` is called
**Then:**
- `isError` becomes true
- `error` contains server error message
- Projects list is not invalidated
**Related Requirement:** spec.md "Create Project Modal > Display toast notification on error"

### useUpdateProject Mutation (2 tests)

#### 16. test_useUpdateProject_updates_project_successfully
**Priority:** Critical
**Given:**
- User owns project with id = "proj-123"
- Update data: `{ name: "Updated Name", description: "New desc" }`
**When:** `mutate({ id: "proj-123", ...updateData })` is called
**Then:**
- `isSuccess` becomes true
- Updated project is returned
- Projects list query is invalidated
**Related Requirement:** spec.md "Edit Project Modal > Optimistic update pattern"

#### 17. test_useUpdateProject_performs_optimistic_update
**Priority:** High
**Given:**
- User owns project with id = "proj-123"
- Current name: "Old Name"
**When:** `mutate({ id: "proj-123", name: "New Name" })` is called
**Then:**
- UI immediately shows "New Name" (before server response)
- On success: new name persists
- On error: rollback to "Old Name"
**Related Requirement:** spec.md "Edit Project Modal > Optimistic update pattern"

### useDeleteProject Mutation (2 tests)

#### 18. test_useDeleteProject_deletes_project_successfully
**Priority:** Critical
**Given:**
- User owns project with id = "proj-123"
**When:** `mutate("proj-123")` is called
**Then:**
- `isSuccess` becomes true
- Project is removed from database
- Projects list query is invalidated
**Related Requirement:** spec.md "Delete Project Confirmation > Hard delete"

#### 19. test_useDeleteProject_handles_not_found_error
**Priority:** Medium
**Given:**
- Project with id = "non-existent" does not exist
**When:** `mutate("non-existent")` is called
**Then:**
- `isError` becomes true
- Error indicates project not found
**Related Requirement:** spec.md "Delete Project Confirmation"

---

## UI Components Layer

### ProjectListPage Component (7 tests)

#### 20. test_ProjectListPage_renders_page_header_with_title
**Priority:** Critical
**Given:**
- User is authenticated
- Component is mounted
**When:** Page renders
**Then:**
- Page title "Projects" is visible (H1)
- "New Project" button is visible in header
**Related Requirement:** spec.md "Project List Page > Page header includes title"

#### 21. test_ProjectListPage_renders_skeleton_while_loading
**Priority:** High
**Given:**
- User is authenticated
- Projects are being fetched (`isLoading: true`)
**When:** Page renders during loading
**Then:**
- Skeleton cards are displayed
- Skeleton matches grid layout (responsive columns)
- "New Project" button is visible but may be disabled
**Related Requirement:** spec.md "Project List Page > Loading state shows skeleton cards"

#### 22. test_ProjectListPage_renders_project_grid_with_data
**Priority:** Critical
**Given:**
- User is authenticated
- 5 projects returned from hook
**When:** Page renders with data
**Then:**
- 5 ProjectCard components are rendered
- Grid layout is applied (gap-4 / 16px)
- Cards are in responsive grid (1/2/3 columns)
**Related Requirement:** spec.md "Project List Page > Display projects in responsive card grid"

#### 23. test_ProjectListPage_renders_empty_state
**Priority:** High
**Given:**
- User is authenticated
- No projects exist (empty array)
**When:** Page renders with empty data
**Then:**
- Empty state illustration is displayed
- "No projects yet" message is visible
- CTA button to create project is visible
**Related Requirement:** spec.md "Project List Page > Empty state"

#### 24. test_ProjectListPage_renders_error_state
**Priority:** High
**Given:**
- User is authenticated
- Fetch failed with error
**When:** Page renders with error
**Then:**
- Error message is displayed
- Retry button is visible
- Grid is not rendered
**Related Requirement:** spec.md "Project List Page > Error state with retry button"

#### 25. test_ProjectListPage_retry_button_refetches_data
**Priority:** Medium
**Given:**
- Page is in error state
- Retry button is visible
**When:** User clicks "Retry" button
**Then:**
- Loading state is shown
- `refetch()` is called
- On success: projects are displayed
**Related Requirement:** spec.md "Project List Page > Error state with retry button"

#### 26. test_ProjectListPage_new_project_button_opens_modal
**Priority:** High
**Given:**
- Page is rendered with data
- CreateProjectModal is not visible
**When:** User clicks "New Project" button
**Then:**
- CreateProjectModal is opened
- Modal form is empty (no pre-populated data)
**Related Requirement:** spec.md "Create Project Modal > Trigger via New Project button"

### ProjectCard Component (7 tests)

#### 27. test_ProjectCard_renders_project_name_truncated
**Priority:** Critical
**Given:**
- Project with name: "This is a very long project name that should be truncated"
**When:** Card renders
**Then:**
- Name is displayed as H4
- Name is truncated to 1 line (text-overflow: ellipsis)
**Related Requirement:** spec.md "Project Card Component > Name truncated at 1 line"

#### 28. test_ProjectCard_renders_description_truncated
**Priority:** High
**Given:**
- Project with long description (>2 lines worth)
**When:** Card renders
**Then:**
- Description is visible
- Description is truncated at 2 lines (line-clamp-2)
**Related Requirement:** spec.md "Project Card Component > Description truncated at 2 lines"

#### 29. test_ProjectCard_renders_owner_name
**Priority:** High
**Given:**
- Project with owner: `{ name: "John Doe", email: "john@test.com" }`
**When:** Card renders
**Then:**
- Owner name "John Doe" is displayed
- If no name, email is shown as fallback
**Related Requirement:** spec.md "Project Card Component > Owner name or email"

#### 30. test_ProjectCard_renders_relative_date
**Priority:** Medium
**Given:**
- Project created 2 days ago (created_at: 2 days prior)
**When:** Card renders
**Then:**
- Date displays as "2 days ago"
- Not showing absolute date format
**Related Requirement:** spec.md "Project Card Component > Relative format"

#### 31. test_ProjectCard_navigates_to_detail_page_on_click
**Priority:** Critical
**Given:**
- Project with id: "proj-123"
- Router mock configured
**When:** User clicks on card (not context menu)
**Then:**
- `router.push('/projects/proj-123')` is called
- Navigation occurs to detail page
**Related Requirement:** spec.md "Project Card Component > Navigates to /projects/[id]"

#### 32. test_ProjectCard_shows_hover_effect
**Priority:** Low
**Given:**
- Card is rendered in default state
**When:** User hovers over card
**Then:**
- Border color changes to border-strong
- Cursor changes to pointer
**Related Requirement:** spec.md "Project Card Component > Subtle hover effect"

#### 33. test_ProjectCard_context_menu_opens_on_click
**Priority:** High
**Given:**
- Card with three-dot menu icon visible
**When:** User clicks three-dot icon
**Then:**
- Context menu opens with "Edit" and "Delete" options
- Click does NOT navigate to detail page
**Related Requirement:** spec.md "Edit Project Modal > Access via context menu"

### CreateProjectModal Component (7 tests)

#### 34. test_CreateProjectModal_renders_form_fields
**Priority:** Critical
**Given:**
- Modal is open (isOpen: true)
**When:** Modal renders
**Then:**
- Name input field is visible (required indicator)
- Description textarea is visible (optional indicator)
- "Create" primary button is visible
- "Cancel" secondary button is visible
**Related Requirement:** spec.md "Create Project Modal > Form fields"

#### 35. test_CreateProjectModal_validates_name_required
**Priority:** High
**Given:**
- Modal is open
- Name field is empty
**When:** User clicks "Create" button
**Then:**
- Inline error message appears under name field
- Form is not submitted
- Modal remains open
**Related Requirement:** spec.md "Create Project Modal > Form validation with inline errors"

#### 36. test_CreateProjectModal_validates_name_max_length
**Priority:** Medium
**Given:**
- Modal is open
- Name field has 101 characters (exceeds 100 max)
**When:** User clicks "Create" or types beyond limit
**Then:**
- Inline error message indicates max length exceeded
- Form is not submitted
**Related Requirement:** spec.md "Create Project Modal > name (max 100 chars)"

#### 37. test_CreateProjectModal_validates_description_max_length
**Priority:** Medium
**Given:**
- Modal is open
- Description field has 501 characters (exceeds 500 max)
**When:** User attempts to submit
**Then:**
- Inline error message indicates max length exceeded
- Form is not submitted
**Related Requirement:** spec.md "Create Project Modal > description (max 500 chars)"

#### 38. test_CreateProjectModal_shows_loading_state_on_submit
**Priority:** High
**Given:**
- Modal is open
- Valid form data entered
- Submit in progress
**When:** User clicks "Create" button
**Then:**
- "Create" button shows loading spinner
- Button is disabled
- Form inputs are disabled
**Related Requirement:** spec.md "Create Project Modal > Loading state on submit button"

#### 39. test_CreateProjectModal_closes_on_successful_create
**Priority:** High
**Given:**
- Modal is open
- Valid form data entered
- Create mutation succeeds
**When:** Submission completes successfully
**Then:**
- Modal closes automatically
- Toast notification shows success message
- Form is reset for next open
**Related Requirement:** spec.md "Create Project Modal > Close modal and refresh list"

#### 40. test_CreateProjectModal_cancel_button_closes_modal
**Priority:** Medium
**Given:**
- Modal is open
- Form may have data entered
**When:** User clicks "Cancel" button
**Then:**
- Modal closes
- Form data is cleared
- No API call is made
**Related Requirement:** spec.md "Create Project Modal > Cancel button"

### EditProjectModal Component (5 tests)

#### 41. test_EditProjectModal_pre_populates_existing_data
**Priority:** Critical
**Given:**
- Modal is open with project: `{ id: "proj-123", name: "Test", description: "Desc" }`
**When:** Modal renders
**Then:**
- Name field shows "Test"
- Description field shows "Desc"
- "Save" button is visible (not "Create")
**Related Requirement:** spec.md "Edit Project Modal > Pre-populate form"

#### 42. test_EditProjectModal_validates_same_as_create
**Priority:** High
**Given:**
- Modal is open with project data
- User clears name field
**When:** User clicks "Save" button
**Then:**
- Inline error message appears
- Form is not submitted
**Related Requirement:** spec.md "Edit Project Modal > Same form structure as create"

#### 43. test_EditProjectModal_shows_success_toast_on_save
**Priority:** High
**Given:**
- Modal is open with valid changes
- Update mutation succeeds
**When:** User clicks "Save" button
**Then:**
- Toast notification shows "Project updated successfully"
- Modal closes
**Related Requirement:** spec.md "Edit Project Modal > Display toast on success"

#### 44. test_EditProjectModal_shows_error_toast_on_failure
**Priority:** Medium
**Given:**
- Modal is open with valid changes
- Update mutation fails (server error)
**When:** User clicks "Save" button
**Then:**
- Toast notification shows error message
- Modal remains open
- Form data is preserved
**Related Requirement:** spec.md "Edit Project Modal > Display toast on error"

#### 45. test_EditProjectModal_cancel_discards_changes
**Priority:** Medium
**Given:**
- Modal is open with original data
- User has made changes to name
**When:** User clicks "Cancel" button
**Then:**
- Modal closes
- Changes are discarded
- Original data unchanged
**Related Requirement:** spec.md "Edit Project Modal > Cancel button"

### DeleteConfirmationDialog Component (5 tests)

#### 46. test_DeleteDialog_displays_project_name
**Priority:** Critical
**Given:**
- Dialog is open for project: "My Important Project"
**When:** Dialog renders
**Then:**
- Project name "My Important Project" is displayed in dialog
- Warning text about permanent deletion is visible
**Related Requirement:** spec.md "Delete Project Confirmation > Project name displayed"

#### 47. test_DeleteDialog_shows_destructive_button
**Priority:** High
**Given:**
- Dialog is open
**When:** Dialog renders
**Then:**
- "Delete" button has destructive styling (red/danger variant)
- "Cancel" button has secondary styling
**Related Requirement:** spec.md "Delete Project Confirmation > Destructive Delete button"

#### 48. test_DeleteDialog_confirms_deletion_on_delete_click
**Priority:** Critical
**Given:**
- Dialog is open for project id: "proj-123"
- Delete mutation is mocked
**When:** User clicks "Delete" button
**Then:**
- Delete mutation is called with "proj-123"
- Dialog closes on success
- Toast shows "Project deleted successfully"
**Related Requirement:** spec.md "Delete Project Confirmation > Refresh list and show success toast"

#### 49. test_DeleteDialog_cancel_button_closes_without_delete
**Priority:** High
**Given:**
- Dialog is open
**When:** User clicks "Cancel" button
**Then:**
- Dialog closes
- No delete mutation is called
- Project remains in list
**Related Requirement:** spec.md "Delete Project Confirmation > Cancel button"

#### 50. test_DeleteDialog_click_outside_closes_dialog
**Priority:** Low
**Given:**
- Dialog is open with overlay backdrop
**When:** User clicks outside dialog (on overlay)
**Then:**
- Dialog closes
- No delete mutation is called
**Related Requirement:** spec.md "Delete Project Confirmation"

### ProjectDetailPage Component (3 tests)

#### 51. test_ProjectDetailPage_displays_project_info
**Priority:** High
**Given:**
- Route: `/projects/proj-123`
- Project exists with name and description
**When:** Page renders
**Then:**
- Project name is displayed (H1)
- Project description is displayed
- Placeholder content for specs/tasks section visible
**Related Requirement:** spec.md "Project Detail Page > Display name and description"

#### 52. test_ProjectDetailPage_shows_breadcrumb_navigation
**Priority:** Medium
**Given:**
- Route: `/projects/proj-123`
**When:** Page renders
**Then:**
- Breadcrumb shows "Projects > [Project Name]"
- "Projects" link navigates to `/projects`
**Related Requirement:** spec.md "Project Detail Page > Breadcrumb navigation"

#### 53. test_ProjectDetailPage_handles_not_found
**Priority:** Medium
**Given:**
- Route: `/projects/non-existent`
- Project does not exist
**When:** Page renders
**Then:**
- 404 error or "Project not found" message displayed
- Link to return to projects list
**Related Requirement:** spec.md "Project Detail Page"

---

## E2E Tests (Playwright)

### E2E Test File: `e2e/dashboard/projects.spec.ts`

#### 54. test_e2e_user_can_view_projects_list
**Priority:** Critical
**Preconditions:**
- User is authenticated (use auth fixture)
- User has at least 2 projects seeded in database
**Steps:**
1. Navigate to `/projects`
2. Wait for page to load (skeleton disappears)
3. Verify project cards are visible
**Success Criteria:**
- Page heading "Projects" is visible
- At least 2 project cards are displayed
- Each card shows name, description, owner, date
**Related User Story:** "As a user, I want to view all my projects in a grid layout"

```typescript
// e2e/dashboard/projects.spec.ts
test('user can view projects list', async ({ authenticatedPage: page }) => {
  await page.goto('/projects');

  await expect(page.getByRole('heading', { name: /projects/i })).toBeVisible();
  await expect(page.getByTestId('project-card')).toHaveCount.greaterThanOrEqual(2);
});
```

#### 55. test_e2e_user_can_create_new_project
**Priority:** Critical
**Preconditions:**
- User is authenticated
- Projects list page is loaded
**Steps:**
1. Click "New Project" button
2. Fill in name: "E2E Test Project"
3. Fill in description: "Created via E2E test"
4. Click "Create" button
5. Wait for modal to close
**Success Criteria:**
- Modal opens with empty form
- After submission, modal closes
- Success toast appears
- New project appears in list
- Project card shows entered name
**Related User Story:** "As a user, I want to create a new project with name and description"

```typescript
test('user can create new project', async ({ authenticatedPage: page }) => {
  await page.goto('/projects');
  await page.getByRole('button', { name: /new project/i }).click();

  await page.getByLabel(/name/i).fill('E2E Test Project');
  await page.getByLabel(/description/i).fill('Created via E2E test');
  await page.getByRole('button', { name: /create/i }).click();

  await expect(page.getByText(/success/i)).toBeVisible();
  await expect(page.getByText('E2E Test Project')).toBeVisible();
});
```

#### 56. test_e2e_user_can_edit_existing_project
**Priority:** Critical
**Preconditions:**
- User is authenticated
- User has a project named "Original Name"
**Steps:**
1. Navigate to `/projects`
2. Find project card with "Original Name"
3. Click three-dot menu on that card
4. Click "Edit" option
5. Change name to "Updated Name"
6. Click "Save" button
**Success Criteria:**
- Edit modal opens with pre-populated data
- After save, modal closes
- Success toast appears
- Card now shows "Updated Name"
**Related User Story:** Edit project functionality

```typescript
test('user can edit existing project', async ({ authenticatedPage: page }) => {
  await page.goto('/projects');

  const card = page.locator('[data-testid="project-card"]').filter({ hasText: 'Original Name' });
  await card.getByRole('button', { name: /menu/i }).click();
  await page.getByRole('menuitem', { name: /edit/i }).click();

  await page.getByLabel(/name/i).clear();
  await page.getByLabel(/name/i).fill('Updated Name');
  await page.getByRole('button', { name: /save/i }).click();

  await expect(page.getByText(/updated/i)).toBeVisible();
  await expect(page.getByText('Updated Name')).toBeVisible();
});
```

#### 57. test_e2e_user_can_delete_project
**Priority:** High
**Preconditions:**
- User is authenticated
- User has a project named "To Delete"
**Steps:**
1. Navigate to `/projects`
2. Find project card with "To Delete"
3. Click three-dot menu
4. Click "Delete" option
5. Confirm deletion in dialog
**Success Criteria:**
- Confirmation dialog shows project name
- After confirm, dialog closes
- Success toast appears
- Project is removed from list
**Related User Story:** Delete project functionality

```typescript
test('user can delete project', async ({ authenticatedPage: page }) => {
  await page.goto('/projects');

  const card = page.locator('[data-testid="project-card"]').filter({ hasText: 'To Delete' });
  await card.getByRole('button', { name: /menu/i }).click();
  await page.getByRole('menuitem', { name: /delete/i }).click();

  await expect(page.getByText(/permanent/i)).toBeVisible();
  await page.getByRole('button', { name: /delete/i }).click();

  await expect(page.getByText(/deleted/i)).toBeVisible();
  await expect(page.getByText('To Delete')).not.toBeVisible();
});
```

#### 58. test_e2e_user_can_navigate_to_project_detail
**Priority:** High
**Preconditions:**
- User is authenticated
- User has a project named "Click Me"
**Steps:**
1. Navigate to `/projects`
2. Click on project card (not menu)
3. Wait for navigation
**Success Criteria:**
- URL changes to `/projects/[id]`
- Detail page shows project name
- Breadcrumb shows navigation path
**Related User Story:** "Click card opens project detail page"

```typescript
test('user can navigate to project detail', async ({ authenticatedPage: page }) => {
  await page.goto('/projects');

  await page.getByText('Click Me').click();

  await expect(page).toHaveURL(/\/projects\/[\w-]+/);
  await expect(page.getByRole('heading', { name: 'Click Me' })).toBeVisible();
});
```

#### 59. test_e2e_create_modal_validates_empty_name
**Priority:** High
**Preconditions:**
- User is authenticated
- Create modal is open
**Steps:**
1. Open create modal
2. Leave name empty
3. Fill description only
4. Click "Create"
**Success Criteria:**
- Form is not submitted
- Validation error appears under name field
- Modal remains open
**Related User Story:** Form validation

```typescript
test('create modal validates empty name', async ({ authenticatedPage: page }) => {
  await page.goto('/projects');
  await page.getByRole('button', { name: /new project/i }).click();

  await page.getByLabel(/description/i).fill('Some description');
  await page.getByRole('button', { name: /create/i }).click();

  await expect(page.getByText(/name.*required/i)).toBeVisible();
});
```

#### 60. test_e2e_empty_state_shows_when_no_projects
**Priority:** High
**Preconditions:**
- User is authenticated
- User has no projects (clean state)
**Steps:**
1. Navigate to `/projects`
2. Wait for page to load
**Success Criteria:**
- Empty state illustration is visible
- "No projects yet" text is displayed
- CTA button to create project is visible
**Related User Story:** Empty state handling

```typescript
test('empty state shows when no projects', async ({ authenticatedPage: page }) => {
  // Requires test user with no projects
  await page.goto('/projects');

  await expect(page.getByText(/no projects yet/i)).toBeVisible();
  await expect(page.getByRole('button', { name: /create.*project/i })).toBeVisible();
});
```

#### 61. test_e2e_cancel_button_closes_modal_without_saving
**Priority:** Medium
**Preconditions:**
- User is authenticated
- Create modal is open with data entered
**Steps:**
1. Open create modal
2. Fill in name: "Unsaved Project"
3. Click "Cancel" button
4. Reopen modal
**Success Criteria:**
- Modal closes on cancel
- No project is created
- Modal form is empty when reopened
**Related User Story:** Cancel functionality

```typescript
test('cancel button closes modal without saving', async ({ authenticatedPage: page }) => {
  await page.goto('/projects');
  await page.getByRole('button', { name: /new project/i }).click();

  await page.getByLabel(/name/i).fill('Unsaved Project');
  await page.getByRole('button', { name: /cancel/i }).click();

  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page.getByText('Unsaved Project')).not.toBeVisible();
});
```

#### 62. test_e2e_responsive_grid_layout
**Priority:** Medium
**Preconditions:**
- User is authenticated
- User has 4+ projects
**Steps:**
1. Navigate to `/projects`
2. Resize viewport to mobile (375px)
3. Verify 1 column layout
4. Resize to tablet (768px)
5. Verify 2 column layout
6. Resize to desktop (1280px)
7. Verify 3 column layout
**Success Criteria:**
- Grid adjusts columns based on viewport
- Cards maintain proper spacing
**Related User Story:** Responsive card grid

```typescript
test('responsive grid layout', async ({ authenticatedPage: page }) => {
  await page.goto('/projects');

  // Mobile
  await page.setViewportSize({ width: 375, height: 667 });
  // Verify single column

  // Tablet
  await page.setViewportSize({ width: 768, height: 1024 });
  // Verify two columns

  // Desktop
  await page.setViewportSize({ width: 1280, height: 800 });
  // Verify three columns
});
```

---

## Test Dependencies

### Execution Order Requirements

1. **Database/RLS tests** must pass before Service/Query tests
   - RLS policies must be verified before testing queries
   - Ensures data isolation is working correctly

2. **Service/Query tests** must pass before UI Component tests
   - Hooks must return correct data before testing UI rendering
   - Mutation behavior must be verified before testing forms

3. **UI Component tests** must pass before E2E tests
   - Components must render correctly in isolation
   - Individual interactions must work before testing flows

4. **Specific Dependencies:**
   - `test_useProjects_fetches_all_user_projects` before `test_ProjectListPage_renders_project_grid_with_data`
   - `test_useCreateProject_creates_project_successfully` before `test_CreateProjectModal_closes_on_successful_create`
   - `test_rls_user_can_delete_own_project` before `test_e2e_user_can_delete_project`

### Parallel Execution Groups

Tests within each layer can run in parallel:

- **Group 1 (RLS):** Tests 1-7 (parallel)
- **Group 2 (Service):** Tests 8-19 (parallel)
- **Group 3 (UI):** Tests 20-53 (parallel)
- **Group 4 (E2E):** Tests 54-62 (sequential - share browser state)

---

## Test Data Requirements

### Fixtures and Seeds

**Test User Accounts:**
```typescript
// e2e/fixtures/users.ts
export const TEST_USERS = {
  primary: {
    email: process.env.TEST_USER_EMAIL,
    password: process.env.TEST_USER_PASSWORD,
  },
  secondary: {
    email: process.env.TEST_USER_2_EMAIL,
    password: process.env.TEST_USER_2_PASSWORD,
  },
}
```

**Sample Projects:**
```typescript
// __tests__/fixtures/projects.ts
export const MOCK_PROJECTS = [
  {
    id: 'proj-001',
    name: 'Test Project 1',
    description: 'First test project description',
    owner_id: 'user-001',
    created_at: '2026-01-04T10:00:00Z',
    updated_at: '2026-01-04T10:00:00Z',
  },
  {
    id: 'proj-002',
    name: 'Very Long Project Name That Should Be Truncated In The Card View',
    description: 'This is a very long description that spans multiple lines and should be truncated at exactly two lines in the project card component to ensure consistent visual appearance.',
    owner_id: 'user-001',
    created_at: '2026-01-02T10:00:00Z',
    updated_at: '2026-01-03T15:30:00Z',
  },
]
```

**Mock Supabase Client:**
```typescript
// __tests__/mocks/supabase.ts
export const createMockSupabaseClient = (options = {}) => ({
  from: vi.fn(() => ({
    select: vi.fn().mockReturnThis(),
    insert: vi.fn().mockReturnThis(),
    update: vi.fn().mockReturnThis(),
    delete: vi.fn().mockReturnThis(),
    eq: vi.fn().mockReturnThis(),
    single: vi.fn(),
  })),
  auth: {
    getUser: vi.fn().mockResolvedValue({
      data: { user: { id: 'user-001', email: 'test@example.com' } },
      error: null,
    }),
  },
  ...options,
})
```

### E2E Test Database Seeding

For E2E tests, use Supabase seed file or API setup:

```sql
-- supabase/seed.sql (for test environment)
INSERT INTO auth.users (id, email) VALUES
  ('test-user-1', 'test@example.com');

INSERT INTO public.projects (id, name, description, owner_id) VALUES
  ('e2e-proj-1', 'Original Name', 'For edit tests', 'test-user-1'),
  ('e2e-proj-2', 'To Delete', 'For delete tests', 'test-user-1'),
  ('e2e-proj-3', 'Click Me', 'For navigation tests', 'test-user-1');
```

---

## Out of Scope

Tests explicitly NOT included in this plan:

1. **Performance/Load Testing**
   - Testing with 1000+ projects
   - API response time benchmarks
   - Requires dedicated performance sprint

2. **Cross-Browser Compatibility**
   - Safari, Firefox specific testing
   - Covered by Playwright multi-browser config in CI

3. **Accessibility Audit**
   - Full WCAG 2.1 compliance testing
   - Screen reader testing
   - Deferred to QA accessibility review

4. **Offline Functionality**
   - Service worker caching
   - Offline project viewing
   - Not in MVP scope

5. **Internationalization**
   - Multi-language support
   - RTL layout testing
   - Not in current scope

6. **Search/Filter Functionality**
   - Out of scope per spec.md

7. **Pagination**
   - Out of scope per spec.md (MVP assumes reasonable count)

---

## Appendix: Test File Structure

```
__tests__/
├── unit/
│   └── validations/
│       └── project.test.ts           # Zod schema tests
├── integration/
│   ├── hooks/
│   │   ├── useProjects.test.ts       # Tests 8-12
│   │   ├── useCreateProject.test.ts  # Tests 13-15
│   │   ├── useUpdateProject.test.ts  # Tests 16-17
│   │   └── useDeleteProject.test.ts  # Tests 18-19
│   └── components/
│       ├── ProjectListPage.test.tsx  # Tests 20-26
│       ├── ProjectCard.test.tsx      # Tests 27-33
│       ├── CreateProjectModal.test.tsx    # Tests 34-40
│       ├── EditProjectModal.test.tsx      # Tests 41-45
│       ├── DeleteConfirmationDialog.test.tsx  # Tests 46-50
│       └── ProjectDetailPage.test.tsx     # Tests 51-53
├── rls/
│   └── projects.rls.test.ts          # Tests 1-7 (requires Supabase test instance)
└── fixtures/
    ├── projects.ts
    └── users.ts

e2e/
├── dashboard/
│   └── projects.spec.ts              # Tests 54-62
└── fixtures/
    └── auth.ts
```
