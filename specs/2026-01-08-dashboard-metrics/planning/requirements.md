# Requirements - Dashboard Metrics

## Overview
Main dashboard showing project counts, task distribution by status, and completion rates.

## Decisions
- **Location**: Default landing page after login (`/dashboard`)
- **Scope**: All user's projects aggregated (no project selector for MVP)
- **Time Period**: All-time metrics (no time filters for MVP)
- **Charts**: Donut chart for task distribution
- **Bug Metrics**: Deferred (depends on Bug Tracking feature #8)

## Functional Requirements

### FR1: Project Metrics Cards
- Total Projects count
- Active Projects (projects with in-progress tasks)
- Completed Projects (all tasks done)
- Display as stat cards with icons

### FR2: Task Distribution Chart
- Donut/pie chart showing tasks by status
- Statuses: backlog, todo, in_progress, in_review, done
- Show count and percentage per status
- Color-coded by status

### FR3: Completion Rate
- Overall task completion percentage (done / total)
- Visual progress bar or percentage display
- Per-project mini-cards showing individual completion rates

### FR4: Recent Activity (Optional)
- List of recent task status changes
- Shows: task title, old status → new status, timestamp
- Limited to last 5-10 items

### FR5: Quick Actions
- "Create Project" button
- Links to projects list
- Empty state when no projects exist

## Data Queries

```sql
-- Project counts
SELECT
  COUNT(*) as total,
  COUNT(*) FILTER (WHERE EXISTS (
    SELECT 1 FROM tasks t
    JOIN sprints s ON t.sprint_id = s.id
    WHERE s.project_id = p.id AND t.status = 'in_progress'
  )) as active
FROM projects p WHERE owner_id = auth.uid();

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

## UI Components
- StatCard - metric display card with icon
- TaskDistributionChart - donut chart (recharts)
- CompletionProgress - percentage with progress bar
- ProjectCompletionList - per-project mini stats
- DashboardEmptyState - when no data

## Layout
```
┌─────────────────────────────────────────────────┐
│  Header: "Dashboard"                            │
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

## Out of Scope (MVP)
- Bug counts/metrics (Feature #8)
- Time period filters
- Velocity charts (Feature #12)
- Timeline view (Feature #13)
- Project selector/filter
- Export functionality

---
Created: 2026-01-08
