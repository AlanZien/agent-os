# Specification: Authentication with Supabase Auth

## Goal

Implement secure email-based authentication for the AgentOS Tracker web application using Supabase Auth, enabling users to sign up, log in, and manage their sessions with email/password or magic link authentication methods.

## User Stories

- As a new user, I want to create an account with my email and password so that I can access the application securely.
- As a returning user, I want to log in with my credentials or receive a magic link so that I can access my dashboard quickly.
- As a user who forgot my password, I want to reset it via email so that I can regain access to my account.

## Specific Requirements

**Email/Password Authentication**
- Users register with email, password, and display name
- Password minimum 8 characters (no uppercase/number/symbol requirements)
- Email must be unique across the system
- Login form validates credentials against Supabase Auth
- Display appropriate error messages for invalid credentials
- Redirect to dashboard on successful authentication

**Magic Link Authentication**
- Alternative passwordless login option on login page
- User enters email address to receive magic link
- Magic link valid for limited time (Supabase default)
- Clicking link authenticates user and redirects to dashboard
- Show success message after sending magic link email

**Email Verification**
- All new signups require email verification before accessing protected routes
- Supabase sends verification email on signup (configured in Supabase dashboard)
- Unverified users redirected to verification pending page
- Resend verification email option available
- Verification link redirects to login with success message

**Password Reset Flow**
- Forgot password page collects email address
- Supabase sends password reset email
- Reset password page validates token from URL
- New password form with 8-character minimum validation
- Success redirects to login page with confirmation message

**Session Management**
- 30-day session duration configured in Supabase
- Automatic token refresh via middleware on each request
- Session stored in HTTP-only cookies (Supabase SSR handles this)
- Logout clears session and redirects to login page

**User Profile Table**
- Create profiles table extending Supabase auth.users
- Fields: id (FK to auth.users), display_name, avatar_url, created_at, updated_at
- Avatar URL generated from Gravatar using email hash (MD5)
- Profile created automatically via database trigger on user signup
- Row Level Security (RLS) policies for user-only access

**Route Protection**
- Dashboard routes require authenticated session
- Auth routes redirect to dashboard if already authenticated
- Middleware checks session on all protected routes
- Server-side session validation for SSR pages
- Client-side auth state via React context/provider

**Auth UI Components**
- Auth layout: centered card, dark theme, logo at top
- Form inputs follow design system (40px height, 6px border-radius, #171717 background)
- Primary button for main actions (#10B981 background)
- Secondary/ghost buttons for alternative actions
- Loading states during form submission
- Error messages displayed below inputs (red, #EF4444)

## Visual Design

No visual mockups provided. Follow design system guidelines:

**Auth Pages Layout**
- Full-screen centered layout with dark background (#0D0D0D)
- Card container: max-width 400px, #171717 background, 8px border-radius
- Simple text logo "AgentOS Tracker" above form
- Generous padding (32px) inside card
- Form elements stacked vertically with 16px spacing

**Form Elements**
- Input fields: 40px height, full width, #171717 background, #2E2E2E border
- Focus state: #10B981 border with subtle ring
- Labels: 14px, #A3A3A3 color, above input
- Error text: 13px, #EF4444 color, below input
- Buttons: 40px height, full width, 8px border-radius

## Existing Code to Leverage

**lib/supabase/client.ts - Browser Supabase Client**
- Already configured with createBrowserClient from @supabase/ssr
- Uses environment variables for URL and anon key
- Use this client for client-side auth operations (login, signup, logout)
- Extend with auth event listeners for session state management

**lib/supabase/server.ts - Server Supabase Client**
- Async createClient function for Server Components
- Handles cookies for session management
- Use for server-side session validation in protected routes
- Use for fetching user profile data in SSR

**lib/supabase/middleware.ts - Session Refresh Middleware**
- updateSession function refreshes auth tokens automatically
- Already integrated with Next.js middleware
- Extend to add route protection logic (redirect unauthenticated users)
- Add logic to redirect authenticated users away from auth pages

**middleware.ts - Next.js Middleware Entry**
- Currently calls updateSession for all matched routes
- Extend to implement auth redirect logic
- Public routes: /login, /signup, /forgot-password, /reset-password
- Protected routes: /dashboard and all (dashboard) routes

**lib/validations/task.ts - Zod Schema Pattern**
- Reference for creating auth validation schemas
- Follow same pattern: define schema, export type inference
- Create: signupSchema, loginSchema, forgotPasswordSchema, resetPasswordSchema

## Out of Scope

- OAuth/social login providers (Google, GitHub) - deferred to Phase 3
- Two-factor authentication (2FA/MFA)
- Single sign-on (SSO/SAML)
- Role-based access control (RBAC) or admin roles
- "Remember me" checkbox functionality
- Account deletion or deactivation
- Profile editing after initial signup (separate feature)
- User preferences or settings
- Session listing or "sign out all devices"
- Rate limiting (handled at infrastructure level)
