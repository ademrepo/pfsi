-- ============================================
-- SEED COMPLET 2024-2026
-- ============================================
-- Ce fichier contient :
-- - DonnÃ©es historiques pour 2024, 2025 et dÃ©but 2026
-- - Montants de factures rÃ©alistes (500-3000 DZD TTC)
-- - Factures impayÃ©es et partiellement payÃ©es
-- ============================================

-- ============================================
-- 1. NETTOYAGE
-- ============================================
DELETE FROM alerte;
DELETE FROM reclamation_expedition;
DELETE FROM reclamation;
DELETE FROM incident_attachment;
DELETE FROM incident;
DELETE FROM paiement;
DELETE FROM facture_expedition;
DELETE FROM facture;
DELETE FROM tracking_expedition;
DELETE FROM expedition;
DELETE FROM tournee;
DELETE FROM tarification;
DELETE FROM type_service;
DELETE FROM destination;
DELETE FROM vehicule;
DELETE FROM chauffeur;
DELETE FROM client;
DELETE FROM favori;
DELETE FROM utilisateur;
DELETE FROM role;
DELETE FROM sqlite_sequence;

-- ============================================
-- 2. RÃ”LES & UTILISATEURS
-- ============================================
INSERT INTO role (code, libelle) VALUES
('ADMIN', 'Administrateur'), 
('AGENT', 'Agent de transport'), 
('COMPTABLE', 'Comptable'), 
('LOGISTIQUE', 'Responsable logistique'), 
('DIRECTION', 'Direction'), 
('CHAUFFEUR', 'Chauffeur');

INSERT INTO utilisateur (username, email, password, nom, prenom, telephone, role_id, is_active, created_at) VALUES
('admin', 'admin@transport.dz', 'password123', 'Benali', 'Ahmed', '0555123456', 1, 1, '2024-01-01 10:00:00'),
('agent1', 'agent1@transport.dz', 'password123', 'Kaci', 'Fatima', '0666234567', 2, 1, '2024-01-01 10:00:00'),
('comptable1', 'compta@transport.dz', 'password123', 'Saidi', 'Meriem', '0555456789', 3, 1, '2024-01-01 10:00:00');

-- ============================================
-- 3. DESTINATIONS
-- ============================================
INSERT INTO destination (pays, ville, zone_geographique, code_zone, tarif_base_defaut, is_active, latitude, longitude) VALUES
('AlgÃ©rie', 'Alger', 'Zone_A', 'ZA001', 500.00, 1, 36.7372, 3.0869),
('AlgÃ©rie', 'Oran', 'Zone_A', 'ZA002', 500.00, 1, 35.7325, -0.6418),
('AlgÃ©rie', 'Constantine', 'Zone_A', 'ZA003', 500.00, 1, 36.3656, 6.6147),
('AlgÃ©rie', 'Annaba', 'Zone_A', 'ZA004', 500.00, 1, 36.9000, 7.7600),
('AlgÃ©rie', 'Blida', 'Zone_A', 'ZA005', 500.00, 1, 36.4844, 2.8277),
('AlgÃ©rie', 'SÃ©tif', 'Zone_A', 'ZA007', 500.00, 1, 36.1900, 5.4080),
('AlgÃ©rie', 'BÃ©jaÃ¯a', 'Zone_B', 'ZB001', 800.00, 1, 36.7519, 5.0840),
('AlgÃ©rie', 'Tizi Ouzou', 'Zone_B', 'ZB002', 800.00, 1, 36.7167, 4.0667),
('AlgÃ©rie', 'Biskra', 'Zone_B', 'ZB003', 800.00, 1, 34.8067, 5.7333),
('AlgÃ©rie', 'Chlef', 'Zone_B', 'ZB004', 800.00, 1, 36.1667, 1.3333),
('AlgÃ©rie', 'Skikda', 'Zone_B', 'ZB005', 800.00, 1, 36.8769, 6.9064),
('AlgÃ©rie', 'Ouargla', 'Zone_C', 'ZC002', 1500.00, 1, 31.9454, 5.3268),
('AlgÃ©rie', 'GhardaÃ¯a', 'Zone_C', 'ZC003', 1500.00, 1, 32.4904, 3.6589),
('AlgÃ©rie', 'Adrar', 'Zone_C', 'ZC004', 1500.00, 1, 27.8789, -0.2711),
('AlgÃ©rie', 'Illizi', 'Zone_C', 'ZC005', 1500.00, 1, 26.1667, 8.4667),
('AlgÃ©rie', 'Tamanrasset', 'Zone_C', 'ZC001', 1500.00, 1, 22.7917, 5.5267);

-- ============================================
-- 4. TYPE SERVICE & TARIFICATION
-- ============================================
INSERT INTO type_service (code, libelle, description, delai_estime_jours, priorite, is_active) VALUES
('STANDARD', 'Livraison Standard', '3-5 jours', 5, 1, 1),
('EXPRESS', 'Livraison Express', '24-48h', 1, 2, 1),
('INTERNATIONAL', 'International', '7-14 jours', 10, 1, 1);

INSERT INTO tarification (type_service_id, destination_id, tarif_base, tarif_poids_kg, tarif_volume_m3, date_debut) 
SELECT 1, id, 500.00, 50.00, 1000.00, '2024-01-01' FROM destination;

-- ============================================
-- 5. CLIENTS
-- ============================================
INSERT INTO client (code_client, type_client, nom, prenom, telephone, email, adresse, ville, pays, solde, statut, created_at) VALUES
('CLI-00001', 'particulier', 'Mokrani', 'Samir', '0555111222', 'mokrani@email.dz', '12 Rue Didouche', 'Alger', 'AlgÃ©rie', 0, 'actif', '2024-01-15 10:00:00'),
('CLI-00002', 'particulier', 'Benali', 'Nadia', '0666222333', 'benali@email.dz', '45 Blvd Zirout', 'Oran', 'AlgÃ©rie', 0, 'actif', '2024-02-10 11:00:00'),
('CLI-00003', 'particulier', 'Khelifa', 'Amine', '0777555666', 'khelifa@email.dz', '23 CitÃ© El Bir', 'SÃ©tif', 'AlgÃ©rie', 0, 'actif', '2024-01-20 09:30:00'),
('CLI-00004', 'particulier', 'Messaoud', 'Leila', '0555666777', 'messaoud@email.dz', 'Rue Larbi Ben Mhidi', 'Annaba', 'AlgÃ©rie', 0, 'actif', '2024-03-05 14:00:00'),
('CLI-00005', 'particulier', 'Zaai', 'Mehdi', '0777888999', 'zaidi@email.dz', 'Les Palmiers', 'Tlemcen', 'AlgÃ©rie', 0, 'actif', '2024-02-15 10:00:00'),
('CLI-00011', 'entreprise', 'SPA TechnoPlus', 'Contact', '0555333444', 'contact@technoplus.dz', 'Zone Ind.', 'Blida', 'AlgÃ©rie', 0, 'actif', '2024-01-05 10:00:00'),
('CLI-00012', 'entreprise', 'SARL DistriMax', 'Contact', '0666444555', 'info@distrimax.dz', 'Rue Commerce', 'Constantine', 'AlgÃ©rie', 0, 'actif', '2024-01-08 11:00:00'),
('CLI-00013', 'entreprise', 'EURL AutoPiÃ¨ces', 'Contact', '0666777888', 'ventes@autopieces.dz', 'RN 1', 'Oran', 'AlgÃ©rie', 0, 'actif', '2024-02-01 09:00:00'),
('CLI-00014', 'entreprise', 'SPA MegaStore', 'Contact', '0666000111', 'achats@megastore.dz', 'Centre Com.', 'Alger', 'AlgÃ©rie', 0, 'actif', '2024-02-15 13:30:00'),
('CLI-00015', 'entreprise', 'SARL PharmaDist', 'Contact', '0666333444', 'commandes@pharmadist.dz', 'Zone Act.', 'SÃ©tif', 'AlgÃ©rie', 0, 'actif', '2024-03-10 10:15:00'),
('CLI-00016', 'entreprise', 'EURL InfoTech', 'Contact', '0666666777', 'contact@infotech.dz', 'Cyber Parc', 'Alger', 'AlgÃ©rie', 0, 'actif', '2024-03-22 14:00:00'),
('CLI-00017', 'entreprise', 'SPA BuildCo', 'Contact', '0666999000', 'admin@buildco.dz', 'Zone Ind. Sud', 'Oran', 'AlgÃ©rie', 0, 'actif', '2024-04-05 11:00:00'),
('CLI-00018', 'entreprise', 'SARL FreshFood', 'Contact', '0666222333', 'logistique@freshfood.dz', 'MarchÃ© Gros', 'Alger', 'AlgÃ©rie', 0, 'actif', '2024-01-02 08:30:00'),
('CLI-00019', 'entreprise', 'EURL TransExport', 'Contact', '0666555666', 'export@transexport.dz', 'Port', 'Alger', 'AlgÃ©rie', 0, 'actif', '2024-04-18 10:00:00'),
('CLI-00020', 'entreprise', 'SPA LogisticPlus', 'Contact', '0666888999', 'ops@logisticplus.dz', 'Zone Log.', 'Alger', 'AlgÃ©rie', 0, 'actif', '2024-05-01 09:00:00');

-- ============================================
-- 6. CHAUFFEURS
-- ============================================
INSERT INTO chauffeur (matricule, nom, prenom, telephone, email, adresse, num_permis, categorie_permis, date_embauche, disponibilite, statut) VALUES
('CHF-00001', 'Brahimi', 'Sofiane', '0770123456', 'brahimi@transport.dz', 'Alger', 'P123456', 'D', '2019-01-15', 'disponible', 'actif'),
('CHF-00002', 'Makhloufi', 'Karim', '0771234567', 'makhloufi@transport.dz', 'Oran', 'P234567', 'D', '2019-03-20', 'disponible', 'actif'),
('CHF-00003', 'BensaÃ¯d', 'Ahmed', '0772345678', 'bensaid@transport.dz', 'Constantine', 'P345678', 'D', '2018-06-10', 'disponible', 'actif'),
('CHF-00004', 'Hamdani', 'Yacine', '0773456789', 'hamdani@transport.dz', 'Blida', 'P456789', 'C', '2020-02-05', 'disponible', 'actif'),
('CHF-00005', 'Zerrouki', 'Malik', '0774567890', 'zerrouki@transport.dz', 'SÃ©tif', 'P567890', 'C', '2019-09-12', 'disponible', 'actif');

-- ============================================
-- 7. VÃ‰HICULES
-- ============================================
INSERT INTO vehicule (immatriculation, type_vehicule, marque, modele, capacite_kg, capacite_m3, consommation_100km, etat, disponibilite, date_mise_en_service) VALUES
('16-32345-01', 'camion', 'Iveco', 'Daily', 3500, 20, 18.0, 'bon', 'disponible', '2019-01-15'),
('16-32346-01', 'camion', 'Mercedes', 'Atego', 4000, 25, 20.0, 'bon', 'disponible', '2019-03-20'),
('16-32347-01', 'camion', 'Man', 'TGL', 3800, 22, 19.0, 'bon', 'disponible', '2018-06-10'),
('16-12345-01', 'fourgon', 'Renault', 'Master', 1500, 10, 12.5, 'bon', 'disponible', '2020-01-15'),
('16-12346-01', 'fourgon', 'Peugeot', 'Boxer', 1500, 11, 13.0, 'bon', 'disponible', '2020-03-20');
-- ============================================
-- TOURNÃ‰ES, EXPÃ‰DITIONS ET FACTURES 2024-2026
-- ============================================

