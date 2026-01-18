# Tests Utilisateur - Agent-OS API Endpoints

## Feature
**Nom:** Agent-OS API Endpoints for Tracker Synchronization
**Date:** 2026-01-18
**Status:** Pret pour tests

---

## Prerequis
- Application AgentOS-Tracker deployee et accessible
- Variable d'environnement `AGENT_OS_API_KEY` configuree
- Outil de test API disponible (curl, Postman, Insomnia, ou HTTPie)
- Base de donnees Supabase accessible avec les migrations appliquees
- Au moins un projet, une feature et un sprint existants pour les tests

---

## Scenarios de Test

### UT-001: Authentification API - Cle valide
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Ouvrir un outil de test API (ex: Postman)<br>2. Configurer une requete POST vers `/api/agent-os/projects`<br>3. Ajouter le header `Authorization: Bearer <AGENT_OS_API_KEY>`<br>4. Ajouter un body JSON: `{ "external_id": "test-auth", "name": "Test Auth" }`<br>5. Envoyer la requete |
| **Resultat attendu** | - Status HTTP 201 Created<br>- Le body contient un objet `data` avec le projet cree<br>- Le body contient un `request_id` unique |
| **Status** | A tester |

---

### UT-002: Authentification API - Cle manquante
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Configurer une requete POST vers `/api/agent-os/projects`<br>2. Ne PAS ajouter de header Authorization<br>3. Ajouter un body JSON valide<br>4. Envoyer la requete |
| **Resultat attendu** | - Status HTTP 401 Unauthorized<br>- Body: `{ "error": { "code": "AUTH_MISSING", "message": "...", "request_id": "..." } }` |
| **Status** | A tester |

---

### UT-003: Authentification API - Cle invalide
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Configurer une requete POST vers `/api/agent-os/projects`<br>2. Ajouter le header `Authorization: Bearer mauvaise-cle-api`<br>3. Ajouter un body JSON valide<br>4. Envoyer la requete |
| **Resultat attendu** | - Status HTTP 401 Unauthorized<br>- Body: `{ "error": { "code": "AUTH_INVALID", "message": "...", "request_id": "..." } }` |
| **Status** | A tester |

---

### UT-004: Creer un nouveau projet
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Configurer POST `/api/agent-os/projects` avec auth valide<br>2. Body: `{ "external_id": "2026-01-18-nouveau-projet", "name": "Mon Nouveau Projet", "description": "Description du projet" }`<br>3. Envoyer la requete<br>4. Verifier dans l'UI Tracker que le projet apparait |
| **Resultat attendu** | - Status HTTP 201 Created<br>- Le projet est visible dans l'interface AgentOS-Tracker<br>- Les champs name et description correspondent |
| **Status** | A tester |

---

### UT-005: Mettre a jour un projet existant (upsert)
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Utiliser le projet cree dans UT-004<br>2. Envoyer POST `/api/agent-os/projects` avec le meme external_id<br>3. Body: `{ "external_id": "2026-01-18-nouveau-projet", "name": "Projet Renomme" }`<br>4. Verifier dans l'UI que le nom a change |
| **Resultat attendu** | - Status HTTP 200 OK<br>- Un seul projet existe avec cet external_id<br>- Le nom est mis a jour dans l'interface |
| **Status** | A tester |

---

### UT-006: Creer une nouvelle feature
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Recuperer l'ID du projet cree<br>2. POST `/api/agent-os/features` avec auth valide<br>3. Body: `{ "external_id": "2026-01-18-nouvelle-feature", "project_id": "<project_id>", "title": "Ma Feature", "description": "Description" }`<br>4. Verifier dans l'UI |
| **Resultat attendu** | - Status HTTP 201 Created<br>- La feature apparait dans le projet<br>- La phase par defaut est "raw-idea" |
| **Status** | A tester |

---

### UT-007: Progression de phase d'une feature
| Champ | Valeur |
|-------|--------|
| **Priorite** | Haute |
| **Etapes** | 1. Utiliser la feature creee dans UT-006<br>2. Envoyer POST `/api/agent-os/features` avec phase: "write"<br>3. Verifier la phase dans l'UI<br>4. Repeter avec phases: "tasks", "implement", "verify" |
| **Resultat attendu** | - Chaque appel retourne 200 OK<br>- La phase est mise a jour visuellement dans l'interface<br>- La progression suit: raw-idea -> write -> tasks -> implement -> verify |
| **Status** | A tester |

---

