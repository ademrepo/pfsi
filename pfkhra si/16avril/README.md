# 🚀 PROJET PF KHRA - Transport & Logistics

Système de gestion de transport et livraison avec Django et SQLite.

---

## � Table des matières
1. [Installation Complète](#installation-complète)
2. [Configuration du Virtual Environment](#configuration-du-virtual-environment)
3. [Initialisation de la Base de Données](#initialisation-de-la-base-de-données)
4. [Lancer le Serveur Django](#lancer-le-serveur-django)
5. [Consulter la Base de Données](#consulter-la-base-de-données)
6. [Structure du Projet](#structure-du-projet)
7. [Base de Données](#base-de-données)
8. [Commandes Git](#commandes-git)
9. [Fichiers à Ignorer](#fichiers-à-ignorer)
10. [Problèmes Courants](#problèmes-courants)

---

## 🔧 Installation Complète

### 1. Cloner le projet
```bash
git clone https://github.com/caameliaz/16avril.git
cd 16avril
```

### 2. Configuration du Virtual Environment

#### ⚠️ Pourquoi un Virtual Environment ?
Un environnement virtuel isolé les dépendances Python du projet de votre système. C'est **OBLIGATOIRE** pour éviter les conflits de versions.

#### Windows
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
venv\Scripts\activate
```

#### Linux / macOS
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate
```

**Vérifier l'activation**: Vous devriez voir `(venv)` au début de votre terminal.

### 3. Installer les dépendances Python

Assurez-vous que le virtual environment est **activé** (voir étape 2), puis :

```bash
pip install -r requirements.txt
```

**Dépendances instalées**:
- Django 4.2.9
- SQLite3 (déjà inclus)
- Autres dépendances (voir `requirements.txt`)

### 4. Initialisation de la base de données (OBLIGATOIRE après un clone / pull)

Le fichier `db.sqlite3` est **ignoré par Git** (voir `.gitignore`). Donc après un clone/pull, vous n'aurez pas la base locale (tables + données de test), ce qui fait que l'API retournera du vide / erreurs.

Initialisez la base via le script :

```bash
python scripts/init_db.py
```

Pour repartir de zéro :

```bash
python scripts/init_db.py --reset
```

Windows (optionnel): script tout-en-un

```powershell
.\scripts\dev_setup_windows.ps1
```

### 4. Initialiser la Base de Données

```bash
cd db
init_db.bat          # Windows
# ou
init_db.sh           # Linux/Mac
```

Le script:
1. Supprime l'ancienne base (si elle existe)
2. Crée les tables (`schema.sql`)
3. Crée les triggers (`triggers.sql`)
4. Insère les données de test (`data.sql`)

### 5. Lancer le serveur Django

Revenir au dossier principal :

```bash
cd ..

# Assurez-vous que le venv est toujours activé
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

python manage.py runserver
```

**Le serveur est actif sur**: http://127.0.0.1:8000

---

## 📌 Utilisation Quotidienne

### Avant chaque session de développement :

```bash
# 1. Naviguer au dossier du projet
cd 16avril

# 2. Activer le virtual environment
venv\Scripts\activate          # Windows
# source venv/bin/activate    # Linux/Mac

# 3. (Optional) Mettre à jour les dépendances
pip install -r requirements.txt

# 4. S'assurer que la DB locale existe (idempotent)
python scripts/init_db.py

# 5. Lancer le serveur Django
python manage.py runserver
```

### Après votre session :

```bash
# Arrêter le serveur: Ctrl + C
# Désactiver l'environnement virtuel (optionnel)
deactivate
```

---

## 🗄️ Consulter la Base de Données

### Option 1: Interface Web (Recommandé)
```bash
# Assurez-vous que vous êtes dans le dossier principal
sqlite_web db.sqlite3
# Ouvre http://127.0.0.1:8080
```

### Option 2: Application Desktop
Télécharger **DB Browser for SQLite**: https://sqlitebrowser.org/dl/

### Option 3: Ligne de commande
```bash
sqlite3 db.sqlite3 "SELECT * FROM client LIMIT 5;"
```

---



## 🔗 Commandes Git

### Configuration initiale (une seule fois)

```bash
# Configurer votre nom et email
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

### Workflow quotidien

```bash
# 1. Avant de commencer: récupérer les derniers changements
git pull origin main

# 2. Créer une branche pour votre feature (optionnel mais recommandé)
git checkout -b feature/ma-feature

# 3. Faire vos modifications dans le code

# 4. Vérifier vos changements
git status

# 5. Ajouter les fichiers modifiés au staging
git add .
# ou pour des fichiers spécifiques:
git add core/views.py mon_projet/settings.py

# 6. Créer un commit avec un message clair
git commit -m "Ajout de la fonctionnalité X"
# Exemples de bons messages:
# - "Ajouter validation des numéros de téléphone"
# - "Corriger bug d'affichage des expéditions"
# - "Refactoriser models.py pour meilleure lisibilité"

# 7. Envoyer vos changements au serveur
git push origin main
# ou si vous êtes sur une branche feature:
git push origin feature/ma-feature

# 8. (Optionnel) Créer une Pull Request sur GitHub pour revue
```

### Commandes utiles

```bash
# Voir l'historique des commits
git log --oneline

# Voir les différences non committées
git diff

# Annuler les changements d'un fichier
git checkout -- nom_du_fichier.py

# Voir l'état actuel
git status
```

---

## 🚫 Fichiers à Ignorer

### Le `.gitignore` doit contenir:

```
# Virtual Environment
venv/
env/
ENV/

# Base de données
db.sqlite3
*.sqlite
*.db

# Cache Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# IDE et éditeurs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Fichiers systèmes
Thumbs.db

# Fichiers de logs
*.log

# Fichiers secrets (variables d'environnement, clés API)
.env
.env.local
secrets.py
```

### ✅ À TOUJOURS COMMIT:
- `schema.sql`, `triggers.sql`, `data.sql` (changements base de données)
- `*.py` (code Python)
- `requirements.txt` (dépendances)
- `README.md`
- `.gitignore`

### ❌ NE JAMAIS COMMIT:
- **`db.sqlite3`** (déjà dans `.gitignore`)
- `venv/` (déjà dans `.gitignore`)
- Fichiers sensibles (clés API, mots de passe)

---

## 📝 Workflow Collaboratif

### Quand quelqu'un change les fichiers SQL:

```bash
# 1. Pull les changements
git pull origin main

# 2. Réinitialiser la base de données
cd db
init_db.bat    # Windows
# init_db.sh   # Linux/Mac

# 3. Vous avez les données mises à jour
cd ..
python manage.py runserver
```

---

## 🆘 Problèmes Courants

### "Module not found" ou "No module named X"
```bash
# Assurez-vous que le venv est activé (vous devez voir (venv) dans le terminal)
venv\Scripts\activate          # Windows
# source venv/bin/activate    # Linux/Mac

# Réinstallez les dépendances
pip install -r requirements.txt
```

### "sqlite3 not found"
```bash
# Windows: Télécharger depuis https://www.sqlite.org/download.html
# Linux: sudo apt install sqlite3
# Mac: brew install sqlite3
```

### "Database locked"
- Fermer tous les programmes qui accèdent à la base de données
- Fermer DB Browser, sqlite-web, et le serveur Django
- Attendre quelques secondes avant de relancer

### "Port 8000 already in use"
```bash
# Le serveur Django est peut-être déjà en cours d'exécution
# Arrêter le serveur existant avec Ctrl+C
# ou démarrer sur un autre port:
python manage.py runserver 8001
```

### Réinitialiser complètement la base de données
```bash
cd db
init_db.bat    # Répond "yes" pour supprimer l'ancienne
# init_db.sh   # Linux/Mac
cd ..
```

### Le venv n'existe pas
```bash
# Recréer l'environnement virtuel
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate    # Linux/Mac
pip install -r requirements.txt
```

---

## 📚 Documentation Supplémentaire

- **Base de données détaillée**: Voir `db/README.md` pour les requêtes de test
- **API Django**: (À compléter)
- **Frontend**: (À compléter)

---

## 👥 Équipe

(Ajouter les membres de l'équipe ici)

---

## ✅ Checklist pour Démarrer

- [ ] Clone le projet: `git clone ...`
- [ ] Crée le venv: `python -m venv venv`
- [ ] Active le venv: `venv\Scripts\activate` (Windows)
- [ ] Installe les dépendances: `pip install -r requirements.txt`
- [ ] Lance le script DB: `cd db && init_db.bat`
- [ ] Lance Django: `python manage.py runserver`
- [ ] Accède à http://127.0.0.1:8000
- [ ] Consulte la DB: `sqlite_web db.sqlite3` (dans une autre console avec venv activé)

---

**Bon développement! 🚀**
