#!/usr/bin/env python
"""
Script to fix database integrity issues before running migrations
"""
import os
import sys
import django
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

from django.db import connection

def fix_database_integrity():
    """Fix foreign key constraint violations"""
    print("Fixing database integrity issues...")
    
    with connection.cursor() as cursor:
        # Check if expedition table exists and has problematic data
        try:
            cursor.execute("SELECT COUNT(*) FROM expedition WHERE client_id NOT IN (SELECT id FROM client)")
            orphaned_expeditions = cursor.fetchone()[0]
            print(f"Found {orphaned_expeditions} expeditions with invalid client references")
            
            if orphaned_expeditions > 0:
                # Delete orphaned expeditions
                cursor.execute("""
                    DELETE FROM expedition 
                    WHERE client_id NOT IN (SELECT id FROM client)
                """)
                print(f"Deleted {cursor.rowcount} orphaned expeditions")
            
            # Check for other foreign key violations
            cursor.execute("SELECT COUNT(*) FROM expedition WHERE type_service_id NOT IN (SELECT id FROM type_service)")
            orphaned_services = cursor.fetchone()[0]
            if orphaned_services > 0:
                cursor.execute("""
                    DELETE FROM expedition 
                    WHERE type_service_id NOT IN (SELECT id FROM type_service)
                """)
                print(f"Deleted {cursor.rowcount} expeditions with invalid service references")
            
            cursor.execute("SELECT COUNT(*) FROM expedition WHERE destination_id NOT IN (SELECT id FROM destination)")
            orphaned_destinations = cursor.fetchone()[0]
            if orphaned_destinations > 0:
                cursor.execute("""
                    DELETE FROM expedition 
                    WHERE destination_id NOT IN (SELECT id FROM destination)
                """)
                print(f"Deleted {cursor.rowcount} expeditions with invalid destination references")
            
            # Check for tracking entries with invalid expedition references
            cursor.execute("SELECT COUNT(*) FROM tracking_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
            orphaned_tracking = cursor.fetchone()[0]
            if orphaned_tracking > 0:
                cursor.execute("""
                    DELETE FROM tracking_expedition 
                    WHERE expedition_id NOT IN (SELECT id FROM expedition)
                """)
                print(f"Deleted {cursor.rowcount} tracking entries with invalid expedition references")
            
            # Check for incidents with invalid expedition references
            cursor.execute("SELECT COUNT(*) FROM incident WHERE expedition_id NOT IN (SELECT id FROM expedition)")
            orphaned_incidents = cursor.fetchone()[0]
            if orphaned_incidents > 0:
                cursor.execute("""
                    DELETE FROM incident 
                    WHERE expedition_id NOT IN (SELECT id FROM expedition)
                """)
                print(f"Deleted {cursor.rowcount} incidents with invalid expedition references")
            
            # Check for facture_expedition entries with invalid references
            cursor.execute("SELECT COUNT(*) FROM facture_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
            orphaned_facture_expeditions = cursor.fetchone()[0]
            if orphaned_facture_expeditions > 0:
                cursor.execute("""
                    DELETE FROM facture_expedition 
                    WHERE expedition_id NOT IN (SELECT id FROM expedition)
                """)
                print(f"Deleted {cursor.rowcount} facture_expedition entries with invalid expedition references")
            
            # Check for reclamation_expedition entries with invalid references
            cursor.execute("SELECT COUNT(*) FROM reclamation_expedition WHERE expedition_id NOT IN (SELECT id FROM expedition)")
            orphaned_reclamation_expeditions = cursor.fetchone()[0]
            if orphaned_reclamation_expeditions > 0:
                cursor.execute("""
                    DELETE FROM reclamation_expedition 
                    WHERE expedition_id NOT IN (SELECT id FROM expedition)
                """)
                print(f"Deleted {cursor.rowcount} reclamation_expedition entries with invalid expedition references")
            
            # Check for alertes with invalid expedition references
            cursor.execute("SELECT COUNT(*) FROM alerte WHERE expedition_id NOT IN (SELECT id FROM expedition)")
            orphaned_alertes = cursor.fetchone()[0]
            if orphaned_alertes > 0:
                cursor.execute("""
                    DELETE FROM alerte 
                    WHERE expedition_id NOT IN (SELECT id FROM expedition)
                """)
                print(f"Deleted {cursor.rowcount} alertes with invalid expedition references")
            
            print("Database integrity issues fixed!")
            
        except Exception as e:
            print(f"Error checking database: {e}")
            # If tables don't exist yet, that's fine - we'll create them with migrations

if __name__ == "__main__":
    fix_database_integrity()