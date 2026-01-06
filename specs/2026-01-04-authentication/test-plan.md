# Test Plan: Authentication with Supabase Auth

## Metadata
- **Feature**: Authentication with Supabase Auth
- **Spec**: agent-os/specs/2026-01-04-authentication/spec.md
- **Requirements**: agent-os/specs/2026-01-04-authentication/planning/requirements.md
- **Created**: 2026-01-04
- **Status**: Planning Complete
- **Tech Stack**: Next.js 14, Supabase Auth, Vitest (unit), Playwright (E2E)

---

## Test Summary

| Layer | Critical | High | Medium | Low | Total |
|-------|----------|------|--------|-----|-------|
| Database | 4 | 3 | 2 | 0 | 9 |
| API | 12 | 8 | 6 | 2 | 28 |
| UI | 8 | 10 | 8 | 4 | 30 |
| E2E | 8 | 4 | 2 | 0 | 14 |
| **Total** | **32** | **25** | **18** | **6** | **81** |

**Coverage Targets:**
- Critical paths: 100%
- High priority: 100%
- Medium priority: 80%
- Low priority: Deferred to QA phase

---

## Database Layer

### Profiles Table Schema (9 tests)

#### 1. test_profiles_table_exists_with_correct_columns
**Priority:** Critical
**Given:**
- Database schema is migrated
**When:** Query the profiles table structure
**Then:**
- Table `profiles` exists
- Columns exist: `id` (UUID), `display_name` (TEXT), `avatar_url` (TEXT), `created_at` (TIMESTAMPTZ), `updated_at` (TIMESTAMPTZ)
- `id` is primary key and foreign key to `auth.users(id)`
**Related Requirement:** spec.md "User Profile Table"

#### 2. test_profile_id_references_auth_users
**Priority:** Critical
**Given:**
- profiles table exists
**When:** Check foreign key constraint on id column
**Then:**
- Foreign key constraint exists referencing auth.users(id)
- ON DELETE CASCADE is configured
**Related Requirement:** spec.md "User Profile Table - id (FK to auth.users)"

#### 3. test_profile_created_at_has_default_now
**Priority:** High
**Given:**
- profiles table exists
**When:** Insert a profile without specifying created_at
**Then:**
- created_at is automatically set to current timestamp
**Related Requirement:** spec.md "User Profile Table - created_at"

#### 4. test_profile_updated_at_has_default_now
**Priority:** High
**Given:**
- profiles table exists
**When:** Insert a profile without specifying updated_at
**Then:**
- updated_at is automatically set to current timestamp
**Related Requirement:** spec.md "User Profile Table - updated_at"

#### 5. test_profile_trigger_creates_profile_on_user_signup
**Priority:** Critical
**Given:**
- Database trigger for auto-creating profiles is in place
- No profile exists for user
**When:** A new user is created in auth.users
**Then:**
- A corresponding profile is automatically created
- Profile id matches auth.users id
- display_name is populated from user metadata if provided
- avatar_url is generated from Gravatar hash
**Related Requirement:** spec.md "Profile created automatically via database trigger on user signup"

#### 6. test_rls_user_can_read_own_profile
**Priority:** Critical
**Given:**
- User A is authenticated
- Profile exists for User A
**When:** User A queries their own profile
**Then:**
- Query succeeds
- Profile data is returned
**Related Requirement:** spec.md "Row Level Security (RLS) policies for user-only access"

#### 7. test_rls_user_cannot_read_other_profiles
**Priority:** High
**Given:**
- User A is authenticated
- Profile exists for User B
**When:** User A attempts to query User B's profile
**Then:**
- Query returns empty result (not an error)
- User B's profile data is not accessible
**Related Requirement:** spec.md "Row Level Security (RLS) policies for user-only access"

#### 8. test_rls_user_can_update_own_profile
**Priority:** Medium
**Given:**
- User A is authenticated
- Profile exists for User A
**When:** User A updates their profile (display_name, avatar_url)
**Then:**
- Update succeeds
- updated_at is refreshed
**Related Requirement:** spec.md "Row Level Security (RLS) policies for user-only access"

#### 9. test_rls_user_cannot_update_other_profiles
**Priority:** Medium
**Given:**
- User A is authenticated
- Profile exists for User B
**When:** User A attempts to update User B's profile
**Then:**
- Update fails or affects 0 rows
- User B's profile remains unchanged
**Related Requirement:** spec.md "Row Level Security (RLS) policies for user-only access"

---

## API Layer

### POST /auth/signup (7 tests)

#### 10. test_signup_with_valid_data_creates_user
**Priority:** Critical
**Given:**
- Request body: `{"email": "newuser@test.com", "password": "password123", "displayName": "New User"}`
- No user exists with this email
**When:** POST /auth/signup
**Then:**
- Status: 201 Created
- Response contains user id
- User is created in auth.users
- Profile is created in profiles table
- Confirmation email is sent (Supabase handles)
**Related Requirement:** spec.md "Email/Password Authentication - Users register with email, password, and display name"

#### 11. test_signup_without_email_returns_400
**Priority:** High
**Given:**
- Request body: `{"password": "password123", "displayName": "User"}`
**When:** POST /auth/signup
**Then:**
- Status: 400 Bad Request
- Error message indicates email is required
**Related Requirement:** spec.md "Email/Password Authentication"

