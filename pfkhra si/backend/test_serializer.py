#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_management.settings')
django.setup()

from authentication.serializers import LoginSerializer

# Test serializer directly
data = {
    'username': 'admin',
    'password': 'password123'
}

serializer = LoginSerializer(data=data)
print(f"Is valid: {serializer.is_valid()}")
print(f"Errors: {serializer.errors}")
print(f"Validated data: {serializer.validated_data if serializer.is_valid() else 'N/A'}")

# Test with invalid password
data2 = {
    'username': 'admin',
    'password': 'wrongpassword'
}

serializer2 = LoginSerializer(data=data2)
print(f"\nWrong password:")
print(f"Is valid: {serializer2.is_valid()}")
print(f"Errors: {serializer2.errors}")
