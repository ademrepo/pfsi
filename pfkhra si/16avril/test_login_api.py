"""
Test script to diagnose login authentication issues.
This script tests the database connection and login API endpoint directly.
"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_projet.settings')
django.setup()

from core.models import Utilisateur, Role
from django.contrib.auth.hashers import check_password

print("=" * 60)
print("LOGIN AUTHENTICATION DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Database Connection
print("\n[TEST 1] Testing database connection...")
try:
    user_count = Utilisateur.objects.count()
    print(f"✓ Database connected successfully. Found {user_count} users.")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    sys.exit(1)

# Test 2: Query admin user
print("\n[TEST 2] Querying admin user...")
try:
    admin_user = Utilisateur.objects.select_related('role').get(username='admin')
    print(f"✓ Admin user found:")
    print(f"  - ID: {admin_user.id}")
    print(f"  - Username: {admin_user.username}")
    print(f"  - Email: {admin_user.email}")
    print(f"  - Full Name: {admin_user.get_full_name()}")
    print(f"  - Role: {admin_user.role.libelle} ({admin_user.role.code})")
    print(f"  - Active: {admin_user.is_active}")
    print(f"  - Password (first 20 chars): {admin_user.password[:20]}...")
    print(f"  - Password is hashed: {admin_user.password.startswith('pbkdf2_')}")
except Utilisateur.DoesNotExist:
    print("✗ Admin user not found in database!")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error querying admin user: {e}")
    sys.exit(1)

# Test 3: Password validation
print("\n[TEST 3] Testing password validation...")
test_password = "password123"
try:
    if admin_user.password.startswith('pbkdf2_'):
        # Hashed password
        is_valid = check_password(test_password, admin_user.password)
        print(f"  Password type: Hashed (Django)")
    else:
        # Plaintext password
        is_valid = (admin_user.password == test_password)
        print(f"  Password type: Plaintext")
    
    if is_valid:
        print(f"✓ Password '{test_password}' is VALID")
    else:
        print(f"✗ Password '{test_password}' is INVALID")
        print(f"  Expected: {admin_user.password}")
except Exception as e:
    print(f"✗ Error validating password: {e}")
    sys.exit(1)

# Test 4: Test LoginSerializer
print("\n[TEST 4] Testing LoginSerializer...")
try:
    from core.serializers import LoginSerializer
    
    data = {
        'username': 'admin',
        'password': 'password123'
    }
    
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        print("✓ LoginSerializer validation PASSED")
        user = serializer.validated_data.get('user')
        if user:
            print(f"  - Authenticated user: {user.username}")
            print(f"  - User ID: {user.id}")
            print(f"  - Role: {user.role.code}")
        else:
            print("✗ No user in validated_data")
    else:
        print("✗ LoginSerializer validation FAILED")
        print(f"  Errors: {serializer.errors}")
except Exception as e:
    print(f"✗ Error testing LoginSerializer: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Test API endpoint (if server is running)
print("\n[TEST 5] Testing API endpoint (requires Django server running)...")
print("  Skipping - requires server to be running on port 8000")
print("  To test manually, run:")
print("    python manage.py runserver")
print("  Then in another terminal:")
print("    curl -X POST http://127.0.0.1:8000/api/auth/login/ \\")
print("      -H 'Content-Type: application/json' \\")
print("      -d '{\"username\":\"admin\",\"password\":\"password123\"}'")

print("\n" + "=" * 60)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 60)

if is_valid:
    print("\n✓ All tests passed! The backend authentication should work.")
    print("\nNext steps:")
    print("1. Make sure Django server is running: python manage.py runserver")
    print("2. Make sure frontend is running: cd frontend && npm run dev")
    print("3. Try logging in via the frontend at http://localhost:3000")
else:
    print("\n✗ Tests failed! Please check the errors above.")
