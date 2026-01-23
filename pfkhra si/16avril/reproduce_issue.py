import os
import sys
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

from core.models import Client, Destination, TypeService, Expedition, Facture
from core.serializers import ExpeditionSerializer
from rest_framework.exceptions import ValidationError

def reproduce():
    print("Starting reproduction script...")
    
    # 1. Get or create dependencies
    client = Client.objects.first()
    if not client:
        print("Creating dummy client...")
        client = Client.objects.create(
            nom="Test Client", 
            code_client="CLI-TEST", 
            email="test@example.com"
        )
    
    dest = Destination.objects.first()
    if not dest:
        print("Creating dummy destination...")
        dest = Destination.objects.create(
            ville="Paris", 
            pays="France", 
            tarif_base_defaut=100
        )
        
    service = TypeService.objects.first()
    if not service:
        print("Creating dummy service...")
        service = TypeService.objects.create(
            libelle="Express", 
            code="EXP"
        )

    print(f"Using Client: {client.id}, Dest: {dest.id}, Service: {service.id}")

    # 2. Prepare data
    data = {
        'client': client.id,
        'destination': dest.id,
        'type_service': service.id,
        'poids_kg': 10.0,
        'volume_m3': 2.5,
        'description_colis': 'Test package',
        'nom_destinataire': 'John Doe',
        'adresse_livraison': '123 Main St'
    }

    # 3. Use Serializer
    serializer = ExpeditionSerializer(data=data)
    if serializer.is_valid():
        try:
            print("Attempting to save expedition...")
            sys.stdout.flush()
            exp = serializer.save()
            print(f"Success! Created Expedition: {exp.code_expedition}")
            sys.stdout.flush()
        except Exception as e:
            print("ERROR_START")
            print(str(e))
            print("ERROR_END")
    else:
        print("Serializer errors:", serializer.errors)

if __name__ == '__main__':
    reproduce()
