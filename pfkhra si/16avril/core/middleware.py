from .models import Utilisateur
from .utils import create_audit_log, AuditLog


class AuthenticationMiddleware:
    """
    Middleware personnalisé pour l'authentification basée sur les sessions.
    Vérifie la session et attache l'utilisateur à la requête.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Récupérer l'ID utilisateur de la session
        user_id = request.session.get('user_id')
        
        if user_id:
            try:
                user = Utilisateur.objects.select_related('role').get(id=user_id, is_active=True)
                request.user_obj = user
                request.is_authenticated = True
            except Utilisateur.DoesNotExist:
                request.user_obj = None
                request.is_authenticated = False
                # Nettoyer la session
                request.session.flush()
        else:
            request.user_obj = None
            request.is_authenticated = False
        
        response = self.get_response(request)
        return response


class AuditLoggingMiddleware:
    """
    Middleware pour logger automatiquement certaines actions.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Log des accès refusés (403, 401)
        if response.status_code in [401, 403]:
            if hasattr(request, 'user_obj') and request.user_obj:
                create_audit_log(
                    user=request.user_obj,
                    action_type='ACCESS_DENIED',
                    request=request,
                    details={
                        'path': request.path,
                        'method': request.method,
                        'status_code': response.status_code
                    }
                )
        
        return response
