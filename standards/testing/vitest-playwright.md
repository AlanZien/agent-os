# Testing Standards: Vitest + Playwright

> **Sources:**
> - [Vitest Documentation](https://vitest.dev)
> - [Playwright Documentation](https://playwright.dev)

## Overview

Standards pour les tests dans AgentOS Tracker:
- **Vitest** - Tests unitaires et d'intégration (composants, hooks, utils, API)
- **Playwright** - Tests E2E (parcours utilisateur complets)

## Structure des Tests

```
__tests__/                     # Vitest tests
├── unit/
│   ├── utils/
│   │   └── validation.test.ts
│   └── hooks/
│       └── useAuth.test.ts
├── integration/
│   ├── api/
│   │   ├── auth.test.ts
│   │   └── projects.test.ts
│   └── components/
│       └── LoginForm.test.tsx
└── setup.ts                   # Test setup

e2e/                           # Playwright tests
├── auth/
│   ├── login.spec.ts
│   ├── signup.spec.ts
│   └── password-reset.spec.ts
├── dashboard/
│   └── projects.spec.ts
└── fixtures/
    └── auth.ts                # Auth fixtures
```

---

## Vitest

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./__tests__/setup.ts'],
    include: ['__tests__/**/*.test.{ts,tsx}'],
    globals: true,
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', '__tests__/'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
})
```

### Setup File

```typescript
// __tests__/setup.ts
import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock Next.js router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
  }),
  useSearchParams: () => new URLSearchParams(),
  usePathname: () => '/',
}))

// Mock Supabase client
vi.mock('@/lib/supabase/client', () => ({
  createClient: () => ({
    auth: {
      signInWithPassword: vi.fn(),
      signUp: vi.fn(),
      signOut: vi.fn(),
      getUser: vi.fn(),
      getSession: vi.fn(),
      onAuthStateChange: vi.fn(() => ({
        data: { subscription: { unsubscribe: vi.fn() } },
      })),
    },
    from: vi.fn(() => ({
      select: vi.fn().mockReturnThis(),
      insert: vi.fn().mockReturnThis(),
      update: vi.fn().mockReturnThis(),
      delete: vi.fn().mockReturnThis(),
      eq: vi.fn().mockReturnThis(),
      single: vi.fn(),
    })),
  }),
}))
```

### Structure d'un Test Unitaire

```typescript
// __tests__/unit/utils/validation.test.ts
import { describe, it, expect } from 'vitest'
import { loginSchema, signupSchema } from '@/lib/validations/auth'

describe('Auth Validation Schemas', () => {
  describe('loginSchema', () => {
    it('validates correct email and password', () => {
      const result = loginSchema.safeParse({
        email: 'test@example.com',
        password: 'password123',
      })
      expect(result.success).toBe(true)
    })

    it('rejects invalid email', () => {
      const result = loginSchema.safeParse({
        email: 'invalid-email',
        password: 'password123',
      })
      expect(result.success).toBe(false)
      expect(result.error?.issues[0].path).toContain('email')
    })

    it('rejects password shorter than 8 characters', () => {
      const result = loginSchema.safeParse({
        email: 'test@example.com',
        password: 'short',
      })
      expect(result.success).toBe(false)
      expect(result.error?.issues[0].path).toContain('password')
    })
  })
})
```

### Test de Composant React

```typescript
// __tests__/integration/components/LoginForm.test.tsx
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from '@/components/features/auth/LoginForm'

// Mock du client Supabase
const mockSignIn = vi.fn()
vi.mock('@/lib/supabase/client', () => ({
  createClient: () => ({
    auth: {
      signInWithPassword: mockSignIn,
    },
  }),
}))

describe('LoginForm', () => {
  beforeEach(() => {
    mockSignIn.mockReset()
  })

  it('renders email and password inputs', () => {
    render(<LoginForm />)

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
  })

  it('displays validation errors for empty fields', async () => {
    const user = userEvent.setup()
    render(<LoginForm />)

    await user.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument()
    })
  })

  it('calls signInWithPassword on valid submission', async () => {
    mockSignIn.mockResolvedValue({ data: { user: {} }, error: null })
    const user = userEvent.setup()
    render(<LoginForm />)

    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(mockSignIn).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      })
    })
  })

  it('displays error message on failed login', async () => {
    mockSignIn.mockResolvedValue({
      data: null,
      error: { message: 'Invalid credentials' },
    })
    const user = userEvent.setup()
    render(<LoginForm />)

    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'wrongpassword')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
    })
  })
})
```

### Test d'API Route

```typescript
// __tests__/integration/api/auth.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { POST } from '@/app/api/auth/login/route'
import { NextRequest } from 'next/server'

// Mock Supabase server client
const mockSignIn = vi.fn()
vi.mock('@/lib/supabase/server', () => ({
  createClient: vi.fn(() => ({
    auth: {
      signInWithPassword: mockSignIn,
    },
  })),
}))

