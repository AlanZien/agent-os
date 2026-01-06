# Tech Stack

## Frontend

### Framework
- **Next.js 14+** - React framework with App Router
- **React 18+** - UI library with Server Components support

### Styling
- **Tailwind CSS 3+** - Utility-first CSS framework
- **shadcn/ui** - Headless component library built on Radix UI
- **Radix UI** - Accessible component primitives (via shadcn/ui)

### State Management
- **React Query (TanStack Query)** - Server state management and caching
- **Zustand** - Lightweight client state management (if needed)

### Form Handling
- **React Hook Form** - Performant form handling
- **Zod** - Schema validation for forms and API

### Drag and Drop
- **@dnd-kit** - Modern drag-and-drop toolkit for Kanban board

### Charts
- **Recharts** - Chart library for metrics and velocity graphs

## Backend

### API
- **Next.js API Routes** - Serverless API endpoints
- **Server Actions** - Direct server mutations from components

### Database
- **Supabase** - PostgreSQL database with realtime subscriptions
- **Supabase Auth** - Authentication and authorization
- **Row Level Security (RLS)** - Database-level security policies

### Validation
- **Zod** - Runtime schema validation for API inputs

## Infrastructure

### Hosting
- **Vercel** - Frontend and API hosting with edge functions
- **Supabase Cloud** - Managed database hosting

### Version Control
- **Git** - Source control
- **GitHub** - Repository hosting and CI/CD

## Development Tools

### Language
- **TypeScript 5+** - Type-safe JavaScript

### Package Manager
- **pnpm** - Fast, disk-efficient package manager

### Linting & Formatting
- **ESLint** - Code linting
- **Prettier** - Code formatting

### Testing
- **Vitest** - Unit testing framework
- **Playwright** - End-to-end testing

## External Integrations

### GitHub API
- **Octokit** - GitHub REST API client for PR/branch linking

### Agent-OS
- **REST API** - Custom endpoints to receive agent-os command data

## File Structure

```
/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Auth routes (login, signup)
│   ├── (dashboard)/       # Protected dashboard routes
│   ├── api/               # API routes
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   └── features/         # Feature-specific components
├── lib/                   # Utilities and configurations
│   ├── supabase/         # Supabase client and helpers
│   ├── validations/      # Zod schemas
│   └── utils.ts          # Utility functions
├── hooks/                 # Custom React hooks
├── types/                 # TypeScript type definitions
└── agent-os/             # Agent-OS configuration
    └── product/          # Product documentation
```

## Key Dependencies

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@supabase/supabase-js": "^2.0.0",
    "@supabase/ssr": "^0.1.0",
    "tailwindcss": "^3.0.0",
    "@tanstack/react-query": "^5.0.0",
    "react-hook-form": "^7.0.0",
    "zod": "^3.0.0",
    "@dnd-kit/core": "^6.0.0",
    "@dnd-kit/sortable": "^8.0.0",
    "recharts": "^2.0.0",
    "lucide-react": "^0.300.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "vitest": "^1.0.0",
    "@playwright/test": "^1.40.0"
  }
}
```
