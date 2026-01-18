# Spec Requirements: Agent-OS API Endpoints

## Initial Description
Create REST API endpoints for AgentOS-Tracker to receive sync data from the Agent-OS orchestrator. This enables the CLI-based Agent-OS workflow to automatically sync project, feature, task, and test data to the tracker application.

## Requirements Discussion

### First Round Questions

**Q1:** What authentication mechanism should be used for the API endpoints?
**Answer:** API Key authentication via `Authorization: Bearer <AGENT_OS_API_KEY>` header

**Q2:** What endpoints are needed and what data will they receive?
**Answer:** 6 endpoints total:
- `POST /api/agent-os/projects` - Create/upsert project (from /plan-product)
- `POST /api/agent-os/features` - Create/upsert feature + update phase (from /write-spec)
- `POST /api/agent-os/tasks` - Bulk create tasks (from /create-tasks)
- `PATCH /api/agent-os/tasks` - Bulk update task status (from /implement-tasks)
- `POST /api/agent-os/tests` - Bulk create tests (from /plan-tests)
- `PATCH /api/agent-os/tests` - Update test status (passed/failed)

**Q3:** How should Agent-OS entities map to AgentOS-Tracker entities?
**Answer:**
- Projects = Agent-OS Projects from /plan-product
- Features = Agent-OS Specs from /write-spec (auto-update phase: write->tasks->implement->verify)
- Tasks = Tasks from /create-tasks
- Tests = Test plans from /plan-tests

**Q4:** What identifier should be used for syncing/upserting entities?
**Answer:** Use `external_id` column (spec folder path like `2026-01-18-agent-os-api-endpoints`)

**Q5:** How should sprint association work for new entities?
**Answer:** Auto-assign to currently active sprint, fallback to first "planning" sprint

**Q6:** Should bulk operations be transactional?
**Answer:** Yes, accept array, all-or-nothing transaction

**Q7:** What response format is expected?
**Answer:** Return full created/updated entity

**Q8:** What error handling approach should be used?
**Answer:** Detailed error codes + request ID tracking. No rate limiting needed (internal use only)

**Q9:** What is explicitly out of scope?
**Answer:**
- Webhooks callbacks to Agent-OS
- WebSocket real-time updates
- UI admin interface for API key management

**Q10:** What database changes are needed?
**Answer:** Add `external_id TEXT UNIQUE` to projects and features tables (migration required)

### Existing Code to Reference

**Similar Features Identified:**
- Feature: React Query hooks - Path: `hooks/` (useProjects, useFeatures, useTasks, useTests)
- Feature: Supabase client - Path: `lib/supabase/`
- Feature: TypeScript types - Path: `types/`
- Components to potentially reuse: Existing CRUD patterns in hooks
- Backend logic to reference: Supabase client configuration and auth patterns

### Follow-up Questions
No follow-up questions needed - requirements were comprehensively answered.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
Not applicable - this is a backend API feature with no UI components.

## Requirements Summary

### Functional Requirements
- API key authentication middleware for all /api/agent-os/* routes
- 6 REST API endpoints for CRUD operations on projects, features, tasks, and tests
- Upsert logic based on `external_id` for projects and features
- Bulk create/update operations for tasks and tests
- Automatic sprint assignment for new entities
- Automatic phase progression for features (write -> tasks -> implement -> verify)
- Transactional bulk operations (all-or-nothing)
- Detailed error responses with request ID tracking

### Reusability Opportunities
- Existing React Query hooks patterns for data fetching
- Supabase client configuration in lib/supabase/
- TypeScript types from types/ directory
- Existing entity structures (Project, Feature, Task, Test)

### Scope Boundaries
**In Scope:**
- API key authentication middleware
- 6 API endpoints (2 POST projects/features, 2 POST bulk create, 2 PATCH bulk update)
- Database migration for external_id column
- Request validation and error handling
- Sprint auto-assignment logic
- Feature phase auto-update logic

**Out of Scope:**
- Webhooks/callbacks to Agent-OS CLI
- WebSocket real-time updates
- UI for API key management
- Rate limiting
- API documentation UI (Swagger/OpenAPI)

### Technical Considerations
- Next.js API Routes (App Router)
- Supabase as database backend
- API key stored in environment variable
- Transactions via Supabase RPC or multi-statement queries
- Request ID generation for error tracking

---

## Complexity Analysis

### Elements Identified
| Element | Count | Points |
|---------|-------|--------|
| UI Components | 0 | 0 |
| API Endpoints | 6 | 12 |
| Database Changes | 2 | 6 |
| External Integrations | 0 | 0 |
| User Scenarios | 8 | 4 |
| State Management | 0 | 0 |
| Auth/Security | 1 | 3 |

**Total Complexity Score: 25**

### Scoring Breakdown
- **API Endpoints (6 x 2 = 12):**
  - POST /api/agent-os/projects
  - POST /api/agent-os/features
  - POST /api/agent-os/tasks
  - PATCH /api/agent-os/tasks
  - POST /api/agent-os/tests
  - PATCH /api/agent-os/tests

- **Database Changes (2 x 3 = 6):**
  - Add external_id to projects table
  - Add external_id to features table

- **User Scenarios (8 x 0.5 = 4):**
  - Create new project via API
  - Update existing project via API
  - Create new feature via API
  - Update feature phase via API
  - Bulk create tasks
  - Bulk update task status
  - Bulk create tests
  - Update test status

- **Auth/Security (1 x 3 = 3):**
  - API key authentication middleware

### Recommended Track
COMPLEX

**Recommended Workflow:**
1. /verify-spec - Review and validate the technical specification
2. /write-spec - Create detailed technical specification
3. /plan-tests - Define test scenarios for API endpoints
4. /create-tasks - Break down into implementation tasks
5. /orchestrate-tasks - Coordinate parallel implementation
6. /verify - Final verification and integration testing
