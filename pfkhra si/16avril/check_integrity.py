import os
import django
from django.conf import settings

# Setup Django standalone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

from core.models import Expedition, Client, Destination, TypeService, Tournee, Chauffeur, Vehicule

def check_integrity():
    print("Checking Expedition Integrity...")
    expeditions = Expedition.objects.all()
    for exp in expeditions:
        issues = []
        # Check Client
        if exp.client_id:
            if not Client.objects.filter(id=exp.client_id).exists():
                issues.append(f"Invalid client_id {exp.client_id}")
        
        # Check Destination
        if exp.destination_id:
            if not Destination.objects.filter(id=exp.destination_id).exists():
                issues.append(f"Invalid destination_id {exp.destination_id}")

        # Check TypeService
        if exp.type_service_id:
            if not TypeService.objects.filter(id=exp.type_service_id).exists():
                issues.append(f"Invalid type_service_id {exp.type_service_id}")
                
        if issues:
            print(f"Expedition {exp.id} / {exp.code_expedition}: {', '.join(issues)}")
        else:
            pass # print(f"Expedition {exp.id} OK")

    print("\nChecking Tournee Integrity...")
    tournees = Tournee.objects.all()
    for t in tournees:
        issues = []
        if t.chauffeur_id and not Chauffeur.objects.filter(id=t.chauffeur_id).exists():
            issues.append(f"Invalid chauffeur_id {t.chauffeur_id}")
        if t.vehicule_id and not Vehicule.objects.filter(id=t.vehicule_id).exists():
             issues.append(f"Invalid vehicule_id {t.vehicule_id}")
             
        if issues:
             print(f"Tournee {t.id} / {t.code_tournee}: {', '.join(issues)}")

if __name__ == '__main__':
    check_integrity()
