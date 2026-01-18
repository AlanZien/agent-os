# Workflow Track

**Selected Track:** 🏗️ COMPLEX
**Selection Method:** Recommended (accepted by user)
**Complexity Score:** 25 points

## Score Breakdown

| Element          | Count | Points |
|------------------|:-----:|:------:|
| UI Components    | 0     | 0      |
| API Endpoints    | 6     | 12     |
| DB Changes       | 2     | 6      |
| Integrations     | 0     | 0      |
| User Scenarios   | 8     | 4      |
| State Management | 0     | 0      |
| Auth/Security    | 1     | 3      |
| **Total**        |       | **25** |

## Workflow Steps

1. ~~`/shape-spec`~~ ✅ Requirements gathered
2. `/verify-spec` → Validate specification coherence (REQUIRED for COMPLEX)
3. `/write-spec` → Generate detailed technical specification
4. `/plan-tests` → Create comprehensive test plan (REQUIRED)
5. `/create-tasks` → Create implementation task list
6. `/orchestrate-tasks` → Parallel implementation with specialized agents
7. `/verify` → Full verification suite

## Track Justification

- 6 API endpoints with different behaviors (create, upsert, bulk)
- Database migrations affecting 2 tables (projects, features)
- Authentication middleware requirement
- Transactional bulk operations with rollback
- Auto-assignment and phase progression logic

---
Created: 2026-01-18