-- TOURNÃ‰ES
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-01-01', '2024-01-23', '2024-01-23 10:00:00', '2024-01-23 21:29:00', 1, 4, 'Terminée', 9000, 9131, 131, 689, 22.97, 'TournÃ©e January 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-01-02', '2024-01-12', '2024-01-12 10:00:00', '2024-01-12 16:56:00', 5, 2, 'Terminée', 7000, 7534, 534, 416, 99.9, 'TournÃ©e January 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-02-01', '2024-02-25', '2024-02-25 06:00:00', '2024-02-25 13:22:00', 1, 3, 'Terminée', 8000, 8288, 288, 442, 52.47, 'TournÃ©e February 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-02-02', '2024-02-21', '2024-02-21 07:00:00', '2024-02-21 13:18:00', 1, 2, 'Terminée', 7534, 7639, 105, 378, 15.06, 'TournÃ©e February 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-02-03', '2024-02-07', '2024-02-07 06:00:00', '2024-02-07 14:28:00', 4, 1, 'Terminée', 6000, 6199, 199, 508, 35.71, 'TournÃ©e February 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-03-01', '2024-03-16', '2024-03-16 07:00:00', '2024-03-16 20:12:00', 3, 3, 'Terminée', 8288, 8732, 444, 792, 76.97, 'TournÃ©e March 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-03-02', '2024-03-10', '2024-03-10 06:00:00', '2024-03-10 12:51:00', 1, 3, 'Terminée', 8732, 9317, 585, 411, 75.11, 'TournÃ©e March 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-03-03', '2024-03-18', '2024-03-18 09:00:00', '2024-03-18 19:24:00', 3, 5, 'Terminée', 10000, 10510, 510, 624, 72.14, 'TournÃ©e March 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-04-01', '2024-04-09', '2024-04-09 08:00:00', '2024-04-09 14:02:00', 5, 4, 'Terminée', 9131, 9722, 591, 362, 111.7, 'TournÃ©e April 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-04-02', '2024-04-25', '2024-04-25 09:00:00', '2024-04-25 18:49:00', 2, 5, 'Terminée', 10510, 10753, 243, 589, 35.54, 'TournÃ©e April 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-04-03', '2024-04-19', '2024-04-19 06:00:00', '2024-04-19 12:40:00', 5, 3, 'Terminée', 9317, 9439, 122, 400, 19.44, 'TournÃ©e April 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-05-01', '2024-05-14', '2024-05-14 07:00:00', '2024-05-14 17:11:00', 4, 1, 'Terminée', 6199, 6519, 320, 611, 48.54, 'TournÃ©e May 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-05-02', '2024-05-15', '2024-05-15 09:00:00', '2024-05-15 15:47:00', 4, 2, 'Terminée', 7639, 8159, 520, 407, 96.94, 'TournÃ©e May 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-06-01', '2024-06-12', '2024-06-12 08:00:00', '2024-06-12 21:30:00', 2, 4, 'Terminée', 9722, 10129, 407, 810, 58.71, 'TournÃ©e June 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-06-02', '2024-06-06', '2024-06-06 06:00:00', '2024-06-06 16:55:00', 1, 2, 'Terminée', 8159, 8374, 215, 655, 28.17, 'TournÃ©e June 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-06-03', '2024-06-10', '2024-06-10 07:00:00', '2024-06-10 15:56:00', 4, 2, 'Terminée', 8374, 8571, 197, 536, 33.55, 'TournÃ©e June 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-07-01', '2024-07-08', '2024-07-08 08:00:00', '2024-07-08 16:13:00', 5, 4, 'Terminée', 10129, 10530, 401, 493, 57.68, 'TournÃ©e July 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-07-02', '2024-07-21', '2024-07-21 08:00:00', '2024-07-21 19:16:00', 2, 2, 'Terminée', 8571, 8804, 233, 676, 45.81, 'TournÃ©e July 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-07-03', '2024-07-18', '2024-07-18 10:00:00', '2024-07-18 19:47:00', 4, 2, 'Terminée', 8804, 9294, 490, 587, 93.31, 'TournÃ©e July 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-08-01', '2024-08-23', '2024-08-23 09:00:00', '2024-08-23 15:07:00', 5, 1, 'Terminée', 6519, 6640, 121, 367, 21.67, 'TournÃ©e August 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-08-02', '2024-08-20', '2024-08-20 10:00:00', '2024-08-20 16:20:00', 1, 4, 'Terminée', 10530, 11082, 552, 380, 67.27, 'TournÃ©e August 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-09-01', '2024-09-21', '2024-09-21 10:00:00', '2024-09-21 16:59:00', 1, 5, 'Terminée', 10753, 10922, 169, 419, 25.09, 'TournÃ©e September 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-09-02', '2024-09-05', '2024-09-05 07:00:00', '2024-09-05 18:01:00', 1, 3, 'Terminée', 9439, 9851, 412, 661, 53.78, 'TournÃ©e September 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-09-03', '2024-09-15', '2024-09-15 09:00:00', '2024-09-15 18:15:00', 5, 2, 'Terminée', 9294, 9775, 481, 555, 92.67, 'TournÃ©e September 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-10-01', '2024-10-16', '2024-10-16 07:00:00', '2024-10-16 13:10:00', 1, 5, 'Terminée', 10922, 11500, 578, 370, 85.08, 'TournÃ©e October 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-10-02', '2024-10-07', '2024-10-07 10:00:00', '2024-10-07 17:10:00', 2, 1, 'Terminée', 6640, 6987, 347, 430, 44.5, 'TournÃ©e October 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-11-01', '2024-11-15', '2024-11-15 07:00:00', '2024-11-15 15:58:00', 3, 3, 'Terminée', 9851, 10221, 370, 538, 44.83, 'TournÃ©e November 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-11-02', '2024-11-22', '2024-11-22 08:00:00', '2024-11-22 18:01:00', 3, 2, 'Terminée', 9775, 9877, 102, 601, 19.79, 'TournÃ©e November 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-12-01', '2024-12-22', '2024-12-22 07:00:00', '2024-12-22 13:53:00', 3, 1, 'Terminée', 6987, 7179, 192, 413, 37.85, 'TournÃ©e December 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2024-12-02', '2024-12-08', '2024-12-08 06:00:00', '2024-12-08 18:21:00', 3, 4, 'Terminée', 11082, 11223, 141, 741, 25.05, 'TournÃ©e December 2024', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-01-01', '2025-01-23', '2025-01-23 09:00:00', '2025-01-23 19:03:00', 1, 3, 'Terminée', 10221, 10411, 190, 603, 29.94, 'TournÃ©e January 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-01-02', '2025-01-16', '2025-01-16 07:00:00', '2025-01-16 15:17:00', 1, 1, 'Terminée', 7179, 7777, 598, 497, 76.61, 'TournÃ©e January 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-01-03', '2025-01-05', '2025-01-05 07:00:00', '2025-01-05 13:47:00', 4, 5, 'Terminée', 11500, 11865, 365, 407, 60.43, 'TournÃ©e January 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-02-01', '2025-02-19', '2025-02-19 09:00:00', '2025-02-19 19:17:00', 3, 2, 'Terminée', 9877, 10460, 583, 617, 84.0, 'TournÃ©e February 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-02-02', '2025-02-08', '2025-02-08 06:00:00', '2025-02-08 13:53:00', 4, 2, 'Terminée', 10460, 11012, 552, 473, 93.74, 'TournÃ©e February 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-02-03', '2025-02-08', '2025-02-08 06:00:00', '2025-02-08 19:22:00', 2, 1, 'Terminée', 7777, 8177, 400, 802, 64.83, 'TournÃ©e February 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-03-01', '2025-03-15', '2025-03-15 07:00:00', '2025-03-15 18:00:00', 4, 2, 'Terminée', 11012, 11421, 409, 660, 66.99, 'TournÃ©e March 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-03-02', '2025-03-25', '2025-03-25 09:00:00', '2025-03-25 22:55:00', 4, 5, 'Terminée', 11865, 11970, 105, 835, 14.37, 'TournÃ©e March 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-03-03', '2025-03-07', '2025-03-07 06:00:00', '2025-03-07 13:32:00', 3, 4, 'Terminée', 11223, 11508, 285, 452, 35.55, 'TournÃ©e March 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-04-01', '2025-04-08', '2025-04-08 07:00:00', '2025-04-08 15:51:00', 2, 3, 'Terminée', 10411, 10983, 572, 531, 78.72, 'TournÃ©e April 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-04-02', '2025-04-13', '2025-04-13 07:00:00', '2025-04-13 19:55:00', 1, 3, 'Terminée', 10983, 11213, 230, 775, 29.42, 'TournÃ©e April 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-04-03', '2025-04-08', '2025-04-08 09:00:00', '2025-04-08 16:23:00', 4, 1, 'Terminée', 8177, 8413, 236, 443, 33.65, 'TournÃ©e April 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-05-01', '2025-05-14', '2025-05-14 06:00:00', '2025-05-14 13:02:00', 1, 2, 'Terminée', 11421, 11556, 135, 422, 26.9, 'TournÃ©e May 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-05-02', '2025-05-19', '2025-05-19 07:00:00', '2025-05-19 19:19:00', 5, 2, 'Terminée', 11556, 12108, 552, 739, 97.48, 'TournÃ©e May 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-05-03', '2025-05-10', '2025-05-10 10:00:00', '2025-05-10 23:34:00', 5, 1, 'Terminée', 8413, 8529, 116, 814, 17.1, 'TournÃ©e May 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-06-01', '2025-06-21', '2025-06-21 08:00:00', '2025-06-21 15:23:00', 1, 3, 'Terminée', 11213, 11373, 160, 443, 20.9, 'TournÃ©e June 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-06-02', '2025-06-19', '2025-06-19 10:00:00', '2025-06-19 19:34:00', 5, 1, 'Terminée', 8529, 8904, 375, 574, 61.0, 'TournÃ©e June 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-06-03', '2025-06-24', '2025-06-24 06:00:00', '2025-06-24 18:48:00', 4, 3, 'Terminée', 11373, 11861, 488, 768, 61.38, 'TournÃ©e June 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-07-01', '2025-07-06', '2025-07-06 10:00:00', '2025-07-06 18:56:00', 5, 5, 'Terminée', 11970, 12431, 461, 536, 75.15, 'TournÃ©e July 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-07-02', '2025-07-06', '2025-07-06 06:00:00', '2025-07-06 17:32:00', 2, 4, 'Terminée', 11508, 11731, 223, 692, 33.56, 'TournÃ©e July 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-07-03', '2025-07-19', '2025-07-19 07:00:00', '2025-07-19 13:18:00', 4, 5, 'Terminée', 12431, 12986, 555, 378, 82.04, 'TournÃ©e July 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-08-01', '2025-08-07', '2025-08-07 09:00:00', '2025-08-07 22:26:00', 4, 1, 'Terminée', 8904, 9156, 252, 806, 45.01, 'TournÃ©e August 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-08-02', '2025-08-19', '2025-08-19 07:00:00', '2025-08-19 16:43:00', 4, 2, 'Terminée', 12108, 12449, 341, 583, 44.19, 'TournÃ©e August 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-08-03', '2025-08-10', '2025-08-10 06:00:00', '2025-08-10 18:30:00', 4, 5, 'Terminée', 12986, 13170, 184, 750, 34.23, 'TournÃ©e August 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-09-01', '2025-09-13', '2025-09-13 06:00:00', '2025-09-13 18:20:00', 4, 2, 'Terminée', 12449, 12916, 467, 740, 79.7, 'TournÃ©e September 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-09-02', '2025-09-09', '2025-09-09 08:00:00', '2025-09-09 20:13:00', 2, 5, 'Terminée', 13170, 13626, 456, 733, 61.92, 'TournÃ©e September 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-09-03', '2025-09-10', '2025-09-10 10:00:00', '2025-09-10 23:58:00', 5, 4, 'Terminée', 11731, 12216, 485, 838, 84.47, 'TournÃ©e September 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-10-01', '2025-10-23', '2025-10-23 07:00:00', '2025-10-23 14:23:00', 4, 1, 'Terminée', 9156, 9646, 490, 443, 59.97, 'TournÃ©e October 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-10-02', '2025-10-15', '2025-10-15 08:00:00', '2025-10-15 19:33:00', 5, 2, 'Terminée', 12916, 13297, 381, 693, 56.73, 'TournÃ©e October 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-10-03', '2025-10-18', '2025-10-18 09:00:00', '2025-10-18 19:04:00', 1, 5, 'Terminée', 13626, 14148, 522, 604, 68.83, 'TournÃ©e October 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-11-01', '2025-11-21', '2025-11-21 08:00:00', '2025-11-21 20:20:00', 5, 3, 'Terminée', 11861, 12318, 457, 740, 66.65, 'TournÃ©e November 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-11-02', '2025-11-14', '2025-11-14 07:00:00', '2025-11-14 15:02:00', 3, 4, 'Terminée', 12216, 12726, 510, 482, 91.95, 'TournÃ©e November 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-12-01', '2025-12-25', '2025-12-25 07:00:00', '2025-12-25 18:04:00', 3, 5, 'Terminée', 14148, 14599, 451, 664, 79.44, 'TournÃ©e December 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2025-12-02', '2025-12-08', '2025-12-08 08:00:00', '2025-12-08 21:26:00', 3, 3, 'Terminée', 12318, 12886, 568, 806, 70.38, 'TournÃ©e December 2025', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2026-01-01', '2026-01-20', '2026-01-20 09:00:00', '2026-01-20 19:22:00', 3, 3, 'Terminée', 12886, 13164, 278, 622, 35.5, 'TournÃ©e January 2026', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2026-01-02', '2026-01-22', '2026-01-22 10:00:00', '2026-01-22 19:08:00', 2, 4, 'Terminée', 12726, 12850, 124, 548, 18.63, 'TournÃ©e January 2026', 1);
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
('TRN-2026-01-03', '2026-01-19', '2026-01-19 06:00:00', '2026-01-19 14:27:00', 5, 3, 'Terminée', 13164, 13686, 522, 507, 83.43, 'TournÃ©e January 2026', 1);

