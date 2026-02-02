
import os
import django
import sys
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

# Setup Django environment
# Assuming script is run from project root (where manage.py is)
# or from scripts/ directory.
# We need to make sure project root is in sys.path
# If running as `python scripts/apply_data_fixes.py`, CWD is root.
# Appending CWD to sys.path is safe.
sys.path.append(os.getcwd())
# Also append backend/ to be sure
sys.path.append(os.path.join(os.getcwd(), 'backend'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mon_projet.settings")
try:
    django.setup()
except Exception as e:
    # Try adjusting path if 'mon_projet' not found
    print(f"Initial setup failed: {e}")
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    django.setup()

from core.models import (
    Expedition, Tournee, Client, Facture, Paiement, 
    TrackingExpedition, FactureExpedition, Incident, Alerte
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
    if s in ['en_attente', 'en attente']:
        return 'En attente'
        
    # Tournee mappings
    if s in ['complete', 'complète', 'terminee', 'terminée']:
        return 'Terminée'
    if s in ['en_cours', 'en cours']:
        return 'En cours'
    if s in ['planifiee', 'planifiée', 'prevue', 'prévue', 'preparée', 'prÃ©parÃ©e']:
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

def normalize_text(text):
    if not text:
        return text
    
    replacements = {
        'Ã©': 'é',
        'Ã¨': 'è',
        'Ã ': 'à',
        'Ã¢': 'â',
        'Ãª': 'ê',
        'Ã»': 'û',
        'Ã®': 'î',
        'Ã¯': 'ï',
        'Ã´': 'ô',
        'Ã§': 'ç',
        'AlgÃ©rie': 'Algérie',
        'BÃ©jaÃ¯a': 'Béjaïa',
        'SÃ©tif': 'Sétif',
        'GhardaÃ¯a': 'Ghardaïa',
        'MÃ©dÃ©a': 'Médéa'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def run_fixes():
    print("Starting data normalization and integrity enforcement...")
    
    try:
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
                
                # Round & Scale amounts (keep it pretty and realistic)
                # User requested scaling down because amounts are "too big"
                if exp.montant_total:
                    # Scale down by 10 if it looks like a raw generated value (> 500)
                    if exp.montant_total > 500: 
                        exp.montant_total = exp.montant_total / 10.0
                    
                    exp.montant_total = round(exp.montant_total)
                    exp.save(update_fields=['montant_total'])

            # 2. Normalize Tournees
            print("Normalizing Tournees...")
            tournees = Tournee.objects.all()
            for trn in tournees:
                new_statut = normalize_status(trn.statut)
                if new_statut != trn.statut:
                    trn.statut = new_statut
                    trn.save(update_fields=['statut'])

            # 3. Normalize Factures
            print("Normalizing Factures and Recalculating Status & Amounts...")
            factures = Facture.objects.all()
            for fac in factures:
                # Normalization
                fac.statut = normalize_status(fac.statut)
                
                # Strict Consistency: Recalculate amounts from Linked Expeditions
                # This ensures "Chiffre d'Affaire" matches perfectly
                linked_exps = FactureExpedition.objects.filter(facture=fac).values_list('expedition', flat=True)
                sum_ttc = Expedition.objects.filter(id__in=linked_exps).aggregate(total=Sum('montant_total'))['total'] or 0
                
                if sum_ttc > 0:
                    fac.total_ttc = sum_ttc
                    fac.total_ht = round(fac.total_ttc / 1.19) # Assuming 19% TVA
                    fac.montant_tva = fac.total_ttc - fac.total_ht
                else:
                    # Fallback if no linked expeditions (orphaned facture? shouldn't happen after thinning)
                    if fac.total_ttc and fac.total_ttc > 500: # Legacy scaling just in case
                         fac.total_ttc = round(fac.total_ttc / 10.0)
                         fac.total_ht = round(fac.total_ttc / 1.19)
                         fac.montant_tva = fac.total_ttc - fac.total_ht

                # Recalculate status based on payments vs NEW total_ttc
                total_paid = fac.paiement_set.aggregate(total=Sum('montant'))['total'] or 0
                total_due = fac.total_ttc or 0
                
                if total_paid >= total_due and total_due > 0:
                    fac.statut = 'Payée'
                elif total_paid > 0:
                    fac.statut = 'Partiellement payée'
                else:
                    fac.statut = 'Impayée'
                
                fac.save(update_fields=['statut', 'total_ht', 'total_ttc', 'montant_tva'])

            # 5. Scale Payments (Fix for Negative Balances)
            print("Scaling Payments...")
            paginator = Paiement.objects.all()
            for p in paginator:
                if p.montant and p.montant > 500:
                    p.montant = round(p.montant / 10.0)
                    p.save(update_fields=['montant'])

            # 6. Integrity Check: Expedition 'est_facturee' flag
            print("Enforcing Expedition 'est_facturee' consistency...")
            # Reset all
            # Expedition.objects.update(est_facturee=False) # Too heavy? No, bulk update is fine.
            # actually let's update based on existence
            linked_exp_ids = FactureExpedition.objects.values_list('expedition_id', flat=True)
            Expedition.objects.filter(id__in=linked_exp_ids).update(est_facturee=True)
            Expedition.objects.exclude(id__in=linked_exp_ids).update(est_facturee=False)

            # 7. Recalculate Client Balances
            print("Recalculating Client Balances...")
            clients = Client.objects.all()
            for client in clients:
                # Solde = Total Factured (Assets/Receivables) - Total Paid
                total_facture = Facture.objects.filter(client=client).aggregate(s=Sum('total_ttc'))['s'] or 0
                total_paye = Paiement.objects.filter(client=client).aggregate(s=Sum('montant'))['s'] or 0
                
                # Solde is amount DUE by client
                new_solde = total_facture - total_paye
                
                if client.solde != new_solde:
                    client.solde = new_solde
                    client.save(update_fields=['solde'])
                    
                    
            # 8. Normalize Text Fields (Fix Encoding)
            print("Fixing character encoding...")
            from core.models import Destination
            
            for client in Client.objects.all():
                client.nom = normalize_text(client.nom)
                client.prenom = normalize_text(client.prenom)
                client.adresse = normalize_text(client.adresse)
                client.ville = normalize_text(client.ville)
                client.pays = normalize_text(client.pays)
                client.save()
                
            for dest in Destination.objects.all():
                dest.ville = normalize_text(dest.ville)
                dest.pays = normalize_text(dest.pays)
                dest.save()

            # 9. Ensure Demo Incident (Restoring Functionality)
            print("Ensuring Demo Incident exists...")
            if not Incident.objects.exists():
                exp = Expedition.objects.first()
                if exp:
                    inc = Incident.objects.create(
                        code_incident='INC-DEMO-001',
                        expedition=exp,
                        type_incident='Retard',
                        commentaire="Incident de test généré automatiquement (Demo)",
                        notify_direction=True,
                        action_appliquee='En cours d\'analyse'
                    )
                    # Create Alerte explicitly
                    Alerte.objects.create(
                        incident=inc,
                        expedition=exp,
                        type_alerte='Retard',
                        titre="Nouvel Incident Détecté",
                        message=f"Incident déclaré pour l'expédition {exp.code_expedition}",
                        destination='dashboard'
                    )
                    print("  - Created Demo Incident & Alerte.")

            print("Data normalization and integrity checks complete!")
        
    except Exception as e:
        print(f"Error during data fixes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_fixes()
