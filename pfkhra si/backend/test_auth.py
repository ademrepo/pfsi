#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_management.settings')
django.setup()

from authentication.models import CustomUser
from django.contrib.auth import authenticate

# Test user existence
admin_user = CustomUser.objects.filter(username='admin').first()
print(f"Admin user exists: {admin_user is not None}")
if admin_user:
    print(f"  Username: {admin_user.username}")
    print(f"  Is active: {admin_user.is_active}")
    print(f"  Role: {admin_user.role}")

# Test authentication
user = authenticate(username='admin', password='password123')
print(f"\nAuthenticate with 'admin'/'password123': {user}")

if user:
    print(f"  User: {user.username}")
    print(f"  Is active: {user.is_active}")
else:
    print("  Authentication failed")
    # Try to check if password hashing works
    if admin_user:
        print(f"  Direct check password: {admin_user.check_password('password123')}")
