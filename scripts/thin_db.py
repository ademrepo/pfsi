import sqlite3
import os

# Robust path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'backend', 'db.sqlite3')

def thin_database():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    print("=== STARTING DATABASE THINNING (Removing 2024 Data) ===")
    
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        # Disable foreign keys to allow deleting parents
        cur.execute("PRAGMA foreign_keys = OFF;")

        # 1. Balanced Thinning: Keep latest 150 expeditions (Sweet spot)
        print("Enforcing 'Balanced Volume' (Top 150 Recent)...")
        
        # Get list of IDs to keep (Latest 150 expeditions)
        cur.execute("SELECT id FROM expedition ORDER BY id DESC LIMIT 150")
        ids_to_keep = [row[0] for row in cur.fetchall()]
        
        if not ids_to_keep:
            print("  - No expeditions found to keep!")
        else:
            id_list_str = ','.join(map(str, ids_to_keep))
            print(f"  - Keeping {len(ids_to_keep)} expeditions (IDs: {id_list_str})")
            cur.execute(f"DELETE FROM expedition WHERE id NOT IN ({id_list_str})")
            print(f"  - Deleted {cur.rowcount} excess expeditions.")

        # Cleanup Unused Clients (Performance Boost)
        print("Removing unused clients...")
        cur.execute(f"DELETE FROM client WHERE id NOT IN (SELECT DISTINCT client_id FROM expedition)")
        print(f"  - Deleted {cur.rowcount} unused clients.")


        # Delete orphan Factures (factures not linked to remaining expeditions)
        # Note: Some factures might not be linked to expeditions (direct factures? rare in this seed).
        # We'll strictly delete factures that were linked to DELETED expeditions.
        # But wait, we deleted the expeditions already so we lost the link? 
        # No, 'facture_expedition' still exists (foreign keys off).
        # So we can find factures linked to deleted expeditions.
        
        # Simpler: Delete any facture OLDER than Sept 2025 (General Cleanup)
        # AND keep factures linked to the kept expeditions.
        
        # Actually, let's just keep factures linked to the kept expeditions
        # Get Facture IDs linked to kept expeditions
        cur.execute(f"SELECT facture_id FROM facture_expedition WHERE expedition_id IN ({id_list_str})")
        valid_facture_ids = [str(row[0]) for row in cur.fetchall()]
        
        if valid_facture_ids:
            valid_facture_str = ','.join(valid_facture_ids)
            print(f"  - Keeping {len(valid_facture_ids)} factures linked to kept expeditions.")
            cur.execute(f"DELETE FROM facture WHERE id NOT IN ({valid_facture_str})")
        else:
            print("  - No valid factures found linked to kept expeditions. Clearing all factures...")
            cur.execute("DELETE FROM facture")
            
        print(f"  - Deleted {cur.rowcount} orphaned factures.")

        # Delete Tournees that have NO expeditions remaining
        # (This cleans up empty tournees)
        cur.execute("DELETE FROM tournee WHERE id NOT IN (SELECT DISTINCT tournee_id FROM expedition WHERE tournee_id IS NOT NULL)")
        print(f"  - Deleted {cur.rowcount} empty tournees.")

        # 2. Delete Orphans (Records that lost their parents)
        print("Cleaning up orphaned records...")

        # Tracking (Linked to Expedition or Tournee)
        cur.execute("DELETE FROM tracking_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
        print(f"  - Deleted {cur.rowcount} orphaned tracking records (missing expedition).")
        cur.execute("DELETE FROM tracking_expedition WHERE tournee_id NOT IN (SELECT id FROM tournee) AND tournee_id IS NOT NULL")
        print(f"  - Deleted {cur.rowcount} orphaned tracking records (missing tournee).")

        # Facture-Expedition Link (Linked to Facture or Expedition)
        cur.execute("DELETE FROM facture_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
        print(f"  - Deleted {cur.rowcount} orphaned facture-expedition links (missing expedition).")
        cur.execute("DELETE FROM facture_expedition WHERE facture_id NOT IN (SELECT id FROM facture)")
        print(f"  - Deleted {cur.rowcount} orphaned facture-expedition links (missing facture).")

        # Paiement (Linked to Facture)
        cur.execute("DELETE FROM paiement WHERE facture_id NOT IN (SELECT id FROM facture)")
        print(f"  - Deleted {cur.rowcount} orphaned paiements.")

        # Reclamation (Linked to Expedition or Facture)
        cur.execute("DELETE FROM reclamation WHERE expedition_id IS NOT NULL AND expedition_id NOT IN (SELECT id FROM expedition)")
        print(f"  - Deleted {cur.rowcount} orphaned reclamations (missing expedition).")
        cur.execute("DELETE FROM reclamation WHERE facture_id IS NOT NULL AND facture_id NOT IN (SELECT id FROM facture)")
        print(f"  - Deleted {cur.rowcount} orphaned reclamations (missing facture).")
        
        # Reclamation-Expedition Link
        cur.execute("DELETE FROM reclamation_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
        print(f"  - Deleted {cur.rowcount} orphaned reclamation-expedition links.")

        # Incident (Linked to Expedition or Tournee)
        cur.execute("DELETE FROM incident WHERE expedition_id IS NOT NULL AND expedition_id NOT IN (SELECT id FROM expedition)")
        print(f"  - Deleted {cur.rowcount} orphaned incidents (missing expedition).")
        cur.execute("DELETE FROM incident WHERE tournee_id IS NOT NULL AND tournee_id NOT IN (SELECT id FROM tournee)")
        print(f"  - Deleted {cur.rowcount} orphaned incidents (missing tournee).")

        # IncidentAttachment (Linked to Incident)
        cur.execute("DELETE FROM incident_attachment WHERE incident_id NOT IN (SELECT id FROM incident)")
        print(f"  - Deleted {cur.rowcount} orphaned incident attachments.")


        # Alerte (Linked to Incident, Tournee, or Expedition)
        cur.execute("DELETE FROM alerte WHERE incident_id IS NOT NULL AND incident_id NOT IN (SELECT id FROM incident)")
        print(f"  - Deleted {cur.rowcount} orphaned alertes (missing incident).")
        cur.execute("DELETE FROM alerte WHERE tournee_id IS NOT NULL AND tournee_id NOT IN (SELECT id FROM tournee)")
        print(f"  - Deleted {cur.rowcount} orphaned alertes (missing tournee).")
        cur.execute("DELETE FROM alerte WHERE expedition_id IS NOT NULL AND expedition_id NOT IN (SELECT id FROM expedition)")
        print(f"  - Deleted {cur.rowcount} orphaned alertes (missing expedition).")

        con.commit()
        
        # Re-enable foreign keys
        cur.execute("PRAGMA foreign_keys = ON;")
        
        # Optimize storage
        print("Optimizing database storage (VACUUM)...")
        con.execute("VACUUM")
        
        print("=== DATABASE THINNING COMPLETE ===")

    except Exception as e:
        print(f"ERROR: {e}")
        con.rollback()
    finally:
        con.close()

if __name__ == "__main__":
    thin_database()
