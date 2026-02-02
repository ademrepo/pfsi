import sqlite3
import os

db_path = 'backend/db.sqlite3'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

con = sqlite3.connect(db_path)
cur = con.cursor()

print('=== STATUS COUNTS ===')
for row in cur.execute('SELECT statut, COUNT(*) FROM expedition GROUP BY statut'):
    print(row)

print('\n=== DATES (YYYY-MM) ===')
for row in cur.execute("SELECT strftime('%Y-%m', date_creation), COUNT(*) FROM expedition GROUP BY strftime('%Y-%m', date_creation) ORDER BY 1 DESC LIMIT 10"):
    print(row)

con.close()
