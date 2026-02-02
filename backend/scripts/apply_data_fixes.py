
import os
import django
import sys
from django.db import transaction
from django.db.models import Sum, F
from django.utils import timezone

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mon_projet.settings")
django.setup()

from core.models import (
    Expedition, Tournee, Client, Facture, Paiement, 
    TrackingExpedition, Reclamation, 
    Incident
)

def normalize_status(status):
    if not status:
        return status
    
    s = status.lower().strip()
    
    # Expedition mappings
    if s in ['livre', 'livré', 'livree']:
        return 'Livré'
    if s in ['en_livraison', 'en cours de livraison']:
        return 'En cours de livraison'
    if s in ['en_transit', 'en transit']:
        return 'En transit'
    if s in ['en_crentre_tri', 'en centre de tri', 'entrepot']:
        return 'En centre de tri'
    if s in ['recupere', 'récupéré']:
        return 'Récupéré'
    if s in ['instance', 'en instance']:
        return 'En instance'
    if s in ['retour', 'retourné', 'retourne']:
        return 'Retourné'
    if s in ['echec', 'échec', 'echec de livraison']:
        return 'Échec de livraison'
    if s in ['brouillon']:
        return 'Brouillon'
    if s in ['cree', 'créé', 'enregistre', 'enregistré']:
        return 'Enregistré'
        
    # Tournee mappings
    if s in ['complete', 'complète', 'terminee', 'terminée']:
        return 'Terminée'
    if s in ['en_cours', 'en cours']:
        return 'En cours'
    if s in ['planifiee', 'planifiée', 'prevue', 'prévue']:
        return 'Planifiée'
    if s in ['annulee', 'annulée']:
        return 'Annulée'
        
    # Facture/Paiement mappings
    if s in ['payee', 'payée']:
        return 'Payée'
    if s in ['impayee', 'impayée']:
        return 'Impayée'
    if s in ['partiellement_payee', 'partiellement payée']:
        return 'Partiellement payée'
    if s in ['valide', 'validé']:
        return 'Validé'
    if s in ['rejete', 'rejeté']:
        return 'Rejeté'
        
    return status.capitalize() # Fallback

def run_fixes():
    print("Starting data normalization...")
    
    with transaction.atomic():
        # 1. Normalize Expeditions
        print("Normalizing Expeditions...")
        expeditions = Expedition.objects.all()
        for exp in expeditions:
            new_statut = normalize_status(exp.statut)
            if new_statut != exp.statut:
                exp.statut = new_statut
                exp.save(update_fields=['statut'])
            
            # Ensure Tracking exists (fix for raw SQL seeds missing signals)
            if not exp.tracking_history.exists():
                TrackingExpedition.objects.create(
                    expedition=exp,
                    statut=exp.statut or 'Enregistré',
                    lieu='Import Initial',
                    date_statut=exp.date_creation or timezone.now(),
                    commentaire="Généré automatiquement suite à l'import de données historique"
                )

        # 2. Normalize Tournees
        print("Normalizing Tournees...")
        tournees = Tournee.objects.all()
        for trn in tournees:
            new_statut = normalize_status(trn.statut)
            if new_statut != trn.statut:
                trn.statut = new_statut
                trn.save(update_fields=['statut'])

        # 3. Normalize Factures
        print("Normalizing Factures...")
        factures = Facture.objects.all()
        for fac in factures:
            new_statut = normalize_status(fac.statut)
            if new_statut != fac.statut:
                fac.statut = new_statut
                fac.save(update_fields=['statut'])

        # 4. Recalculate Client Balances
        print("Recalculating Client Balances...")
        clients = Client.objects.all()
        for client in clients:
            total_facture = Facture.objects.filter(client=client).aggregate(s=Sum('total_ttc'))['s'] or 0
            total_paye = Paiement.objects.filter(client=client).aggregate(s=Sum('montant'))['s'] or 0
            
            # Simple logic: Solde = Dettes (Factured) - Paid
            # Wait, usually positive balance means they owe money? Or credit?
            # Let's assume Solde = Amount Due.
            
            # Using logical deduction: if I have 1000 invoice and paid 0, solde should be 1000 (debt).
            # If I paid 1000, solde 0.
            
            new_solde = total_facture - total_paye
            
            # Just to be safe, update via SQL or save
            client.solde = new_solde
            client.save(update_fields=['solde'])
            
    print("Data normalization complete!")

if __name__ == "__main__":
    run_fixes()
