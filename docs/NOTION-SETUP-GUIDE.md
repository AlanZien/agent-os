# 📊 Notion PM System - Setup Guide

Guide pour configurer les databases Notion pour AgentOS-Tracker.

## 🎯 Database 1 : Projects

**Ouvre la database "🎯 Projects"** dans Notion

### Propriétés à Créer

1. **Status** (Select)
   - Not Started (gray)
   - In Progress (blue)
   - On Hold (yellow)
   - Completed (green)
   - Cancelled (red)

2. **Phase** (Select)
   - Phase 0 - Setup (gray)
   - Phase 1 - Core Features (blue)
   - Phase 2 - Advanced Features (purple)

3. **% Done** (Number → Format: Percent)

4. **Start Date** (Date)

5. **End Date** (Date)

6. **Owner** (Person)

7. **Description** (Text)

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

7. **Tags** (Multi-select)
   - Backend (blue)
   - Frontend (green)
   - Database (purple)
   - DevOps (orange)
   - Testing (pink)
   - Documentation (gray)

8. **Notes** (Text)

---

## 📋 Database 3 : Specs

**Ouvre "📋 Specs"**

### Propriétés

1. **Status** (Select): Draft, In Progress, Completed
2. **Project** (Relation → Projects)
3. **Created Date** (Date)
4. **Completion Date** (Date)
5. **Description** (Text)

---

## 🧪 Database 4 : Tests

**Ouvre "🧪 Tests"**

### Propriétés

1. **Status** (Select): Passing, Failing, Pending
2. **Type** (Select): Unit, Integration, E2E
3. **Spec** (Relation → Specs)
4. **File Path** (Text)
5. **Test Count** (Number)
6. **Notes** (Text)

---

## 🐛 Database 5 : Bugs

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

---

## 🎨 Vues Recommandées

### Pour Tasks Database

**Vue Kanban** :
- Group by: Status
- Sort by: Priority (descending)

### Pour Tests Database

**Vue Table** :
- Group by: Type
- Filter: Status = Failing (pour voir les problèmes)

---

## ✅ Checklist Final

- [ ] Database Projects créée avec propriétés
- [ ] Database Tasks créée avec propriétés
- [ ] Database Specs créée avec propriétés
- [ ] Database Tests créée avec propriétés
- [ ] Database Bugs créée avec propriétés
- [ ] Relations testées

**Temps estimé : 10-15 minutes**
