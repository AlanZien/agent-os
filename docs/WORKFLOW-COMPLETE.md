# Agent-OS Complete Workflow

## 10 Étapes du Product au Code

```
1. /plan-product              → mission.md, roadmap.md, tech-stack.md, design-system.md
2. /bootstrap-project         → Structure projet (Next.js, Supabase, etc.)
3. /shape-spec (Phase 1)      → raw-idea.md
4. /shape-spec (Phase 2)      → requirements.md
5. /write-spec                → spec.md
6. /plan-tests                → test-plan.md (Given-When-Then)
7. /create-tasks              → tasks.md + sync Notion
8. /orchestrate-tasks         → Délégation aux subagents
9. [Itération task groups]    → Implémentation + tests
10. [Commit & Next Feature]   → git commit + nouvelle spec
```

## Stack Technique AgentOS-Tracker

| Catégorie | Technologie |
|-----------|-------------|
| Frontend | Next.js 14 (App Router) |
| UI | shadcn/ui + Tailwind CSS |
| Auth | Supabase Auth (SSR) |
| Database | Supabase PostgreSQL |
| State | React Context + Hooks |
| Tests | Vitest + Playwright |
| PM | Notion (via MCP) |

## Workflow Détaillé

### Phase 1: Planification Produit

```bash
/plan-product
```

Crée :
- `agent-os/product/mission.md` - Vision du produit
- `agent-os/product/roadmap.md` - Features planifiées
- `agent-os/product/tech-stack.md` - Choix techniques
- `agent-os/product/design-system.md` - Design tokens

### Phase 2: Bootstrap (optionnel)

```bash
/bootstrap-project
```

Initialise automatiquement :
- Structure Next.js
- Configuration Supabase
- Dépendances npm
- Fichiers de config

### Phase 3: Spécification Feature

```bash
/shape-spec    # Collecte requirements
/write-spec    # Génère spec.md
/plan-tests    # Génère test-plan.md
/create-tasks  # Génère tasks.md + sync Notion
```

### Phase 4: Implémentation

```bash
/orchestrate-tasks
```

Pour chaque task group :
1. Agent implémente le code
2. Agent écrit les tests
3. Agent vérifie que les tests passent
4. Agent met à jour tasks.md

### Phase 5: Validation

```bash
npm run test:run    # Tests unitaires (150 tests)
npm run test:e2e    # Tests E2E (30 tests)
npm run lint        # Vérification code
npm run build       # Vérification build
```

## Commandes Disponibles

| Commande | Description |
|----------|-------------|
| `npm run dev` | Serveur développement |
| `npm run build` | Build production |
| `npm run test:run` | Tests unitaires |
| `npm run test:e2e` | Tests E2E Playwright |
| `npm run lint` | Linting ESLint |

## Structure Projet

```
AgentOS-Tracker/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Routes auth (login, signup, etc.)
│   ├── (protected)/       # Routes protégées (dashboard)
│   └── api/               # API Routes
├── components/            # Composants React
├── lib/                   # Utilities et config
├── hooks/                 # Custom React hooks
├── __tests__/             # Tests unitaires Vitest
├── e2e/                   # Tests E2E Playwright
├── agent-os/              # Configuration Agent-OS
│   ├── product/           # Documents produit
│   ├── specs/             # Spécifications features
│   └── standards/         # Standards de développement
└── supabase/              # Migrations et config Supabase
```

## Feature Implémentée : Authentication

✅ **Complète** - 12 task groups implémentés :

1. database-layer (Supabase schema)
2. validation-schemas (Zod)
3. api-core-auth (API routes)
4. api-session-support (Session handling)
5. middleware-route-protection (Next.js middleware)
6. ui-auth-layout (Layout composants)
7. ui-login-page (Page login)
8. ui-signup-page (Page signup)
9. ui-password-reset (Pages reset password)
10. ui-verification (Page verification pending)
11. auth-context-hooks (React Context + hooks)
12. e2e-tests (Playwright tests)

## Prochaines Étapes

Pour ajouter une nouvelle feature :

```bash
# 1. Définir la feature
/shape-spec

# 2. Créer la spécification
/write-spec

# 3. Planifier les tests
/plan-tests

# 4. Créer les tâches
/create-tasks

# 5. Implémenter
/orchestrate-tasks
```
