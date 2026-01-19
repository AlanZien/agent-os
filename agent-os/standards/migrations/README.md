# Migration Guides

Ce dossier contient des **guides de migration** pour faciliter le passage d'une stack technique à une autre.

## 📖 Quand Utiliser

Lorsque votre projet évolue et que vous devez migrer :
- **Database**: Supabase → AWS RDS, Firebase → PostgreSQL
- **Auth**: Supabase Auth → AWS Cognito, Auth0
- **Backend**: FastAPI monolith → Microservices
- **Frontend**: Expo managed → Expo bare workflow → React Native

## 📁 Structure d'un Guide de Migration

Chaque migration guide suit ce format:

```markdown
# Migration: [Source] vers [Destination]

## Overview
[Description courte de la migration et pourquoi]

## Prérequis
- Version minimum de [source]
- Services à configurer sur [destination]
- Outils nécessaires

## Impact
- **Complexité**: Faible / Moyenne / Élevée
- **Durée estimée**: X heures/jours
- **Risque**: Faible / Moyen / Élevé
- **Réversible**: Oui / Non

## Code Patterns à Remplacer

### Before ([Source])
\`\`\`typescript
// Code actuel avec [source]
\`\`\`

### After ([Destination])
\`\`\`typescript
// Nouveau code avec [destination]
\`\`\`

## Files Affectés
- `chemin/vers/fichier1.ts` → Modifications nécessaires
- `chemin/vers/fichier2.ts` → À remplacer entièrement
- `chemin/vers/fichier3.ts` → À supprimer

## Migration Steps

### 1. Préparation
[Steps de backup, tests, configuration]

### 2. Setup [Destination]
[Configuration du nouveau service]

### 3. Migration Data
[Si applicable, migration de données]

### 4. Update Code
[Remplacement du code]

### 5. Testing
[Tests à effectuer]

### 6. Deployment
[Déploiement et rollback plan]

## Rollback Plan
[Comment revenir en arrière si problème]

## Post-Migration
- [ ] Vérifier logs
- [ ] Monitoring actif
- [ ] Supprimer ancien service (après X jours)
```

## 📝 Exemple: Supabase → AWS RDS

### Fichier: `supabase-to-aws-rds.md`

**Overview**: Migration de Supabase (PostgreSQL managed + APIs) vers AWS RDS (PostgreSQL uniquement) pour plus de contrôle et réduction des coûts à grande échelle.

**Impact**:
- Complexité: Moyenne
- Durée: 2-3 jours
- Risque: Moyen (nécessite backup complet)
- Réversible: Oui (via backup)

**Code Changes**:
```typescript
// BEFORE: Supabase client
import { supabase } from '@/services/supabase'
const { data } = await supabase.from('users').select('*')

// AFTER: Direct PostgreSQL queries
import { pool } from '@/services/database'
const { rows } = await pool.query('SELECT * FROM users')
```

**Files Affectés**:
- `services/supabase.ts` → `services/database.ts`
- `hooks/useSupabase.ts` → `hooks/useDatabase.ts`
- Tous les stores Zustand qui utilisent Supabase
- `.env` variables (SUPABASE_URL → DATABASE_URL)

## 🚀 Workflow Automatisé (Futur)

Quand le command `/migrate-stack` sera implémenté:

```bash
# 1. User update tech-stack.md
database: supabase → database: aws-rds

# 2. Run migration command
/migrate-stack

# 3. Agent:
# - Détecte changement dans tech-stack.md
# - Lit migrations/supabase-to-aws-rds.md
# - Analyse codebase pour fichiers affectés
# - Crée spec de migration avec tasks
# - Replace standards: integrations/databases/supabase → aws-rds
# - Génère tests de migration

# 4. User valide et implémente via /implement-tasks
```

## 📚 Migrations Disponibles

### 🔜 À Créer (Quand Besoin)

Actuellement, le dossier est vide. Les migrations seront ajoutées **au besoin** quand:
1. Un votre projet démontre un besoin de migration
2. Une stack devient obsolète
3. Une amélioration est identifiée

**Migrations Probables**:
- `supabase-to-aws-rds.md`
- `supabase-auth-to-cognito.md`
- `expo-managed-to-bare.md`
- `fastapi-to-microservices.md`

## 🤝 Contributing

Pour ajouter un guide de migration:

1. **Créer le fichier**: `migrations/[source]-to-[destination].md`
2. **Suivre le template** ci-dessus
3. **Tester la migration** sur un projet réel
4. **Documenter les gotchas** et erreurs rencontrées
5. **Pull request** avec validation

## 📖 Références

- [Architecture Layered](../README.md)
- [Core Standards](../core/)
- [Integrations Standards](../integrations/)

---

**Note**: Les migrations sont documentées **après expérience pratique**, pas de manière théorique. Chaque guide provient d'une vraie migration effectuée sur un projet.
