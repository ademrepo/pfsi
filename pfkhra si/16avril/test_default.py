import os
import sys
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

from core.models import Client, Destination, TypeService, Expedition, Facture, FactureExpedition
from django.db.models import Max

def test():
    print("Testing default values...")
    try:
        # Create dependencies
        client = Client.objects.first()
        dest = Destination.objects.first()
        srv = TypeService.objects.first()
        if not client or not dest or not srv:
            print("Missing deps")
            return

        # Create Expedition explicitly
        print("Creating Expedition...")
        exp = Expedition.objects.create(
            client=client, destination=dest, type_service=srv,
            poids_kg=10, volume_m3=1,
            code_expedition=f"TEST-{datetime.datetime.now().timestamp()}",
            est_facturee=False 
        )
        print(f"Expedition created. ID={exp.id}, est_facturee={exp.est_facturee}")
        
        print("Refreshing from DB...")
        exp.refresh_from_db()
        print(f"Refreshed. est_facturee={exp.est_facturee} (Type: {type(exp.est_facturee)})")
        
        # Create Facture
        print("Creating Facture...")
        fac = Facture.objects.create(
            numero_facture=f"TESTFAC-{datetime.datetime.now().timestamp()}",
            client=client,
            statut='Emise'
        )
        print(f"Facture created. ID={fac.id}")
        
        # Link
        print("Linking...")
        sys.stdout.flush()
        FactureExpedition.objects.create(facture=fac, expedition=exp)
        print("Link created successfully.")
        
        print("Checking status after link...")
        exp.refresh_from_db()
        print(f"Refreshed. est_facturee={exp.est_facturee}")
        
    except Exception as e:
        print("\nERROR:")
        print(e)
        
if __name__ == '__main__':
    test()
