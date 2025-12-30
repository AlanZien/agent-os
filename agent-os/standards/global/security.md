# Security Standards - ForkIt

**Version**: 1.0 | **Scope**: Backend + Frontend + Mobile | **Token-Optimized**

## OWASP Top 10 Mitigation

### 1. Broken Access Control
```python
# Backend - Route Protection
from fastapi import Depends, HTTPException
from app.utils.security import get_current_user

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: str, user_id: str = Depends(get_current_user)):
    recipe = await RecipeService.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404)

    # Verify ownership before deletion
    if recipe.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await RecipeService.delete(recipe_id)
    return {"status": "deleted"}
```

### 2. Cryptographic Failures
```python
# Backend - Password Hashing
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# NEVER store plain passwords
# NEVER use weak algorithms (MD5, SHA1)
# ALWAYS use bcrypt, argon2, or scrypt
```

### 3. Injection (SQL, NoSQL, Command)
```python
# ✅ SAFE - Parameterized queries (Supabase handles this)
response = supabase.table("recipes").select("*").eq("user_id", user_id).execute()

# ❌ DANGEROUS - String concatenation
query = f"SELECT * FROM recipes WHERE user_id = '{user_id}'"  # NEVER DO THIS

# Input validation with Pydantic
from pydantic import BaseModel, validator

class RecipeCreate(BaseModel):
    title: str
    ingredients: list[str]

    @validator('title')
    def title_must_be_safe(cls, v):
        if len(v) > 200:
            raise ValueError('Title too long')
        # Remove dangerous characters
        dangerous_chars = ['<', '>', ';', '--', '/*', '*/']
        for char in dangerous_chars:
            if char in v:
                raise ValueError('Invalid characters in title')
        return v
```

### 4. Insecure Design
```python
# Rate limiting with slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(request: Request, credentials: LoginRequest):
    # Login logic
    pass
```

### 5. Security Misconfiguration
```python
# Backend - CORS Configuration
from fastapi.middleware.cors import CORSMiddleware

# ❌ Development only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # NEVER in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://forkit.app",
        "https://mobile.forkit.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)
```

### 6. Vulnerable Components
```bash
# Regular dependency updates
pip list --outdated
npm outdated

# Security audits
pip-audit  # Python
npm audit  # Node.js

# Pin versions in production
# requirements.txt
fastapi==0.109.0  # Not fastapi>=0.109.0
```

### 7. Authentication Failures
```python
# Backend - JWT with expiration
from datetime import datetime, timedelta
from jose import jwt

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=30)  # Short-lived tokens
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

# Refresh token pattern
def create_refresh_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    payload = {"sub": user_id, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
```

```typescript
// Mobile - Secure token storage
import * as SecureStore from 'expo-secure-store';

export const authStorage = {
  async saveToken(token: string) {
    await SecureStore.setItemAsync('auth_token', token);
  },

  async getToken(): Promise<string | null> {
    return await SecureStore.getItemAsync('auth_token');
  },

  async deleteToken() {
    await SecureStore.deleteItemAsync('auth_token');
  }
};

// ❌ NEVER use AsyncStorage for sensitive data
// ✅ ALWAYS use SecureStore (iOS Keychain / Android KeyStore)
```

### 8. Data Integrity Failures
```python
# File upload validation
from fastapi import UploadFile
import magic

ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']
MAX_SIZE = 5 * 1024 * 1024  # 5MB

async def validate_upload(file: UploadFile):
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    # Verify actual file type (not just extension)
    mime = magic.from_buffer(contents, mime=True)
    if mime not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    await file.seek(0)
    return file
```

### 9. Logging & Monitoring
```python
# Backend - Secure logging
import logging

logger = logging.getLogger(__name__)

# ✅ GOOD - Log security events
logger.warning(f"Failed login attempt for user: {email}")
logger.info(f"User {user_id} accessed sensitive resource")

# ❌ BAD - Never log sensitive data
logger.info(f"User logged in with password: {password}")  # NEVER
logger.debug(f"JWT token: {token}")  # NEVER
logger.info(f"Credit card: {card_number}")  # NEVER

# Sanitize user input in logs
def sanitize_for_log(user_input: str) -> str:
    return user_input[:100].replace('\n', ' ').replace('\r', '')

logger.info(f"User search: {sanitize_for_log(search_query)}")
```

### 10. Server-Side Request Forgery (SSRF)
```python
# Backend - URL validation
from urllib.parse import urlparse
import httpx

ALLOWED_DOMAINS = ['api.trusted-service.com']

async def fetch_external_data(url: str):
    parsed = urlparse(url)

    # Validate domain
    if parsed.netloc not in ALLOWED_DOMAINS:
        raise HTTPException(status_code=400, detail="Untrusted domain")

    # Prevent internal network access
    if parsed.hostname in ['localhost', '127.0.0.1'] or parsed.hostname.startswith('192.168.'):
        raise HTTPException(status_code=400, detail="Invalid URL")

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url)
        return response.json()
```

## Environment Variables & Secrets

```bash
# .env.example - Template (commit this)
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_key_here
JWT_SECRET=generate_with_openssl_rand_hex_32

# .env - Actual secrets (NEVER commit)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
JWT_SECRET=a3f8b2c9d1e4f5a6b7c8d9e0f1a2b3c4

# Generate secure secrets
openssl rand -hex 32
```

```python
# Backend - Environment validation
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    jwt_secret: str

    @validator('jwt_secret')
    def jwt_secret_must_be_strong(cls, v):
        if len(v) < 32:
            raise ValueError('JWT secret must be at least 32 characters')
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

# Fail fast if environment is misconfigured
settings = Settings()
```

## Mobile Security

```typescript
// Secure API calls
import axios from 'axios';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const api = axios.create({
  baseURL: __DEV__
    ? 'http://localhost:8000'
    : 'https://api.forkit.app',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Certificate pinning for production
if (!__DEV__ && Platform.OS === 'ios') {
  // Use expo-ssl-pinning or react-native-ssl-pinning
}

// Request interceptor
api.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - Auto logout on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await SecureStore.deleteItemAsync('auth_token');
      // Redirect to login
    }
    return Promise.reject(error);
  }
);
```

## Security Headers

```python
# Backend - Security headers
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Production only
if not settings.debug:
    # Force HTTPS
    app.add_middleware(HTTPSRedirectMiddleware)

    # Prevent host header injection
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["forkit.app", "*.forkit.app"]
    )

# Custom security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

## Best Practices Checklist

### Backend
- [ ] All passwords hashed with bcrypt (min 10 rounds)
- [ ] JWT tokens expire within 30 minutes
- [ ] Refresh tokens used for long sessions
- [ ] Rate limiting on auth endpoints
- [ ] Input validation with Pydantic
- [ ] CORS configured for production domains only
- [ ] HTTPS enforced in production
- [ ] Security headers set
- [ ] Secrets in environment variables
- [ ] SQL injection prevented (parameterized queries)

### Frontend/Mobile
- [ ] Tokens stored in SecureStore (not AsyncStorage)
- [ ] API calls over HTTPS only
- [ ] Certificate pinning in production
- [ ] Auto-logout on token expiration
- [ ] Sensitive data cleared on logout
- [ ] No secrets in source code
- [ ] Input sanitization on user data
- [ ] Biometric authentication for sensitive actions

### General
- [ ] Dependencies updated monthly
- [ ] Security audit run before releases
- [ ] Error messages don't expose internals
- [ ] Logging doesn't include sensitive data
- [ ] File uploads validated (type, size)
- [ ] External URLs validated before fetching

---

**Token Count**: ~1100 tokens | **Reusable for**: All projects
