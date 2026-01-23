# Architecture des dossiers & structure BDD (référence agents)

Objectif : aider les agents à comprendre *où* coder (dossiers) et *quoi* manipuler (schéma de données), sans remplacer le README existant.

## Vue d'ensemble des dossiers (dans `pfkhra si/`)

### `16avril/` (monolithe Django historique - référence métier principale)
Ce dossier contient **la logique métier complète** (models/serializers/views/permissions/utils/middleware) et la **référence SQL** de la base.

- `16avril/core/` : cœur métier (transport & logistique)
  - `models.py` : modèles métiers (clients, expéditions, tournées, factures, paiements, etc.)
  - `serializers.py` : règles métier côté API (validation, calculs, agrégations)
  - `views.py` : endpoints (CRUD + actions), filtrage, permissions appliquées
  - `permissions.py`, `middleware.py`, `utils.py` : contrôle d'accès, audit/traçabilité, helpers
  - `management/` : commandes Django custom (scripts internes)
  - `migrations/` : migrations Django (si utilisées)
- `16avril/mon_projet/` : configuration Django du monolithe (settings, urls, wsgi/asgi)
- `16avril/db/` : **référence BDD** (à lire avant de toucher aux données)
  - `schema.sql` : tables + contraintes + clés étrangères (source de vérité du schéma)
  - `triggers.sql` : automatisations (codes, timestamps, protections, etc.)
  - `data.sql` : données de démo / tests
  - `init_db.bat` / `init_db.sh` : reconstruction complète de `db.sqlite3`
  - `README.md` : explications d'usage et requêtes utiles
- `16avril/db.sqlite3` : base SQLite locale (souvent utilisée pour démo/tests)
- `16avril/reproduce_issue.py`, `16avril/test_default.py`, `16avril/*.txt` : scripts & logs (diagnostic/migrations/triggers)

Quand un agent doit “comprendre le métier”, c'est **en priorité** dans `16avril/core/` et `16avril/db/`.

### `backend/` (API Django/DRF - couche plus récente / orientée auth + endpoints)
Dossier orienté **API** (Django + DRF) avec une structure plus compacte.

- `backend/authentication/` : authentification, rôles, permissions, audit
  - `models.py` : `CustomUser` (rôle via choix), `AuditLog` (journal)
  - `middleware.py` : audit logging (actions sensibles)
  - `permissions.py` : règles d'accès (RBAC)
  - `serializers.py`, `views.py`, `urls.py` : endpoints d'auth + admin utilisateurs
  - `migrations/` : migrations de l'app authentication
- `backend/transport_management/` : projet Django (settings DRF/CORS/sessions, urls, wsgi/asgi)
- `backend/core/` : contient actuellement surtout `serializers.py` (règles métier API)
- `backend/db.sqlite3` : base SQLite locale du backend (dev)

Important : il existe des différences possibles entre la modélisation “monolithe” (`16avril/db/schema.sql` : tables `utilisateur`, `role`, etc.) et le modèle Django custom du backend (`CustomUser` avec rôle en `CharField`). **Avant d'ajouter/modifier une entité**, vérifier quel “monde” est utilisé par l'environnement ciblé (monolithe vs backend).

### `frontend/` (React + Vite)
Interface utilisateur (Admin/Agent) consommant l'API.

- `frontend/src/api.js` : point central Axios (baseURL, headers, interceptors)
- `frontend/src/components/` : composants partagés (`Layout`, `Sidebar`)
- `frontend/src/pages/Admin/` : écrans admin (audit logs, gestion utilisateurs)
- `frontend/src/pages/Agent/` : écrans opérationnels (clients, expéditions, tournées, factures, paiements)
- `frontend/src/App.jsx` / `frontend/src/main.jsx` : routage + bootstrap
- `frontend/vite.config.js`, `frontend/package.json` : config build + dépendances

## Structure de la base de données (SQLite) - référence `16avril/db/schema.sql`

La base est SQLite, avec `PRAGMA foreign_keys = ON;` dans le schéma.

