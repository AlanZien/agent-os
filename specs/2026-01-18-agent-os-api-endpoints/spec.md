# Specification: Agent-OS API Endpoints

## Goal
Create 6 REST API endpoints to enable the Agent-OS CLI orchestrator to sync project, feature, task, and test data to the AgentOS-Tracker application, using API key authentication and upsert behavior based on external_id.

## User Stories
- As the Agent-OS orchestrator, I want to sync project and feature data to the tracker so that teams can visualize development progress in real-time
- As the Agent-OS orchestrator, I want to bulk create tasks and tests so that implementation plans are immediately visible in the tracker
- As the Agent-OS orchestrator, I want to update task and test statuses so that progress is tracked automatically without manual intervention

## Specific Requirements

**API Key Authentication Middleware**
- Create middleware that validates `Authorization: Bearer <AGENT_OS_API_KEY>` header
- API key stored in `AGENT_OS_API_KEY` environment variable
- Return 401 Unauthorized with error code if key is missing or invalid
- Apply middleware to all `/api/agent-os/*` routes

**POST /api/agent-os/projects Endpoint**
- Accept project data with `external_id` (spec folder path like `2026-01-18-project-name`)
- Upsert behavior: create if external_id not found, update if exists
- Required fields: `external_id`, `name`; optional: `description`
- Return full project entity on success

**POST /api/agent-os/features Endpoint**
- Accept feature data with `external_id` (spec folder path)
- Upsert behavior based on `external_id` match
- Required fields: `external_id`, `project_id`, `title`; optional: `description`, `phase`
- Auto-update phase based on Agent-OS workflow stage (write -> tasks -> implement -> verify)
- Return full feature entity on success

**POST /api/agent-os/tasks Endpoint**
- Accept array of tasks for bulk creation
- Required fields per task: `title`, `feature_id`; optional: `description`, `status`, `priority`, `estimated_hours`, `task_group`, `parent_task_id`
- Auto-assign to active sprint, fallback to first "planning" sprint
- Transactional: all tasks created or none (rollback on error)
- Return array of created task entities

**PATCH /api/agent-os/tasks Endpoint**
- Accept array of task updates with `id` or `external_id` identifier
- Updateable fields: `status`, `logged_hours`, `remaining_hours`
- Transactional: all updates applied or none
- Return array of updated task entities

**POST /api/agent-os/tests Endpoint**
- Accept array of tests for bulk creation
- Required fields per test: `name`, `feature_id`; optional: `description`, `status`
- Default status: `pending`
- Transactional: all tests created or none
- Return array of created test entities

**PATCH /api/agent-os/tests Endpoint**
- Accept array of test updates with `id` identifier
- Updateable fields: `status` (pending, passed, failed)
- Transactional: all updates applied or none
- Return array of updated test entities

**Database Migration for external_id**
- Add `external_id TEXT UNIQUE` column to `projects` table
- Add `external_id TEXT UNIQUE` column to `features` table
- Create index on external_id for efficient upsert lookups

**Error Handling and Response Format**
- Generate unique request ID for each API call (UUID)
- Return structured error responses: `{ error: { code, message, request_id } }`
- Error codes: `AUTH_MISSING`, `AUTH_INVALID`, `VALIDATION_ERROR`, `NOT_FOUND`, `TRANSACTION_FAILED`
- Success responses: `{ data: <entity or array>, request_id }`

**Sprint Auto-Assignment Logic**
- Query for sprint with `status = 'active'` in the same project
- Fallback to first sprint with `status = 'planning'` ordered by start_date
- If no sprint found, return validation error

## Existing Code to Leverage

**lib/supabase/server.ts - Server-side Supabase client**
- Use `createClient()` for API route database access
- Already configured for server-side usage with cookies handling
- Adapt for API routes by creating a variant that doesn't require cookies for API key auth

**types/feature.ts - Feature type definitions**
- Reuse `Feature`, `FeaturePhase`, `FEATURE_PHASES` types
- Extend `Feature` interface to include optional `external_id` field
- Reference phase progression logic: raw-idea -> shape -> write -> tasks -> implement -> verify

**types/task.ts - Task type definitions**
- Reuse `Task`, `TaskStatus`, `TaskPriority`, `CreateTaskInput` types
- Reference `TASK_STATUSES` and `TASK_PRIORITIES` for validation
- Adapt `CreateTaskInput` for bulk API input

**types/test.ts - Test type definitions**
- Reuse `Test`, `TestStatus`, `CreateTestInput`, `UpdateTestInput` types
- Reference `TEST_STATUSES` for validation
- Use same entity structure for API responses

**hooks/useSprints.ts - Sprint query logic**
- Reference sprint status values: 'planning', 'active', 'completed'
- Adapt query logic for finding active/planning sprint for auto-assignment

## Out of Scope
- Webhooks or callbacks from Tracker to Agent-OS CLI
- WebSocket real-time update notifications
- UI admin interface for API key management or rotation
- Rate limiting (internal use only)
- OpenAPI/Swagger documentation generation
- Authentication via OAuth or user sessions (API key only)
- DELETE endpoints for any entities
- Bulk update for projects or features (single upsert only)
- File attachments or binary data handling
- Audit logging or change history tracking
