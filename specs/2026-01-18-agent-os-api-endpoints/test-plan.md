# Test Plan: Agent-OS API Endpoints

## Metadata
- **Feature**: Agent-OS API Endpoints for Tracker Synchronization
- **Spec**: agent-os/specs/2026-01-18-agent-os-api-endpoints/spec.md
- **Requirements**: agent-os/specs/2026-01-18-agent-os-api-endpoints/planning/requirements.md
- **Created**: 2026-01-18
- **Status**: Planning Complete

## Test Summary

| Layer | Critical | High | Medium | Low | Total |
|-------|----------|------|--------|-----|-------|
| Database | 4 | 4 | 2 | 0 | 10 |
| API | 28 | 18 | 12 | 4 | 62 |
| Integration | 4 | 2 | 0 | 0 | 6 |
| **Total** | **36** | **24** | **14** | **4** | **78** |

**Coverage Targets:**
- Critical paths: 100%
- High priority: 100%
- Medium priority: 80%
- Low priority: Deferred to future iterations

---

## Database Layer

### Migration: external_id Columns (10 tests)

#### 1. test_projects_table_has_external_id_column
**Priority:** Critical
**Given:** Database migration has been applied
**When:** Query the projects table schema
**Then:** Column `external_id` exists with type TEXT and UNIQUE constraint
**Related Requirement:** spec.md "Database Migration for external_id"

#### 2. test_features_table_has_external_id_column
**Priority:** Critical
**Given:** Database migration has been applied
**When:** Query the features table schema
**Then:** Column `external_id` exists with type TEXT and UNIQUE constraint
**Related Requirement:** spec.md "Database Migration for external_id"

#### 3. test_projects_external_id_unique_constraint
**Priority:** Critical
**Given:** Project exists with external_id "2026-01-18-project-alpha"
**When:** Attempt to insert another project with same external_id
**Then:** Database raises unique constraint violation error
**Related Requirement:** spec.md "Database Migration for external_id"

#### 4. test_features_external_id_unique_constraint
**Priority:** Critical
**Given:** Feature exists with external_id "2026-01-18-feature-beta"
**When:** Attempt to insert another feature with same external_id
**Then:** Database raises unique constraint violation error
**Related Requirement:** spec.md "Database Migration for external_id"

#### 5. test_projects_external_id_index_exists
**Priority:** High
**Given:** Database migration has been applied
**When:** Query for indexes on projects table
**Then:** Index on external_id column exists for efficient lookups
**Related Requirement:** spec.md "Create index on external_id for efficient upsert lookups"

#### 6. test_features_external_id_index_exists
**Priority:** High
**Given:** Database migration has been applied
**When:** Query for indexes on features table
**Then:** Index on external_id column exists for efficient lookups
**Related Requirement:** spec.md "Create index on external_id for efficient upsert lookups"

#### 7. test_projects_external_id_allows_null
**Priority:** High
**Given:** Database migration has been applied
**When:** Insert a project without external_id
**Then:** Project is created successfully with external_id as NULL
**Related Requirement:** spec.md "Database Migration for external_id" (backward compatibility)

#### 8. test_features_external_id_allows_null
**Priority:** High
**Given:** Database migration has been applied
**When:** Insert a feature without external_id
**Then:** Feature is created successfully with external_id as NULL
**Related Requirement:** spec.md "Database Migration for external_id" (backward compatibility)

#### 9. test_multiple_null_external_ids_allowed_projects
**Priority:** Medium
**Given:** Database migration has been applied
**When:** Insert multiple projects without external_id (NULL values)
**Then:** All projects are created successfully (NULL does not violate UNIQUE)
**Related Requirement:** spec.md "Database Migration for external_id" (backward compatibility)

#### 10. test_multiple_null_external_ids_allowed_features
**Priority:** Medium
**Given:** Database migration has been applied
**When:** Insert multiple features without external_id (NULL values)
**Then:** All features are created successfully (NULL does not violate UNIQUE)
**Related Requirement:** spec.md "Database Migration for external_id" (backward compatibility)

---

## API Layer

### Authentication Middleware (8 tests)

