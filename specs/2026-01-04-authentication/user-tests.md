# User Tests - Authentication with Supabase Auth

## Feature
**Name:** Authentication with Supabase Auth
**Date:** 2026-01-04
**Status:** Ready for Testing

---

## Prerequisites
- Application deployed to test environment
- Valid email address for receiving verification/reset emails
- Browser with JavaScript enabled
- Stable internet connection

---

## Test Scenarios

### UT-001: Signup with Valid Information
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Navigate to /signup<br>2. Enter a valid email address<br>3. Enter a password (at least 8 characters)<br>4. Enter a display name<br>5. Click "Sign up" button |
| **Expected Result** | User is redirected to verification pending page. Success message indicates to check email for verification link. |
| **Status** | To Test |

---

### UT-002: Signup Form Validation - Short Password
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Navigate to /signup<br>2. Enter a valid email address<br>3. Enter a password with less than 8 characters (e.g., "short")<br>4. Enter a display name<br>5. Click "Sign up" button |
| **Expected Result** | Error message appears: "Password must be at least 8 characters". Form does not submit. |
| **Status** | To Test |

---

### UT-003: Signup Form Validation - Invalid Email
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Navigate to /signup<br>2. Enter an invalid email (e.g., "not-an-email")<br>3. Enter a valid password<br>4. Enter a display name<br>5. Click "Sign up" button |
| **Expected Result** | Error message appears: "Invalid email address". Form does not submit. |
| **Status** | To Test |

---

### UT-004: Signup with Duplicate Email
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Navigate to /signup<br>2. Enter an email that is already registered<br>3. Enter a valid password<br>4. Enter a display name<br>5. Click "Sign up" button |
| **Expected Result** | Error message appears indicating the email is already registered. |
| **Status** | To Test |

---

### UT-005: Email Verification Flow
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Complete signup (UT-001)<br>2. Check email inbox for verification email<br>3. Click the verification link in the email<br>4. Observe the redirect |
| **Expected Result** | User is redirected to login page with success message "Email verified successfully". |
| **Status** | To Test |

---

### UT-006: Resend Verification Email
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Complete signup but do not verify email<br>2. Go to verification pending page<br>3. Click "Resend verification email" button<br>4. Check email inbox |
| **Expected Result** | Success message appears. New verification email is received in inbox. |
| **Status** | To Test |

---

### UT-007: Login with Valid Credentials
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Navigate to /login<br>2. Enter email of a verified account<br>3. Enter the correct password<br>4. Click "Login" button |
| **Expected Result** | User is redirected to /dashboard. User profile information is visible. |
| **Status** | To Test |

---

### UT-008: Login with Wrong Password
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Navigate to /login<br>2. Enter a valid email<br>3. Enter an incorrect password<br>4. Click "Login" button |
| **Expected Result** | Error message appears: "Invalid credentials". User remains on login page. |
| **Status** | To Test |

---

### UT-009: Login with Non-existent Email
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Navigate to /login<br>2. Enter an email that is not registered<br>3. Enter any password<br>4. Click "Login" button |
| **Expected Result** | Error message appears: "Invalid credentials" (same as wrong password for security). |
| **Status** | To Test |

---

### UT-010: Login with Unverified Email
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Create a new account but do not verify email<br>2. Navigate to /login<br>3. Enter the unverified account credentials<br>4. Click "Login" button |
| **Expected Result** | User is redirected to verification pending page. Message indicates email must be verified. |
| **Status** | To Test |

---

### UT-011: Magic Link Login
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Navigate to /login<br>2. Click "Use magic link" option<br>3. Enter email of a verified account<br>4. Click "Send magic link" button<br>5. Check email inbox<br>6. Click the magic link |
| **Expected Result** | Success message after sending. Magic link email received. Clicking link logs user in and redirects to dashboard. |
| **Status** | To Test |

---

### UT-012: Magic Link for Non-existent Email
| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Steps** | 1. Navigate to /login<br>2. Click "Use magic link" option<br>3. Enter an email that is not registered<br>4. Click "Send magic link" button |
| **Expected Result** | Same success message appears (for security - does not reveal if email exists). |
| **Status** | To Test |

---

### UT-013: Forgot Password Request
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Navigate to /login<br>2. Click "Forgot password?" link<br>3. Enter email of registered account<br>4. Click "Reset password" button<br>5. Check email inbox |
| **Expected Result** | Success message appears. Password reset email is received with reset link. |
| **Status** | To Test |

---

