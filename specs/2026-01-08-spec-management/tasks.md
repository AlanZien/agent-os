# Task Breakdown: Spec Management

## Overview
Total Tasks: 42

This feature enables users to manage specifications (specs) within projects, with CRUD operations and a visual phase stepper to track lifecycle progress through six development phases: raw-idea, shape, write, tasks, implement, verify.

## Task List

### Database Layer

#### Task Group 1: Database Schema and Migration
**Dependencies:** None

- [ ] 1.1 Create specs table migration (`supabase/migrations/00002_create_specs_table.sql`)
- [ ] 1.2 Add indexes on project_id and phase columns
- [ ] 1.3 Add updated_at trigger
- [ ] 1.4 Enable RLS with project ownership policies
- [ ] 1.5 Grant permissions to authenticated users

### TypeScript Types and Validation

#### Task Group 2: Type Definitions and Zod Schemas
**Dependencies:** Task Group 1

- [ ] 2.1 Create Spec interface in `types/spec.ts`
- [ ] 2.2 Define SpecPhase type and SPEC_PHASES constant
- [ ] 2.3 Create Zod schemas in `lib/validations/spec.ts`

### React Query Hooks

#### Task Group 3: Data Fetching and Mutations
**Dependencies:** Task Groups 1, 2

- [ ] 3.1 Create useSpecs hook (`hooks/useSpecs.ts`)
- [ ] 3.2 Create useSpec hook (single spec)
- [ ] 3.3 Create useCreateSpec hook
- [ ] 3.4 Create useUpdateSpec hook
- [ ] 3.5 Create useUpdateSpecPhase hook
- [ ] 3.6 Create useDeleteSpec hook

### UI Components

#### Task Group 4: SpecStepper Component
**Dependencies:** Task Group 2

- [ ] 4.1 Create SpecStepper component (`components/features/specs/SpecStepper.tsx`)
- [ ] 4.2 Implement phase styling (completed/current/future)
- [ ] 4.3 Add responsive behavior
- [ ] 4.4 Implement clickable mode

#### Task Group 5: SpecCard Component
**Dependencies:** Task Groups 3, 4

- [ ] 5.1 Create SpecCard component
- [ ] 5.2 Integrate SpecStepper
- [ ] 5.3 Add due date display
- [ ] 5.4 Implement context menu (Edit/Delete)

#### Task Group 6: CreateSpecModal Component
**Dependencies:** Task Groups 2, 3

- [ ] 6.1 Create CreateSpecModal component
- [ ] 6.2 Implement form with react-hook-form
- [ ] 6.3 Handle form submission

#### Task Group 7: EditSpecModal Component
**Dependencies:** Task Group 6

- [ ] 7.1 Create EditSpecModal component
- [ ] 7.2 Pre-populate form data
- [ ] 7.3 Handle update submission

#### Task Group 8: DeleteSpecConfirmation Dialog
**Dependencies:** Task Group 3

- [ ] 8.1 Create DeleteSpecConfirmation component
- [ ] 8.2 Implement delete action

#### Task Group 9: SpecDetailPanel Component
**Dependencies:** Task Groups 3, 4, 7, 8

- [ ] 9.1 Create SpecDetailPanel component
- [ ] 9.2 Display spec information
- [ ] 9.3 Implement large SpecStepper with clickable phases
- [ ] 9.4 Add phase transition buttons
- [ ] 9.5 Add header action buttons (Edit/Delete)

### Integration

#### Task Group 10: Project Detail Page Integration
**Dependencies:** Task Groups 3, 5, 6, 9

- [ ] 10.1 Update ProjectDetailPage with specs section
- [ ] 10.2 Create SpecsList component
- [ ] 10.3 Implement empty state
- [ ] 10.4 Add loading state
- [ ] 10.5 Wire up modals and panel

## Files to Create

- `supabase/migrations/00002_create_specs_table.sql`
- `types/spec.ts`
- `lib/validations/spec.ts`
- `hooks/useSpecs.ts`
- `hooks/useCreateSpec.ts`
- `hooks/useUpdateSpec.ts`
- `hooks/useDeleteSpec.ts`
- `components/features/specs/SpecStepper.tsx`
- `components/features/specs/SpecCard.tsx`
- `components/features/specs/SpecsList.tsx`
- `components/features/specs/CreateSpecModal.tsx`
- `components/features/specs/EditSpecModal.tsx`
- `components/features/specs/DeleteSpecConfirmation.tsx`
- `components/features/specs/SpecDetailPanel.tsx`
- `components/features/specs/index.ts`

## Files to Modify

- `components/features/projects/ProjectDetailPage.tsx` (add specs section)
- `hooks/index.ts` (add spec hooks exports)

---
Created: 2026-01-08
