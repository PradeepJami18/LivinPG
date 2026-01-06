import requests
import random
import time

BASE_URL = "https://livinpg-backend.onrender.com"
# BASE_URL = "http://127.0.0.1:8000" # Toggle for testing local if needed

def seed_cloud_data():
    print(f"--- Seeding Data to {BASE_URL} ---")

    admin_email = "admin@example.com"
    admin_pass = "admin123"
    
    # 1. Login Admin to get Token
    print("\n[Admin] Logging in...")
    try:
        res = requests.post(f"{BASE_URL}/users/login", json={"email": admin_email, "password": admin_pass})
        if res.status_code != 200:
            print(f"❌ Admin login failed: {res.text}")
            return
        admin_token = res.json()["access_token"]
        print("✅ Admin Logged In")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    # 2. Create Dummy Residents
    residents = [
        {"name": "Alice Wonderland", "email": "alice@test.com", "pass": "pass123"},
        {"name": "Bob Builder", "email": "bob@test.com", "pass": "pass123"},
        {"name": "Charlie Chaplin", "email": "charlie@test.com", "pass": "pass123"},
    ]

    for r in residents:
        print(f"\n[Resident] Creating {r['name']}...")
        reg_res = requests.post(f"{BASE_URL}/users/register", json={
            "full_name": r['name'],
            "email": r['email'],
            "password": r['pass'],
            "phone": "9876543210",
            "role": "resident"
        })
        
        if reg_res.status_code == 200:
            print(f"✅ Created {r['name']}")
        elif "already exists" in reg_res.text:
            print(f"ℹ️ {r['name']} already exists.")
        else:
            print(f"⚠️ Failed to create {r['name']}: {reg_res.text}")
            continue

        # 3. resident login to make payments
        print(f"   Log in as {r['name']}...")
        login_res = requests.post(f"{BASE_URL}/users/login", json={"email": r['email'], "password": r['pass']})
        if login_res.status_code == 200:
            user_token = login_res.json()["access_token"]
            
            # Make a payment
            amount = random.choice([5000, 7500, 12000])
            tid = f"TXN{random.randint(10000,99999)}"
            print(f"   Making payment of ₹{amount}...")
            pay_res = requests.post(
                f"{BASE_URL}/payments", 
                json={"amount": amount, "transaction_id": tid},
                headers={"Authorization": f"Bearer {user_token}"}
            )
            
            if pay_res.status_code == 200:
                pid = pay_res.json()["id"]
                print(f"   ✅ Payment ID {pid} created. Approving as Admin...")
                
                # 4. Approve immediately using Admin Token
                approve_res = requests.put(
                    f"{BASE_URL}/payments/{pid}/approve",
                    headers={"Authorization": f"Bearer {admin_token}"}
                )
                if approve_res.status_code == 200:
                    print("   ✅ Payment Approved (Revenue Updated)")
                else:
                    print(f"   ❌ Failed to approve: {approve_res.text}")
            else:
                print(f"   ❌ Payment failed: {pay_res.text}")
        else:
            print(f"   ❌ Login failed for {r['name']}")

    print("\n--- Seeding Complete ---")
    print("Check your Mobile App Admin Dashboard now.")

if __name__ == "__main__":
    seed_cloud_data()