### A. Authentification / utilisateurs
- `role(id, code UNIQUE, libelle)`
- `utilisateur(...)`
  - champs clés : `username UNIQUE`, `email UNIQUE`, `password`, `nom`, `prenom`, `telephone`, `role_id`, `is_active`, `created_at`, `updated_at`
  - relation : `utilisateur.role_id -> role.id`
- `favori(...)`
  - relation : `favori.utilisateur_id -> utilisateur.id`

### B. Référentiels (clients, ressources, destinations)
- `client(...)`
  - champs clés : `code_client UNIQUE`, `type_client` (particulier/entreprise), coordonnées, `solde`, `statut`, timestamps
- `chauffeur(...)`
  - champs clés : `matricule UNIQUE`, `num_permis UNIQUE`, coordonnées, disponibilité/statut
- `vehicule(...)`
  - champs clés : `immatriculation UNIQUE`, capacités kg/m3, état/disponibilité
- `destination(...)`
  - champs clés : zone géographique, `tarif_base_defaut`, `is_active`
- `type_service(...)`
  - champs clés : `code UNIQUE`, libellé, délai/priorité, `is_active`
- `tarification(...)`
  - relations : `tarification.type_service_id -> type_service.id`, `tarification.destination_id -> destination.id`
  - unicité : `UNIQUE(type_service_id, destination_id, date_debut)`
  - objectif : gérer une grille tarifaire “par période” + calcul (base + poids + volume)

### C. Exploitation (tournées, expéditions, tracking)
- `tournee(...)`
  - relations : `tournee.chauffeur_id -> chauffeur.id`, `tournee.vehicule_id -> vehicule.id`
  - champs clés : `code_tournee UNIQUE`, dates, métriques (km/durée/consommation), `created_by` (référence applicative)
  - note : `created_by` est un entier (pas de FK définie dans `schema.sql`)
- `expedition(...)`
  - relations : `expedition.client_id -> client.id`, `expedition.type_service_id -> type_service.id`, `expedition.destination_id -> destination.id`
  - champs clés : `code_expedition UNIQUE`, poids/volume, adresse livraison, statut, `montant_total`, `est_facturee`, `created_by` (référence applicative)
- `tracking_expedition(...)`
  - relations : `tracking_expedition.expedition_id -> expedition.id`,
    `tracking_expedition.chauffeur_id -> chauffeur.id`,
    `tracking_expedition.tournee_id -> tournee.id`
  - objectif : historiser l'avancement (statut/lieu/commentaire/date)

### D. Facturation & paiements
- `facture(...)`
  - relation : `facture.client_id -> client.id`
  - champs clés : `numero_facture UNIQUE`, totaux HT/TVA/TTC, statut
- `facture_expedition(...)`
  - relations : `facture_expedition.facture_id -> facture.id`, `facture_expedition.expedition_id -> expedition.id`
  - unicité : `UNIQUE(facture_id, expedition_id)`
- `paiement(...)`
  - relations : `paiement.facture_id -> facture.id`, `paiement.client_id -> client.id`
  - objectif : tracer les règlements et impacter le solde client côté logique métier (voir triggers/serializers)

### E. Incidents & réclamations
- `incident(...)`
  - règle : `CHECK (expedition_id IS NOT NULL OR tournee_id IS NOT NULL)` (au moins une référence)
  - (NB : pas de FK explicite définie dans `schema.sql` pour incident/reclamation, c'est une décision à valider si on renforce l'intégrité)
- `reclamation(...)`
  - référence `client_id`, et optionnellement `expedition_id`, `facture_id`, `traite_par`

## Ce qui est “automatique” (référence `16avril/db/triggers.sql`)
Selon la version des triggers présents, on trouve généralement :
- génération de codes (clients/expéditions/factures)
- mise à jour de `updated_at`
- protections : empêcher la modification d'éléments déjà facturés / verrouillés
- effets “comptables” : mise à jour du solde client, création/complétion d'historique de tracking

Avant de modifier une règle métier “automatique”, vérifier si elle est gérée :
- côté SQL (triggers), ou
- côté Django/DRF (serializers/views), ou
- dans les deux (risque de double-effet).

