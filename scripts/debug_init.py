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
    cur.executescript(schema_path.read_text(encoding='utf-8', errors='replace'))
    
    # Load seed with detailed error reporting
    print("Loading seed...")
    seed_content = seed_path.read_text(encoding='utf-8', errors='replace')
    
    # Split by statement and execute one by one to find the error
    statements = seed_content.split(';')
    for i, stmt in enumerate(statements):
        stmt = stmt.strip()
        if stmt:
            try:
                cur.execute(stmt)
            except Exception as e:
                print(f"Error at statement {i}:")
                print(f"Statement: {stmt[:200]}...")
                print(f"Error: {e}")
                raise
    
    con.commit()
    print("Success!")
    
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    con.close()
