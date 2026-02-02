import sqlite3 
import os 


SCRIPT_DIR =os .path .dirname (os .path .abspath (__file__ ))
PROJECT_ROOT =os .path .dirname (SCRIPT_DIR )
DB_PATH =os .path .join (PROJECT_ROOT ,'backend','db.sqlite3')

def thin_database ():
    if not os .path .exists (DB_PATH ):
        print (f"Database not found at {DB_PATH }")
        return 

    print ("=== STARTING DATABASE THINNING (Removing 2024 Data) ===")

    con =sqlite3 .connect (DB_PATH )
    cur =con .cursor ()

    try :

        cur .execute ("PRAGMA foreign_keys = OFF;")


        print ("Enforcing 'Balanced Volume' (Top 150 Recent)...")


        cur .execute ("SELECT id FROM expedition ORDER BY id DESC LIMIT 150")
        ids_to_keep =[row [0 ]for row in cur .fetchall ()]

        if not ids_to_keep :
            print ("  - No expeditions found to keep!")
        else :
            id_list_str =','.join (map (str ,ids_to_keep ))
            print (f"  - Keeping {len (ids_to_keep )} expeditions (IDs: {id_list_str })")
            cur .execute (f"DELETE FROM expedition WHERE id NOT IN ({id_list_str })")
            print (f"  - Deleted {cur .rowcount } excess expeditions.")


        print ("Removing unused clients...")
        cur .execute (f"DELETE FROM client WHERE id NOT IN (SELECT DISTINCT client_id FROM expedition)")
        print (f"  - Deleted {cur .rowcount } unused clients.")














        cur .execute (f"SELECT facture_id FROM facture_expedition WHERE expedition_id IN ({id_list_str })")
        valid_facture_ids =[str (row [0 ])for row in cur .fetchall ()]

        if valid_facture_ids :
            valid_facture_str =','.join (valid_facture_ids )
            print (f"  - Keeping {len (valid_facture_ids )} factures linked to kept expeditions.")
            cur .execute (f"DELETE FROM facture WHERE id NOT IN ({valid_facture_str })")
        else :
            print ("  - No valid factures found linked to kept expeditions. Clearing all factures...")
            cur .execute ("DELETE FROM facture")

        print (f"  - Deleted {cur .rowcount } orphaned factures.")



        cur .execute ("DELETE FROM tournee WHERE id NOT IN (SELECT DISTINCT tournee_id FROM expedition WHERE tournee_id IS NOT NULL)")
        print (f"  - Deleted {cur .rowcount } empty tournees.")


        print ("Cleaning up orphaned records...")


        cur .execute ("DELETE FROM tracking_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
        print (f"  - Deleted {cur .rowcount } orphaned tracking records (missing expedition).")
        cur .execute ("DELETE FROM tracking_expedition WHERE tournee_id NOT IN (SELECT id FROM tournee) AND tournee_id IS NOT NULL")
        print (f"  - Deleted {cur .rowcount } orphaned tracking records (missing tournee).")


        cur .execute ("DELETE FROM facture_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
        print (f"  - Deleted {cur .rowcount } orphaned facture-expedition links (missing expedition).")
        cur .execute ("DELETE FROM facture_expedition WHERE facture_id NOT IN (SELECT id FROM facture)")
        print (f"  - Deleted {cur .rowcount } orphaned facture-expedition links (missing facture).")


        cur .execute ("DELETE FROM paiement WHERE facture_id NOT IN (SELECT id FROM facture)")
        print (f"  - Deleted {cur .rowcount } orphaned paiements.")


        cur .execute ("DELETE FROM reclamation WHERE expedition_id IS NOT NULL AND expedition_id NOT IN (SELECT id FROM expedition)")
        print (f"  - Deleted {cur .rowcount } orphaned reclamations (missing expedition).")
        cur .execute ("DELETE FROM reclamation WHERE facture_id IS NOT NULL AND facture_id NOT IN (SELECT id FROM facture)")
        print (f"  - Deleted {cur .rowcount } orphaned reclamations (missing facture).")


        cur .execute ("DELETE FROM reclamation_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
        print (f"  - Deleted {cur .rowcount } orphaned reclamation-expedition links.")


        cur .execute ("DELETE FROM incident WHERE expedition_id IS NOT NULL AND expedition_id NOT IN (SELECT id FROM expedition)")
        print (f"  - Deleted {cur .rowcount } orphaned incidents (missing expedition).")
        cur .execute ("DELETE FROM incident WHERE tournee_id IS NOT NULL AND tournee_id NOT IN (SELECT id FROM tournee)")
        print (f"  - Deleted {cur .rowcount } orphaned incidents (missing tournee).")


        cur .execute ("DELETE FROM incident_attachment WHERE incident_id NOT IN (SELECT id FROM incident)")
        print (f"  - Deleted {cur .rowcount } orphaned incident attachments.")



        cur .execute ("DELETE FROM alerte WHERE incident_id IS NOT NULL AND incident_id NOT IN (SELECT id FROM incident)")
        print (f"  - Deleted {cur .rowcount } orphaned alertes (missing incident).")
        cur .execute ("DELETE FROM alerte WHERE tournee_id IS NOT NULL AND tournee_id NOT IN (SELECT id FROM tournee)")
        print (f"  - Deleted {cur .rowcount } orphaned alertes (missing tournee).")
        cur .execute ("DELETE FROM alerte WHERE expedition_id IS NOT NULL AND expedition_id NOT IN (SELECT id FROM expedition)")
        print (f"  - Deleted {cur .rowcount } orphaned alertes (missing expedition).")

        con .commit ()


        cur .execute ("PRAGMA foreign_keys = ON;")


        print ("Optimizing database storage (VACUUM)...")
        con .execute ("VACUUM")

        print ("=== DATABASE THINNING COMPLETE ===")

    except Exception as e :
        print (f"ERROR: {e }")
        con .rollback ()
    finally :
        con .close ()

if __name__ =="__main__":
    thin_database ()
