# PF KHRA - Système de Gestion Transport & Logistique

Application web complète de gestion de transport et de logistique pour une entreprise de livraison.

## Fonctionnalités Principales

*   **Gestion des Expéditions**: Suivi complet des colis, statuts (enregistré, en transit, livré), et calcul automatique des tarifs.
*   **Gestion des Tournées**: Planification optimale des itinéraires et assignation des chauffeurs/véhicules.
*   **Gestion Clients**: Portefeuille clients, historique des envois et facturation.
*   **Gestion Flotte**: Suivi du parc de véhicules, maintenance et consommation.
*   **Comptabilité**: Facturation automatique, suivi des paiements et statistiques financières.
*   **Tableau de Bord**: KPIs de performance, analyses de coûts et revenus en temps réel.

## Technologies

*   **Backend**: Python (Django, Django REST Framework), SQLite (Base de données).
*   **Frontend**: React 18, Vite, Tailwind CSS, Leaflet (Cartes), Recharts (Graphiques).

## Installation et Lancement

1.  **Prérequis**: Python 3.10+, Node.js 16+.
2.  **Installation**:
    *   Backend:
        ```bash
        cd backend
        python -m venv venv
        # Windows: venv\Scripts\activate | Linux/Mac: source venv/bin/activate
        pip install -r requirements.txt
        python ../scripts/init_db.py --reset --seed
        python manage.py migrate
        ```
    *   Frontend:
        ```bash
        cd frontend
        npm install
        ```
3.  **Lancement**:
    ```bash
    # Racine du projet (lance backend + frontend)
    ./start_app.bat
    ```
    Ou séparément:
    *   Backend: `cd backend && python manage.py runserver`
    *   Frontend: `cd frontend && npm run dev`

## Accès Rapide

*   **Frontend**: http://localhost:3000
*   **Backend API**: http://127.0.0.1:8000
*   **Admin**: http://127.0.0.1:8000/admin/

**Identifiants de Test**:
*   **Admin**: `admin` / `password123`
*   **Agent**: `agent1` / `password123`
*   **Comptable**: `comptable1` / `password123`