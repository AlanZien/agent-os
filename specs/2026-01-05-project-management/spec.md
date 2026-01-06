# Specification: Project Management

## Goal

Enable users to manage their projects with full CRUD operations, providing a card-based list view with modals for creating, editing, and deleting projects.

## User Stories

- As a user, I want to view all my projects in a grid layout so that I can quickly see and access my work
- As a user, I want to create a new project with a name and description so that I can organize my tasks

## Specific Requirements

**Project List Page**
- Display projects in a responsive card grid (1 col mobile, 2 cols tablet, 3 cols desktop)
- Grid uses 16px gap between cards
- Page header includes title "Projects" and "New Project" button
- Loading state shows skeleton cards while fetching
- Empty state displays illustration with "No projects yet" message and CTA button
- Error state shows error message with retry button

**Project Card Component**
- Card displays project name (H4, truncated at 1 line)
- Card displays description (body text, truncated at 2 lines)
- Card displays owner name or email
- Card displays creation date in relative format (e.g., "2 days ago")
- Card is clickable and navigates to `/projects/[id]` on click
- Card shows subtle hover effect (border color change to border-strong)

**Create Project Modal**
- Trigger via "New Project" button in page header
- Form fields: name (required, max 100 chars), description (optional, max 500 chars)
- Primary "Create" button and secondary "Cancel" button
- Form validation with inline error messages using zod schema
- Loading state on submit button while creating
- Close modal and refresh list on successful creation
- Display toast notification on success/error

**Edit Project Modal**
- Access via context menu (three-dot icon) on project card
- Pre-populate form with existing project data
- Same form structure as create modal
- Primary "Save" button and secondary "Cancel" button
- Optimistic update pattern for better UX
- Display toast notification on success/error

**Delete Project Confirmation**
- Trigger via context menu on project card
- Confirmation dialog with project name displayed
- Warning text explaining deletion is permanent
- Destructive "Delete" button and secondary "Cancel" button
- Hard delete from database (no soft delete)
- Refresh list and show success toast after deletion

**Project Detail Page (Placeholder)**
- Route: `/projects/[id]`
- Display project name and description
- Placeholder content for future specs/tasks section
- Breadcrumb navigation back to projects list
- This is a minimal placeholder; full implementation is out of scope

**Data Fetching with React Query**
- Use `@tanstack/react-query` for all data operations
- Query key pattern: `['projects']` for list, `['projects', id]` for single
- Invalidate queries after mutations for cache consistency
- Configure stale time of 30 seconds for project list
- Handle error boundaries at page level

**API Integration**
- All database operations via Supabase client directly (no API routes needed)
- Server-side initial fetch in page.tsx using server Supabase client
- Client-side mutations using browser Supabase client
- RLS policies handle authorization automatically

## Visual Design

No visual mockups were provided. Follow the design system guidelines:
- Dark theme with surface background for cards (#171717)
- Primary teal accent (#10B981) for buttons and hover states
- 8px border radius for cards, 12px for modals
- Lucide React icons for UI elements
- Inter font family throughout

## Existing Code to Leverage

**Button Component (components/ui/Button.tsx)**
- Reusable button with variants: primary, secondary, ghost, outline
- Supports isLoading state with spinner animation
- Use for all modal actions and page header CTA

**Supabase Client Setup (lib/supabase/)**
- `client.ts` for browser-side operations (mutations)
- `server.ts` for server-side operations (initial data fetch)
- Pattern established for cookie-based session handling

**Dashboard Layout (app/(dashboard)/layout.tsx)**
- Projects page already scaffolded at `app/(dashboard)/projects/page.tsx`
- Sidebar navigation includes Projects link
- Layout provides consistent structure with sidebar

**AuthProvider Pattern (components/providers/AuthProvider.tsx)**
- Context pattern for accessing user data
- Use `useAuth()` hook to get current user for owner display
- Pattern can be replicated for QueryClientProvider

**Database Schema (supabase/migrations/)**
- `projects` table exists with: id, name, description, owner_id, created_at, updated_at
- RLS policies configured for user-based access control
- No migration needed; use existing schema

## Out of Scope

- Member/team management for projects
- Project statistics or metrics dashboard
- Search functionality for projects
- Filter or sort functionality
- Project archiving or soft delete
- Pagination (initial MVP assumes reasonable project count)
- Project settings or configuration
- Project sharing or collaboration features
- Bulk operations (multi-select, bulk delete)
- Project templates or duplication