### UT-008: Creation de taches en masse
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Recuperer l'ID de la feature creee<br>2. POST `/api/agent-os/tasks` avec auth valide<br>3. Body: `{ "tasks": [{ "title": "Tache 1", "feature_id": "<id>" }, { "title": "Tache 2", "feature_id": "<id>" }, { "title": "Tache 3", "feature_id": "<id>" }] }`<br>4. Verifier dans l'UI |
| **Resultat attendu** | - Status HTTP 201 Created<br>- 3 taches sont creees<br>- Toutes les taches sont assignees au sprint actif<br>- Les taches apparaissent dans la vue Kanban |
| **Status** | A tester |

---

### UT-009: Assignment automatique au sprint actif
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. S'assurer qu'un sprint "actif" existe<br>2. Creer des taches via l'API<br>3. Verifier le sprint_id dans la reponse<br>4. Verifier dans l'UI que les taches sont dans le bon sprint |
| **Resultat attendu** | - Les taches sont automatiquement assignees au sprint actif<br>- Si pas de sprint actif, elles vont au premier sprint "planning" |
| **Status** | A tester |

---

### UT-010: Mise a jour des statuts de taches
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Recuperer les IDs des taches creees<br>2. PATCH `/api/agent-os/tasks`<br>3. Body: `{ "tasks": [{ "id": "<id1>", "status": "in_progress" }, { "id": "<id2>", "status": "done" }] }`<br>4. Verifier dans la vue Kanban |
| **Resultat attendu** | - Status HTTP 200 OK<br>- Les taches se deplacent dans les bonnes colonnes Kanban<br>- Les statuts correspondent a la mise a jour |
| **Status** | A tester |

---

### UT-011: Mise a jour du temps de travail
| Champ | Valeur |
|-------|--------|
| **Priorite** | Haute |
| **Etapes** | 1. Recuperer l'ID d'une tache<br>2. PATCH `/api/agent-os/tasks`<br>3. Body: `{ "tasks": [{ "id": "<id>", "logged_hours": 4, "remaining_hours": 2 }] }`<br>4. Verifier dans l'UI les heures affichees |
| **Resultat attendu** | - Status HTTP 200 OK<br>- Les heures loguees et restantes sont mises a jour<br>- Les statistiques du sprint refletent les changements |
| **Status** | A tester |

---

### UT-012: Creation de tests en masse
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Recuperer l'ID de la feature<br>2. POST `/api/agent-os/tests`<br>3. Body: `{ "tests": [{ "name": "Test unitaire 1", "feature_id": "<id>" }, { "name": "Test integration", "feature_id": "<id>", "description": "Test e2e" }] }`<br>4. Verifier dans l'UI |
| **Resultat attendu** | - Status HTTP 201 Created<br>- Les tests sont crees avec status "pending" par defaut<br>- Les tests apparaissent dans la section tests de la feature |
| **Status** | A tester |

---

### UT-013: Mise a jour des statuts de tests
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Recuperer les IDs des tests crees<br>2. PATCH `/api/agent-os/tests`<br>3. Body: `{ "tests": [{ "id": "<id1>", "status": "passed" }, { "id": "<id2>", "status": "failed" }] }`<br>4. Verifier dans l'UI |
| **Resultat attendu** | - Status HTTP 200 OK<br>- Les tests affichent les bons statuts (passed en vert, failed en rouge)<br>- Les metriques de couverture sont mises a jour |
| **Status** | A tester |

---

### UT-014: Transaction - Rollback sur erreur (taches)
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. POST `/api/agent-os/tasks`<br>2. Body avec une tache valide ET une tache avec feature_id invalide<br>3. Verifier la reponse<br>4. Verifier qu'aucune tache n'a ete creee |
| **Resultat attendu** | - Status HTTP 400 ou 404<br>- Message d'erreur clair<br>- AUCUNE tache n'est creee (rollback complet) |
| **Status** | A tester |

---

### UT-015: Transaction - Rollback sur erreur (tests)
| Champ | Valeur |
|-------|--------|
| **Priorite** | Haute |
| **Etapes** | 1. POST `/api/agent-os/tests`<br>2. Body avec un test valide ET un test avec feature_id inexistant<br>3. Verifier qu'aucun test n'a ete cree |
| **Resultat attendu** | - Transaction annulee completement<br>- Aucun test cree dans la base |
| **Status** | A tester |

---

### UT-016: Validation - Champs requis manquants (projet)
| Champ | Valeur |
|-------|--------|
| **Priorite** | Haute |
| **Etapes** | 1. POST `/api/agent-os/projects`<br>2. Body: `{ "name": "Projet sans external_id" }` (external_id manquant)<br>3. Verifier l'erreur |
| **Resultat attendu** | - Status HTTP 400 Bad Request<br>- Error code: VALIDATION_ERROR<br>- Message indiquant que external_id est requis |
| **Status** | A tester |

