
import random
import datetime
import calendar

# --- CONFIGURATION ---
# We want data from Jan 1, 2025 to Tomorrow
START_DATE = datetime.date(2025, 1, 1)
END_DATE = datetime.date.today() + datetime.timedelta(days=2)

NUM_EXPEDITIONS = 450
NUM_TOURNEES = 120
CLIENTS_COUNT = 20
CHAUFFEURS_COUNT = 15
TYPE_SERVICES = [1, 2, 3] # Standard, Express, International

# Statuses
STATUS_TOURNEE_COMPLETE = 'Terminée' 
STATUS_TOURNEE_IN_PROGRESS = 'En cours'
# Expedition statuses
STATUS_EXP_DELIVERED = 'Livré'
STATUS_EXP_FAILED = 'Échec de livraison'
STATUS_EXP_TRANSIT = 'En transit'
STATUS_EXP_REGISTERED = 'Enregistré'

# --- HEADER (Static Data) ---
SQL_HEADER = """
PRAGMA foreign_keys = ON;

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
-- 2. RÔLES & USERS
-- ============================================
INSERT INTO role (code, libelle) VALUES
('ADMIN', 'Administrateur'), ('AGENT', 'Agent de transport'), ('COMPTABLE', 'Comptable'), ('LOGISTIQUE', 'Responsable logistique'), ('DIRECTION', 'Direction'), ('CHAUFFEUR', 'Chauffeur');

INSERT INTO utilisateur (username, email, password, nom, prenom, telephone, role_id, is_active, created_at) VALUES
('admin', 'admin@transport.dz', 'password123', 'Benali', 'Ahmed', '0555123456', 1, 1, '2025-01-01 10:00:00'),
('agent1', 'agent1@transport.dz', 'password123', 'Kaci', 'Fatima', '0666234567', 2, 1, '2025-01-01 10:00:00'),
('comptable1', 'compta@transport.dz', 'password123', 'Saidi', 'Meriem', '0555456789', 3, 1, '2025-01-01 10:00:00');

-- ============================================
-- 3. DESTINATIONS
-- ============================================
INSERT INTO destination (pays, ville, zone_geographique, code_zone, tarif_base_defaut, is_active, latitude, longitude) VALUES
('Algérie', 'Alger', 'Zone_A', 'ZA001', 500.00, 1, 36.7372, 3.0869),
('Algérie', 'Oran', 'Zone_A', 'ZA002', 500.00, 1, 35.7325, -0.6418),
('Algérie', 'Constantine', 'Zone_A', 'ZA003', 500.00, 1, 36.3656, 6.6147),
('Algérie', 'Annaba', 'Zone_A', 'ZA004', 500.00, 1, 36.9000, 7.7600),
('Algérie', 'Blida', 'Zone_A', 'ZA005', 500.00, 1, 36.4844, 2.8277),
('Algérie', 'Sétif', 'Zone_A', 'ZA007', 500.00, 1, 36.1900, 5.4080),
('Algérie', 'Béjaïa', 'Zone_B', 'ZB001', 800.00, 1, 36.7519, 5.0840),
('Algérie', 'Tizi Ouzou', 'Zone_B', 'ZB002', 800.00, 1, 36.7167, 4.0667),
('Algérie', 'Biskra', 'Zone_B', 'ZB003', 800.00, 1, 34.8067, 5.7333),
('Algérie', 'Chlef', 'Zone_B', 'ZB004', 800.00, 1, 36.1667, 1.3333),
('Algérie', 'Skikda', 'Zone_B', 'ZB005', 800.00, 1, 36.8769, 6.9064),
('Algérie', 'Ouargla', 'Zone_C', 'ZC002', 1500.00, 1, 31.9454, 5.3268),
('Algérie', 'Ghardaïa', 'Zone_C', 'ZC003', 1500.00, 1, 32.4904, 3.6589),
('Algérie', 'Adrar', 'Zone_C', 'ZC004', 1500.00, 1, 27.8789, -0.2711),
('Algérie', 'Illizi', 'Zone_C', 'ZC005', 1500.00, 1, 26.1667, 8.4667),
('Algérie', 'Tamanrasset', 'Zone_C', 'ZC001', 1500.00, 1, 22.7917, 5.5267),
('France', 'Paris', 'International', 'INT001', 5000.00, 1, 48.8566, 2.3522),
('France', 'Marseille', 'International', 'INT002', 5000.00, 1, 43.2965, 5.3698);

-- ============================================
-- 4. SERVICE TYPE & TARIF
-- ============================================
INSERT INTO type_service (code, libelle, description, delai_estime_jours, priorite, is_active) VALUES
('STANDARD', 'Livraison Standard', '3-5 jours', 5, 1, 1),
('EXPRESS', 'Livraison Express', '24-48h', 1, 2, 1),
('INTERNATIONAL', 'International', '7-14 jours', 10, 1, 1);

INSERT INTO tarification (type_service_id, destination_id, tarif_base, tarif_poids_kg, tarif_volume_m3, date_debut) 
SELECT 1, id, 500.00, 50.00, 1000.00, '2025-01-01' FROM destination;

-- ============================================
-- 5. CLIENTS
-- ============================================
INSERT INTO client (code_client, type_client, nom, prenom, telephone, email, adresse, ville, pays, solde, statut, created_at) VALUES
('CLI-00001', 'particulier', 'Mokrani', 'Samir', '0555111222', 'mokrani@email.dz', '12 Rue Didouche', 'Alger', 'Algérie', 0, 'actif', '2025-01-15 10:00:00'),
('CLI-00002', 'particulier', 'Benali', 'Nadia', '0666222333', 'benali@email.dz', '45 Blvd Zirout', 'Oran', 'Algérie', 0, 'actif', '2025-02-10 11:00:00'),
('CLI-00003', 'particulier', 'Khelifa', 'Amine', '0777555666', 'khelifa@email.dz', '23 Cité El Bir', 'Sétif', 'Algérie', 0, 'actif', '2025-01-20 09:30:00'),
('CLI-00004', 'particulier', 'Messaoud', 'Leila', '0555666777', 'messaoud@email.dz', 'Rue Larbi Ben Mhidi', 'Annaba', 'Algérie', 0, 'actif', '2025-03-05 14:00:00'),
('CLI-00005', 'particulier', 'Zaai', 'Mehdi', '0777888999', 'zaidi@email.dz', 'Les Palmiers', 'Tlemcen', 'Algérie', 0, 'actif', '2025-02-15 10:00:00'),
('CLI-00011', 'entreprise', 'SPA TechnoPlus', 'Contact', '0555333444', 'contact@technoplus.dz', 'Zone Ind.', 'Blida', 'Algérie', 0, 'actif', '2025-01-05 10:00:00'),
('CLI-00012', 'entreprise', 'SARL DistriMax', 'Contact', '0666444555', 'info@distrimax.dz', 'Rue Commerce', 'Constantine', 'Algérie', 0, 'actif', '2025-01-08 11:00:00'),
('CLI-00013', 'entreprise', 'EURL AutoPièces', 'Contact', '0666777888', 'ventes@autopieces.dz', 'RN 1', 'Oran', 'Algérie', 0, 'actif', '2025-02-01 09:00:00'),
('CLI-00014', 'entreprise', 'SPA MegaStore', 'Contact', '0666000111', 'achats@megastore.dz', 'Centre Com.', 'Alger', 'Algérie', 0, 'actif', '2025-02-15 13:30:00'),
('CLI-00015', 'entreprise', 'SARL PharmaDist', 'Contact', '0666333444', 'commandes@pharmadist.dz', 'Zone Act.', 'Sétif', 'Algérie', 0, 'actif', '2025-03-10 10:15:00'),
('CLI-00016', 'entreprise', 'EURL InfoTech', 'Contact', '0666666777', 'contact@infotech.dz', 'Cyber Parc', 'Alger', 'Algérie', 0, 'actif', '2025-03-22 14:00:00'),
('CLI-00017', 'entreprise', 'SPA BuildCo', 'Contact', '0666999000', 'admin@buildco.dz', 'Zone Ind. Sud', 'Oran', 'Algérie', 0, 'actif', '2025-04-05 11:00:00'),
('CLI-00018', 'entreprise', 'SARL FreshFood', 'Contact', '0666222333', 'logistique@freshfood.dz', 'Marché Gros', 'Alger', 'Algérie', 0, 'actif', '2025-01-02 08:30:00'),
('CLI-00019', 'entreprise', 'EURL TransExport', 'Contact', '0666555666', 'export@transexport.dz', 'Port', 'Alger', 'Algérie', 0, 'actif', '2025-04-18 10:00:00'),
('CLI-00020', 'entreprise', 'SPA LogisticPlus', 'Contact', '0666888999', 'ops@logisticplus.dz', 'Zone Log.', 'Alger', 'Algérie', 0, 'actif', '2025-05-01 09:00:00'),
('CLI-00021', 'entreprise', 'SARL AgriFood', 'Contact', '0555777888', 'contact@agrifood.dz', 'Zone Ind.', 'Biskra', 'Algérie', 0, 'actif', '2025-06-15 10:00:00'),
('CLI-00022', 'entreprise', 'EURL BatimMat', 'Contact', '0666111222', 'vente@batimmat.dz', 'Zone Ind.', 'Sétif', 'Algérie', 0, 'actif', '2025-07-20 11:00:00'),
('CLI-00023', 'entreprise', 'SPA Electra', 'Contact', '0777333444', 'info@electra.dz', 'Zone Ind.', 'Oran', 'Algérie', 0, 'actif', '2025-08-05 09:30:00'),
('CLI-00024', 'entreprise', 'SARL TexMode', 'Contact', '0555999888', 'contact@texmode.dz', 'Centre Ville', 'Tizi Ouzou', 'Algérie', 0, 'actif', '2025-09-10 14:00:00'),
('CLI-00025', 'entreprise', 'EURL PlasticInd', 'Contact', '0666222111', 'comm@plasticind.dz', 'Zone Ind.', 'Béjaïa', 'Algérie', 0, 'actif', '2025-10-01 10:00:00');

-- ============================================
-- 6. CHAUFFEURS
-- ============================================
INSERT INTO chauffeur (matricule, nom, prenom, telephone, email, adresse, num_permis, categorie_permis, date_embauche, disponibilite, statut) VALUES
('CHF-00001', 'Brahimi', 'Sofiane', '0770123456', 'brahimi@transport.dz', 'Alger', 'P123456', 'D', '2019-01-15', 'disponible', 'actif'),
('CHF-00002', 'Makhloufi', 'Karim', '0771234567', 'makhloufi@transport.dz', 'Oran', 'P234567', 'D', '2019-03-20', 'disponible', 'actif'),
('CHF-00003', 'Bensaïd', 'Ahmed', '0772345678', 'bensaid@transport.dz', 'Constantine', 'P345678', 'D', '2018-06-10', 'disponible', 'actif'),
('CHF-00004', 'Hamdani', 'Yacine', '0773456789', 'hamdani@transport.dz', 'Blida', 'P456789', 'C', '2020-02-05', 'disponible', 'actif'),
('CHF-00005', 'Zerrouki', 'Malik', '0774567890', 'zerrouki@transport.dz', 'Sétif', 'P567890', 'C', '2019-09-12', 'disponible', 'actif'),
('CHF-00006', 'Touati', 'Riad', '0775678901', 'touati@transport.dz', 'Annaba', 'P678901', 'C', '2018-11-25', 'disponible', 'actif'),
('CHF-00007', 'Menai', 'Farid', '0776789012', 'menai@transport.dz', 'Tlemcen', 'P789012', 'C', '2020-05-18', 'disponible', 'actif'),
('CHF-00008', 'Djelloul', 'Nassim', '0777890123', 'djelloul@transport.dz', 'Béjaïa', 'P890123', 'C', '2019-07-22', 'disponible', 'actif'),
('CHF-00009', 'Sahraoui', 'Bilal', '0778901234', 'sahraoui@transport.dz', 'Tizi Ouzou', 'P901234', 'C', '2020-01-30', 'disponible', 'actif'),
('CHF-00010', 'Benkhaled', 'Mourad', '0779012345', 'benkhaled@transport.dz', 'Biskra', 'P012345', 'D', '2018-04-14', 'disponible', 'actif'),
('CHF-00011', 'Kaci', 'Amine', '0770223344', 'kaci@transport.dz', 'Chlef', 'P112233', 'C', '2021-08-09', 'disponible', 'actif'),
('CHF-00012', 'Lounis', 'Samir', '0771334455', 'lounis@transport.dz', 'Skikda', 'P223344', 'C', '2020-12-01', 'disponible', 'actif'),
('CHF-00013', 'Benamar', 'Hocine', '0772445566', 'benamar@transport.dz', 'Mostaganem', 'P334455', 'D', '2018-08-17', 'disponible', 'actif'),
('CHF-00014', 'Meziane', 'Tahar', '0773556677', 'meziane@transport.dz', 'El Oued', 'P445566', 'C', '2020-03-22', 'disponible', 'actif'),
('CHF-00015', 'Boudiaf', 'Walid', '0774667788', 'boudiaf@transport.dz', 'Béchar', 'P556677', 'C', '2019-10-11', 'disponible', 'actif');

-- ============================================
-- 7. VÉHICULES
-- ============================================
INSERT INTO vehicule (immatriculation, type_vehicule, marque, modele, capacite_kg, capacite_m3, consommation_100km, etat, disponibilite, date_mise_en_service) VALUES
('16-32345-01', 'camion', 'Iveco', 'Daily', 3500, 20, 18.0, 'bon', 'disponible', '2019-01-15'),
('16-32346-01', 'camion', 'Mercedes', 'Atego', 4000, 25, 20.0, 'bon', 'disponible', '2019-03-20'),
('16-32347-01', 'camion', 'Man', 'TGL', 3800, 22, 19.0, 'bon', 'disponible', '2018-06-10'),
('16-32348-01', 'camion', 'Volvo', 'FL', 3600, 21, 18.5, 'moyen', 'disponible', '2018-11-25'),
('16-32349-01', 'camion', 'Renault', 'D-Series', 3700, 23, 19.5, 'bon', 'disponible', '2019-09-12'),
('16-12345-01', 'fourgon', 'Renault', 'Master', 1500, 10, 12.5, 'bon', 'disponible', '2020-01-15'),
('16-12346-01', 'fourgon', 'Peugeot', 'Boxer', 1500, 11, 13.0, 'bon', 'disponible', '2020-03-20'),
('16-12347-01', 'fourgon', 'Fiat', 'Ducato', 1400, 10.5, 12.8, 'bon', 'disponible', '2019-06-10'),
('16-12348-01', 'fourgon', 'Mercedes', 'Sprinter', 1600, 12, 14.0, 'bon', 'disponible', '2020-02-05'),
('16-12349-01', 'fourgon', 'Ford', 'Transit', 1550, 11.5, 13.5, 'bon', 'disponible', '2019-09-12'),
('16-12350-01', 'fourgon', 'Renault', 'Master', 1500, 10, 12.5, 'moyen', 'disponible', '2018-11-25'),
('16-22345-01', 'camionnette', 'Hyundai', 'H100', 1000, 6, 10.0, 'bon', 'disponible', '2020-05-18'),
('16-22346-01', 'camionnette', 'VW', 'Crafter', 1100, 6.5, 10.5, 'bon', 'disponible', '2019-07-22'),
('16-22347-01', 'camionnette', 'Nissan', 'Cabstar', 1050, 6.2, 10.2, 'bon', 'disponible', '2020-01-30'),
('16-22348-01', 'camionnette', 'Isuzu', 'NLR', 1200, 7, 11.0, 'bon', 'disponible', '2018-04-14');

"""

