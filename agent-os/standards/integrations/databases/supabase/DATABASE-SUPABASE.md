# Supabase Database Standards - {ProjectName}

**Version**: 1.0 | **Stack**: Supabase (PostgreSQL) + Row Level Security | **Token-Optimized**

## Architecture

### Database Structure
```
{ProjectName} Database
├── auth.users (managed by Supabase Auth)
├── public.profiles
├── public.recipes
├── public.favorites
├── public.recipe_comments
└── public.shopping_lists
```

### Schema Design Principles

1. **Normalization** - 3NF for data integrity
2. **RLS Enabled** - Row Level Security on all tables
3. **UUID Primary Keys** - Use `uuid` type with `gen_random_uuid()`
4. **Timestamps** - Always include `created_at`, `updated_at`
5. **Soft Deletes** - Use `deleted_at` instead of hard deletes
6. **Foreign Keys** - Enforce referential integrity
7. **Indexes** - Add indexes on foreign keys and frequently queried columns

## Core Tables

### 1. Profiles Table
```sql
-- Extends auth.users with profile data
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  email text unique not null,
  display_name text,
  avatar_url text,
  bio text,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- RLS Policies
alter table public.profiles enable row level security;

create policy "Public profiles are viewable by everyone"
  on profiles for select
  using (true);

create policy "Users can insert their own profile"
  on profiles for insert
  with check (auth.uid() = id);

create policy "Users can update own profile"
  on profiles for update
  using (auth.uid() = id);

-- Indexes
create index profiles_email_idx on public.profiles(email);

-- Trigger for updated_at
create trigger handle_updated_at before update on public.profiles
  for each row execute function moddatetime (updated_at);
```

### 2. Recipes Table
```sql
create table public.recipes (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  title text not null,
  description text,
  ingredients jsonb not null default '[]'::jsonb,
  steps jsonb not null default '[]'::jsonb,
  prep_time_minutes integer,
  cook_time_minutes integer,
  servings integer,
  difficulty text check (difficulty in ('easy', 'medium', 'hard')),
  cuisine_type text,
  image_url text,
  is_public boolean default true not null,
  deleted_at timestamptz,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- RLS Policies
alter table public.recipes enable row level security;

create policy "Public recipes are viewable by everyone"
  on recipes for select
  using (is_public = true and deleted_at is null);

create policy "Users can view own recipes"
  on recipes for select
  using (auth.uid() = user_id);

create policy "Users can create recipes"
  on recipes for insert
  with check (auth.uid() = user_id);

create policy "Users can update own recipes"
  on recipes for update
  using (auth.uid() = user_id);

create policy "Users can soft-delete own recipes"
  on recipes for update
  using (auth.uid() = user_id and deleted_at is null)
  with check (deleted_at is not null);

-- Indexes
create index recipes_user_id_idx on public.recipes(user_id);
create index recipes_is_public_idx on public.recipes(is_public) where deleted_at is null;
create index recipes_cuisine_type_idx on public.recipes(cuisine_type) where deleted_at is null;
create index recipes_created_at_idx on public.recipes(created_at desc);

-- Full-text search
create index recipes_title_search_idx on public.recipes using gin(to_tsvector('english', title));

-- Trigger for updated_at
create trigger handle_updated_at before update on public.recipes
  for each row execute function moddatetime (updated_at);
```

### 3. Favorites Table
```sql
create table public.favorites (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  recipe_id uuid references public.recipes(id) on delete cascade not null,
  created_at timestamptz default now() not null,
  unique(user_id, recipe_id)
);

-- RLS Policies
alter table public.favorites enable row level security;

create policy "Users can view own favorites"
  on favorites for select
  using (auth.uid() = user_id);

create policy "Users can add favorites"
  on favorites for insert
  with check (auth.uid() = user_id);

create policy "Users can remove favorites"
  on favorites for delete
  using (auth.uid() = user_id);

-- Indexes
create index favorites_user_id_idx on public.favorites(user_id);
create index favorites_recipe_id_idx on public.favorites(recipe_id);
```

### 4. Recipe Comments Table
```sql
create table public.recipe_comments (
  id uuid default gen_random_uuid() primary key,
  recipe_id uuid references public.recipes(id) on delete cascade not null,
  user_id uuid references public.profiles(id) on delete cascade not null,
  content text not null,
  rating integer check (rating >= 1 and rating <= 5),
  deleted_at timestamptz,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- RLS Policies
alter table public.recipe_comments enable row level security;

create policy "Comments are viewable by everyone"
  on recipe_comments for select
  using (deleted_at is null);

create policy "Authenticated users can create comments"
  on recipe_comments for insert
  with check (auth.uid() = user_id);

create policy "Users can update own comments"
  on recipe_comments for update
  using (auth.uid() = user_id);

create policy "Users can delete own comments"
  on recipe_comments for delete
  using (auth.uid() = user_id);

-- Indexes
create index recipe_comments_recipe_id_idx on public.recipe_comments(recipe_id);
create index recipe_comments_user_id_idx on public.recipe_comments(user_id);

-- Trigger for updated_at
create trigger handle_updated_at before update on public.recipe_comments
  for each row execute function moddatetime (updated_at);
```

### 5. Shopping Lists Table
```sql
create table public.shopping_lists (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  name text not null default 'My Shopping List',
  items jsonb not null default '[]'::jsonb,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- RLS Policies
alter table public.shopping_lists enable row level security;

create policy "Users can view own shopping lists"
  on shopping_lists for select
  using (auth.uid() = user_id);

create policy "Users can create shopping lists"
  on shopping_lists for insert
  with check (auth.uid() = user_id);

create policy "Users can update own shopping lists"
  on shopping_lists for update
  using (auth.uid() = user_id);

create policy "Users can delete own shopping lists"
  on shopping_lists for delete
  using (auth.uid() = user_id);

-- Indexes
create index shopping_lists_user_id_idx on public.shopping_lists(user_id);

-- Trigger for updated_at
create trigger handle_updated_at before update on public.shopping_lists
  for each row execute function moddatetime (updated_at);
```

