-- ============================================
-- DATA.SQL - Données de test
-- Système de Gestion Transport & Livraison
-- ============================================

-- ============================================
-- 1. ROLES
-- ============================================

INSERT INTO role (code, libelle) VALUES
('ADMIN', 'Administrateur'),
('AGENT', 'Agent de transport'),
('COMPTABLE', 'Comptable'),
('LOGISTIQUE', 'Responsable logistique'),
('DIRECTION', 'Direction'),
('CHAUFFEUR', 'Chauffeur');

-- ============================================
-- 2. UTILISATEURS
-- ============================================

-- Mot de passe: password123 (à hasher en production)
INSERT INTO utilisateur (username, email, password, nom, prenom, telephone, role_id, is_active) VALUES
('admin', 'admin@transport.dz', 'password123', 'Benali', 'Ahmed', '0555123456', 1, 1),
('agent1', 'agent1@transport.dz', 'password123', 'Kaci', 'Fatima', '0666234567', 2, 1),
('agent2', 'agent2@transport.dz', 'password123', 'Meziane', 'Karim', '0777345678', 2, 1),
('agent3', 'ademglps@gmail.com', 'password123', 'Adem', 'Hadjammar', '0777345478', 2, 1),
('comptable1', 'compta@transport.dz', 'password123', 'Saidi', 'Meriem', '0555456789', 3, 1),
('logistique1', 'logi@transport.dz', 'password123', 'Hamdi', 'Yacine', '0666567890', 4, 1);

-- ============================================
-- 3. DESTINATIONS (30+)
-- ============================================

INSERT INTO destination (pays, ville, zone_geographique, tarif_base_defaut, is_active) VALUES
-- Algérie - Zone A (grandes villes)
('Algérie', 'Alger', 'Zone_A', 500.00, 1),
('Algérie', 'Oran', 'Zone_A', 500.00, 1),
('Algérie', 'Constantine', 'Zone_A', 500.00, 1),
('Algérie', 'Annaba', 'Zone_A', 500.00, 1),
('Algérie', 'Blida', 'Zone_A', 500.00, 1),
('Algérie', 'Batna', 'Zone_A', 500.00, 1),
('Algérie', 'Sétif', 'Zone_A', 500.00, 1),
('Algérie', 'Tlemcen', 'Zone_A', 500.00, 1),

-- Algérie - Zone B (villes moyennes)
('Algérie', 'Béjaïa', 'Zone_B', 800.00, 1),
('Algérie', 'Tizi Ouzou', 'Zone_B', 800.00, 1),
('Algérie', 'Biskra', 'Zone_B', 800.00, 1),
('Algérie', 'Chlef', 'Zone_B', 800.00, 1),
('Algérie', 'Skikda', 'Zone_B', 800.00, 1),
('Algérie', 'Mostaganem', 'Zone_B', 800.00, 1),
('Algérie', 'El Oued', 'Zone_B', 800.00, 1),
('Algérie', 'Béchar', 'Zone_B', 800.00, 1),

-- Algérie - Zone C (sud)
('Algérie', 'Tamanrasset', 'Zone_C', 1500.00, 1),
('Algérie', 'Ouargla', 'Zone_C', 1500.00, 1),
('Algérie', 'Ghardaïa', 'Zone_C', 1500.00, 1),
('Algérie', 'Adrar', 'Zone_C', 1500.00, 1),
('Algérie', 'Illizi', 'Zone_C', 1500.00, 1),
('Algérie', 'Tindouf', 'Zone_C', 1500.00, 1),

-- International
('France', 'Paris', 'International', 5000.00, 1),
('France', 'Marseille', 'International', 5000.00, 1),
('France', 'Lyon', 'International', 5000.00, 1),
('Tunisie', 'Tunis', 'International', 3000.00, 1),
('Maroc', 'Casablanca', 'International', 3500.00, 1),
('Maroc', 'Rabat', 'International', 3500.00, 1),
('Espagne', 'Madrid', 'International', 6000.00, 1),
('Allemagne', 'Berlin', 'International', 7000.00, 1);

