# Task Breakdown: Dashboard Metrics

## Overview
Total Tasks: 25
Tech Stack: Next.js 15, React Query, Recharts, Supabase, TypeScript

## Task List

### Data Layer

#### Task Group 1: Dashboard Metrics Hook
**Dependencies:** None

- [ ] 1.1 Create TypeScript types (`types/dashboard.ts`)
- [ ] 1.2 Create useDashboardMetrics hook (`hooks/useDashboardMetrics.ts`)
- [ ] 1.3 Implement Supabase aggregation queries

### UI Components

#### Task Group 2: StatCard Component
**Dependencies:** None

- [ ] 2.1 Create StatCard component (`components/features/dashboard/StatCard.tsx`)
- [ ] 2.2 Implement skeleton loading state

#### Task Group 3: TaskDistributionChart Component
**Dependencies:** None

- [ ] 3.1 Create TaskDistributionChart component
- [ ] 3.2 Configure Recharts donut chart
- [ ] 3.3 Implement status color mapping
- [ ] 3.4 Add chart skeleton

#### Task Group 4: ProjectCompletionList Component
**Dependencies:** None

- [ ] 4.1 Create ProjectCompletionList component
- [ ] 4.2 Implement progress bars
- [ ] 4.3 Add project links
- [ ] 4.4 Create list skeleton

#### Task Group 5: Dashboard Page Assembly
**Dependencies:** Task Groups 1-4

- [ ] 5.1 Create DashboardPage component (`components/features/dashboard/DashboardPage.tsx`)
- [ ] 5.2 Implement layout (4 stat cards + 2-column below)
- [ ] 5.3 Implement empty state
- [ ] 5.4 Implement error state
- [ ] 5.5 Create barrel export (`components/features/dashboard/index.ts`)

### Route Integration

#### Task Group 6: Route Updates
**Dependencies:** Task Group 5

- [ ] 6.1 Update dashboard route (`app/(dashboard)/dashboard/page.tsx`)
- [ ] 6.2 Remove redirect to /kanban
- [ ] 6.3 Verify as default landing page after login

## Files to Create

- `types/dashboard.ts`
- `hooks/useDashboardMetrics.ts`
- `components/features/dashboard/StatCard.tsx`
- `components/features/dashboard/TaskDistributionChart.tsx`
- `components/features/dashboard/ProjectCompletionList.tsx`
- `components/features/dashboard/DashboardPage.tsx`
- `components/features/dashboard/index.ts`

## Files to Modify

- `app/(dashboard)/dashboard/page.tsx` (replace redirect with DashboardPage)

## Status Color Mapping

```typescript
const STATUS_COLORS: Record<string, string> = {
  backlog: '#6B7280',
  todo: '#6B7280',
  in_progress: '#3B82F6',
  in_review: '#8B5CF6',
  done: '#10B981',
};
```

---
Created: 2026-01-08
