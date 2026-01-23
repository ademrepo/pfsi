from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import models
from .models import (
    Utilisateur, Role, AuditLog,
    Client, Chauffeur, Vehicule, Destination, TypeService, Tarification,
    Expedition, TrackingExpedition, Tournee,
    Facture, FactureExpedition, Paiement
)
from .serializers import (
    LoginSerializer, UtilisateurSerializer, UtilisateurCreateSerializer,
    UtilisateurUpdateSerializer, PasswordResetSerializer, AuditLogSerializer,
    RoleSerializer, ClientSerializer, ChauffeurSerializer, VehiculeSerializer,
    DestinationSerializer, TypeServiceSerializer, TarificationSerializer,
    ExpeditionSerializer, TrackingExpeditionSerializer, TourneeSerializer,
    FactureSerializer, FactureExpeditionSerializer, PaiementSerializer
)
from .permissions import IsAuthenticated, IsAdminSysteme, IsAgentAdministratif
from .utils import create_audit_log


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint de connexion.
    Authentifie l'utilisateur et crée une session.
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Créer la session
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        request.session['role_code'] = user.role.code
        
        # Log de connexion réussie
        create_audit_log(
            user=user,
            action_type='LOGIN_SUCCESS',
            request=request
        )
        
        user_data = UtilisateurSerializer(user).data
        return Response({
            'message': 'Connexion réussie',
            'user': user_data
        }, status=status.HTTP_200_OK)
    else:
        # Log de connexion échouée
        username = request.data.get('username', 'unknown')
        create_audit_log(
            username=username,
            action_type='LOGIN_FAILED',
            request=request,
            details={'errors': serializer.errors}
        )
        
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint de déconnexion.
    Détruit la session utilisateur.
    """
    # Log de déconnexion
    if hasattr(request, 'user_obj') and request.user_obj:
        create_audit_log(
            user=request.user_obj,
            action_type='LOGOUT',
            request=request
        )
    
    # Détruire la session
    request.session.flush()
    
    return Response({
        'message': 'Déconnexion réussie'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Retourne les informations de l'utilisateur connecté.
    """
    if hasattr(request, 'user_obj') and request.user_obj:
        serializer = UtilisateurSerializer(request.user_obj)
        return Response(serializer.data)
    return Response(
        {'detail': 'Non authentifié'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
@ensure_csrf_cookie
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    Endpoint pour obtenir le token CSRF.
    """
    return Response({'detail': 'CSRF cookie set'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_roles(request):
    """
    Retourne la liste des rôles disponibles.
    """
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)


class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs.
    Accessible uniquement par l'Administrateur Système.
    """
    queryset = Utilisateur.objects.select_related('role').all()
    permission_classes = [IsAuthenticated, IsAdminSysteme]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UtilisateurCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UtilisateurUpdateSerializer
        return UtilisateurSerializer
    
    def create(self, request, *args, **kwargs):
        """Créer un nouvel utilisateur"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log de création
        create_audit_log(
            user=request.user_obj,
            action_type='USER_CREATED',
            request=request,
            details={
                'created_user_id': user.id,
                'created_username': user.username,
                'role_id': user.role_id
            }
        )
        
        return Response(
            UtilisateurSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Modifier un utilisateur"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_role_id = instance.role_id
        old_is_active = instance.is_active
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log de modification
        details = {
            'modified_user_id': user.id,
            'modified_username': user.username
        }
        
        if old_role_id != user.role_id:
            details['old_role_id'] = old_role_id
            details['new_role_id'] = user.role_id
        
        if old_is_active != user.is_active:
            action_type = (
                'USER_ACTIVATED'
                if user.is_active
                else 'USER_DEACTIVATED'
            )
        else:
            action_type = 'USER_UPDATED'
        
        create_audit_log(
            user=request.user_obj,
            action_type=action_type,
            request=request,
            details=details
        )
        
        return Response(UtilisateurSerializer(user).data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Désactiver un utilisateur au lieu de le supprimer.
        La suppression complète n'est pas autorisée pour la traçabilité.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        
        # Log de désactivation
        create_audit_log(
            user=request.user_obj,
            action_type='USER_DEACTIVATED',
            request=request,
            details={
                'deactivated_user_id': instance.id,
                'deactivated_username': instance.username
            }
        )
        
        return Response(
            {'message': 'Utilisateur désactivé avec succès'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Réinitialiser le mot de passe d'un utilisateur"""
        user = self.get_object()
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.password = make_password(new_password)
            user.save()
            
            # Log de réinitialisation
            create_audit_log(
                user=request.user_obj,
                action_type='PASSWORD_RESET',
                request=request,
                details={
                    'target_user_id': user.id,
                    'target_username': user.username
                }
            )
            
            return Response({
                'message': 'Mot de passe réinitialisé avec succès'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activer un utilisateur"""
        user = self.get_object()
        user.is_active = True
        user.save()
        
        # Log d'activation
        create_audit_log(
            user=request.user_obj,
            action_type='USER_ACTIVATED',
            request=request,
            details={
                'activated_user_id': user.id,
                'activated_username': user.username
            }
        )
        
        return Response({
            'message': 'Utilisateur activé avec succès'
        })
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Désactiver un utilisateur"""
        user = self.get_object()
        user.is_active = False
        user.save()
        
        # Log de désactivation
        create_audit_log(
            user=request.user_obj,
            action_type='USER_DEACTIVATED',
            request=request,
            details={
                'deactivated_user_id': user.id,
                'deactivated_username': user.username
            }
        )
        
        return Response({
            'message': 'Utilisateur désactivé avec succès'
        })


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour consulter les logs d'audit.
    Accessible uniquement par l'Administrateur Système.
    Lecture seule.
    """
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminSysteme]
    
    def get_queryset(self):
        """Filtrer les logs par utilisateur ou type d'action si spécifié"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        action_type = self.request.query_params.get('action_type', None)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        return queryset


class BaseAgentViewSet(viewsets.ModelViewSet):
    """Classe de base pour les vues accessibles aux agents"""
    permission_classes = [IsAuthenticated, IsAgentAdministratif | IsAdminSysteme]


class ClientViewSet(BaseAgentViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(nom__icontains=search) | 
                models.Q(prenom__icontains=search) | 
                models.Q(code_client__icontains=search)
            )
        return queryset


class ChauffeurViewSet(BaseAgentViewSet):
    queryset = Chauffeur.objects.all()
    serializer_class = ChauffeurSerializer


class VehiculeViewSet(BaseAgentViewSet):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer


class DestinationViewSet(BaseAgentViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class TypeServiceViewSet(BaseAgentViewSet):
    queryset = TypeService.objects.all()
    serializer_class = TypeServiceSerializer


class TarificationViewSet(BaseAgentViewSet):
    queryset = Tarification.objects.all()
    serializer_class = TarificationSerializer


class ExpeditionViewSet(BaseAgentViewSet):
    queryset = Expedition.objects.all().order_by('-date_creation')
    serializer_class = ExpeditionSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        client = self.request.query_params.get('client_id', None)
        
        if status:
            queryset = queryset.filter(statut=status)
        if client:
            queryset = queryset.filter(client_id=client)
            
        return queryset
        
    def perform_destroy(self, instance):
        # Vérifier si l'expédition est liée à une tournée
        if instance.tournee:
             from rest_framework.exceptions import ValidationError
             raise ValidationError("Impossible de supprimer une expédition liée à une tournée.")
             
        instance.delete()


class TourneeViewSet(BaseAgentViewSet):
    queryset = Tournee.objects.all().order_by('-date_tournee')
    serializer_class = TourneeSerializer


class TrackingExpeditionViewSet(BaseAgentViewSet):
    queryset = TrackingExpedition.objects.all().order_by('-date_statut')
    serializer_class = TrackingExpeditionSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        exp_id = self.request.query_params.get('expedition_id', None)
        if exp_id:
            queryset = queryset.filter(expedition_id=exp_id)
        return queryset


class FactureViewSet(BaseAgentViewSet):
    queryset = Facture.objects.all().order_by('-date_facture', '-id')
    serializer_class = FactureSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client_id')
        statut = self.request.query_params.get('statut')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if statut:
            queryset = queryset.filter(statut=statut)
        return queryset

    def perform_destroy(self, instance):
        from django.db import transaction
        with transaction.atomic():
            # 1. Libérer les expéditions
            links = FactureExpedition.objects.filter(facture=instance)
            for link in links:
                exp = link.expedition
                exp.est_facturee = False
                exp.save()
            
            # 2. Annuler les paiements et restaurer solde client
            paiements = Paiement.objects.filter(facture=instance)
            for p in paiements:
                if instance.client:
                    instance.client.solde += p.montant
                p.delete()
            
            if instance.client:
                # 3. Restaurer le solde (retirer le montant de la facture)
                instance.client.solde -= instance.total_ttc
                instance.client.save()

            instance.delete()


class PaiementViewSet(BaseAgentViewSet):
    queryset = Paiement.objects.all().order_by('-date_paiement', '-id')
    serializer_class = PaiementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client_id')
        facture_id = self.request.query_params.get('facture_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if facture_id:
            queryset = queryset.filter(facture_id=facture_id)
        return queryset

    def perform_destroy(self, instance):
        from django.db import transaction
        with transaction.atomic():
            # Restaurer le solde client
            if instance.client:
                instance.client.solde += instance.montant
                instance.client.save()
            
            # Maj statut facture si liée
            facture = instance.facture
            instance.delete()
            
            if facture:
                deja_paye = Paiement.objects.filter(facture=facture).aggregate(models.Sum('montant'))['montant__sum'] or 0
                if deja_paye >= facture.total_ttc:
                    facture.statut = 'Payée'
                elif deja_paye > 0:
                    facture.statut = 'Partiellement Payée'
                else:
                    facture.statut = 'Émise'
                facture.save()
