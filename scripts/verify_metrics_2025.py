import sqlite3
import datetime

def verify():
    con = sqlite3.connect("c:/L3 ISIL A 2025-2026/PFKHRA/backend/db.sqlite3")
    cur = con.cursor()
    
    print("--- VERIFICATION ---")
    
    # 1. Counts per Month
    cur.execute("SELECT strftime('%Y-%m', date_creation), COUNT(*) FROM expedition GROUP BY 1 ORDER BY 1")
    months = cur.fetchall()
    print("Expeditions per month:", months)
    
    # 2. Active Status
    cur.execute("SELECT COUNT(*) FROM tournee WHERE statut IN ('En cours', 'Planifiée')")
    active_trn = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM expedition WHERE statut = 'En transit'")
    active_exp = cur.fetchone()[0]
    print(f"Active Tournees: {active_trn}, Active Expeditions: {active_exp}")
    
    # 3. Finance
    cur.execute("SELECT COUNT(*), SUM(total_ttc) FROM facture WHERE statut='impayée'")
    unpaid = cur.fetchone()
    print(f"Unpaid Invoices: {unpaid[0]} (Total: {unpaid[1]:.2f} DA)")
    
    cur.execute("SELECT COUNT(*) FROM paiement")
    payments = cur.fetchone()[0]
    print(f"Total Payments recorded: {payments}")
    
    # 4. Solde Clients
    cur.execute("SELECT COUNT(*), SUM(solde) FROM client WHERE solde > 0")
    debtors = cur.fetchone()
    print(f"Clients with debt: {debtors[0]} (Total Debt: {debtors[1]:.2f} DA)")
    
    con.close()

if __name__ == "__main__":
    verify()
