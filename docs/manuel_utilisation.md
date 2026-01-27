# Manuel d’utilisation — projet si (Transport & Logistics Management)

Ce manuel décrit l’utilisation de l’application Web PF KHRA (gestion des expéditions, tournées, incidents, réclamations, facturation et paiements), selon les écrans disponibles dans l’interface.

> Accès (en environnement local) : Frontend `http://localhost:3000` — API `http://127.0.0.1:8000/api/`

---

## 1) Connexion et principes généraux

### 1.1 Connexion
1. Ouvrir l’application (`http://localhost:3000`).
2. Saisir **Nom d’utilisateur** et **Mot de passe**.
3. Cliquer **Se connecter**.

Comptes de test  : `admin`, `agent1`, `comptable1`, `logistique1` (mot de passe souvent `password123` en environnement démo).

### 1.2 Rôles et accès
L’application gère des rôles (exemples : **ADMIN**, **AGENT**, **COMPTABLE**, **LOGISTIQUE**, **DIRECTION**, **CHAUFFEUR**). Selon votre rôle, certains menus ou actions peuvent être visibles/masqués.

Recommandation d’usage :
- **ADMIN** : paramétrage + utilisateurs + audit.
- **AGENT** : opérations (clients, expéditions, tournées, incidents, réclamations) et selon paramétrage, la facturation.
suivi opérationnel.


### 1.3 Navigation
Le menu latéral donne accès aux modules :
- Tableau de bord
- Expéditions, Tournées, Incidents, Alertes, Réclamations, Clients
- Factures, Paiements
- Référentiels : Chauffeurs, Véhicules, Destinations
- Administration (ADMIN) : Utilisateurs, Journal d’audit

---

## 2) Tableau de bord

Le tableau de bord sert de point d’entrée :
- raccourcis vers **Nouvelle expédition** et **Nouvelle tournée**
- accès rapide aux référentiels (chauffeurs, véhicules, destinations)

---

## 3) Clients

### 3.1 Consulter la liste
Menu **Clients** :
- affiche le code client, identité, coordonnées, adresse, et **solde**.

> Interprétation solde : selon la configuration, un solde négatif peut représenter un crédit ou une dette. Référez-vous à vos règles internes.

### 3.2 Créer un client
1. Menu **Clients** → **+ Nouveau Client**
2. Renseigner type (particulier/entreprise), nom, prénom (optionnel), téléphone, email, adresse, ville, pays
3. **Créer le client**

### 3.3 Modifier un client
Selon l’interface, la modification peut se faire via un écran dédié (si un bouton “Modifier” est présent).

---

## 4) Expéditions (colis)

### 4.1 Créer une expédition
1. Menu **Expéditions** → **+ Nouvelle Expédition**
2. Renseigner :
   - **Client**
   - **Type de service**
   - **Destination**
   - **Poids / Volume**
   - Informations de livraison (destinataire, téléphone, adresse)
3. Choisir le **statut** initial (souvent “Enregistré”)
4. Cliquer **Créer l’expédition**

### 4.2 Comprendre les statuts d’expédition
Exemples de statuts utilisés :
- Enregistré
- Validé
- En transit
- En centre de tri
- En cours de livraison
- Livré
- Échec de livraison

Ces statuts servent au suivi opérationnel et peuvent être mis à jour manuellement ou automatiquement selon certaines actions (ex : clôture tournée / incident).

### 4.3 Modifier / supprimer une expédition
- **Modifier** : possible tant que l’expédition n’est pas verrouillée par la tournée (selon règles).
- **Supprimer** : généralement interdit si l’expédition est déjà liée à une tournée.

### 4.4 Signaler un incident depuis une expédition
Dans l’écran **Modifier l’expédition**, bouton **Signaler un incident** :
- ouvre le formulaire incident pré-rempli avec l’expédition concernée.

---

## 5) Tournées (planification & exécution)

### 5.1 Créer une tournée
1. Menu **Tournées** → **+ Nouvelle Tournée**
2. Renseigner :
   - Chauffeur
   - Véhicule
   - Date tournée
   - Points de passage (optionnel)
   - Statut (ex : “Préparée”, “En cours”, “Terminée”, “Annulée”)
3. Section **Expéditions à charger** :
   - sélectionner une ou plusieurs expéditions “Enregistré” disponibles
4. **Créer la tournée**

### 5.2 Terminer une tournée (clôture)
Lorsque vous passez une tournée à **Terminée** :
- l’application peut exiger les données de trajet (kilométrage départ/retour, consommation, etc.)
- les expéditions liées peuvent être automatiquement passées à **Livré** (selon implémentation)

### 5.3 Signaler un incident depuis une tournée
Dans l’écran **Modifier la tournée**, bouton **Signaler un incident** :
- ouvre le formulaire incident pré-rempli avec la tournée concernée.

---

## 6) Suivi (tracking) des expéditions

Le suivi s’appuie sur l’historique de statuts (tracking). Selon l’organisation, il peut être alimenté :
- manuellement (statuts et commentaires)
- automatiquement (ex : fin de tournée, incident)

Bonnes pratiques :
- saisir un commentaire clair à chaque changement majeur (retard, tentative de livraison, dépôt en agence…)
- garder des dates/lieux cohérents

---

## 7) Incidents