-- EXPÃ‰DITIONS
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-01-001', 5, 1, 8, 15.8, 2.5, 'Colis standard', 'Livraison 8', 'Destinataire 1', '0555000001', '2024-01-22 10:00:00', 'livre', 1587.89, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-01-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-01-002', 19, 1, 6, 9.4, 0.8, 'Colis standard', 'Livraison 6', 'Destinataire 2', '0555000002', '2024-01-22 10:00:00', 'livre', 1556.07, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-01-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-01-003', 5, 1, 8, 23.9, 1.8, 'Colis standard', 'Livraison 8', 'Destinataire 3', '0555000003', '2024-01-11 10:00:00', 'livre', 1574.56, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-01-004', 12, 1, 9, 11.1, 1.8, 'Colis standard', 'Livraison 9', 'Destinataire 4', '0555000004', '2024-01-11 10:00:00', 'livre', 2110.59, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-01-005', 6, 1, 3, 13.5, 0.6, 'Colis standard', 'Livraison 3', 'Destinataire 5', '0555000005', '2024-01-11 10:00:00', 'livre', 1621.93, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-01-006', 1, 1, 4, 27.3, 2.5, 'Colis standard', 'Livraison 4', 'Destinataire 6', '0555000006', '2024-01-11 10:00:00', 'livre', 2819.57, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-007', 18, 1, 14, 20.6, 1.1, 'Colis standard', 'Livraison 14', 'Destinataire 7', '0555000007', '2024-02-24 10:00:00', 'livre', 1840.45, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-008', 10, 1, 14, 8.3, 1.0, 'Colis standard', 'Livraison 14', 'Destinataire 8', '0555000008', '2024-02-24 10:00:00', 'livre', 1740.92, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-009', 12, 1, 1, 24.2, 1.7, 'Colis standard', 'Livraison 1', 'Destinataire 9', '0555000009', '2024-02-24 10:00:00', 'livre', 2807.21, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-010', 1, 1, 7, 11.5, 2.3, 'Colis standard', 'Livraison 7', 'Destinataire 10', '0555000010', '2024-02-20 10:00:00', 'livre', 2670.87, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-011', 18, 1, 5, 12.1, 1.1, 'Colis standard', 'Livraison 5', 'Destinataire 11', '0555000011', '2024-02-20 10:00:00', 'livre', 955.38, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-012', 4, 1, 16, 18.6, 1.7, 'Colis standard', 'Livraison 16', 'Destinataire 12', '0555000012', '2024-02-20 10:00:00', 'livre', 1051.28, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-013', 17, 1, 3, 9.0, 1.3, 'Colis standard', 'Livraison 3', 'Destinataire 13', '0555000013', '2024-02-06 10:00:00', 'livre', 1378.36, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-014', 3, 1, 12, 22.8, 1.0, 'Colis standard', 'Livraison 12', 'Destinataire 14', '0555000014', '2024-02-06 10:00:00', 'livre', 2453.3, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-015', 18, 1, 4, 19.5, 1.0, 'Colis standard', 'Livraison 4', 'Destinataire 15', '0555000015', '2024-02-06 10:00:00', 'livre', 646.73, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-02-016', 1, 1, 5, 23.1, 2.1, 'Colis standard', 'Livraison 5', 'Destinataire 16', '0555000016', '2024-02-06 10:00:00', 'livre', 877.71, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-02-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-017', 20, 1, 2, 28.5, 2.1, 'Colis standard', 'Livraison 2', 'Destinataire 17', '0555000017', '2024-03-15 10:00:00', 'livre', 1028.68, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-018', 10, 1, 16, 10.7, 1.5, 'Colis standard', 'Livraison 16', 'Destinataire 18', '0555000018', '2024-03-15 10:00:00', 'livre', 2384.45, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-019', 6, 1, 9, 28.6, 1.0, 'Colis standard', 'Livraison 9', 'Destinataire 19', '0555000019', '2024-03-09 10:00:00', 'livre', 2168.22, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-020', 11, 1, 7, 18.3, 0.9, 'Colis standard', 'Livraison 7', 'Destinataire 20', '0555000020', '2024-03-09 10:00:00', 'livre', 2397.7, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-021', 16, 1, 12, 21.1, 2.2, 'Colis standard', 'Livraison 12', 'Destinataire 21', '0555000021', '2024-03-09 10:00:00', 'livre', 2136.62, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-022', 1, 1, 9, 11.8, 1.0, 'Colis standard', 'Livraison 9', 'Destinataire 22', '0555000022', '2024-03-17 10:00:00', 'livre', 2086.97, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-023', 20, 1, 16, 19.7, 1.5, 'Colis standard', 'Livraison 16', 'Destinataire 23', '0555000023', '2024-03-17 10:00:00', 'livre', 1827.73, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-024', 2, 1, 5, 20.5, 0.9, 'Colis standard', 'Livraison 5', 'Destinataire 24', '0555000024', '2024-03-17 10:00:00', 'livre', 2499.83, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-03-025', 5, 1, 5, 11.6, 2.0, 'Colis standard', 'Livraison 5', 'Destinataire 25', '0555000025', '2024-03-17 10:00:00', 'livre', 1133.3, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-03-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-026', 11, 1, 1, 11.8, 1.8, 'Colis standard', 'Livraison 1', 'Destinataire 26', '0555000026', '2024-04-08 10:00:00', 'livre', 2351.18, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-027', 7, 1, 9, 15.3, 2.0, 'Colis standard', 'Livraison 9', 'Destinataire 27', '0555000027', '2024-04-08 10:00:00', 'livre', 1042.53, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-028', 13, 1, 7, 14.3, 0.8, 'Colis standard', 'Livraison 7', 'Destinataire 28', '0555000028', '2024-04-08 10:00:00', 'livre', 1312.55, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-029', 18, 1, 9, 27.2, 1.0, 'Colis standard', 'Livraison 9', 'Destinataire 29', '0555000029', '2024-04-08 10:00:00', 'livre', 668.98, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-030', 14, 1, 14, 26.0, 1.9, 'Colis standard', 'Livraison 14', 'Destinataire 30', '0555000030', '2024-04-24 10:00:00', 'livre', 1187.66, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-031', 14, 1, 2, 29.6, 2.0, 'Colis standard', 'Livraison 2', 'Destinataire 31', '0555000031', '2024-04-24 10:00:00', 'livre', 1247.18, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-032', 7, 1, 10, 8.5, 2.4, 'Colis standard', 'Livraison 10', 'Destinataire 32', '0555000032', '2024-04-24 10:00:00', 'livre', 2115.79, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-033', 18, 1, 3, 25.4, 1.3, 'Colis standard', 'Livraison 3', 'Destinataire 33', '0555000033', '2024-04-24 10:00:00', 'livre', 2237.78, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-034', 14, 1, 9, 26.5, 1.2, 'Colis standard', 'Livraison 9', 'Destinataire 34', '0555000034', '2024-04-18 10:00:00', 'livre', 653.25, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-035', 18, 1, 10, 8.4, 2.4, 'Colis standard', 'Livraison 10', 'Destinataire 35', '0555000035', '2024-04-18 10:00:00', 'livre', 2069.59, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-04-036', 5, 1, 16, 20.0, 1.9, 'Colis standard', 'Livraison 16', 'Destinataire 36', '0555000036', '2024-04-18 10:00:00', 'livre', 1844.53, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-04-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-05-037', 13, 1, 9, 29.5, 1.1, 'Colis standard', 'Livraison 9', 'Destinataire 37', '0555000037', '2024-05-13 10:00:00', 'livre', 812.51, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-05-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-05-038', 7, 1, 14, 18.4, 2.2, 'Colis standard', 'Livraison 14', 'Destinataire 38', '0555000038', '2024-05-13 10:00:00', 'livre', 1240.78, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-05-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-05-039', 16, 1, 5, 8.2, 2.2, 'Colis standard', 'Livraison 5', 'Destinataire 39', '0555000039', '2024-05-14 10:00:00', 'livre', 2364.78, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-05-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-05-040', 20, 1, 12, 18.8, 1.0, 'Colis standard', 'Livraison 12', 'Destinataire 40', '0555000040', '2024-05-14 10:00:00', 'livre', 2055.08, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-05-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-05-041', 20, 1, 4, 17.3, 1.7, 'Colis standard', 'Livraison 4', 'Destinataire 41', '0555000041', '2024-05-14 10:00:00', 'livre', 2043.41, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-05-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-05-042', 5, 1, 11, 17.3, 2.3, 'Colis standard', 'Livraison 11', 'Destinataire 42', '0555000042', '2024-05-14 10:00:00', 'livre', 2797.61, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-05-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-043', 6, 1, 13, 17.1, 0.8, 'Colis standard', 'Livraison 13', 'Destinataire 43', '0555000043', '2024-06-11 10:00:00', 'livre', 2603.32, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-044', 3, 1, 4, 21.1, 1.6, 'Colis standard', 'Livraison 4', 'Destinataire 44', '0555000044', '2024-06-11 10:00:00', 'livre', 1351.67, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-045', 18, 1, 4, 28.1, 1.9, 'Colis standard', 'Livraison 4', 'Destinataire 45', '0555000045', '2024-06-11 10:00:00', 'livre', 1072.14, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-046', 8, 1, 3, 9.4, 2.2, 'Colis standard', 'Livraison 3', 'Destinataire 46', '0555000046', '2024-06-11 10:00:00', 'livre', 721.25, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-047', 19, 1, 13, 26.9, 1.7, 'Colis standard', 'Livraison 13', 'Destinataire 47', '0555000047', '2024-06-05 10:00:00', 'livre', 1582.17, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-048', 11, 1, 7, 14.8, 1.9, 'Colis standard', 'Livraison 7', 'Destinataire 48', '0555000048', '2024-06-05 10:00:00', 'livre', 1440.39, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-049', 20, 1, 15, 16.2, 1.4, 'Colis standard', 'Livraison 15', 'Destinataire 49', '0555000049', '2024-06-05 10:00:00', 'livre', 742.15, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-050', 3, 1, 14, 12.0, 1.1, 'Colis standard', 'Livraison 14', 'Destinataire 50', '0555000050', '2024-06-09 10:00:00', 'livre', 2900.83, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-06-051', 16, 1, 11, 17.5, 1.0, 'Colis standard', 'Livraison 11', 'Destinataire 51', '0555000051', '2024-06-09 10:00:00', 'livre', 2469.2, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-06-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-052', 14, 1, 3, 23.0, 0.9, 'Colis standard', 'Livraison 3', 'Destinataire 52', '0555000052', '2024-07-07 10:00:00', 'livre', 2341.53, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-053', 10, 1, 10, 16.5, 1.7, 'Colis standard', 'Livraison 10', 'Destinataire 53', '0555000053', '2024-07-07 10:00:00', 'livre', 1140.18, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-054', 15, 1, 5, 17.3, 1.0, 'Colis standard', 'Livraison 5', 'Destinataire 54', '0555000054', '2024-07-20 10:00:00', 'livre', 2428.28, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-055', 14, 1, 11, 9.1, 1.7, 'Colis standard', 'Livraison 11', 'Destinataire 55', '0555000055', '2024-07-20 10:00:00', 'livre', 2998.54, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-056', 10, 1, 14, 23.4, 2.0, 'Colis standard', 'Livraison 14', 'Destinataire 56', '0555000056', '2024-07-20 10:00:00', 'livre', 2287.31, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-057', 2, 1, 7, 8.2, 1.1, 'Colis standard', 'Livraison 7', 'Destinataire 57', '0555000057', '2024-07-20 10:00:00', 'livre', 1849.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-058', 14, 1, 3, 12.3, 0.6, 'Colis standard', 'Livraison 3', 'Destinataire 58', '0555000058', '2024-07-17 10:00:00', 'livre', 1740.46, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-059', 7, 1, 6, 11.5, 1.3, 'Colis standard', 'Livraison 6', 'Destinataire 59', '0555000059', '2024-07-17 10:00:00', 'livre', 602.39, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-060', 2, 1, 10, 23.5, 0.8, 'Colis standard', 'Livraison 10', 'Destinataire 60', '0555000060', '2024-07-17 10:00:00', 'livre', 1097.09, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-07-061', 11, 1, 1, 23.2, 1.5, 'Colis standard', 'Livraison 1', 'Destinataire 61', '0555000061', '2024-07-17 10:00:00', 'livre', 2981.71, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-07-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-08-062', 16, 1, 11, 29.2, 1.1, 'Colis standard', 'Livraison 11', 'Destinataire 62', '0555000062', '2024-08-22 10:00:00', 'livre', 1109.29, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-08-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-08-063', 10, 1, 11, 24.5, 2.0, 'Colis standard', 'Livraison 11', 'Destinataire 63', '0555000063', '2024-08-22 10:00:00', 'livre', 2114.82, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-08-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-08-064', 8, 1, 13, 25.6, 1.6, 'Colis standard', 'Livraison 13', 'Destinataire 64', '0555000064', '2024-08-22 10:00:00', 'livre', 1644.18, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-08-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-08-065', 6, 1, 15, 25.1, 1.9, 'Colis standard', 'Livraison 15', 'Destinataire 65', '0555000065', '2024-08-22 10:00:00', 'livre', 1734.09, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-08-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-08-066', 7, 1, 7, 25.3, 0.7, 'Colis standard', 'Livraison 7', 'Destinataire 66', '0555000066', '2024-08-19 10:00:00', 'livre', 1192.61, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-08-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-08-067', 13, 1, 9, 10.7, 1.0, 'Colis standard', 'Livraison 9', 'Destinataire 67', '0555000067', '2024-08-19 10:00:00', 'livre', 2845.16, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-08-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-09-068', 15, 1, 10, 9.0, 1.4, 'Colis standard', 'Livraison 10', 'Destinataire 68', '0555000068', '2024-09-20 10:00:00', 'livre', 2381.79, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-09-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-09-069', 19, 1, 3, 14.0, 2.2, 'Colis standard', 'Livraison 3', 'Destinataire 69', '0555000069', '2024-09-20 10:00:00', 'livre', 1404.44, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-09-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-09-070', 20, 1, 3, 11.1, 2.1, 'Colis standard', 'Livraison 3', 'Destinataire 70', '0555000070', '2024-09-04 10:00:00', 'livre', 2635.86, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-09-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-09-071', 5, 1, 7, 14.7, 1.9, 'Colis standard', 'Livraison 7', 'Destinataire 71', '0555000071', '2024-09-04 10:00:00', 'livre', 2524.56, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-09-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-09-072', 15, 1, 16, 17.8, 1.0, 'Colis standard', 'Livraison 16', 'Destinataire 72', '0555000072', '2024-09-14 10:00:00', 'livre', 2005.21, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-09-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-09-073', 12, 1, 3, 29.4, 2.0, 'Colis standard', 'Livraison 3', 'Destinataire 73', '0555000073', '2024-09-14 10:00:00', 'livre', 1827.85, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-09-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-10-074', 3, 1, 2, 18.4, 2.0, 'Colis standard', 'Livraison 2', 'Destinataire 74', '0555000074', '2024-10-15 10:00:00', 'livre', 1451.46, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-10-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-10-075', 9, 1, 16, 29.0, 0.6, 'Colis standard', 'Livraison 16', 'Destinataire 75', '0555000075', '2024-10-15 10:00:00', 'livre', 729.2, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-10-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-10-076', 3, 1, 9, 16.1, 1.4, 'Colis standard', 'Livraison 9', 'Destinataire 76', '0555000076', '2024-10-06 10:00:00', 'livre', 2507.29, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-10-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-10-077', 4, 1, 15, 18.8, 1.7, 'Colis standard', 'Livraison 15', 'Destinataire 77', '0555000077', '2024-10-06 10:00:00', 'livre', 2713.53, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-10-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-11-078', 11, 1, 16, 16.7, 1.4, 'Colis standard', 'Livraison 16', 'Destinataire 78', '0555000078', '2024-11-14 10:00:00', 'livre', 2892.55, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-11-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-11-079', 2, 1, 1, 17.1, 1.6, 'Colis standard', 'Livraison 1', 'Destinataire 79', '0555000079', '2024-11-14 10:00:00', 'livre', 1741.77, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-11-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-11-080', 1, 1, 8, 17.7, 0.7, 'Colis standard', 'Livraison 8', 'Destinataire 80', '0555000080', '2024-11-21 10:00:00', 'livre', 2902.82, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-11-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-11-081', 11, 1, 8, 24.8, 2.0, 'Colis standard', 'Livraison 8', 'Destinataire 81', '0555000081', '2024-11-21 10:00:00', 'livre', 634.4, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-11-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-11-082', 7, 1, 14, 25.9, 1.9, 'Colis standard', 'Livraison 14', 'Destinataire 82', '0555000082', '2024-11-21 10:00:00', 'livre', 2141.17, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-11-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-11-083', 4, 1, 12, 15.0, 2.4, 'Colis standard', 'Livraison 12', 'Destinataire 83', '0555000083', '2024-11-21 10:00:00', 'livre', 1645.03, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-11-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-12-084', 17, 1, 4, 20.0, 2.4, 'Colis standard', 'Livraison 4', 'Destinataire 84', '0555000084', '2024-12-21 10:00:00', 'livre', 568.19, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-12-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-12-085', 20, 1, 5, 8.8, 1.9, 'Colis standard', 'Livraison 5', 'Destinataire 85', '0555000085', '2024-12-21 10:00:00', 'livre', 1665.25, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-12-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-12-086', 16, 1, 7, 28.9, 1.4, 'Colis standard', 'Livraison 7', 'Destinataire 86', '0555000086', '2024-12-21 10:00:00', 'livre', 2377.91, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-12-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-12-087', 12, 1, 1, 16.2, 1.2, 'Colis standard', 'Livraison 1', 'Destinataire 87', '0555000087', '2024-12-07 10:00:00', 'livre', 2552.95, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-12-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2024-12-088', 6, 1, 15, 25.4, 1.9, 'Colis standard', 'Livraison 15', 'Destinataire 88', '0555000088', '2024-12-07 10:00:00', 'livre', 1487.92, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2024-12-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-089', 6, 1, 4, 11.2, 2.0, 'Colis standard', 'Livraison 4', 'Destinataire 89', '0555000089', '2025-01-22 10:00:00', 'livre', 2045.03, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-090', 6, 1, 9, 18.2, 0.8, 'Colis standard', 'Livraison 9', 'Destinataire 90', '0555000090', '2025-01-22 10:00:00', 'livre', 2261.9, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-091', 8, 1, 13, 23.5, 0.9, 'Colis standard', 'Livraison 13', 'Destinataire 91', '0555000091', '2025-01-22 10:00:00', 'livre', 519.34, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-092', 3, 1, 11, 17.7, 1.1, 'Colis standard', 'Livraison 11', 'Destinataire 92', '0555000092', '2025-01-15 10:00:00', 'livre', 895.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-093', 17, 1, 7, 23.4, 2.3, 'Colis standard', 'Livraison 7', 'Destinataire 93', '0555000093', '2025-01-15 10:00:00', 'livre', 2817.76, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-094', 13, 1, 15, 24.9, 1.4, 'Colis standard', 'Livraison 15', 'Destinataire 94', '0555000094', '2025-01-15 10:00:00', 'livre', 1611.83, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-095', 12, 1, 5, 9.5, 2.0, 'Colis standard', 'Livraison 5', 'Destinataire 95', '0555000095', '2025-01-15 10:00:00', 'livre', 2088.61, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-096', 19, 1, 4, 16.2, 2.1, 'Colis standard', 'Livraison 4', 'Destinataire 96', '0555000096', '2025-01-04 10:00:00', 'livre', 888.66, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-097', 2, 1, 1, 16.4, 1.7, 'Colis standard', 'Livraison 1', 'Destinataire 97', '0555000097', '2025-01-04 10:00:00', 'livre', 2959.48, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-098', 20, 1, 13, 21.1, 1.1, 'Colis standard', 'Livraison 13', 'Destinataire 98', '0555000098', '2025-01-04 10:00:00', 'livre', 2934.55, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-099', 5, 1, 4, 10.2, 1.6, 'Colis standard', 'Livraison 4', 'Destinataire 99', '0555000099', '2025-01-04 10:00:00', 'livre', 1534.25, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-100', 5, 1, 4, 19.2, 1.4, 'Colis standard', 'Livraison 4', 'Destinataire 100', '0555000100', '2025-02-18 10:00:00', 'livre', 1739.85, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-101', 10, 1, 13, 26.9, 1.7, 'Colis standard', 'Livraison 13', 'Destinataire 101', '0555000101', '2025-02-18 10:00:00', 'livre', 1923.34, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-102', 3, 1, 9, 26.3, 1.3, 'Colis standard', 'Livraison 9', 'Destinataire 102', '0555000102', '2025-02-18 10:00:00', 'livre', 1126.06, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-103', 5, 1, 11, 25.4, 1.4, 'Colis standard', 'Livraison 11', 'Destinataire 103', '0555000103', '2025-02-18 10:00:00', 'livre', 2400.62, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-104', 15, 1, 9, 29.5, 0.8, 'Colis standard', 'Livraison 9', 'Destinataire 104', '0555000104', '2025-02-07 10:00:00', 'livre', 1600.62, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-105', 9, 1, 7, 17.8, 1.6, 'Colis standard', 'Livraison 7', 'Destinataire 105', '0555000105', '2025-02-07 10:00:00', 'livre', 1279.99, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-106', 12, 1, 10, 21.3, 1.1, 'Colis standard', 'Livraison 10', 'Destinataire 106', '0555000106', '2025-02-07 10:00:00', 'livre', 2086.64, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-107', 11, 1, 13, 11.8, 1.3, 'Colis standard', 'Livraison 13', 'Destinataire 107', '0555000107', '2025-02-07 10:00:00', 'livre', 860.84, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-108', 16, 1, 5, 10.4, 1.5, 'Colis standard', 'Livraison 5', 'Destinataire 108', '0555000108', '2025-02-07 10:00:00', 'livre', 2684.93, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-109', 5, 1, 9, 16.9, 1.5, 'Colis standard', 'Livraison 9', 'Destinataire 109', '0555000109', '2025-02-07 10:00:00', 'livre', 2933.65, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-02-110', 3, 1, 6, 8.3, 0.8, 'Colis standard', 'Livraison 6', 'Destinataire 110', '0555000110', '2025-02-07 10:00:00', 'livre', 1032.48, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-111', 3, 1, 8, 22.7, 1.9, 'Colis standard', 'Livraison 8', 'Destinataire 111', '0555000111', '2025-03-14 10:00:00', 'livre', 595.72, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-112', 5, 1, 13, 29.2, 2.2, 'Colis standard', 'Livraison 13', 'Destinataire 112', '0555000112', '2025-03-14 10:00:00', 'livre', 1099.63, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-113', 13, 1, 1, 24.8, 2.3, 'Colis standard', 'Livraison 1', 'Destinataire 113', '0555000113', '2025-03-14 10:00:00', 'livre', 2308.6, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-114', 3, 1, 4, 29.2, 1.8, 'Colis standard', 'Livraison 4', 'Destinataire 114', '0555000114', '2025-03-14 10:00:00', 'livre', 2546.37, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-115', 6, 1, 15, 16.9, 2.0, 'Colis standard', 'Livraison 15', 'Destinataire 115', '0555000115', '2025-03-24 10:00:00', 'livre', 2486.34, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-116', 19, 1, 2, 28.1, 1.5, 'Colis standard', 'Livraison 2', 'Destinataire 116', '0555000116', '2025-03-24 10:00:00', 'livre', 1659.05, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-117', 11, 1, 4, 9.7, 0.8, 'Colis standard', 'Livraison 4', 'Destinataire 117', '0555000117', '2025-03-24 10:00:00', 'livre', 1049.3, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-118', 18, 1, 11, 27.8, 0.9, 'Colis standard', 'Livraison 11', 'Destinataire 118', '0555000118', '2025-03-06 10:00:00', 'livre', 2794.62, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-03-119', 2, 1, 2, 11.2, 1.9, 'Colis standard', 'Livraison 2', 'Destinataire 119', '0555000119', '2025-03-06 10:00:00', 'livre', 1337.19, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-04-120', 2, 1, 13, 25.4, 2.0, 'Colis standard', 'Livraison 13', 'Destinataire 120', '0555000120', '2025-04-07 10:00:00', 'livre', 2067.03, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-04-121', 12, 1, 4, 18.1, 1.6, 'Colis standard', 'Livraison 4', 'Destinataire 121', '0555000121', '2025-04-07 10:00:00', 'livre', 1452.4, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-04-122', 20, 1, 2, 16.1, 1.2, 'Colis standard', 'Livraison 2', 'Destinataire 122', '0555000122', '2025-04-07 10:00:00', 'livre', 2020.63, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-04-123', 3, 1, 16, 16.5, 1.8, 'Colis standard', 'Livraison 16', 'Destinataire 123', '0555000123', '2025-04-12 10:00:00', 'livre', 1295.62, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-04-124', 20, 1, 6, 16.4, 1.6, 'Colis standard', 'Livraison 6', 'Destinataire 124', '0555000124', '2025-04-12 10:00:00', 'livre', 2186.61, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-04-125', 2, 1, 7, 25.1, 1.9, 'Colis standard', 'Livraison 7', 'Destinataire 125', '0555000125', '2025-04-07 10:00:00', 'livre', 874.41, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-04-126', 6, 1, 9, 17.9, 1.3, 'Colis standard', 'Livraison 9', 'Destinataire 126', '0555000126', '2025-04-07 10:00:00', 'livre', 1414.96, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-05-127', 19, 1, 15, 24.3, 1.3, 'Colis standard', 'Livraison 15', 'Destinataire 127', '0555000127', '2025-05-13 10:00:00', 'livre', 2141.12, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-05-128', 14, 1, 9, 26.0, 2.4, 'Colis standard', 'Livraison 9', 'Destinataire 128', '0555000128', '2025-05-13 10:00:00', 'livre', 922.05, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-05-129', 8, 1, 7, 10.7, 1.0, 'Colis standard', 'Livraison 7', 'Destinataire 129', '0555000129', '2025-05-18 10:00:00', 'livre', 1060.03, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-05-130', 11, 1, 16, 10.3, 0.7, 'Colis standard', 'Livraison 16', 'Destinataire 130', '0555000130', '2025-05-18 10:00:00', 'livre', 2376.08, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-05-131', 14, 1, 11, 19.5, 0.9, 'Colis standard', 'Livraison 11', 'Destinataire 131', '0555000131', '2025-05-09 10:00:00', 'livre', 643.76, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-05-132', 18, 1, 4, 24.7, 1.0, 'Colis standard', 'Livraison 4', 'Destinataire 132', '0555000132', '2025-05-09 10:00:00', 'livre', 2158.41, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-05-133', 16, 1, 5, 27.0, 1.8, 'Colis standard', 'Livraison 5', 'Destinataire 133', '0555000133', '2025-05-09 10:00:00', 'livre', 1189.69, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-134', 2, 1, 10, 13.8, 2.4, 'Colis standard', 'Livraison 10', 'Destinataire 134', '0555000134', '2025-06-20 10:00:00', 'livre', 1994.73, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-135', 2, 1, 16, 14.7, 0.8, 'Colis standard', 'Livraison 16', 'Destinataire 135', '0555000135', '2025-06-20 10:00:00', 'livre', 2111.14, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-136', 19, 1, 9, 11.0, 0.8, 'Colis standard', 'Livraison 9', 'Destinataire 136', '0555000136', '2025-06-20 10:00:00', 'livre', 691.4, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-137', 4, 1, 4, 10.8, 1.1, 'Colis standard', 'Livraison 4', 'Destinataire 137', '0555000137', '2025-06-20 10:00:00', 'livre', 2562.36, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-138', 6, 1, 16, 15.5, 1.6, 'Colis standard', 'Livraison 16', 'Destinataire 138', '0555000138', '2025-06-18 10:00:00', 'livre', 556.71, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-139', 13, 1, 12, 14.4, 1.9, 'Colis standard', 'Livraison 12', 'Destinataire 139', '0555000139', '2025-06-18 10:00:00', 'livre', 2394.47, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-140', 5, 1, 10, 10.7, 2.2, 'Colis standard', 'Livraison 10', 'Destinataire 140', '0555000140', '2025-06-23 10:00:00', 'livre', 1540.97, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-141', 14, 1, 4, 10.1, 1.2, 'Colis standard', 'Livraison 4', 'Destinataire 141', '0555000141', '2025-06-23 10:00:00', 'livre', 1145.65, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-06-142', 20, 1, 2, 19.1, 2.3, 'Colis standard', 'Livraison 2', 'Destinataire 142', '0555000142', '2025-06-23 10:00:00', 'livre', 1672.27, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-07-143', 4, 1, 10, 16.7, 1.5, 'Colis standard', 'Livraison 10', 'Destinataire 143', '0555000143', '2025-07-05 10:00:00', 'livre', 1385.08, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-07-144', 14, 1, 1, 24.3, 1.6, 'Colis standard', 'Livraison 1', 'Destinataire 144', '0555000144', '2025-07-05 10:00:00', 'livre', 2322.81, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-07-145', 9, 1, 15, 15.4, 2.1, 'Colis standard', 'Livraison 15', 'Destinataire 145', '0555000145', '2025-07-05 10:00:00', 'livre', 530.87, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-07-146', 7, 1, 10, 9.0, 0.7, 'Colis standard', 'Livraison 10', 'Destinataire 146', '0555000146', '2025-07-05 10:00:00', 'livre', 1688.97, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-07-147', 17, 1, 7, 22.3, 1.0, 'Colis standard', 'Livraison 7', 'Destinataire 147', '0555000147', '2025-07-05 10:00:00', 'livre', 1574.39, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-07-148', 3, 1, 6, 26.3, 1.8, 'Colis standard', 'Livraison 6', 'Destinataire 148', '0555000148', '2025-07-05 10:00:00', 'livre', 2972.47, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-07-149', 10, 1, 3, 24.4, 1.6, 'Colis standard', 'Livraison 3', 'Destinataire 149', '0555000149', '2025-07-18 10:00:00', 'livre', 2724.59, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-07-150', 8, 1, 14, 9.6, 1.5, 'Colis standard', 'Livraison 14', 'Destinataire 150', '0555000150', '2025-07-18 10:00:00', 'livre', 2352.03, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-08-151', 20, 1, 8, 27.2, 1.8, 'Colis standard', 'Livraison 8', 'Destinataire 151', '0555000151', '2025-08-06 10:00:00', 'livre', 2423.12, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-08-152', 13, 1, 8, 11.9, 1.4, 'Colis standard', 'Livraison 8', 'Destinataire 152', '0555000152', '2025-08-06 10:00:00', 'livre', 959.08, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-08-153', 17, 1, 1, 12.1, 2.2, 'Colis standard', 'Livraison 1', 'Destinataire 153', '0555000153', '2025-08-06 10:00:00', 'livre', 1603.49, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-08-154', 3, 1, 12, 23.8, 2.1, 'Colis standard', 'Livraison 12', 'Destinataire 154', '0555000154', '2025-08-18 10:00:00', 'livre', 1762.79, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-08-155', 3, 1, 10, 8.7, 2.1, 'Colis standard', 'Livraison 10', 'Destinataire 155', '0555000155', '2025-08-18 10:00:00', 'livre', 1610.29, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-08-156', 12, 1, 6, 27.6, 1.7, 'Colis standard', 'Livraison 6', 'Destinataire 156', '0555000156', '2025-08-09 10:00:00', 'livre', 893.85, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-08-157', 20, 1, 16, 16.3, 1.6, 'Colis standard', 'Livraison 16', 'Destinataire 157', '0555000157', '2025-08-09 10:00:00', 'livre', 1922.98, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-158', 4, 1, 7, 26.8, 0.9, 'Colis standard', 'Livraison 7', 'Destinataire 158', '0555000158', '2025-09-12 10:00:00', 'livre', 986.09, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-159', 4, 1, 8, 19.2, 1.2, 'Colis standard', 'Livraison 8', 'Destinataire 159', '0555000159', '2025-09-12 10:00:00', 'livre', 1918.58, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-160', 18, 1, 12, 29.6, 1.9, 'Colis standard', 'Livraison 12', 'Destinataire 160', '0555000160', '2025-09-12 10:00:00', 'livre', 2872.83, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-161', 4, 1, 6, 14.6, 0.6, 'Colis standard', 'Livraison 6', 'Destinataire 161', '0555000161', '2025-09-12 10:00:00', 'livre', 704.5, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-162', 5, 1, 16, 21.3, 1.1, 'Colis standard', 'Livraison 16', 'Destinataire 162', '0555000162', '2025-09-08 10:00:00', 'livre', 1108.42, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-163', 3, 1, 9, 17.4, 2.4, 'Colis standard', 'Livraison 9', 'Destinataire 163', '0555000163', '2025-09-08 10:00:00', 'livre', 2381.26, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-164', 5, 1, 8, 27.4, 1.8, 'Colis standard', 'Livraison 8', 'Destinataire 164', '0555000164', '2025-09-09 10:00:00', 'livre', 941.99, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-165', 2, 1, 9, 15.7, 1.9, 'Colis standard', 'Livraison 9', 'Destinataire 165', '0555000165', '2025-09-09 10:00:00', 'livre', 2727.31, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-166', 6, 1, 6, 14.4, 1.1, 'Colis standard', 'Livraison 6', 'Destinataire 166', '0555000166', '2025-09-09 10:00:00', 'livre', 1073.57, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-09-167', 1, 1, 3, 14.2, 1.6, 'Colis standard', 'Livraison 3', 'Destinataire 167', '0555000167', '2025-09-09 10:00:00', 'livre', 1065.44, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-168', 1, 1, 3, 12.2, 1.8, 'Colis standard', 'Livraison 3', 'Destinataire 168', '0555000168', '2025-10-22 10:00:00', 'livre', 706.43, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-169', 7, 1, 2, 8.8, 0.6, 'Colis standard', 'Livraison 2', 'Destinataire 169', '0555000169', '2025-10-22 10:00:00', 'livre', 1092.47, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-170', 16, 1, 7, 29.7, 1.4, 'Colis standard', 'Livraison 7', 'Destinataire 170', '0555000170', '2025-10-22 10:00:00', 'livre', 1815.81, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-171', 2, 1, 10, 10.8, 0.9, 'Colis standard', 'Livraison 10', 'Destinataire 171', '0555000171', '2025-10-14 10:00:00', 'livre', 1500.62, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-172', 18, 1, 3, 16.1, 2.2, 'Colis standard', 'Livraison 3', 'Destinataire 172', '0555000172', '2025-10-14 10:00:00', 'livre', 1995.1, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-173', 17, 1, 3, 11.1, 2.0, 'Colis standard', 'Livraison 3', 'Destinataire 173', '0555000173', '2025-10-14 10:00:00', 'livre', 1074.99, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-174', 15, 1, 9, 9.5, 0.8, 'Colis standard', 'Livraison 9', 'Destinataire 174', '0555000174', '2025-10-17 10:00:00', 'livre', 2601.74, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-175', 18, 1, 5, 23.0, 2.0, 'Colis standard', 'Livraison 5', 'Destinataire 175', '0555000175', '2025-10-17 10:00:00', 'livre', 1189.83, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-176', 5, 1, 13, 25.9, 1.3, 'Colis standard', 'Livraison 13', 'Destinataire 176', '0555000176', '2025-10-17 10:00:00', 'livre', 1419.74, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-10-177', 20, 1, 14, 27.3, 1.2, 'Colis standard', 'Livraison 14', 'Destinataire 177', '0555000177', '2025-10-17 10:00:00', 'livre', 2468.74, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-11-178', 13, 1, 9, 14.0, 2.4, 'Colis standard', 'Livraison 9', 'Destinataire 178', '0555000178', '2025-11-20 10:00:00', 'livre', 2025.2, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-11-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-11-179', 4, 1, 10, 23.9, 2.1, 'Colis standard', 'Livraison 10', 'Destinataire 179', '0555000179', '2025-11-20 10:00:00', 'livre', 1230.64, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-11-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-11-180', 6, 1, 13, 17.9, 1.9, 'Colis standard', 'Livraison 13', 'Destinataire 180', '0555000180', '2025-11-13 10:00:00', 'livre', 1111.73, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-11-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-11-181', 4, 1, 7, 12.2, 2.3, 'Colis standard', 'Livraison 7', 'Destinataire 181', '0555000181', '2025-11-13 10:00:00', 'livre', 2079.6, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-11-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-11-182', 1, 1, 10, 29.0, 1.4, 'Colis standard', 'Livraison 10', 'Destinataire 182', '0555000182', '2025-11-13 10:00:00', 'livre', 2760.11, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-11-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-11-183', 18, 1, 10, 23.3, 2.4, 'Colis standard', 'Livraison 10', 'Destinataire 183', '0555000183', '2025-11-13 10:00:00', 'livre', 2568.65, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-11-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-12-184', 2, 1, 11, 23.9, 2.4, 'Colis standard', 'Livraison 11', 'Destinataire 184', '0555000184', '2025-12-24 10:00:00', 'livre', 2601.91, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-12-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-12-185', 20, 1, 3, 14.9, 1.0, 'Colis standard', 'Livraison 3', 'Destinataire 185', '0555000185', '2025-12-24 10:00:00', 'livre', 2219.95, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-12-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-12-186', 13, 1, 5, 16.0, 1.6, 'Colis standard', 'Livraison 5', 'Destinataire 186', '0555000186', '2025-12-07 10:00:00', 'livre', 1069.29, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-12-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-12-187', 11, 1, 3, 21.0, 0.9, 'Colis standard', 'Livraison 3', 'Destinataire 187', '0555000187', '2025-12-07 10:00:00', 'livre', 1741.84, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-12-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-12-188', 3, 1, 7, 9.2, 1.3, 'Colis standard', 'Livraison 7', 'Destinataire 188', '0555000188', '2025-12-07 10:00:00', 'livre', 1498.34, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-12-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-12-189', 14, 1, 4, 11.1, 2.3, 'Colis standard', 'Livraison 4', 'Destinataire 189', '0555000189', '2025-12-07 10:00:00', 'livre', 507.92, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-12-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2026-01-190', 19, 1, 9, 18.0, 1.2, 'Colis standard', 'Livraison 9', 'Destinataire 190', '0555000190', '2026-01-19 10:00:00', 'livre', 2497.57, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2026-01-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2026-01-191', 13, 1, 4, 9.8, 1.8, 'Colis standard', 'Livraison 4', 'Destinataire 191', '0555000191', '2026-01-19 10:00:00', 'livre', 2041.68, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2026-01-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2026-01-192', 7, 1, 12, 16.9, 1.1, 'Colis standard', 'Livraison 12', 'Destinataire 192', '0555000192', '2026-01-19 10:00:00', 'livre', 1720.6, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2026-01-01'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2026-01-193', 20, 1, 8, 16.5, 1.8, 'Colis standard', 'Livraison 8', 'Destinataire 193', '0555000193', '2026-01-21 10:00:00', 'livre', 927.01, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2026-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2026-01-194', 8, 1, 15, 14.1, 1.3, 'Colis standard', 'Livraison 15', 'Destinataire 194', '0555000194', '2026-01-21 10:00:00', 'livre', 2912.77, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2026-01-02'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2026-01-195', 12, 1, 3, 19.4, 2.4, 'Colis standard', 'Livraison 3', 'Destinataire 195', '0555000195', '2026-01-18 10:00:00', 'livre', 1401.36, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2026-01-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2026-01-196', 15, 1, 8, 11.4, 1.5, 'Colis standard', 'Livraison 8', 'Destinataire 196', '0555000196', '2026-01-18 10:00:00', 'livre', 1546.29, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2026-01-03'), 1);
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2026-01-197', 1, 1, 8, 10.9, 1.0, 'Colis standard', 'Livraison 8', 'Destinataire 197', '0555000197', '2026-01-18 10:00:00', 'livre', 2442.97, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2026-01-03'), 1);

