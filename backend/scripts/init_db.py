import argparse
import sqlite3
from pathlib import Path
import time
import sys


def _exec_sql_file(cur, path: Path):
    sql = path.read_text(encoding="utf-8", errors="replace")
    # Disable foreign key constraints during data loading
    cur.execute("PRAGMA foreign_keys = OFF;")
    cur.executescript(sql)
    cur.execute("PRAGMA foreign_keys = ON;")


def _db_has_any_tables(con: sqlite3.Connection) -> bool:
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return cur.fetchone() is not None


def main():
    parser = argparse.ArgumentParser(
        description="Initialize db.sqlite3 from SQL files (schema + data + optional seed)."
    )
    parser.add_argument("--reset", action="store_true", help="Delete existing db.sqlite3 and recreate it.")
    parser.add_argument("--seed", action="store_true", help="Load complete_seed_2024_2026.sql for realistic test data.")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent  # backend/
    db_path = base_dir / "db.sqlite3"
    schema_path = base_dir.parent / "db" / "schema.sql"
    data_path = base_dir.parent / "db" / "data.sql"
    seed_path = base_dir.parent / "db" / "complete_seed_2024_2026.sql"

    # Check for required files
    for p in (schema_path, data_path):
        if not p.exists():
            raise SystemExit(f"Missing SQL file: {p}")

    if args.reset and db_path.exists():
        attempts = 3
        for i in range(attempts):
            try:
                db_path.unlink()
                break  # Success
            except PermissionError:
                if i < attempts - 1:
                    print(f"Warning: Could not delete database file '{db_path}'. Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    print(f"Error: Could not delete existing database file at {db_path}.")
                    print("Please ensure no other programs are using this file (e.g., a database viewer or a previous run of the application).")
                    sys.exit(1)

    con = sqlite3.connect(db_path)
    try:
        con.execute("PRAGMA foreign_keys = ON;")
        cur = con.cursor()

        if not args.reset and _db_has_any_tables(con):
            print(f"DB already initialized: {db_path}")
            if args.seed and seed_path.exists():
                print("Loading complete_seed_2024_2026.sql...")
                _exec_sql_file(cur, seed_path)
                con.commit()
                print("Seed data loaded successfully!")
            return

        print(f"Initializing DB: {db_path}")
        _exec_sql_file(cur, schema_path)
        _exec_sql_file(cur, data_path)
        
        # Load seed data if requested
        if args.seed:
            if seed_path.exists():
                print("Loading complete_seed_2024_2026.sql...")
                _exec_sql_file(cur, seed_path)
            else:
                print(f"Warning: complete_seed_2024_2026.sql not found at {seed_path}")
        
        # Fix foreign key constraints after data insertion
        print("Fixing foreign key constraints...")
        cur.execute("""
            UPDATE expedition 
            SET client_id = NULL 
            WHERE client_id NOT IN (SELECT id FROM client)
        """)
        cur.execute("""
            UPDATE expedition 
            SET destination_id = NULL 
            WHERE destination_id NOT IN (SELECT id FROM destination)
        """)
        cur.execute("""
            UPDATE expedition 
            SET type_service_id = NULL 
            WHERE type_service_id NOT IN (SELECT id FROM type_service)
        """)
        cur.execute("""
            UPDATE expedition 
            SET tournee_id = NULL 
            WHERE tournee_id NOT IN (SELECT id FROM tournee)
        """)
        # Fix facture FK violations - remap invalid client_ids to valid ones
        cur.execute("""
            UPDATE facture 
            SET client_id = ((client_id - 1) % (SELECT MAX(id) FROM client)) + 1
            WHERE client_id NOT IN (SELECT id FROM client)
        """)
        # Fix paiement FK violations - remap invalid client_ids to valid ones
        cur.execute("""
            UPDATE paiement 
            SET client_id = ((client_id - 1) % (SELECT MAX(id) FROM client)) + 1
            WHERE client_id NOT IN (SELECT id FROM client)
        """)
        # Remove 2026 data to keep graphs clean (data only through 2025)
        # Must delete child records first to avoid FK violations
        
        # 0. Get IDs to delete
        cur.execute("CREATE TEMP TABLE ids_exp AS SELECT id FROM expedition WHERE date_creation >= '2026-01-01'")
        cur.execute("CREATE TEMP TABLE ids_trn AS SELECT id FROM tournee WHERE date_tournee >= '2026-01-01'")
        cur.execute("CREATE TEMP TABLE ids_fac AS SELECT id FROM facture WHERE date_facture >= '2026-01-01'")
        cur.execute("CREATE TEMP TABLE ids_inc AS SELECT id FROM incident WHERE expedition_id IN (SELECT id FROM ids_exp) OR tournee_id IN (SELECT id FROM ids_trn) OR created_at >= '2026-01-01'")

        # 1. Accessoires: Alerte, Attachment (depend on Incident/Exp/Trn)
        cur.execute("DELETE FROM alerte WHERE incident_id IN (SELECT id FROM ids_inc) OR expedition_id IN (SELECT id FROM ids_exp) OR tournee_id IN (SELECT id FROM ids_trn)")
        cur.execute("DELETE FROM incident_attachment WHERE incident_id IN (SELECT id FROM ids_inc)")
        
        # 2. Level 2: Tracking, Incidents, Reclamation Links
        cur.execute("DELETE FROM tracking_expedition WHERE expedition_id IN (SELECT id FROM ids_exp) OR tournee_id IN (SELECT id FROM ids_trn)")
        cur.execute("DELETE FROM incident WHERE id IN (SELECT id FROM ids_inc)")
        cur.execute("DELETE FROM reclamation_expedition WHERE expedition_id IN (SELECT id FROM ids_exp)")
        
        # 3. Facture links & Paiements
        cur.execute("DELETE FROM facture_expedition WHERE expedition_id IN (SELECT id FROM ids_exp)")
        cur.execute("DELETE FROM facture_expedition WHERE facture_id IN (SELECT id FROM ids_fac)")
        cur.execute("DELETE FROM paiement WHERE facture_id IN (SELECT id FROM ids_fac)")
        
        # 4. Main entities
        cur.execute("DELETE FROM expedition WHERE id IN (SELECT id FROM ids_exp)")
        cur.execute("DELETE FROM facture WHERE id IN (SELECT id FROM ids_fac)")
        
        # 5. Tournees (unlink leftovers first)
        cur.execute("UPDATE expedition SET tournee_id = NULL WHERE tournee_id IN (SELECT id FROM ids_trn)")
        cur.execute("DELETE FROM tournee WHERE id IN (SELECT id FROM ids_trn)")
        
        # Cleanup temp tables
        cur.execute("DROP TABLE ids_exp")
        cur.execute("DROP TABLE ids_trn")
        cur.execute("DROP TABLE ids_fac")
        cur.execute("DROP TABLE ids_inc")

        # ============================================
        # DATA ENRICHMENT & FIXES (User Request)
        # ============================================
        print("Enriching data: fixing statuses, encoding, balances...")

        # 1. DISTRIBUTION OF TOURNEES (En cours / Préparée)
        # Get recent tournee IDs (e.g., last 4)
        cur.execute("SELECT id FROM tournee ORDER BY date_tournee DESC LIMIT 4")
        recent_tours = [row[0] for row in cur.fetchall()]
        if len(recent_tours) >= 4:
            # Last 2 -> En cours
            cur.execute(f"UPDATE tournee SET statut = 'En cours' WHERE id IN ({recent_tours[0]}, {recent_tours[1]})")
            # Next 2 -> En préparation (Préparée)
            cur.execute(f"UPDATE tournee SET statut = 'Préparée' WHERE id IN ({recent_tours[2]}, {recent_tours[3]})")
        
        # 2. RECLAMATIONS STATUS FIX
        # Normalize to 'En cours', 'Résolue', 'Annulée' matching frontend expectations
        cur.execute("UPDATE reclamation SET statut = 'En cours' WHERE statut LIKE 'en_cours'")
        cur.execute("UPDATE reclamation SET statut = 'Résolue' WHERE statut LIKE 'resolu'")
        cur.execute("UPDATE reclamation SET statut = 'Annulée' WHERE statut LIKE 'annule'")
        
        # 3. FACTURE STATUS FIX
        cur.execute("UPDATE facture SET statut = 'Impayée' WHERE statut = 'impayee'")
        cur.execute("UPDATE facture SET statut = 'Payée' WHERE statut = 'payee'")
        cur.execute("UPDATE facture SET statut = 'Partiellement payée' WHERE statut = 'partiellement_payee'")
        
        # 4. PAIEMENT ENCODING FIX (Mojibake)
        cur.execute("UPDATE paiement SET mode_paiement = 'Espèces' WHERE mode_paiement LIKE 'Esp%'")
        cur.execute("UPDATE paiement SET mode_paiement = 'Chèque' WHERE mode_paiement LIKE 'Ch%'")
        cur.execute("UPDATE paiement SET mode_paiement = 'Virement' WHERE mode_paiement LIKE 'Vir%'")

        # 5. CLIENT STATUS & SOLDE UPDATE
        # Ensure 'Actif' (Title Case) if frontend expects it, or just keep 'actif'. 
        # But 'solde' needs check.
        # Calc: Solde = Note: System usually has Solde = What is DUE (Positive).
        # Calculation: SUM(Factures TTC) - SUM(Paiements)
        cur.execute("""
            UPDATE client 
            SET solde = (
                COALESCE((SELECT SUM(total_ttc) FROM facture WHERE client_id = client.id), 0) - 
                COALESCE((SELECT SUM(montant) FROM paiement WHERE client_id = client.id), 0)
            )
        """)
        
        # 6. VEHICLE DRIVER ASSIGNMENT (If UI looks for missing link)
        # Ensure vehicles in active tours have the chauffeur assigned (if schema supported it).
        # Since schema lacks 'vehicule.chauffeur_id', we rely on tournee.
        # However, checking basic consistency:
        pass 
        
        # 7. EXPEDITION STATUS FIX (Mojibake & Consistency)
        # Fix 'Livré', 'Échec de livraison' which likely have encoding issues
        cur.execute("UPDATE expedition SET statut = 'Livré' WHERE statut LIKE 'Livr%'")
        cur.execute("UPDATE expedition SET statut = 'Échec de livraison' WHERE statut LIKE 'Echec%' OR statut LIKE 'Échec%'")
        cur.execute("UPDATE expedition SET statut = 'En transit' WHERE statut LIKE 'En tran%'")
        cur.execute("UPDATE expedition SET statut = 'En attente' WHERE statut LIKE 'En att%'")
        
        # 8. RECLAMATIONS STATUS FIX (Frontend expects UPPERCASE)
        # Convert 'En cours' -> 'EN_COURS', etc.
        cur.execute("UPDATE reclamation SET statut = 'EN_COURS' WHERE statut LIKE 'En cours' OR statut LIKE 'en_cours'")
        cur.execute("UPDATE reclamation SET statut = 'RESOLUE' WHERE statut LIKE 'Résolue' OR statut LIKE 'resolu'")
        cur.execute("UPDATE reclamation SET statut = 'ANNULEE' WHERE statut LIKE 'Annulée' OR statut LIKE 'annule'")

        # 9. CLIENT STATUS FIX
        # Ensure 'Actif' (Title Case)
        cur.execute("UPDATE client SET statut = 'Actif' WHERE statut LIKE 'actif'")

        # 10. DIVERSIFY EXPEDITIONS
        # Add 'En centre de tri', 'En attente', 'Brouillon'
        cur.execute("UPDATE expedition SET statut = 'En centre de tri' WHERE id % 10 = 5")
        cur.execute("UPDATE expedition SET statut = 'En attente' WHERE id % 10 = 6")
        
        # 11. ADD MISSING GRAPH DATA (Nov/Dec 2025 Terminée Tours)
        # Insert duplicate tours with specific dates and 'Terminée' status to populate fuel graph
        # Using INSERT OR IGNORE to prevent unique constraint errors on re-run
        try:
            cur.execute("""
                INSERT OR IGNORE INTO tournee (code_tournee, date_tournee, statut, consommation_litres, distance_km, chauffeur_id, vehicule_id, created_by) 
                SELECT 'TRN-20251115-99', '2025-11-15', 'Terminée', 45.5, 300, chauffeur_id, vehicule_id, created_by 
                FROM tournee WHERE statut = 'Terminée' LIMIT 1
            """)
            cur.execute("""
                INSERT OR IGNORE INTO tournee (code_tournee, date_tournee, statut, consommation_litres, distance_km, chauffeur_id, vehicule_id, created_by) 
                SELECT 'TRN-20251215-99', '2025-12-15', 'Terminée', 50.2, 320, chauffeur_id, vehicule_id, created_by 
                FROM tournee WHERE statut = 'Terminée' LIMIT 1
            """)
        except Exception as e:
            print(f"Warning: Could not insert fake graph data: {e}")

        con.commit()
        print("DB initialized OK - Django will handle all business logic (no SQL triggers).")
    finally:
        con.close()


if __name__ == "__main__":
    main()
