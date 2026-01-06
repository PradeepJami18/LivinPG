import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "admin_check@example.com"
PWD = "password123"

def run():
    print(f"--- Reproducing Delete Crash at {BASE_URL} ---")
    
    # 1. Login Admin
    print("1. Logging in Admin...")
    login = requests.post(f"{BASE_URL}/users/login", json={"email": ADMIN_EMAIL, "password": PWD})
    if login.status_code != 200:
        print("   Admin login failed. Registering admin...")
        requests.post(f"{BASE_URL}/users/register", json={"full_name":"Admin","email":ADMIN_EMAIL,"password":PWD,"phone":"000","role":"admin"})
        login = requests.post(f"{BASE_URL}/users/login", json={"email": ADMIN_EMAIL, "password": PWD})
    
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create User with Data
    print("2. Creating User with linked data...")
    u_email = "linked_user@example.com"
    u_pwd = "password"
    
    # Register
    reg = requests.post(f"{BASE_URL}/users/register", json={
        "full_name": "Linked User",
        "email": u_email,
        "password": u_pwd,
        "phone": "123",
        "role": "resident"
    })
    
    if reg.status_code == 200:
        uid = reg.json()["id"]
    else:
        # fetch existing
        residents = requests.get(f"{BASE_URL}/users/residents", headers=headers).json()
        target = next((r for r in residents if r["email"] == u_email), None)
        if target:
            uid = target["id"]
        else:
            print("   Failed to get user ID.")
            return

    print(f"   Target User ID: {uid}")

    # Login as User to create complaint
    print("3. Creating dependent complaint...")
    u_login = requests.post(f"{BASE_URL}/users/login", json={"email": u_email, "password": u_pwd})
    u_token = u_login.json()["access_token"]
    
    comp_res = requests.post(f"{BASE_URL}/complaints/", headers={"Authorization": f"Bearer {u_token}"}, json={
        "category": "Test",
        "description": "Block deletion"
    })
    print(f"   Complaint created: {comp_res.status_code}")

    # 4. Try Delete as Admin
    print("4. Attempting to delete user (Expect Error)...")
    del_res = requests.delete(f"{BASE_URL}/users/{uid}", headers=headers)
    print(f"   Delete Status: {del_res.status_code}")
    print(f"   Delete Body: {del_res.text}")
    
    if del_res.status_code == 500:
        print("SUCCESS: Reproduced IntegrityError/Crash.")
    else:
        print("   Did not crash as expected (or already fixed?).")

if __name__ == "__main__":
    run()
