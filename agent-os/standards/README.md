# Agent-OS Standards

Standards organisés en **architecture layered** pour supporter l'évolution des stacks techniques.

## 📁 Structure

```
standards/
├── global/                    # Standards universels (tous projets)
│   ├── global-standards.md
│   ├── security.md
│   ├── ci-cd-devops.md
│   └── code-quality.md
│
├── testing/                   # Standards de tests (universels)
│   └── test-writing.md
│
├── core/                      # Core frameworks (rarement changent)
│   └── mobile-expo/
│       ├── MOBILE-EXPO.md
│       └── expo-patterns.md
│
├── integrations/              # Services (peuvent changer)
│   ├── databases/
│   │   └── supabase/
│   │       ├── DATABASE-SUPABASE.md
│   │       └── supabase-patterns.md
│   ├── backend/
│   │   └── fastapi/
│   │       ├── BACKEND-FASTAPI.md
│   │       └── fastapi-patterns.md
│   └── auth/
│       └── supabase-auth/
│
└── migrations/                # Migration guides
    └── README.md
```

## 🎯 Philosophie

### Séparation en Couches

#### 1️⃣ Global (Stable ∞)
Standards qui s'appliquent à **tous les projets**, quelle que soit la stack :
- Conventions de code
- Sécurité (OWASP, auth, secrets)
- CI/CD et DevOps
- Qualité du code

**Changent**: Jamais (ou très rarement)

#### 2️⃣ Core (Stable 2-5 ans)
Frameworks principaux qui définissent l'architecture :
- Frontend: `mobile-expo`, `web-nextjs`, `web-vite`
- Ces choix sont **structurants** et changent rarement

**Changent**: Quand refonte majeure (ex: Expo → React Native pur)

#### 3️⃣ Integrations (Flexible 6-18 mois)
Services qui peuvent évoluer sans impacter le core :
- Databases: `supabase` → `aws-rds` → `firebase`
- Auth: `supabase-auth` → `aws-cognito` → `auth0`
- Backend: `fastapi` → `express` → microservices

**Changent**: Quand le projet scale ou pivot

## 🔄 Évolution d'une Stack

### Exemple: Projet {ProjectName}

**Phase 1: MVP (Mois 0-6)**
```yaml
core: mobile-expo
integrations:
  database: supabase
  auth: supabase-auth
  backend: fastapi
```

**Phase 2: Scale (Mois 6-12)**
```yaml
core: mobile-expo           # ✅ Reste stable
integrations:
  database: aws-rds        # ⚠️ Migration depuis Supabase
  auth: aws-cognito        # ⚠️ Migration depuis Supabase Auth
  backend: fastapi         # ✅ Reste stable
```

**Phase 3: Refonte (Mois 12+)**
```yaml
core: mobile-react-native  # ⚠️ Migration depuis Expo (rare)
integrations:
  database: aws-rds
  auth: aws-cognito
  backend: microservices   # ⚠️ Migration depuis FastAPI monolith
```

### Avantages

✅ **Isolation des changements**
- Migrer database n'affecte pas le code mobile
- Les standards Expo restent valides même si DB change

✅ **Migration guidée**
- Guides dans `migrations/`
- Command `/migrate-stack` (futur)

✅ **Réutilisabilité**
- Nouveau projet: Mix & match des standards existants
- Expo + Firebase: `core/mobile-expo` + `integrations/databases/firebase`

## 📖 Comment Utiliser

### 1. Nouveau Projet

**Lors de `/plan-product`:**
```
User choisit:
- Frontend: Expo
- Database: Supabase
- Backend: FastAPI
```

**`/bootstrap-project` copie automatiquement:**
```
→ core/mobile-expo/         (standards Expo)
→ integrations/databases/supabase/
→ integrations/backend/fastapi/
```

### 2. Migration de Stack

**Décision de migrer:**
```yaml
# tech-stack.md (AVANT)
database: supabase

# tech-stack.md (APRÈS)
database: aws-rds
```

**`/migrate-stack` (futur):**
1. Lit `migrations/supabase-to-aws-rds.md`
2. Remplace standards: `integrations/databases/supabase` → `aws-rds`
3. Analyse code affecté
4. Crée spec de migration + tasks

### 3. Agents Utilisent les Standards

Les agents chargent automatiquement:
```markdown
# implementer.md
@agent-os/standards/global/security.md
@agent-os/standards/core/mobile-expo/
@agent-os/standards/integrations/databases/supabase/
```

## 🆕 Ajouter une Nouvelle Stack

### Stack Populaire (Web Next.js)

**1. Créer la structure:**
```bash
mkdir -p agent-os/standards/core/web-nextjs
```

**2. Créer les standards:**
```
core/web-nextjs/
├── FRONTEND-NEXTJS.md      # Patterns Next.js (App Router, SSR, etc.)
└── nextjs-patterns.md      # Components, routing, data fetching
```

**3. Intégration avec Supabase:**
```
integrations/databases/supabase/
├── DATABASE-SUPABASE.md    # ✅ Déjà existe (réutilisable)
└── supabase-web.md         # Patterns spécifiques web (si nécessaire)
```

### Stack Rare (Génération)

Si stack non couverte:
```bash
/generate-standards
# Agent génère standards basés sur:
# - templates/ (génériques)
# - stacks similaires
# - Connaissance Claude
```

## 📊 Stacks Actuellement Supportées

### ✅ Mobile
- **Expo + Supabase + FastAPI** (complet)

### 🔄 Web (À venir)
- Next.js + Supabase
- Vite + Firebase

### 🔄 Backend (À venir)
- Express + MongoDB
- Django + PostgreSQL

## 🤝 Contributing

Pour ajouter une nouvelle stack:
1. Fork le repo template
2. Créer `core/[framework]/` ou `integrations/[service]/`
3. Suivre le format des standards existants
4. Pull request

---

**Architecture Version**: 2.0
**Last Updated**: 2025-12-30
