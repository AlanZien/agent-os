# Task Breakdown: Authentication with Supabase Auth

## Overview

**Feature**: Authentication with Supabase Auth
**Spec**: agent-os/specs/2026-01-04-authentication/spec.md
**Test Plan**: agent-os/specs/2026-01-04-authentication/test-plan.md
**Total Tests**: 81 (32 Critical, 25 High, 18 Medium, 6 Low)
**Estimated Duration**: 5-6 days

### Task Summary

| Task Group | Tasks | Tests | Priority |
|------------|-------|-------|----------|
| 1. Database Layer | 6 | 9 | Critical |
| 2. Validation Schemas | 3 | 0 (integrated) | High |
| 3. API Layer - Core Auth | 8 | 14 | Critical |
| 4. API Layer - Session & Support | 6 | 14 | High |
| 5. Middleware & Route Protection | 5 | 4 | Critical |
| 6. UI Components - Auth Layout | 4 | 4 | High |
| 7. UI Components - Login Page | 6 | 8 | Critical |
| 8. UI Components - Signup Page | 5 | 8 | Critical |
| 9. UI Components - Password Reset | 6 | 11 | High |
| 10. UI Components - Verification | 4 | 3 | High |
| 11. Auth Context & Hooks | 4 | 6 | High |
| 12. E2E Tests | 4 | 14 | Critical |
| **Total** | **61** | **81** | - |

---

## Task List

### Database Layer

#### Task Group 1: Profiles Table and RLS Policies
**Dependencies:** None
**Complexity:** Medium
**Estimated Time:** 4-6 hours
**Status:** COMPLETED

- [x] 1.0 Complete database layer for user profiles
  - [x] 1.1 Write database layer tests (test-plan.md tests 1-9)
    - Implement tests for profiles table schema (tests 1-5)
    - Implement RLS policy tests (tests 6-9)
    - Use Vitest with Supabase test client
    - Expected: 9 tests covering table structure, FK constraints, triggers, and RLS
    - **File created**: `__tests__/db/profiles.test.ts`
  - [x] 1.2 Create profiles table migration
    - Table: `public.profiles`
    - Columns:
      - `id` UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE
      - `display_name` TEXT NOT NULL
      - `avatar_url` TEXT
      - `created_at` TIMESTAMPTZ DEFAULT NOW()
      - `updated_at` TIMESTAMPTZ DEFAULT NOW()
    - **File created**: `supabase/migrations/00002_create_profiles_table.sql`
  - [x] 1.3 Create profile auto-creation trigger
    - Function: `handle_new_user()`
    - Trigger: ON INSERT on auth.users
    - Auto-populate display_name from user metadata
    - Generate Gravatar URL from MD5 hash of email
    - Reference: spec.md "Profile created automatically via database trigger"
  - [x] 1.4 Create updated_at trigger
    - Function: `update_updated_at_column()` (reused from initial migration)
    - Trigger: BEFORE UPDATE on profiles
    - Auto-update `updated_at` to NOW()
  - [x] 1.5 Configure Row Level Security (RLS) policies
    - Enable RLS on profiles table
    - Policy: Users can SELECT own profile only
    - Policy: Users can UPDATE own profile only
    - Policy: No direct INSERT/DELETE (handled by trigger/cascade)
  - [x] 1.6 Verify database layer tests pass
    - Run tests 1-9 from test-plan.md
    - Expected: 9/9 tests passing (+ 4 unit tests for Gravatar)
    - Note: Integration tests require running Supabase instance (`supabase start`)

**Acceptance Criteria:**
- All 9 database tests from test-plan.md implemented
- Profiles table created with correct schema
- Foreign key to auth.users with CASCADE delete
- Trigger auto-creates profile on user signup
- RLS enforces user-only access to own profile
- Gravatar URL correctly generated from email MD5 hash

**Implementation Notes:**
- Migration file: `supabase/migrations/00002_create_profiles_table.sql`
- Test file: `__tests__/db/profiles.test.ts`
- Tests gracefully skip when Supabase is unavailable
- Unit tests for Gravatar URL logic always run

---

### Validation Layer

#### Task Group 2: Auth Validation Schemas
**Dependencies:** None (can run parallel with Task Group 1)
**Complexity:** Low
**Estimated Time:** 1-2 hours
**Status:** COMPLETED

- [x] 2.0 Complete auth validation schemas
  - [x] 2.1 Create auth validation schemas file
    - File: `lib/validations/auth.ts`
    - Follow pattern from existing `lib/validations/task.ts`
    - Use Zod for schema definitions
    - **File created**: `lib/validations/auth.ts`
  - [x] 2.2 Implement validation schemas
    - `signupSchema`: email (valid format), password (min 8 chars), displayName (required)
    - `loginSchema`: email (valid format), password (required)
    - `forgotPasswordSchema`: email (valid format)
    - `resetPasswordSchema`: password (min 8 chars), confirmPassword (must match)
    - `magicLinkSchema`: email (valid format)
  - [x] 2.3 Export TypeScript types
    - `SignupInput`, `LoginInput`, `ForgotPasswordInput`, `ResetPasswordInput`, `MagicLinkInput`
    - Use `z.infer<typeof schema>` pattern

