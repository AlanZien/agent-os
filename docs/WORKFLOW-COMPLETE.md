# Agent-OS Complete Workflow

## 11 Étapes du Product au Code

```
1. /plan-product              → mission.md, roadmap.md, tech-stack.md, design-system.md
2. /bootstrap-project  (NEW)  → Structure projet complète (mobile/, backend/, supabase/)
3. /shape-spec (Phase 1)      → raw-idea.md
4. /shape-spec (Phase 2)      → requirements.md
5. /write-spec                → spec.md
6. /plan-tests                → test-plan.md (Given-When-Then)
7. /create-tasks              → tasks.md + sync Notion
8. /implement-tasks           → Code + Tests (TDD) + sync Notion
9. [Reprise automatique]      → Détection état + resume
10. [Itération task groups]   → Repeat step 8 pour chaque groupe
11. [Commit & Next Feature]   → git commit + nouvelle spec
```

## Détail Étape 2: /bootstrap-project (NOUVEAU)

### Avant (workflow incomplet)
```
/plan-product
↓
tech-stack.md créé
↓
❌ GAP: Vous devez manuellement:
   - npx create-expo-app mobile
   - cd mobile && npm install zustand @supabase/supabase-js
   - Créer supabase/client.ts manuellement
   - Créer stores/ manuellement
   - Créer backend/ manuellement
   - 30-60 minutes de setup manuel
↓
/shape-spec
```

### Maintenant (workflow complet)
```
/plan-product
↓
tech-stack.md créé
↓
/bootstrap-project  ← AUTOMATIQUE 🚀
↓
✅ Tout est créé en 2-3 minutes:
   - mobile/ initialisé (Expo)
   - supabase/ configuré
   - backend/ créé (si choisi)
   - Toutes dépendances installées
   - Configuration files créés
   - Initial commit fait
↓
/shape-spec
```

## Ce que /bootstrap-project fait automatiquement

### 1. Lit tech-stack.md
```markdown
Frontend: Expo (React Native) avec TypeScript
Backend: FastAPI avec Python
Database: Supabase
State: Zustand
Navigation: Expo Router
```

### 2. Exécute les commandes appropriées
```bash
# Frontend
npx create-expo-app@latest mobile --template blank
cd mobile && npm install @supabase/supabase-js zustand

# Backend
mkdir -p backend/app/models backend/app/routes backend/app/services
pip install -r backend/requirements.txt

# Supabase
mkdir -p supabase/migrations
```

### 3. Crée les fichiers de configuration

**mobile/services/supabase.ts**
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseKey)
```

**mobile/stores/authStore.ts** (exemple)
```typescript
import { create } from 'zustand'

interface AuthState {
  user: User | null
  setUser: (user: User | null) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}))
```

**backend/app/main.py**
```python
from fastapi import FastAPI

app = FastAPI(title="ForkIt API")

@app.get("/")
def read_root():
    return {"status": "ok"}
```

### 4. Fait le commit initial
```bash
git add .
git commit -m "chore: bootstrap project structure

- Initialize Expo project with TypeScript
- Add Supabase client configuration
- Add Zustand state management
- Set up FastAPI backend
- Create initial folder structure"
```

## Quand utiliser /bootstrap-project ?

### ✅ Utilisez /bootstrap-project si:
- Vous avez terminé `/plan-product`
- Vous voulez un setup automatique
- Vous voulez économiser 30-60 minutes
- Vous voulez des configurations standardisées

### ⚠️ N'utilisez PAS /bootstrap-project si:
- Vous n'avez pas encore fait `/plan-product`
- Vous voulez une structure personnalisée
- Vous préférez tout contrôler manuellement

## Testing ForkIt - Workflow Recommandé

Pour tester le workflow complet sur ForkIt:

```bash
# 1. Planification produit
/plan-product

# Questions interactives sur:
# - Mission du produit
# - Fonctionnalités principales
# - Stack technique (Expo, Supabase, Zustand...)
# - Design system

# Crée: mission.md, roadmap.md, tech-stack.md, design-system.md

# 2. Bootstrap automatique (NOUVEAU)
/bootstrap-project

# Lit tech-stack.md et crée AUTOMATIQUEMENT:
# - mobile/ (Expo initialisé)
# - backend/ (FastAPI si choisi)
# - supabase/ (structure + migrations)
# - Toutes configurations
# - Initial commit

# 3. Première feature
/shape-spec
# → Définit votre première fonctionnalité en détail

/write-spec
# → Crée spec.md technique

/plan-tests
# → Crée test-plan.md avec tous les tests

/create-tasks
# → Crée tasks.md + sync Notion

/implement-tasks
# → Implémente code + tests (TDD automatique)

# 4. Commit
git push

# 5. Feature suivante
# Relancer le cycle depuis /shape-spec
```

## Gains de Performance

| Étape | Avant | Maintenant | Gain |
|-------|-------|------------|------|
| Setup Expo | 10 min manuel | 1 min auto | -90% |
| Install deps | 15 min manuel | 1 min auto | -93% |
| Config files | 20 min manuel | 30 sec auto | -97% |
| Backend setup | 15 min manuel | 1 min auto | -93% |
| **TOTAL** | **60 min** | **3 min** | **-95%** |

## Architecture du Bootstrap

```
.claude/
  commands/
    agent-os/
      bootstrap-project.md        ← Commande orchestrateur
  agents/
    agent-os/
      project-bootstrapper.md     ← Agent exécutant

Workflow:
1. User tape: /bootstrap-project
2. Command lit: tech-stack.md
3. Command appelle: project-bootstrapper agent
4. Agent exécute: init commands
5. Agent crée: structure + configs
6. Agent fait: git commit
7. User reçoit: résumé de ce qui a été créé
```

## Prochaines Étapes Pour ForkIt

Maintenant que le workflow est complet:

1. **Tester le workflow** sur ForkIt
   ```bash
   /plan-product      # Définir la vision de ForkIt
   /bootstrap-project # Setup automatique
   /shape-spec       # Première feature
   ```

2. **Valider chaque étape**
   - Vérifier que les fichiers sont bien créés
   - Vérifier que les tests passent
   - Vérifier que Notion se sync correctement

3. **Documenter les bugs ou améliorations**
   - Noter ce qui fonctionne bien
   - Noter ce qui pourrait être amélioré

4. **Créer le template**
   - Nettoyer ForkIt de tout code spécifique
   - Garder uniquement le système Agent-OS
   - Fork sur GitHub ou archive locale

5. **Utiliser sur projet conséquent**
   - Clone du template
   - Lancer le workflow complet
   - Développer le vrai produit
