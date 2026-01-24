#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_management.settings')
django.setup()

from authentication.models import CustomUser, UserRole

# Create test users
users_to_create = [
    ('admin', 'password123', UserRole.ADMIN_SYSTEME),
    ('agent1', 'password123', UserRole.AGENT_ADMINISTRATIF),
    ('comptable1', 'password123', UserRole.COMPTABLE),
    ('logistique1', 'password123', UserRole.RESPONSABLE_LOGISTIQUE),
]

for username, password, role in users_to_create:
    if not CustomUser.objects.filter(username=username).exists():
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            role=role,
            is_active=True
        )
        print(f'Created user: {username} ({role})')
    else:
        # Update password
        user = CustomUser.objects.get(username=username)
        user.set_password(password)
        user.is_active = True
        user.save()
        print(f'Updated user: {username} (password reset)')

# Verify users
users = CustomUser.objects.all()
print(f'\nTotal users: {users.count()}')
for u in users:
    print(f'  {u.username}: {u.role} (active={u.is_active})')