def gen_random_date(start, end):
    delta = end - start
    random_days = random.randrange(delta.days + 1)
    dt = datetime.datetime.combine(start + datetime.timedelta(days=random_days), datetime.time(random.randint(6, 18), random.randint(0, 59)))
    return dt

def main():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, 'db', 'seed_demo.sql')
    
    print(f"Generating SQL to {output_path}...")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(SQL_HEADER)
        
        # --- 8. TOURNÉES ---
        f.write("\n-- TOURNÉES\n")
        tournees = []
        
        for i in range(1, NUM_TOURNEES + 1):
            
            # Bias date: 20% chances for "Recent" (last 10 days) to ensure current data
            if random.random() < 0.2:
                recent_start = datetime.date.today() - datetime.timedelta(days=10)
                if recent_start > END_DATE: recent_start = START_DATE # Fallback
                created_dt = gen_random_date(recent_start, END_DATE)
            else:
                cutoff = datetime.date.today() - datetime.timedelta(days=10)
                if cutoff < START_DATE: cutoff = END_DATE # Fallback
                created_dt = gen_random_date(START_DATE, cutoff)

            code = f"TRN-{created_dt.strftime('%Y%m%d')}-{i:03d}"
            
            driver_id = random.randint(1, CHAUFFEURS_COUNT)
            vehicule_id = random.randint(1, 15)
            
            status = STATUS_TOURNEE_COMPLETE
            date_retour_dt = created_dt + datetime.timedelta(hours=random.randint(4, 12))
            date_retour_str = f"'{date_retour_dt.strftime('%Y-%m-%d %H:%M:%S')}'"
            
            km_start = 10000 + (i * 100)
            dist = random.randint(50, 600)
            km_end = km_start + dist
            duration = random.randint(120, 720) # mins
            fuel = round((dist/100.0) * random.uniform(10, 20), 2)
            
            # Active tournées for "Vehicle with Driver" visibility (only recent ones)
            # If created_dt is > today - 2 days, make it IN PROGRESS
             #[FIX]: logic must ensure we don't have finished tours in the future
            if created_dt > datetime.datetime.now():
                 status = 'Planifiée'
                 date_retour_str = 'NULL'
                 km_end = 'NULL'
                 duration = 'NULL'
                 fuel = 'NULL'
            elif created_dt.date() >= (datetime.date.today() - datetime.timedelta(days=1)):
                 status = STATUS_TOURNEE_IN_PROGRESS
                 date_retour_str = 'NULL'
                 km_end = 'NULL'
                 duration = 'NULL'
                 fuel = 'NULL'
            
            notes = f"Tournée {code}"
            
            sql = f"INSERT INTO tournee (code_tournee, date_tournee, date_depart, date_retour, chauffeur_id, vehicule_id, statut, kilometrage_depart, kilometrage_retour, distance_km, duree_minutes, consommation_litres, notes, created_by) VALUES "
            sql += f"('{code}', '{created_dt.strftime('%Y-%m-%d')}', '{created_dt.strftime('%Y-%m-%d %H:%M:%S')}', {date_retour_str}, {driver_id}, {vehicule_id}, '{status}', {km_start}, {km_end}, {dist}, {duration}, {fuel}, '{notes}', 1);\n"
            f.write(sql)
            
            tournees.append({'id': i, 'date': created_dt, 'driver': driver_id, 'status': status})

        # --- 9. EXPÉDITIONS ---
        f.write("\n-- EXPÉDITIONS\n")
        expeditions = []
        
        for i in range(1, NUM_EXPEDITIONS + 1):
            client = random.randint(1, CLIENTS_COUNT)
            service = random.choice(TYPE_SERVICES)
            dest = random.randint(1, 18)
            weight = round(random.uniform(1.0, 50.0), 2)
            vol = round(random.uniform(0.1, 3.0), 2)
            
            # Date mirroring tournées or random
            if i <= len(tournees):
                # Ensure we have expeditions for our tournées
                t = tournees[i-1]
                created_dt = t['date'] - datetime.timedelta(days=random.randint(0, 3))
            else:
                created_dt = gen_random_date(START_DATE, END_DATE) # Changed END_DATE.date() to END_DATE

            code = f"EXP-{created_dt.strftime('%Y%m%d')}-{i:03d}"
            
            # Default
            status = STATUS_EXP_REGISTERED
            tournee = None
            tournee_sql = 'NULL'
            
            # Try to link to a compatible tournee (same date-ish)
            candidates = [t for t in tournees if t['date'] >= created_dt and (t['date'] - created_dt).days < 5]
            if candidates:
                tournee = random.choice(candidates)
                if tournee['status'] == STATUS_TOURNEE_COMPLETE:
                    status = STATUS_EXP_DELIVERED
                    if random.random() < 0.05: status = STATUS_EXP_FAILED
                elif tournee['status'] == STATUS_TOURNEE_IN_PROGRESS:
                    status = STATUS_EXP_TRANSIT
                else: 
                     status = STATUS_EXP_REGISTERED
                     tournee = None # Planned tournee, maybe assigned but not delivered
            
            if tournee: tournee_sql = tournee['id']
            
            amount = random.randint(500, 15000)
            
            sql = f"INSERT INTO expedition (code_expedition, client_id, type_service_id, destination_id, poids_kg, volume_m3, description_colis, adresse_livraison, nom_destinataire, telephone_destinataire, date_creation, statut, montant_total, est_facturee, tournee_id, created_by) VALUES "
            sql += f"('{code}', {client}, {service}, {dest}, {weight}, {vol}, 'Colis {i}', 'Adresse {i}', 'Dest {i}', '0555000000', '{created_dt.strftime('%Y-%m-%d %H:%M:%S')}', '{status}', {amount}, 1, {tournee_sql}, 1);\n"
            f.write(sql)
            
            expeditions.append({'id': i, 'client': client, 'amount': amount, 'date': created_dt, 'status': status, 'code': code})

        # --- 10. FACTURES & PAIEMENTS ---
        f.write("\n-- FACTURES & PAIEMENTS\n")
        
        fact_id = 1
        paiement_id = 1
        
        for exp in expeditions:
            # Only invoice delivered items (usually)
            if exp['status'] in [STATUS_EXP_DELIVERED, STATUS_EXP_FAILED]:
                inv_date = exp['date'] + datetime.timedelta(days=1)
                ref = f"FACT-{inv_date.strftime('%Y%m')}-{fact_id:04d}"
                ht = exp['amount']
                tva = round(ht * 0.19, 2)
                ttc = ht + tva
                
                # Create Facture
                sql = f"INSERT INTO facture (numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES "
                sql += f"('{ref}', {exp['client']}, '{inv_date.strftime('%Y-%m-%d')}', {ht}, {tva}, {ttc}, 'payee');\n"
                f.write(sql)
                
                # Link Facture-Expedition
                sql = f"INSERT INTO facture_expedition (facture_id, expedition_id) VALUES ({fact_id}, {exp['id']});\n"
                f.write(sql)
                
                # Create Paiement (Fix for '0 total paiement')
                pay_date = inv_date + datetime.timedelta(days=random.randint(0, 5))
                mode = random.choice(['Virement', 'Espèces', 'Chèque'])
                
                sql = f"INSERT INTO paiement (facture_id, client_id, date_paiement, mode_paiement, montant, statut, updated_at) VALUES "
                sql += f"({fact_id}, {exp['client']}, '{pay_date.strftime('%Y-%m-%d')}', '{mode}', {ttc}, 'Validé', '{pay_date.strftime('%Y-%m-%d %H:%M:%S')}');\n"
                f.write(sql)
                
                fact_id += 1
                paiement_id += 1
                
        # --- 11. INCIDENTS ---
        f.write("\n-- INCIDENTS\n")
        inc_id = 1
        for exp in expeditions:
            if random.random() < 0.03: # 3% incidents
                i_type = random.choice(['RETARD', 'ENDOMMAGEMENT'])
                created = exp['date'] + datetime.timedelta(hours=24)
                code = f"INC-{created.strftime('%Y%m%d')}-{inc_id:03d}"
                sql = f"INSERT INTO incident (code_incident, type_incident, expedition_id, tournee_id, commentaire, action_appliquee, notify_direction, notify_client, created_by, created_at) VALUES "
                sql += f"('{code}', '{i_type}', {exp['id']}, NULL, 'Incident auto', 'NONE', 1, 0, 1, '{created.strftime('%Y-%m-%d %H:%M:%S')}');\n"
                f.write(sql)
                inc_id += 1
    
    print("Done.")

if __name__ == "__main__":
    main()