-- ============================================
-- 4. TYPES DE SERVICE
-- ============================================

INSERT INTO type_service (code, libelle, description, delai_estime_jours, priorite, is_active) VALUES
('STANDARD', 'Livraison Standard', 'Livraison en 3-5 jours ouvrables', 5, 1, 1),
('EXPRESS', 'Livraison Express', 'Livraison en 24-48h', 1, 2, 1),
('INTERNATIONAL', 'Livraison Internationale', 'Livraison à l''étranger en 7-14 jours', 10, 1, 1);

-- ============================================
-- 5. TARIFICATION
-- ============================================

-- Standard - Zone A
INSERT INTO tarification (type_service_id, destination_id, tarif_poids_kg, tarif_volume_m3, date_debut) 
SELECT 1, id, 50.00, 1000.00, DATE('now')
FROM destination WHERE zone_geographique = 'Zone_A';

-- Standard - Zone B
INSERT INTO tarification (type_service_id, destination_id, tarif_poids_kg, tarif_volume_m3, date_debut) 
SELECT 1, id, 80.00, 1500.00, DATE('now')
FROM destination WHERE zone_geographique = 'Zone_B';

-- Standard - Zone C
INSERT INTO tarification (type_service_id, destination_id, tarif_poids_kg, tarif_volume_m3, date_debut) 
SELECT 1, id, 150.00, 3000.00, DATE('now')
FROM destination WHERE zone_geographique = 'Zone_C';

-- Express - Zone A (×1.5)
INSERT INTO tarification (type_service_id, destination_id, tarif_poids_kg, tarif_volume_m3, date_debut) 
SELECT 2, id, 75.00, 1500.00, DATE('now')
FROM destination WHERE zone_geographique = 'Zone_A';

-- Express - Zone B (×1.5)
INSERT INTO tarification (type_service_id, destination_id, tarif_poids_kg, tarif_volume_m3, date_debut) 
SELECT 2, id, 120.00, 2250.00, DATE('now')
FROM destination WHERE zone_geographique = 'Zone_B';

-- International (×2)
INSERT INTO tarification (type_service_id, destination_id, tarif_poids_kg, tarif_volume_m3, date_debut) 
SELECT 3, id, 200.00, 4000.00, DATE('now')
FROM destination WHERE zone_geographique = 'International';

-- ============================================
-- 6. CLIENTS (25+)
-- ============================================

