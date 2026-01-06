import requests
import sys
import random

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "admin_check@example.com"
PWD = "password123"

def run():
    print(f"--- Verifying Admin Endpoints at {BASE_URL} ---")
    
    # 1. Register Admin (if not exists)
    print("1. Registering/Checking Admin User...")
    try:
        requests.post(f"{BASE_URL}/users/register", json={
            "full_name": "Admin Check",
            "email": EMAIL,
            "password": PWD,
            "phone": "9999999999",
            "role": "admin"
        })
    except Exception as e:
        print(f"Registration request failed: {e}")

    # 2. Login
    print("2. Logging in...")
    login_res = requests.post(f"{BASE_URL}/users/login", json={"email": EMAIL, "password": PWD})
    if login_res.status_code != 200:
        print(f"LOGIN FAILED: {login_res.text}")
        sys.exit(1)
        
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Login Successful.")

    # 3. Test /stats
    print("3. Testing /stats endpoint...")
    stats_res = requests.get(f"{BASE_URL}/stats", headers=headers)
    print(f"   Status: {stats_res.status_code}")
    if stats_res.status_code == 200:
        print(f"   Response: {stats_res.json()}")
    else:
        print(f"   ERROR: {stats_res.text}")

    # 4. Test /complaints/all
    print("4. Testing /complaints/all endpoint...")
    comp_res = requests.get(f"{BASE_URL}/complaints/all", headers=headers)
    print(f"   Status: {comp_res.status_code}")
    if comp_res.status_code == 200:
        # print first 2
        print(f"   Count: {len(comp_res.json())}")
    else:
        print(f"   ERROR: {comp_res.text}")

    # 5. Test /payments
    print("5. Testing /payments endpoint...")
    pay_res = requests.get(f"{BASE_URL}/payments", headers=headers)
    print(f"   Status: {pay_res.status_code}")
    if pay_res.status_code == 200:
         print(f"   Count: {len(pay_res.json())}")
    else:
        print(f"   ERROR: {pay_res.text}")

if __name__ == "__main__":
    run()
