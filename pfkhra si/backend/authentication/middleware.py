from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog
from .utils import create_audit_log


class AuditLoggingMiddleware(MiddlewareMixin):
    """
    Middleware pour logger automatiquement certaines actions.
    Vérifie également que l'utilisateur est actif.
    """
    
    def process_request(self, request):
        """
        Vérifie que l'utilisateur authentifié est actif.
        Si l'utilisateur est désactivé, on le déconnecte.
        """
        if request.user.is_authenticated:
            if not request.user.is_active:
                from django.contrib.auth import logout
                logout(request)
                
                # Log de tentative d'accès avec compte désactivé
                create_audit_log(
                    username=request.user.username,
                    action_type=AuditLog.ActionType.ACCESS_DENIED,
                    request=request,
                    details={'reason': 'Compte désactivé'}
                )
        
        return None
    
    def process_response(self, request, response):
        """
        Log des accès refusés (403, 401).
        """
        if response.status_code in [401, 403]:
            if request.user.is_authenticated:
                create_audit_log(
                    user=request.user,
                    action_type=AuditLog.ActionType.ACCESS_DENIED,
                    request=request,
                    details={
                        'path': request.path,
                        'method': request.method,
                        'status_code': response.status_code
                    }
                )
        
        return response