INSERT INTO client (code_client, type_client, nom, prenom, telephone, email, adresse, ville, pays, statut) VALUES
('CLI-00001', 'particulier', 'Mokrani', 'Samir', '0555111222', 'mokrani@email.dz', '12 Rue Didouche', 'Alger', 'Algérie', 'actif'),
('CLI-00002', 'particulier', 'Benali', 'Nadia', '0666222333', 'benali@email.dz', '45 Boulevard Zirout', 'Oran', 'Algérie', 'actif'),
('CLI-00003', 'entreprise', 'SPA TechnoPlus', NULL, '0555333444', 'contact@technoplus.dz', 'Zone Industrielle', 'Blida', 'Algérie', 'actif'),
('CLI-00004', 'entreprise', 'SARL DistriMax', NULL, '0666444555', 'info@distrimax.dz', 'Rue du Commerce 78', 'Constantine', 'Algérie', 'actif'),
('CLI-00005', 'particulier', 'Khelifa', 'Amine', '0777555666', 'khelifa@email.dz', '23 Cité El Bir', 'Sétif', 'Algérie', 'actif'),
('CLI-00006', 'particulier', 'Messaoud', 'Leila', '0555666777', 'messaoud@email.dz', '67 Rue Larbi Ben M''hidi', 'Annaba', 'Algérie', 'actif'),
('CLI-00007', 'entreprise', 'EURL AutoPièces', NULL, '0666777888', 'ventes@autopieces.dz', 'Route Nationale 1', 'Oran', 'Algérie', 'actif'),
('CLI-00008', 'particulier', 'Zaïdi', 'Mehdi', '0777888999', 'zaidi@email.dz', '12 Lotissement Les Palmiers', 'Tlemcen', 'Algérie', 'actif'),
('CLI-00009', 'particulier', 'Hamza', 'Farida', '0555999000', 'hamza@email.dz', '89 Rue de la Liberté', 'Béjaïa', 'Algérie', 'actif'),
('CLI-00010', 'entreprise', 'SPA MegaStore', NULL, '0666000111', 'achats@megastore.dz', 'Centre Commercial', 'Alger', 'Algérie', 'actif'),
('CLI-00011', 'particulier', 'Boudiaf', 'Rachid', '0777111222', 'boudiaf@email.dz', '34 Avenue de l''Indépendance', 'Batna', 'Algérie', 'actif'),
('CLI-00012', 'particulier', 'Amrani', 'Samia', '0555222333', 'amrani@email.dz', '56 Cité Nouvelle', 'Biskra', 'Algérie', 'actif'),
('CLI-00013', 'entreprise', 'SARL PharmaDist', NULL, '0666333444', 'commandes@pharmadist.dz', 'Zone Activités', 'Sétif', 'Algérie', 'actif'),
('CLI-00014', 'particulier', 'Chérif', 'Karim', '0777444555', 'cherif@email.dz', '78 Boulevard Mohamed V', 'Chlef', 'Algérie', 'actif'),
('CLI-00015', 'particulier', 'Djamel', 'Yasmine', '0555555666', 'djamel@email.dz', '90 Rue des Frères', 'Skikda', 'Algérie', 'actif'),
('CLI-00016', 'entreprise', 'EURL InfoTech', NULL, '0666666777', 'contact@infotech.dz', 'Cyber Parc', 'Alger', 'Algérie', 'actif'),
('CLI-00017', 'particulier', 'Laâouni', 'Sofiane', '0777777888', 'laaouni@email.dz', '12 Impasse du Stade', 'Mostaganem', 'Algérie', 'actif'),
('CLI-00018', 'particulier', 'Bouazza', 'Naïma', '0555888999', 'bouazza@email.dz', '45 Rue Ali Boumendjel', 'El Oued', 'Algérie', 'actif'),
('CLI-00019', 'entreprise', 'SPA BuildCo', NULL, '0666999000', 'admin@buildco.dz', 'Zone Industrielle Sud', 'Oran', 'Algérie', 'actif'),
('CLI-00020', 'particulier', 'Sadek', 'Mounir', '0777000111', 'sadek@email.dz', '23 Cité 20 Août', 'Ouargla', 'Algérie', 'actif'),
('CLI-00021', 'particulier', 'Ferhat', 'Malika', '0555111222', 'ferhat@email.dz', '67 Avenue Emir Abdelkader', 'Tizi Ouzou', 'Algérie', 'actif'),
('CLI-00022', 'entreprise', 'SARL FreshFood', NULL, '0666222333', 'logistique@freshfood.dz', 'Marché de Gros', 'Alger', 'Algérie', 'actif'),
('CLI-00023', 'particulier', 'Madani', 'Hichem', '0777333444', 'madani@email.dz', '89 Lotissement El Wafa', 'Béchar', 'Algérie', 'actif'),
('CLI-00024', 'particulier', 'Zahia', 'Imène', '0555444555', 'zahia@email.dz', '34 Rue Hassiba Ben Bouali', 'Ghardaïa', 'Algérie', 'actif'),
('CLI-00025', 'entreprise', 'EURL TransExport', NULL, '0666555666', 'export@transexport.dz', 'Port d''Alger', 'Alger', 'Algérie', 'actif');

-- Forcer les soldes à zéro dans les insertions de clients
UPDATE client SET solde = 0 WHERE solde IS NULL;

