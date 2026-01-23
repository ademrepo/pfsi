import argparse
import sqlite3
from pathlib import Path


def _exec_sql_file(cur, path: Path):
    sql = path.read_text(encoding="utf-8", errors="replace")
    cur.executescript(sql)


def _db_has_any_tables(con: sqlite3.Connection) -> bool:
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return cur.fetchone() is not None


def main():
    parser = argparse.ArgumentParser(
        description="Initialize 16avril/db.sqlite3 from SQL files (schema + triggers + data)."
    )
    parser.add_argument("--reset", action="store_true", help="Delete existing db.sqlite3 and recreate it.")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent  # 16avril/
    db_path = base_dir / "db.sqlite3"
    schema_path = base_dir / "db" / "schema.sql"
    triggers_path = base_dir / "db" / "triggers.sql"
    data_path = base_dir / "db" / "data.sql"

    for p in (schema_path, triggers_path, data_path):
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
            return

        print(f"Initializing DB: {db_path}")
        _exec_sql_file(cur, schema_path)
        _exec_sql_file(cur, triggers_path)
        _exec_sql_file(cur, data_path)
        con.commit()
        print("DB initialized OK.")
    finally:
        con.close()


if __name__ == "__main__":
    main()

