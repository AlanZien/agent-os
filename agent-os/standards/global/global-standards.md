# Global Standards - ForkIt

**Version**: 1.0 | **Applies to**: All code (Backend + Mobile) | **Token-Optimized**

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth + JWT
- **API**: REST (OpenAPI/Swagger docs)

### Mobile
- **Framework**: React Native + Expo 50+
- **Language**: TypeScript 5.0+
- **Navigation**: Expo Router (file-based)
- **State**: Zustand
- **UI**: Custom components + React Native Paper

### Shared
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Deployment**: Railway (backend), EAS (mobile)
- **Monitoring**: Sentry
- **Testing**: Pytest (backend), Jest + React Native Testing Library (mobile)

## Naming Conventions

### Python (Backend)
```python
# Variables & functions: snake_case
user_id = "123"
def get_item_by_id(item_id: str) -> Item:
    pass

# Classes: PascalCase
class ItemService:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_UPLOAD_SIZE = 5_000_000
JWT_ALGORITHM = "HS256"

# Private methods: _leading_underscore
def _validate_input(data: dict) -> bool:
    pass

# Files: snake_case
# auth_service.py, item_router.py
```

### TypeScript (Mobile)
```typescript
// Variables & functions: camelCase
const userId = "123";
function getItemById(itemId: string): Item {}

// Components & Types: PascalCase
export function ItemCard({ item }: ItemCardProps) {}
interface ItemCardProps {
  item: Item;
}

// Constants: UPPER_SNAKE_CASE
const MAX_FILE_SIZE = 5_000_000;
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL;

// Private functions: _leadingUnderscore (or just don't export)
function _formatDate(date: Date): string {}

// Files: PascalCase for components, camelCase for others
// ItemCard.tsx, useAuth.ts, apiClient.ts
```

## Code Style

### Clean Functions
```python
# ✅ GOOD - Small, focused, single responsibility
def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed.encode())

# ❌ BAD - Too many responsibilities
def handle_user_authentication(email: str, password: str):
    # Validates, hashes, creates user, sends email, logs in
    # 100 lines of mixed logic
    pass
```

### DRY Principle
```typescript
// ✅ GOOD - Reusable hook
export function useApi<T>(endpoint: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);

  const fetch = async () => {
    setLoading(true);
    const response = await api.get<T>(endpoint);
    setData(response.data);
    setLoading(false);
  };

  return { data, loading, fetch };
}

// Usage
const { data: items, loading, fetch: fetchItems } = useApi<Item[]>('/api/items');

// ❌ BAD - Duplicated fetch logic in every component
function ItemList() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  // ... duplicate fetch logic
}
```

### Remove Dead Code
```python
# ✅ GOOD - Clean, only what's needed
from app.models import Item
from app.database import supabase

def get_items(user_id: str) -> list[Item]:
    response = supabase.table("items").select("*").eq("user_id", user_id).execute()
    return [Item(**item) for item in response.data]

# ❌ BAD - Commented code, unused imports
# from app.old_models import OldItem  # Old implementation
import time  # Unused
import json  # Unused

def get_items(user_id: str) -> list[Item]:
    # Old way:
    # items = db.query(Item).filter_by(user_id=user_id).all()
    response = supabase.table("items").select("*").eq("user_id", user_id).execute()
    return [Item(**item) for item in response.data]
```

## Code Comments

### When to Comment
```typescript
// ✅ GOOD - Explain WHY, not WHAT
export function ItemCard({ item }: ItemCardProps) {
  // Use React.memo to prevent re-renders when parent updates
  // but item data hasn't changed
  return useMemo(() => (
    <Card>
      <Text>{item.title}</Text>
    </Card>
  ), [item.id]);
}

// ❌ BAD - Obvious comments
// Loop through items
items.forEach(item => {
  // Print item title
  console.log(item.title);
});
```

### Self-Documenting Code
```python
# ✅ GOOD - Code explains itself
def is_item_owner(item: Item, user_id: str) -> bool:
    return item.user_id == user_id

if is_item_owner(item, current_user.id):
    await ItemService.delete(item.id)

# ❌ BAD - Needs comment to understand
# Check if user can delete (is owner)
if item.user_id == current_user.id:
    await ItemService.delete(item.id)
```

## Error Handling

### User-Friendly Messages
```python
# ✅ GOOD - Clear, actionable
@router.post("/items/")
async def create_item(item: ItemCreate, user_id: str = Depends(get_current_user)):
    try:
        return await ItemService.create(item, user_id)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid item data. Please check all required fields."
        )
    except Exception as e:
        logger.error(f"Failed to create item: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Unable to create item. Please try again."
        )

# ❌ BAD - Exposes technical details
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

### Fail Fast
```typescript
// ✅ GOOD - Validate early
export function ItemForm({ onSubmit }: ItemFormProps) {
  const handleSubmit = async (data: ItemFormData) => {
    // Validate immediately
    if (!data.title?.trim()) {
      throw new Error('Item title is required');
    }
    if (data.propertys.length === 0) {
      throw new Error('At least one property is required');
    }

    await onSubmit(data);
  };
}

