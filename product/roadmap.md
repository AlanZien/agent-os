# Product Roadmap

## Phase 1: Core Foundation (MVP)

1. [x] **Database Schema** - Create Supabase tables for projects, features, tasks, tests with proper relationships and RLS policies `S` ✅

2. [x] **Authentication** - Implement user authentication with Supabase Auth including login, signup, and session management `S` ✅

3. [x] **Project Management** - CRUD operations for projects with list view, create modal, edit, and delete functionality `M` ✅

4. [x] **Feature Management** - CRUD operations for features within projects, including lifecycle phase tracking (raw-idea, shape, write, tasks, implement, verify) `M` ✅

5. [ ] **Task Kanban Board** - Drag-and-drop Kanban board with 5 columns (Backlog, To Do, In Progress, In Review, Done) for managing tasks within sprints `M`

6. [ ] **Task Details** - Full task editing with title, description, priority, tags, due date, and time estimates `S`

7. [ ] **Test Tracking** - CRUD operations for tests within features, with status tracking (pending, passed, failed) `S`

8. [ ] **Bug Tracking** - CRUD operations for bugs with severity, priority, status, and linking to features/tasks `M`

9. [x] **Dashboard Metrics** - Main dashboard showing project counts, task distribution by status, bug counts, and completion rates `M` ✅

## Phase 2: Enhanced Tracking

10. [ ] **Feature Progress Metrics** - Progress indicators per feature showing task completion percentage and test pass rate `S`

11. [ ] **Project Progress Rollup** - Aggregate metrics from features to project level with visual progress bars `S`

12. [ ] **Velocity Charts** - Charts showing tasks completed over time per project and overall `M`

13. [ ] **Timeline View** - Calendar/Gantt view for visualizing tasks and features with due dates `L`

14. [ ] **Search and Filter** - Global search across projects, features, tasks with filters by status, priority, tags `M`

15. [ ] **Notifications** - In-app notifications for due dates, status changes, and blocked tasks `M`

## Phase 3: Integrations

16. [ ] **Agent-OS API Endpoints** - REST API endpoints to receive data from agent-os commands (/plan-product, /write-spec, /create-tasks, /plan-tests) `M`

17. [ ] **GitHub OAuth** - GitHub authentication for linking accounts `S`

18. [ ] **GitHub Task Linking** - Link tasks to GitHub branches and PRs with visual indicators `M`

19. [ ] **GitHub Auto-Sync** - Automatically update task status when linked PR is merged `M`

20. [ ] **Webhook Support** - Webhooks for external integrations and automation `S`

## Phase 4: Public Release

21. [ ] **Export Functionality** - Export projects/features/tasks to CSV and PDF reports `M`

22. [ ] **Public Documentation** - User documentation for agent-os community adoption `M`

23. [ ] **Production Deployment** - Deploy to Vercel with production Supabase instance `S`

24. [ ] **Onboarding Flow** - First-time user onboarding with guided tour `S`

25. [ ] **Settings Page** - User preferences, GitHub connection management, notification settings `S`

---

> Notes
> - Order items by technical dependencies and product architecture
> - Each item represents an end-to-end (frontend + backend) functional and testable feature
> - Effort scale: XS (1 day), S (2-3 days), M (1 week), L (2 weeks), XL (3+ weeks)
> - Phase 1 establishes core entities and CRUD
> - Phase 2 adds metrics and enhanced UX
> - Phase 3 enables integrations with agent-os and GitHub
> - Phase 4 prepares for public release