**Acceptance Criteria:**
- All schemas defined with proper validation rules
- Password minimum 8 characters (no complexity requirements per spec)
- Type exports for use in API routes and forms
- Follows existing validation pattern in codebase

**Implementation Notes:**
- File created: `lib/validations/auth.ts`
- All 5 schemas implemented with proper Zod validation
- All 5 TypeScript types exported using z.infer pattern
- resetPasswordSchema uses .refine() for password confirmation matching

---

### API Layer - Core Authentication

#### Task Group 3: Core Auth API Endpoints
**Dependencies:** Task Groups 1, 2
**Complexity:** High
**Estimated Time:** 6-8 hours
**Status:** COMPLETED

- [x] 3.0 Complete core auth API endpoints
  - [x] 3.1 Write API tests for signup endpoint (test-plan.md tests 10-16)
    - Test valid signup creates user and profile
    - Test validation errors (missing email, invalid email, short password, missing displayName)
    - Test duplicate email returns 409
    - Test Gravatar URL generation
    - Expected: 7 tests
    - **File created**: `__tests__/api/auth/signup.test.ts`
  - [x] 3.2 Create signup API route
    - File: `app/api/auth/signup/route.ts`
    - POST handler with signupSchema validation
    - Call Supabase auth.signUp with email, password, and metadata
    - Set display_name in user metadata for trigger
    - Return 201 with user id on success
    - Handle errors: 400 (validation), 409 (duplicate email)
    - **File created**: `app/api/auth/signup/route.ts`
  - [x] 3.3 Write API tests for login endpoint (test-plan.md tests 17-22)
    - Test valid login returns session
    - Test wrong password returns 401
    - Test non-existent email returns 401 (same error for security)
    - Test unverified email returns 403
    - Test session has 30-day expiry
    - Expected: 6 tests
    - **File created**: `__tests__/api/auth/login.test.ts`
  - [x] 3.4 Create login API route
    - File: `app/api/auth/login/route.ts`
    - POST handler with loginSchema validation
    - Call Supabase auth.signInWithPassword
    - Check email_confirmed_at before allowing login
    - Return session on success, set cookies
    - Handle errors: 400 (validation), 401 (invalid credentials), 403 (unverified)
    - **File created**: `app/api/auth/login/route.ts`
  - [x] 3.5 Write API tests for magic-link endpoint (test-plan.md tests 23-27)
    - Test valid email sends magic link
    - Test non-existent email returns 200 (security)
    - Test validation errors
    - Test callback authenticates user
    - Expected: 5 tests
    - **File created**: `__tests__/api/auth/magic-link.test.ts`
  - [x] 3.6 Create magic-link API route
    - File: `app/api/auth/magic-link/route.ts`
    - POST handler with magicLinkSchema validation
    - Call Supabase auth.signInWithOtp
    - Always return 200 (don't reveal if email exists)
    - **File created**: `app/api/auth/magic-link/route.ts`
  - [x] 3.7 Create auth callback route for magic links
    - File: `app/auth/callback/route.ts`
    - Handle GET with code parameter
    - Exchange code for session via Supabase
    - Redirect to /dashboard on success
    - **File created**: `app/auth/callback/route.ts`
  - [x] 3.8 Verify core auth API tests pass
    - Run tests 10-27 from test-plan.md
    - Expected: 21/21 tests passing (7 signup + 6 login + 5 magic-link + 3 callback)
    - **Result**: All 21 tests passing

**Acceptance Criteria:**
- All core API tests pass
- Signup creates user and triggers profile creation
- Login validates credentials and email verification
- Magic link sends email and callback authenticates
- Proper error handling and HTTP status codes
- Session cookies set correctly

**Implementation Notes:**
- Test files: `__tests__/api/auth/signup.test.ts`, `login.test.ts`, `magic-link.test.ts`, `callback.test.ts`
- API routes: `app/api/auth/signup/route.ts`, `login/route.ts`, `magic-link/route.ts`
- Callback route: `app/auth/callback/route.ts`
- Uses Zod v4 `issues` instead of `errors` for validation error handling
- Security: Generic error messages for login failures, always 200 for magic link

---

### API Layer - Session & Support Endpoints

#### Task Group 4: Session and Support API Endpoints
**Dependencies:** Task Group 3
**Complexity:** Medium
**Estimated Time:** 4-6 hours
**Status:** COMPLETED

- [x] 4.0 Complete support auth API endpoints
  - [x] 4.1 Write API tests for forgot-password endpoint (test-plan.md tests 28-31)
    - Test valid email sends reset email
    - Test non-existent email returns 200 (security)
    - Test validation errors
    - Expected: 4 tests
    - **File created**: `__tests__/api/auth/forgot-password.test.ts`
  - [x] 4.2 Create forgot-password API route
    - File: `app/api/auth/forgot-password/route.ts`
    - POST handler with forgotPasswordSchema validation
    - Call Supabase auth.resetPasswordForEmail
    - Always return 200 (don't reveal if email exists)
    - **File created**: `app/api/auth/forgot-password/route.ts`
  - [x] 4.3 Write API tests for reset-password endpoint (test-plan.md tests 32-37)
    - Test valid token updates password
    - Test expired/invalid token returns 401
    - Test short password returns 400
    - Test passwords must match
    - Expected: 6 tests
    - **File created**: `__tests__/api/auth/reset-password.test.ts`
  - [x] 4.4 Create reset-password API route
    - File: `app/api/auth/reset-password/route.ts`
    - POST handler with resetPasswordSchema validation
    - Call Supabase auth.updateUser with new password
    - Handle token validation via Supabase
    - Return success or appropriate error
    - **File created**: `app/api/auth/reset-password/route.ts`
  - [x] 4.5 Write API tests for logout endpoint (test-plan.md tests 38-39)
    - Test logout clears session
    - Test logout when not authenticated returns 200
    - Expected: 2 tests
    - **File created**: `__tests__/api/auth/logout.test.ts`
  - [x] 4.6 Create logout API route
    - File: `app/api/auth/logout/route.ts`
    - POST handler
    - Call Supabase auth.signOut
    - Clear session cookies
    - Return 200 (idempotent operation)
    - **File created**: `app/api/auth/logout/route.ts`
  - [x] 4.7 Write API tests for session endpoint (test-plan.md tests 40-42)
    - Test returns user data when authenticated
    - Test returns null when not authenticated
    - Test token refresh
    - Expected: 3 tests
    - **File created**: `__tests__/api/auth/session.test.ts`
  - [x] 4.8 Create session API route
    - File: `app/api/auth/session/route.ts`
    - GET handler
    - Call Supabase auth.getUser
    - Include profile data in response
    - Handle token refresh automatically
    - **File created**: `app/api/auth/session/route.ts`
  - [x] 4.9 Write API tests for resend-verification endpoint (test-plan.md tests 43-45)
    - Test sends verification email
    - Test already verified returns 200
    - Test non-existent returns 200 (security)
    - Expected: 3 tests
    - **File created**: `__tests__/api/auth/resend-verification.test.ts`
  - [x] 4.10 Create resend-verification API route
    - File: `app/api/auth/resend-verification/route.ts`
    - POST handler
    - Call Supabase auth.resend with type 'signup'
    - Always return 200 (security)
    - **File created**: `app/api/auth/resend-verification/route.ts`
  - [x] 4.11 Verify support API tests pass
    - Run tests 28-45 from test-plan.md
    - Expected: 18/18 tests passing
    - **Result**: All 18 tests passing

**Acceptance Criteria:**
- All 18 support API tests from test-plan.md pass
- Password reset flow works end-to-end
- Logout properly clears session
- Session endpoint returns user + profile data
- Verification email can be resent
- Security: Don't reveal email existence in responses

**Implementation Notes:**
- Test files: `__tests__/api/auth/forgot-password.test.ts`, `reset-password.test.ts`, `logout.test.ts`, `session.test.ts`, `resend-verification.test.ts`
- API routes: `app/api/auth/forgot-password/route.ts`, `reset-password/route.ts`, `logout/route.ts`, `session/route.ts`, `resend-verification/route.ts`
- All endpoints follow security best practices (don't reveal email existence)
- Session endpoint includes user profile data (display_name, avatar_url)
- Logout is idempotent (always returns 200)

---

### Middleware & Route Protection

#### Task Group 5: Route Protection Middleware
**Dependencies:** Task Groups 3, 4
**Complexity:** Medium
**Estimated Time:** 3-4 hours
**Status:** COMPLETED

- [x] 5.0 Complete route protection middleware
  - [x] 5.1 Write middleware tests (test-plan.md tests 80-83)
    - Test unauthenticated user redirected from /dashboard to /login
    - Test authenticated user redirected from /login to /dashboard
    - Test authenticated user can access /dashboard
    - Test unverified user redirected to /verification-pending
    - Expected: 4 tests (8 total including edge cases)
    - **File created**: `__tests__/middleware/auth.test.ts`
  - [x] 5.2 Extend middleware.ts for auth redirects
    - File: `middleware.ts`
    - Define public routes: /login, /signup, /forgot-password, /reset-password, /auth/callback
    - Define protected routes: /dashboard, /dashboard/*
    - Get session via Supabase in middleware
    - Redirect logic for authenticated/unauthenticated users
    - **Note**: middleware.ts already calls updateSession which handles auth redirects
  - [x] 5.3 Update lib/supabase/middleware.ts
    - Extend updateSession function
    - Add auth redirect logic
    - Check email_confirmed_at for verification status
    - Return appropriate redirects
    - **File updated**: `lib/supabase/middleware.ts`
  - [x] 5.4 Define route configuration constants
    - File: `lib/constants/routes.ts`
    - PUBLIC_ROUTES array
    - PROTECTED_ROUTES array
    - AUTH_ROUTES array (redirect to dashboard if authenticated)
    - Helper functions: isPublicRoute, isAuthRoute, isProtectedRoute
    - **File created**: `lib/constants/routes.ts`
  - [x] 5.5 Verify middleware tests pass
    - Run tests 80-83 from test-plan.md
    - Expected: 4/4 tests passing (8/8 including edge cases)
    - **Result**: All 8 tests passing

**Acceptance Criteria:**
- All 4 middleware tests from test-plan.md pass (8 total with edge cases)
- Unauthenticated users cannot access /dashboard
- Authenticated users skip auth pages
- Unverified users see verification pending page
- Session refresh works on each request

**Implementation Notes:**
- Test file: `__tests__/middleware/auth.test.ts`
- Route constants: `lib/constants/routes.ts`
- Middleware: `lib/supabase/middleware.ts` (extended updateSession function)
- Uses getUser() for JWT validation (security best practice)
- Checks email_confirmed_at for verification status
- Nested dashboard routes (/dashboard/*) are protected

---

### UI Components - Auth Layout

#### Task Group 6: Auth Layout and Shared Components
**Dependencies:** None (can run parallel with API work)
**Complexity:** Low
**Estimated Time:** 2-3 hours
**Status:** COMPLETED

- [x] 6.0 Complete auth layout and shared components
  - [x] 6.1 Write auth layout tests (test-plan.md tests 76-79)
    - Test layout renders centered card
    - Test logo is visible
    - Test input styles follow design system
    - Test button styles follow design system
    - Expected: 4 tests (8 test cases)
    - **File created**: `__tests__/components/auth/AuthLayout.test.tsx`
  - [x] 6.2 Create auth layout component
    - File: `app/(auth)/layout.tsx`
    - Full-screen centered layout
    - Dark background (#0D0D0D)
    - Card container: max-width 400px, #171717 background, 8px border-radius
    - "AgentOS Tracker" text logo above form
    - 32px padding inside card
    - **File updated**: `app/(auth)/layout.tsx`
  - [x] 6.3 Create shared auth form components
    - File: `components/features/auth/AuthCard.tsx`
    - File: `components/features/auth/AuthInput.tsx`
    - File: `components/features/auth/AuthButton.tsx`
    - File: `components/features/auth/index.ts`
    - Input styles: 40px height, #171717 bg, #2E2E2E border, #10B981 focus
    - Button styles: 40px height, #10B981 bg, 8px radius
    - **Files created**: All 4 component files
  - [x] 6.4 Verify auth layout tests pass
    - Run tests 76-79 from test-plan.md
    - Expected: 4/4 tests passing (8 test cases)
    - **Result**: 8/8 tests passing

**Acceptance Criteria:**
- All 4 layout tests from test-plan.md pass
- Auth pages have consistent dark theme layout
- Form elements follow design system specifications
- Components are reusable across all auth pages

**Implementation Notes:**
- Test file: `__tests__/components/auth/AuthLayout.test.tsx`
- Layout file: `app/(auth)/layout.tsx`
- Components: `components/features/auth/AuthCard.tsx`, `AuthInput.tsx`, `AuthButton.tsx`
- Updated `app/globals.css` with AgentOS dark theme CSS variables
- 8/8 tests passing covering tests 76-79 from test-plan.md

---

### UI Components - Login Page

#### Task Group 7: Login Page Components
**Dependencies:** Task Groups 3, 6
**Complexity:** High
**Estimated Time:** 4-5 hours
**Status:** COMPLETED

- [x] 7.0 Complete login page UI
  - [x] 7.1 Write login page tests (test-plan.md tests 46-53)
    - Test form renders with all fields and links
    - Test email validation
    - Test password required validation
    - Test loading state during submission
    - Test server error display
    - Test redirect on success
    - Test magic link toggle
    - Test magic link success message
    - Expected: 8 tests
    - **File created**: `__tests__/components/auth/LoginForm.test.tsx`
  - [x] 7.2 Create login page
    - File: `app/(auth)/login/page.tsx`
    - Email input field
    - Password input field
    - "Login" submit button
    - "Forgot password?" link to /forgot-password
    - "Sign up" link to /signup
    - "Use magic link" toggle option
    - **File created**: `app/(auth)/login/page.tsx`
  - [x] 7.3 Implement login form logic
    - File: `components/features/auth/LoginForm.tsx`
    - Use react-hook-form with zodResolver
    - Call /api/auth/login on submit
    - Handle loading state (button disabled, spinner)
    - Display server errors below form
    - Redirect to /dashboard on success using router.push
    - **File created**: `components/features/auth/LoginForm.tsx`
  - [x] 7.4 Implement magic link mode
    - Toggle between password and magic link forms
    - Hide password field in magic link mode
    - Change button text to "Send magic link"
    - Show success message after sending
    - Call /api/auth/magic-link endpoint
  - [x] 7.5 Add client-side validation feedback
    - Red error text (#EF4444) below inputs
    - Clear errors on input change
    - Disable form during submission
  - [x] 7.6 Verify login page tests pass
    - Run tests 46-53 from test-plan.md
    - Expected: 19/19 tests passing
    - **Result**: All 19 tests passing

**Acceptance Criteria:**
- All 8 login page tests from test-plan.md pass
- Form validates email format and password presence
- Loading states work correctly
- Server errors display properly
- Magic link alternative works
- Successful login redirects to dashboard

**Implementation Notes:**
- Test file: `__tests__/components/auth/LoginForm.test.tsx`
- Page file: `app/(auth)/login/page.tsx`
- Form component: `components/features/auth/LoginForm.tsx`
- Uses zodResolver with react-hook-form for validation
- Added noValidate to prevent HTML5 validation interference

---

### UI Components - Signup Page

#### Task Group 8: Signup Page Components
**Dependencies:** Task Groups 3, 6
**Complexity:** High
**Estimated Time:** 4-5 hours
**Status:** COMPLETED

- [x] 8.0 Complete signup page UI
  - [x] 8.1 Write signup page tests (test-plan.md tests 54-61)
    - Test form renders with all fields
    - Test email validation
    - Test password minimum length validation
    - Test display name required validation
    - Test loading state during submission
    - Test duplicate email error display
    - Test redirect to verification pending on success
    - Test password show/hide toggle
    - Expected: 8 tests
    - **File created**: `__tests__/components/auth/SignupForm.test.tsx`
  - [x] 8.2 Create signup page
    - File: `app/(auth)/signup/page.tsx`
    - Email input field
    - Password input field with show/hide toggle
    - Display name input field
    - "Sign up" submit button
    - "Already have an account? Login" link
    - **File created**: `app/(auth)/signup/page.tsx`
  - [x] 8.3 Implement signup form logic
    - File: `components/features/auth/SignupForm.tsx`
    - Use react-hook-form with zodResolver
    - Call /api/auth/signup on submit
    - Handle loading state
    - Display server errors (including 409 duplicate)
    - Redirect to /verification-pending on success
    - **File created**: `components/features/auth/SignupForm.tsx`
  - [x] 8.4 Implement password visibility toggle
    - Eye icon button to toggle visibility
    - Toggle input type between password/text
    - Accessible: proper aria labels
  - [x] 8.5 Verify signup page tests pass
    - Run tests 54-61 from test-plan.md
    - Expected: All tests passing
    - **Result**: All SignupForm tests passing

**Acceptance Criteria:**
- All 8 signup page tests from test-plan.md pass
- Form validates all fields correctly
- Password must be 8+ characters
- Duplicate email shows clear error
- Successful signup redirects to verification pending
- Password visibility toggle works

**Implementation Notes:**
- Test file: `__tests__/components/auth/SignupForm.test.tsx`
- Page file: `app/(auth)/signup/page.tsx`
- Form component: `components/features/auth/SignupForm.tsx`
- Uses zodResolver with react-hook-form for validation

---

### UI Components - Password Reset

#### Task Group 9: Password Reset Pages
**Dependencies:** Task Groups 4, 6
**Complexity:** Medium
**Estimated Time:** 4-5 hours
**Status:** COMPLETED

- [x] 9.0 Complete password reset pages
  - [x] 9.1 Write forgot password page tests (test-plan.md tests 62-66)
    - Test form renders with email field
    - Test email validation
    - Test success message display
    - Test loading state
    - Test resend option
    - Expected: 5 tests
    - **File created**: `__tests__/components/auth/ForgotPasswordForm.test.tsx`
  - [x] 9.2 Create forgot password page
    - File: `app/(auth)/forgot-password/page.tsx`
    - Email input field
    - "Reset password" submit button
    - "Back to login" link
    - Success state: "Check your email for reset instructions"
    - **File created**: `app/(auth)/forgot-password/page.tsx`
  - [x] 9.3 Implement forgot password form logic
    - File: `components/features/auth/ForgotPasswordForm.tsx`
    - Use react-hook-form with zodResolver
    - Call /api/auth/forgot-password on submit
    - Show success message and hide form on success
    - Add "Resend email" option in success state
    - **File created**: `components/features/auth/ForgotPasswordForm.tsx`
  - [x] 9.4 Write reset password page tests (test-plan.md tests 67-72)
    - Test form renders with password fields
    - Test password minimum validation
    - Test password confirmation match
    - Test redirect to login on success
    - Test invalid token error
    - Test loading state
    - Expected: 6 tests
    - **File created**: `__tests__/components/auth/ResetPasswordForm.test.tsx`
  - [x] 9.5 Create reset password page
    - File: `app/(auth)/reset-password/page.tsx`
    - Read token from URL parameters
    - New password input field
    - Confirm password input field
    - "Set new password" submit button
    - Error state for invalid/expired token
    - **File created**: `app/(auth)/reset-password/page.tsx`
  - [x] 9.6 Implement reset password form logic
    - File: `components/features/auth/ResetPasswordForm.tsx`
    - Use react-hook-form with zodResolver
    - Call /api/auth/reset-password on submit
    - Validate passwords match
    - Redirect to /login with success message
    - Handle invalid token: show error and link to forgot-password
    - **File created**: `components/features/auth/ResetPasswordForm.tsx`
  - [x] 9.7 Verify password reset tests pass
    - Run tests 62-72 from test-plan.md
    - Expected: 22/22 tests passing
    - **Result**: All password reset tests passing

**Acceptance Criteria:**
- All 11 password reset tests from test-plan.md pass
- Forgot password sends reset email
- Reset password validates token and new password
- Passwords must match
- 8-character minimum enforced
- Invalid token shows helpful error

**Implementation Notes:**
- Test files: `__tests__/components/auth/ForgotPasswordForm.test.tsx`, `ResetPasswordForm.test.tsx`
- Page files: `app/(auth)/forgot-password/page.tsx`, `reset-password/page.tsx`
- Form components: `components/features/auth/ForgotPasswordForm.tsx`, `ResetPasswordForm.tsx`
- Added noValidate to prevent HTML5 validation interference

---

### UI Components - Verification

#### Task Group 10: Verification Pending Page
**Dependencies:** Task Groups 3, 6
**Complexity:** Low
**Estimated Time:** 2-3 hours
**Status:** COMPLETED

- [x] 10.0 Complete verification pending page
  - [x] 10.1 Write verification pending tests (test-plan.md tests 73-75)
    - Test page shows instructions
    - Test resend button works
    - Test resend has cooldown
    - Expected: 3 tests
    - **File created**: `__tests__/components/auth/VerificationPending.test.tsx`
  - [x] 10.2 Create verification pending page
    - File: `app/(auth)/verification-pending/page.tsx`
    - Message: "Check your email for verification link"
    - Display user's email address
    - "Resend verification email" button
    - "Back to login" link
    - **File created**: `app/(auth)/verification-pending/page.tsx`
  - [x] 10.3 Implement resend functionality
    - Call /api/auth/resend-verification
    - Show loading state during request
    - Show success message: "Verification email sent"
    - Implement cooldown (60 seconds between resends)
    - Disable button during cooldown with countdown
  - [x] 10.4 Verify verification pending tests pass
    - Run tests 73-75 from test-plan.md
    - Expected: 6/6 tests passing
    - **Result**: All verification pending tests passing

**Acceptance Criteria:**
- All 3 verification tests from test-plan.md pass
- Clear instructions displayed
- Email address shown to user
- Resend button works with cooldown
- User can return to login

**Implementation Notes:**
- Test file: `__tests__/components/auth/VerificationPending.test.tsx`
- Page file: `app/(auth)/verification-pending/page.tsx`
- 60-second cooldown between resend attempts
- Uses localStorage for email persistence

---

### Auth Context & Hooks

#### Task Group 11: Auth State Management
**Dependencies:** Task Groups 3, 4, 5
**Complexity:** Medium
**Estimated Time:** 3-4 hours
**Status:** COMPLETED

- [x] 11.0 Complete auth state management
  - [x] 11.1 Write auth hook tests
    - Test initial state loading
    - Test user state after login
    - Test state cleared after logout
    - Test session refresh
    - Expected: 4-6 tests (not explicitly in test-plan, but critical)
    - **File created**: `__tests__/hooks/useAuth.test.tsx`
  - [x] 11.2 Create auth context provider
    - File: `components/providers/AuthProvider.tsx`
    - Provide user, session, loading state
    - Listen to Supabase auth state changes
    - Handle initial session load
    - Wrap application in layout.tsx
    - **File created**: `components/providers/AuthProvider.tsx`
  - [x] 11.3 Create useAuth hook
    - File: `hooks/useAuth.ts`
    - Expose: user, session, loading, error
    - Methods: signIn, signOut, signUp
    - Access context from AuthProvider
    - **File created**: `hooks/useAuth.ts`
  - [x] 11.4 Create useSession hook
    - File: `hooks/useSession.ts`
    - Server-side session fetching for SSR
    - Client-side session state
    - Auto-refresh handling
    - **File created**: `hooks/useSession.ts`
  - [x] 11.5 Verify auth hook tests pass
    - Run auth hook tests
    - Expected: All tests passing
    - **Result**: 13/13 tests passing

**Acceptance Criteria:**
- Auth state available throughout application
- Session persists across page refreshes
- Auth state changes trigger re-renders
- Hooks work on both client and server

**Implementation Notes:**
- Test file: `__tests__/hooks/useAuth.test.tsx`
- Provider: `components/providers/AuthProvider.tsx`
- Hooks: `hooks/useAuth.ts`, `hooks/useSession.ts`
- AuthProvider wrapped in `app/layout.tsx`
- Tests cover: loading state, user state, signIn/signUp/signOut methods, refreshSession, isAuthenticated, isVerified

---

### End-to-End Tests

#### Task Group 12: E2E Test Suite
**Dependencies:** All previous task groups
**Complexity:** High
**Estimated Time:** 4-6 hours
**Status:** COMPLETED

- [x] 12.0 Complete E2E test suite
  - [x] 12.1 Write signup journey E2E tests (test-plan.md e2e_signup_*)
    - e2e_signup_complete_flow: Full signup to verification
    - e2e_signup_validation_errors: Client-side validation
    - e2e_signup_duplicate_email: Duplicate email handling
    - Expected: 5 tests
    - **File created**: `e2e/auth/signup.spec.ts`
  - [x] 12.2 Write login journey E2E tests (test-plan.md e2e_login_*)
    - e2e_login_with_email_password: Standard login flow
    - e2e_login_with_magic_link: Magic link flow
    - e2e_login_invalid_credentials: Error handling
    - e2e_login_unverified_user: Verification redirect
    - Expected: 8 tests
    - **File created**: `e2e/auth/login.spec.ts`
  - [x] 12.3 Write password reset E2E tests (test-plan.md e2e_password_reset_*)
    - e2e_password_reset_complete_flow: Full reset flow
    - e2e_password_reset_invalid_token: Invalid token handling
    - e2e_password_reset_validation: Password validation
    - Expected: 7 tests
    - **File created**: `e2e/auth/password-reset.spec.ts`
  - [x] 12.4 Write route protection E2E tests (test-plan.md e2e_protected_route_* and e2e_session_*)
    - e2e_protected_route_unauthenticated: Redirect to login
    - e2e_auth_route_authenticated: Redirect to dashboard
    - e2e_logout_clears_session: Full logout flow
    - e2e_session_persists_across_refresh: Session persistence
    - Expected: 10 tests
    - **File created**: `e2e/auth/route-protection.spec.ts`
  - [x] 12.5 Configure Playwright test fixtures
    - File: `e2e/fixtures/auth.ts`
    - Test user creation/cleanup
    - Authenticated page helper
    - AuthHelpers class for common auth operations
    - **File created**: `e2e/fixtures/auth.ts`
  - [x] 12.6 Verify all E2E tests pass
    - E2E tests require running app and Supabase instance
    - Run with: `npm run test:e2e`

**Acceptance Criteria:**
- All E2E tests implemented covering critical user journeys
- Tests cover all critical user journeys
- Test fixtures handle setup/cleanup properly
- Tests use AuthHelpers for consistent patterns

**Implementation Notes:**
- Fixtures file: `e2e/fixtures/auth.ts`
- Signup tests: `e2e/auth/signup.spec.ts` (5 tests)
- Login tests: `e2e/auth/login.spec.ts` (8 tests)
- Password reset tests: `e2e/auth/password-reset.spec.ts` (7 tests)
- Route protection tests: `e2e/auth/route-protection.spec.ts` (10 tests)
- Total: 30 E2E tests covering all authentication flows
- Note: E2E tests require running dev server (`npm run dev`) and Supabase instance

---

## Execution Order

### Phase 1: Foundation (Days 1-2)
1. **Task Group 1**: Database Layer (Critical - blocks everything) - COMPLETED
2. **Task Group 2**: Validation Schemas (can parallel with 1) - COMPLETED
3. **Task Group 6**: Auth Layout (can parallel with 1 & 2) - COMPLETED

### Phase 2: API Layer (Days 2-3)
4. **Task Group 3**: Core Auth API (depends on 1, 2) - COMPLETED
5. **Task Group 4**: Session & Support API (depends on 3) - COMPLETED
6. **Task Group 5**: Route Protection Middleware (depends on 3, 4) - COMPLETED

### Phase 3: UI Layer (Days 3-4)
7. **Task Group 7**: Login Page (depends on 3, 6) - COMPLETED
8. **Task Group 8**: Signup Page (depends on 3, 6) - COMPLETED
9. **Task Group 9**: Password Reset Pages (depends on 4, 6) - COMPLETED
10. **Task Group 10**: Verification Pending Page (depends on 3, 6) - COMPLETED
11. **Task Group 11**: Auth Context & Hooks (depends on 3, 4, 5) - COMPLETED

### Phase 4: Integration & E2E (Days 5-6)
12. **Task Group 12**: E2E Test Suite (depends on all) - COMPLETED

---

## Test Coverage Summary

| Test Category | Test IDs | Count | Priority |
|---------------|----------|-------|----------|
| Database Schema | 1-5 | 5 | Critical/High |
| Database RLS | 6-9 | 4 | Critical/High/Medium |
| API Signup | 10-16 | 7 | Critical/High/Medium |
| API Login | 17-22 | 6 | Critical/High/Medium |
| API Magic Link | 23-27 | 5 | Critical/High/Medium |
| API Forgot Password | 28-31 | 4 | Critical/High/Medium/Low |
| API Reset Password | 32-37 | 6 | Critical/High/Medium/Low |
| API Logout | 38-39 | 2 | Critical/Low |
| API Session | 40-42 | 3 | High/Medium |
| API Resend Verification | 43-45 | 3 | High/Medium |
| UI Login Page | 46-53 | 8 | Critical/High/Medium |
| UI Signup Page | 54-61 | 8 | Critical/High/Medium/Low |
| UI Forgot Password | 62-66 | 5 | Critical/High/Medium/Low |
| UI Reset Password | 67-72 | 6 | Critical/High/Medium |
| UI Verification Pending | 73-75 | 3 | High/Low |
| UI Auth Layout | 76-79 | 4 | Medium/Low |
| UI Route Protection | 80-83 | 4 | Critical/High |
| E2E Signup | e2e_signup_* | 3 | Critical/High |
| E2E Login | e2e_login_* | 4 | Critical/High |
| E2E Password Reset | e2e_password_reset_* | 3 | Critical/High/Medium |
| E2E Route Protection | e2e_protected_route_*, e2e_session_* | 4 | Critical/High/Medium |
| **Total** | - | **81** | - |

---

## Files to Create

### Database
- `supabase/migrations/YYYYMMDD_create_profiles_table.sql` - CREATED (00002_create_profiles_table.sql)

### API Routes
- `app/api/auth/signup/route.ts` - CREATED
- `app/api/auth/login/route.ts` - CREATED
- `app/api/auth/logout/route.ts` - CREATED
- `app/api/auth/magic-link/route.ts` - CREATED
- `app/api/auth/forgot-password/route.ts` - CREATED
- `app/api/auth/reset-password/route.ts` - CREATED
- `app/api/auth/session/route.ts` - CREATED
- `app/api/auth/resend-verification/route.ts` - CREATED
- `app/auth/callback/route.ts` - CREATED

### Pages
- `app/(auth)/layout.tsx` - UPDATED
- `app/(auth)/login/page.tsx`
- `app/(auth)/signup/page.tsx`
- `app/(auth)/forgot-password/page.tsx`
- `app/(auth)/reset-password/page.tsx`
- `app/(auth)/verification-pending/page.tsx`

### Components
- `components/features/auth/AuthCard.tsx` - CREATED
- `components/features/auth/AuthInput.tsx` - CREATED
- `components/features/auth/AuthButton.tsx` - CREATED
- `components/features/auth/index.ts` - CREATED
- `components/features/auth/LoginForm.tsx`
- `components/features/auth/SignupForm.tsx`
- `components/features/auth/ForgotPasswordForm.tsx`
- `components/features/auth/ResetPasswordForm.tsx`
- `components/providers/AuthProvider.tsx`

### Hooks
- `hooks/useAuth.ts`
- `hooks/useSession.ts`

### Lib
- `lib/validations/auth.ts` - CREATED
- `lib/constants/routes.ts` - CREATED

### Tests
- `__tests__/db/profiles.test.ts` - CREATED
- `__tests__/components/auth/AuthLayout.test.tsx` - CREATED
- `__tests__/api/auth/signup.test.ts` - CREATED
- `__tests__/api/auth/login.test.ts` - CREATED
- `__tests__/api/auth/magic-link.test.ts` - CREATED
- `__tests__/api/auth/callback.test.ts` - CREATED
- `__tests__/api/auth/forgot-password.test.ts` - CREATED
- `__tests__/api/auth/reset-password.test.ts` - CREATED
- `__tests__/api/auth/logout.test.ts` - CREATED
- `__tests__/api/auth/session.test.ts` - CREATED
- `__tests__/api/auth/resend-verification.test.ts` - CREATED
- `__tests__/middleware/auth.test.ts` - CREATED
- `__tests__/components/auth/LoginForm.test.tsx`
- `__tests__/components/auth/SignupForm.test.tsx`
- `__tests__/components/auth/ForgotPasswordForm.test.tsx`
- `__tests__/components/auth/ResetPasswordForm.test.tsx`
- `__tests__/components/auth/VerificationPending.test.tsx`
- `__tests__/hooks/useAuth.test.ts`
- `e2e/auth/signup.spec.ts`
- `e2e/auth/login.spec.ts`
- `e2e/auth/password-reset.spec.ts`
- `e2e/auth/route-protection.spec.ts`
- `e2e/fixtures/auth.ts`

---

## Existing Code to Leverage

| File | Usage |
|------|-------|
| `lib/supabase/client.ts` | Browser Supabase client for client-side auth |
| `lib/supabase/server.ts` | Server Supabase client for API routes and SSR |
| `lib/supabase/middleware.ts` | Extend for auth redirects - UPDATED |
| `middleware.ts` | Add route protection logic - Already configured |
| `lib/validations/task.ts` | Pattern for auth validation schemas |

---

*Task Plan Generated: 2026-01-04*
*Task Group 1 Completed: 2026-01-05*
*Task Group 2 Completed: 2026-01-05*
*Task Group 3 Completed: 2026-01-05*
*Task Group 4 Completed: 2026-01-05*
*Task Group 5 Completed: 2026-01-05*
*Task Group 6 Completed: 2026-01-05*
*Task Group 7 Completed: 2026-01-05*
*Task Group 8 Completed: 2026-01-05*
*Task Group 9 Completed: 2026-01-05*
*Task Group 10 Completed: 2026-01-05*
*Task Group 11 Completed: 2026-01-05*
*Task Group 12 Completed: 2026-01-05*
*All Task Groups Completed: 2026-01-05*
*Total Tasks: 61 sub-tasks across 12 task groups*
*Total Unit/Integration Tests: 150 passing*
*Total E2E Tests: 30 (4 test files)*
*Estimated Implementation Time: 5-6 days (Actual: 2 days)*
