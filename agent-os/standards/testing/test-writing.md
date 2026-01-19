# Testing Standards - {ProjectName}

**Version**: 2.0 | **Stack**: Pytest + Jest + React Native Testing Library | **Token-Optimized**

## Testing Philosophy

- **Write Minimal Tests During Development**: Complete feature implementation first, then add strategic tests at logical completion points
- **Test Only Core User Flows**: Focus on critical paths and primary workflows, skip non-critical utilities
- **Defer Edge Cases**: Address edge cases and error states in dedicated testing phases, not during feature development
- **Test Behavior, Not Implementation**: Focus on what code does, not how it does it
- **Clear Test Names**: Descriptive names that explain what's tested and expected outcome
- **Mock External Dependencies**: Isolate units by mocking databases, APIs, file systems
- **Fast Execution**: Unit tests should run in milliseconds

## Coverage Targets

- **Overall**: Minimum 80% code coverage
- **Critical paths**: 100% coverage (auth, payments, data loss scenarios)
- **Utils/helpers**: 90% coverage
- **UI components**: 70% coverage (focus on interaction logic)

## Backend Testing (Python + Pytest)

### Test Structure
```
backend/tests/
├── conftest.py          # Shared fixtures
├── test_auth.py         # Auth tests
├── test_recipes.py      # Recipe CRUD tests
├── test_services/
│   ├── test_auth_service.py
│   └── test_recipe_service.py
└── test_utils/
    ├── test_security.py
    └── test_validators.py
```

### 1. Unit Tests

```python
# tests/test_utils/test_security.py
import pytest
from app.utils.security import hash_password, verify_password, create_access_token
from jose import jwt
from app.config import settings

def test_hash_password_creates_different_hashes():
    """Hashing same password twice should produce different hashes"""
    password = "testpass123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2  # Bcrypt uses salt
    assert len(hash1) > 20  # Reasonable hash length

def test_verify_password_with_correct_password():
    """Verifying correct password should return True"""
    password = "testpass123"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True

def test_verify_password_with_wrong_password():
    """Verifying wrong password should return False"""
    password = "testpass123"
    hashed = hash_password(password)

    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token_contains_user_id():
    """JWT token should contain user ID in sub claim"""
    user_id = "user123"
    token = create_access_token(user_id)

    payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    assert payload["sub"] == user_id
    assert "exp" in payload  # Expiration should be set
```

### 2. Service Tests

```python
# tests/test_services/test_recipe_service.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.recipe_service import RecipeService
from app.models.recipe import RecipeCreate, Recipe

@pytest.mark.asyncio
async def test_create_recipe_success():
    """Creating recipe should return Recipe object with ID"""
    recipe_data = RecipeCreate(
        title="Test Recipe",
        ingredients=["ingredient1"],
        steps=["step1"]
    )
    user_id = "user123"

    # Mock Supabase response
    mock_response = Mock()
    mock_response.data = [{
        "id": "recipe123",
        "title": "Test Recipe",
        "ingredients": ["ingredient1"],
        "steps": ["step1"],
        "user_id": user_id,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }]

    with patch('app.services.recipe_service.supabase') as mock_supabase:
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response

        result = await RecipeService.create(recipe_data, user_id)

        assert isinstance(result, Recipe)
        assert result.id == "recipe123"
        assert result.title == "Test Recipe"
        assert result.user_id == user_id

@pytest.mark.asyncio
async def test_get_recipe_not_found():
    """Getting non-existent recipe should return None"""
    mock_response = Mock()
    mock_response.data = []

    with patch('app.services.recipe_service.supabase') as mock_supabase:
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        result = await RecipeService.get_by_id("nonexistent")

        assert result is None
```

### 3. API Integration Tests

