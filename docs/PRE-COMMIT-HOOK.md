# Pre-Commit Hook - Guide d'Utilisation

## 📍 Emplacement

```
.git/hooks/pre-commit
```

## 🎯 Rôle

Ce hook s'exécute **automatiquement avant chaque commit** pour valider que :
- ✅ Tous les tests backend passent (si backend existe)
- ✅ Tous les tests frontend passent (si frontend existe)
- ✅ La couverture de tests est complète (si test-plan.md existe)

**Si un test échoue → le commit est BLOQUÉ** 🚫

## 🔧 Installation / Activation

### 1. Vérifier que le hook existe

```bash
ls -la .git/hooks/pre-commit
```

Si le fichier existe, passer à l'étape 2.

### 2. Rendre le hook exécutable

```bash
chmod +x .git/hooks/pre-commit
```

### 3. Tester le hook

```bash
# Faire un commit test (sans réellement committer)
git commit --dry-run -m "Test hook"

# Ou faire un vrai commit
git add .
git commit -m "Test pre-commit hook"
```

## 📊 Ce Que Le Hook Fait

### Étape 1 : Backend Tests
```bash
cd backend
pytest --tb=short -q
```

- Exécute tous les tests pytest du backend
- Affiche résumé court des failures
- ❌ Bloque si tests échouent

### Étape 2 : Frontend Tests
```bash
cd mobile
npm test -- --passWithNoTests --silent
```

- Exécute tous les tests Jest/React Native Testing Library
- Mode silencieux (moins verbeux)
- ❌ Bloque si tests échouent

### Étape 3 : Validation Couverture
```bash
./scripts/verify-tests.sh agent-os/specs/[current-spec]
```

- Compare tests planifiés (test-plan.md) vs tests implémentés
- Vérifie que tous les tests Critical et High sont présents
- ❌ Bloque si couverture < 100% pour Critical/High

## 🎨 Exemple de Sortie

### ✅ Cas de Succès (Commit Autorisé)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 Pre-Commit Test Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Current Spec: agent-os/specs/2024-01-15_user-authentication

🔧 Running Backend Tests...
✅ Backend tests passed

📱 Running Frontend Tests...
✅ Frontend tests passed

📊 Verifying Test Coverage...
✅ Test coverage verified

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ALL CHECKS PASSED - Commit allowed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### ❌ Cas d'Échec (Commit Bloqué)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 Pre-Commit Test Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Current Spec: agent-os/specs/2024-01-15_user-authentication

🔧 Running Backend Tests...
❌ Backend tests FAILED

FAILED backend/tests/test_user.py::test_user_creation_requires_email

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ COMMIT BLOCKED

Tests are failing. Please fix the issues before committing.

To debug:
  - Check test output above
  - Run: pytest backend/tests/ -v
  - Run: npm test --prefix mobile
  - Run: ./scripts/verify-tests.sh agent-os/specs/2024-01-15_user-authentication

To skip this hook (NOT RECOMMENDED):
  git commit --no-verify

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🚨 Bypass du Hook (Déconseillé)

Si tu dois absolument commit avec des tests qui échouent :

```bash
git commit --no-verify -m "WIP: fixing tests"
```

**⚠️ À utiliser uniquement pour** :
- Work in progress (WIP) commits temporaires
- Commits de debug
- Situations d'urgence

**NE JAMAIS** bypass le hook pour :
- Push vers main/master
- Merge de pull requests
- Release commits

## 🔄 Workflow Recommandé

### Développement Normal
```bash
# 1. Implémenter feature + tests
vim backend/models/user.py
vim backend/tests/test_user.py

# 2. Run tests manuellement pendant dev
pytest backend/tests/test_user.py -v

# 3. Une fois tests passent, commit
git add .
git commit -m "Add user email validation"
# → Hook valide automatiquement ✅

# 4. Push
git push
```

### Si Hook Bloque
```bash
# 1. Identifier le problème
./scripts/verify-tests.sh agent-os/specs/current-spec
pytest backend/tests/ -v

# 2. Fixer le problème
# - Corriger le code
# - OU fixer le test
# - OU logger bug dans Notion

# 3. Re-tester
pytest backend/tests/ -v

# 4. Re-essayer commit
git commit -m "Fix email validation"
# → Hook valide ✅
```

## 🎯 Intégration avec Workflow Agent-OS

Le pre-commit hook s'intègre naturellement dans le workflow :

```
/implement-tasks
  ↓
[Agent implémente + tests]
  ↓
[Agent run tests localement]
  ↓
[Agent update tasks.md]
  ↓
git add .
git commit -m "..."  ← 🚨 Pre-commit hook s'exécute ICI
  ↓
✅ Si tests passent → Commit réussit
❌ Si tests échouent → Commit bloqué
  ↓
git push
```

## 📋 Checklist Avant Commit

Avant chaque commit, le hook vérifie automatiquement :

- [ ] Backend tests passent (`pytest`)
- [ ] Frontend tests passent (`npm test`)
- [ ] Couverture tests complète (`verify-tests.sh`)
- [ ] Aucune régression introduite

Si tout est ✅ → Commit autorisé
Si un seul ❌ → Commit bloqué

## 🆘 Troubleshooting

### "Permission denied" lors du commit

**Problème** : Le hook n'est pas exécutable

**Solution** :
```bash
chmod +x .git/hooks/pre-commit
```

### Hook ne s'exécute pas du tout

**Problème** : Le fichier n'existe pas ou est mal nommé

**Solution** :
```bash
# Vérifier présence
ls -la .git/hooks/pre-commit

# Si absent, recréer depuis backup
cp docs/PRE-COMMIT-HOOK.md.backup .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Hook s'exécute mais tests ne run pas

**Problème** : pytest ou npm non disponibles

**Solution** :
```bash
# Vérifier installations
which pytest
which npm

# Installer si manquant
pip install pytest
npm install
```

### Désactiver temporairement le hook

**Solution** :
```bash
# Renommer pour désactiver
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled

# Renommer pour réactiver
mv .git/hooks/pre-commit.disabled .git/hooks/pre-commit
```

## 📚 Références

- Script source : `.git/hooks/pre-commit`
- Validation tests : `scripts/verify-tests.sh`
- Test planning : `.claude/agents/agent-os/test-planner.md`
- Debug workflow : `.claude/agents/agent-os/implementer.md` (section "When Tests Fail")
