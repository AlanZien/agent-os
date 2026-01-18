# Product Roadmap

## Phase 1: Core Foundation (MVP)

1. [x] **Database Schema** - Create Supabase tables for projects, features, tasks, tests with proper relationships and RLS policies `S` ✅

2. [x] **Authentication** - Implement user authentication with Supabase Auth including login, signup, and session management `S` ✅

3. [x] **Project Management** - CRUD operations for projects with list view, create modal, edit, and delete functionality `M` ✅

4. [x] **Feature Management** - CRUD operations for features within projects, including lifecycle phase tracking (raw-idea, shape, write, tasks, implement, verify) `M` ✅

5. [x] **Task Kanban Board** - Drag-and-drop Kanban board with 5 columns (Backlog, To Do, In Progress, In Review, Done) for managing tasks within sprints `M` ✅ *Sprint 1*

6. [x] **Task Details** - Full task editing with title, description, priority, tags, due date, and time estimates `S` ✅ *Sprint 1*

7. [x] **Test Tracking** - CRUD operations for tests within features, with status tracking (pending, passed, failed) `S` ✅ *Sprint 2*

8. [x] **Bug Tracking** - CRUD operations for bugs with severity, priority, status, and linking to features/tasks `M` ✅ *Sprint 2*

9. [x] **Dashboard Metrics** - Main dashboard showing project counts, task distribution by status, bug counts, and completion rates `M` ✅ *Sprint 2*

## Phase 2: Enhanced Tracking

10. [x] **Feature Progress Metrics** - Progress indicators per feature showing task completion percentage and test pass rate `S` ✅ *Sprint 2*

11. [x] **Project Progress Rollup** - Aggregate metrics from features to project level with visual progress bars `S` ✅ *Sprint 2*

12. [ ] **Velocity Charts** - Charts showing tasks completed over time per project and overall `M` *Sprint 4*

13. [ ] **Timeline View** - Calendar/Gantt view for visualizing tasks and features with due dates `L` *Sprint 4*

14. [ ] **Search and Filter** - Global search across projects, features, tasks with filters by status, priority, tags `M`

15. [ ] **Notifications** - In-app notifications for due dates, status changes, and blocked tasks `M` *Sprint 5*

## Phase 3: Integrations

16. [ ] **Agent-OS API Endpoints** - REST API endpoints to receive data from agent-os commands (/plan-product, /write-spec, /create-tasks, /plan-tests) `M` *Sprint 3* ⭐ PRIORITAIRE

17. [ ] **GitHub OAuth** - GitHub authentication for linking accounts `S` *Sprint 6*

18. [ ] **GitHub Task Linking** - Link tasks to GitHub branches and PRs with visual indicators `M` *Sprint 6*

19. [ ] **GitHub Auto-Sync** - Automatically update task status when linked PR is merged `M` *Sprint 6*

20. [ ] **Webhook Support** - Webhooks for external integrations and automation `S` *Sprint 6*

## Phase 4: Public Release

21. [ ] **Export Functionality** - Export projects/features/tasks to CSV and PDF reports `M` *Sprint 8*

22. [ ] **Public Documentation** - User documentation for agent-os community adoption `M` *Sprint 8*

23. [ ] **Production Deployment** - Deploy to Vercel with production Supabase instance `S` *Sprint 8*

24. [ ] **Onboarding Flow** - First-time user onboarding with guided tour `S` *Sprint 8*

25. [ ] **Settings Page** - User preferences, GitHub connection management, notification settings `S` *Sprint 8*

---

## Sprint Mapping

| Sprint | Dates | Items | Status |
|--------|-------|-------|--------|
| Sprint 0 | 02-08 jan | #1-4 (Setup) | ✅ Done |
| Sprint 1 | 08-14 jan | #5-6 (Kanban) | ✅ Done |
| Sprint 2 | 14-18 jan | #7-11 (Tests, Bugs, Metrics) | ✅ Done |
| Sprint 3 | 20 jan - 03 fév | #16 (Agent-OS API) | 🎯 Next |
| Sprint 4 | 03-17 fév | #12-13 (Charts, Timeline) | Planning |
| Sprint 5 | 17 fév - 03 mars | #15 (Notifications) | Planning |
| Sprint 6 | 03-17 mars | #17-20 (GitHub) | Planning |
| Sprint 7 | 17-31 mars | QA Pipeline | Planning |
| Sprint 8 | 31 mars - 14 avr | #21-25 (Release) | Planning |

---

> Notes
> - Order items by technical dependencies and product architecture
> - Each item represents an end-to-end (frontend + backend) functional and testable feature
> - Effort scale: XS (1 day), S (2-3 days), M (1 week), L (2 weeks), XL (3+ weeks)
> - Phase 1 establishes core entities and CRUD ✅ **COMPLETE**
> - Phase 2 adds metrics and enhanced UX (partially complete)
> - Phase 3 enables integrations with agent-os and GitHub
> - Phase 4 prepares for public release
> - Last sync: 2026-01-18