```python
# tests/test_recipes.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    """Fixture providing authenticated headers"""
    # Login and get token
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_recipe_authenticated(auth_headers):
    """Creating recipe with auth should return 201"""
    recipe_data = {
        "title": "Test Recipe",
        "description": "A test recipe",
        "ingredients": ["ingredient1", "ingredient2"],
        "steps": ["step1", "step2"]
    }

    response = client.post("/api/recipes/", json=recipe_data, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Recipe"
    assert "id" in data
    assert "created_at" in data

def test_create_recipe_unauthenticated():
    """Creating recipe without auth should return 401"""
    recipe_data = {"title": "Test Recipe"}

    response = client.post("/api/recipes/", json=recipe_data)

    assert response.status_code == 401

def test_get_recipe_success(auth_headers):
    """Getting existing recipe should return 200"""
    # First create a recipe
    create_response = client.post("/api/recipes/", json={
        "title": "Test Recipe",
        "ingredients": ["ing1"],
        "steps": ["step1"]
    }, headers=auth_headers)
    recipe_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/recipes/{recipe_id}")

    assert response.status_code == 200
    assert response.json()["id"] == recipe_id

def test_get_recipe_not_found():
    """Getting non-existent recipe should return 404"""
    response = client.get("/api/recipes/nonexistent")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

### 4. Pytest Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import supabase

@pytest.fixture
def client():
    """Test client for API"""
    return TestClient(app)

@pytest.fixture
def test_user():
    """Create a test user"""
    user_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    # Create user in Supabase test instance
    response = supabase.auth.sign_up(user_data)
    yield response.user
    # Cleanup
    supabase.auth.admin.delete_user(response.user.id)

@pytest.fixture
def auth_headers(client, test_user):
    """Authenticated headers for test user"""
    response = client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

## Frontend/Mobile Testing (Jest + React Native Testing Library)

### Test Structure
```
mobile/__tests__/
├── components/
│   ├── Button.test.tsx
│   └── RecipeCard.test.tsx
├── hooks/
│   ├── useAuth.test.ts
│   └── useRecipes.test.ts
├── screens/
│   ├── LoginScreen.test.tsx
│   └── RecipeListScreen.test.tsx
└── utils/
    └── validators.test.ts
```

### 1. Component Tests

```typescript
// __tests__/components/Button.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from '@/components/ui/Button';

describe('Button', () => {
  it('renders title correctly', () => {
    const { getByText } = render(
      <Button title="Click Me" onPress={() => {}} />
    );

    expect(getByText('Click Me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPressMock = jest.fn();
    const { getByText } = render(
      <Button title="Click Me" onPress={onPressMock} />
    );

    fireEvent.press(getByText('Click Me'));

    expect(onPressMock).toHaveBeenCalledTimes(1);
  });

  it('shows loading indicator when loading', () => {
    const { getByTestId, queryByText } = render(
      <Button title="Click Me" onPress={() => {}} loading />
    );

    expect(queryByText('Click Me')).toBeNull();
    expect(getByTestId('activity-indicator')).toBeTruthy();
  });

  it('is disabled when loading', () => {
    const onPressMock = jest.fn();
    const { getByTestId } = render(
      <Button title="Click Me" onPress={onPressMock} loading />
    );

    const button = getByTestId('button');
    fireEvent.press(button);

    expect(onPressMock).not.toHaveBeenCalled();
  });
});
```

### 2. Hook Tests

```typescript
// __tests__/hooks/useAuth.test.ts
import { renderHook, act, waitFor } from '@testing-library/react-native';
import { useAuth } from '@/hooks/useAuth';
import * as SecureStore from 'expo-secure-store';
import { authService } from '@/services/auth';

jest.mock('expo-secure-store');
jest.mock('@/services/auth');

describe('useAuth', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('loads token on mount if exists', async () => {
    const mockToken = 'test-token';
    const mockUser = { id: '1', email: 'test@test.com' };

    (SecureStore.getItemAsync as jest.Mock).mockResolvedValue(mockToken);
    (authService.getProfile as jest.Mock).mockResolvedValue(mockUser);

    const { result } = renderHook(() => useAuth());

    await waitFor(() => {
      expect(result.current.user).toEqual(mockUser);
      expect(result.current.token).toBe(mockToken);
    });
  });

  it('login sets user and token', async () => {
    const mockUser = { id: '1', email: 'test@test.com' };
    const mockToken = 'new-token';

    (authService.login as jest.Mock).mockResolvedValue({
      user: mockUser,
      token: mockToken
    });

    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.login('test@test.com', 'password');
    });

    expect(result.current.user).toEqual(mockUser);
    expect(result.current.token).toBe(mockToken);
    expect(SecureStore.setItemAsync).toHaveBeenCalledWith('auth_token', mockToken);
  });

  it('logout clears user and token', async () => {
    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.logout();
    });

    expect(result.current.user).toBeNull();
    expect(result.current.token).toBeNull();
    expect(SecureStore.deleteItemAsync).toHaveBeenCalledWith('auth_token');
  });
});
```

### 3. Screen Tests

```typescript
// __tests__/screens/LoginScreen.test.tsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import LoginScreen from '@/app/(auth)/login';
import { useAuth } from '@/hooks/useAuth';