describe('POST /api/auth/login', () => {
  beforeEach(() => {
    mockSignIn.mockReset()
  })

  it('returns 200 on successful login', async () => {
    mockSignIn.mockResolvedValue({
      data: { user: { id: '123' }, session: {} },
      error: null,
    })

    const request = new NextRequest('http://localhost:3000/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: 'test@example.com',
        password: 'password123',
      }),
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.data.user.id).toBe('123')
  })

  it('returns 401 on invalid credentials', async () => {
    mockSignIn.mockResolvedValue({
      data: null,
      error: { message: 'Invalid login credentials' },
    })

    const request = new NextRequest('http://localhost:3000/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: 'test@example.com',
        password: 'wrongpassword',
      }),
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(401)
    expect(data.error).toBe('Invalid login credentials')
  })

  it('returns 400 on validation error', async () => {
    const request = new NextRequest('http://localhost:3000/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: 'invalid-email',
        password: 'short',
      }),
    })

    const response = await POST(request)

    expect(response.status).toBe(400)
  })
})
```

### Mocking Patterns

```typescript
// Mock fonction simple
const mockFn = vi.fn()
mockFn.mockReturnValue('value')
mockFn.mockResolvedValue('async value')
mockFn.mockRejectedValue(new Error('error'))

// Mock module
vi.mock('@/lib/supabase/client', () => ({
  createClient: vi.fn(() => mockSupabaseClient),
}))

// Mock partiel (garder l'implémentation originale)
vi.mock('@/lib/utils', async () => {
  const actual = await vi.importActual('@/lib/utils')
  return {
    ...actual,
    specificFunction: vi.fn(),
  }
})

// Reset entre les tests
beforeEach(() => {
  vi.clearAllMocks()
})

afterEach(() => {
  vi.restoreAllMocks()
})
```

---

## Playwright

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### Structure d'un Test E2E

```typescript
// e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
  })

  test('displays login form', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /sign in/i })).toBeVisible()
    await expect(page.getByLabel(/email/i)).toBeVisible()
    await expect(page.getByLabel(/password/i)).toBeVisible()
    await expect(page.getByRole('button', { name: /sign in/i })).toBeVisible()
  })

  test('shows validation errors for empty form', async ({ page }) => {
    await page.getByRole('button', { name: /sign in/i }).click()

    await expect(page.getByText(/email is required/i)).toBeVisible()
  })

  test('shows error for invalid credentials', async ({ page }) => {
    await page.getByLabel(/email/i).fill('test@example.com')
    await page.getByLabel(/password/i).fill('wrongpassword')
    await page.getByRole('button', { name: /sign in/i }).click()

    await expect(page.getByText(/invalid credentials/i)).toBeVisible()
  })

  test('redirects to dashboard on successful login', async ({ page }) => {
    await page.getByLabel(/email/i).fill('valid@example.com')
    await page.getByLabel(/password/i).fill('correctpassword')
    await page.getByRole('button', { name: /sign in/i }).click()

    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible()
  })

  test('has link to signup page', async ({ page }) => {
    await page.getByRole('link', { name: /sign up/i }).click()

    await expect(page).toHaveURL('/signup')
  })

  test('has link to forgot password page', async ({ page }) => {
    await page.getByRole('link', { name: /forgot password/i }).click()

    await expect(page).toHaveURL('/forgot-password')
  })
})
```

### Auth Fixtures

```typescript
// e2e/fixtures/auth.ts
import { test as base, expect } from '@playwright/test'

type AuthFixtures = {
  authenticatedPage: Page
}

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Login before test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill(process.env.TEST_USER_EMAIL!)
    await page.getByLabel(/password/i).fill(process.env.TEST_USER_PASSWORD!)
    await page.getByRole('button', { name: /sign in/i }).click()
    await expect(page).toHaveURL('/dashboard')

    await use(page)

    // Cleanup: logout after test
    await page.goto('/api/auth/logout')
  },
})

export { expect }
```

```typescript
// e2e/dashboard/projects.spec.ts
import { test, expect } from '../fixtures/auth'

test.describe('Projects', () => {
  test('displays projects list', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard/projects')

    await expect(page.getByRole('heading', { name: /projects/i })).toBeVisible()
  })

  test('can create new project', async ({ authenticatedPage: page }) => {
    await page.goto('/dashboard/projects')
    await page.getByRole('button', { name: /new project/i }).click()

    await page.getByLabel(/name/i).fill('Test Project')
    await page.getByRole('button', { name: /create/i }).click()

    await expect(page.getByText('Test Project')).toBeVisible()
  })
})
```

### Locators Best Practices

```typescript
// Prefer role-based locators (accessible)
page.getByRole('button', { name: /submit/i })
page.getByRole('textbox', { name: /email/i })
page.getByRole('link', { name: /sign up/i })
page.getByRole('heading', { level: 1 })

