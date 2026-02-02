import sqlite3
import os
from datetime import datetime

db_path = 'backend/db.sqlite3'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

con = sqlite3.connect(db_path)
cur = con.cursor()

print('=== TOTAL EXPEDITIONS ===')
count = cur.execute('SELECT COUNT(*) FROM expedition').fetchone()[0]
print(f"Total: {count}")

print('\n=== EXPEDITIONS IN FEB 2026 ===')
# Check exact format in DB
rows = cur.execute("SELECT code_expedition, date_creation, statut FROM expedition WHERE date_creation LIKE '2026-02%'").fetchall()
if not rows:
    print("No expeditions found for 2026-02")
    
    # Check what months DO have data
    print("\nMonths with data:")
    months = cur.execute("SELECT strftime('%Y-%m', date_creation), COUNT(*) FROM expedition GROUP BY 1 ORDER BY 1 DESC LIMIT 5").fetchall()
    for m in months:
        print(f"  {m[0]}: {m[1]} records")
else:
    print(f"Found {len(rows)} records in Feb 2026:")
    for row in rows:
        print(f"  {row[0]} | {row[1]} | {row[2]}")

con.close()
