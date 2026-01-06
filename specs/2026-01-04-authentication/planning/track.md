# Workflow Track

**Selected Track:** 🏗️ COMPLEX
**Selection Method:** Recommended
**Complexity Score:** 31 points

## Workflow Steps

1. `/verify-spec` → Validate specification coherence (REQUIRED)
2. `/write-spec` → Generate detailed technical specification
3. `/plan-tests` → Create comprehensive test plan (REQUIRED)
4. `/create-tasks` → Create task list
5. `/orchestrate-tasks` → Parallel implementation
6. `/verify` → Full verification suite

## Complexity Breakdown

| Element | Count | Points |
|---------|-------|--------|
| UI Components | 4 | 4 |
| API Endpoints | 5 | 10 |
| DB Changes | 1 | 3 |
| Integrations | 1 | 5 |
| User Scenarios | 8 | 4 |
| State Management | 1 | 2 |
| Auth/Security | 1 | 3 |
| **Total** | - | **31** |

## Rationale

Score exceeds 20-point threshold for COMPLEX track due to:
- External integration with Supabase Auth
- Multiple API endpoints (5 distinct operations)
- Core security feature requiring thorough implementation
- Multiple user scenarios (8 distinct flows)
