-- ============================================
-- DONNÉES HISTORIQUES 2025 (POUR ANALYTICS)
-- ============================================

-- ============================================
-- 1. TOURNÉES 2025
-- ============================================
INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES
-- JANVIER
('TRN-2025-01-A', '2025-01-15', '2025-01-15 08:00:00', '2025-01-15 17:00:00', 1, 1, 'complete', 10000, 10300, 300, 540, 45.5, 'Tournée Janvier A', 1),
('TRN-2025-01-B', '2025-01-20', '2025-01-20 09:00:00', '2025-01-20 16:00:00', 2, 2, 'complete', 12000, 12150, 150, 420, 22.0, 'Tournée Janvier B', 1),

-- FÉVRIER
('TRN-2025-02-A', '2025-02-10', '2025-02-10 08:00:00', '2025-02-10 18:00:00', 1, 1, 'complete', 10300, 10700, 400, 600, 58.0, 'Tournée Février A', 1),
('TRN-2025-02-B', '2025-02-25', '2025-02-25 08:30:00', '2025-02-25 15:30:00', 3, 3, 'complete', 5000, 5200, 200, 420, 28.5, 'Tournée Février B', 1),

-- MARS
('TRN-2025-03-A', '2025-03-05', '2025-03-05 07:00:00', '2025-03-05 19:00:00', 2, 2, 'complete', 12150, 12650, 500, 720, 75.0, 'Tournée Mars A', 1),
('TRN-2025-03-B', '2025-03-20', '2025-03-20 08:00:00', '2025-03-20 16:00:00', 4, 4, 'complete', 8000, 8250, 250, 480, 35.0, 'Tournée Mars B', 1),

-- AVRIL
('TRN-2025-04-A', '2025-04-12', '2025-04-12 08:00:00', '2025-04-12 17:00:00', 1, 1, 'complete', 10700, 11050, 350, 540, 50.0, 'Tournée Avril A', 1),
('TRN-2025-04-B', '2025-04-28', '2025-04-28 09:00:00', '2025-04-28 15:00:00', 5, 5, 'complete', 2000, 2100, 100, 360, 15.0, 'Tournée Avril B', 1),

-- MAI
('TRN-2025-05-A', '2025-05-15', '2025-05-15 07:30:00', '2025-05-15 18:30:00', 2, 2, 'complete', 12650, 13150, 500, 660, 72.0, 'Tournée Mai A', 1),
('TRN-2025-05-B', '2025-05-30', '2025-05-30 08:00:00', '2025-05-30 16:00:00', 3, 3, 'complete', 5200, 5400, 200, 480, 29.0, 'Tournée Mai B', 1),

-- JUIN
('TRN-2025-06-A', '2025-06-10', '2025-06-10 08:00:00', '2025-06-10 17:00:00', 1, 1, 'complete', 11050, 11400, 350, 540, 52.0, 'Tournée Juin A', 1),
('TRN-2025-06-B', '2025-06-25', '2025-06-25 10:00:00', '2025-06-25 14:00:00', 4, 4, 'complete', 8250, 8350, 100, 240, 14.0, 'Tournée Juin B', 1),

-- JUILLET
('TRN-2025-07-A', '2025-07-05', '2025-07-05 06:00:00', '2025-07-05 20:00:00', 1, 1, 'complete', 11400, 12000, 600, 840, 85.0, 'Tournée Juillet A', 1),
('TRN-2025-07-B', '2025-07-20', '2025-07-20 08:00:00', '2025-07-20 16:00:00', 5, 5, 'complete', 2100, 2350, 250, 480, 38.0, 'Tournée Juillet B', 1),

-- AOÛT
('TRN-2025-08-A', '2025-08-15', '2025-08-15 08:00:00', '2025-08-15 17:00:00', 2, 2, 'complete', 13150, 13450, 300, 540, 44.0, 'Tournée Août A', 1),
('TRN-2025-08-B', '2025-08-25', '2025-08-25 09:00:00', '2025-08-25 15:00:00', 3, 3, 'complete', 5400, 5550, 150, 360, 22.0, 'Tournée Août B', 1),

