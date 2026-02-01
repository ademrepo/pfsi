import random
from datetime import datetime, timedelta
import faker

fake = faker.Faker('fr_FR')

def generate_sql():
    lines = []
    lines.append("-- ============================================")
    lines.append("-- INCREMENTAL SEED FOR JAN 2025")
    lines.append("-- Appended to existing data.sql")
    lines.append("-- ============================================")
    lines.append("PRAGMA foreign_keys = ON;")
    lines.append("")

    # 1. Global Price Fix (Lower by 60%)
    lines.append("-- 1. LOWER EXISTING PRICES")
    lines.append("UPDATE tarification SET tarif_base = tarif_base * 0.4, tarif_poids_kg = tarif_poids_kg * 0.4, tarif_volume_m3 = tarif_volume_m3 * 0.4;")
    lines.append("")

    # 2. Add Missing Destinations (if not exist)
    lines.append("-- 2. NEW DESTINATIONS")
    new_dests = [
        (1001, 'Libye', 'Tripoli', 'International', 2200),
        (1002, 'Italie', 'Rome', 'International', 4200),
        (1003, 'Portugal', 'Lisbon', 'Europe', 4500)
    ]
    for d in new_dests:
        lines.append(f"INSERT INTO destination (id, pays, ville, zone_geographique, tarif_base_defaut) SELECT {d[0]}, '{d[1]}', '{d[2]}', '{d[3]}', {d[4]} WHERE NOT EXISTS (SELECT 1 FROM destination WHERE ville = '{d[2]}');")
    
    # 3. New Clients (Start ID 100)
    lines.append("-- 3. NEW CLIENTS (Dec/Jan)")
    clients = []
    for i in range(101, 121):
        c_code = f"CLI-25-{i:03d}"
        c_type = 'entreprise'
        c_nom = fake.company().replace("'", "''")
        c_solde = 0
        if i % 3 == 0: c_solde = random.randint(10000, 50000)
        clients.append(i)
        lines.append(f"INSERT INTO client (id, code_client, type_client, nom, prenom, email, ville, Solde, statut) VALUES ({i}, '{c_code}', '{c_type}', '{c_nom}', 'Contact', 'client{i}@jan25.com', 'Alger', {c_solde}, 'actif');")
    lines.append("")

    # 4. Operations (Tournees + Expeditions + Finance)
    lines.append("-- 4. DEC 2024 / JAN 2025 OPERATIONS")
    
    start_date = datetime(2024, 12, 1)
    end_date = datetime(2025, 1, 30)
    
    # IDs start high to avoid collisions
    tournee_id = 1000
    exp_id = 1000
    facture_id = 1000
    paiement_id = 1000
    
    current_date = start_date
    while current_date <= end_date:
        daily_tournees = random.randint(1, 3)
        for _ in range(daily_tournees):
            t_statut = 'Terminée'
            if current_date > datetime(2025, 1, 26):
                t_statut = random.choice(['En cours', 'Planifiée'])
            
            # Simple logic for vehicle/chauffeur (using IDs 1-10 which surely exist in data.sql)
            chauf_id = random.randint(1, 10)
            veh_id = random.randint(1, 15)
            
            duree = random.randint(120, 600)
            dist = random.randint(50, 500)
            conso = dist * 0.15
            
            t_code = f"TRN-{current_date.strftime('%Y%m%d')}-{tournee_id}"
            
            # Insert Tournee
            lines.append(f"INSERT INTO tournee (id, code_tournee, date_tournee, date_depart, chauffeur_id, vehicule_id, statut, distance_km, duree_minutes, consommation_litres, created_by) VALUES ({tournee_id}, '{t_code}', '{current_date.strftime('%Y-%m-%d')}', '{current_date.strftime('%Y-%m-%d')} 08:00:00', {chauf_id}, {veh_id}, '{t_statut}', {dist}, {duree}, {conso}, 1);")
            
            # Expeditions
            nb_colis = random.randint(1, 4)
            for _ in range(nb_colis):
                client_id = random.choice(clients)
                
                # Pick valid destination ID logic: 
                # We can use IDs 1-30 safely (from data.sql) OR our new 1001-1003
                dest_id = random.choice(list(range(1, 11)) + [1001, 1002])
                
                srv_id = 1
                if dest_id > 1000 or dest_id > 60: srv_id = 3 # International check rough guess
                
                poids = random.uniform(5, 100)
                vol = random.uniform(0.1, 2.0)
                price = 300 + (poids * 10) + (vol * 150) # New low pricing formula
                if srv_id == 3: price *= 2
                
                e_statut = 'Livré'
                if t_statut != 'Terminée': e_statut = 'En transit'
                
                e_code = f"EXP-25-{exp_id}"
                
                # Link to Tournee
                lines.append(f"INSERT INTO expedition (id, code_expedition, client_id, destination_id, type_service_id, tournee_id, poids_kg, volume_m3, montant_total, statut, date_creation, created_by) VALUES ({exp_id}, '{e_code}', {client_id}, {dest_id}, {srv_id}, {tournee_id}, {poids:.2f}, {vol:.2f}, {price:.2f}, '{e_statut}', '{current_date.strftime('%Y-%m-%d')} 09:00:00', 1);")
                
                # Finance
                if e_statut == 'Livré':
                    f_code = f"FAC-25-{facture_id}"
                    tva = price * 0.19
                    ttc = price + tva
                    f_statut = 'payée'
                    
                    is_paid = True
                    if random.random() < 0.25: 
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
    print("Incremental seed generated!")
