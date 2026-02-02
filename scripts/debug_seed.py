import sqlite3
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
db_path = base_dir / "backend" / "db.sqlite3"
schema_path = base_dir / "db" / "schema.sql"
seed_path = base_dir / "db" / "complete_seed_2024_2026.sql"

# Delete old DB
if db_path.exists():
    db_path.unlink()

con = sqlite3.connect(db_path)
cur = con.cursor()

try:
    # Disable foreign keys
    con.execute("PRAGMA foreign_keys = OFF;")
    
    # Load schema
    print("Loading schema...")
    schema_sql = schema_path.read_text(encoding='utf-8-sig', errors='ignore')
    cur.executescript(schema_sql)
    print("Schema loaded successfully")
    
    # Load seed with detailed error reporting
    print("\nLoading seed...")
    seed_content = seed_path.read_text(encoding='utf-8-sig', errors='ignore')
    
    # Split by semicolon and execute one by one
    statements = []
    current_stmt = []
    
    for line in seed_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('--'):
            continue
        current_stmt.append(line)
        if line.endswith(';'):
            statements.append(' '.join(current_stmt))
            current_stmt = []
    
    print(f"Found {len(statements)} SQL statements")
    
    for i, stmt in enumerate(statements):
        if i % 10 == 0:
            print(f"Processing statement {i}/{len(statements)}...")
        try:
            cur.execute(stmt)
        except Exception as e:
            print(f"\n❌ ERROR at statement {i}:")
            print(f"Statement preview: {stmt[:300]}...")
            print(f"Error: {e}")
            print("\nStopping here. Fix this statement and try again.")
            break
    else:
        con.commit()
        print("\n✅ All statements executed successfully!")
        
        # Verify data
        print("\n=== DATA VERIFICATION ===")
        print(f"Clients: {cur.execute('SELECT COUNT(*) FROM client').fetchone()[0]}")
        print(f"Factures: {cur.execute('SELECT COUNT(*) FROM facture').fetchone()[0]}")
        print(f"Expeditions: {cur.execute('SELECT COUNT(*) FROM expedition').fetchone()[0]}")
        print(f"Paiements: {cur.execute('SELECT COUNT(*) FROM paiement').fetchone()[0]}")
    
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    con.close()
