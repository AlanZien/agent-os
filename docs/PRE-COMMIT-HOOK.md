# Pre-Commit Hook - Guide d'Utilisation

## 📍 Emplacement

```
.git/hooks/pre-commit
```

## 🎯 Rôle

Ce hook s'exécute **automatiquement avant chaque commit** pour valider que :
- ✅ Tous les tests unitaires passent
- ✅ Le linting passe
- ✅ Le build TypeScript réussit

**Si un test échoue → le commit est BLOQUÉ** 🚫

## 🔧 Installation / Activation

### 1. Créer le hook

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Pre-Commit Test Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run unit tests
echo ""
echo "🔧 Running Unit Tests..."
npm run test:run
if [ $? -ne 0 ]; then
  echo "❌ Unit tests FAILED"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "❌ COMMIT BLOCKED - Fix tests before committing"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  exit 1
fi
echo "✅ Unit tests passed"

# Run linting
echo ""
echo "📝 Running Linter..."
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Linting FAILED"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "❌ COMMIT BLOCKED - Fix lint errors before committing"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  exit 1
fi
echo "✅ Linting passed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ALL CHECKS PASSED - Commit allowed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
exit 0
EOF
```

### 2. Rendre le hook exécutable

```bash
chmod +x .git/hooks/pre-commit
```

### 3. Tester le hook

```bash
git commit --dry-run -m "Test hook"
```

## 📊 Ce Que Le Hook Fait

### Étape 1 : Tests Unitaires
```bash
npm run test:run
```
- Exécute tous les tests Vitest
- ❌ Bloque si tests échouent

### Étape 2 : Linting
```bash
npm run lint
```
- Vérifie le code avec ESLint
- ❌ Bloque si erreurs de lint

## 🚨 Bypass du Hook (Déconseillé)

Si tu dois absolument commit avec des tests qui échouent :

```bash
git commit --no-verify -m "WIP: fixing tests"
```

**⚠️ À utiliser uniquement pour** :
- Work in progress (WIP) commits temporaires
- Situations d'urgence

**NE JAMAIS** bypass le hook pour :
- Push vers main/master
- Merge de pull requests

## 🔄 Workflow Recommandé

```bash
# 1. Développer + écrire tests
npm run test:run -- --watch

# 2. Une fois tests passent, commit
git add .
git commit -m "feat: add feature"
# → Hook valide automatiquement ✅

# 3. Push
git push
```

## 🆘 Troubleshooting

### "Permission denied"

```bash
chmod +x .git/hooks/pre-commit
```

### Hook ne s'exécute pas

```bash
ls -la .git/hooks/pre-commit
# Si absent, recréer avec les instructions ci-dessus
```

### Désactiver temporairement

```bash
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
```