jest.mock('@/hooks/useAuth');

describe('LoginScreen', () => {
  it('renders login form', () => {
    (useAuth as jest.Mock).mockReturnValue({
      login: jest.fn(),
      user: null
    });

    const { getByPlaceholderText, getByText } = render(<LoginScreen />);

    expect(getByPlaceholderText('Email')).toBeTruthy();
    expect(getByPlaceholderText('Password')).toBeTruthy();
    expect(getByText('Login')).toBeTruthy();
  });

  it('calls login with form values', async () => {
    const mockLogin = jest.fn().mockResolvedValue(undefined);
    (useAuth as jest.Mock).mockReturnValue({
      login: mockLogin,
      user: null
    });

    const { getByPlaceholderText, getByText } = render(<LoginScreen />);

    fireEvent.changeText(getByPlaceholderText('Email'), 'test@test.com');
    fireEvent.changeText(getByPlaceholderText('Password'), 'password123');
    fireEvent.press(getByText('Login'));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@test.com', 'password123');
    });
  });

  it('shows validation error for invalid email', async () => {
    (useAuth as jest.Mock).mockReturnValue({
      login: jest.fn(),
      user: null
    });

    const { getByPlaceholderText, getByText, findByText } = render(<LoginScreen />);

    fireEvent.changeText(getByPlaceholderText('Email'), 'invalid-email');
    fireEvent.press(getByText('Login'));

    expect(await findByText('Invalid email address')).toBeTruthy();
  });
});
```

## Test Best Practices

### DO ✅

```python
# Clear, descriptive test names
def test_user_cannot_delete_another_users_recipe():
    pass

# Arrange, Act, Assert pattern
def test_create_recipe():
    # Arrange
    recipe_data = RecipeCreate(title="Test")
    user_id = "user123"

    # Act
    result = RecipeService.create(recipe_data, user_id)

    # Assert
    assert result.user_id == user_id
```

### DON'T ❌

```python
# Vague test names
def test_recipe():  # ❌ What about recipe?
    pass

# Testing implementation details
def test_recipe_service_calls_supabase_insert():  # ❌ Implementation detail
    pass

# Multiple assertions without clear intent
def test_everything():  # ❌ Too broad
    assert True
    assert 1 == 1
    assert "string" == "string"
```

## Running Tests

```bash
# Backend
cd backend
pytest                          # Run all tests
pytest tests/test_auth.py       # Specific file
pytest -v                       # Verbose
pytest --cov=app --cov-report=html  # Coverage report
pytest -k "auth"                # Tests matching pattern
pytest -m "slow"                # Tests with @pytest.mark.slow

# Mobile
cd mobile
npm test                        # Run all tests
npm test -- Button.test.tsx     # Specific file
npm test -- --coverage          # With coverage
npm test -- --watch             # Watch mode
```

## Coverage Reports

```bash
# View coverage in terminal
pytest --cov=app --cov-report=term-missing

# Generate HTML report
pytest --cov=app --cov-report=html
open htmlcov/index.html

# Mobile coverage
npm test -- --coverage
open coverage/lcov-report/index.html
```

---

**Token Count**: ~1500 tokens | **Reusable for**: All projects
