from rest_framework import permissions
from .models import UserRole


class IsAdminSysteme(permissions.BasePermission):
    """
    Permission pour l'Administrateur Système.
    Accès total à toutes les fonctionnalités.
    """
    message = "Seul l'Administrateur Système peut effectuer cette action."
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == UserRole.ADMIN_SYSTEME
        )


class IsAgentAdministratif(permissions.BasePermission):
    """
    Permission pour l'Agent Administratif.
    Accès aux fonctionnalités opérationnelles (hors finance).
    """
    message = "Accès réservé aux Agents Administratifs."
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [
                UserRole.ADMIN_SYSTEME,
                UserRole.AGENT_ADMINISTRATIF
            ]
        )


class IsResponsableLogistique(permissions.BasePermission):
    """
    Permission pour le Responsable Logistique.
    Accès aux tournées, affectations, incidents.
    """
    message = "Accès réservé aux Responsables Logistique."
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [
                UserRole.ADMIN_SYSTEME,
                UserRole.RESPONSABLE_LOGISTIQUE
            ]
        )


class IsComptable(permissions.BasePermission):
    """
    Permission pour le Comptable.
    Accès aux factures et paiements.
    """
    message = "Accès réservé aux Comptables."
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [
                UserRole.ADMIN_SYSTEME,
                UserRole.COMPTABLE
            ]
        )


class IsDirection(permissions.BasePermission):
    """
    Permission pour la Direction.
    Accès en lecture seule aux tableaux de bord et statistiques.
    """
    message = "Accès réservé à la Direction."
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [
                UserRole.ADMIN_SYSTEME,
                UserRole.DIRECTION
            ]
        )


class IsChauffeur(permissions.BasePermission):
    """
    Permission pour le Chauffeur.
    Accès limité à ses tournées et expéditions.
    """
    message = "Accès réservé aux Chauffeurs."
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [
                UserRole.ADMIN_SYSTEME,
                UserRole.CHAUFFEUR
            ]
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
            request.user and
            request.user.is_authenticated and
            request.user.role == UserRole.DIRECTION
        )