---

### UT-017: Validation - Champs requis manquants (feature)
| Champ | Valeur |
|-------|--------|
| **Priorite** | Haute |
| **Etapes** | 1. POST `/api/agent-os/features`<br>2. Body sans project_id<br>3. Verifier l'erreur |
| **Resultat attendu** | - Status HTTP 400 Bad Request<br>- Error code: VALIDATION_ERROR |
| **Status** | A tester |

---

### UT-018: Validation - Phase invalide
| Champ | Valeur |
|-------|--------|
| **Priorite** | Moyenne |
| **Etapes** | 1. POST `/api/agent-os/features`<br>2. Body avec phase: "phase-inexistante"<br>3. Verifier l'erreur |
| **Resultat attendu** | - Status HTTP 400 Bad Request<br>- Message listant les phases valides |
| **Status** | A tester |

---

### UT-019: Validation - Status de tache invalide
| Champ | Valeur |
|-------|--------|
| **Priorite** | Moyenne |
| **Etapes** | 1. PATCH `/api/agent-os/tasks`<br>2. Body avec status: "status-invalide"<br>3. Verifier l'erreur |
| **Resultat attendu** | - Status HTTP 400 Bad Request<br>- Message listant les statuts valides |
| **Status** | A tester |

---

### UT-020: Request ID - Tracabilite
| Champ | Valeur |
|-------|--------|
| **Priorite** | Moyenne |
| **Etapes** | 1. Effectuer plusieurs requetes API (successe et erreurs)<br>2. Noter les request_id retournes<br>3. Verifier qu'ils sont tous differents et au format UUID |
| **Resultat attendu** | - Chaque reponse contient un request_id unique<br>- Le format est un UUID valide (ex: "550e8400-e29b-41d4-a716-446655440000") |
| **Status** | A tester |

---

### UT-021: Workflow complet - Cycle de vie d'une feature
| Champ | Valeur |
|-------|--------|
| **Priorite** | Critique |
| **Etapes** | 1. Creer un projet via API<br>2. Creer une feature via API<br>3. Creer 5 taches pour cette feature<br>4. Creer 3 tests pour cette feature<br>5. Mettre a jour les taches vers "done"<br>6. Mettre a jour les tests vers "passed"<br>7. Verifier l'etat final dans l'UI |
| **Resultat attendu** | - Toutes les entites sont creees et liees<br>- Les mises a jour sont appliquees<br>- L'UI reflete correctement l'etat final<br>- La feature a progresse dans ses phases |
| **Status** | A tester |

---

### UT-022: Idempotence - Upsert repetitif
| Champ | Valeur |
|-------|--------|
| **Priorite** | Haute |
| **Etapes** | 1. Envoyer 3 fois la meme requete POST /api/agent-os/projects<br>2. Envoyer 3 fois la meme requete POST /api/agent-os/features<br>3. Verifier le nombre d'entites en base |
| **Resultat attendu** | - Un seul projet existe avec l'external_id<br>- Une seule feature existe avec l'external_id<br>- Aucune erreur sur les appels repetes |
| **Status** | A tester |

---

## Resume

| Priorite | Nombre de tests |
|----------|-----------------|
| Critique | 11 |
| Haute | 7 |
| Moyenne | 4 |
| **Total** | **22** |

---

## Notes

### Outils de test recommandes
- **Postman**: Collection disponible dans `/docs/postman/agent-os-api.json`
- **curl**: Exemples de commandes fournis ci-dessous
- **HTTPie**: Alternative CLI plus lisible

### Exemples curl

```bash
# Test d'authentification valide
curl -X POST http://localhost:3000/api/agent-os/projects \
  -H "Authorization: Bearer $AGENT_OS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"external_id": "test-curl", "name": "Test Curl"}'

# Test de creation de taches
curl -X POST http://localhost:3000/api/agent-os/tasks \
  -H "Authorization: Bearer $AGENT_OS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tasks": [{"title": "Tache 1", "feature_id": "uuid-feature"}]}'

# Test de mise a jour de statut
curl -X PATCH http://localhost:3000/api/agent-os/tasks \
  -H "Authorization: Bearer $AGENT_OS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tasks": [{"id": "uuid-task", "status": "done"}]}'
```

### Environnements de test
- **Local**: `http://localhost:3000`
- **Staging**: `https://staging.agentos-tracker.example.com`
- **Production**: `https://agentos-tracker.example.com`

### Points d'attention
- Verifier que le `AGENT_OS_API_KEY` n'est PAS expose dans les logs ou reponses
- Tester avec des volumes importants (50+ taches) pour verifier la performance
- S'assurer que les transactions rollback correctement en cas d'erreur partielle