#### 12. test_signup_with_invalid_email_returns_400
**Priority:** High
**Given:**
- Request body: `{"email": "not-an-email", "password": "password123", "displayName": "User"}`
**When:** POST /auth/signup
**Then:**
- Status: 400 Bad Request
- Error message indicates invalid email format
**Related Requirement:** spec.md "Email/Password Authentication"

#### 13. test_signup_with_short_password_returns_400
**Priority:** Critical
**Given:**
- Request body: `{"email": "user@test.com", "password": "short", "displayName": "User"}`
- Password is less than 8 characters
**When:** POST /auth/signup
**Then:**
- Status: 400 Bad Request
- Error message indicates password must be at least 8 characters
**Related Requirement:** spec.md "Password minimum 8 characters"

#### 14. test_signup_with_duplicate_email_returns_409
**Priority:** Critical
**Given:**
- User exists with email "existing@test.com"
- Request body: `{"email": "existing@test.com", "password": "password123", "displayName": "User"}`
**When:** POST /auth/signup
**Then:**
- Status: 409 Conflict
- Error message indicates email already registered
- No new user is created
**Related Requirement:** spec.md "Email must be unique across the system"

#### 15. test_signup_generates_gravatar_avatar_url
**Priority:** Medium
**Given:**
- Request body with email "test@example.com"
**When:** POST /auth/signup succeeds
**Then:**
- Profile avatar_url contains Gravatar URL
- URL contains MD5 hash of lowercase email
- Hash of "test@example.com" = "55502f40dc8b7c769880b10874abc9d0"
**Related Requirement:** spec.md "Avatar URL generated from Gravatar using email hash (MD5)"

#### 16. test_signup_without_display_name_returns_400
**Priority:** Medium
**Given:**
- Request body: `{"email": "user@test.com", "password": "password123"}`
- displayName is missing
**When:** POST /auth/signup
**Then:**
- Status: 400 Bad Request
- Error message indicates display name is required
**Related Requirement:** spec.md "Users register with email, password, and display name"

---

### POST /auth/login (6 tests)

#### 17. test_login_with_valid_credentials_returns_session
**Priority:** Critical
**Given:**
- User exists with email "user@test.com" and password "password123"
- User email is verified
**When:** POST /auth/login with `{"email": "user@test.com", "password": "password123"}`
**Then:**
- Status: 200 OK
- Response contains session token
- Session cookie is set (HTTP-only)
**Related Requirement:** spec.md "Login form validates credentials against Supabase Auth"

#### 18. test_login_with_wrong_password_returns_401
**Priority:** Critical
**Given:**
- User exists with email "user@test.com"
**When:** POST /auth/login with `{"email": "user@test.com", "password": "wrongpassword"}`
**Then:**
- Status: 401 Unauthorized
- Error message: "Invalid credentials" (generic for security)
**Related Requirement:** spec.md "Display appropriate error messages for invalid credentials"

#### 19. test_login_with_nonexistent_email_returns_401
**Priority:** Critical
**Given:**
- No user exists with email "nobody@test.com"
**When:** POST /auth/login with `{"email": "nobody@test.com", "password": "anypassword"}`
**Then:**
- Status: 401 Unauthorized
- Error message: "Invalid credentials" (same as wrong password for security)
**Related Requirement:** spec.md "Display appropriate error messages for invalid credentials"

#### 20. test_login_with_unverified_email_returns_403
**Priority:** High
**Given:**
- User exists but email is not verified
**When:** POST /auth/login with valid credentials
**Then:**
- Status: 403 Forbidden
- Error message indicates email verification required
- Response includes flag: `emailVerified: false`
**Related Requirement:** spec.md "Email verification required before accessing protected routes"

#### 21. test_login_sets_session_with_30_day_expiry
**Priority:** High
**Given:**
- User exists with verified email
**When:** POST /auth/login with valid credentials
**Then:**
- Session token has expiry approximately 30 days from now
**Related Requirement:** spec.md "30-day session duration configured in Supabase"

#### 22. test_login_without_email_returns_400
**Priority:** Medium
**Given:**
- Request body missing email field
**When:** POST /auth/login with `{"password": "password123"}`
**Then:**
- Status: 400 Bad Request
- Error message indicates email is required
**Related Requirement:** spec.md "Email/Password Authentication"

---

### POST /auth/magic-link (5 tests)

#### 23. test_magic_link_with_valid_email_sends_email
**Priority:** Critical
**Given:**
- User exists with email "user@test.com"
**When:** POST /auth/magic-link with `{"email": "user@test.com"}`
**Then:**
- Status: 200 OK
- Response message confirms email sent
- Magic link email is triggered (Supabase handles delivery)
**Related Requirement:** spec.md "User enters email address to receive magic link"