-- ============================================
-- 7. CHAUFFEURS (15+)
-- ============================================

INSERT INTO chauffeur (matricule, nom, prenom, telephone, num_permis, categorie_permis, date_embauche, disponibilite, statut) VALUES
('CHF-00001', 'Brahimi', 'Sofiane', '0770123456', 'P123456', 'C', '2020-01-15', 'disponible', 'actif'),
('CHF-00002', 'Makhloufi', 'Karim', '0771234567', 'P234567', 'C', '2020-03-20', 'disponible', 'actif'),
('CHF-00003', 'Bensaïd', 'Ahmed', '0772345678', 'P345678', 'D', '2019-06-10', 'disponible', 'actif'),
('CHF-00004', 'Hamdani', 'Yacine', '0773456789', 'P456789', 'C', '2021-02-05', 'disponible', 'actif'),
('CHF-00005', 'Zerrouki', 'Malik', '0774567890', 'P567890', 'C', '2020-09-12', 'disponible', 'actif'),
('CHF-00006', 'Touati', 'Riad', '0775678901', 'P678901', 'D', '2019-11-25', 'disponible', 'actif'),
('CHF-00007', 'Menai', 'Farid', '0776789012', 'P789012', 'C', '2021-05-18', 'disponible', 'actif'),
('CHF-00008', 'Djelloul', 'Nassim', '0777890123', 'P890123', 'C', '2020-07-22', 'disponible', 'actif'),
('CHF-00009', 'Sahraoui', 'Bilal', '0778901234', 'P901234', 'C', '2021-01-30', 'disponible', 'actif'),
('CHF-00010', 'Benkhaled', 'Mourad', '0779012345', 'P012345', 'D', '2019-04-14', 'disponible', 'actif'),
('CHF-00011', 'Kaci', 'Amine', '0770223344', 'P112233', 'C', '2021-08-09', 'disponible', 'actif'),
('CHF-00012', 'Lounis', 'Samir', '0771334455', 'P223344', 'C', '2020-12-01', 'disponible', 'actif'),
('CHF-00013', 'Benamar', 'Hocine', '0772445566', 'P334455', 'D', '2019-08-17', 'disponible', 'actif'),
('CHF-00014', 'Meziane', 'Tahar', '0773556677', 'P445566', 'C', '2021-03-22', 'disponible', 'actif'),
('CHF-00015', 'Boudiaf', 'Walid', '0774667788', 'P556677', 'C', '2020-10-11', 'disponible', 'actif');

-- ============================================
-- 8. VÉHICULES (18+)
-- ============================================

INSERT INTO vehicule (immatriculation, type_vehicule, marque, modele, capacite_kg, capacite_m3, consommation_100km, etat, disponibilite) VALUES
-- Fourgons
('16-12345-01', 'fourgon', 'Renault', 'Master', 1500.00, 10.00, 12.5, 'bon', 'disponible'),
('16-12346-01', 'fourgon', 'Peugeot', 'Boxer', 1500.00, 11.00, 13.0, 'bon', 'disponible'),
('16-12347-01', 'fourgon', 'Fiat', 'Ducato', 1400.00, 10.50, 12.8, 'bon', 'disponible'),
('16-12348-01', 'fourgon', 'Mercedes', 'Sprinter', 1600.00, 12.00, 14.0, 'bon', 'disponible'),
('16-12349-01', 'fourgon', 'Ford', 'Transit', 1550.00, 11.50, 13.5, 'bon', 'disponible'),
('16-12350-01', 'fourgon', 'Renault', 'Master', 1500.00, 10.00, 12.5, 'moyen', 'disponible'),

