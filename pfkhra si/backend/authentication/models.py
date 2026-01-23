from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class UserRole(models.TextChoices):
    """Rôles utilisateurs définis selon le cahier des charges"""
    ADMIN_SYSTEME = 'ADMIN_SYSTEME', 'Administrateur Système'
    AGENT_ADMINISTRATIF = 'AGENT_ADMINISTRATIF', 'Agent Administratif'
    RESPONSABLE_LOGISTIQUE = 'RESPONSABLE_LOGISTIQUE', 'Responsable Logistique'
    COMPTABLE = 'COMPTABLE', 'Comptable / Facturation'
    DIRECTION = 'DIRECTION', 'Direction'
    CHAUFFEUR = 'CHAUFFEUR', 'Chauffeur'


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec gestion des rôles.
    Étend AbstractUser de Django pour ajouter le champ role.
    """
    role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.AGENT_ADMINISTRATIF,
        verbose_name="Rôle"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Désactiver au lieu de supprimer l'utilisateur"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def has_role(self, role):
        """Vérifie si l'utilisateur a un rôle spécifique"""
        return self.role == role
    
    def can_manage_users(self):
        """Seul l'admin système peut gérer les utilisateurs"""
        return self.role == UserRole.ADMIN_SYSTEME


class AuditLog(models.Model):
    """
    Journal d'audit pour la traçabilité des actions.
    Enregistre toutes les actions sensibles selon le cahier des charges.
    """
    
    class ActionType(models.TextChoices):
        LOGIN_SUCCESS = 'LOGIN_SUCCESS', 'Connexion réussie'
        LOGIN_FAILED = 'LOGIN_FAILED', 'Connexion échouée'
        LOGOUT = 'LOGOUT', 'Déconnexion'
        USER_CREATED = 'USER_CREATED', 'Utilisateur créé'
        USER_UPDATED = 'USER_UPDATED', 'Utilisateur modifié'
        USER_ACTIVATED = 'USER_ACTIVATED', 'Utilisateur activé'
        USER_DEACTIVATED = 'USER_DEACTIVATED', 'Utilisateur désactivé'
        PASSWORD_RESET = 'PASSWORD_RESET', 'Mot de passe réinitialisé'
        ACCESS_DENIED = 'ACCESS_DENIED', 'Accès refusé'
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name="Utilisateur"
    )
    
    username = models.CharField(
        max_length=150,
        verbose_name="Nom d'utilisateur",
        help_text="Stocké même si l'utilisateur est supprimé"
    )
    
    action_type = models.CharField(
        max_length=50,
        choices=ActionType.choices,
        verbose_name="Type d'action"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresse IP"
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name="User Agent"
    )
    
    details = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Détails",
        help_text="Informations supplémentaires en JSON"
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date et heure"
    )
    
    class Meta:
        verbose_name = "Journal d'audit"
        verbose_name_plural = "Journaux d'audit"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action_type', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.username} - {self.get_action_type_display()} - {self.timestamp}"
