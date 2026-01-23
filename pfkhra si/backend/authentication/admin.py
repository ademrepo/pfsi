from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AuditLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Interface d'administration pour CustomUser"""
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role',)
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Interface d'administration pour AuditLog"""
    list_display = ['username', 'action_type', 'ip_address', 'timestamp']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['user', 'username', 'action_type', 'ip_address', 'user_agent', 'details', 'timestamp']
    
    def has_add_permission(self, request):
        """Empêcher l'ajout manuel de logs"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Empêcher la modification des logs"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Empêcher la suppression des logs (traçabilité)"""
        return False
