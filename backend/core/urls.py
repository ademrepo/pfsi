from django .urls import path ,include 
from rest_framework .routers import DefaultRouter 
from .views import (
login_view ,logout_view ,current_user_view ,get_csrf_token ,get_roles ,
password_reset_request_view ,password_reset_confirm_view ,
analytics_summary_view ,analytics_advanced_view ,
UtilisateurViewSet ,AuditLogViewSet ,
ClientViewSet ,ChauffeurViewSet ,VehiculeViewSet ,DestinationViewSet ,
TypeServiceViewSet ,TarificationViewSet ,ExpeditionViewSet ,TourneeViewSet ,
TrackingExpeditionViewSet ,IncidentViewSet ,AlerteViewSet ,
ReclamationViewSet ,
FactureViewSet ,PaiementViewSet 
)

router =DefaultRouter ()
router .register (r'utilisateurs',UtilisateurViewSet ,basename ='utilisateur')
router .register (r'audit-logs',AuditLogViewSet ,basename ='auditlog')
router .register (r'clients',ClientViewSet ,basename ='client')
router .register (r'chauffeurs',ChauffeurViewSet ,basename ='chauffeur')
router .register (r'vehicules',VehiculeViewSet ,basename ='vehicule')
router .register (r'destinations',DestinationViewSet ,basename ='destination')
router .register (r'types-service',TypeServiceViewSet ,basename ='typeservice')
router .register (r'tarifications',TarificationViewSet ,basename ='tarification')
router .register (r'expeditions',ExpeditionViewSet ,basename ='expedition')
router .register (r'tournees',TourneeViewSet ,basename ='tournee')
router .register (r'tracking',TrackingExpeditionViewSet ,basename ='tracking')
router .register (r'incidents',IncidentViewSet ,basename ='incident')
router .register (r'alertes',AlerteViewSet ,basename ='alerte')
router .register (r'reclamations',ReclamationViewSet ,basename ='reclamation')
router .register (r'factures',FactureViewSet ,basename ='facture')
router .register (r'paiements',PaiementViewSet ,basename ='paiement')

urlpatterns =[

path ('auth/login/',login_view ,name ='login'),
path ('auth/logout/',logout_view ,name ='logout'),
path ('auth/me/',current_user_view ,name ='current-user'),
path ('auth/csrf/',get_csrf_token ,name ='csrf-token'),
path ('auth/roles/',get_roles ,name ='roles'),
path ('auth/password-reset/request/',password_reset_request_view ,name ='password-reset-request'),
path ('auth/password-reset/confirm/',password_reset_confirm_view ,name ='password-reset-confirm'),


path ('analytics/summary/',analytics_summary_view ,name ='analytics-summary'),
path ('analytics/advanced/',analytics_advanced_view ,name ='analytics-advanced'),


path ('',include (router .urls )),
]
