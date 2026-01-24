from django.contrib import admin
from .models import Incident, IncidentAttachment, Alerte, Reclamation, ReclamationExpedition

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('code_incident', 'type_incident', 'expedition', 'tournee', 'action_appliquee', 'created_at')
    list_filter = ('type_incident', 'action_appliquee', 'notify_direction', 'notify_client', 'created_at')
    search_fields = ('code_incident', 'commentaire', 'expedition__code_expedition', 'tournee__code_tournee')


@admin.register(IncidentAttachment)
class IncidentAttachmentAdmin(admin.ModelAdmin):
    list_display = ('incident', 'original_name', 'uploaded_at', 'uploaded_by')
    search_fields = ('original_name', 'file')


@admin.register(Alerte)
class AlerteAdmin(admin.ModelAdmin):
    list_display = ('destination', 'titre', 'is_read', 'created_at')
    list_filter = ('destination', 'is_read', 'created_at')
    search_fields = ('titre', 'message')


@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'statut', 'date_reclamation', 'facture', 'type_service', 'traite_par')
    list_filter = ('statut', 'date_reclamation')
    search_fields = ('objet', 'description', 'client__nom', 'client__prenom')


@admin.register(ReclamationExpedition)
class ReclamationExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reclamation', 'expedition')