-- SEPTEMBRE
('TRN-2025-09-A', '2025-09-10', '2025-09-10 08:00:00', '2025-09-10 18:00:00', 1, 1, 'complete', 12000, 12400, 400, 600, 59.0, 'Tournée Septembre A', 1),
('TRN-2025-09-B', '2025-09-25', '2025-09-25 08:30:00', '2025-09-25 16:30:00', 4, 4, 'complete', 8350, 8600, 250, 480, 36.0, 'Tournée Septembre B', 1),

-- OCTOBRE
('TRN-2025-10-A', '2025-10-05', '2025-10-05 07:00:00', '2025-10-05 19:00:00', 2, 2, 'complete', 13450, 13950, 500, 720, 73.0, 'Tournée Octobre A', 1),
('TRN-2025-10-B', '2025-10-20', '2025-10-20 08:00:00', '2025-10-20 16:00:00', 5, 5, 'complete', 2350, 2550, 200, 480, 30.0, 'Tournée Octobre B', 1),

-- NOVEMBRE
('TRN-2025-11-A', '2025-11-12', '2025-11-12 08:00:00', '2025-11-12 17:00:00', 1, 1, 'complete', 12400, 12750, 350, 540, 51.0, 'Tournée Novembre A', 1),
('TRN-2025-11-B', '2025-11-28', '2025-11-28 09:00:00', '2025-11-28 15:00:00', 3, 3, 'complete', 5550, 5700, 150, 360, 23.0, 'Tournée Novembre B', 1),

-- DÉCEMBRE
('TRN-2025-12-A', '2025-12-10', '2025-12-10 08:00:00', '2025-12-10 17:00:00', 2, 2, 'complete', 13950, 14250, 300, 540, 43.0, 'Tournée Décembre A', 1),
('TRN-2025-12-B', '2025-12-24', '2025-12-24 08:00:00', '2025-12-24 14:00:00', 1, 1, 'complete', 12750, 12900, 150, 360, 21.0, 'Tournée Décembre B', 1);

