# ForkIt Development Standards

**Version**: 1.0 | **Project**: ForkIt (Recipe App) | **Reusable for**: Maison Epigenetic

## Overview

Standards condensés et optimisés pour tokens, réutilisables pour tous les projets de la stack React Native + FastAPI + Supabase.

## Stack Technique

- **Mobile**: React Native + Expo + TypeScript
- **Backend**: FastAPI + Python 3.11+
- **Database**: Supabase (PostgreSQL)
- **State Management**: Zustand
- **Form Validation**: React Hook Form + Zod
- **API Client**: Axios
- **Authentication**: JWT + Supabase Auth

## Standards Disponibles

### 1. [Backend - FastAPI](BACKEND-FASTAPI.md)

**Couverture**: Architecture, Patterns, Security, Testing

**Contenu**:
- Structure de projet complète
- Pydantic models et validation
- Route handlers avec dependency injection
- Service layer pattern
- JWT authentication
- Error handling
- Testing avec pytest
- Deployment guidelines

**Token Count**: ~1200 tokens

**Utilisation**: Copy-paste pour démarrer un nouveau backend FastAPI

---

### 2. [Mobile - React Native](MOBILE-REACT-NATIVE.md)

**Couverture**: Architecture, Components, State, Navigation

**Contenu**:
- Expo Router (file-based routing)
- TypeScript types et interfaces
- Zustand state management
- Custom hooks patterns
- API client avec intercepteurs
- Reusable components
- Form validation (react-hook-form + zod)
- Styling conventions
- Performance tips

**Token Count**: ~1400 tokens

**Utilisation**: Copy-paste pour démarrer une nouvelle app React Native

---

### 3. [Database - Supabase](DATABASE-SUPABASE.md)

**Couverture**: Schema, RLS, Functions, Storage

**Contenu**:
- Schema design principles
- Tables complètes avec RLS policies
- Database functions (RPC)
- Storage buckets configuration
- Migrations structure
- Security checklist
- Client usage examples
- Performance best practices

**Token Count**: ~1300 tokens

**Utilisation**: Copy-paste pour setup Supabase database

---

## Quick Start

### Pour ForkIt

1. **Backend Setup**
   ```bash
   cd backend/
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Configurer .env avec credentials Supabase
   uvicorn app.main:app --reload
   ```

2. **Mobile Setup**
   ```bash
   cd mobile/
   npm install
   cp .env.example .env
   # Configurer .env avec API URL
   npx expo start
   ```

3. **Database Setup**
   ```bash
   # Créer projet Supabase sur supabase.com
   # Copier credentials
   # Appliquer migrations depuis docs/standards/DATABASE-SUPABASE.md
   ```

### Pour Maison Epigenetic

**Réutilisation**: Copier les 3 standards et adapter :
- Remplacer "Recipe" par votre domaine métier
- Adapter les tables selon vos besoins
- Garder la structure et les patterns

## Conventions de Code

### Naming Conventions

**Python (Backend)**:
- `snake_case` pour variables, fonctions, fichiers
- `PascalCase` pour classes
- `UPPER_CASE` pour constantes

**TypeScript (Mobile)**:
- `camelCase` pour variables, fonctions
- `PascalCase` pour components, types, interfaces
- `UPPER_CASE` pour constantes

**SQL (Database)**:
- `snake_case` pour tables, colonnes
- `verb_noun` pour functions (ex: `get_user_favorites`)

### File Organization

**Backend**: Domain-driven (models, routes, services par feature)

**Mobile**: Feature-based (components, hooks, types regroupés)

**Database**: Migration-based (chronological SQL files)

## Architecture Principles

1. **Separation of Concerns** - Routes, Services, Models séparés
2. **Type Safety** - TypeScript strict mode, Pydantic validation
3. **Security First** - RLS, JWT, Input validation partout
4. **DRY** - Reusable components, services, hooks
5. **Testing** - Tests unitaires + intégration
6. **Performance** - Async/await, pagination, indexes
7. **Maintainability** - Code lisible, commenté si complexe

## Testing Strategy

**Backend**: pytest avec 80%+ coverage
- Unit tests pour services
- Integration tests pour routes
- Mock Supabase client

**Mobile**: Jest + React Testing Library
- Component tests
- Hook tests
- Integration tests

**Database**: Supabase local development
- Test RLS policies
- Test functions
- Test migrations

## Deployment

**Backend**: Railway, Render, ou Fly.io
- Env variables pour secrets
- Health check endpoint
- Logging configuré

**Mobile**: Expo EAS Build
- iOS App Store
- Google Play Store
- OTA updates

**Database**: Supabase hosted
- Automatic backups
- Point-in-time recovery
- Monitoring dashboard

## Token Economy

**Total Standards**: ~3900 tokens

**Optimisations**:
- Exemples concis mais complets
- Pas de répétition
- Focus sur patterns réutilisables
- Code commenté seulement si nécessaire

**Usage Recommandé**:
- Include standards pertinent dans context quand besoin
- Ne pas inclure tous les standards à chaque fois
- Référencer par lien plutôt que copier

## Updates

**Version 1.0** (2024-12-27):
- Initial standards pour ForkIt
- FastAPI, React Native, Supabase
- Prêt pour Maison Epigenetic

**Prochaines versions**:
- Patterns avancés (caching, real-time)
- CI/CD guidelines
- Monitoring et logging
- Scaling strategies

---

**Maintenu par**: Agent OS + Claude Code
**Contact**: Voir [NOTION-SETUP-GUIDE.md](../NOTION-SETUP-GUIDE.md) pour tracking
