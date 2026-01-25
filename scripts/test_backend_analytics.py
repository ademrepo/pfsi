#!/usr/bin/env python
"""
Quick test script to verify the analytics endpoint works
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.test import RequestFactory
from core.views import analytics_advanced_view
from core.models import Utilisateur, Role

try:
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/api/analytics/advanced/')
    
    # Create a mock user
    role, _ = Role.objects.get_or_create(
        code='ADMIN_SYSTEME',
        defaults={'libelle': 'Administrateur Système'}
    )
    user, _ = Utilisateur.objects.get_or_create(
        username='test_admin',
        defaults={
            'email': 'test@example.com',
            'role': role,
            'nom': 'Test',
            'prenom': 'Admin'
        }
    )
    
    # Add user to request
    request.user_obj = user
    request.session = {}
    
    # Call the view
    response = analytics_advanced_view(request)
    
    if response.status_code == 200:
        print("✓ Analytics endpoint is working correctly!")
        print(f"Status Code: {response.status_code}")
        print(f"Response has data: {len(response.data) > 0}")
        print(f"Keys in response: {list(response.data.keys())[:5]}...")
    else:
        print(f"✗ Analytics endpoint returned error: {response.status_code}")
        print(f"Response: {response.data}")
        
except Exception as e:
    print(f"✗ Error testing analytics endpoint:")
    import traceback
    traceback.print_exc()