#### 11. test_auth_missing_authorization_header_returns_401
**Priority:** Critical
**Given:** Request has no Authorization header
**When:** POST /api/agent-os/projects with valid body
**Then:**
- Status: 401 Unauthorized
- Body: `{ "error": { "code": "AUTH_MISSING", "message": "Authorization header required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "API Key Authentication Middleware"

#### 12. test_auth_invalid_bearer_format_returns_401
**Priority:** Critical
**Given:** Authorization header is "Basic abc123" (not Bearer)
**When:** POST /api/agent-os/projects with valid body
**Then:**
- Status: 401 Unauthorized
- Body: `{ "error": { "code": "AUTH_INVALID", "message": "Invalid authorization format. Use Bearer token", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "API Key Authentication Middleware"

#### 13. test_auth_invalid_api_key_returns_401
**Priority:** Critical
**Given:** Authorization header is "Bearer wrong-api-key"
**When:** POST /api/agent-os/projects with valid body
**Then:**
- Status: 401 Unauthorized
- Body: `{ "error": { "code": "AUTH_INVALID", "message": "Invalid API key", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "API Key Authentication Middleware"

#### 14. test_auth_valid_api_key_allows_request
**Priority:** Critical
**Given:** Authorization header is "Bearer <valid-AGENT_OS_API_KEY>"
**When:** POST /api/agent-os/projects with valid body
**Then:** Request proceeds to endpoint handler (not blocked by auth)
**Related Requirement:** spec.md "API Key Authentication Middleware"

#### 15. test_auth_empty_bearer_token_returns_401
**Priority:** High
**Given:** Authorization header is "Bearer " (empty token)
**When:** POST /api/agent-os/projects with valid body
**Then:**
- Status: 401 Unauthorized
- Body: `{ "error": { "code": "AUTH_MISSING", "message": "API key required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "API Key Authentication Middleware"

#### 16. test_auth_middleware_applied_to_all_endpoints
**Priority:** High
**Given:** No Authorization header provided
**When:** Call each of the 6 endpoints (projects POST, features POST, tasks POST/PATCH, tests POST/PATCH)
**Then:** All 6 endpoints return 401 Unauthorized with AUTH_MISSING code
**Related Requirement:** spec.md "Apply middleware to all /api/agent-os/* routes"

#### 17. test_auth_request_id_unique_per_request
**Priority:** Medium
**Given:** Two identical requests without auth
**When:** POST /api/agent-os/projects twice
**Then:** Each response has a different request_id (UUID format)
**Related Requirement:** spec.md "Generate unique request ID for each API call"

#### 18. test_auth_response_includes_request_id_on_success
**Priority:** Medium
**Given:** Valid Authorization header
**When:** POST /api/agent-os/projects with valid body
**Then:** Response body includes `request_id` field with valid UUID
**Related Requirement:** spec.md "Success responses: { data: <entity>, request_id }"

---

### POST /api/agent-os/projects Endpoint (10 tests)

#### 19. test_projects_create_new_with_required_fields
**Priority:** Critical
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-new-project", "name": "New Project" }`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 201 Created
- Body: `{ "data": { "id": "<uuid>", "external_id": "2026-01-18-new-project", "name": "New Project", "description": null, ... }, "request_id": "<uuid>" }`
- Project exists in database with matching external_id
**Related Requirement:** spec.md "POST /api/agent-os/projects Endpoint"

#### 20. test_projects_create_new_with_all_fields
**Priority:** High
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-full-project", "name": "Full Project", "description": "A detailed description" }`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 201 Created
- Body includes all provided fields in the data object
- Description field is populated
**Related Requirement:** spec.md "POST /api/agent-os/projects Endpoint"

#### 21. test_projects_upsert_updates_existing
**Priority:** Critical
**Given:**
- Valid Authorization header
- Project exists with external_id "2026-01-18-existing-project" and name "Old Name"
- Request body: `{ "external_id": "2026-01-18-existing-project", "name": "Updated Name" }`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 200 OK
- Body: data.name equals "Updated Name"
- Only one project exists with that external_id
- updated_at timestamp is newer than before
**Related Requirement:** spec.md "Upsert behavior: create if external_id not found, update if exists"

#### 22. test_projects_upsert_partial_update
**Priority:** High
**Given:**
- Valid Authorization header
- Project exists with external_id "2026-01-18-project", name "Name", description "Old desc"
- Request body: `{ "external_id": "2026-01-18-project", "name": "Name", "description": "New desc" }`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 200 OK
- Description is updated to "New desc"
- Name remains unchanged
**Related Requirement:** spec.md "Upsert behavior"

#### 23. test_projects_missing_external_id_returns_400
**Priority:** Critical
**Given:**
- Valid Authorization header
- Request body: `{ "name": "Project Without ID" }`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "external_id is required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields: external_id, name"

#### 24. test_projects_missing_name_returns_400
**Priority:** Critical
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-project" }`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "name is required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields: external_id, name"

#### 25. test_projects_empty_name_returns_400
**Priority:** High
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-project", "name": "" }`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "name cannot be empty", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields: external_id, name"

#### 26. test_projects_invalid_json_returns_400
**Priority:** Medium
**Given:**
- Valid Authorization header
- Request body: `invalid json string`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "Invalid JSON body", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Error Handling and Response Format"

#### 27. test_projects_extra_fields_ignored
**Priority:** Medium
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-project", "name": "Name", "unknown_field": "value" }`
**When:** POST /api/agent-os/projects
**Then:**
- Status: 201 Created
- Project is created without the unknown_field
**Related Requirement:** spec.md (implicit - API should be lenient with extra fields)

#### 28. test_projects_returns_full_entity
**Priority:** High
**Given:**
- Valid Authorization header
- Request body with required fields
**When:** POST /api/agent-os/projects
**Then:**
- Response data includes: id, external_id, name, description, owner_id, created_at, updated_at
**Related Requirement:** spec.md "Return full project entity on success"

---

### POST /api/agent-os/features Endpoint (12 tests)

#### 29. test_features_create_new_with_required_fields
**Priority:** Critical
**Given:**
- Valid Authorization header
- Valid project_id exists
- Request body: `{ "external_id": "2026-01-18-new-feature", "project_id": "<project_id>", "title": "New Feature" }`
**When:** POST /api/agent-os/features
**Then:**
- Status: 201 Created
- Body: `{ "data": { "id": "<uuid>", "external_id": "2026-01-18-new-feature", "title": "New Feature", "phase": "raw-idea", ... }, "request_id": "<uuid>" }`
**Related Requirement:** spec.md "POST /api/agent-os/features Endpoint"

#### 30. test_features_create_with_phase
**Priority:** High
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-feature", "project_id": "<id>", "title": "Feature", "phase": "write" }`
**When:** POST /api/agent-os/features
**Then:**
- Status: 201 Created
- Feature created with phase "write"
**Related Requirement:** spec.md "optional: description, phase"

#### 31. test_features_upsert_updates_existing
**Priority:** Critical
**Given:**
- Feature exists with external_id "2026-01-18-existing" and title "Old Title"
- Request body: `{ "external_id": "2026-01-18-existing", "project_id": "<id>", "title": "New Title" }`
**When:** POST /api/agent-os/features
**Then:**
- Status: 200 OK
- Body: data.title equals "New Title"
- Only one feature exists with that external_id
**Related Requirement:** spec.md "Upsert behavior based on external_id match"

#### 32. test_features_auto_update_phase_write
**Priority:** Critical
**Given:**
- Feature exists with external_id and phase "raw-idea"
- Request body includes phase: "write"
**When:** POST /api/agent-os/features
**Then:**
- Status: 200 OK
- Phase is updated to "write"
**Related Requirement:** spec.md "Auto-update phase based on Agent-OS workflow stage"

#### 33. test_features_auto_update_phase_progression
**Priority:** High
**Given:**
- Feature exists with phase "write"
- Request body includes phase: "tasks"
**When:** POST /api/agent-os/features
**Then:**
- Status: 200 OK
- Phase is updated to "tasks"
**Related Requirement:** spec.md "Phase progression: write -> tasks -> implement -> verify"

#### 34. test_features_missing_external_id_returns_400
**Priority:** Critical
**Given:**
- Valid Authorization header
- Request body: `{ "project_id": "<id>", "title": "Feature" }`
**When:** POST /api/agent-os/features
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "external_id is required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields: external_id, project_id, title"

#### 35. test_features_missing_project_id_returns_400
**Priority:** Critical
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-feature", "title": "Feature" }`
**When:** POST /api/agent-os/features
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "project_id is required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields: external_id, project_id, title"

#### 36. test_features_missing_title_returns_400
**Priority:** Critical
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-feature", "project_id": "<id>" }`
**When:** POST /api/agent-os/features
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "title is required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields: external_id, project_id, title"

#### 37. test_features_invalid_project_id_returns_404
**Priority:** High
**Given:**
- Valid Authorization header
- Request body: `{ "external_id": "2026-01-18-feature", "project_id": "non-existent-uuid", "title": "Feature" }`
**When:** POST /api/agent-os/features
**Then:**
- Status: 404 Not Found
- Body: `{ "error": { "code": "NOT_FOUND", "message": "Project not found", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Error codes: NOT_FOUND"

#### 38. test_features_invalid_phase_returns_400
**Priority:** Medium
**Given:**
- Valid Authorization header
- Request body includes phase: "invalid-phase"
**When:** POST /api/agent-os/features
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "Invalid phase. Must be one of: raw-idea, shape, write, tasks, implement, verify", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md (implicit - validate against FEATURE_PHASES)

#### 39. test_features_create_with_description
**Priority:** Medium
**Given:**
- Valid Authorization header
- Request body includes description field
**When:** POST /api/agent-os/features
**Then:**
- Status: 201 Created
- Feature includes the provided description
**Related Requirement:** spec.md "optional: description"

#### 40. test_features_returns_full_entity
**Priority:** High
**Given:**
- Valid Authorization header and valid request
**When:** POST /api/agent-os/features
**Then:**
- Response data includes: id, external_id, project_id, title, description, phase, due_date, created_at, updated_at
**Related Requirement:** spec.md "Return full feature entity on success"

---

### POST /api/agent-os/tasks Endpoint (12 tests)

#### 41. test_tasks_bulk_create_single_task
**Priority:** Critical
**Given:**
- Valid Authorization header
- Active sprint exists in project
- Request body: `{ "tasks": [{ "title": "Task 1", "feature_id": "<id>" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 201 Created
- Body: `{ "data": [{ "id": "<uuid>", "title": "Task 1", "sprint_id": "<active_sprint_id>", ... }], "request_id": "<uuid>" }`
- Task exists in database
**Related Requirement:** spec.md "POST /api/agent-os/tasks Endpoint"

#### 42. test_tasks_bulk_create_multiple_tasks
**Priority:** Critical
**Given:**
- Valid Authorization header
- Request body: `{ "tasks": [{ "title": "Task 1", "feature_id": "<id>" }, { "title": "Task 2", "feature_id": "<id>" }, { "title": "Task 3", "feature_id": "<id>" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 201 Created
- Body: data array contains 3 task objects
- All 3 tasks exist in database
**Related Requirement:** spec.md "Accept array of tasks for bulk creation"

#### 43. test_tasks_auto_assign_active_sprint
**Priority:** Critical
**Given:**
- Project has active sprint (status: 'active')
- Project has planning sprint (status: 'planning')
- Request body: `{ "tasks": [{ "title": "Task", "feature_id": "<id>" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Task is assigned to the active sprint (not planning sprint)
**Related Requirement:** spec.md "Auto-assign to active sprint"

#### 44. test_tasks_fallback_to_planning_sprint
**Priority:** Critical
**Given:**
- Project has no active sprint
- Project has planning sprint ordered first by start_date
- Request body: `{ "tasks": [{ "title": "Task", "feature_id": "<id>" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Task is assigned to the first planning sprint
**Related Requirement:** spec.md "fallback to first 'planning' sprint"

#### 45. test_tasks_no_sprint_returns_validation_error
**Priority:** Critical
**Given:**
- Project has no active or planning sprints
- Request body with valid task
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "No active or planning sprint found for project", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "If no sprint found, return validation error"

#### 46. test_tasks_transaction_rollback_on_error
**Priority:** Critical
**Given:**
- Valid Authorization header
- Request body: `{ "tasks": [{ "title": "Valid Task", "feature_id": "<id>" }, { "title": "Task", "feature_id": "invalid-uuid" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 400 or 500
- No tasks are created in database (all rolled back)
**Related Requirement:** spec.md "Transactional: all tasks created or none (rollback on error)"

#### 47. test_tasks_with_optional_fields
**Priority:** High
**Given:**
- Valid Authorization header
- Request body: `{ "tasks": [{ "title": "Task", "feature_id": "<id>", "description": "Desc", "status": "todo", "priority": "high", "estimated_hours": 4, "task_group": "Backend" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 201 Created
- Task includes all optional fields
**Related Requirement:** spec.md "optional: description, status, priority, estimated_hours, task_group, parent_task_id"

#### 48. test_tasks_with_parent_task_id
**Priority:** High
**Given:**
- Parent task exists with id
- Request body: `{ "tasks": [{ "title": "Subtask", "feature_id": "<id>", "parent_task_id": "<parent_id>" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 201 Created
- Subtask has parent_task_id set correctly
**Related Requirement:** spec.md "optional: parent_task_id"

#### 49. test_tasks_missing_title_returns_400
**Priority:** High
**Given:**
- Valid Authorization header
- Request body: `{ "tasks": [{ "feature_id": "<id>" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "title is required for all tasks", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields per task: title, feature_id"

#### 50. test_tasks_missing_feature_id_returns_400
**Priority:** High
**Given:**
- Valid Authorization header
- Request body: `{ "tasks": [{ "title": "Task" }] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "feature_id is required for all tasks", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields per task: title, feature_id"

#### 51. test_tasks_empty_array_returns_400
**Priority:** Medium
**Given:**
- Valid Authorization header
- Request body: `{ "tasks": [] }`
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "At least one task is required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md (implicit - empty array is not useful)

#### 52. test_tasks_invalid_status_returns_400
**Priority:** Medium
**Given:**
- Valid Authorization header
- Request body includes task with status: "invalid-status"
**When:** POST /api/agent-os/tasks
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "Invalid status. Must be one of: backlog, todo, in_progress, in_review, done", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md (implicit - validate against TASK_STATUSES)

---

### PATCH /api/agent-os/tasks Endpoint (10 tests)

#### 53. test_tasks_update_by_id
**Priority:** Critical
**Given:**
- Task exists with known id
- Request body: `{ "tasks": [{ "id": "<task_id>", "status": "done" }] }`
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 200 OK
- Task status is updated to "done"
**Related Requirement:** spec.md "PATCH /api/agent-os/tasks Endpoint"

#### 54. test_tasks_update_by_external_id
**Priority:** Critical
**Given:**
- Task exists linked to feature with external_id
- Request body: `{ "tasks": [{ "external_id": "<feature_external_id>", "task_title": "Task 1", "status": "in_progress" }] }`
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 200 OK
- Task matching criteria is updated
**Related Requirement:** spec.md "Accept array of task updates with id or external_id identifier"

#### 55. test_tasks_update_multiple
**Priority:** Critical
**Given:**
- Multiple tasks exist
- Request body updates 3 tasks
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 200 OK
- All 3 tasks are updated
- Response includes all 3 updated entities
**Related Requirement:** spec.md "Accept array of task updates"

#### 56. test_tasks_update_logged_hours
**Priority:** High
**Given:**
- Task exists with logged_hours: 0
- Request body: `{ "tasks": [{ "id": "<id>", "logged_hours": 4.5 }] }`
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 200 OK
- Task logged_hours is now 4.5
**Related Requirement:** spec.md "Updateable fields: status, logged_hours, remaining_hours"

#### 57. test_tasks_update_remaining_hours
**Priority:** High
**Given:**
- Task exists with remaining_hours: 8
- Request body: `{ "tasks": [{ "id": "<id>", "remaining_hours": 2 }] }`
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 200 OK
- Task remaining_hours is now 2
**Related Requirement:** spec.md "Updateable fields: status, logged_hours, remaining_hours"

#### 58. test_tasks_update_transaction_rollback
**Priority:** Critical
**Given:**
- Two tasks exist (A and B)
- Request body: `{ "tasks": [{ "id": "<id_A>", "status": "done" }, { "id": "non-existent-id", "status": "done" }] }`
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 404 Not Found
- Task A status is NOT changed (rolled back)
**Related Requirement:** spec.md "Transactional: all updates applied or none"

#### 59. test_tasks_update_not_found_returns_404
**Priority:** High
**Given:**
- Request body references non-existent task id
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 404 Not Found
- Body: `{ "error": { "code": "NOT_FOUND", "message": "Task not found: <id>", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Error codes: NOT_FOUND"

#### 60. test_tasks_update_missing_identifier_returns_400
**Priority:** High
**Given:**
- Request body: `{ "tasks": [{ "status": "done" }] }` (no id or external_id)
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "Each task update requires id or external_id", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Accept array of task updates with id or external_id identifier"

#### 61. test_tasks_update_empty_array_returns_400
**Priority:** Medium
**Given:**
- Request body: `{ "tasks": [] }`
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "At least one task update is required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md (implicit)

#### 62. test_tasks_update_invalid_status_returns_400
**Priority:** Medium
**Given:**
- Request body includes invalid status value
**When:** PATCH /api/agent-os/tasks
**Then:**
- Status: 400 Bad Request
- Body includes VALIDATION_ERROR for invalid status
**Related Requirement:** spec.md (implicit - validate against TASK_STATUSES)

---

### POST /api/agent-os/tests Endpoint (10 tests)

#### 63. test_tests_bulk_create_single
**Priority:** Critical
**Given:**
- Valid Authorization header
- Feature exists
- Request body: `{ "tests": [{ "name": "Test Case 1", "feature_id": "<id>" }] }`
**When:** POST /api/agent-os/tests
**Then:**
- Status: 201 Created
- Body: `{ "data": [{ "id": "<uuid>", "name": "Test Case 1", "status": "pending", ... }], "request_id": "<uuid>" }`
**Related Requirement:** spec.md "POST /api/agent-os/tests Endpoint"

#### 64. test_tests_bulk_create_multiple
**Priority:** Critical
**Given:**
- Request body: `{ "tests": [{ "name": "Test 1", "feature_id": "<id>" }, { "name": "Test 2", "feature_id": "<id>" }] }`
**When:** POST /api/agent-os/tests
**Then:**
- Status: 201 Created
- Body: data array contains 2 test objects
**Related Requirement:** spec.md "Accept array of tests for bulk creation"

#### 65. test_tests_default_status_pending
**Priority:** Critical
**Given:**
- Request body without status field
**When:** POST /api/agent-os/tests
**Then:**
- Created test has status: "pending"
**Related Requirement:** spec.md "Default status: pending"

#### 66. test_tests_transaction_rollback
**Priority:** Critical
**Given:**
- Request body: `{ "tests": [{ "name": "Valid", "feature_id": "<id>" }, { "name": "Invalid", "feature_id": "non-existent" }] }`
**When:** POST /api/agent-os/tests
**Then:**
- No tests are created (transaction rolled back)
**Related Requirement:** spec.md "Transactional: all tests created or none"

#### 67. test_tests_with_description
**Priority:** High
**Given:**
- Request body includes description
**When:** POST /api/agent-os/tests
**Then:**
- Created test includes description
**Related Requirement:** spec.md "optional: description, status"

#### 68. test_tests_with_explicit_status
**Priority:** High
**Given:**
- Request body: `{ "tests": [{ "name": "Test", "feature_id": "<id>", "status": "passed" }] }`
**When:** POST /api/agent-os/tests
**Then:**
- Created test has status: "passed"
**Related Requirement:** spec.md "optional: status"

#### 69. test_tests_missing_name_returns_400
**Priority:** High
**Given:**
- Request body: `{ "tests": [{ "feature_id": "<id>" }] }`
**When:** POST /api/agent-os/tests
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "name is required for all tests", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields per test: name, feature_id"

#### 70. test_tests_missing_feature_id_returns_400
**Priority:** High
**Given:**
- Request body: `{ "tests": [{ "name": "Test" }] }`
**When:** POST /api/agent-os/tests
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "feature_id is required for all tests", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Required fields per test: name, feature_id"

#### 71. test_tests_empty_array_returns_400
**Priority:** Medium
**Given:**
- Request body: `{ "tests": [] }`
**When:** POST /api/agent-os/tests
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "At least one test is required", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md (implicit)

#### 72. test_tests_invalid_status_returns_400
**Priority:** Medium
**Given:**
- Request body includes status: "invalid"
**When:** POST /api/agent-os/tests
**Then:**
- Status: 400 Bad Request
- Body includes VALIDATION_ERROR for invalid status
**Related Requirement:** spec.md (implicit - validate against TEST_STATUSES)

---

### PATCH /api/agent-os/tests Endpoint (8 tests)

#### 73. test_tests_update_status_to_passed
**Priority:** Critical
**Given:**
- Test exists with status: "pending"
- Request body: `{ "tests": [{ "id": "<id>", "status": "passed" }] }`
**When:** PATCH /api/agent-os/tests
**Then:**
- Status: 200 OK
- Test status is now "passed"
**Related Requirement:** spec.md "PATCH /api/agent-os/tests Endpoint"

#### 74. test_tests_update_status_to_failed
**Priority:** Critical
**Given:**
- Test exists with status: "pending"
- Request body: `{ "tests": [{ "id": "<id>", "status": "failed" }] }`
**When:** PATCH /api/agent-os/tests
**Then:**
- Status: 200 OK
- Test status is now "failed"
**Related Requirement:** spec.md "Updateable fields: status (pending, passed, failed)"

#### 75. test_tests_update_multiple
**Priority:** Critical
**Given:**
- Multiple tests exist
- Request body updates 3 tests
**When:** PATCH /api/agent-os/tests
**Then:**
- Status: 200 OK
- All 3 tests are updated
**Related Requirement:** spec.md "Accept array of test updates"

#### 76. test_tests_update_transaction_rollback
**Priority:** Critical
**Given:**
- Two tests exist (A and B)
- Request body: `{ "tests": [{ "id": "<id_A>", "status": "passed" }, { "id": "non-existent", "status": "passed" }] }`
**When:** PATCH /api/agent-os/tests
**Then:**
- Test A status is NOT changed (rolled back)
**Related Requirement:** spec.md "Transactional: all updates applied or none"

#### 77. test_tests_update_not_found_returns_404
**Priority:** High
**Given:**
- Request body references non-existent test id
**When:** PATCH /api/agent-os/tests
**Then:**
- Status: 404 Not Found
- Body: `{ "error": { "code": "NOT_FOUND", "message": "Test not found: <id>", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Error codes: NOT_FOUND"

#### 78. test_tests_update_missing_id_returns_400
**Priority:** High
**Given:**
- Request body: `{ "tests": [{ "status": "passed" }] }` (no id)
**When:** PATCH /api/agent-os/tests
**Then:**
- Status: 400 Bad Request
- Body: `{ "error": { "code": "VALIDATION_ERROR", "message": "id is required for each test update", "request_id": "<uuid>" } }`
**Related Requirement:** spec.md "Accept array of test updates with id identifier"

#### 79. test_tests_update_empty_array_returns_400
**Priority:** Medium
**Given:**
- Request body: `{ "tests": [] }`
**When:** PATCH /api/agent-os/tests
**Then:**
- Status: 400 Bad Request
**Related Requirement:** spec.md (implicit)

#### 80. test_tests_update_invalid_status_returns_400
**Priority:** Medium
**Given:**
- Request body includes status: "invalid-status"
**When:** PATCH /api/agent-os/tests
**Then:**
- Status: 400 Bad Request
- Body includes VALIDATION_ERROR
**Related Requirement:** spec.md (implicit - validate against TEST_STATUSES)

---

## Integration Tests

### End-to-End Workflow (6 tests)

#### 81. test_full_workflow_project_feature_tasks_tests
**Priority:** Critical
**Given:**
- Valid Authorization header
- No existing data for external_id "2026-01-18-integration-test"
**When:**
1. POST /api/agent-os/projects - Create project
2. POST /api/agent-os/features - Create feature with project_id
3. POST /api/agent-os/tasks - Create tasks with feature_id
4. POST /api/agent-os/tests - Create tests with feature_id
5. PATCH /api/agent-os/tasks - Update task statuses to done
6. PATCH /api/agent-os/tests - Update test statuses to passed
**Then:**
- All entities are created and linked correctly
- All updates are applied
- Feature phase can be verified via database
**Related Requirement:** spec.md "User Stories"

#### 82. test_upsert_idempotency
**Priority:** Critical
**Given:**
- Project and feature created via API
**When:**
- POST /api/agent-os/projects with same external_id 3 times
- POST /api/agent-os/features with same external_id 3 times
**Then:**
- Only 1 project and 1 feature exist in database
- No errors on repeated calls
**Related Requirement:** spec.md "Upsert behavior"

#### 83. test_feature_phase_auto_progression
**Priority:** Critical
**Given:**
- Feature created with phase "raw-idea"
**When:**
1. POST /api/agent-os/features with phase: "write"
2. POST /api/agent-os/features with phase: "tasks"
3. POST /api/agent-os/features with phase: "implement"
4. POST /api/agent-os/features with phase: "verify"
**Then:**
- Each upsert updates the phase correctly
- Phase progression follows: raw-idea -> write -> tasks -> implement -> verify
**Related Requirement:** spec.md "Auto-update phase based on Agent-OS workflow stage"

#### 84. test_sprint_auto_assignment_priority
**Priority:** Critical
**Given:**
- Project with one active sprint and two planning sprints
**When:**
- Create tasks via API
**Then:**
- All tasks are assigned to the active sprint
**Related Requirement:** spec.md "Sprint Auto-Assignment Logic"

#### 85. test_concurrent_bulk_operations
**Priority:** High
**Given:**
- Valid project, feature, and sprint setup
**When:**
- Simultaneously POST 50 tasks in a single request
**Then:**
- All 50 tasks are created successfully
- No race conditions or duplicates
**Related Requirement:** spec.md "Accept array of tasks for bulk creation"

#### 86. test_request_id_tracking_across_errors
**Priority:** High
**Given:**
- Invalid request that will fail
**When:**
- Make request and capture request_id from error response
**Then:**
- request_id is a valid UUID
- request_id can be used for debugging/logging
**Related Requirement:** spec.md "Generate unique request ID for each API call"

---

## Test Dependencies

1. **Database migration tests** must pass before API tests (external_id columns required)
2. **Authentication tests** (11-18) should pass before endpoint tests
3. **Project endpoint tests** should pass before feature tests (project_id dependency)
4. **Feature endpoint tests** should pass before task/test tests (feature_id dependency)
5. **POST tests** should pass before PATCH tests (entities must exist)
6. **Integration tests** run last after all unit/API tests pass

---

## Test Data Requirements

### Test Fixtures Needed

1. **Test Users/API Keys:**
   - Valid AGENT_OS_API_KEY in environment
   - Invalid API key for negative tests

2. **Project Data:**
   - Project with external_id for upsert tests
   - Project without external_id for backward compatibility

3. **Feature Data:**
   - Features in various phases (raw-idea, write, tasks, implement, verify)
   - Features linked to test project

4. **Sprint Data:**
   - Active sprint (status: 'active')
   - Planning sprint (status: 'planning')
   - Completed sprint (status: 'completed')
   - Project with no sprints for error case

5. **Task Data:**
   - Parent tasks for subtask tests
   - Tasks in various statuses
   - Tasks with logged_hours and remaining_hours

6. **Test Data:**
   - Tests in pending, passed, failed statuses

### Database Seeding

```sql
-- Test project with external_id
INSERT INTO projects (id, name, external_id, owner_id)
VALUES ('test-project-id', 'Test Project', '2026-01-18-test-project', 'owner-id');

-- Test sprints
INSERT INTO sprints (id, project_id, name, status, start_date, end_date)
VALUES
  ('active-sprint-id', 'test-project-id', 'Active Sprint', 'active', '2026-01-01', '2026-01-14'),
  ('planning-sprint-id', 'test-project-id', 'Planning Sprint', 'planning', '2026-01-15', '2026-01-28');

-- Test feature
INSERT INTO features (id, project_id, title, external_id, phase)
VALUES ('test-feature-id', 'test-project-id', 'Test Feature', '2026-01-18-test-feature', 'raw-idea');
```

---

## Out of Scope

The following tests are explicitly NOT included in this plan:

1. **Performance/Load Testing:**
   - Stress testing with 1000+ concurrent requests
   - Response time benchmarking
   - Database connection pool limits

2. **Rate Limiting Tests:**
   - Not implemented per spec (internal use only)

3. **UI Tests:**
   - No UI components in this feature

4. **Webhook/Callback Tests:**
   - Out of scope per spec

5. **WebSocket Tests:**
   - Out of scope per spec

6. **API Key Rotation Tests:**
   - No admin UI per spec

7. **Audit Logging Tests:**
   - Out of scope per spec

---

## Test Implementation Notes

### Recommended Test Framework

Based on the tech stack (Next.js):
- **Vitest** or **Jest** for API route testing
- **MSW** (Mock Service Worker) for mocking external services if needed
- **Supertest** for HTTP request testing

### Test File Structure

```
__tests__/
  api/
    agent-os/
      auth.test.ts           # Tests 11-18
      projects.test.ts       # Tests 19-28
      features.test.ts       # Tests 29-40
      tasks-create.test.ts   # Tests 41-52
      tasks-update.test.ts   # Tests 53-62
      tests-create.test.ts   # Tests 63-72
      tests-update.test.ts   # Tests 73-80
      integration.test.ts    # Tests 81-86
  db/
    migrations.test.ts       # Tests 1-10
```

### Environment Setup

```env
# .env.test
AGENT_OS_API_KEY=test-api-key-for-testing
SUPABASE_URL=http://localhost:54321
SUPABASE_SERVICE_KEY=test-service-key
```
