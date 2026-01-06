# User Testing Database

## Overview

À la fin de chaque implémentation de feature, des tests utilisateur peuvent être ajoutés à une database Notion dédiée pour tracker les tests manuels requis.

## Database Structure

Créer une database Notion "Tests Utilisateur - AgentOS-Tracker" avec les propriétés suivantes :

| Property | Type | Options |
|----------|------|---------|
| Name | Title | - |
| Groupe | Select | Auth, Dashboard, Settings, etc. |
| Statut | Select | À tester, Validé, Bug |
| Priorité | Select | Critique, Important, Normal |
| Étapes | Text | Instructions étape par étape |
| Résultat attendu | Text | Ce qui devrait se passer |
| Date | Date | Date de complétion du test |

## Workflow Integration

### Après avoir complété un Task Group :

1. Identifier toutes les features user-facing implémentées
2. Créer les entrées de test dans la database via MCP :

```json
{
  "parent": {"type": "data_source_id", "data_source_id": "[your-database-id]"},
  "pages": [{
    "properties": {
      "Name": "Description de la feature à tester",
      "Groupe": "Auth",
      "Statut": "À tester",
      "Priorité": "Critique",
      "Étapes": "1. Aller sur /login\n2. Entrer email\n3. Entrer password\n4. Cliquer Login",
      "Résultat attendu": "Redirection vers /dashboard"
    }
  }]
}
```

### Flow des Statuts :

```
À tester → Validé (si test passe)
         → Bug (si test échoue - créer bug dans 🐛 Bugs database)
```

## Exemple: Tests Authentication

| Test | Priorité |
|------|----------|
| Inscription avec email valide | Critique |
| Validation email (format) | Critique |
| Login après inscription | Critique |
| Forgot password flow | Important |
| Magic link login | Important |
| Logout | Important |
| Protection route /dashboard | Critique |
| Redirect authenticated user from /login | Normal |

## Bénéfices

- Visibilité claire sur ce qui doit être testé manuellement
- Tracking du progrès des tests par feature group
- Lien entre bugs découverts et tests spécifiques
- Assurance qu'aucune feature n'est livrée sans QA manuel