-- Camionnettes
('16-22345-01', 'camionnette', 'Hyundai', 'H100', 1000.00, 6.00, 10.0, 'bon', 'disponible'),
('16-22346-01', 'camionnette', 'Volkswagen', 'Crafter', 1100.00, 6.50, 10.5, 'bon', 'disponible'),
('16-22347-01', 'camionnette', 'Nissan', 'Cabstar', 1050.00, 6.20, 10.2, 'bon', 'disponible'),
('16-22348-01', 'camionnette', 'Isuzu', 'NLR', 1200.00, 7.00, 11.0, 'bon', 'disponible'),

-- Camions
('16-32345-01', 'camion', 'Iveco', 'Daily', 3500.00, 20.00, 18.0, 'bon', 'disponible'),
('16-32346-01', 'camion', 'Mercedes', 'Atego', 4000.00, 25.00, 20.0, 'bon', 'disponible'),
('16-32347-01', 'camion', 'Man', 'TGL', 3800.00, 22.00, 19.0, 'bon', 'disponible'),
('16-32348-01', 'camion', 'Volvo', 'FL', 3600.00, 21.00, 18.5, 'moyen', 'disponible'),
('16-32349-01', 'camion', 'Renault', 'D-Series', 3700.00, 23.00, 19.5, 'bon', 'disponible'),

-- Motos
('16-42345-01', 'moto', 'Honda', 'CB500', 50.00, 0.30, 4.5, 'bon', 'disponible'),
('16-42346-01', 'moto', 'Yamaha', 'MT-07', 50.00, 0.30, 4.8, 'bon', 'disponible'),
('16-42347-01', 'moto', 'Suzuki', 'V-Strom', 55.00, 0.35, 5.0, 'bon', 'disponible');

-- ============================================
-- 9. EXPÉDITIONS (50+)
-- ============================================

-- Explication de la partie expéditions:
-- On crée 50 expéditions avec des données aléatoires réalistes
-- Le code_expedition sera auto-généré par un trigger
-- Le montant_total sera calculé manuellement car SQLite n'a pas de fonctions stockées

-- Expédition 1-10: Zone A, Standard
INSERT INTO expedition (client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, statut, montant_total, created_by) VALUES
(1, 1, 1, 10.5, 0.8, 'Colis documents', '12 Rue Didouche Mourad, Alger', 'M. Samir', '0555111222', 'livre', 0, 2),
(2, 1, 2, 25.0, 1.2, 'Matériel informatique', '45 Boulevard Zirout Youcef, Oran', 'Mme Nadia', '0666222333', 'livre', 0, 2),
(3, 1, 1, 5.2, 0.4, 'Livres', '23 Cité El Bir, Alger', 'M. Amine', '0777555666', 'en_livraison', 0, 2),
(4, 1, 3, 15.8, 0.9, 'Vêtements', '67 Rue Larbi Ben M''hidi, Constantine', 'Mme Leila', '0555666777', 'centre_tri', 0, 2),
(5, 1, 2, 30.0, 1.5, 'Pièces auto', '89 Route Nationale 1, Oran', 'Service EURL', '0666777888', 'en_transit', 0, 2),
(6, 1, 4, 8.3, 0.6, 'Colis divers', '12 Lotissement Palmiers, Annaba', 'M. Mehdi', '0777888999', 'livre', 0, 2),
(7, 1, 1, 45.0, 2.0, 'Électroménager', '34 Avenue Indépendance, Alger', 'Mme Farida', '0555999000', 'livre', 0, 2),
(8, 1, 5, 12.5, 0.7, 'Produits cosmétiques', '56 Cité Nouvelle, Blida', 'Mme Samia', '0555222333', 'en_livraison', 0, 2),
(9, 1, 3, 20.0, 1.0, 'Fournitures bureau', '78 Boulevard Mohamed V, Constantine', 'M. Karim', '0777444555', 'centre_tri', 0, 2),
(10, 1, 6, 35.5, 1.8, 'Matériel médical', '90 Rue des Frères, Batna', 'Pharmacie', '0555555666', 'en_transit', 0, 2),