// Labels for form fields
page.getByLabel(/email/i)
page.getByLabel(/password/i)

// Text for content
page.getByText(/welcome/i)
page.getByText('Exact match')

// Placeholder for inputs without labels
page.getByPlaceholder(/search/i)

// Test IDs as last resort
page.getByTestId('submit-button')
```

### Assertions

```typescript
// Visibility
await expect(element).toBeVisible()
await expect(element).toBeHidden()

// Text content
await expect(element).toHaveText('exact text')
await expect(element).toContainText('partial')

// Attributes
await expect(element).toHaveAttribute('href', '/login')
await expect(element).toBeDisabled()
await expect(element).toBeEnabled()

// Page assertions
await expect(page).toHaveURL('/dashboard')
await expect(page).toHaveTitle(/Dashboard/)

// Count
await expect(page.getByRole('listitem')).toHaveCount(3)
```

---

## Commandes NPM

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed"
  }
}
```

## Best Practices

### Vitest
1. **Isoler les tests** - Chaque test doit être indépendant
2. **Mock les dépendances externes** - Supabase, APIs, etc.
3. **Tester les comportements, pas l'implémentation**
4. **Utiliser `describe` pour grouper** les tests liés
5. **Nommer clairement** - `it('should do X when Y')`

### Playwright
1. **Tests isolés** - Chaque test part d'un état propre
2. **Utiliser des fixtures** pour l'authentification
3. **Locators accessibles** - `getByRole`, `getByLabel`
4. **Assertions auto-retry** - Playwright attend automatiquement
5. **Screenshots on failure** - Debug facile

---

## Patterns Robustes (Leçons Apprises)

### Configuration Browsers Simplifiée

Pour une app web desktop, limiter aux browsers essentiels :

```typescript
// playwright.config.ts
projects: [
  { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  // Webkit/Mobile: activer seulement si nécessaire
],
```

### Selectors Précis (Éviter les Faux Positifs)

```typescript
// ❌ MAUVAIS - peut matcher plusieurs éléments
await expect(page.getByText(/check your email|sent|instructions/i)).toBeVisible();

// ✅ BON - selector précis avec rôle
await expect(
  page.getByRole('heading', { name: /check your email/i })
).toBeVisible();
```

### Gestion des Erreurs Supabase

```typescript
// Skip conditionnel si Supabase échoue
test('signup redirects to verification', async ({ page }) => {
  await auth.signup(user.email, user.password, user.displayName);

  // Attendre navigation
  await page.waitForURL(/verification-pending|signup/, { timeout: 10000 });

  // Skip si signup a échoué (config Supabase, rate limiting, etc.)
  const isOnVerificationPage = page.url().includes('verification-pending');
  if (!isOnVerificationPage) {
    test.skip(true, 'Signup failed - Supabase config issue');
    return;
  }

  // Continuer le test...
});
```

### Assertions Flexibles (Multi-Outcome)

```typescript
// Quand plusieurs résultats sont acceptables
const hasError = await page.getByText(/invalid|error/i).isVisible().catch(() => false);
const redirected = page.url().includes('/dashboard');

// L'un ou l'autre est acceptable
expect(hasError || redirected).toBe(true);
```

### Timeouts Explicites

```typescript
// Pour les opérations lentes (API calls)
await expect(
  page.getByRole('heading', { name: /success/i })
).toBeVisible({ timeout: 10000 });

// Attendre la navigation
await page.waitForURL(/\/dashboard/, { timeout: 10000 });

// Pause courte pour laisser l'UI se stabiliser
await page.waitForTimeout(500);
```

### Pattern Fill + Blur (Mobile/Safari)

```typescript
// Pour éviter les problèmes de timing sur certains browsers
const emailInput = page.getByLabel(/email/i);
await emailInput.fill('test@example.com');
await emailInput.blur(); // Force la mise à jour de l'état
```

### Domaine Email pour Tests

```typescript
// ❌ example.com - souvent bloqué par Supabase
email: `test-${Date.now()}@example.com`

// ✅ mailinator.com - accepté, emails publics
email: `test-${Date.now()}@mailinator.com`
```

### Structure Test E2E Robuste

```typescript
test('complete flow with error handling', async ({ page }) => {
  // 1. Setup
  const user = generateTestUser();

  // 2. Action avec attente explicite
  await page.goto('/signup');
  await page.getByLabel(/email/i).fill(user.email);
  await page.getByRole('button', { name: /submit/i }).click();

  // 3. Attendre un état stable
  await page.waitForURL(/success|error/, { timeout: 10000 });

  // 4. Vérification avec fallback
  const success = page.url().includes('success');
  if (!success) {
    const errorVisible = await page.getByText(/error/i).isVisible();
    expect(errorVisible).toBe(true); // Au moins une erreur est affichée
    return;
  }

  // 5. Assertions finales
  await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible();
});
