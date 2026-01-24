import os
import sys
import sqlite3
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "db.sqlite3"
SQL_DIR = BASE_DIR / "db"

def run_command(command, cwd=None):
    try:
        subprocess.check_call(command, cwd=cwd, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        sys.exit(1)

def init_db():
    print("============================================")
    print("Database Initialization (Python)")
    print("============================================")
    
    # 1. Check if DB exists
    if DB_FILE.exists():
        print(f"Warning: Database file already exists at {DB_FILE}")
        response = input("Do you want to DELETE it and create a new one? (yes/no): ").lower().strip()
        if response == 'yes':
            try:
                os.remove(DB_FILE)
                print("Deleted existing database.")
            except OSError as e:
                print(f"Error deleting database: {e}")
                print("Make sure no server is running and locking the file.")
                sys.exit(1)
        else:
            print("Operation cancelled.")
            return

    # 2. Run Django Migrations (Creates core structure: auth, permissions, etc.)
    print("\n[1/4] Running Django migrations...")
    # Using sys.executable ensures we use the same python interpreter (venv)
    run_command(f'"{sys.executable}" manage.py migrate', cwd=BASE_DIR)

    # 3. Create Superuser (Admin) if not exists
    print("\n[2/4] Ensuring admin user exists...")
    try:
        # Setup Django environment within this script
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'password123')
            print("Created superuser 'admin' (password: password123)")
        else:
            print("Superuser 'admin' already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")
        # Don't exit, try to continue to SQL scripts which are critical


    # 4. Apply SQL Scripts (Schema updates, Data, Triggers)
    # Note: We skip parts of schema.sql that might conflict if needed, 
    # but based on our manual fix, apply all seems to work if we ignore "table exists" errors gracefully,
    # OR better: we rely on Django for schema and only use data/triggers.
    # However, user's schema.sql has custom tables not managed by django migrations yet?
    # Let's apply them.
    
    print("\n[3/4] Applying SQL scripts...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    scripts = ["schema.sql", "data.sql", "triggers.sql"]
    
    for script_name in scripts:
        script_path = SQL_DIR / script_name
        if script_path.exists():
            print(f"  - Applying {script_name}...")
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                cursor.executescript(sql_script)
            except sqlite3.OperationalError as e:
                # Ignore "table already exists" errors common when mixing methods
                if "already exists" in str(e):
                    print(f"    Notice: Some tables in {script_name} already exist (skipped).")
                else:
                    print(f"    Error applying {script_name}: {e}")
        else:
            print(f"  Warning: {script_name} not found at {script_path}")

    conn.commit()
    conn.close()

    print("\n[4/4] Database initialized successfully!")
    print(f"Location: {DB_FILE}")

if __name__ == "__main__":
    init_db()
