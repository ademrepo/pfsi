from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Incident

@receiver(post_save, sender=Incident)
def send_incident_alert_email(sender, instance, created, **kwargs):
    """
    Envoie un email d'alerte lors de la création d'un incident.
    """
    if created and instance.notify_direction:
        try:
            subject = f"[ALERTE INCIDENT] {instance.type_incident} - {instance.code_incident}"
            
            exp_code = instance.expedition.code_expedition if instance.expedition else "N/A"
            trn_code = instance.tournee.code_tournee if instance.tournee else "N/A"
            
            message = (
                f"Nouvel incident déclaré :\n\n"
                f"Code : {instance.code_incident}\n"
                f"Type : {instance.type_incident}\n"
                f"Expédition concernée : {exp_code}\n"
                f"Tournée concernée : {trn_code}\n\n"
                f"Commentaire :\n{instance.commentaire}\n\n"
                f"Action appliquée : {instance.get_action_appliquee_display()}\n\n"
                f"Veuillez vérifier le tableau de bord pour plus de détails."
            )
            
            # Use specific email requested by user or fallback to defaults
            recipient_list = ['ademglps@gmail.com'] 
            
            # Add Admin emails if configured
            if hasattr(settings, 'ADMINS') and settings.ADMINS:
                recipient_list.extend([mail for name, mail in settings.ADMINS])
                
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

            if not from_email:
                print("WARNING: DEFAULT_FROM_EMAIL not set in settings. Email might fail.")

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False  # We want to see errors in logs
            )
            print(f"  -> Email sent successfully to {recipient_list}")
            
        except Exception as e:
            print(f"ERROR: Failed to send incident email: {str(e)}")
            # Do not re-raise to avoid breaking the transaction/script
