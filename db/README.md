# Documentation Base de Données

## 📁 Fichiers

- **`schema.sql`** - Structure des tables
- **`triggers.sql`** - Triggers et logique métier
- **`data.sql`** - Données de test (25 clients, 50 expéditions, etc.)
- **`init_db.bat`** - Script d'initialisation Windows
- **`init_db.sh`** - Script d'initialisation Linux/Mac

---

## 🚀 Initialisation

### Windows
```bash
init_db.bat
```

### Linux/Mac
```bash
chmod +x init_db.sh
./init_db.sh
```

Le script:
1. Supprime l'ancienne base (si elle existe)
2. Crée les tables (`schema.sql`)
3. Crée les triggers (`triggers.sql`)
4. Insère les données de test (`data.sql`)

---

## 🔍 Voir les Données

### Option 1: Interface Web
```bash
cd ..
sqlite_web db.sqlite3
# Ouvre http://127.0.0.1:8080
```

### Option 2: DB Browser for SQLite
Télécharger: https://sqlitebrowser.org/dl/

### Option 3: Ligne de commande
```bash
cd ..
sqlite3 db.sqlite3 "SELECT * FROM client LIMIT 5;"
```

---

## 📊 Tables Principales

| Table | Description | Nombre |
|-------|-------------|--------|
| `client` | Clients (particuliers/entreprises) | 25 |
| `chauffeur` | Chauffeurs avec permis | 15 |
| `vehicule` | Véhicules (camions, fourgons, motos) | 18 |
| `destination` | Destinations (Algérie + International) | 30+ |
| `expedition` | Expéditions | 50 |
| `type_service` | Types de service | 3 |
| `role` | Rôles utilisateurs | 6 |
| `utilisateur` | Utilisateurs | 5 |

---

## 🔧 Triggers Automatiques

- **Codes automatiques**: `CLI-00001`, `EXP-20260108-00001`, `FACT-202601-00001`
- **Timestamps**: Auto-update de `updated_at`
- **Tracking**: Création automatique du suivi d'expédition
- **Solde client**: Mise à jour automatique
- **Protections**: Empêche la modification des expéditions facturées

---

## 🧪 Requêtes de Test

```sql
-- Compter les clients
SELECT COUNT(*) FROM client;

-- Voir les expéditions par statut
SELECT statut, COUNT(*) FROM expedition GROUP BY statut;

-- Vérifier les codes auto-générés
SELECT code_expedition, date_creation FROM expedition LIMIT 5;

-- Voir le tracking
SELECT e.code_expedition, t.statut, t.date_statut 
FROM expedition e
JOIN tracking_expedition t ON e.id = t.expedition_id
LIMIT 5;
```

---

## ⚠️ Important

- **Ne jamais commit `db.sqlite3`** dans Git
- Chaque développeur crée sa propre base avec les scripts
- Après un pull avec changements SQL, re-run `init_db.bat`

---

## 🆘 Problèmes

**"sqlite3 not found"**
- Windows: https://www.sqlite.org/download.html
- Linux: `sudo apt install sqlite3`
- Mac: `brew install sqlite3`

**"Database locked"**
- Fermer DB Browser, sqlite-web, et le serveur Django

**Réinitialiser**
```bash
init_db.bat  # Répond "yes"
```
