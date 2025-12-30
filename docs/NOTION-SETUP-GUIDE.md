# 📊 Notion PM System - Setup Guide Manuel

Guide rapide pour configurer les databases Notion pour ForkIt (réutilisable pour Maison Epigenetic).

## 🎯 Database 1 : Projects

**Ouvre la database "🎯 Projects"** dans Notion

### Propriétés à Créer

Clique sur **"+ Add a property"** pour chaque :

1. **Status** (Select)
   - Not Started (gray)
   - In Progress (blue)
   - On Hold (yellow)
   - Completed (green)
   - Cancelled (red)

2. **Phase** (Select)
   - Phase 0 - Setup (gray)
   - Phase 1 - ForkIt (blue)
   - Phase 2 - Maison Epigenetic (purple)

3. **% Done** (Number → Format: Percent)

4. **Start Date** (Date)

5. **End Date** (Date)

6. **Owner** (Person)

7. **Description** (Text)

### Première Entrée à Créer

**Clique "New"** et remplis :
- **Name**: Setup System
- **Status**: In Progress
- **Phase**: Phase 0 - Setup
- **% Done**: 50
- **Start Date**: 2024-12-27
- **Description**: Installation et configuration du système de développement complet (Agent OS + Claude-Mem + Notion PM + Standards)

---

## ✅ Database 2 : Tasks

**Ouvre la database "✅ Tasks"**

### Propriétés à Créer

1. **Status** (Select)
   - Todo (gray)
   - In Progress (blue)
   - Blocked (red)
   - Review (yellow)
   - Done (green)

2. **Priority** (Select)
   - Critical (red)
   - High (orange)
   - Medium (yellow)
   - Low (gray)

3. **Project** (Relation → Projects database)

4. **Assignee** (Person)

5. **Due Date** (Date)

6. **Story Points** (Number)

7. **Time Estimate (h)** (Number)

8. **Time Spent (h)** (Number)

9. **Tags** (Multi-select)
   - Backend (blue)
   - Frontend (green)
   - Database (purple)
   - DevOps (orange)
   - Testing (pink)
   - Documentation (gray)

10. **Blocked By** (Relation → Tasks database - self-relation)

11. **Dependencies** (Text)

12. **Notes** (Text)

### 8 Tâches Initiales à Créer

Clique **"New"** 8 fois et remplis :

1. **Clone Agent OS**
   - Status: Done
   - Priority: High
   - Project: Setup System
   - Tags: DevOps

2. **Create ForkIt structure**
   - Status: Done
   - Priority: High
   - Project: Setup System
   - Tags: DevOps

3. **Setup Notion databases**
   - Status: Done
   - Priority: High
   - Project: Setup System
   - Tags: DevOps

4. **Configure Agent OS workflows**
   - Status: Todo
   - Priority: High
   - Project: Setup System
   - Tags: DevOps

5. **Create condensed standards**
   - Status: Todo
   - Priority: Medium
   - Project: Setup System
   - Tags: DevOps

6. **Setup Supabase project**
   - Status: Todo
   - Priority: Medium
   - Project: Setup System
   - Tags: DevOps

7. **Configure Claude-Mem**
   - Status: Todo
   - Priority: Low
   - Project: Setup System
   - Tags: DevOps

8. **Test complete workflow**
   - Status: Todo
   - Priority: High
   - Project: Setup System
   - Tags: DevOps

---

## 📋 Database 3 : Sprints

**Ouvre "📋 Sprints"**

### Propriétés

1. **Status** (Select): Planned, Active, Completed
2. **Start Date** (Date)
3. **End Date** (Date)
4. **Goal** (Text)
5. **Tasks** (Relation → Tasks)
6. **Velocity (SP)** (Number)
7. **Completed (SP)** (Number)
8. **Retrospective** (Text)

*(Pas de données initiales)*

---

## 🐛 Database 4 : Bugs

**Ouvre "🐛 Bugs"**

### Propriétés

1. **Status** (Select): New, Investigating, In Progress, Fixed, Wont Fix
2. **Severity** (Select): Critical, High, Medium, Low
3. **Project** (Relation → Projects)
4. **Assignee** (Person)
5. **Reported Date** (Date)
6. **Fixed Date** (Date)
7. **Steps to Reproduce** (Text)
8. **Root Cause** (Text)
9. **Fix Description** (Text)

*(Pas de données initiales)*

---

## 📝 Database 5 : Decisions (ADR)

**Ouvre "📝 Decisions (ADR)"**

### Propriétés

1. **Status** (Select): Proposed, Accepted, Rejected, Superseded
2. **Project** (Relation → Projects)
3. **Category** (Select): Architecture, Technology Stack, Design Pattern, Process, Security
4. **Decision Date** (Date)
5. **Decision Maker** (Person)
6. **Context** (Text)
7. **Decision** (Text)
8. **Consequences** (Text)
9. **Alternatives** (Text)

*(Pas de données initiales)*

---

## 📚 Database 6 : Standards

**Ouvre "📚 Standards"**

### Propriétés

1. **Category** (Select): Backend, Frontend, Database, Testing, Security, DevOps
2. **Status** (Select): Draft, Review, Active, Deprecated
3. **Token Size** (Number)
4. **Last Updated** (Date)
5. **File Path** (Text)
6. **Summary** (Text)

*(Pas de données initiales)*

---

## 🔄 Database 7 : Daily Standup

**Ouvre "🔄 Daily Standup"**

### Propriétés

1. **Project** (Relation → Projects)
2. **What I Did** (Text)
3. **What I Will Do** (Text)
4. **Blockers** (Text)
5. **Progress %** (Number → Percent)
6. **Time Spent (h)** (Number)
7. **Notes** (Text)

*(Pas de données initiales)*

---

## 🎨 Vues Recommandées à Créer

### Pour Tasks Database

**Vue Kanban** :
- Group by: Status
- Sort by: Priority (descending)

**Vue Timeline** :
- Layout: Timeline
- Date property: Due Date

### Pour Sprints Database

**Vue Timeline** :
- Layout: Timeline
- Start date: Start Date
- End date: End Date

### Pour Daily Standup

**Vue Calendar** :
- Layout: Calendar
- Date property: Date

---

## ✅ Checklist Final

- [ ] Database Projects : 7 propriétés + 1 projet créé
- [ ] Database Tasks : 12 propriétés + 8 tâches créées
- [ ] Database Sprints : 8 propriétés
- [ ] Database Bugs : 9 propriétés
- [ ] Database Decisions : 9 propriétés
- [ ] Database Standards : 6 propriétés
- [ ] Database Daily Standup : 7 propriétés
- [ ] Vue Kanban créée pour Tasks
- [ ] Relations testées (Project → Tasks fonctionne)

**Temps estimé : 10-15 minutes**

Une fois terminé, ton système PM Notion sera complètement opérationnel et réutilisable pour Maison Epigenetic ! 🚀