-- ============================================
-- 2. EXPÉDITIONS 2025
-- ============================================
INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES
('EXP-2025-01-A', 1, 1, 1, 10.0, 1.0, 'Colis Jan A', 'Alger', 'Dest A', '0555000000', '2025-01-14 10:00:00', 'livre', 500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-A'), 1),
('EXP-2025-01-B', 2, 1, 2, 20.0, 2.0, 'Colis Jan B', 'Oran', 'Dest B', '0555000000', '2025-01-19 10:00:00', 'livre', 1000.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-01-B'), 1),

('EXP-2025-02-A', 3, 1, 3, 15.0, 1.5, 'Colis Fev A', 'Constantine', 'Dest C', '0555000000', '2025-02-09 10:00:00', 'livre', 750.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-A'), 1),
('EXP-2025-02-B', 4, 1, 4, 25.0, 2.5, 'Colis Fev B', 'Annaba', 'Dest D', '0555000000', '2025-02-24 10:00:00', 'livre', 1250.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-02-B'), 1),

('EXP-2025-03-A', 5, 1, 5, 30.0, 3.0, 'Colis Mars A', 'Blida', 'Dest E', '0555000000', '2025-03-04 10:00:00', 'livre', 1500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-A'), 1),
('EXP-2025-03-B', 1, 1, 1, 10.0, 1.0, 'Colis Mars B', 'Alger', 'Dest F', '0555000000', '2025-03-19 10:00:00', 'livre', 500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-03-B'), 1),

('EXP-2025-04-A', 2, 1, 2, 20.0, 2.0, 'Colis Avril A', 'Oran', 'Dest G', '0555000000', '2025-04-11 10:00:00', 'livre', 1000.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-A'), 1),
('EXP-2025-04-B', 3, 1, 3, 15.0, 1.5, 'Colis Avril B', 'Constantine', 'Dest H', '0555000000', '2025-04-27 10:00:00', 'livre', 750.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-04-B'), 1),

('EXP-2025-05-A', 4, 1, 4, 25.0, 2.5, 'Colis Mai A', 'Annaba', 'Dest I', '0555000000', '2025-05-14 10:00:00', 'livre', 1250.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-A'), 1),
('EXP-2025-05-B', 5, 1, 5, 30.0, 3.0, 'Colis Mai B', 'Blida', 'Dest J', '0555000000', '2025-05-29 10:00:00', 'livre', 1500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-05-B'), 1),

('EXP-2025-06-A', 1, 1, 1, 10.0, 1.0, 'Colis Juin A', 'Alger', 'Dest K', '0555000000', '2025-06-09 10:00:00', 'livre', 500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-A'), 1),
('EXP-2025-06-B', 2, 1, 2, 20.0, 2.0, 'Colis Juin B', 'Oran', 'Dest L', '0555000000', '2025-06-24 10:00:00', 'livre', 1000.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-06-B'), 1),

('EXP-2025-07-A', 3, 1, 3, 15.0, 1.5, 'Colis Juil A', 'Constantine', 'Dest M', '0555000000', '2025-07-04 10:00:00', 'livre', 750.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-A'), 1),
('EXP-2025-07-B', 4, 1, 4, 25.0, 2.5, 'Colis Juil B', 'Annaba', 'Dest N', '0555000000', '2025-07-19 10:00:00', 'livre', 1250.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-07-B'), 1),

('EXP-2025-08-A', 5, 1, 5, 30.0, 3.0, 'Colis Aout A', 'Blida', 'Dest O', '0555000000', '2025-08-14 10:00:00', 'livre', 1500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-A'), 1),
('EXP-2025-08-B', 1, 1, 1, 10.0, 1.0, 'Colis Aout B', 'Alger', 'Dest P', '0555000000', '2025-08-24 10:00:00', 'livre', 500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-08-B'), 1),

('EXP-2025-09-A', 2, 1, 2, 20.0, 2.0, 'Colis Sept A', 'Oran', 'Dest Q', '0555000000', '2025-09-09 10:00:00', 'livre', 1000.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-A'), 1),
('EXP-2025-09-B', 3, 1, 3, 15.0, 1.5, 'Colis Sept B', 'Constantine', 'Dest R', '0555000000', '2025-09-24 10:00:00', 'livre', 750.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-09-B'), 1),

('EXP-2025-10-A', 4, 1, 4, 25.0, 2.5, 'Colis Oct A', 'Annaba', 'Dest S', '0555000000', '2025-10-04 10:00:00', 'livre', 1250.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-A'), 1),
('EXP-2025-10-B', 5, 1, 5, 30.0, 3.0, 'Colis Oct B', 'Blida', 'Dest T', '0555000000', '2025-10-19 10:00:00', 'livre', 1500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-10-B'), 1),

('EXP-2025-11-A', 1, 1, 1, 10.0, 1.0, 'Colis Nov A', 'Alger', 'Dest U', '0555000000', '2025-11-11 10:00:00', 'livre', 500.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-11-A'), 1),
('EXP-2025-11-B', 2, 1, 2, 20.0, 2.0, 'Colis Nov B', 'Oran', 'Dest V', '0555000000', '2025-11-27 10:00:00', 'livre', 1000.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-11-B'), 1),

('EXP-2025-12-A', 3, 1, 3, 15.0, 1.5, 'Colis Dec A', 'Constantine', 'Dest W', '0555000000', '2025-12-09 10:00:00', 'livre', 750.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-12-A'), 1),
('EXP-2025-12-B', 4, 1, 4, 25.0, 2.5, 'Colis Dec B', 'Annaba', 'Dest X', '0555000000', '2025-12-23 10:00:00', 'livre', 1250.0, 1, (SELECT id FROM tournee WHERE code_tournee='TRN-2025-12-B'), 1);
