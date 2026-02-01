import os
import django
import sys

# Add the current directory to sys.path to ensure modules can be imported
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

from core.models import Utilisateur, Role

try:
    # Search for Ahmed Benali
    user = Utilisateur.objects.filter(nom__icontains='benali', prenom__icontains='ahmed').first()
    if not user:
        user = Utilisateur.objects.filter(nom__icontains='ahmed', prenom__icontains='benali').first()
    
    if user:
        # Search for Admin role
        admin_role = Role.objects.filter(code='ADMIN').first()
        if not admin_role:
             admin_role = Role.objects.filter(libelle__icontains='admin').first()
             
        if admin_role:
            user.role = admin_role
            user.save()
            print(f"Successfully updated user {user.username} ({user.prenom} {user.nom}) to {admin_role.libelle}.")
        else:
            print("Role ADMIN not found in database.")
    else:
        # List all users to see what's available
        print("User Ahmed Benali not found. Available users:")
        for u in Utilisateur.objects.all():
            print(f"- {u.prenom} {u.nom} ({u.username})")
except Exception as e:
    print(f"Error: {e}")
