from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, AuditLog, UserRole


class LoginSerializer(serializers.Serializer):
    """Serializer pour la connexion utilisateur"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError(
                    "Nom d'utilisateur ou mot de passe incorrect."
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    "Ce compte a été désactivé."
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                "Le nom d'utilisateur et le mot de passe sont requis."
            )


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour les informations utilisateur"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'utilisateur (admin uniquement)"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'role', 'password', 'password_confirm', 'is_active'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        return attrs
    
    def validate_role(self, value):
        """Valider que le rôle est dans les choix autorisés"""
        if value not in [choice[0] for choice in UserRole.choices]:
            raise serializers.ValidationError("Rôle invalide.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la modification d'utilisateur"""
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'role', 'is_active'
        ]
    
    def validate_role(self, value):
        """Valider que le rôle est dans les choix autorisés"""
        if value not in [choice[0] for choice in UserRole.choices]:
            raise serializers.ValidationError("Rôle invalide.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    """Serializer pour la réinitialisation de mot de passe"""
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": "Les mots de passe ne correspondent pas."
            })
        return attrs


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer pour les logs d'audit"""
    user_display = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_type_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_display', 'username', 'action_type',
            'action_display', 'ip_address', 'user_agent', 'details', 'timestamp'
        ]
        read_only_fields = fields
    
    def get_user_display(self, obj):
        if obj.user:
            return f"{obj.user.get_full_name()} ({obj.user.username})"
        return obj.username
