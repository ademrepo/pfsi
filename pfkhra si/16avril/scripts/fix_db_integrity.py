#!/usr/bin/env python3
"""
Database integrity fix script for PF KHRA project.
This script fixes foreign key constraint violations in the expedition table.
Run this after init_db.py to ensure database integrity before migrations.
"""

import sqlite3
from pathlib import Path


def fix_foreign_key_constraints():
    """Fix foreign key constraint violations in expedition table."""
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "db.sqlite3"
    
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        print("Please run 'python scripts/init_db.py' first.")
        return False
    
    con = sqlite3.connect(db_path)
    try:
        con.execute("PRAGMA foreign_keys = ON;")
        cur = con.cursor()
        
        print("Checking for foreign key constraint violations...")
        
        # Fix client_id references
        cur.execute("""
            UPDATE expedition 
            SET client_id = NULL 
            WHERE client_id NOT IN (SELECT id FROM client)
        """)
        client_fixes = cur.rowcount
        
        # Fix destination_id references  
        cur.execute("""
            UPDATE expedition 
            SET destination_id = NULL 
            WHERE destination_id NOT IN (SELECT id FROM destination)
        """)
        dest_fixes = cur.rowcount
        
        # Fix type_service_id references
        cur.execute("""
            UPDATE expedition 
            SET type_service_id = NULL 
            WHERE type_service_id NOT IN (SELECT id FROM type_service)
        """)
        service_fixes = cur.rowcount
        
        # Fix tournee_id references
        cur.execute("""
            UPDATE expedition 
            SET tournee_id = NULL 
            WHERE tournee_id NOT IN (SELECT id FROM tournee)
        """)
        tournee_fixes = cur.rowcount
        
        con.commit()
        
        total_fixes = client_fixes + dest_fixes + service_fixes + tournee_fixes
        
        if total_fixes > 0:
            print(f"✓ Fixed {total_fixes} foreign key constraint violations:")
            print(f"  - client_id: {client_fixes} fixes")
            print(f"  - destination_id: {dest_fixes} fixes") 
            print(f"  - type_service_id: {service_fixes} fixes")
            print(f"  - tournee_id: {tournee_fixes} fixes")
        else:
            print("✓ No foreign key constraint violations found.")
        
        # Verify no remaining issues
        cur.execute("""
            SELECT COUNT(*) FROM expedition e
            LEFT JOIN client c ON e.client_id = c.id
            LEFT JOIN destination d ON e.destination_id = d.id
            LEFT JOIN type_service ts ON e.type_service_id = ts.id
            LEFT JOIN tournee t ON e.tournee_id = t.id
            WHERE c.id IS NULL AND e.client_id IS NOT NULL
               OR d.id IS NULL AND e.destination_id IS NOT NULL
               OR ts.id IS NULL AND e.type_service_id IS NOT NULL
               OR t.id IS NULL AND e.tournee_id IS NOT NULL
        """)
        remaining_issues = cur.fetchone()[0]
        
        if remaining_issues == 0:
            print("✓ Database integrity verified - ready for Django migrations!")
            return True
        else:
            print(f"⚠ Warning: {remaining_issues} issues remaining")
            return False
            
    except Exception as e:
        print(f"Error fixing database: {e}")
        con.rollback()
        return False
    finally:
        con.close()


if __name__ == "__main__":
    success = fix_foreign_key_constraints()
    if not success:
        exit(1)
