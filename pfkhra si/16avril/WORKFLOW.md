# 🔄 Development Workflow - PF KHRA Project

Guide complet du workflow de développement pour le projet PF KHRA Transport & Logistics.

---

## 📋 Matin - Démarrage Session

### 1. Mise à jour du code
```bash
cd "c:\L3 ISIL A 2025-2026\PFKHRA\pfkhra si\16avril"
git pull origin adot
```

### 2. Activation environnement
```bash
venv\Scripts\activate
```

### 3. Vérification rapide
```bash
git status
git log --oneline -5
```

### 4. Lancement serveurs
```bash
# Terminal 1 - Backend
python manage.py runserver

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

---

## 💼 Pendant Développement

### 🔍 Avant de modifier:
```bash
# Vérifier branche actuelle
git branch

# S'assurer d'être sur adot
git checkout adot
```

### 📝 Cycle de développement:
```bash
# 1. Faire modifications...

# 2. Vérifier changements
git status
git diff

# 3. Tester rapidement
python manage.py check
python scripts/test_login_api.py

# 4. Stager et committer
git add .
git commit -m "Description claire du changement"

# 5. Pousser régulièrement
git push origin adot
```

### 🧪 Tests fréquents:
```bash
# Backend
python manage.py check
python manage.py migrate --check
python simple_test.py

# Frontend (dans dossier frontend)
npm run build  # Vérifier que ça compile
```

---

## 🔄 Fin de Session

### ✅ Check-list avant de quitter:
```bash
# 1. Sauvegarder travail
git add .
git commit -m "WIP: description du travail en cours"

# 2. Pousser vers GitHub
git push origin adot

# 3. Vérifier que tout est poussé
git status
git log --oneline -3
```

### 🛑 Arrêt propre:
```bash
# Terminal 1 - Ctrl+C pour arrêter Django
# Terminal 2 - Ctrl+C pour arrêter React
deactivate  # Désactiver venv
```

---

## 🚀 Workflow par Type de Tâche

### 🐛 Bug Fix:
```bash
git checkout -b fix/nom-du-bug
# ... travailler sur le bug ...
git add .
git commit -m "Fix: description du bug corrigé"
git checkout adot
git merge fix/nom-du-bug
git push origin adot
git branch -d fix/nom-du-bug
```

### ✨ Nouvelle Feature:
```bash
git checkout -b feature/nom-feature
# ... développer la feature ...
git add .
git commit -m "Feat: ajouter fonctionnalité X"
git checkout adot
git merge feature/nom-feature
git push origin adot
git branch -d feature/nom-feature
```

### 🔧 Refactoring:
```bash
git checkout -b refactor/nom-module
# ... refactoriser ...
git add .
git commit -m "Refactor: améliorer structure du module X"
git checkout adot
git merge refactor/nom-module
git push origin adot
git branch -d refactor/nom-module
```

---

## 🗄️ Gestion Base de Données

### 🔄 Après modifications SQL:
```bash
# 1. Mettre à jour les fichiers SQL
# 2. Tester localement
python scripts/init_db.py --reset
python manage.py migrate

# 3. Vérifier intégrité
python scripts/fix_db_integrity.py

# 4. Commiter les changements
git add db/
git commit -m "Update database schema/data: description"

# 5. Pousser
git push origin adot
```

### 🧪 Tests DB:
```bash
# Vérifier intégrité
python scripts/fix_db_integrity.py

# Test authentification
python simple_test.py

# Vérifier migrations
python manage.py migrate --check
```

---

## 📱 Workflow Frontend

### 🔄 Développement React:
```bash
cd frontend

# Installation dépendances
npm install

# Développement
npm run dev

# Build test
npm run build

# Tests (si configurés)
npm test
```

### 📦 Mise en production:
```bash
cd frontend
npm run build
# Les fichiers build/ sont prêts pour déploiement
```

---

## 🚨 Gestion des Conflits

### 🔄 Quand il y a un conflit:
```bash
# 1. Mettre à jour
git pull origin adot

# 2. Résoudre conflits dans les fichiers marqués
# (chercher <<<<<<<, =======, >>>>>>>)

# 3. Après résolution:
git add fichier_resolu.py
git commit -m "Resolve: conflit de fusion"

# 4. Pousser
git push origin adot
```

### 🛡️ Prévention des conflits:
```bash
# Toujours pull avant de push
git pull origin adot
git push origin adot

# Commits fréquents et petits
git add .
git commit -m "Petit changement spécifique"
git push origin adot
```

---

## 📊 Monitoring et Qualité

### 📈 Vérifications régulières:
```bash
# Statut du repository
git status

# Historique récent
git log --oneline --graph -10

# Branches
git branch -a

# Remote status
git remote -v
```

### 🔍 Code quality:
```bash
# Python (si configuré)
flake8 .
black .

# JavaScript (dans frontend)
cd frontend
npm run lint
```

---

## 🎯 Rôles et Responsabilités

### 👤 Développeur Backend:
- Maintenir les models Django
- Gérer les API endpoints
- S'assurer de l'intégrité DB
- Tester les migrations

### 👤 Développeur Frontend:
- Maintenir les composants React
- Gérer le routing
- Optimiser les performances
- Assurer la responsive design

### 👤 DevOps/Déploiement:
- Maintenir requirements.txt
- Gérer les environnements
- Surveiller les performances
- Gérer les backups

---

## 📝 Documentation

### 📚 À maintenir:
- `README.md` - Instructions setup
- `WORKFLOW.md` - Ce fichier
- `GIT_ROUTINE.md` - Commandes Git
- `QUICK_START.md` - Démarrage rapide

### 🔄 Quand documenter:
- Après chaque feature majeure
- Quand le workflow change
- Pour les procédures complexes
- Pour les problèmes récurrents

---

## 🆘 Procédures d'Urgence

### 💾 Backup avant gros changement:
```bash
git tag backup-$(date +%Y%m%d-%H%M%S)
git push origin --tags
```

### 🔄 Rollback:
```bash
# Voir les états précédents
git reflog

# Revenir à un état stable
git reset --hard HEAD@{5}
git push --force-with-lease origin adot
```

### 🚨 Problème critique:
```bash
# 1. Créer issue sur GitHub
# 2. Taguer la version stable
git tag stable-$(date +%Y%m%d)
git push origin --tags
# 3. Travailler sur branch fix
git checkout -b hotfix/critical-issue
```

---

## 📅 Planning Hebdomadaire

### 🌅 Lundi:
- Pull et mise à jour
- Review des changements weekend
- Planning des tâches semaine

### 📊 Mercredi:
- Review du milieu de semaine
- Nettoyage des branches
- Mise à jour documentation

### 🌆 Vendredi:
- Finalisation des features
- Tests complets
- Préparation weekend

---

## 🎯 Objectifs de Qualité

### ✅ Pour chaque commit:
- [ ] Message clair et descriptif
- [ ] Tests passent
- [ ] Pas de fichiers inutiles
- [ ] Documentation mise à jour si besoin

### ✅ Pour chaque journée:
- [ ] Au moins un push
- [ ] Pas de conflits non résolus
- [ ] Backend et frontend fonctionnels
- [ ] Base de données stable

---

**💡 Astuce**: Gardez ce workflow ouvert pendant vos sessions de développement!

---

*Document maintenu pour l'équipe PF KHRA - Transport & Logistics*
