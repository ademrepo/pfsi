# 🚀 Git Routine - Cheat Sheet for Programming Sessions

Cheat sheet essentiel pour les commandes Git utilisées quotidiennement dans le développement du projet PF KHRA.

---

## 📋 Démarrage de Session

### 1. Récupérer les derniers changements
```bash
git pull origin adot
```

### 2. Vérifier l'état actuel
```bash
git status
```

### 3. Voir les derniers commits
```bash
git log --oneline -10
```

---

## 💼 Workflow Quotidien

### Pendant le développement:
```bash
# Voir ce qui a été modifié
git status

# Ajouter tous les changements
git add .

# Ajouter des fichiers spécifiques
git add core/views.py README.md

# Faire un commit avec message clair
git commit -m "Description claire du changement"

# Pousser vers GitHub
git push origin adot
```

## 🔧 Commandes Essentielles

### Vérification:
```bash
git status                    # État des fichiers
git log --oneline            # Historique compact
git diff                      # Voir les changements non commités
git diff --staged            # Voir les changements stagés
```

### Navigation:
```bash
git checkout adot             # Revenir à la branche principale
git checkout -b feature/nom   # Créer nouvelle branche
git branch                    # Voir les branches locales
git branch -a                 # Voir toutes les branches
```

### Annulation:
```bash
git checkout -- fichier.py    # Annuler changements dans un fichier
git reset HEAD fichier.py     # Unstage un fichier
git reset --soft HEAD~1       # Annuler dernier commit (garder changements)
git reset --hard HEAD~1       # Annuler dernier commit (perdre changements)
```

---

## 🔄 Gestion des Conflits

### Quand il y a un conflit:
```bash
# 1. Voir les fichiers en conflit
git status

# 2. Ouvrir les fichiers et résoudre les conflits manuellement
# (chercher <<<<<<<, =======, >>>>>>>)

# 3. Après résolution:
git add fichier_conflit.py
git commit -m "Résoudre conflit de fusion"
```

### Éviter les conflits:
```bash
# Toujours pull avant de push
git pull origin adot
git push origin adot
```

---

## 📊 Historique et Recherche

### Voir l'historique:
```bash
git log --oneline --graph      # Vue graphique
git log --author="Votre Nom"    # Commits d'un auteur
git log --grep="mot clé"        # Chercher dans les messages
git log --since="1 week ago"    # Commits récents
```

### Suivre les changements d'un fichier:
```bash
git log -p core/views.py        # Historique + changements
git blame core/views.py         # Qui a modifié chaque ligne
```

---

## 🏷️ Tags et Versions

### Créer un tag:
```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Release initiale"
git push origin v1.0.0
```

### Voir les tags:
```bash
git tag                          # Liste des tags
git show v1.0.0                  # Détails d'un tag
```

---

## 🛠️ Maintenance

### Nettoyer le repository:
```bash
git clean -fd                    # Supprimer fichiers non suivis
git gc                           # Garbage collection
git prune                         # Nettoyer branches inaccessibles
```

### Stash (mettre de côté temporairement):
```bash
git stash                        # Mettre changements de côté
git stash pop                    # Récupérer derniers changements
git stash list                   # Voir stashs disponibles
```

---

## 🌐 Remote Operations

### Voir les remotes:
```bash
git remote -v                    # Voir les URLs des remotes
git remote show origin           # Détails du remote origin
```

### Gérer les remotes:
```bash
git remote add upstream https://github.com/original/repo.git
git fetch upstream
git merge upstream/adot
```

---

## 🚨 Commandes de Sécurité

### Avant les opérations destructives:
```bash
# TOUJOURS vérifier:
git status
git log --oneline -5

# Faire une backup si nécessaire:
git branch backup-avant-changement
```

### Récupération d'urgence:
```bash
git reflog                       # Historique de toutes les opérations
git reset --hard HEAD@{2}        # Revenir à un état précédent
```

---

## 📝 Check-list Avant Push

### ✅ Checklist:
- [ ] `git status` - vérifier fichiers à commit
- [ ] `git diff --staged` - vérifier changements
- [ ] Message de commit clair et descriptif
- [ ] Tests passent si applicable
- [ ] `git pull origin adot` - récupérer derniers changements
- [ ] `git push origin adot` - pousser

---

## 🔍 Débogage Git

### Problèmes courants:
```bash
# "Detached HEAD" - revenir à une branche:
git checkout adot

# "Merge conflict" - résoudre manuellement puis:
git add .
git commit

# "Push rejected" - faire pull avant:
git pull origin adot
git push origin adot
```

### Vérifier l'intégrité:
```bash
git fsck                        # Vérifier integrity du repository
```

---

## 📱 Alias Utiles (Optionnel)

### Ajouter à votre ~/.gitconfig:
```bash
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
```

---

## 🎯 Bonnes Pratiques

### ✅ Faire:
- Commits fréquents et petits
- Messages de commit clairs
- Pull avant de push
- Utiliser des branches pour les features
- Tester avant de commit

### ❌ Éviter:
- Commits massifs
- Messages vagues
- Forcer push (git push --force)
- Commiter fichiers sensibles
- Ignorer git status

---

**💡 Astuce**: Gardez cette cheat sheet ouverte pendant vos sessions de développement !

---

*Document mis à jour pour le projet PF KHRA - Transport & Logistics*
