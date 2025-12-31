# User Testing Database

## Overview

At the end of each task group implementation, user tests should be added to a dedicated Notion database to track manual testing requirements.

## Database Structure

Create a Notion database named "Tests Utilisateur - [Project Name]" with the following properties:

| Property | Type | Options |
|----------|------|---------|
| Name | Title | - |
| Groupe | Select | Auth, Recettes, Planning, etc. (per feature group) |
| Statut | Select | À tester, Validé, Bug |
| Priorité | Select | Critique, Important, Normal |
| Étapes | Text | Step-by-step test instructions |
| Résultat attendu | Text | Expected outcome |
| Date | Date | Test completion date |

## Workflow Integration

### After completing a Task Group:

1. Identify all user-facing features implemented
2. Create test entries in the database via MCP:

```json
{
  "parent": {"type": "data_source_id", "data_source_id": "[your-database-id]"},
  "pages": [{
    "properties": {
      "Name": "Feature description to test",
      "Groupe": "Feature Group",
      "Statut": "À tester",
      "Priorité": "Critique",
      "Étapes": "1. Step one\\n2. Step two\\n3. Step three",
      "Résultat attendu": "What should happen"
    }
  }]
}
```

### Status Flow:

```
À tester → Validé (if test passes)
         → Bug (if test fails - create bug in 🐛 Bugs database)
```

## Example Test Entries

### Authentication Feature Group:

| Test | Priority |
|------|----------|
| Registration with valid email | Critique |
| Email validation | Critique |
| Login after validation | Critique |
| Biometric toggle | Normal |
| Logout | Important |
| Forgot password flow | Important |

## Benefits

- Clear visibility on what needs manual testing
- Tracks testing progress per feature group
- Links bugs discovered to specific tests
- Ensures no feature ships without manual QA
