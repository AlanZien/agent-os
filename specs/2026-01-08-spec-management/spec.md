# Specification: Spec Management

## Goal

Enable users to manage specifications (specs) within projects, with CRUD operations and a visual phase stepper to track lifecycle progress through six development phases.

## User Stories

- As a user, I want to create and manage specs within a project so that I can organize my development work into discrete features
- As a user, I want to see a visual stepper showing the current phase of each spec so that I can track progress through the development lifecycle

## Specific Requirements

**Specs Table Database Schema**
- Create `specs` table with columns: id (UUID), project_id (UUID FK), title (TEXT), description (TEXT), phase (TEXT), due_date (DATE), created_at, updated_at
- Phase column uses CHECK constraint for values: 'raw-idea', 'shape', 'write', 'tasks', 'implement', 'verify'
- Default phase is 'raw-idea'
- ON DELETE CASCADE from projects table
- Create indexes on project_id and phase columns
- Enable RLS with policies matching project ownership pattern

**Spec List Section on Project Detail Page**
- Replace placeholder content in ProjectDetailPage with specs list section
- Display specs as cards in a vertical list within the project detail page
- Show empty state with illustration and "Create First Spec" CTA when no specs exist
- Sort specs by created_at descending (newest first)
- Loading state shows skeleton cards while fetching

**SpecCard Component**
- Display spec title (H4, truncated at 1 line) and description (truncated at 2 lines)
- Include horizontal SpecStepper component showing all 6 phases with current phase highlighted
- Display due date in relative format (e.g., "Due in 3 days") or "No due date"
- Context menu (three-dot icon) with Edit and Delete actions
- Card is clickable to open SpecDetailPanel

**SpecStepper Component**
- Horizontal stepper with 6 phases: raw-idea, shape, write, tasks, implement, verify
- Each phase shown as a small circle or pill with abbreviated label
- Completed phases use primary color fill, current phase has ring/outline emphasis
- Future phases use muted/gray styling
- Responsive: on mobile, show abbreviated labels or icons only
- Clickable steps to advance/revert phase (when in SpecDetailPanel)

**CreateSpecModal Component**
- Modal triggered by "New Spec" button in project detail page header
- Form fields: title (required, max 100 chars), description (optional, max 1000 chars), due_date (optional date picker)
- Initial phase automatically set to 'raw-idea' (not shown in form)
- Auto-link to current project via project_id from URL params
- Use react-hook-form with zod validation following existing project pattern
- Success toast and close modal on creation

**EditSpecModal Component**
- Access via context menu on SpecCard
- Pre-populate form with existing spec data (title, description, due_date)
- Phase change handled separately via SpecStepper in SpecDetailPanel, not in edit form
- Same validation rules as create modal
- Optimistic update pattern for better UX

**DeleteSpecConfirmation Dialog**
- Confirmation dialog triggered from SpecCard context menu
- Display spec title in warning message
- Hard delete from database (no soft delete for MVP)
- Invalidate specs cache and show success toast after deletion

**SpecDetailPanel Component**
- Slide-over panel or modal showing full spec information
- Large SpecStepper at top with clickable phases for manual transitions
- Display full title, description, due date
- Phase transition buttons: "Advance to [next phase]" and "Revert to [previous phase]"
- "Edit" and "Delete" action buttons in panel header

**React Query Hooks for Specs**
- useSpecs(projectId): fetch all specs for a project, ordered by created_at desc
- useSpec(specId): fetch single spec by ID
- useCreateSpec(): mutation to create spec with project_id
- useUpdateSpec(): mutation to update spec fields
- useUpdateSpecPhase(): dedicated mutation for phase transitions
- useDeleteSpec(): mutation to delete spec
- Query key pattern: ['specs', projectId] for list, ['specs', 'detail', specId] for single

**TypeScript Types and Validation**
- Create Spec interface in types/spec.ts matching database schema
- Create zod schemas in lib/validations/spec.ts for create/update operations
- Phase type as union literal: 'raw-idea' | 'shape' | 'write' | 'tasks' | 'implement' | 'verify'
- Export SPEC_PHASES constant array for iteration in SpecStepper

## Visual Design

Follow the design system guidelines:
- Dark theme with surface background (#171717) for SpecCard
- Primary teal (#10B981) for completed/current phase indicators
- Muted gray (#737373) for future phases in stepper
- 8px border radius for cards, 12px for modals/panels
- Lucide React icons: FileText for spec, ChevronRight for stepper, Calendar for due date

## Existing Code to Leverage

| File | Purpose |
|------|---------|
| components/features/projects/ProjectDetailPage.tsx | Target for specs list integration |
| components/features/projects/CreateProjectModal.tsx | Modal pattern to follow |
| components/features/projects/ProjectCard.tsx | Card pattern with context menu |
| hooks/useProjects.ts | React Query hook pattern |
| hooks/useCreateProject.ts | Mutation pattern |
| types/project.ts | TypeScript types pattern |
| lib/validations/project.ts | Zod validation pattern |
| supabase/migrations/00001_create_initial_tables.sql | Database migration pattern |

## Out of Scope

- Priority field for specs
- Tags or labels system
- Assignee field
- Task linking within specs (separate feature)
- Bulk operations
- Import/export functionality
- Spec templates
- Search or filter functionality
- Drag-and-drop reordering
- Phase transition history
