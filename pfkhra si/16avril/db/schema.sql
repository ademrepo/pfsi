PRAGMA foreign_keys = ON;

-- ===========================
-- AUTHENTIFICATION
-- ===========================
CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    libelle TEXT NOT NULL
);

CREATE TABLE utilisateur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    telephone TEXT,
    role_id INTEGER NOT NULL,
    is_active INTEGER DEFAULT 1 CHECK (is_active IN (0,1)),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

-- ===========================
-- FAVORIS
-- ===========================
CREATE TABLE favori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    titre TEXT NOT NULL,
    url_ou_route TEXT NOT NULL,
    icone TEXT,
    ordre INTEGER,
    is_active INTEGER DEFAULT 1 CHECK (is_active IN (0,1)),
    updated_at DATETIME,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
);

-- ===========================
-- CLIENT
-- ===========================
CREATE TABLE client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_client TEXT UNIQUE,
    type_client TEXT CHECK (type_client IN ('particulier','entreprise')),
    nom TEXT NOT NULL,
    prenom TEXT,
    telephone TEXT,
    email TEXT,
    adresse TEXT,
    ville TEXT,
    pays TEXT,
    solde REAL DEFAULT 0,
    statut TEXT DEFAULT 'actif',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

-- ===========================
-- CHAUFFEUR
-- ===========================
CREATE TABLE chauffeur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricule TEXT UNIQUE,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    telephone TEXT,
    email TEXT,
    adresse TEXT,
    num_permis TEXT UNIQUE NOT NULL,
    categorie_permis TEXT,
    date_embauche DATE,
    disponibilite TEXT,
    statut TEXT,
    updated_at DATETIME
);

-- ===========================
-- VEHICULE
-- ===========================
CREATE TABLE vehicule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    immatriculation TEXT UNIQUE NOT NULL,
    type_vehicule TEXT,
    marque TEXT,
    modele TEXT,
    capacite_kg REAL NOT NULL,
    capacite_m3 REAL NOT NULL,
    consommation_100km REAL,
    etat TEXT,
    disponibilite TEXT,
    date_mise_en_service DATE,
    updated_at DATETIME
);

-- ===========================
-- DESTINATION / SERVICE / TARIFICATION
-- ===========================
CREATE TABLE destination (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pays TEXT,
    ville TEXT,
    zone_geographique TEXT,
    code_zone TEXT,
    tarif_base_defaut REAL NOT NULL,
    is_active INTEGER DEFAULT 1,
    updated_at DATETIME
);

CREATE TABLE type_service (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    libelle TEXT,
    description TEXT,
    delai_estime_jours INTEGER,
    priorite INTEGER,
    is_active INTEGER DEFAULT 1,
    updated_at DATETIME
);

CREATE TABLE tarification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_service_id INTEGER,
    destination_id INTEGER,
    tarif_base REAL DEFAULT 0,
    tarif_poids_kg REAL,
    tarif_volume_m3 REAL,
    date_debut DATE,
    date_fin DATE,
    updated_at DATETIME,
    UNIQUE (type_service_id, destination_id, date_debut),
    FOREIGN KEY (type_service_id) REFERENCES type_service(id),
    FOREIGN KEY (destination_id) REFERENCES destination(id)
);

-- ===========================
-- TOURNEE (DOIT ÊTRE AVANT TRACKING)
-- ===========================
CREATE TABLE tournee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_tournee TEXT UNIQUE,
    date_tournee DATE,
    date_depart DATETIME,
    date_retour DATETIME,
    chauffeur_id INTEGER,
    vehicule_id INTEGER,
    statut TEXT,
    kilometrage_depart REAL,
    kilometrage_retour REAL,
    distance_km REAL,
    duree_minutes INTEGER,
    consommation_litres REAL,
    notes TEXT,
    points_passage TEXT,
    created_by INTEGER,
    updated_at DATETIME,
    FOREIGN KEY (chauffeur_id) REFERENCES chauffeur(id),
    FOREIGN KEY (vehicule_id) REFERENCES vehicule(id)
);

-- ===========================
-- EXPEDITION
-- ===========================
CREATE TABLE expedition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_expedition TEXT UNIQUE,
    client_id INTEGER,
    type_service_id INTEGER,
    destination_id INTEGER,
    poids_kg REAL NOT NULL,
    volume_m3 REAL NOT NULL,
    description_colis TEXT,
    adresse_livraison TEXT,
    nom_destinataire TEXT,
    telephone_destinataire TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    statut TEXT,
    montant_total REAL DEFAULT 0,
    est_facturee INTEGER DEFAULT 0,
    tournee_id INTEGER,
    created_by INTEGER,
    updated_at DATETIME,
    FOREIGN KEY (client_id) REFERENCES client(id),
    FOREIGN KEY (type_service_id) REFERENCES type_service(id),
    FOREIGN KEY (destination_id) REFERENCES destination(id),
    FOREIGN KEY (tournee_id) REFERENCES tournee(id)
);

CREATE TABLE tracking_expedition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expedition_id INTEGER,
    chauffeur_id INTEGER,
    tournee_id INTEGER,
    statut TEXT,
    lieu TEXT,
    commentaire TEXT,
    date_statut DATETIME,
    FOREIGN KEY (expedition_id) REFERENCES expedition(id),
    FOREIGN KEY (chauffeur_id) REFERENCES chauffeur(id),
    FOREIGN KEY (tournee_id) REFERENCES tournee(id)
);

-- ===========================
-- FACTURATION
-- ===========================
CREATE TABLE facture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_facture TEXT UNIQUE,
    client_id INTEGER,
    date_facture DATE,
    total_ht REAL,
    montant_tva REAL,
    total_ttc REAL,
    statut TEXT,
    updated_at DATETIME,
    FOREIGN KEY (client_id) REFERENCES client(id)
);

CREATE TABLE facture_expedition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture_id INTEGER,
    expedition_id INTEGER,
    UNIQUE (facture_id, expedition_id),
    FOREIGN KEY (facture_id) REFERENCES facture(id),
    FOREIGN KEY (expedition_id) REFERENCES expedition(id)
);

CREATE TABLE paiement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facture_id INTEGER,
    client_id INTEGER,
    date_paiement DATE,
    mode_paiement TEXT,
    montant REAL,
    statut TEXT,
    updated_at DATETIME,
    FOREIGN KEY (facture_id) REFERENCES facture(id),
    FOREIGN KEY (client_id) REFERENCES client(id)
);

-- ===========================
-- INCIDENT / RECLAMATION
-- ===========================
CREATE TABLE incident (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expedition_id INTEGER,
    tournee_id INTEGER,
    type_incident TEXT,
    gravite TEXT,
    description TEXT,
    statut TEXT,
    date_declaration DATE,
    date_cloture DATE,
    declare_par INTEGER,
    piece_jointe TEXT,
    CHECK (expedition_id IS NOT NULL OR tournee_id IS NOT NULL)
);

CREATE TABLE reclamation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    objet TEXT,
    description TEXT,
    date_reclamation DATE,
    statut TEXT,
    expedition_id INTEGER,
    facture_id INTEGER,
    traite_par INTEGER,
    date_resolution DATE
);
