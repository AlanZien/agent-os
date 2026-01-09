# Requirements - Spec Management

## Overview
CRUD operations for specs within projects, including lifecycle phase tracking.

## Decisions
- **UI Location**: Specs displayed within project detail page (hierarchical navigation)
- **Phase Display**: Horizontal stepper showing all phases with current highlighted
- **Phase Transitions**: Manual only (user clicks to advance)
- **Fields**: Minimal - title, description, phase, due_date, created_at, updated_at

## Functional Requirements

### FR1: Spec List View
- Display specs as cards/rows within project detail page
- Show: title, current phase (stepper), due date, progress indicator
- Filter by phase (optional)
- Sort by created_at desc (default)

### FR2: Create Spec
- Modal form triggered from project page
- Fields: title (required), description (optional), due_date (optional)
- Initial phase: "raw-idea"
- Auto-link to current project

### FR3: Edit Spec
- Edit modal or inline editing
- Editable: title, description, due_date
- Phase change via dedicated stepper UI (not form field)

### FR4: Delete Spec
- Confirmation dialog
- Soft delete (mark as deleted) or hard delete
- Cascade consideration: what happens to linked tasks?

### FR5: Phase Transitions
- 6 phases: raw-idea → shape → write → tasks → implement → verify
- Manual advancement only
- Can go backwards (revert to previous phase)
- Visual stepper component showing progress

### FR6: Spec Detail View
- Dedicated panel or page showing full spec info
- Phase stepper with transition buttons
- Link to related tasks (future integration)

## Data Model

```sql
CREATE TABLE specs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  phase TEXT NOT NULL DEFAULT 'raw-idea'
    CHECK (phase IN ('raw-idea', 'shape', 'write', 'tasks', 'implement', 'verify')),
  due_date DATE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_specs_project_id ON specs(project_id);
CREATE INDEX idx_specs_phase ON specs(phase);
```

## UI Components
- SpecCard - displays spec in list
- SpecStepper - horizontal phase indicator
- SpecFormModal - create/edit form
- SpecDetailPanel - full spec view

## Out of Scope (MVP)
- Priority field
- Tags/labels
- Assignee
- Task linking (separate feature)
- Bulk operations
- Import/export
- Spec templates

---
Created: 2026-01-08
