import random
from datetime import datetime, timedelta
import faker

fake = faker.Faker('fr_FR')

def generate_sql():
    lines = []
    lines.append("-- ============================================")
    lines.append("-- SEED GENERATED FOR JAN 2025 SHOWCASE")
    lines.append("-- ============================================")
    lines.append("PRAGMA foreign_keys = ON;")
    lines.append("")
    
    # 1. Clean
    tables = ['alerte', 'reclamation_expedition', 'reclamation', 'incident_attachment', 'incident', 
              'paiement', 'facture_expedition', 'facture', 'tracking_expedition', 'expedition', 
              'tournee', 'tarification', 'type_service', 'destination', 'vehicule', 
              'chauffeur', 'client', 'favori', 'utilisateur', 'role']
    for t in tables:
        lines.append(f"DELETE FROM {t};")
    lines.append("DELETE FROM sqlite_sequence;")
    lines.append("")

    # 2. Key Static Data (Users, Roles)
    lines.append("-- ROLES & USERS")
    lines.append("INSERT INTO role (id, code, libelle) VALUES (1, 'ADMIN', 'Administrateur'), (2, 'AGENT', 'Agent'), (3, 'COMPTABLE', 'Comptable'), (4, 'CHAUFFEUR', 'Chauffeur');")
    lines.append("INSERT INTO utilisateur (id, username, email, password, nom, prenom, role_id) VALUES (1, 'admin', 'admin@transport.dz', 'password123', 'Admin', 'Sys', 1);")
    lines.append("")

    # 3. Destinations (International + Local)
    destinations = [
        (1, 'Algérie', 'Alger', 'Zone_A', 300),
        (2, 'Algérie', 'Oran', 'Zone_A', 300),
        (3, 'Algérie', 'Constantine', 'Zone_A', 300),
        (4, 'Algérie', 'Sétif', 'Zone_A', 300),
        (5, 'Algérie', 'Hassi Messaoud', 'Zone_Sud', 800),
        (6, 'Tunisie', 'Tunis', 'International', 2000),
        (7, 'Maroc', 'Casablanca', 'International', 2500),
        (8, 'Libye', 'Tripoli', 'International', 2200),
        (9, 'Espagne', 'Madrid', 'Europe', 4000),
        (10, 'France', 'Paris', 'Europe', 4500),
        (11, 'Italie', 'Rome', 'Europe', 4200),
    ]
    lines.append("-- DESTINATIONS")
    for d in destinations:
        lines.append(f"INSERT INTO destination (id, pays, ville, zone_geographique, tarif_base_defaut) VALUES ({d[0]}, '{d[1]}', '{d[2]}', '{d[3]}', {d[4]});")
    
    # 4. Services
    lines.append("-- SERVICES")
    lines.append("INSERT INTO type_service (id, code, libelle, priorite) VALUES (1, 'STD', 'Standard', 1), (2, 'EXP', 'Express', 2), (3, 'INT', 'International', 3);")
    
    # 5. Tarification (Realistic Low Prices)
    lines.append("-- TARIFICATION")
    # Mapping: service_id, dest_id, base, kg, m3
    for d in destinations:
        d_id = d[0]
        # Standard
        lines.append(f"INSERT INTO tarification (type_service_id, destination_id, tarif_base, tarif_poids_kg, tarif_volume_m3, date_debut) VALUES (1, {d_id}, {d[4]}, 15, 200, '2024-01-01');")
        # Express (+50%)
        lines.append(f"INSERT INTO tarification (type_service_id, destination_id, tarif_base, tarif_poids_kg, tarif_volume_m3, date_debut) VALUES (2, {d_id}, {d[4]*1.5}, 25, 300, '2024-01-01');")
        # Intel
        if d[3] in ['International', 'Europe']:
             lines.append(f"INSERT INTO tarification (type_service_id, destination_id, tarif_base, tarif_poids_kg, tarif_volume_m3, date_debut) VALUES (3, {d_id}, {d[4]*2}, 40, 500, '2024-01-01');")

    # 6. Clients (With Balances)
    lines.append("-- CLIENTS")
    clients = []
    for i in range(1, 21):
        c_code = f"CLI-{i:05d}"
        c_type = 'entreprise' if i > 5 else 'particulier'
        c_nom = fake.company() if c_type == 'entreprise' else fake.last_name()
        escaped_nom = c_nom.replace("'", "''")
        c_solde = 0
        if i % 3 == 0: c_solde = random.randint(5000, 50000) # Some debt
        if i % 4 == 0: c_solde = 0 # Clean
        clients.append(i)
        lines.append(f"INSERT INTO client (id, code_client, type_client, nom, prenom, email, ville, Solde) VALUES ({i}, '{c_code}', '{c_type}', '{escaped_nom}', 'Contact', 'client{i}@test.com', 'Alger', {c_solde});")

    # 7. Chauffeurs & Vehicules
    lines.append("-- FLOTTE")
    for i in range(1, 11):
        lines.append(f"INSERT INTO chauffeur (id, matricule, nom, prenom, num_permis, statut) VALUES ({i}, 'CH-{i:03d}', '{fake.last_name()}', '{fake.first_name()}', 'PERMIS-{i}', 'actif');")
        lines.append(f"INSERT INTO vehicule (id, immatriculation, marque, modeLe, capacite_kg, capacite_m3) VALUES ({i}, '00{i}-116-16', 'Renault', 'Master', 1500, 12);")

    # 8. Tournees & Expeditions (The Meat)
    lines.append("-- OPERATIONS")
    
    # Dates: Dec 2024 (History) and Jan 2025 (Active)
    start_date = datetime(2024, 12, 1)
    end_date = datetime(2025, 1, 30)
    
    tournee_id = 1
    exp_id = 1
    facture_id = 1
    paiement_id = 1
    
    current_date = start_date
    while current_date <= end_date:
        # 1-3 tournees per day
        daily_tournees = random.randint(1, 3)
        for _ in range(daily_tournees):
            t_statut = 'Terminée'
            if current_date > datetime(2025, 1, 25):
                t_statut = random.choice(['En cours', 'Planifiée', 'Terminée'])
            
            duree = random.randint(120, 600)
            dist = random.randint(50, 500)
            conso = dist * 0.15
            chauf_id = random.randint(1, 10)
            veh_id = random.randint(1, 10)
            
            t_code = f"TRN-{current_date.strftime('%Y%m%d')}-{tournee_id:03d}"
            
            lines.append(f"INSERT INTO tournee (id, code_tournee, date_tournee, date_depart, chauffeur_id, vehicule_id, statut, distance_km, duree_minutes, consommation_litres, created_by) VALUES ({tournee_id}, '{t_code}', '{current_date.strftime('%Y-%m-%d')}', '{current_date.strftime('%Y-%m-%d')} 08:00:00', {chauf_id}, {veh_id}, '{t_statut}', {dist}, {duree}, {conso}, 1);")
            
            # Expeditions per tournee
            nb_colis = random.randint(2, 6)
            for _ in range(nb_colis):
                client_id = random.choice(clients)
                dest = random.choice(destinations)
                dest_id = dest[0]
                
                srv_id = 1
                if dest[3] != 'Zone_A': srv_id = 3
                
                poids = random.uniform(5, 100)
                vol = random.uniform(0.1, 2.0)
                
                # Pricing logic (simple)
                base = dest[4]
                if srv_id == 3: base *= 2
                price = base + (poids * 15) + (vol * 200)
                
                e_statut = 'Livré'
                if t_statut != 'Terminée': e_statut = 'En transit'
                if random.random() < 0.05: e_statut = 'Échec de livraison' # 5% fail rate
                
                e_code = f"EXP-{current_date.strftime('%Y%m')}-{exp_id:04d}"
                
                lines.append(f"INSERT INTO expedition (id, code_expedition, client_id, destination_id, type_service_id, tournee_id, poids_kg, volume_m3, montant_total, statut, date_creation, created_by) VALUES ({exp_id}, '{e_code}', {client_id}, {dest_id}, {srv_id}, {tournee_id}, {poids:.2f}, {vol:.2f}, {price:.2f}, '{e_statut}', '{current_date.strftime('%Y-%m-%d')} 09:00:00', 1);")
                
                # Finance (Only for delivered/shipped items)
                if e_statut in ['Livré', 'En transit']:
                    # Create Invoice
                    f_code = f"FAC-{current_date.strftime('%Y')}-{facture_id:05d}"
                    tva = price * 0.19
                    ttc = price + tva
                    f_statut = 'payée'
                    
                    # Payment Logic
                    is_paid = True
                    if random.random() < 0.2: # 20% unpaid
                        f_statut = 'impayée'
                        is_paid = False
                    
                    lines.append(f"INSERT INTO facture (id, numero_facture, client_id, date_facture, total_ht, montant_tva, total_ttc, statut) VALUES ({facture_id}, '{f_code}', {client_id}, '{current_date.strftime('%Y-%m-%d')}', {price:.2f}, {tva:.2f}, {ttc:.2f}, '{f_statut}');")
                    lines.append(f"INSERT INTO facture_expedition (facture_id, expedition_id) VALUES ({facture_id}, {exp_id});")
                    
                    if is_paid:
                        lines.append(f"INSERT INTO paiement (id, facture_id, client_id, date_paiement, montant, mode_paiement, statut) VALUES ({paiement_id}, {facture_id}, {client_id}, '{current_date.strftime('%Y-%m-%d')}', {ttc:.2f}, 'Virement', 'Validé');")
                        paiement_id += 1
                        
                    facture_id += 1
                
                exp_id += 1
            tournee_id += 1
        current_date += timedelta(days=1)
        
    return "\n".join(lines)

if __name__ == "__main__":
    sql = generate_sql()
    with open("c:/L3 ISIL A 2025-2026/PFKHRA/db/seed_demo.sql", "w", encoding="utf-8") as f:
        f.write(sql)
    print("Generate successfully!")
