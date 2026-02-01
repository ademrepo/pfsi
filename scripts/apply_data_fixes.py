
import sqlite3
import os

DB_PATH = 'backend/db.sqlite3'

def apply_fixes():
    print(f"Connecting to {DB_PATH}...")
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        
        print("Applying data fixes...")

        # 7. EXPEDITION STATUS FIX
        cur.execute("UPDATE expedition SET statut = 'Livré' WHERE statut LIKE 'Livr%'")
        cur.execute("UPDATE expedition SET statut = 'Échec de livraison' WHERE statut LIKE 'Echec%' OR statut LIKE 'Échec%'")
        cur.execute("UPDATE expedition SET statut = 'En transit' WHERE statut LIKE 'En tran%'")
        cur.execute("UPDATE expedition SET statut = 'En attente' WHERE statut LIKE 'En att%'")
        
        # 8. RECLAMATIONS STATUS FIX
        cur.execute("UPDATE reclamation SET statut = 'EN_COURS' WHERE statut LIKE 'En cours' OR statut LIKE 'en_cours'")
        cur.execute("UPDATE reclamation SET statut = 'RESOLUE' WHERE statut LIKE 'Résolue' OR statut LIKE 'resolu'")
        cur.execute("UPDATE reclamation SET statut = 'ANNULEE' WHERE statut LIKE 'Annulée' OR statut LIKE 'annule'")

        # 9. CLIENT STATUS FIX
        cur.execute("UPDATE client SET statut = 'Actif' WHERE statut LIKE 'actif'")

        # 10. DIVERSIFY EXPEDITIONS
        # Add 'En centre de tri', 'En attente'
        cur.execute("UPDATE expedition SET statut = 'En centre de tri' WHERE id % 10 = 5")
        cur.execute("UPDATE expedition SET statut = 'En attente' WHERE id % 10 = 6")
        
        # 11. ADD MISSING GRAPH DATA (Nov/Dec 2025 Terminée Tours)
        try:
            # Check if they already exist to avoid duplicates if re-run
            cur.execute("SELECT count(*) FROM tournee WHERE code_tournee IN ('TRN-20251115-99', 'TRN-20251215-99')")
            count = cur.fetchone()[0]
            if count == 0:
                print("Inserting missing graph data for Nov/Dec...")
                cur.execute("""
                    INSERT INTO tournee (code_tournee, date_tournee, statut, consommation_litres, distance_km, chauffeur_id, vehicule_id, created_by) 
                    SELECT 'TRN-20251115-99', '2025-11-15', 'Terminée', 45.5, 300, chauffeur_id, vehicule_id, created_by 
                    FROM tournee WHERE statut = 'Terminée' LIMIT 1
                """)
                cur.execute("""
                    INSERT INTO tournee (code_tournee, date_tournee, statut, consommation_litres, distance_km, chauffeur_id, vehicule_id, created_by) 
                    SELECT 'TRN-20251215-99', '2025-12-15', 'Terminée', 50.2, 320, chauffeur_id, vehicule_id, created_by 
                    FROM tournee WHERE statut = 'Terminée' LIMIT 1
                """)
            else:
                print("Graph data already exists.")
        except Exception as e:
            print(f"Warning: Could not insert fake graph data: {e}")

        con.commit()
        print("Fixes applied successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'con' in locals():
            con.close()

if __name__ == "__main__":
    apply_fixes()
