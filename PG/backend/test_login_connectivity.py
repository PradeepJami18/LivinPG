import requests
import sys
import random
import time

BASE_URL = "http://127.0.0.1:8000"

def run():
    print(f"Checking {BASE_URL}...")
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
    except requests.exceptions.ConnectionError:
        print("SERVER_DOWN")
        return

    # Register random user to ensure we can log in
    email = f"test_{random.randint(1000,9999)}@example.com"
    pwd = "password123"
    
    print(f"Registering {email}...")
    reg = requests.post(f"{BASE_URL}/users/register", json={
        "full_name": "Test User",
        "email": email,
        "password": pwd,
        "phone": "1234567890",
        "role": "resident"
    })
    
    if reg.status_code != 200:
        # If user exists, that's fine, we try to login anyway (though with random it shouldn't happen often)
        print(f"Registration response: {reg.status_code} {reg.text}")

    # Login
    print(f"Logging in...")
    login = requests.post(f"{BASE_URL}/users/login", json={"email": email, "password": pwd})
    
    if login.status_code == 200 and "access_token" in login.json():
        print("LOGIN_SUCCESS")
        print("Token received.")
    else:
        print(f"LOGIN_FAILED: {login.status_code} {login.text}")

if __name__ == "__main__":
    run()
