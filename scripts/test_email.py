import os
import sys
import django
from django.core.mail import send_mail
from django.conf import settings

# Setup Django
# Robust path setup:
# Script is in /scripts/. Backend is in /backend/.
# We need to add /backend/ to sys.path.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
sys.path.append(BACKEND_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mon_projet.settings")
django.setup()

def test_email():
    print("\n" + "="*50)
    print("📧 DIAGNOSTIC EMAIL START")
    print("="*50)

    # Check settings
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"Host: {settings.EMAIL_HOST}")
    print(f"Port: {settings.EMAIL_PORT}")
    print(f"User: {settings.EMAIL_HOST_USER}")
    print(f"TLS: {settings.EMAIL_USE_TLS}")
    print(f"SSL: {settings.EMAIL_USE_SSL}")
    
    # Check for placeholder
    pwd = settings.EMAIL_HOST_PASSWORD
    if 'PUT_YOUR_APP_PASSWORD_HERE' in pwd:
        print("\n❌ ERREUR: Vous n'avez pas mis votre mot de passe dans .env!")
        return

    print(f"\n🔑 Vérification Mot de Passe:")
    print(f"   Longueur reçue: {len(pwd)} caractères")
    if len(pwd) > 0:
        masked = pwd[0] + "*"*(len(pwd)-2) + pwd[-1] if len(pwd) > 2 else "***"
        print(f"   Aperçu: {masked}")
    
    if len(pwd) != 16:
        print("   ⚠️  ATTENTION: Un mot de passe d'application Google fait normalement 16 caractères.")
        print(f"       Vous avez fourni {len(pwd)} caractères. Il en manque peut-être ?")


    print("\nTentative d'envoi à ademglps@gmail.com ...")
    
    try:
        sent = send_mail(
            subject='Test SMTP Configuration',
            message='Ceci est un email de test pour vérifier la configuration SMTP.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['ademglps@gmail.com'],
            fail_silently=False,
        )
        if sent:
            print("✅ SUCCÈS: Email envoyé avec succès !")
        else:
            print("⚠️ AVERTISSEMENT: send_mail a retourné 0 (non envoyé).")
            
    except Exception as e:
        print(f"\n❌ ÉCHEC: L'envoi a échoué.")
        print(f"Erreur détaillée : {e}")
        
    print("="*50 + "\n")

if __name__ == "__main__":
    test_email()
