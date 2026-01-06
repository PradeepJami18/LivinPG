import requests
import os
import time
import sys

BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "persistent_admin@example.com"
PWD = "password123"
DB_FILE = "sql_app.db"

def run():
    print("--- Reproducing Token Reuse Issues ---")

    # 1. Register & Login to get Token
    print("1. Registering Admin...")
    try:
        requests.post(f"{BASE_URL}/users/register", json={
            "full_name": "Admin", "email": ADMIN_EMAIL, "password": PWD, "phone": "123", "role": "admin"
        })
    except: pass # maybe exists

    print("2. Logging in...")
    login = requests.post(f"{BASE_URL}/users/login", json={"email": ADMIN_EMAIL, "password": PWD})
    if login.status_code != 200:
        print("Login failed")
        return
    token = login.json()["access_token"]
    print(f"   Token recieved: {token[:10]}...")

    # 3. Simulate DB Reset (We can't easily kill/restart server from here, but we can delete the user via API or raw SQL if we had access, but actually the USER simulated this by deleting sql_app.db)
    # Since I cannot restart the server process from this script (it runs separately), I will assume the server is running with a NEW DB.
    # To mimic 'Token valid but Data gone', I will simply DELETE the admin user from DB via API, then try to use the token.
    # Wait, if I delete the admin user, get_residents check:
    # current_user = get_current_user (decodes token) -> OK
    # current_user["role"] == "admin" -> OK
    # db query ... -> OK.
    
    # So deleting user shouldn't affect get_residents if auth.py doesn't check DB.
    
    print("3. Checking /back residents with this token...")
    res = requests.get(f"{BASE_URL}/users/residents", headers={"Authorization": f"Bearer {token}"})
    print(f"   Status: {res.status_code}")
    print(f"   Body: {res.text}")

    if res.status_code == 200:
        print("   Success! (This implies token reuse IS allowed and works).")
    else:
        print("   Failed! (This implies something is wrong).")

if __name__ == "__main__":
    run()