-- FACTURES ET LIENS
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202401-0001', 5, '2024-01-25', 1334.36, 253.53, 1587.89, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (1, 1);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202401-0002', 19, '2024-01-26', 1307.62, 248.45, 1556.07, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (2, 2);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202401-0003', 5, '2024-01-14', 1323.16, 251.4, 1574.56, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (3, 3);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202401-0004', 12, '2024-01-14', 1773.61, 336.98, 2110.59, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (4, 4);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202401-0005', 6, '2024-01-13', 1362.97, 258.96, 1621.93, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (5, 5);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202401-0006', 1, '2024-01-13', 2369.39, 450.18, 2819.57, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (6, 6);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0007', 18, '2024-02-26', 1546.6, 293.85, 1840.45, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (7, 7);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0008', 10, '2024-02-27', 1462.96, 277.96, 1740.92, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (8, 8);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0009', 12, '2024-02-28', 2359.0, 448.21, 2807.21, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (9, 9);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0010', 1, '2024-02-22', 2244.43, 426.44, 2670.87, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (10, 10);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0011', 18, '2024-02-23', 802.84, 152.54, 955.38, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (11, 11);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0012', 4, '2024-02-23', 883.43, 167.85, 1051.28, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (12, 12);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0013', 17, '2024-02-09', 1158.29, 220.07, 1378.36, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (13, 13);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0014', 3, '2024-02-09', 2061.6, 391.7, 2453.3, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (14, 14);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0015', 18, '2024-02-10', 543.47, 103.26, 646.73, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (15, 15);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202402-0016', 1, '2024-02-10', 737.57, 140.14, 877.71, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (16, 16);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0017', 20, '2024-03-17', 864.44, 164.24, 1028.68, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (17, 17);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0018', 10, '2024-03-17', 2003.74, 380.71, 2384.45, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (18, 18);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0019', 6, '2024-03-13', 1822.03, 346.19, 2168.22, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (19, 19);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0020', 11, '2024-03-13', 2014.87, 382.83, 2397.7, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (20, 20);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0021', 16, '2024-03-12', 1795.48, 341.14, 2136.62, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (21, 21);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0022', 1, '2024-03-21', 1753.76, 333.21, 2086.97, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (22, 22);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0023', 20, '2024-03-19', 1535.91, 291.82, 1827.73, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (23, 23);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0024', 2, '2024-03-21', 2100.7, 399.13, 2499.83, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (24, 24);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202403-0025', 5, '2024-03-21', 952.35, 180.95, 1133.3, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (25, 25);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0026', 11, '2024-04-10', 1975.78, 375.4, 2351.18, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (26, 26);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0027', 7, '2024-04-12', 876.08, 166.45, 1042.53, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (27, 27);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0028', 13, '2024-04-10', 1102.98, 209.57, 1312.55, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (28, 28);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0029', 18, '2024-04-11', 562.17, 106.81, 668.98, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (29, 29);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0030', 14, '2024-04-28', 998.03, 189.63, 1187.66, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (30, 30);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0031', 14, '2024-04-26', 1048.05, 199.13, 1247.18, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (31, 31);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0032', 7, '2024-04-26', 1777.97, 337.82, 2115.79, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (32, 32);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0033', 18, '2024-04-27', 1880.49, 357.29, 2237.78, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (33, 33);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0034', 14, '2024-04-21', 548.95, 104.3, 653.25, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (34, 34);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0035', 18, '2024-04-22', 1739.15, 330.44, 2069.59, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (35, 35);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202404-0036', 5, '2024-04-22', 1550.03, 294.5, 1844.53, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (36, 36);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202405-0037', 13, '2024-05-17', 682.78, 129.73, 812.51, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (37, 37);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202405-0038', 7, '2024-05-17', 1042.67, 198.11, 1240.78, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (38, 38);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202405-0039', 16, '2024-05-17', 1987.21, 377.57, 2364.78, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (39, 39);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202405-0040', 20, '2024-05-17', 1726.96, 328.12, 2055.08, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (40, 40);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202405-0041', 20, '2024-05-16', 1717.15, 326.26, 2043.41, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (41, 41);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202405-0042', 5, '2024-05-17', 2350.93, 446.68, 2797.61, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (42, 42);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0043', 6, '2024-06-13', 2187.66, 415.66, 2603.32, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (43, 43);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0044', 3, '2024-06-15', 1135.86, 215.81, 1351.67, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (44, 44);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0045', 18, '2024-06-13', 900.96, 171.18, 1072.14, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (45, 45);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0046', 8, '2024-06-14', 606.09, 115.16, 721.25, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (46, 46);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0047', 19, '2024-06-08', 1329.55, 252.62, 1582.17, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (47, 47);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0048', 11, '2024-06-07', 1210.41, 229.98, 1440.39, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (48, 48);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0049', 20, '2024-06-08', 623.66, 118.49, 742.15, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (49, 49);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0050', 3, '2024-06-13', 2437.67, 463.16, 2900.83, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (50, 50);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202406-0051', 16, '2024-06-12', 2074.96, 394.24, 2469.2, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (51, 51);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0052', 14, '2024-07-09', 1967.67, 373.86, 2341.53, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (52, 52);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0053', 10, '2024-07-10', 958.13, 182.05, 1140.18, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (53, 53);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0054', 15, '2024-07-24', 2040.57, 387.71, 2428.28, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (54, 54);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0055', 14, '2024-07-24', 2519.78, 478.76, 2998.54, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (55, 55);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0056', 10, '2024-07-23', 1922.11, 365.2, 2287.31, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (56, 56);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0057', 2, '2024-07-23', 1553.78, 295.22, 1849.0, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (57, 57);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0058', 14, '2024-07-21', 1462.57, 277.89, 1740.46, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (58, 58);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0059', 7, '2024-07-21', 506.21, 96.18, 602.39, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (59, 59);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0060', 2, '2024-07-21', 921.92, 175.17, 1097.09, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (60, 60);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202407-0061', 11, '2024-07-20', 2505.64, 476.07, 2981.71, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (61, 61);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202408-0062', 16, '2024-08-25', 932.18, 177.11, 1109.29, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (62, 62);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202408-0063', 10, '2024-08-24', 1777.16, 337.66, 2114.82, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (63, 63);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202408-0064', 8, '2024-08-26', 1381.66, 262.52, 1644.18, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (64, 64);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202408-0065', 6, '2024-08-24', 1457.22, 276.87, 1734.09, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (65, 65);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202408-0066', 7, '2024-08-21', 1002.19, 190.42, 1192.61, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (66, 66);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202408-0067', 13, '2024-08-23', 2390.89, 454.27, 2845.16, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (67, 67);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202409-0068', 15, '2024-09-23', 2001.5, 380.29, 2381.79, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (68, 68);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202409-0069', 19, '2024-09-23', 1180.2, 224.24, 1404.44, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (69, 69);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202409-0070', 20, '2024-09-07', 2215.01, 420.85, 2635.86, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (70, 70);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202409-0071', 5, '2024-09-07', 2121.48, 403.08, 2524.56, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (71, 71);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202409-0072', 15, '2024-09-16', 1685.05, 320.16, 2005.21, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (72, 72);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202409-0073', 12, '2024-09-16', 1536.01, 291.84, 1827.85, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (73, 73);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202410-0074', 3, '2024-10-17', 1219.71, 231.75, 1451.46, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (74, 74);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202410-0075', 9, '2024-10-18', 612.77, 116.43, 729.2, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (75, 75);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202410-0076', 3, '2024-10-08', 2106.97, 400.32, 2507.29, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (76, 76);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202410-0077', 4, '2024-10-08', 2280.28, 433.25, 2713.53, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (77, 77);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202411-0078', 11, '2024-11-17', 2430.71, 461.84, 2892.55, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (78, 78);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202411-0079', 2, '2024-11-17', 1463.67, 278.1, 1741.77, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (79, 79);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202411-0080', 1, '2024-11-25', 2439.34, 463.48, 2902.82, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (80, 80);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202411-0081', 11, '2024-11-25', 533.11, 101.29, 634.4, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (81, 81);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202411-0082', 7, '2024-11-24', 1799.3, 341.87, 2141.17, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (82, 82);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202411-0083', 4, '2024-11-25', 1382.38, 262.65, 1645.03, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (83, 83);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202412-0084', 17, '2024-12-25', 477.47, 90.72, 568.19, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (84, 84);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202412-0085', 20, '2024-12-24', 1399.37, 265.88, 1665.25, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (85, 85);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202412-0086', 16, '2024-12-23', 1998.24, 379.67, 2377.91, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (86, 86);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202412-0087', 12, '2024-12-09', 2145.34, 407.61, 2552.95, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (87, 87);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202412-0088', 6, '2024-12-09', 1250.35, 237.57, 1487.92, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (88, 88);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0089', 6, '2025-01-25', 1718.51, 326.52, 2045.03, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (89, 89);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0090', 6, '2025-01-25', 1900.76, 361.14, 2261.9, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (90, 90);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0091', 8, '2025-01-26', 436.42, 82.92, 519.34, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (91, 91);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0092', 3, '2025-01-17', 752.1, 142.9, 895.0, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (92, 92);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0093', 17, '2025-01-18', 2367.87, 449.89, 2817.76, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (93, 93);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0094', 13, '2025-01-18', 1354.48, 257.35, 1611.83, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (94, 94);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0095', 12, '2025-01-18', 1755.13, 333.48, 2088.61, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (95, 95);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0096', 19, '2025-01-08', 746.77, 141.89, 888.66, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (96, 96);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0097', 2, '2025-01-07', 2486.96, 472.52, 2959.48, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (97, 97);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0098', 20, '2025-01-06', 2466.01, 468.54, 2934.55, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (98, 98);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202501-0099', 5, '2025-01-06', 1289.29, 244.96, 1534.25, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (99, 99);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0100', 5, '2025-02-22', 1462.06, 277.79, 1739.85, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (100, 100);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0101', 10, '2025-02-21', 1616.25, 307.09, 1923.34, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (101, 101);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0102', 3, '2025-02-20', 946.27, 179.79, 1126.06, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (102, 102);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0103', 5, '2025-02-22', 2017.33, 383.29, 2400.62, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (103, 103);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0104', 15, '2025-02-09', 1345.06, 255.56, 1600.62, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (104, 104);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0105', 9, '2025-02-09', 1075.62, 204.37, 1279.99, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (105, 105);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0106', 12, '2025-02-10', 1753.48, 333.16, 2086.64, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (106, 106);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0107', 11, '2025-02-09', 723.39, 137.45, 860.84, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (107, 107);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0108', 16, '2025-02-11', 2256.24, 428.69, 2684.93, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (108, 108);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0109', 5, '2025-02-09', 2465.25, 468.4, 2933.65, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (109, 109);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202502-0110', 3, '2025-02-10', 867.63, 164.85, 1032.48, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (110, 110);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0111', 3, '2025-03-17', 500.61, 95.11, 595.72, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (111, 111);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0112', 5, '2025-03-16', 924.06, 175.57, 1099.63, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (112, 112);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0113', 13, '2025-03-18', 1940.0, 368.6, 2308.6, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (113, 113);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0114', 3, '2025-03-16', 2139.81, 406.56, 2546.37, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (114, 114);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0115', 6, '2025-03-27', 2089.36, 396.98, 2486.34, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (115, 115);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0116', 19, '2025-03-26', 1394.16, 264.89, 1659.05, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (116, 116);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0117', 11, '2025-03-28', 881.76, 167.54, 1049.3, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (117, 117);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0118', 18, '2025-03-08', 2348.42, 446.2, 2794.62, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (118, 118);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202503-0119', 2, '2025-03-09', 1123.69, 213.5, 1337.19, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (119, 119);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202504-0120', 2, '2025-04-10', 1737.0, 330.03, 2067.03, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (120, 120);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202504-0121', 12, '2025-04-11', 1220.5, 231.9, 1452.4, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (121, 121);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202504-0122', 20, '2025-04-09', 1698.01, 322.62, 2020.63, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (122, 122);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202504-0123', 3, '2025-04-14', 1088.76, 206.86, 1295.62, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (123, 123);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202504-0124', 20, '2025-04-15', 1837.49, 349.12, 2186.61, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (124, 124);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202504-0125', 2, '2025-04-09', 734.8, 139.61, 874.41, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (125, 125);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202504-0126', 6, '2025-04-11', 1189.04, 225.92, 1414.96, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (126, 126);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202505-0127', 19, '2025-05-15', 1799.26, 341.86, 2141.12, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (127, 127);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202505-0128', 14, '2025-05-16', 774.83, 147.22, 922.05, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (128, 128);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202505-0129', 8, '2025-05-20', 890.78, 169.25, 1060.03, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (129, 129);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202505-0130', 11, '2025-05-20', 1996.71, 379.37, 2376.08, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (130, 130);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202505-0131', 14, '2025-05-12', 540.97, 102.79, 643.76, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (131, 131);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202505-0132', 18, '2025-05-11', 1813.79, 344.62, 2158.41, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (132, 132);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202505-0133', 16, '2025-05-11', 999.74, 189.95, 1189.69, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (133, 133);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0134', 2, '2025-06-22', 1676.24, 318.49, 1994.73, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (134, 134);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0135', 2, '2025-06-22', 1774.07, 337.07, 2111.14, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (135, 135);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0136', 19, '2025-06-24', 581.01, 110.39, 691.4, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (136, 136);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0137', 4, '2025-06-23', 2153.24, 409.12, 2562.36, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (137, 137);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0138', 6, '2025-06-20', 467.82, 88.89, 556.71, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (138, 138);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0139', 13, '2025-06-20', 2012.16, 382.31, 2394.47, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (139, 139);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0140', 5, '2025-06-26', 1294.93, 246.04, 1540.97, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (140, 140);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0141', 14, '2025-06-27', 962.73, 182.92, 1145.65, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (141, 141);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202506-0142', 20, '2025-06-26', 1405.27, 267.0, 1672.27, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (142, 142);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202507-0143', 4, '2025-07-07', 1163.93, 221.15, 1385.08, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (143, 143);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202507-0144', 14, '2025-07-09', 1951.94, 370.87, 2322.81, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (144, 144);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202507-0145', 9, '2025-07-07', 446.11, 84.76, 530.87, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (145, 145);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202507-0146', 7, '2025-07-08', 1419.3, 269.67, 1688.97, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (146, 146);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202507-0147', 17, '2025-07-09', 1323.02, 251.37, 1574.39, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (147, 147);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202507-0148', 3, '2025-07-07', 2497.87, 474.6, 2972.47, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (148, 148);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202507-0149', 10, '2025-07-21', 2289.57, 435.02, 2724.59, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (149, 149);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202507-0150', 8, '2025-07-20', 1976.5, 375.53, 2352.03, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (150, 150);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202508-0151', 20, '2025-08-10', 2036.24, 386.88, 2423.12, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (151, 151);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202508-0152', 13, '2025-08-09', 805.95, 153.13, 959.08, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (152, 152);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202508-0153', 17, '2025-08-10', 1347.47, 256.02, 1603.49, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (153, 153);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202508-0154', 3, '2025-08-22', 1481.34, 281.45, 1762.79, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (154, 154);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202508-0155', 3, '2025-08-21', 1353.18, 257.11, 1610.29, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (155, 155);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202508-0156', 12, '2025-08-12', 751.13, 142.72, 893.85, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (156, 156);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202508-0157', 20, '2025-08-11', 1615.95, 307.03, 1922.98, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (157, 157);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0158', 4, '2025-09-16', 828.65, 157.44, 986.09, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (158, 158);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0159', 4, '2025-09-16', 1612.25, 306.33, 1918.58, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (159, 159);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0160', 18, '2025-09-15', 2414.14, 458.69, 2872.83, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (160, 160);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0161', 4, '2025-09-15', 592.02, 112.48, 704.5, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (161, 161);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0162', 5, '2025-09-12', 931.45, 176.97, 1108.42, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (162, 162);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0163', 3, '2025-09-10', 2001.06, 380.2, 2381.26, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (163, 163);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0164', 5, '2025-09-13', 791.59, 150.4, 941.99, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (164, 164);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0165', 2, '2025-09-11', 2291.86, 435.45, 2727.31, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (165, 165);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0166', 6, '2025-09-12', 902.16, 171.41, 1073.57, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (166, 166);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202509-0167', 1, '2025-09-12', 895.33, 170.11, 1065.44, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (167, 167);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0168', 1, '2025-10-25', 593.64, 112.79, 706.43, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (168, 168);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0169', 7, '2025-10-24', 918.04, 174.43, 1092.47, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (169, 169);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0170', 16, '2025-10-24', 1525.89, 289.92, 1815.81, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (170, 170);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0171', 2, '2025-10-18', 1261.03, 239.59, 1500.62, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (171, 171);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0172', 18, '2025-10-16', 1676.55, 318.55, 1995.1, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (172, 172);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0173', 17, '2025-10-17', 903.35, 171.64, 1074.99, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (173, 173);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0174', 15, '2025-10-19', 2186.34, 415.4, 2601.74, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (174, 174);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0175', 18, '2025-10-19', 999.86, 189.97, 1189.83, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (175, 175);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0176', 5, '2025-10-21', 1193.06, 226.68, 1419.74, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (176, 176);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202510-0177', 20, '2025-10-19', 2074.57, 394.17, 2468.74, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (177, 177);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202511-0178', 13, '2025-11-22', 1701.85, 323.35, 2025.2, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (178, 178);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202511-0179', 4, '2025-11-22', 1034.15, 196.49, 1230.64, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (179, 179);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202511-0180', 6, '2025-11-15', 934.23, 177.5, 1111.73, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (180, 180);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202511-0181', 4, '2025-11-17', 1747.56, 332.04, 2079.6, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (181, 181);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202511-0182', 1, '2025-11-17', 2319.42, 440.69, 2760.11, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (182, 182);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202511-0183', 18, '2025-11-16', 2158.53, 410.12, 2568.65, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (183, 183);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202512-0184', 2, '2025-12-28', 2186.48, 415.43, 2601.91, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (184, 184);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202512-0185', 20, '2025-12-26', 1865.5, 354.45, 2219.95, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (185, 185);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202512-0186', 13, '2025-12-10', 898.56, 170.73, 1069.29, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (186, 186);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202512-0187', 11, '2025-12-10', 1463.73, 278.11, 1741.84, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (187, 187);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202512-0188', 3, '2025-12-09', 1259.11, 239.23, 1498.34, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (188, 188);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202512-0189', 14, '2025-12-09', 426.82, 81.1, 507.92, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (189, 189);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202601-0190', 19, '2026-01-21', 2098.8, 398.77, 2497.57, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (190, 190);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202601-0191', 13, '2026-01-23', 1715.7, 325.98, 2041.68, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (191, 191);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202601-0192', 7, '2026-01-23', 1445.88, 274.72, 1720.6, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (192, 192);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202601-0193', 20, '2026-01-24', 779.0, 148.01, 927.01, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (193, 193);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202601-0194', 8, '2026-01-25', 2447.71, 465.06, 2912.77, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (194, 194);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202601-0195', 12, '2026-01-21', 1177.61, 223.75, 1401.36, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (195, 195);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202601-0196', 15, '2026-01-21', 1299.4, 246.89, 1546.29, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (196, 196);
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-202601-0197', 1, '2026-01-21', 2052.92, 390.05, 2442.97, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (197, 197);