### 7.1 Créer un incident
1. Menu **Incidents** → **+ Signaler un incident** (ou via les boutons depuis expédition/tournée)
2. Choisir **Concerne** :
   - Expédition **ou** Tournée
3. Choisir le **type d’incident** (retard, perte, endommagement, problème technique, autre)
4. Ajouter un **commentaire**
5. (Optionnel) joindre des **documents / photos**
6. Choisir les **alertes** :
   - Direction (alerte interne)
   - Client (uniquement si incident lié à une expédition)
7. Valider : **Créer l’incident**

### 7.2 Effets automatiques (statuts)
Selon la configuration actuelle :
- incident lié à une **expédition** → statut expédition passe à **Échec de livraison** + trace de suivi
- incident lié à une **tournée** → statut tournée passe à **Annulée** et les expéditions non livrées peuvent passer à **Échec de livraison** + traces

### 7.3 Historique des incidents
Menu **Incidents** :
- liste des incidents (code, date, type, référence, action statut, nb pièces jointes)
- filtres possibles via liens contextuels (ex : incidents d’une expédition/tournée)

---

## 8) Alertes

### 8.1 Consulter les alertes
Menu **Alertes** :
- affiche le destinataire (Direction/Client), le titre, la date, et l’état **Lu / Non lu**.

### 8.2 Marquer une alerte comme lue
Sur une alerte “Non lue”, cliquer **Marquer lue**.

---

## 9) Réclamations clients (SAV)

Une réclamation est un ticket SAV pouvant être lié à :
- un ou plusieurs **colis / expéditions**
- une **facture**
- un **service** (type de service)

### 9.1 Créer une réclamation
1. Menu **Réclamations** → **+ Nouvelle réclamation**
2. Renseigner :
   - **Client** (obligatoire)
   - **Date**
   - **Statut** : En cours / Résolue / Annulée
   - Objet/Nature et description
3. Lier la réclamation à au moins un élément :
   - **Colis** : sélectionner 1..N expéditions (recherche par code + cases à cocher)
   - **Facture** (optionnel)
   - **Service** (optionnel)
4. Valider : **Créer la réclamation**

### 9.2 Modifier et suivre l’état
Dans l’écran **Modifier la réclamation** :
- mettre à jour statut et détails
- conserver l’historique (date de résolution si statut “Résolue”, selon paramétrage)

### 9.3 Consulter la liste
Menu **Réclamations** :
- liste avec client, objet, liens (colis/facture/service), statut

---

## 10) Factures

### 10.1 Créer une facture
1. Menu **Factures** → **+ Nouvelle Facture**
2. Sélectionner un **client**
3. Sélectionner une ou plusieurs expéditions **non facturées**
4. Vérifier les totaux (HT, TVA, TTC)
5. **Générer la facture**

La facture regroupe des expéditions et calcule les totaux.

### 10.2 Consulter le journal des factures
Menu **Factures** :
- filtre par client / statut
- accès au détail d’une facture

### 10.3 Détails et impression
Dans **Détails Facture** :
- liste des expéditions facturées
- totaux
- historique des paiements (si disponible)
- bouton **Imprimer / PDF**

### 10.4 Suppression d’une facture
La suppression peut :
- annuler/supprimer ses paiements
- mettre à jour le solde client

À utiliser avec prudence (préférez “Annulée” si votre organisation le permet).

---

## 11) Paiements

### 11.1 Enregistrer un paiement
1. Menu **Paiements** → **+ Enregistrer un Paiement**
2. Sélectionner le **client**
3. Sélectionner la **facture à régler** (ou paiement libre si autorisé)
4. Renseigner date, montant, mode
5. **Enregistrer le paiement**

L’enregistrement peut mettre à jour :
- le statut de la facture (payée / partiellement payée)
- le solde client

### 11.2 Consulter et supprimer un paiement
Menu **Paiements** :
- filtre par client
- suppression d’un paiement possible (impact sur solde client)

---

## 12) Référentiels (lecture)

### 12.1 Chauffeurs / Véhicules / Destinations
Ces écrans sont en lecture (dans l’UI actuelle) :
- affichage + recherche + impression

---

## 13) Administration (ADMIN)

### 13.1 Gestion des utilisateurs
Menu **Administration → Utilisateurs** :
- créer un utilisateur (username, identité, email, rôle, mot de passe)
- activer/désactiver un compte
- modifier un utilisateur
- réinitialiser un mot de passe (si bouton disponible)

### 13.2 Journal d’audit
Menu **Administration → Journal d’audit** :
- filtre par utilisateur et type d’action
- traçabilité : connexions, créations, modifications, désactivations, etc.

---

## 14) Dépannage (FAQ courte)

### 14.1 Je ne peux pas supprimer une expédition
Cause fréquente : l’expédition est liée à une tournée. Détacher l’expédition de la tournée (si autorisé) ou annuler la tournée selon procédure.

### 14.2 Les libellés s’affichent avec des caractères bizarres (ex: “ExpÃ©ditions”)
Cause : encodage (UTF-8) sur certains fichiers/terminaux. Côté utilisateur, rafraîchir la page. Côté déploiement, vérifier l’encodage des sources et de la base.

### 14.3 Je ne vois pas “Administration”
Vous n’avez probablement pas le rôle **ADMIN**.