#### 24. test_magic_link_with_nonexistent_email_returns_200
**Priority:** High
**Given:**
- No user exists with email "nobody@test.com"
**When:** POST /auth/magic-link with `{"email": "nobody@test.com"}`
**Then:**
- Status: 200 OK (security: don't reveal if email exists)
- Response message is same as success case
**Related Requirement:** spec.md "Magic Link Authentication"

#### 25. test_magic_link_without_email_returns_400
**Priority:** Medium
**Given:**
- Request body is empty or missing email
**When:** POST /auth/magic-link with `{}`
**Then:**
- Status: 400 Bad Request
- Error message indicates email is required
**Related Requirement:** spec.md "Magic Link Authentication"

#### 26. test_magic_link_with_invalid_email_format_returns_400
**Priority:** Medium
**Given:**
- Request body with invalid email format
**When:** POST /auth/magic-link with `{"email": "not-valid"}`
**Then:**
- Status: 400 Bad Request
- Error message indicates invalid email format
**Related Requirement:** spec.md "Magic Link Authentication"

#### 27. test_magic_link_callback_authenticates_user
**Priority:** Critical
**Given:**
- Valid magic link token exists for user
**When:** User clicks magic link (GET /auth/callback?token=...)
**Then:**
- User is authenticated
- Session is created
- User is redirected to dashboard
**Related Requirement:** spec.md "Clicking link authenticates user and redirects to dashboard"

---

### POST /auth/forgot-password (4 tests)

#### 28. test_forgot_password_with_valid_email_sends_reset_email
**Priority:** Critical
**Given:**
- User exists with email "user@test.com"
**When:** POST /auth/forgot-password with `{"email": "user@test.com"}`
**Then:**
- Status: 200 OK
- Response confirms email sent
- Password reset email is triggered (Supabase handles)
**Related Requirement:** spec.md "Forgot password page collects email address"

#### 29. test_forgot_password_with_nonexistent_email_returns_200
**Priority:** High
**Given:**
- No user exists with email "nobody@test.com"
**When:** POST /auth/forgot-password with `{"email": "nobody@test.com"}`
**Then:**
- Status: 200 OK (security: don't reveal if email exists)
- Response message is same as success case
**Related Requirement:** spec.md "Password Reset Flow"

#### 30. test_forgot_password_without_email_returns_400
**Priority:** Medium
**Given:**
- Request body is empty
**When:** POST /auth/forgot-password with `{}`
**Then:**
- Status: 400 Bad Request
- Error indicates email is required
**Related Requirement:** spec.md "Password Reset Flow"

#### 31. test_forgot_password_with_invalid_email_returns_400
**Priority:** Low
**Given:**
- Request body with invalid email format
**When:** POST /auth/forgot-password with `{"email": "invalid"}`
**Then:**
- Status: 400 Bad Request
- Error indicates invalid email format
**Related Requirement:** spec.md "Password Reset Flow"

---

### POST /auth/reset-password (6 tests)

#### 32. test_reset_password_with_valid_token_updates_password
**Priority:** Critical
**Given:**
- Valid password reset token exists
- Request body: `{"token": "valid-token", "password": "newpassword123"}`
**When:** POST /auth/reset-password
**Then:**
- Status: 200 OK
- Password is updated
- User can login with new password
- Old password no longer works
**Related Requirement:** spec.md "Reset password page validates token from URL"

#### 33. test_reset_password_with_expired_token_returns_401
**Priority:** Critical
**Given:**
- Password reset token is expired
**When:** POST /auth/reset-password with expired token
**Then:**
- Status: 401 Unauthorized
- Error indicates token is expired
- Password is not changed
**Related Requirement:** spec.md "Reset password page validates token from URL"

#### 34. test_reset_password_with_invalid_token_returns_401
**Priority:** High
**Given:**
- Token is invalid/malformed
**When:** POST /auth/reset-password with invalid token
**Then:**
- Status: 401 Unauthorized
- Error indicates invalid token
**Related Requirement:** spec.md "Reset password page validates token from URL"

#### 35. test_reset_password_with_short_password_returns_400
**Priority:** High
**Given:**
- Valid token
- New password is less than 8 characters
**When:** POST /auth/reset-password with `{"token": "valid", "password": "short"}`
**Then:**
- Status: 400 Bad Request
- Error indicates password must be at least 8 characters
- Password is not changed
**Related Requirement:** spec.md "New password form with 8-character minimum validation"

#### 36. test_reset_password_without_token_returns_400
**Priority:** Medium
**Given:**
- Request body missing token
**When:** POST /auth/reset-password with `{"password": "newpassword"}`
**Then:**
- Status: 400 Bad Request
- Error indicates token is required
**Related Requirement:** spec.md "Password Reset Flow"

#### 37. test_reset_password_invalidates_token_after_use
**Priority:** Low
**Given:**
- Valid password reset token
**When:** POST /auth/reset-password succeeds, then same request is sent again
**Then:**
- First request: 200 OK
- Second request: 401 Unauthorized (token already used)
**Related Requirement:** spec.md "Password Reset Flow"

---

### POST /auth/logout (2 tests)

#### 38. test_logout_clears_session
**Priority:** Critical
**Given:**
- User is authenticated with valid session
**When:** POST /auth/logout
**Then:**
- Status: 200 OK
- Session cookie is cleared
- Subsequent authenticated requests fail
**Related Requirement:** spec.md "Logout clears session and redirects to login page"

#### 39. test_logout_when_not_authenticated_returns_200
**Priority:** Low
**Given:**
- No active session
**When:** POST /auth/logout
**Then:**
- Status: 200 OK (idempotent operation)
**Related Requirement:** spec.md "Session Management"

---

### GET /auth/session (3 tests)

#### 40. test_session_returns_user_data_when_authenticated
**Priority:** High
**Given:**
- User is authenticated
**When:** GET /auth/session
**Then:**
- Status: 200 OK
- Response includes user id, email, profile data
**Related Requirement:** spec.md "Session Management"

#### 41. test_session_returns_null_when_not_authenticated
**Priority:** High
**Given:**
- No active session
**When:** GET /auth/session
**Then:**
- Status: 200 OK
- Response: `{"user": null}`
**Related Requirement:** spec.md "Session Management"

#### 42. test_session_refreshes_token_automatically
**Priority:** Medium
**Given:**
- User has valid session approaching expiry
**When:** GET /auth/session
**Then:**
- Session token is refreshed
- New token has extended expiry
**Related Requirement:** spec.md "Automatic token refresh via middleware on each request"

---

### POST /auth/resend-verification (3 tests)

#### 43. test_resend_verification_sends_email
**Priority:** High
**Given:**
- User exists with unverified email
**When:** POST /auth/resend-verification with `{"email": "unverified@test.com"}`
**Then:**
- Status: 200 OK
- Verification email is sent
**Related Requirement:** spec.md "Resend verification email option available"

#### 44. test_resend_verification_for_already_verified_returns_200
**Priority:** Medium
**Given:**
- User exists with verified email
**When:** POST /auth/resend-verification with `{"email": "verified@test.com"}`
**Then:**
- Status: 200 OK (don't reveal verification status)
**Related Requirement:** spec.md "Email Verification"

#### 45. test_resend_verification_for_nonexistent_returns_200
**Priority:** Medium
**Given:**
- No user exists with the email
**When:** POST /auth/resend-verification with `{"email": "nobody@test.com"}`
**Then:**
- Status: 200 OK (security: don't reveal if email exists)
**Related Requirement:** spec.md "Email Verification"

---

## UI Layer

### Login Page Component (8 tests)

#### 46. test_login_page_renders_email_password_form
**Priority:** Critical
**Given:**
- User navigates to /login
- User is not authenticated
**When:** Page loads
**Then:**
- Email input field is visible with label
- Password input field is visible with label
- "Login" submit button is visible
- "Forgot password?" link is visible
- "Sign up" link is visible
- "Magic link" option is visible
**Related Requirement:** spec.md "Auth UI Components"

#### 47. test_login_form_validates_email_format
**Priority:** High
**Given:**
- Login page is rendered
**When:** User enters "invalid-email" in email field and submits
**Then:**
- Form does not submit
- Error message "Invalid email address" appears below email input
- Error text is red (#EF4444)
**Related Requirement:** spec.md "Error messages displayed below inputs (red, #EF4444)"

#### 48. test_login_form_requires_password
**Priority:** High
**Given:**
- Login page is rendered
**When:** User enters email but leaves password empty and submits
**Then:**
- Form does not submit
- Error message appears indicating password is required
**Related Requirement:** spec.md "Email/Password Authentication"

#### 49. test_login_shows_loading_state_during_submission
**Priority:** Medium
**Given:**
- Login page is rendered
- User has entered valid credentials
**When:** User clicks login button
**Then:**
- Button shows loading indicator
- Button is disabled during loading
- Form inputs are disabled
**Related Requirement:** spec.md "Loading states during form submission"

#### 50. test_login_displays_server_error_message
**Priority:** High
**Given:**
- Login page is rendered
**When:** Server returns 401 with "Invalid credentials" error
**Then:**
- Error message "Invalid credentials" is displayed
- Error is visible near form (not in input field)
**Related Requirement:** spec.md "Display appropriate error messages for invalid credentials"

#### 51. test_login_redirects_to_dashboard_on_success
**Priority:** Critical
**Given:**
- Login page is rendered
- User enters valid credentials
**When:** Login API returns success
**Then:**
- User is redirected to /dashboard
**Related Requirement:** spec.md "Redirect to dashboard on successful authentication"

#### 52. test_login_magic_link_toggle_shows_email_only_form
**Priority:** Medium
**Given:**
- Login page is rendered
**When:** User clicks "Use magic link" option
**Then:**
- Password field is hidden
- Only email field is visible
- Submit button text changes to "Send magic link"
**Related Requirement:** spec.md "Alternative passwordless login option on login page"

#### 53. test_login_magic_link_shows_success_message
**Priority:** Medium
**Given:**
- Login page in magic link mode
- User enters valid email
**When:** Magic link request succeeds
**Then:**
- Success message "Check your email for the login link" is displayed
- Form is hidden or disabled
**Related Requirement:** spec.md "Show success message after sending magic link email"

---

### Signup Page Component (8 tests)

#### 54. test_signup_page_renders_registration_form
**Priority:** Critical
**Given:**
- User navigates to /signup
- User is not authenticated
**When:** Page loads
**Then:**
- Email input field is visible
- Password input field is visible
- Display name input field is visible
- "Sign up" submit button is visible
- "Already have an account? Login" link is visible
**Related Requirement:** spec.md "Auth UI Components"

#### 55. test_signup_form_validates_email_format
**Priority:** High
**Given:**
- Signup page is rendered
**When:** User enters invalid email and submits
**Then:**
- Error message for invalid email is shown
- Form does not submit
**Related Requirement:** spec.md "Email/Password Authentication"

#### 56. test_signup_form_validates_password_minimum_length
**Priority:** Critical
**Given:**
- Signup page is rendered
**When:** User enters password with less than 8 characters
**Then:**
- Error message "Password must be at least 8 characters" appears
- Form does not submit
**Related Requirement:** spec.md "Password minimum 8 characters"

#### 57. test_signup_form_requires_display_name
**Priority:** High
**Given:**
- Signup page is rendered
**When:** User leaves display name empty and submits
**Then:**
- Error message indicates display name is required
- Form does not submit
**Related Requirement:** spec.md "Users register with email, password, and display name"

#### 58. test_signup_shows_loading_state_during_submission
**Priority:** Medium
**Given:**
- Signup page is rendered
- User has filled all fields with valid data
**When:** User clicks signup button
**Then:**
- Button shows loading indicator
- Button and inputs are disabled
**Related Requirement:** spec.md "Loading states during form submission"

#### 59. test_signup_displays_duplicate_email_error
**Priority:** High
**Given:**
- Signup page is rendered
**When:** Server returns 409 Conflict for duplicate email
**Then:**
- Error message "Email already registered" is displayed
**Related Requirement:** spec.md "Email must be unique across the system"

#### 60. test_signup_success_redirects_to_verification_pending
**Priority:** Critical
**Given:**
- Signup page is rendered
- User submits valid registration data
**When:** Signup API returns success
**Then:**
- User is redirected to verification pending page
- Success message indicates email verification required
**Related Requirement:** spec.md "All new signups require email verification"

#### 61. test_signup_password_field_has_show_hide_toggle
**Priority:** Low
**Given:**
- Signup page is rendered
**When:** User clicks show/hide password icon
**Then:**
- Password field toggles between type="password" and type="text"
**Related Requirement:** spec.md "Form inputs follow design system"

---

### Forgot Password Page Component (5 tests)

#### 62. test_forgot_password_page_renders_email_form
**Priority:** Critical
**Given:**
- User navigates to /forgot-password
**When:** Page loads
**Then:**
- Email input field is visible
- "Reset password" submit button is visible
- "Back to login" link is visible
**Related Requirement:** spec.md "Forgot password page collects email address"

#### 63. test_forgot_password_validates_email_format
**Priority:** High
**Given:**
- Forgot password page is rendered
**When:** User enters invalid email and submits
**Then:**
- Error message for invalid email is shown
**Related Requirement:** spec.md "Password Reset Flow"

#### 64. test_forgot_password_shows_success_message
**Priority:** High
**Given:**
- Forgot password page is rendered
- User enters valid email
**When:** Request succeeds
**Then:**
- Success message "Check your email for reset instructions" is displayed
- Form is hidden or shows confirmation state
**Related Requirement:** spec.md "Supabase sends password reset email"

#### 65. test_forgot_password_shows_loading_state
**Priority:** Medium
**Given:**
- Forgot password page is rendered
**When:** User submits form
**Then:**
- Button shows loading indicator
**Related Requirement:** spec.md "Loading states during form submission"

#### 66. test_forgot_password_allows_resend
**Priority:** Low
**Given:**
- Forgot password success state is shown
**When:** User clicks "Resend email" link
**Then:**
- New reset email request is sent
- Loading state shows during request
**Related Requirement:** spec.md "Password Reset Flow"

---

### Reset Password Page Component (6 tests)

#### 67. test_reset_password_page_renders_password_form
**Priority:** Critical
**Given:**
- User navigates to /reset-password with valid token in URL
**When:** Page loads
**Then:**
- New password input field is visible
- Confirm password input field is visible
- "Set new password" submit button is visible
**Related Requirement:** spec.md "Reset password page validates token from URL"

#### 68. test_reset_password_validates_password_minimum
**Priority:** Critical
**Given:**
- Reset password page is rendered
**When:** User enters password with less than 8 characters
**Then:**
- Error message about minimum length is shown
**Related Requirement:** spec.md "New password form with 8-character minimum validation"

#### 69. test_reset_password_validates_password_confirmation_match
**Priority:** High
**Given:**
- Reset password page is rendered
**When:** User enters different values in password and confirm fields
**Then:**
- Error message "Passwords do not match" is shown
**Related Requirement:** spec.md "Password Reset Flow"

#### 70. test_reset_password_success_redirects_to_login
**Priority:** High
**Given:**
- Reset password page is rendered with valid token
- User enters valid new password
**When:** Reset API returns success
**Then:**
- User is redirected to /login
- Success message "Password updated successfully" is shown
**Related Requirement:** spec.md "Success redirects to login page with confirmation message"

#### 71. test_reset_password_shows_invalid_token_error
**Priority:** High
**Given:**
- User navigates to /reset-password with invalid/expired token
**When:** Page loads or form is submitted
**Then:**
- Error message "Invalid or expired reset link" is shown
- Link to request new reset email is provided
**Related Requirement:** spec.md "Reset password page validates token from URL"

#### 72. test_reset_password_shows_loading_state
**Priority:** Medium
**Given:**
- Reset password page is rendered
**When:** User submits form
**Then:**
- Button shows loading indicator
**Related Requirement:** spec.md "Loading states during form submission"

---

### Verification Pending Page Component (3 tests)

#### 73. test_verification_pending_page_shows_instructions
**Priority:** High
**Given:**
- User has signed up but not verified email
- User navigates to /verification-pending
**When:** Page loads
**Then:**
- Message explains to check email for verification link
- Email address is displayed
- "Resend verification email" button is visible
**Related Requirement:** spec.md "Unverified users redirected to verification pending page"

#### 74. test_verification_pending_resend_button_works
**Priority:** High
**Given:**
- Verification pending page is rendered
**When:** User clicks "Resend verification email"
**Then:**
- Loading state shows
- Success message "Verification email sent" appears
**Related Requirement:** spec.md "Resend verification email option available"

#### 75. test_verification_pending_resend_has_cooldown
**Priority:** Low
**Given:**
- User just clicked resend button
**When:** User tries to click resend again immediately
**Then:**
- Button is disabled for cooldown period
- Countdown or message indicates wait time
**Related Requirement:** spec.md "Resend verification email option available"

---

### Auth Layout Component (4 tests)

#### 76. test_auth_layout_renders_centered_card
**Priority:** Medium
**Given:**
- Any auth page is rendered
**When:** Page loads
**Then:**
- Content is centered on screen
- Card container has max-width 400px
- Background is dark (#0D0D0D)
- Card has #171717 background
**Related Requirement:** spec.md "Visual Design - Auth Pages Layout"

#### 77. test_auth_layout_shows_logo
**Priority:** Medium
**Given:**
- Any auth page is rendered
**When:** Page loads
**Then:**
- "AgentOS Tracker" logo/text is visible above form
**Related Requirement:** spec.md "Simple text logo 'AgentOS Tracker' above form"

#### 78. test_auth_form_inputs_follow_design_system
**Priority:** Low
**Given:**
- Any auth form is rendered
**When:** Inspecting input styles
**Then:**
- Input height is 40px
- Input background is #171717
- Input border is #2E2E2E
- Focus state shows #10B981 border
**Related Requirement:** spec.md "Form inputs follow design system (40px height, 6px border-radius, #171717 background)"

#### 79. test_auth_buttons_follow_design_system
**Priority:** Low
**Given:**
- Any auth form is rendered
**When:** Inspecting button styles
**Then:**
- Primary button has #10B981 background
- Button height is 40px
- Button has 8px border-radius
**Related Requirement:** spec.md "Primary button for main actions (#10B981 background)"

---

### Route Protection / Middleware (4 tests)

#### 80. test_dashboard_redirects_to_login_when_not_authenticated
**Priority:** Critical
**Given:**
- User is not authenticated (no session)
**When:** User navigates to /dashboard
**Then:**
- User is redirected to /login
- Original destination may be stored for post-login redirect
**Related Requirement:** spec.md "Dashboard routes require authenticated session"

#### 81. test_auth_routes_redirect_to_dashboard_when_authenticated
**Priority:** High
**Given:**
- User is authenticated
**When:** User navigates to /login or /signup
**Then:**
- User is redirected to /dashboard
**Related Requirement:** spec.md "Auth routes redirect to dashboard if already authenticated"

#### 82. test_protected_route_allows_authenticated_user
**Priority:** Critical
**Given:**
- User is authenticated with valid session
**When:** User navigates to /dashboard
**Then:**
- Page loads successfully
- User data is available
**Related Requirement:** spec.md "Dashboard routes require authenticated session"

#### 83. test_unverified_user_redirected_to_verification_page
**Priority:** High
**Given:**
- User is authenticated but email is not verified
**When:** User navigates to /dashboard
**Then:**
- User is redirected to /verification-pending
**Related Requirement:** spec.md "Unverified users redirected to verification pending page"

---

## E2E Tests (Playwright)

### User Signup Journey (3 tests)

#### e2e_signup_complete_flow
**Priority:** Critical
**Preconditions:**
- Fresh test database
- Valid SMTP configuration for test emails
**Steps:**
1. Navigate to /signup
2. Fill in email, password (8+ chars), display name
3. Click "Sign up" button
4. Verify redirect to verification pending page
5. (If email accessible) Click verification link
6. Verify redirect to login with success message
**Success Criteria:**
- User created in database
- Profile created with display name
- Avatar URL is Gravatar hash
- Email verification flow completes
**Related User Story:** requirements.md "User signs up with email/password"

#### e2e_signup_validation_errors
**Priority:** High
**Preconditions:**
- Application running
**Steps:**
1. Navigate to /signup
2. Try submit with empty form - verify all validation errors
3. Enter invalid email - verify email error
4. Enter short password (< 8 chars) - verify password error
5. Fix errors and verify form submits
**Success Criteria:**
- All client-side validations work
- Error messages are visible and helpful
**Related User Story:** requirements.md "User signs up with email/password"

#### e2e_signup_duplicate_email
**Priority:** High
**Preconditions:**
- User already exists with test email
**Steps:**
1. Navigate to /signup
2. Enter existing email address
3. Fill valid password and display name
4. Submit form
5. Verify error message for duplicate email
**Success Criteria:**
- 409 error is displayed user-friendly
- Form remains with data intact
**Related User Story:** requirements.md "User signs up with email/password"

---

### User Login Journey (4 tests)

#### e2e_login_with_email_password
**Priority:** Critical
**Preconditions:**
- Verified user exists
**Steps:**
1. Navigate to /login
2. Enter valid email and password
3. Click login button
4. Verify redirect to /dashboard
5. Verify user profile data is displayed
**Success Criteria:**
- Session is established
- Dashboard shows user info
**Related User Story:** requirements.md "User logs in with email/password"

#### e2e_login_with_magic_link
**Priority:** Critical
**Preconditions:**
- Verified user exists
- Email inbox accessible for testing
**Steps:**
1. Navigate to /login
2. Click "Use magic link" option
3. Enter email address
4. Click "Send magic link"
5. Verify success message
6. (Access email) Click magic link
7. Verify redirect to dashboard
**Success Criteria:**
- Magic link email received
- Clicking link authenticates user
- Session is established
**Related User Story:** requirements.md "User logs in with magic link"

#### e2e_login_invalid_credentials
**Priority:** High
**Preconditions:**
- User exists with known password
**Steps:**
1. Navigate to /login
2. Enter correct email, wrong password
3. Click login
4. Verify error message displayed
5. Enter wrong email, any password
6. Click login
7. Verify same error message (security)
**Success Criteria:**
- Generic "Invalid credentials" error shown
- No indication which field was wrong
**Related User Story:** requirements.md "User logs in with email/password"

#### e2e_login_unverified_user
**Priority:** High
**Preconditions:**
- User exists with unverified email
**Steps:**
1. Navigate to /login
2. Enter valid credentials for unverified user
3. Click login
4. Verify redirect to verification pending page
5. Verify resend verification option available
**Success Criteria:**
- User cannot access dashboard
- Clear path to verify email
**Related User Story:** requirements.md "User verifies email"

---

### Password Reset Journey (3 tests)

#### e2e_password_reset_complete_flow
**Priority:** Critical
**Preconditions:**
- Verified user exists
- Email inbox accessible
**Steps:**
1. Navigate to /login
2. Click "Forgot password?"
3. Enter email address
4. Submit form
5. Verify success message
6. (Access email) Click reset link
7. Enter new password (8+ chars)
8. Confirm new password
9. Submit form
10. Verify redirect to login with success message
11. Login with new password
**Success Criteria:**
- Reset email received
- Password successfully changed
- Old password no longer works
- New password works
**Related User Story:** requirements.md "User requests password reset" & "User resets password"

#### e2e_password_reset_invalid_token
**Priority:** High
**Preconditions:**
- None
**Steps:**
1. Navigate to /reset-password with invalid token
2. Try to submit new password
3. Verify error about invalid/expired token
4. Verify link to request new reset
**Success Criteria:**
- Clear error message
- Path to request new reset
**Related User Story:** requirements.md "User resets password"

#### e2e_password_reset_validation
**Priority:** Medium
**Preconditions:**
- Valid reset token
**Steps:**
1. Navigate to reset password page with valid token
2. Enter password < 8 characters
3. Verify validation error
4. Enter mismatched passwords
5. Verify mismatch error
6. Enter valid matching passwords
7. Verify success
**Success Criteria:**
- Client-side validation works
- Password requirements enforced
**Related User Story:** requirements.md "User resets password"

---

### Route Protection Journey (2 tests)

#### e2e_protected_route_unauthenticated
**Priority:** Critical
**Preconditions:**
- No active session
**Steps:**
1. Navigate directly to /dashboard
2. Verify redirect to /login
3. Login with valid credentials
4. Verify redirect back to /dashboard
**Success Criteria:**
- Unauthenticated users cannot access dashboard
- Post-login redirect works
**Related User Story:** requirements.md "User is redirected when not authenticated"

#### e2e_auth_route_authenticated
**Priority:** High
**Preconditions:**
- User is logged in
**Steps:**
1. Navigate to /login
2. Verify redirect to /dashboard
3. Navigate to /signup
4. Verify redirect to /dashboard
**Success Criteria:**
- Authenticated users skip auth pages
**Related User Story:** requirements.md "User accesses protected route (authenticated)"

---

### Session Management Journey (2 tests)

#### e2e_logout_clears_session
**Priority:** Critical
**Preconditions:**
- User is logged in
**Steps:**
1. Verify user is on dashboard
2. Click logout button
3. Verify redirect to /login
4. Try to navigate to /dashboard
5. Verify redirect back to /login
**Success Criteria:**
- Session completely cleared
- Protected routes inaccessible after logout
**Related User Story:** requirements.md "Session Management"

#### e2e_session_persists_across_refresh
**Priority:** Medium
**Preconditions:**
- User is logged in
**Steps:**
1. Verify user is on dashboard
2. Refresh the page (F5)
3. Verify still on dashboard
4. Verify user data still displayed
5. Close and reopen browser tab
6. Navigate to /dashboard
7. Verify still authenticated
**Success Criteria:**
- Session persists across page refreshes
- Session persists in same browser session
**Related User Story:** requirements.md "30-day session duration"

---

## Test Dependencies

### Execution Order Requirements

1. **Database tests first**: Schema and RLS tests must pass before API tests
2. **API tests before UI**: API endpoints must work before testing UI interactions
3. **Unit tests before integration**: Individual components tested before flows
4. **E2E tests last**: Full flow tests run after all unit/integration pass

### Specific Dependencies

| Test | Depends On |
|------|------------|
| test_profile_trigger_creates_profile_on_user_signup | test_profiles_table_exists_with_correct_columns |
| test_login_with_valid_credentials_returns_session | test_signup_with_valid_data_creates_user |
| test_magic_link_callback_authenticates_user | test_magic_link_with_valid_email_sends_email |
| test_reset_password_with_valid_token_updates_password | test_forgot_password_with_valid_email_sends_reset_email |
| All UI tests | Corresponding API tests |
| All E2E tests | All unit and integration tests |

---

## Test Data Requirements

### Test Users

| User Type | Email | Password | Status |
|-----------|-------|----------|--------|
| Verified User | verified@test.com | Test1234 | Email verified |
| Unverified User | unverified@test.com | Test1234 | Email not verified |
| Password Reset User | reset@test.com | OldPass123 | For password reset tests |

### Test Fixtures

```typescript
// fixtures/auth.ts
export const validSignupData = {
  email: 'newuser@test.com',
  password: 'password123',
  displayName: 'Test User'
};

export const invalidEmails = [
  'not-an-email',
  '@missing-local.com',
  'missing-domain@',
  'spaces in@email.com'
];

export const shortPasswords = [
  '',
  '1',
  '1234567'  // 7 chars
];

export const validPasswords = [
  '12345678',     // exactly 8 chars
  'password123',  // common format
  'a'.repeat(100) // long password
];
```

### Mock Responses

```typescript
// mocks/supabase.ts
export const mockAuthResponses = {
  signupSuccess: {
    user: { id: 'uuid', email: 'user@test.com' },
    session: null // Email confirmation required
  },
  loginSuccess: {
    user: { id: 'uuid', email: 'user@test.com', email_confirmed_at: '2024-01-01' },
    session: { access_token: 'token', expires_at: Date.now() + 30 * 24 * 60 * 60 * 1000 }
  },
  invalidCredentials: {
    error: { message: 'Invalid login credentials' }
  },
  emailNotConfirmed: {
    error: { message: 'Email not confirmed' }
  }
};
```

---

## Out of Scope

Tests explicitly NOT included in this plan:

- **OAuth/Social Login**: Deferred to Phase 3 per spec.md
- **Two-Factor Authentication (2FA/MFA)**: Out of scope per spec.md
- **Single Sign-On (SSO/SAML)**: Out of scope per spec.md
- **Role-Based Access Control (RBAC)**: Out of scope per spec.md
- **Rate Limiting Tests**: Handled at infrastructure level per spec.md
- **"Remember Me" Functionality**: Out of scope per spec.md
- **Account Deletion/Deactivation**: Out of scope per spec.md
- **Profile Editing**: Separate feature per spec.md
- **Load/Performance Testing**: Requires dedicated sprint
- **Browser Compatibility Matrix**: Covered by CI/CD pipeline
- **Mobile Responsive Testing**: Visual regression in separate suite

---

## Validation Schemas Reference

For test implementation, use these Zod schemas:

```typescript
// lib/validations/auth.ts
import { z } from 'zod';

export const signupSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  displayName: z.string().min(1, 'Display name is required')
});

export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required')
});

export const forgotPasswordSchema = z.object({
  email: z.string().email('Invalid email address')
});

export const resetPasswordSchema = z.object({
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword']
});

export const magicLinkSchema = z.object({
  email: z.string().email('Invalid email address')
});
```

---

## Coverage Checklist

### User Stories Coverage

| User Story | Tests |
|------------|-------|
| US1: User signs up with email/password | #10-16, #54-61, e2e_signup_* |
| US2: User verifies email | #5, #43-45, #73-75 |
| US3: User logs in with email/password | #17-22, #46-53, e2e_login_with_email_password |
| US4: User logs in with magic link | #23-27, #52-53, e2e_login_with_magic_link |
| US5: User requests password reset | #28-31, #62-66, e2e_password_reset_* |
| US6: User resets password | #32-37, #67-72, e2e_password_reset_* |
| US7: User accesses protected route | #40-41, #80, #82, e2e_protected_route_* |
| US8: User is redirected when not authenticated | #80-81, #83, e2e_protected_route_unauthenticated |

### Critical Path Coverage: 100%

All critical priority tests cover:
- User registration with validation
- Email/password login flow
- Magic link authentication
- Password reset flow
- Session management
- Route protection
- Database profile creation

---

*Test Plan Generated: 2026-01-04*
*Total Tests: 81*
*Estimated Implementation Time: 3-4 days*
