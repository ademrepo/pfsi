import requests
import json

BASE_URL = "http://localhost:8000/api"

# Test login
print("Testing login with admin / password123...")
response = requests.post(
    f"{BASE_URL}/auth/login/",
    json={
        "username": "admin",
        "password": "password123"
    },
    headers={
        "Content-Type": "application/json"
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print(f"Cookies: {response.cookies}")
