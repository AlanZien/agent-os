# Specification: Dashboard Metrics

## Goal

Provide users with an at-a-glance overview of their project portfolio health through aggregated metrics, task distribution charts, and completion rates on the main dashboard landing page.

## User Stories

- As a user, I want to see my project and task statistics on the dashboard so that I can quickly assess my portfolio status
- As a user, I want to visualize task distribution by status so that I can identify bottlenecks in my workflow

## Specific Requirements

**Dashboard Page Route**
- Replace current redirect in `/dashboard` with actual metrics dashboard
- Set as default landing page after login
- Page header displays "Dashboard" title
- Include "Create Project" quick action button in header

**Project Metrics Stat Cards**
- Display 4 stat cards in a horizontal row (responsive: 2x2 on mobile, 4 in row on desktop)
- Card 1: Total Projects - count of all user's projects
- Card 2: Active Projects - projects with at least one task in `in_progress` status
- Card 3: Completed Projects - projects where all tasks are in `done` status
- Card 4: Completion Rate - percentage of done tasks vs total tasks (rounded to integer)
- Each card shows an icon (Lucide), label, and value
- Use design system surface color (#171717) for card background

**Task Distribution Donut Chart**
- Display using Recharts library (already in dependencies)
- Show tasks grouped by status: backlog, todo, in_progress, in_review, done
- Use Kanban status colors from design system for each segment
- Display count and percentage for each status in legend or tooltip
- Center text shows total task count
- Responsive sizing: 250px on mobile, 300px on desktop

**Project Completion List**
- Display per-project completion rates in a scrollable list
- Each row shows: project name, progress bar, percentage
- Progress bar uses primary color (#10B981) for filled portion
- Sort by completion percentage descending (most complete first)
- Limit to 5 projects initially (no pagination for MVP)
- Link each project name to `/projects/[id]`

**Data Fetching with React Query**
- Create `useDashboardMetrics` hook for aggregated data
- Query key: `['dashboard', 'metrics']`
- Stale time: 30 seconds (consistent with projects)
- Single query fetching all metrics in one request for efficiency
- Handle loading and error states at page level

**Empty State Handling**
- Show empty state when user has no projects
- Display illustration with "No data yet" message
- Include CTA button linking to create project modal
- Reuse empty state pattern from ProjectListPage

**Loading State**
- Show skeleton placeholders for all metric cards
- Show skeleton for chart area
- Show skeleton rows for project completion list
- Use consistent animation with existing skeleton patterns

**SQL Aggregation Queries**
```sql
-- Project counts
SELECT COUNT(*) as total FROM projects WHERE owner_id = auth.uid();

-- Task distribution
SELECT status, COUNT(*) as count
FROM tasks t
JOIN sprints s ON t.sprint_id = s.id
JOIN projects p ON s.project_id = p.id
WHERE p.owner_id = auth.uid()
GROUP BY status;

-- Completion rate
SELECT
  COUNT(*) FILTER (WHERE status = 'done') as completed,
  COUNT(*) as total
FROM tasks t
JOIN sprints s ON t.sprint_id = s.id
JOIN projects p ON s.project_id = p.id
WHERE p.owner_id = auth.uid();
```

## Visual Design

**Layout Structure**
```
┌─────────────────────────────────────────────────┐
│  Header: "Dashboard"              [+ Project]   │
├─────────────────────────────────────────────────┤
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐        │
│  │Total │  │Active│  │Done  │  │Rate  │        │
│  │  12  │  │   5  │  │   4  │  │ 67%  │        │
│  └──────┘  └──────┘  └──────┘  └──────┘        │
├─────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────────────┐ │
│  │                │  │ Project Completion     │ │
│  │  Donut Chart   │  │ - Project A: 80%      │ │
│  │  (Tasks by     │  │ - Project B: 45%      │ │
│  │   status)      │  │ - Project C: 100%     │ │
│  │                │  │                        │ │
│  └────────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

**Stat Card Design**
- Icon in top-left (20px, muted color)
- Large value below (H2 size, 24px, semibold)
- Label at bottom (small text, secondary color)
- Subtle border (#2E2E2E) around card

**Chart Design**
- Donut chart with inner radius 60% of outer radius
- Status colors: backlog (#6B7280), todo (#6B7280), in_progress (#3B82F6), in_review (#8B5CF6), done (#10B981)
- Legend below chart on mobile, beside chart on desktop

## Existing Code to Leverage

| File | Purpose |
|------|---------|
| hooks/useProjects.ts | React Query pattern |
| components/features/projects/ProjectListPage.tsx | Page layout, empty/loading states |
| components/ui/Button.tsx | Button variants |
| lib/supabase/client.ts | Supabase client |
| supabase/migrations/00001_create_initial_tables.sql | Schema reference |

## Out of Scope

- Bug metrics (depends on Feature #8)
- Time period filters (all-time only for MVP)
- Velocity charts (Feature #12)
- Timeline view (Feature #13)
- Project selector/filter
- Export functionality
- Real-time updates
- Pagination for project list
