#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_management.settings')
django.setup()

from django.test import Client

client = Client()

# Test login endpoint with proper headers
response = client.post(
    '/api/auth/login/',
    json.dumps({
        'username': 'admin',
        'password': 'password123'
    }),
    content_type='application/json',
    HTTP_HOST='127.0.0.1:3001'
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(json.loads(response.content.decode()), indent=2)}")
print(f"\nCookies in response: {response.cookies}")
