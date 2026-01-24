#!/usr/bin/env python
import os
import django
import json
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_management.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate

client = Client()

try:
    # Test login endpoint
    response = client.post(
        '/api/auth/login/',
        json.dumps({
            'username': 'admin',
            'password': 'password123'
        }),
        content_type='application/json'
    )

    print(f"Status Code: {response.status_code}")
    try:
        data = json.loads(response.content.decode())
        print(f"Response JSON: {json.dumps(data, indent=2)}")
    except:
        print(f"Content (first 500 chars): {response.content.decode()[:500]}")
except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()