### UT-014: Reset Password with Valid Token
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Complete forgot password flow (UT-013)<br>2. Click reset link in email<br>3. Enter new password (at least 8 characters)<br>4. Confirm new password<br>5. Click "Set new password" button<br>6. Try logging in with old password<br>7. Login with new password |
| **Expected Result** | Success message, redirected to login. Old password no longer works. New password works. |
| **Status** | To Test |

---

### UT-015: Reset Password - Password Mismatch
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Navigate to reset password page with valid token<br>2. Enter a new password<br>3. Enter a different password in confirm field<br>4. Click submit |
| **Expected Result** | Error message: "Passwords do not match". Form does not submit. |
| **Status** | To Test |

---

### UT-016: Reset Password - Short Password
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Navigate to reset password page with valid token<br>2. Enter password with less than 8 characters<br>3. Confirm password<br>4. Click submit |
| **Expected Result** | Error message: "Password must be at least 8 characters". Form does not submit. |
| **Status** | To Test |

---

### UT-017: Reset Password - Expired Token
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Request password reset<br>2. Wait for token to expire (or use an old link)<br>3. Click the expired reset link<br>4. Try to set new password |
| **Expected Result** | Error message indicates link is expired. Option to request new reset link is provided. |
| **Status** | To Test |

---

### UT-018: Protected Route - Unauthenticated Access
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Ensure you are logged out<br>2. Navigate directly to /dashboard in browser<br>3. Observe the redirect |
| **Expected Result** | User is redirected to /login page. Dashboard content is not accessible. |
| **Status** | To Test |

---

### UT-019: Auth Route - Authenticated Redirect
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Login to the application<br>2. Navigate directly to /login in browser<br>3. Navigate directly to /signup in browser |
| **Expected Result** | User is redirected to /dashboard from both /login and /signup pages. |
| **Status** | To Test |

---

### UT-020: Logout
| Field | Value |
|-------|--------|
| **Priority** | Critical |
| **Steps** | 1. Login to the application<br>2. Click logout button/link<br>3. Observe the redirect<br>4. Try to navigate to /dashboard |
| **Expected Result** | User is redirected to /login. Attempting to access dashboard redirects back to login. |
| **Status** | To Test |

---

### UT-021: Session Persistence
| Field | Value |
|-------|--------|
| **Priority** | High |
| **Steps** | 1. Login to the application<br>2. Refresh the page (F5)<br>3. Verify still logged in<br>4. Close and reopen browser tab<br>5. Navigate to /dashboard |
| **Expected Result** | User remains logged in after page refresh. Session persists when reopening tab. |
| **Status** | To Test |

---

### UT-022: Loading States During Form Submission
| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Steps** | 1. Navigate to /login<br>2. Enter valid credentials<br>3. Click login button<br>4. Observe button during submission |
| **Expected Result** | Button shows loading indicator. Button and form inputs are disabled during loading. |
| **Status** | To Test |

---

### UT-023: Visual Design - Auth Pages
| Field | Value |
|-------|--------|
| **Priority** | Medium |
| **Steps** | 1. Navigate to /login<br>2. Observe page layout and styling<br>3. Check other auth pages (/signup, /forgot-password) |
| **Expected Result** | Dark background. Centered card layout. "AgentOS Tracker" logo above form. Consistent styling across all auth pages. |
| **Status** | To Test |

---

### UT-024: Form Input Focus States
| Field | Value |
|-------|--------|
| **Priority** | Low |
| **Steps** | 1. Navigate to /login<br>2. Click on email input field<br>3. Observe focus styling |
| **Expected Result** | Input shows green border (#10B981) on focus. Subtle focus ring visible. |
| **Status** | To Test |

---

### UT-025: Password Visibility Toggle
| Field | Value |
|-------|--------|
| **Priority** | Low |
| **Steps** | 1. Navigate to /signup<br>2. Enter text in password field<br>3. Click show/hide password icon |
| **Expected Result** | Password text toggles between hidden (dots) and visible (plain text). |
| **Status** | To Test |

---

## Summary

| Priority | Number of Tests |
|----------|-----------------|
| Critical | 10 |
| High | 10 |
| Medium | 3 |
| Low | 2 |
| **Total** | **25** |

---

## Notes
- These tests should be performed on both desktop and mobile viewport sizes
- Test with slow network conditions (use browser DevTools throttling)
- Verify error messages are user-friendly and do not expose technical details
- Ensure all email deliveries work with actual SMTP in test environment
- Check accessibility: forms should be navigable via keyboard (Tab key)
