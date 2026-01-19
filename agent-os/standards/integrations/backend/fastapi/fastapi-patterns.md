# Backend Patterns - {ProjectName}

**Version**: 1.0 | **Complement to**: BACKEND-FASTAPI.md | **Token-Optimized**

## API Endpoint Patterns

### REST Conventions
```python
# Resource naming (plural, lowercase)
/api/items          # Collection
/api/items/{id}     # Single resource
/api/users/{id}/items  # Nested resource

# HTTP Methods
GET    /api/items       # List (with pagination)
POST   /api/items       # Create
GET    /api/items/{id}  # Retrieve
PUT    /api/items/{id}  # Full update
PATCH  /api/items/{id}  # Partial update
DELETE /api/items/{id}  # Delete

# Status codes
200 OK          # Successful GET, PUT, PATCH
201 Created     # Successful POST
204 No Content  # Successful DELETE
400 Bad Request # Validation error
401 Unauthorized # Missing/invalid auth
403 Forbidden   # Insufficient permissions
404 Not Found   # Resource doesn't exist
500 Server Error # Unexpected error
```

### Pagination
```python
@router.get("/items/", response_model=ItemList)
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: str = Depends(get_current_user)
):
    total = await ItemService.count(user_id)
    items = await ItemService.list(user_id, skip, limit)

    return ItemList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

# Response model
class ItemList(BaseModel):
    items: list[Item]
    total: int
    skip: int
    limit: int
```

### Filtering & Sorting
```python
@router.get("/items/")
async def list_items(
    category: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|title)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
):
    return await ItemService.list(
        category=category,
        sort_by=sort_by,
        order=order
    )
```

## Pydantic Models

### Model Inheritance
```python
# Base model with common config
class BaseModelConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True
    )

# Domain models
class ItemBase(BaseModelConfig):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    ingredients: list[str] = Field(..., min_items=1)
    steps: list[str] = Field(..., min_items=1)

class ItemCreate(ItemBase):
    """For POST requests"""
    pass

class ItemUpdate(BaseModel):
    """For PATCH requests - all fields optional"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    ingredients: Optional[list[str]] = None
    steps: Optional[list[str]] = None

class Item(ItemBase):
    """Full model with DB fields"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
```

### Custom Validators
```python
from pydantic import validator, field_validator

class ItemCreate(BaseModel):
    title: str
    ingredients: list[str]

    @field_validator('title')
    @classmethod
    def title_must_be_safe(cls, v: str) -> str:
        # Remove dangerous characters
        if any(char in v for char in ['<', '>', ';', '--']):
            raise ValueError('Invalid characters in title')
        return v.strip()

    @field_validator('ingredients')
    @classmethod
    def ingredients_not_empty(cls, v: list[str]) -> list[str]:
        if not v or len(v) == 0:
            raise ValueError('At least one ingredient required')
        # Remove empty strings
        return [ing.strip() for ing in v if ing.strip()]
```

## Database Queries (Supabase)

### Basic CRUD
```python
# Create
response = supabase.table("items").insert({
    "title": "Pasta",
    "user_id": user_id,
    "ingredients": ["pasta", "tomato"]
}).execute()

# Read single
response = supabase.table("items")\
    .select("*")\
    .eq("id", item_id)\
    .single()\
    .execute()

# Read list with filter
response = supabase.table("items")\
    .select("*")\
    .eq("user_id", user_id)\
    .order("created_at", desc=True)\
    .limit(20)\
    .execute()

# Update
response = supabase.table("items")\
    .update({"title": "New Title"})\
    .eq("id", item_id)\
    .execute()

# Delete
response = supabase.table("items")\
    .delete()\
    .eq("id", item_id)\
    .execute()
```

### Complex Queries
```python
# Multiple filters (AND)
response = supabase.table("items")\
    .select("*")\
    .eq("user_id", user_id)\
    .eq("category", "dessert")\
    .execute()

# OR conditions
response = supabase.table("items")\
    .select("*")\
    .or_(f"category.eq.dessert,category.eq.breakfast")\
    .execute()

# Search (ILIKE)
response = supabase.table("items")\
    .select("*")\
    .ilike("title", f"%{search_term}%")\
    .execute()

# Count
response = supabase.table("items")\
    .select("*", count="exact")\
    .eq("user_id", user_id)\
    .execute()
total_count = response.count

# Relations (join)
response = supabase.table("items")\
    .select("*, user:users(name, email)")\
    .eq("id", item_id)\
    .execute()
```

### Pagination Pattern
```python
async def list_with_pagination(
    table: str,
    user_id: str,
    skip: int = 0,
    limit: int = 20
):
    # Get total count
    count_response = supabase.table(table)\
        .select("*", count="exact")\
        .eq("user_id", user_id)\
        .execute()

    # Get paginated data
    data_response = supabase.table(table)\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .range(skip, skip + limit - 1)\
        .execute()

    return {
        "items": data_response.data,
        "total": count_response.count,
        "skip": skip,
        "limit": limit
    }
```

## Database Migrations

### Supabase SQL Migrations
```sql
-- migrations/001_create_items.sql
CREATE TABLE items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL CHECK (char_length(title) > 0),
    description TEXT,
    ingredients JSONB NOT NULL DEFAULT '[]',
    steps JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for user queries
CREATE INDEX idx_items_user_id ON items(user_id);

-- Index for search
CREATE INDEX idx_items_title ON items USING gin(to_tsvector('english', title));

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER items_updated_at
    BEFORE UPDATE ON items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

### Row Level Security (RLS)
```sql
-- Enable RLS
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Users can only read their own items
CREATE POLICY "Users can view own items"
    ON items FOR SELECT
    USING (auth.uid() = user_id);

-- Users can only insert items for themselves
CREATE POLICY "Users can create own items"
    ON items FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can only update their own items
CREATE POLICY "Users can update own items"
    ON items FOR UPDATE
    USING (auth.uid() = user_id);

-- Users can only delete their own items
CREATE POLICY "Users can delete own items"
    ON items FOR DELETE
    USING (auth.uid() = user_id);
```

### Running Migrations
```bash
# Using Supabase CLI
supabase migration new create_items
# Edit file in supabase/migrations/
supabase db push

# Or via Supabase Dashboard
# SQL Editor → Run migration SQL → Save as migration
```

## Best Practices

1. **API Design**: Use plural nouns, consistent naming, proper HTTP methods
2. **Validation**: Validate at Pydantic level, not in business logic
3. **Queries**: Use indexes for filtered/sorted fields
4. **Migrations**: Version control all schema changes
5. **RLS**: Always enable Row Level Security on user data tables
6. **Errors**: Return appropriate status codes with clear messages
7. **Pagination**: Always paginate list endpoints (default 20, max 100)

---

**Token Count**: ~900 tokens | **Use with**: BACKEND-FASTAPI.md