-- Expédition 11-20: Zone A, Express
(11, 2, 1, 3.0, 0.2, 'Documents urgents', 'Cyber Parc, Alger', 'Direction InfoTech', '0666666777', 'livre', 0, 2),
(12, 2, 2, 8.5, 0.5, 'Échantillons', '12 Impasse Stade, Oran', 'M. Sofiane', '0777777888', 'livre', 0, 3),
(13, 2, 1, 5.0, 0.3, 'Médicaments', '45 Rue Ali Boumendjel, Alger', 'Clinique', '0555888999', 'en_livraison', 0, 2),
(14, 2, 7, 10.0, 0.6, 'Pièces détachées', 'Zone Industrielle Sud, Sétif', 'Atelier BuildCo', '0666999000', 'centre_tri', 0, 3),
(15, 2, 3, 2.5, 0.1, 'Contrats', '23 Cité 20 Août, Constantine', 'Cabinet Avocat', '0777000111', 'en_transit', 0, 2),
(16, 2, 8, 15.0, 0.9, 'Colis express', '67 Avenue Emir Abdelkader, Tlemcen', 'Mme Malika', '0555111222', 'livre', 0, 3),
(17, 2, 1, 4.2, 0.25, 'Cartes bancaires', 'Marché de Gros, Alger', 'Banque', '0666222333', 'livre', 0, 2),
(18, 2, 2, 7.8, 0.4, 'Chèques', '89 Lotissement El Wafa, Oran', 'Entreprise', '0777333444', 'en_livraison', 0, 2),
(19, 2, 4, 6.5, 0.35, 'Documents légaux', '34 Rue Hassiba, Annaba', 'Tribunal', '0555444555', 'centre_tri', 0, 3),
(20, 2, 1, 12.0, 0.7, 'Colis urgent', 'Port d''Alger', 'Service Export', '0666555666', 'en_transit', 0, 2),

-- Expédition 21-30: Zone B
(21, 1, 9, 18.5, 1.1, 'Marchandises', '12 Centre Ville, Béjaïa', 'Magasin', '0770123456', 'livre', 0, 2),
(22, 1, 10, 22.0, 1.3, 'Équipements', '45 Route Principale, Tizi Ouzou', 'Entreprise', '0771234567', 'livre', 0, 3),
(23, 1, 11, 14.8, 0.85, 'Produits alimentaires', '78 Marché Central, Biskra', 'Épicerie', '0772345678', 'en_livraison', 0, 2),
(24, 1, 12, 28.0, 1.6, 'Textile', '23 Zone Commerciale, Chlef', 'Boutique', '0773456789', 'centre_tri', 0, 2),
(25, 1, 13, 16.5, 0.95, 'Matériel scolaire', '56 Rue École, Skikda', 'Librairie', '0774567890', 'en_transit', 0, 3),
(25, 1, 14, 31.0, 1.75, 'Meubles', '89 Avenue Hassan, Mostaganem', 'M. Client', '0775678901', 'livre', 0, 2),
(27, 1, 15, 19.5, 1.15, 'Électronique', '12 Cité Nouvelle, El Oued', 'Magasin Tech', '0776789012', 'livre', 0, 2),
(28, 1, 16, 24.0, 1.4, 'Quincaillerie', '45 Souk, Béchar', 'Commerce', '0777890123', 'en_livraison', 0, 3),
(29, 2, 9, 6.5, 0.4, 'Urgent Béjaïa', '78 Centre, Béjaïa', 'Client Express', '0778901234', 'centre_tri', 0, 2),
(30, 2, 10, 9.0, 0.55, 'Urgent Tizi', '34 Village, Tizi Ouzou', 'Destinataire', '0779012345', 'en_transit', 0, 2),

