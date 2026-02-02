import json 
from .models import AuditLog 


def get_client_ip (request ):
    """Récupère l'adresse IP du client"""
    x_forwarded_for =request .META .get ('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for :
        ip =x_forwarded_for .split (',')[0 ]
    else :
        ip =request .META .get ('REMOTE_ADDR')
    return ip 


def get_user_agent (request ):
    """Récupère le User Agent du client"""
    return request .META .get ('HTTP_USER_AGENT','')


def create_audit_log (user =None ,username =None ,action_type =None ,request =None ,details =None ):
    """
    Crée une entrée dans le journal d'audit.
    
    Args:
        user: Instance de Utilisateur (optionnel si username fourni)
        username: Nom d'utilisateur (utilisé si user non fourni)
        action_type: Type d'action (voir AuditLog.ACTION_CHOICES)
        request: Objet request Django
        details: Dictionnaire de détails supplémentaires
    """
    if user :
        username =user .username 

    if not username :
        username ='anonymous'

    audit_data ={
    'user':user ,
    'username':username ,
    'action_type':action_type ,
    'details':json .dumps (details )if details else None 
    }

    if request :
        audit_data ['ip_address']=get_client_ip (request )
        audit_data ['user_agent']=get_user_agent (request )

    return AuditLog .objects .create (**audit_data )
