"""
Django management command to load seed data.
Usage: python manage.py load_seed_data
"""
from django.core.management.base import BaseCommand
from django.db import transaction
import sqlite3
from pathlib import Path


class Command(BaseCommand):
    help = 'Load seed data from SQL file into Django models'

    def handle(self, *args, **options):
        self.stdout.write('Loading seed data...')
        
        # Get paths
        backend_dir = Path(__file__).resolve().parent.parent.parent.parent
        project_root = backend_dir.parent
        seed_path = project_root / 'db' / 'complete_seed_2024_2026.sql'
        db_path = backend_dir / 'db.sqlite3'
        
        if not seed_path.exists():
            self.stdout.write(self.style.ERROR(f'Seed file not found: {seed_path}'))
            return
        
        try:
            # Load seed data directly via SQLite with foreign keys disabled
            # This bypasses Django ORM but works with Django-created tables
            con = sqlite3.connect(str(db_path))
            con.execute('PRAGMA foreign_keys = OFF;')
            cur = con.cursor()
            
            # Read seed file
            seed_content = seed_path.read_text(encoding='utf-8', errors='replace')
            
            # Replace table names with core_ prefix
            tables = [
                'role', 'utilisateur', 'audit_log', 'password_reset_token', 'favori',
                'client', 'chauffeur', 'vehicule', 'destination', 'type_service', 
                'tarification', 'tournee', 'expedition', 'tracking_expedition',
                'facture', 'facture_expedition', 'paiement', 'incident', 'reclamation',
                'reclamation_expedition', 'incident_attachment', 'alerte'
            ]
            
            # More comprehensive table name replacement
            import re
            
            # First, remove all DELETE statements since Django creates empty tables
            seed_content = re.sub(r'DELETE\s+FROM\s+\w+;', '', seed_content, flags=re.IGNORECASE)
            
            # Now replace table names in remaining statements
            for table in tables:
                # Use word boundaries to avoid partial matches
                seed_content = re.sub(rf'\bINSERT\s+INTO\s+{table}\s', f'INSERT INTO core_{table} ', seed_content, flags=re.IGNORECASE)
                seed_content = re.sub(rf'\bUPDATE\s+{table}\s', f'UPDATE core_{table} ', seed_content, flags=re.IGNORECASE)
                seed_content = re.sub(rf'\bFROM\s+{table}\b', f'FROM core_{table}', seed_content, flags=re.IGNORECASE)
            
            # Execute the modified seed
            self.stdout.write('Executing seed SQL...')
            cur.executescript(seed_content)
            con.commit()
            con.close()
            
            self.stdout.write(self.style.SUCCESS('Seed data loaded successfully!'))
            self.stdout.write(self.style.WARNING('Remember to run: python ../scripts/apply_data_fixes.py'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading seed data: {e}'))
            import traceback
            traceback.print_exc()
