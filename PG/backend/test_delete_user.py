import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "admin_check@example.com"
PWD = "password123"

def run():
    print(f"--- Testing Delete Endpoint at {BASE_URL} ---")
    
    # 1. Login as Admin
    print("1. Logging in as Admin...")
    try:
        login_res = requests.post(f"{BASE_URL}/users/login", json={"email": ADMIN_EMAIL, "password": PWD})
        if login_res.status_code != 200:
            print(f"LOGIN FAILED: {login_res.text}")
            # Try to register if login fails (maybe previous script didn't run or DB cleared)
            print("   Login failed, attempting to register admin...")
            requests.post(f"{BASE_URL}/users/register", json={
                "full_name": "Admin Check",
                "email": ADMIN_EMAIL,
                "password": PWD,
                "phone": "9999999999",
                "role": "admin"
            })
            login_res = requests.post(f"{BASE_URL}/users/login", json={"email": ADMIN_EMAIL, "password": PWD})
            if login_res.status_code != 200:
                print("   FATAL: Could not login/register admin.")
                sys.exit(1)
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Admin Login Successful.")

    # 2. Create Dummy Resident to Delete
    print("2. Creating Dummy Resident to delete...")
    res_email = "todelete@example.com"
    reg_res = requests.post(f"{BASE_URL}/users/register", json={
        "full_name": "Delete Me",
        "email": res_email,
        "password": "password",
        "phone": "0000000000",
        "role": "resident"
    })
    
    if reg_res.status_code == 200:
        user_id = reg_res.json()["id"]
        print(f"   Created user ID: {user_id}")
    elif reg_res.status_code == 400:
        # User might already exist, find ID
        print("   User likely exists, fetching residents list to find ID...")
        list_res = requests.get(f"{BASE_URL}/users/residents", headers=headers)
        users = list_res.json()
        target = next((u for u in users if u["email"] == res_email), None)
        if target:
            user_id = target["id"]
            print(f"   Found existing user ID: {user_id}")
        else:
             print("   FATAL: Could not find user to delete.")
             sys.exit(1)
    else:
        print(f"   FATAL: Error creating user: {reg_res.text}")
        sys.exit(1)

    # 3. Delete the User
    print(f"3. Deleting User ID {user_id}...")
    del_res = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    
    print(f"   Status: {del_res.status_code}")
    print(f"   Response: {del_res.text}")

    if del_res.status_code == 200:
        print("SUCCESS: User deleted.")
    else:
        print("FAILURE: Could not delete user.")

if __name__ == "__main__":
    run()
