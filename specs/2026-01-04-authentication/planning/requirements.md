# Spec Requirements: Authentication with Supabase Auth

## Initial Description

Implement authentication for the AgentOS Tracker web application using Supabase Auth. This is part of Phase 1 MVP and is a foundational feature that other features will depend on. The tech stack includes Next.js 14 + React + Tailwind CSS + shadcn/ui + Supabase.

## Requirements Discussion

### First Round Questions

**Q1:** I assume you want email/password as the primary authentication method, with a simple magic link option as an alternative. Is that correct, or do you also want OAuth providers (Google, GitHub) from the start?
**Answer:** Email/password and magic link confirmed. No OAuth for MVP - deferred to Phase 3.

**Q2:** I'm thinking we should add GitHub OAuth since Phase 3 includes GitHub integration anyway, and it's a natural fit for a developer tool. Should we include it in the MVP, or defer to Phase 3?
**Answer:** Defer to Phase 3. MVP focuses on email-based authentication only.

**Q3:** I assume a minimal user profile for MVP: just email, display name, and avatar (from OAuth or Gravatar). Should we add any other fields like organization, role, or preferences now?
**Answer:** Confirmed minimal profile: email, display name, avatar (Gravatar based on email). Extensible later.

**Q4:** For password requirements, I'm assuming standard security: minimum 8 characters, at least one uppercase, one lowercase, and one number. Should we adjust these requirements?
**Answer:** Simplified: minimum 8 characters only. No complex rules (uppercase/number not required). Supabase handles secure hashing.

**Q5:** I assume email verification should be required before users can access the app (security best practice). Is that correct, or should unverified users have limited access?
**Answer:** Email verification REQUIRED before app access. No limited access for unverified users.

**Q6:** I'm thinking we need a password reset flow via email link. Is that correct? Any specific requirements for the reset flow?
**Answer:** Confirmed. Standard password reset via email link.

**Q7:** For session duration, I assume 7 days with automatic refresh is reasonable for a productivity tool. Should it be longer/shorter, or do you want a "remember me" option?
**Answer:** 30 days duration with automatic refresh. No "remember me" option needed.

**Q8:** I assume no RBAC for MVP - all authenticated users have the same access level. Is that correct, or do you need admin/user roles from the start?
**Answer:** Confirmed. No RBAC for MVP. All authenticated users have same access level.

**Q9:** For the login/signup UI, I'm assuming clean, minimal forms following the dark theme design system with shadcn/ui components. Should the auth pages have any special branding, illustrations, or layout preferences?
**Answer:** Clean, minimal forms. Dark theme (design-system from Auto Claude screenshots). Centered layout with simple logo.

**Q10:** Is there anything specific you want to exclude from this authentication feature, or any edge cases we should handle specially?
**Answer:** Exclusions confirmed: No 2FA/MFA, No SSO, No social/OAuth login, No admin roles.

### Existing Code to Reference

No similar existing features identified for reference. This is the first feature being built for the application.

### Follow-up Questions

No follow-up questions were needed - user approved all recommendations.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
- Design should follow the dark theme design system
- Centered layout with simple logo
- Clean, minimal forms using shadcn/ui components

## Requirements Summary

### Functional Requirements

**Authentication Methods:**
- Email/password signup and login
- Magic link (passwordless) as alternative login method
- Email verification required before app access
- Password reset via email link

**User Profile:**
- Email address (from auth)
- Display name (user-provided)
- Avatar (Gravatar based on email hash)

**Password Policy:**
- Minimum 8 characters
- No complexity requirements (uppercase, numbers, symbols not required)
- Supabase handles secure hashing (bcrypt)

**Session Management:**
- 30-day session duration
- Automatic token refresh
- Secure session storage

**Pages Required:**
- `/login` - Email/password login + magic link option
- `/signup` - User registration form
- `/forgot-password` - Request password reset email
- `/reset-password` - Set new password (from email link)

### Reusability Opportunities

- Form components can be reused across other features
- Auth hooks/context can be referenced by all protected features
- Validation patterns can be standardized for future forms

### Scope Boundaries

**In Scope:**
- Email/password authentication
- Magic link authentication
- Email verification flow
- Password reset flow
- Session management with 30-day duration
- User profile (email, display name, Gravatar avatar)
- Protected route middleware
- Auth context/hooks for React components
- 4 auth pages: login, signup, forgot-password, reset-password

**Out of Scope:**
- OAuth/social login (Google, GitHub) - deferred to Phase 3
- Two-factor authentication (2FA/MFA)
- Single sign-on (SSO)
- Role-based access control (RBAC)
- Admin roles or user hierarchies
- "Remember me" checkbox
- Account deletion/deactivation
- Profile editing (beyond initial signup)

### Technical Considerations

- Integration with Supabase Auth API
- Next.js 14 App Router for routing
- Server-side session validation for protected routes
- Client-side auth state management
- Supabase client configuration
- Environment variables for Supabase credentials
- Email templates configured in Supabase dashboard

---

## Complexity Analysis

### Elements Identified

| Element | Count | Points |
|---------|-------|--------|
| UI Components | 4 | 4 |
| API Endpoints | 5 | 10 |
| Database Changes | 1 | 3 |
| External Integrations | 1 | 5 |
| User Scenarios | 8 | 4 |
| State Management | 1 | 2 |
| Auth/Security | 1 | 3 |

**Breakdown:**

**UI Components (4):**
1. Login page with form
2. Signup page with form
3. Forgot password page
4. Reset password page

**API Endpoints (5):**
1. POST /auth/signup - Register new user
2. POST /auth/login - Email/password login
3. POST /auth/magic-link - Send magic link
4. POST /auth/forgot-password - Request reset email
5. POST /auth/reset-password - Set new password

**Database Changes (1):**
1. User profiles table (extends Supabase auth.users)

**External Integrations (1):**
1. Supabase Auth service

**User Scenarios (8):**
1. User signs up with email/password
2. User verifies email
3. User logs in with email/password
4. User logs in with magic link
5. User requests password reset
6. User resets password
7. User accesses protected route (authenticated)
8. User is redirected when not authenticated

**State Management (1):**
1. Auth context/provider for React

**Auth/Security (1):**
1. Core authentication logic involved

**Total Complexity Score: 31**

### Recommended Track

**COMPLEX**

**Recommended Workflow:**
1. `/verify-spec` - Validate specification completeness
2. `/write-spec` - Create detailed technical specification
3. `/plan-tests` - Define test scenarios and acceptance criteria
4. `/create-tasks` - Break down into implementation tasks
5. `/orchestrate-tasks` - Coordinate parallel task execution
6. `/verify` - Validate implementation against requirements
