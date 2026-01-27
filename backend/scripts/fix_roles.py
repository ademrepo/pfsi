import sqlite3
from pathlib import Path


def main() -> int:
    base_dir = Path(__file__).resolve().parent.parent  # pfsi/backend
    db_path = base_dir / "db.sqlite3"
    if not db_path.exists():
        print(f"DB not found: {db_path}")
        return 1

    desired_roles_by_username = {
        "admin": "ADMIN",
        "agent1": "AGENT",
        "agent2": "AGENT",
        "comptable1": "COMPTABLE",
        "logistique1": "LOGISTIQUE",
    }

    con = sqlite3.connect(db_path)
    try:
        cur = con.cursor()

        role_rows = cur.execute("SELECT id, code FROM role").fetchall()
        role_id_by_code = {code: role_id for (role_id, code) in role_rows}
        missing = sorted({c for c in desired_roles_by_username.values() if c not in role_id_by_code})
        if missing:
            print(f"Missing role codes in DB: {missing}")
            return 1

        updated = 0
        for username, role_code in desired_roles_by_username.items():
            role_id = role_id_by_code[role_code]
            row = cur.execute("SELECT id, role_id FROM utilisateur WHERE username = ?", (username,)).fetchone()
            if not row:
                continue
            user_id, current_role_id = row
            if current_role_id == role_id:
                continue
            cur.execute("UPDATE utilisateur SET role_id = ? WHERE id = ?", (role_id, user_id))
            updated += 1

        con.commit()
        print(f"Updated {updated} user(s) in {db_path.name}.")
        return 0
    finally:
        con.close()


if __name__ == "__main__":
    raise SystemExit(main())