## Database Functions

### 1. Handle New User (Trigger)
```sql
-- Automatically create profile when user signs up
create function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email, display_name)
  values (new.id, new.email, new.raw_user_meta_data->>'display_name');
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
```

### 2. Get User Favorites (RPC)
```sql
create function public.get_user_favorites(user_uuid uuid)
returns setof recipes as $$
  select r.*
  from recipes r
  join favorites f on r.id = f.recipe_id
  where f.user_id = user_uuid
    and r.deleted_at is null
  order by f.created_at desc;
$$ language sql stable;
```

### 3. Search Recipes (RPC)
```sql
create function public.search_recipes(search_query text)
returns setof recipes as $$
  select *
  from recipes
  where to_tsvector('english', title || ' ' || coalesce(description, '')) @@ plainto_tsquery('english', search_query)
    and is_public = true
    and deleted_at is null
  order by created_at desc;
$$ language sql stable;
```

### 4. Get Recipe with Stats (RPC)
```sql
create function public.get_recipe_with_stats(recipe_uuid uuid)
returns json as $$
  select json_build_object(
    'recipe', row_to_json(r.*),
    'author', row_to_json(p.*),
    'favorites_count', (select count(*) from favorites where recipe_id = recipe_uuid),
    'comments_count', (select count(*) from recipe_comments where recipe_id = recipe_uuid and deleted_at is null),
    'average_rating', (select avg(rating) from recipe_comments where recipe_id = recipe_uuid and deleted_at is null)
  )
  from recipes r
  join profiles p on r.user_id = p.id
  where r.id = recipe_uuid;
$$ language sql stable;
```

## Storage Buckets

### Recipe Images
```sql
-- Create storage bucket
insert into storage.buckets (id, name, public)
values ('recipe-images', 'recipe-images', true);

-- RLS Policies for storage
create policy "Anyone can view recipe images"
  on storage.objects for select
  using (bucket_id = 'recipe-images');

create policy "Authenticated users can upload recipe images"
  on storage.objects for insert
  with check (
    bucket_id = 'recipe-images'
    and auth.role() = 'authenticated'
  );

create policy "Users can update own recipe images"
  on storage.objects for update
  using (
    bucket_id = 'recipe-images'
    and auth.uid()::text = (storage.foldername(name))[1]
  );
```

## Migrations

### Migration File Structure
```
supabase/migrations/
├── 20240101000000_create_profiles.sql
├── 20240101000001_create_recipes.sql
├── 20240101000002_create_favorites.sql
├── 20240101000003_create_comments.sql
├── 20240101000004_create_shopping_lists.sql
├── 20240101000005_create_functions.sql
└── 20240101000006_create_storage.sql
```

### Running Migrations
```bash
# Apply all migrations
supabase db push

# Reset database (dev only)
supabase db reset

# Create new migration
supabase migration new <migration_name>
```

## Best Practices

1. **Row Level Security (RLS)**
   - Enable RLS on ALL tables
   - Test policies thoroughly
   - Use `auth.uid()` for user-specific policies

2. **JSONB for Flexible Data**
   - Use JSONB for arrays (ingredients, steps)
   - Index JSONB fields if queried frequently
   - Validate JSONB structure in application layer

3. **Soft Deletes**
   - Add `deleted_at` column for important tables
   - Filter `deleted_at is null` in queries
   - Periodic cleanup job for old soft-deleted records

4. **Timestamps**
   - Always include `created_at`, `updated_at`
   - Use `moddatetime` extension for auto-update

5. **Indexes**
   - Add indexes on foreign keys
   - Add indexes on frequently queried columns
   - Use partial indexes for filtered queries
   - Monitor slow queries with `pg_stat_statements`

6. **Database Functions**
   - Use RPC functions for complex queries
   - Mark functions as `stable` or `immutable` when possible
   - Use `security definer` carefully

7. **Performance**
   - Use `select *` sparingly (specify columns)
   - Implement pagination (limit/offset)
   - Use database functions for aggregations
   - Monitor query performance

## Client Usage (JavaScript)

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Fetch recipes with RLS
const { data: recipes } = await supabase
  .from('recipes')
  .select('*, profiles(display_name, avatar_url)')
  .eq('is_public', true)
  .is('deleted_at', null)
  .order('created_at', { ascending: false })
  .limit(20);

// Create recipe
const { data: newRecipe } = await supabase
  .from('recipes')
  .insert({
    title: 'Pasta Carbonara',
    ingredients: ['pasta', 'eggs', 'bacon'],
    steps: ['Cook pasta', 'Mix eggs', 'Combine'],
  })
  .select()
  .single();

// Call RPC function
const { data: favorites } = await supabase
  .rpc('get_user_favorites', { user_uuid: userId });

// Upload image
const { data: uploadData } = await supabase
  .storage
  .from('recipe-images')
  .upload(`${userId}/${recipeId}.jpg`, file);
```

## Security Checklist

- [ ] RLS enabled on all tables
- [ ] RLS policies tested for all user scenarios
- [ ] Foreign keys with proper cascade rules
- [ ] Input validation in application layer
- [ ] Storage bucket policies configured
- [ ] Database secrets not exposed to client
- [ ] Anon key has read-only access where appropriate
- [ ] Service role key used only on backend

---

**Token Count**: ~1300 tokens | **Reusable for**: Maison Epigenetic
