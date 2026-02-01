# PF KHRA - Système de Gestion Transport & Logistique

Application web complète de gestion de transport et de logistique pour une entreprise de livraison.

## Fonctionnalités Principales

### 🚚 **Gestion des Expéditions**
- Création et suivi des colis
- Gestion des statuts (enregistré, en transit, livré, échec)
- Suivi en temps réel avec historique de tracking
- Calcul automatique des tarifs selon poids, volume et destination

### 📋 **Gestion des Tournées**
- Planification des itinéraires
- Assignation des chauffeurs et véhicules
- Suivi de la performance (kilométrage, consommation, temps)
- Optimisation des livraisons

### 👥 **Gestion Clients**
- Portefeuille clients (particuliers et entreprises)
- Historique des expéditions par client
- Solde et facturation
- Système de favoris

### 🚛 **Gestion Flotte**
- Parc véhicules (camions, fourgons, camionnettes, motos)
- Suivi de l'état et disponibilité
- Consommation et entretien

### 💰 **Gestion Comptable**
- Facturation automatique
- Suivi des paiements
- Gestion TVA
- Statistiques financières

### 📊 **Tableau de Bord Analytics**
- KPI de performance
- Statistiques par période
- Analyse des coûts et revenus
- Taux de satisfaction

### 🚨 **Gestion Incidents**
- Signalement d'incidents
- Système de réclamations
- Notifications automatiques
- Suivi des résolutions

## Technologies

### Backend
- **Python 3.10+**
- **Django 4.2+** (Framework web)
- **Django REST Framework** (API REST)
- **SQLite** (Base de données - production: PostgreSQL recommandé)

### Frontend
- **React 18** (Interface utilisateur)
- **Vite** (Build tool)
- **Tailwind CSS** (Styling)
- **React Router** (Navigation)
- **React Query** (Gestion d'état)

### Architecture
- **API RESTful** backend
- **SPA** frontend
- **Authentification JWT**
- **Système de rôles** (Admin, Agent, Comptable, Logistique, Direction)

## Installation

### Prérequis
- Python 3.10+
- Node.js 16+ et npm
- Git

### 1. Clonage du projet
```bash
git clone <repository-url>
cd PF-KHRA
```

### 2. Configuration Backend

#### Création de l'environnement virtuel
```bash
cd backend
python -m venv venv
```

#### Activation de l'environnement
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

#### Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration Frontend

```bash
cd frontend
npm install
```

### 4. Initialisation de la Base de Données

#### Option 1: Initialisation Simple (Données de base uniquement)
```bash
cd backend
python ../scripts/init_db.py
python manage.py migrate
```

#### Option 2: Initialisation avec Données de Démo (Recommandé)
```bash
cd backend
python ../scripts/init_db.py --reset --seed
python manage.py migrate
```

Cette option charge:
- **schema.sql** - Structure de la base de données
- **data.sql** - Données de base (rôles, utilisateurs, destinations)
- **complete_seed_2024_2026.sql** - Données de démonstration réalistes 2024-2026

### 5. Lancement de l'Application

#### Lancement complet (Backend + Frontend)
```bash
# Depuis la racine du projet
npm run dev
```

#### Lancement séparé

**Backend (API):**
```bash
cd backend
python manage.py runserver
```

**Frontend (Interface):**
```bash
cd frontend
npm run dev
```

## Accès à l'Application

Une fois lancée, l'application est accessible via:

- **Frontend:** http://localhost:3000
- **Backend API:** http://127.0.0.1:8000
- **Django Admin:** http://127.0.0.1:8000/admin/

### Comptes de Test

#### Administrateur
- **Utilisateur:** `admin`
- **Mot de passe:** `password123`

#### Agents
- **Utilisateur:** `agent1` / `agent2`
- **Mot de passe:** `password123`

#### Comptable
- **Utilisateur:** `comptable1`
- **Mot de passe:** `password123`

#### Logistique
- **Utilisateur:** `logistique1`
- **Mot de passe:** `password123`

## Structure du Projet

```
PF-KHRA/
├── backend/                 # Backend Django
│   ├── manage.py           # Script de gestion Django
│   ├── requirements.txt    # Dépendances Python
│   ├── mon_projet/         # Configuration Django
│   ├── core/              # Application principale
│   │   ├── models.py      # Modèles Django
│   │   ├── views.py       # Vues API
│   │   ├── serializers.py # Serializers DRF
│   │   └── migrations/    # Migrations Django
│   └── scripts/           # Scripts utilitaires
│       └── init_db.py     # Initialisation base de données
├── frontend/              # Frontend React
│   ├── package.json       # Dépendances npm
│   ├── vite.config.js     # Configuration Vite
│   ├── src/
│   │   ├── main.jsx       # Point d'entrée
│   │   ├── App.jsx        # Composant principal
│   │   ├── api.js         # Configuration API
│   │   ├── components/    # Composants React
│   │   └── pages/         # Pages de l'application
├── db/                    # Scripts SQL
│   ├── schema.sql         # Structure de la base
│   ├── data.sql          # Données de base
│   └── complete_seed_2024_2026.sql  # Données de démonstration
├── scripts/              # Scripts utilitaires
└── docs/                 # Documentation
```

## Workflow de Développement

### 1. Initialisation (Recommandé)
```bash
# Lancer le script d'initialisation avec données de démo
python backend/scripts/init_db.py --reset --seed

# Appliquer les migrations Django
cd backend && python manage.py migrate
```

### 2. Lancement en Développement
```bash
# Lancer les deux serveurs (backend + frontend)
npm run dev
```

### 3. Lancement en Production
```bash
# Build frontend
cd frontend && npm run build

# Lancer backend en production
cd backend && python manage.py runserver --settings=mon_projet.settings.production
```

## Documentation

- **[Guide d'Utilisation](docs/manuel_utilisation.md)** - Manuel complet pour les utilisateurs
- **[API Documentation](docs/api.md)** - Documentation technique de l'API
- **[Architecture](docs/architecture.md)** - Détails techniques et architecture

## Déploiement

### Environnement de Production

1. **Base de Données:** Remplacer SQLite par PostgreSQL
2. **Serveur Web:** Utiliser Gunicorn + Nginx
3. **Static Files:** Configurer le serveur pour les fichiers statiques
4. **Sécurité:** Configurer les clés secrètes et HTTPS

### Variables d'Environnement

```bash
# Backend
DJANGO_SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
DEBUG=False

# Frontend
VITE_API_URL=http://your-domain.com/api
```

## Support

Pour toute question ou problème:

1. Consultez la documentation dans `/docs/`
2. Vérifiez les logs backend: `cd backend && python manage.py runserver`
3. Vérifiez la console frontend dans les outils de développement du navigateur
4. Contactez l'équipe de développement

## License

Projet académique - Licence MIT

---

**Projet réalisé par:** Adem, L3 ISIL A 2025-2026