-- Expédition 31-40: Zone C (Sud)
(31, 1, 17, 42.0, 2.5, 'Matériel construction', 'Chantier Sud, Tamanrasset', 'Entreprise BTP', '0770223344', 'en_transit', 0, 2),
(32, 1, 18, 38.5, 2.2, 'Pièces mécaniques', 'Zone Industrielle, Ouargla', 'Garage', '0771334455', 'centre_tri', 0, 3),
(33, 1, 19, 35.0, 2.0, 'Produits pétrochimie', 'Base Vie, Ghardaïa', 'Société Pétrole', '0772445566', 'en_transit', 0, 2),
(34, 1, 20, 40.0, 2.3, 'Matériel forage', 'Site Désert, Adrar', 'Chantier', '0773556677', 'enregistre', 0, 2),
(35, 1, 21, 33.5, 1.9, 'Équipement solaire', 'Station, Illizi', 'Projet Énergie', '0774667788', 'enregistre', 0, 3),
(36, 2, 17, 15.0, 0.9, 'Urgent Sud', 'Hôpital, Tamanrasset', 'Service Médical', '0775778899', 'centre_tri', 0, 2),
(37, 1, 18, 45.0, 2.6, 'Approvisionnement', 'Base Militaire, Ouargla', 'Service', '0776889900', 'en_transit', 0, 2),
(38, 1, 19, 37.5, 2.15, 'Matériel agricole', 'Palmeraie, Ghardaïa', 'Exploitation', '0777990011', 'enregistre', 0, 3),
(39, 1, 20, 41.0, 2.4, 'Pièces véhicules', 'Garage Centre, Adrar', 'Mécanique', '0778001122', 'enregistre', 0, 2),
(40, 2, 18, 12.0, 0.7, 'Documents urgents', 'Administration, Ouargla', 'Wilaya', '0779112233', 'centre_tri', 0, 2),

-- Expédition 41-50: International
(41, 3, 23, 25.0, 1.5, 'Exportation France', '123 Rue Paris, France', 'Importateur FR', '+33612345678', 'en_transit', 0, 2),
(42, 3, 24, 30.0, 1.8, 'Export Marseille', '456 Bd Marseille, France', 'Client FR', '+33623456789', 'centre_tri', 0, 3),
(43, 3, 27, 22.0, 1.3, 'Artisanat Tunisie', '789 Avenue Tunis', 'Boutique TN', '+21612345678', 'en_transit', 0, 2),
(44, 3, 28, 28.5, 1.65, 'Export Maroc', '321 Rue Casa, Maroc', 'Société MA', '+212612345678', 'centre_tri', 0, 2),
(45, 3, 23, 18.0, 1.1, 'Colis Paris', '654 Paris 15ème', 'M. Dupont', '+33634567890', 'en_transit', 0, 3),
(46, 3, 25, 26.0, 1.55, 'Export Lyon', '987 Lyon Centre', 'Entreprise FR', '+33645678901', 'enregistre', 0, 2),
(47, 3, 27, 20.5, 1.2, 'Produits Tunis', '147 Tunis Médina', 'Client TN', '+21623456789', 'enregistre', 0, 2),
(48, 3, 28, 24.0, 1.4, 'Export Rabat', '258 Rabat Centre', 'Société MA', '+212623456789', 'enregistre', 0, 3),
(49, 3, 30, 32.0, 1.9, 'Export Espagne', '369 Madrid', 'Client ES', '+34612345678', 'enregistre', 0, 2),
(50, 3, 31, 35.0, 2.05, 'Export Allemagne', '741 Berlin', 'Firma DE', '+49151234567', 'enregistre', 0, 2);

-- Donnees de test: completer les champs optionnels (utile pour l'UI)
UPDATE destination
SET code_zone = printf('%05d', 10000 + id)
WHERE code_zone IS NULL OR TRIM(code_zone) = '';

UPDATE chauffeur
SET num_permis = 'P' || printf('%06d', 100000 + id)
WHERE num_permis IS NULL OR TRIM(num_permis) = '';

-- "Matricule vehicule" (interprete comme immatriculation): completer si manquant
UPDATE vehicule
SET immatriculation = 'VH-' || printf('%05d', id)
WHERE immatriculation IS NULL OR TRIM(immatriculation) = '';
