# Agent-OS Usage Guide

## Workflow Tracks

Agent-OS utilise quatre tracks adaptes a la complexite de la feature. Le track est **detecte automatiquement** lors du `/shape-spec` via un scoring multidimensionnel (base × risque × integration + dependances).

---

## Les 4 Tracks

| Track | Score | Duree | Quand l'utiliser |
|-------|:-----:|-------|------------------|
| 🚀 **FAST** | ≤ 10 pts | 1-3 jours | Bug fixes, petites features, ajustements |
| ⚙️ **STANDARD** | 11-25 pts | 3-7 jours | Features completes, nouveaux ecrans |
| 🏗️ **COMPLEX** | 26-50 pts | 1-3 semaines | Multi-composants, integrations complexes |
| ⚠️ **EPIC** | > 50 pts | - | Trop large, doit etre decoupe en features plus petites |

---

## 🚀 Track FAST

### Workflow
```
/shape-spec → /write-spec → /create-tasks → /implement-tasks
```

### Caracteristiques
- Pas de test-plan obligatoire
- Implementation directe
- Verification standards uniquement

### Exemples
- Ajouter un bouton logout
- Fix bug d'affichage
- Nouveau champ dans un formulaire existant
- Ajustements styling/CSS

---

## ⚙️ Track STANDARD

### Workflow
```
/shape-spec → /write-spec → /plan-tests → /create-tasks → /implement-tasks → /verify
```

### Caracteristiques
- **Test-plan obligatoire** (TDD)
- Implementation avec tests
- Verification complete

### Exemples
- Recipe Browsing (liste + detail)
- Shopping List Generation
- User Profile & Preferences
- Favoris avec persistence

---

## 🏗️ Track COMPLEX

### Workflow
```
/shape-spec → /verify-spec → /write-spec → /plan-tests → /create-tasks → /orchestrate-tasks → /verify
```

### Caracteristiques
- **Verification de spec obligatoire**
- Test-plan exhaustif
- **Orchestration parallele** des agents
- Suite de verification complete

### Exemples
- Systeme d'authentification complet
- AI-Powered Menu Suggestions
- Offline Support avec sync
- Systeme de paiement

---

## Detection Automatique (Scoring Multidimensionnel)

Lors du `/shape-spec`, l'agent analyse les requirements et calcule un score de complexite en 3 etapes :

### 1. Points de Base

| Element | Points |
|---------|:------:|
| UI Components (ecrans, modals, forms) | 1 pt chacun |
| API Endpoints | 2 pts chacun |
| Database Changes (tables, migrations) | 3 pts chacun |
| External Integrations | 5 pts chacun |
| User Scenarios | 0.5 pts chacun |
| State Management (stores) | 2 pts chacun |
| Auth/Security implique | 3 pts |

### 2. Multiplicateurs

**Multiplicateur de Risque (selon le type de donnees) :**

| Type de donnees | Multiplicateur |
|-----------------|:--------------:|
| Standard (settings, preferences) | ×1 |
| Personnelles/PII (noms, emails) | ×1.5 |
| Sensibles (sante, finances) | ×2 |
| Critiques (auth, paiements) | ×2.5 |

**Multiplicateur d'Integration (selon la complexite externe) :**

| Type d'integration | Multiplicateur |
|--------------------|:--------------:|
| Interne uniquement | ×1 |
| API externe simple (REST, pas d'auth) | ×1.25 |
| API externe avec auth (OAuth, API keys) | ×1.5 |
| Integration complexe (webhooks, temps reel) | ×2 |

### 3. Bonus de Dependances

| Dependances | Bonus |
|-------------|:-----:|
| Feature standalone | +0 pts |
| 1-2 features dependantes | +2 pts |
| 3+ features dependantes | +5 pts |

### Formule

```
Score Final = (Base × Risque × Integration) + Dependances
```

### Exemple de calcul

**Feature : Sync donnees sante depuis wearable**
- Base : API(2) + DB(3) + External(5) = **10 pts**
- Risque : Donnees de sante = **×2**
- Integration : OAuth + webhooks = **×2**
- Dependances : 2 features dependantes = **+2 pts**

**Score Final : (10 × 2 × 2) + 2 = 42 pts → 🏗️ COMPLEX**

---

**Feature : Shopping List Generation (exemple classique)**
- Base : UI(3) + API(4) + DB(3) + Scenarios(2.5) + State(2) = **14.5 pts**
- Risque : Standard = **×1**
- Integration : Interne = **×1**
- Dependances : Aucune = **+0 pts**

**Score Final : (14.5 × 1 × 1) + 0 = 14.5 pts → ⚙️ STANDARD**

---

## Override du Track

Apres l'analyse, vous pouvez override le track recommande :

```
🎯 RECOMMENDED TRACK: ⚙️ STANDARD

Do you accept this track? (yes/override with: fast, standard, complex)
> fast
```

### Raisons de faire un override

| Override | Raison valide |
|----------|---------------|
| → FAST | Feature bien comprise, pattern existant, deadline serre |
| → STANDARD | Feature critique meme si petite, besoin de tests |
| → COMPLEX | Integration avec systemes externes, risque eleve |

---

## Fichiers generes par track

### 🚀 FAST
```
agent-os/specs/YYYY-MM-DD-feature-name/
├── raw-idea.md
├── planning/
│   ├── requirements.md
│   └── track.md
├── spec.md
└── tasks.md
```

### ⚙️ STANDARD
```
agent-os/specs/YYYY-MM-DD-feature-name/
├── raw-idea.md
├── planning/
│   ├── requirements.md
│   ├── track.md
│   └── visuals/
├── spec.md
├── tasks.md
├── test-plan.md          ← Obligatoire
└── verifications/
    └── final-verification.md
```

### 🏗️ COMPLEX
```
agent-os/specs/YYYY-MM-DD-feature-name/
├── raw-idea.md
├── planning/
│   ├── requirements.md
│   ├── track.md
│   └── visuals/
├── spec.md
├── spec-verification.md  ← Obligatoire
├── tasks.md
├── test-plan.md          ← Obligatoire
├── implementation/
│   └── [task-group-reports]
└── verifications/
    └── final-verification.md
```

---

## Commandes par Track

| Commande | FAST | STANDARD | COMPLEX |
|----------|------|----------|---------|
| `/shape-spec` | ✅ | ✅ | ✅ |
| `/verify-spec` | - | - | ✅ Obligatoire |
| `/write-spec` | ✅ | ✅ | ✅ |
| `/plan-tests` | Optionnel | ✅ Obligatoire | ✅ Obligatoire |
| `/create-tasks` | ✅ | ✅ | ✅ |
| `/implement-tasks` | ✅ | ✅ | - |
| `/orchestrate-tasks` | - | - | ✅ |
| Verification finale | Standards only | ✅ Complet | ✅ Complet |

---

## Regle de decision rapide

> **En cas de doute, laissez la detection automatique decider.**

Le calcul du score est base sur des criteres objectifs. Si vous pensez que le track recommande est incorrect, c'est souvent parce que :

1. Vous sous-estimez la complexite (laissez STANDARD)
2. Vous avez deja un pattern similaire (override vers FAST)
3. La feature a des implications cachees (override vers COMPLEX)

---

## Notes

- Le track est sauvegarde dans `planning/track.md`
- Changer de track en cours de route est possible mais deconseille
- Les standards (`verify-standards.sh`) sont verifies a tous les tracks
- La sync Notion fonctionne a tous les tracks
