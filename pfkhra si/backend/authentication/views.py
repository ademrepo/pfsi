from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import CustomUser, AuditLog
from .serializers import (
    LoginSerializer, UserSerializer, UserCreateSerializer,
    UserUpdateSerializer, PasswordResetSerializer, AuditLogSerializer
)
from .permissions import IsAdminSysteme
from .utils import get_client_ip, create_audit_log


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
        login(request, user)
        
        # Log de connexion réussie
        create_audit_log(
            user=user,
            action_type=AuditLog.ActionType.LOGIN_SUCCESS,
            request=request
        )
        
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Connexion réussie',
            'user': user_data
        }, status=status.HTTP_200_OK)
    else:
        # Log de connexion échouée
        username = request.data.get('username', 'unknown')
        create_audit_log(
            username=username,
            action_type=AuditLog.ActionType.LOGIN_FAILED,
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
    create_audit_log(
        user=request.user,
        action_type=AuditLog.ActionType.LOGOUT,
        request=request
    )
    
    logout(request)
    
    return Response({
        'message': 'Déconnexion réussie'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Retourne les informations de l'utilisateur connecté.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@ensure_csrf_cookie
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    Endpoint pour obtenir le token CSRF.
    """
    return Response({'detail': 'CSRF cookie set'})


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs.
    Accessible uniquement par l'Administrateur Système.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminSysteme]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        """Créer un nouvel utilisateur"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log de création
        create_audit_log(
            user=request.user,
            action_type=AuditLog.ActionType.USER_CREATED,
            request=request,
            details={
                'created_user_id': user.id,
                'created_username': user.username,
                'role': user.role
            }
        )
        
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Modifier un utilisateur"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_role = instance.role
        old_is_active = instance.is_active
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log de modification
        details = {
            'modified_user_id': user.id,
            'modified_username': user.username
        }
        
        if old_role != user.role:
            details['old_role'] = old_role
            details['new_role'] = user.role
        
        if old_is_active != user.is_active:
            action_type = (
                AuditLog.ActionType.USER_ACTIVATED
                if user.is_active
                else AuditLog.ActionType.USER_DEACTIVATED
            )
        else:
            action_type = AuditLog.ActionType.USER_UPDATED
        
        create_audit_log(
            user=request.user,
            action_type=action_type,
            request=request,
            details=details
        )
        
        return Response(UserSerializer(user).data)
    
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
            user=request.user,
            action_type=AuditLog.ActionType.USER_DEACTIVATED,
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
            user.set_password(new_password)
            user.save()
            
            # Log de réinitialisation
            create_audit_log(
                user=request.user,
                action_type=AuditLog.ActionType.PASSWORD_RESET,
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
            user=request.user,
            action_type=AuditLog.ActionType.USER_ACTIVATED,
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
            user=request.user,
            action_type=AuditLog.ActionType.USER_DEACTIVATED,
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
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminSysteme]
    
    def get_queryset(self):
        """Filtrer les logs par utilisateur si spécifié"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        action_type = self.request.query_params.get('action_type', None)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        return queryset