// ❌ BAD - Process first, validate later
export function ItemForm({ onSubmit }: ItemFormProps) {
  const handleSubmit = async (data: ItemFormData) => {
    const formattedData = formatItemData(data);
    const processedData = processPropertys(formattedData);
    // Only now check if valid - wasted processing
    if (!processedData.title) throw new Error('Title required');
  };
}
```

### Graceful Degradation
```typescript
// ✅ GOOD - Continue with cached data on error
export function useItems() {
  const [items, setItems] = useState<Item[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchItems = async () => {
    try {
      const { data } = await api.get<Item[]>('/api/items');
      setItems(data);
      setError(null);
    } catch (err) {
      setError('Unable to load items. Showing cached data.');
      // Keep existing items, show error banner
    }
  };

  return { items, error, fetchItems };
}
```

## Input Validation

### Server-Side First
```python
# ✅ GOOD - Validate on server
class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    propertys: list[str] = Field(..., min_items=1)

    @field_validator('title')
    @classmethod
    def title_must_be_safe(cls, v: str) -> str:
        if any(char in v for char in ['<', '>', ';', '--']):
            raise ValueError('Invalid characters in title')
        return v.strip()

@router.post("/items/")
async def create_item(item: ItemCreate):  # Pydantic validates automatically
    return await ItemService.create(item)
```

### Client-Side for UX
```typescript
// ✅ GOOD - Immediate feedback, but server validates too
export function ItemForm() {
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');

  const validateTitle = (value: string) => {
    if (!value.trim()) {
      setError('Title is required');
      return false;
    }
    if (value.length > 200) {
      setError('Title must be less than 200 characters');
      return false;
    }
    setError('');
    return true;
  };

  const handleSubmit = async () => {
    if (!validateTitle(title)) return;

    try {
      // Server will re-validate
      await api.post('/api/items/', { title });
    } catch (err) {
      setError(err.response.data.detail);
    }
  };
}
```

### Allowlists Over Blocklists
```python
# ✅ GOOD - Define what's allowed
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}

def validate_image_upload(file: UploadFile):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(f"Only {', '.join(ALLOWED_IMAGE_TYPES)} allowed")

# ❌ BAD - Try to block everything bad
BLOCKED_TYPES = {'application/exe', 'application/bat', ...}  # Incomplete list
```

## Version Control

### Commit Messages
```bash
# ✅ GOOD - Clear, descriptive
git commit -m "Add item search endpoint with pagination

- Implement /api/items/search with query parameter
- Add pagination (default 20, max 100)
- Include tests for search functionality"

# ❌ BAD - Vague
git commit -m "fix stuff"
git commit -m "updates"
```

### Branch Naming
```bash
# ✅ GOOD - Type/scope/description
feature/item-search
bugfix/login-token-expiry
hotfix/critical-security-patch

# ❌ BAD
my-changes
test
branch-1
```

## Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── database.py          # Supabase client
│   ├── models/              # Pydantic models
│   │   ├── item.py
│   │   └── user.py
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   └── items.py
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   └── item_service.py
│   └── utils/               # Helpers
│       └── security.py
├── tests/
├── requirements.txt
└── .env.example
```

### Mobile Structure
```
mobile/
├── app/                     # Expo Router screens
│   ├── (auth)/
│   │   ├── login.tsx
│   │   └── register.tsx
│   ├── (tabs)/
│   │   ├── index.tsx
│   │   └── items.tsx
│   └── _layout.tsx
├── components/              # Reusable components
│   ├── ui/
│   │   ├── Button.tsx
│   │   └── Input.tsx
│   └── item/
│       └── ItemCard.tsx
├── hooks/                   # Custom hooks
│   └── useAuth.ts
├── services/                # API calls
│   └── api.ts
├── stores/                  # Zustand stores
│   └── authStore.ts
└── constants/
    └── theme.ts
```

## Best Practices

1. **Naming**: Descriptive names, consistent conventions per language
2. **Functions**: Small, focused, single responsibility
3. **Comments**: Explain WHY, not WHAT. Code should be self-documenting
4. **Errors**: User-friendly messages, fail fast, graceful degradation
5. **Validation**: Server-side required, client-side for UX
6. **Dead Code**: Delete it, don't comment it out
7. **DRY**: Extract common logic into reusable functions/hooks
8. **Version Control**: Clear commits, feature branches, meaningful PRs
9. **Structure**: Consistent, predictable organization
10. **No Secrets**: Use environment variables, never commit keys

---

**Token Count**: ~1400 tokens | **Use with**: QUICK-REFERENCE.md
