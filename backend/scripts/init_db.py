import argparse
import sqlite3
from pathlib import Path


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
        description="Initialize db.sqlite3 from SQL files (schema + data + optional demo seed)."
    )
    parser.add_argument("--reset", action="store_true", help="Delete existing db.sqlite3 and recreate it.")
    parser.add_argument("--seed-demo", action="store_true", help="Load seed_demo.sql for realistic test data.")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent  # backend/
    db_path = base_dir / "db.sqlite3"
    schema_path = base_dir / "db" / "schema.sql"
    data_path = base_dir / "db" / "data.sql"
    seed_demo_path = base_dir / "db" / "seed_demo.sql"

    # Check for required files
    for p in (schema_path, data_path):
        if not p.exists():
            raise SystemExit(f"Missing SQL file: {p}")

    if args.reset and db_path.exists():
        db_path.unlink()

    con = sqlite3.connect(db_path)
    try:
        con.execute("PRAGMA foreign_keys = ON;")
        cur = con.cursor()

        # If db exists and already has tables, don't overwrite unless --reset.
        if not args.reset and _db_has_any_tables(con):
            print(f"DB already initialized: {db_path}")
            if args.seed_demo and seed_demo_path.exists():
                print("Loading seed_demo.sql...")
                _exec_sql_file(cur, seed_demo_path)
                con.commit()
                print("Demo data loaded successfully!")
            return

        print(f"Initializing DB: {db_path}")
        _exec_sql_file(cur, schema_path)
        _exec_sql_file(cur, data_path)
        
        # Load demo seed data if requested
        if args.seed_demo:
            if seed_demo_path.exists():
                print("Loading seed_demo.sql...")
                _exec_sql_file(cur, seed_demo_path)
            else:
                print(f"Warning: seed_demo.sql not found at {seed_demo_path}")
        
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
        
        con.commit()
        print("DB initialized OK - Django will handle all business logic (no SQL triggers).")
    finally:
        con.close()


if __name__ == "__main__":
    main()
