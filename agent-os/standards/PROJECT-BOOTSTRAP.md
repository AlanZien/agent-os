# Project Bootstrap - ForkIt

**Version**: 1.0 | **Use for**: Initial project setup from scratch | **Token-Optimized**

## Stack Overview

- **Backend**: FastAPI + Python 3.11+
- **Mobile**: React Native + Expo 50+
- **Database**: Supabase (PostgreSQL + Auth)
- **Deployment**: Railway (backend), EAS (mobile)

## Backend Setup (FastAPI)

### 1. Initialize Project

```bash
# Create project directory
mkdir backend && cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-dotenv supabase pydantic[email] bcrypt python-jose[cryptography]

# Create requirements.txt
pip freeze > requirements.txt
```

### 2. Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Settings & env vars
│   ├── database.py       # Supabase client
│   ├── models/           # Pydantic models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/          # API endpoints
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── services/         # Business logic
│   │   ├── __init__.py
│   │   └── auth_service.py
│   └── utils/            # Helpers
│       ├── __init__.py
│       └── security.py
├── tests/
│   ├── __init__.py
│   └── conftest.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### 3. Initial Files

**app/config.py**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ForkIt API"
    supabase_url: str
    supabase_key: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

**app/database.py**
```python
from supabase import create_client, Client
from app.config import settings

supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
```

**app/main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth

app = FastAPI(title="ForkIt API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "ForkIt API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**.env.example**
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
JWT_SECRET=your-secret-key-generate-with-openssl-rand-hex-32
```

**.gitignore**
```
venv/
__pycache__/
*.pyc
.env
.pytest_cache/
htmlcov/
.coverage
```

### 4. Run Development Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API docs available at:
# http://localhost:8000/docs (Swagger)
# http://localhost:8000/redoc (ReDoc)
```

## Mobile Setup (React Native + Expo)

### 1. Initialize Project

```bash
# Create Expo project
npx create-expo-app@latest mobile --template blank-typescript

cd mobile

# Install dependencies
npx expo install expo-router expo-secure-store expo-image-picker
npm install zustand axios react-native-paper

# Install dev dependencies
npm install -D @types/react @types/react-native jest @testing-library/react-native
```

### 2. Project Structure

```
mobile/
├── app/                  # Expo Router screens
│   ├── (auth)/
│   │   ├── login.tsx
│   │   └── register.tsx
│   ├── (tabs)/
│   │   ├── _layout.tsx
│   │   └── index.tsx
│   └── _layout.tsx
├── components/           # Reusable components
│   └── ui/
│       ├── Button.tsx
│       └── Input.tsx
├── services/             # API calls
│   └── api.ts
├── stores/               # Zustand stores
│   └── authStore.ts
├── constants/            # Theme, colors
│   └── theme.ts
├── hooks/                # Custom hooks
│   └── useAuth.ts
├── utils/                # Helper functions
│   └── validators.ts
├── __tests__/
├── app.json
├── package.json
├── tsconfig.json
└── .env.example
```

### 3. Initial Files

**app.json**
```json
{
  "expo": {
    "name": "ForkIt",
    "slug": "forkit",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "light",
    "scheme": "forkit",
    "plugins": [
      "expo-router",
      "expo-secure-store"
    ],
    "platforms": ["ios", "android"],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.yourcompany.forkit"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.yourcompany.forkit"
    }
  }
}
```

**services/api.ts**
```typescript
import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

**constants/theme.ts**
```typescript
export const COLORS = {
  primary: '#FF6B6B',
  secondary: '#4ECDC4',
  background: '#FFFFFF',
  text: '#1F2937',
  border: '#E5E7EB',
};

export const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};
```

**.env.example**
```bash
EXPO_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Run Development

```bash
# Start Expo dev server
npx expo start

# Options:
# - Press 'i' for iOS simulator
# - Press 'a' for Android emulator
# - Scan QR code with Expo Go app for physical device
```

## Supabase Setup

### 1. Create Project

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Note your project URL and anon key

### 2. Database Schema

Create initial tables in SQL Editor:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase auth.users)
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

### 3. Environment Variables

Add to backend `.env`:
```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...your-anon-key
```

Add to mobile `.env`:
```bash
EXPO_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...your-anon-key
```

## Testing Setup

### Backend (Pytest)

```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Create pytest.ini
cat > pytest.ini << EOF
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
EOF

# Run tests
pytest
pytest --cov=app --cov-report=html
```

### Mobile (Jest)

```bash
cd mobile

# Install test dependencies
npm install -D jest @testing-library/react-native @testing-library/jest-native

# Run tests
npm test
npm test -- --coverage
```

## Git Setup

```bash
# Initialize git
git init

# Create .gitignore
cat > .gitignore << EOF
# Dependencies
node_modules/
venv/

# Environment
.env
.env.local

# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/

# Testing
coverage/
htmlcov/
.coverage

# Build
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# Initial commit
git add .
git commit -m "Initial project setup

- FastAPI backend with basic structure
- React Native + Expo mobile app
- Supabase database configuration
- Testing setup (Pytest + Jest)

🤖 Generated with Claude Code"
```

## First Feature Checklist

After bootstrap, implement authentication:

- [ ] Backend: Auth endpoints (register, login, logout)
- [ ] Backend: JWT token generation & validation
- [ ] Backend: Password hashing with bcrypt
- [ ] Mobile: Login & Register screens
- [ ] Mobile: Auth state management (Zustand)
- [ ] Mobile: Secure token storage (SecureStore)
- [ ] Tests: Auth flow (backend + mobile)
- [ ] Supabase: RLS policies for user data

---

**Token Count**: ~1400 tokens | **Use once** at project start