-- PAIEMENTS
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(2, 19, '2024-02-06', 'Virement', 1556.07, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(3, 5, '2024-01-22', 'EspÃ¨ces', 1038.57, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(4, 12, '2024-01-20', 'EspÃ¨ces', 1126.91, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(5, 6, '2024-01-27', 'EspÃ¨ces', 1621.93, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(6, 1, '2024-01-16', 'EspÃ¨ces', 2819.57, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(7, 18, '2024-03-03', 'Virement', 1840.45, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(8, 10, '2024-03-08', 'ChÃ¨que', 1740.92, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(9, 12, '2024-03-02', 'ChÃ¨que', 2807.21, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(11, 18, '2024-03-03', 'EspÃ¨ces', 955.38, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(12, 4, '2024-02-26', 'Virement', 1051.28, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(13, 17, '2024-02-14', 'EspÃ¨ces', 1378.36, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(15, 18, '2024-02-24', 'ChÃ¨que', 646.73, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(16, 1, '2024-02-13', 'EspÃ¨ces', 877.71, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(18, 10, '2024-04-01', 'ChÃ¨que', 2384.45, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(19, 6, '2024-03-19', 'Virement', 2168.22, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(21, 16, '2024-03-23', 'ChÃ¨que', 1587.02, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(22, 1, '2024-04-01', 'ChÃ¨que', 2086.97, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(23, 20, '2024-03-29', 'ChÃ¨que', 1827.73, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(24, 2, '2024-04-03', 'EspÃ¨ces', 2499.83, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(26, 11, '2024-04-24', 'EspÃ¨ces', 1467.12, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(28, 13, '2024-04-25', 'ChÃ¨que', 1312.55, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(29, 18, '2024-04-22', 'EspÃ¨ces', 668.98, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(31, 14, '2024-05-07', 'EspÃ¨ces', 1247.18, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(32, 7, '2024-05-03', 'Virement', 2115.79, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(33, 18, '2024-05-09', 'ChÃ¨que', 2237.78, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(34, 14, '2024-04-26', 'EspÃ¨ces', 653.25, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(35, 18, '2024-04-28', 'Virement', 2069.59, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(36, 5, '2024-04-27', 'EspÃ¨ces', 1844.53, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(37, 13, '2024-05-23', 'EspÃ¨ces', 812.51, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(38, 7, '2024-05-20', 'Virement', 1240.78, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(40, 20, '2024-05-31', 'ChÃ¨que', 2055.08, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(41, 20, '2024-05-30', 'ChÃ¨que', 979.61, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(45, 18, '2024-06-19', 'EspÃ¨ces', 1072.14, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(46, 8, '2024-06-29', 'ChÃ¨que', 518.59, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(47, 19, '2024-06-13', 'Virement', 1582.17, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(48, 11, '2024-06-21', 'EspÃ¨ces', 1440.39, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(49, 20, '2024-06-20', 'EspÃ¨ces', 742.15, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(50, 3, '2024-06-19', 'Virement', 2900.83, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(51, 16, '2024-06-20', 'Virement', 1352.23, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(52, 14, '2024-07-13', 'ChÃ¨que', 2341.53, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(53, 10, '2024-07-24', 'EspÃ¨ces', 704.79, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(54, 15, '2024-08-07', 'ChÃ¨que', 2428.28, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(55, 14, '2024-08-04', 'Virement', 2998.54, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(56, 10, '2024-07-31', 'ChÃ¨que', 2287.31, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(57, 2, '2024-08-02', 'EspÃ¨ces', 1849.0, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(58, 14, '2024-08-02', 'Virement', 719.32, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(59, 7, '2024-07-24', 'Virement', 602.39, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(60, 2, '2024-08-01', 'Virement', 1097.09, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(61, 11, '2024-07-29', 'Virement', 2263.74, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(62, 16, '2024-08-29', 'EspÃ¨ces', 1109.29, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(63, 10, '2024-08-29', 'ChÃ¨que', 1398.67, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(64, 8, '2024-09-06', 'EspÃ¨ces', 1644.18, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(65, 6, '2024-09-06', 'Virement', 1734.09, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(66, 7, '2024-09-03', 'Virement', 774.27, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(67, 13, '2024-08-31', 'ChÃ¨que', 2845.16, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(68, 15, '2024-10-02', 'Virement', 1454.95, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(69, 19, '2024-09-27', 'EspÃ¨ces', 1404.44, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(70, 20, '2024-09-13', 'Virement', 2635.86, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(71, 5, '2024-09-13', 'ChÃ¨que', 2524.56, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(72, 15, '2024-09-24', 'ChÃ¨que', 2005.21, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(74, 3, '2024-10-29', 'ChÃ¨que', 665.5, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(75, 9, '2024-10-29', 'EspÃ¨ces', 729.2, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(76, 3, '2024-10-16', 'EspÃ¨ces', 2507.29, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(77, 4, '2024-10-22', 'EspÃ¨ces', 2713.53, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(78, 11, '2024-11-26', 'Virement', 2892.55, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(79, 2, '2024-11-25', 'ChÃ¨que', 1741.77, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(80, 1, '2024-11-29', 'ChÃ¨que', 2902.82, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(81, 11, '2024-11-28', 'EspÃ¨ces', 634.4, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(82, 7, '2024-11-27', 'EspÃ¨ces', 2141.17, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(83, 4, '2024-12-06', 'EspÃ¨ces', 1645.03, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(84, 17, '2025-01-04', 'Virement', 568.19, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(85, 20, '2025-01-07', 'EspÃ¨ces', 1665.25, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(87, 12, '2024-12-21', 'EspÃ¨ces', 2552.95, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(88, 6, '2024-12-17', 'Virement', 1487.92, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(89, 6, '2025-02-04', 'ChÃ¨que', 2045.03, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(90, 6, '2025-02-08', 'EspÃ¨ces', 2261.9, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(91, 8, '2025-01-30', 'ChÃ¨que', 400.06, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(92, 3, '2025-01-23', 'Virement', 895.0, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(93, 17, '2025-01-23', 'Virement', 2817.76, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(96, 19, '2025-01-18', 'EspÃ¨ces', 888.66, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(97, 2, '2025-01-10', 'ChÃ¨que', 2959.48, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(98, 20, '2025-01-12', 'EspÃ¨ces', 2934.55, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(99, 5, '2025-01-21', 'Virement', 649.35, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(101, 10, '2025-03-05', 'EspÃ¨ces', 1095.77, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(102, 3, '2025-03-02', 'Virement', 1126.06, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(103, 5, '2025-03-04', 'ChÃ¨que', 2400.62, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(105, 9, '2025-02-18', 'ChÃ¨que', 1012.13, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(107, 11, '2025-02-16', 'Virement', 860.84, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(109, 5, '2025-02-15', 'Virement', 1396.32, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(110, 3, '2025-02-15', 'Virement', 567.43, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(111, 3, '2025-03-24', 'ChÃ¨que', 595.72, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(112, 5, '2025-03-25', 'EspÃ¨ces', 1099.63, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(114, 3, '2025-03-21', 'Virement', 2546.37, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(115, 6, '2025-04-10', 'Virement', 2486.34, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(116, 19, '2025-04-02', 'EspÃ¨ces', 1659.05, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(117, 11, '2025-04-03', 'Virement', 1049.3, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(119, 2, '2025-03-21', 'ChÃ¨que', 1337.19, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(121, 12, '2025-04-18', 'EspÃ¨ces', 1452.4, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(124, 20, '2025-04-18', 'ChÃ¨que', 2186.61, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(125, 2, '2025-04-24', 'EspÃ¨ces', 874.41, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(126, 6, '2025-04-14', 'ChÃ¨que', 1414.96, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(127, 19, '2025-05-27', 'EspÃ¨ces', 2141.12, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(128, 14, '2025-05-26', 'Virement', 922.05, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(130, 11, '2025-05-24', 'ChÃ¨que', 2376.08, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(131, 14, '2025-05-23', 'EspÃ¨ces', 643.76, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(132, 18, '2025-05-14', 'ChÃ¨que', 1148.36, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(133, 16, '2025-05-25', 'Virement', 1189.69, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(134, 2, '2025-06-25', 'Virement', 1994.73, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(135, 2, '2025-07-04', 'EspÃ¨ces', 2111.14, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(136, 19, '2025-06-28', 'EspÃ¨ces', 691.4, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(137, 4, '2025-06-28', 'Virement', 2562.36, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(138, 6, '2025-07-01', 'Virement', 556.71, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(139, 13, '2025-06-30', 'EspÃ¨ces', 2394.47, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(140, 5, '2025-07-03', 'ChÃ¨que', 1540.97, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(141, 14, '2025-07-05', 'ChÃ¨que', 1145.65, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(142, 20, '2025-07-04', 'EspÃ¨ces', 1672.27, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(143, 4, '2025-07-13', 'Virement', 1385.08, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(144, 14, '2025-07-12', 'ChÃ¨que', 2322.81, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(145, 9, '2025-07-14', 'ChÃ¨que', 530.87, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(146, 7, '2025-07-22', 'EspÃ¨ces', 1688.97, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(147, 17, '2025-07-17', 'EspÃ¨ces', 1574.39, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(148, 3, '2025-07-13', 'ChÃ¨que', 2972.47, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(149, 10, '2025-07-24', 'EspÃ¨ces', 2026.85, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(150, 8, '2025-07-30', 'ChÃ¨que', 1732.71, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(151, 20, '2025-08-14', 'Virement', 2423.12, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(152, 13, '2025-08-15', 'Virement', 959.08, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(153, 17, '2025-08-20', 'ChÃ¨que', 1603.49, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(155, 3, '2025-08-25', 'Virement', 1610.29, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(156, 12, '2025-08-23', 'EspÃ¨ces', 893.85, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(157, 20, '2025-08-21', 'ChÃ¨que', 1922.98, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(159, 4, '2025-10-01', 'ChÃ¨que', 1918.58, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(161, 4, '2025-09-25', 'Virement', 704.5, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(162, 5, '2025-09-24', 'Virement', 1108.42, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(163, 3, '2025-09-18', 'Virement', 2381.26, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(164, 5, '2025-09-21', 'EspÃ¨ces', 648.63, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(166, 6, '2025-09-25', 'EspÃ¨ces', 535.69, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(168, 1, '2025-11-03', 'Virement', 706.43, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(169, 7, '2025-11-03', 'EspÃ¨ces', 1092.47, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(170, 16, '2025-10-31', 'EspÃ¨ces', 1815.81, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(171, 2, '2025-10-30', 'ChÃ¨que', 1500.62, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(172, 18, '2025-10-21', 'EspÃ¨ces', 1995.1, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(174, 15, '2025-10-29', 'ChÃ¨que', 2601.74, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(175, 18, '2025-11-01', 'Virement', 1189.83, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(177, 20, '2025-10-26', 'EspÃ¨ces', 2468.74, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(179, 4, '2025-11-29', 'ChÃ¨que', 1230.64, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(181, 4, '2025-11-22', 'Virement', 2079.6, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(182, 1, '2025-11-27', 'Virement', 2760.11, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(183, 18, '2025-11-20', 'EspÃ¨ces', 1358.91, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(184, 2, '2026-01-04', 'ChÃ¨que', 2601.91, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(185, 20, '2025-12-31', 'ChÃ¨que', 2219.95, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(186, 13, '2025-12-19', 'ChÃ¨que', 1069.29, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(187, 11, '2025-12-17', 'Virement', 1741.84, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(188, 3, '2025-12-22', 'Virement', 1498.34, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(189, 14, '2025-12-19', 'Virement', 507.92, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(192, 7, '2026-02-02', 'Virement', 1720.6, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(193, 20, '2026-02-06', 'EspÃ¨ces', 927.01, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(194, 8, '2026-01-28', 'ChÃ¨que', 2912.77, 'ValidÃ©');
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES
(197, 1, '2026-02-05', 'Virement', 2442.97, 'ValidÃ©');

-- Statistiques:
-- Total tournÃ©es: 67
-- Total expÃ©ditions: 197
-- Total factures: 197
-- Total paiements: 158
-- ============================================
-- COMPLÃ‰MENTS : INTERNATIONAL + RÃ‰CLAMATIONS + ALERTES
-- ============================================

-- ============================================
-- 1. DESTINATIONS INTERNATIONALES
-- ============================================

-- Maghreb
INSERT INTO destination (pays, ville, zone_geographique, code_zone, tarif_base_defaut, is_active, latitude, longitude) VALUES
('Maroc', 'Casablanca', 'International', 'INT-MA001', 8000.00, 1, 33.5731, -7.5898),
('Maroc', 'Rabat', 'International', 'INT-MA002', 8000.00, 1, 34.0209, -6.8416),
('Tunisie', 'Tunis', 'International', 'INT-TN001', 7500.00, 1, 36.8065, 10.1815),
('Tunisie', 'Sfax', 'International', 'INT-TN002', 7500.00, 1, 34.7406, 10.7603),
('Libye', 'Tripoli', 'International', 'INT-LY001', 9000.00, 1, 32.8872, 13.1913);

-- Union EuropÃ©enne  
INSERT INTO destination (pays, ville, zone_geographique, code_zone, tarif_base_defaut, is_active, latitude, longitude) VALUES
('France', 'Paris', 'International', 'INT-FR001', 15000.00, 1, 48.8566, 2.3522),
('France', 'Marseille', 'International', 'INT-FR002', 15000.00, 1, 43.2965, 5.3698),
('France', 'Lyon', 'International', 'INT-FR003', 15000.00, 1, 45.7640, 4.8357),
('Espagne', 'Barcelone', 'International', 'INT-ES001', 16000.00, 1, 41.3851, 2.1734),
('Italie', 'Milan', 'International', 'INT-IT001', 16500.00, 1, 45.4642, 9.1900);

-- ============================================
-- 2. EXPÃ‰DITIONS INTERNATIONALES
-- ============================================

-- ExpÃ©ditions vers le Maghreb (2024-2025)
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-INT-2024-001', 11, 3, 17, 45.0, 3.5, 'Ã‰quipements informatiques', 'Casablanca Centre', 'STE TechMaroc', '+212522334455', '2024-03-10 10:00:00', 'livre', 9500.00, 1, NULL, 1),
('EXP-INT-2024-002', 12, 3, 19, 38.0, 2.8, 'PiÃ¨ces automobiles', 'Tunis Industriel', 'AutoTunis SARL', '+216712345678', '2024-05-15 09:00:00', 'livre', 8800.00, 1, NULL, 1),
('EXP-INT-2024-003', 13, 3, 18, 52.0, 4.0, 'MatÃ©riel mÃ©dical', 'Rabat Medical Center', 'Clinique Al Amal', '+212537445566', '2024-08-20 11:00:00', 'livre', 9200.00, 1, NULL, 1),
('EXP-INT-2024-004', 17, 3, 20, 41.0, 3.2, 'Composants Ã©lectroniques', 'Sfax Zone Industrielle', 'ElecTun SPA', '+216742233445', '2024-11-05 10:30:00', 'livre', 8600.00, 1, NULL, 1);

-- ExpÃ©ditions vers l'Union EuropÃ©enne (2024-2025)
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-INT-2024-005', 19, 3, 22, 65.0, 5.0, 'Produits artisanaux', 'Paris 11Ã¨me', 'Galerie Maghreb Art', '+33142556677', '2024-04-12 14:00:00', 'livre', 17500.00, 1, NULL, 1),
('EXP-INT-2024-006', 14, 3, 23, 58.0, 4.5, 'Textiles', 'Marseille Port', 'Import Med SARL', '+33491334455', '2024-06-25 10:00:00', 'livre', 16800.00, 1, NULL, 1),
('EXP-INT-2025-007', 15, 3, 24, 72.0, 5.5, 'Produits pharmaceutiques', 'Lyon Gerland', 'PharmaEU SAS', '+33478223344', '2025-02-18 09:30:00', 'livre', 18200.00, 1, NULL, 1),
('EXP-INT-2025-008', 18, 3, 25, 50.0, 4.0, 'Ã‰quipements industriels', 'Barcelone Zona Franca', 'IndustriaES SA', '+34932445566', '2025-05-22 11:00:00', 'livre', 18500.00, 1, NULL, 1),
('EXP-INT-2025-009', 16, 3, 26, 68.0, 5.2, 'Machines agricoles', 'Milano Sud', 'AgroItalia SpA', '+390223344556', '2025-08-14 10:00:00', 'livre', 19200.00, 1, NULL, 1),
('EXP-INT-2025-010', 11, 3, 21, 35.0, 2.5, 'Documentation technique', 'Tripoli Centre', 'Engineering Libya', '+218912334455', '2025-10-30 15:00:00', 'livre', 10500.00, 1, NULL, 1);

-- ============================================
-- 3. FACTURES POUR EXPÃ‰DITIONS INTERNATIONALES
-- ============================================

-- Factures Maghreb 2024
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202403-001', 11, '2024-03-15', 7983.19, 1516.81, 9500.00, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (198, 198);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(198, 11, '2024-03-25', 'Virement', 9500.00, 'ValidÃ©');

INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202405-002', 12, '2024-05-20', 7394.96, 1405.04, 8800.00, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (199, 199);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(199, 12, '2024-06-05', 'Virement', 8800.00, 'ValidÃ©');

INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202408-003', 13, '2024-08-25', 7731.09, 1468.91, 9200.00, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (200, 200);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(200, 13, '2024-09-10', 'Virement', 5500.00, 'ValidÃ©');

INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202411-004', 17, '2024-11-10', 7226.89, 1373.11, 8600.00, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (201, 201);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(201, 17, '2024-11-22', 'Virement', 8600.00, 'ValidÃ©');

-- Factures UE 2024
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202404-005', 19, '2024-04-18', 14705.88, 2794.12, 17500.00, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (202, 202);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(202, 19, '2024-05-02', 'Virement', 17500.00, 'ValidÃ©');

INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202406-006', 14, '2024-06-30', 14117.65, 2682.35, 16800.00, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (203, 203);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(203, 14, '2024-07-15', 'Virement', 16800.00, 'ValidÃ©');

-- Factures UE 2025
INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202502-007', 15, '2025-02-23', 15294.12, 2905.88, 18200.00, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (204, 204);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(204, 15, '2025-03-08', 'Virement', 18200.00, 'ValidÃ©');

INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202505-008', 18, '2025-05-27', 15546.22, 2953.78, 18500.00, 'impayee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (205, 205);

INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202508-009', 16, '2025-08-19', 16134.45, 3065.55, 19200.00, 'partiellement_payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (206, 206);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(206, 16, '2025-09-05', 'Virement', 12000.00, 'ValidÃ©');

INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES
('FACT-INT-202511-010', 11, '2025-11-05', 8823.53, 1676.47, 10500.00, 'payee');
INSERT INTO facture_expedition (facture_id, expedition_id) VALUES (207, 207);
INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut) VALUES 
(207, 11, '2025-11-18', 'Virement', 10500.00, 'ValidÃ©');

-- ============================================
-- 4. INCIDENTS
-- ============================================

INSERT INTO incident (code_incident, type_incident, expedition_id, tournee_id, commentaire, action_appliquee, notify_direction, notify_client, created_by, created_at) VALUES 
('INC-20240315-001', 'RETARD', 15, NULL, 'Retard dÃ» aux conditions mÃ©tÃ©orologiques', 'NONE', 1, 1, 1, '2024-03-15 14:30:00'),
('INC-20240622-002', 'ENDOMMAGEMENT', 42, NULL, 'Carton endommagÃ© lors du chargement', 'REMBOURSEMENT', 1, 1, 1, '2024-06-22 09:15:00'),
('INC-20240918-003', 'PERTE', 68, NULL, 'Colis Ã©garÃ© en transit', 'REMBOURSEMENT', 1, 1, 1, '2024-09-18 16:45:00'),
('INC-20250225-004', 'RETARD', 105, NULL, 'Retard de 2 jours - problÃ¨me vÃ©hicule', 'NONE', 1, 1, 1, '2025-02-25 11:20:00'),
('INC-20250508-005', 'ENDOMMAGEMENT', 128, NULL, 'Emballage insuffisant - produit cassÃ©', 'REMBOURSEMENT_PARTIEL', 1, 1, 1, '2025-05-08 13:40:00'),
('INC-20250715-006', 'ADRESSE_INCORRECTE', 148, NULL, 'Adresse incomplÃ¨te - retour expÃ©diteur', 'NONE', 0, 1, 1, '2025-07-15 10:00:00'),
('INC-20250923-007', 'RETARD', 172, NULL, 'Retard douanier - frontiÃ¨re', 'NONE', 1, 1, 1, '2025-09-23 15:30:00'),
('INC-INT-20250814-008', 'DOUANE', 206, NULL, 'ProblÃ¨me documentation douaniÃ¨re Milan', 'NONE', 1, 1, 1, '2025-08-14 08:00:00');

-- ============================================
-- 5. RÃ‰CLAMATIONS
-- ============================================

INSERT INTO reclamation (client_id, objet, description, date_reclamation, statut, expedition_id, facture_id, type_service_id, traite_par, date_resolution) VALUES
(3, 'Retard de livraison', 'Colis reÃ§u avec 3 jours de retard par rapport Ã  la date prÃ©vue', '2024-03-18', 'resolu', 15, NULL, 1, 1, '2024-03-20'),
(8, 'Colis endommagÃ©', 'Emballage dÃ©tÃ©riorÃ©, contenu partiellement endommagÃ©', '2024-06-25', 'resolu', 42, NULL, 1, 2, '2024-06-28'),
(15, 'Colis perdu', 'Aucune nouvelle du colis depuis 10 jours', '2024-09-20', 'resolu', 68, NULL, 1, 1, '2024-09-25'),
(11, 'Facturation incorrecte', 'Montant facturÃ© supÃ©rieur au devis initial', '2024-11-15', 'en_cours', NULL, 78, 1, 3, NULL),
(5, 'Service client', 'DifficultÃ© Ã  joindre le service client par tÃ©lÃ©phone', '2025-02-28', 'resolu', NULL, NULL, NULL, 2, '2025-03-02'),
(13, 'Retard chronique', 'TroisiÃ¨me retard consÃ©cutif sur nos expÃ©ditions', '2025-05-12', 'en_cours', 128, NULL, 1, 1, NULL),
(20, 'Adresse erronÃ©e', 'Livraison effectuÃ©e Ã  une mauvaise adresse', '2025-07-18', 'resolu', 148, NULL, 1, 2, '2025-07-20'),
(16, 'ProblÃ¨me douanier', 'DÃ©lai excessif pour dÃ©douanement Ã  Milan', '2025-08-16', 'resolu', 206, 206, 3, 1, '2025-08-22'),
(7, 'Prix international', 'Demande de rÃ©duction sur les frais internationaux', '2025-11-10', 'en_cours', NULL, NULL, 3, 3, NULL);

-- ============================================
-- 6. LIENS RÃ‰CLAMATION-EXPÃ‰DITION
-- ============================================

INSERT INTO reclamation_expedition (reclamation_id, expedition_id) VALUES
(1, 15),
(2, 42),
(3, 68),
(6, 128),
(7, 148),
(8, 206);

-- ============================================
-- 7. ALERTES
-- ============================================

INSERT INTO alerte (type_alerte, destination, titre, message, incident_id, expedition_id, tournee_id, is_read, created_at) VALUES
('incident', 'direction', 'Nouveau incident - Retard livraison', 'Un incident de type RETARD a Ã©tÃ© signalÃ© pour l''expÃ©dition EXP-2024-01-015', 1, 15, NULL, 1, '2024-03-15 14:30:00'),
('incident', 'client', 'Incident sur votre expÃ©dition', 'Votre colis a subi un retard. Nous nous excusons pour ce dÃ©sagrÃ©ment.', 1, 15, NULL, 1, '2024-03-15 14:31:00'),

('incident', 'direction', 'Incident grave - Colis endommagÃ©', 'Endommagement signalÃ© sur expÃ©dition EXP-2024-04-042 - Action requise', 2, 42, NULL, 1, '2024-06-22 09:15:00'),
('incident', 'client', 'Dommage sur votre colis', 'Votre colis a Ã©tÃ© endommagÃ©. Notre Ã©quipe vous contactera sous 24h.', 2, 42, NULL, 1, '2024-06-22 09:20:00'),

('incident', 'direction', 'URGENT - Colis perdu', 'Perte de colis signalÃ©e - EXP-2024-09-068 - Investigation immÃ©diate', 3, 68, NULL, 1, '2024-09-18 16:45:00'),
('incident', 'client', 'Recherche de votre colis', 'Nous recherchons activement votre colis. Suivi en cours.', 3, 68, NULL, 1, '2024-09-18 17:00:00'),

('reclamation', 'service_client', 'Nouvelle rÃ©clamation', 'RÃ©clamation client nÂ°4 - Facturation incorrecte', NULL, NULL, NULL, 0, '2024-11-15 10:00:00'),

('incident', 'direction', 'Retard expÃ©dition', 'Retard de 2 jours sur EXP-2025-02-105', 4, 105, NULL, 1, '2025-02-25 11:20:00'),

('incident', 'direction', 'Colis endommagÃ© - Remboursement partiel', 'Dommage partiel sur EXP-2025-05-128 - Remboursement Ã  effectuer', 5, 128, NULL, 0, '2025-05-08 13:40:00'),
('incident', 'client', 'Compensation pour dommage', 'Suite au dommage constatÃ©, un remboursement partiel sera effectuÃ©.', 5, 128, NULL, 1, '2025-05-08 14:00:00'),

('reclamation', 'service_client', 'RÃ©clamation - Retards rÃ©pÃ©tÃ©s', 'Client mÃ©content - Retards chroniques sur compte entreprise', NULL, NULL, NULL, 0, '2025-05-12 09:00:00'),

('incident', 'direction', 'ProblÃ¨me adresse', 'Adresse incomplÃ¨te - Retour expÃ©diteur EXP-2025-07-148', 6, 148, NULL, 1, '2025-07-15 10:00:00'),

('incident', 'direction', 'Retard douanier - International', 'Retard au passage de la frontiÃ¨re - EXP-2025-09-172', 7, 172, NULL, 0, '2025-09-23 15:30:00'),

('incident', 'direction', 'URGENT - ProblÃ¨me douane Milan', 'Documentation douaniÃ¨re incomplÃ¨te - Blocage Ã  Milan', 8, 206, NULL, 0, '2025-08-14 08:00:00'),
('incident', 'client', 'DÃ©lai douanier', 'Votre expÃ©dition est en attente de dÃ©douanement. DÃ©lai estimÃ©: 2-3 jours.', 8, 206, NULL, 1, '2025-08-14 09:00:00'),

('reclamation', 'commercial', 'Demande rÃ©duction tarifaire', 'Client demande rÃ©vision des tarifs internationaux', NULL, NULL, NULL, 0, '2025-11-10 11:00:00');

-- ============================================
-- 8. PIÃˆCES JOINTES INCIDENTS (exemples)
-- ============================================

INSERT INTO incident_attachment (incident_id, file, original_name, uploaded_by, uploaded_at) VALUES
(2, 'incident_2_photo1.jpg', 'colis_endommage_photo1.jpg', 2, '2024-06-22 09:30:00'),
(2, 'incident_2_photo2.jpg', 'colis_endommage_photo2.jpg', 2, '2024-06-22 09:31:00'),
(3, 'incident_3_constat.pdf', 'constat_perte.pdf', 1, '2024-09-18 17:15:00'),
(5, 'incident_5_photo.jpg', 'produit_casse.jpg', 2, '2025-05-08 14:05:00'),
(8, 'incident_8_douane.pdf', 'documents_douane_milan.pdf', 1, '2025-08-14 08:15:00');
