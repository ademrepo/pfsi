from rest_framework import permissions
from .models import Utilisateur


class IsAuthenticated(permissions.BasePermission):
    """
    Permission de base: utilisateur authentifié
    """
    message = "Vous devez être connecté pour accéder à cette ressource."
    
    def has_permission(self, request, view):
        return (
            hasattr(request, 'user_obj') and
            request.user_obj is not None and
            request.user_obj.is_active
        )


class IsAdminSysteme(permissions.BasePermission):
    """
    Permission pour l'Administrateur Système.
    Accès total à toutes les fonctionnalités.
    """
    message = "Seul l'Administrateur Système peut effectuer cette action."
    
    def has_permission(self, request, view):
        return (
            hasattr(request, 'user_obj') and
            request.user_obj is not None and
            request.user_obj.is_active and
            request.user_obj.role.code == 'ADMIN'
        )


class IsAgentAdministratif(permissions.BasePermission):
    """
    Permission pour l'Agent Administratif.
    Accès aux fonctionnalités opérationnelles (hors finance).
    """
    message = "Accès réservé aux Agents Administratifs."
    
    def has_permission(self, request, view):
        return (
            hasattr(request, 'user_obj') and
            request.user_obj is not None and
            request.user_obj.is_active and
            request.user_obj.role.code in ['ADMIN', 'AGENT']
        )


class IsResponsableLogistique(permissions.BasePermission):
    """
    Permission pour le Responsable Logistique.
    Accès aux tournées, affectations, incidents.
    """
    message = "Accès réservé aux Responsables Logistique."
    
    def has_permission(self, request, view):
        return (
            hasattr(request, 'user_obj') and
            request.user_obj is not None and
            request.user_obj.is_active and
            request.user_obj.role.code in ['ADMIN', 'LOGISTIQUE']
        )


class IsComptable(permissions.BasePermission):
    """
    Permission pour le Comptable.
    Accès aux factures et paiements.
    """
    message = "Accès réservé aux Comptables."
    
    def has_permission(self, request, view):
        return (
            hasattr(request, 'user_obj') and
            request.user_obj is not None and
            request.user_obj.is_active and
            request.user_obj.role.code in ['ADMIN', 'COMPTABLE']
        )


class IsDirection(permissions.BasePermission):
    """
    Permission pour la Direction.
    Accès en lecture seule aux tableaux de bord et statistiques.
    """
    message = "Accès réservé à la Direction."
    
    def has_permission(self, request, view):
        return (
            hasattr(request, 'user_obj') and
            request.user_obj is not None and
            request.user_obj.is_active and
            request.user_obj.role.code in ['ADMIN', 'DIRECTION']
        )


class IsChauffeur(permissions.BasePermission):
    """
    Permission pour le Chauffeur.
    Accès limité à ses tournées et expéditions.
    """
    message = "Accès réservé aux Chauffeurs."
    
    def has_permission(self, request, view):
        return (
            hasattr(request, 'user_obj') and
            request.user_obj is not None and
            request.user_obj.is_active and
            request.user_obj.role.code in ['ADMIN', 'CHAUFFEUR']
        )


class IsDirectionReadOnly(permissions.BasePermission):
    """
    Permission pour la Direction avec lecture seule.
    Autorise uniquement les méthodes GET, HEAD, OPTIONS.
    """
    message = "La Direction a un accès en lecture seule."
    
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return False
        
        return (
            hasattr(request, 'user_obj') and
            request.user_obj is not None and
            request.user_obj.is_active and
            request.user_obj.role.code == 'DIRECTION'
        )
