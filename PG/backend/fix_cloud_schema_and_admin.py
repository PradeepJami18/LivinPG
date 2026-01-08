import requests
import time

BASE_URL = "https://livinpg-backend.onrender.com"

def fix_and_restore():
    print(f"Target: {BASE_URL}")

    # Step 1: Fix Schema (Wipe & Recreate)
    print("\n--- Step 1: Triggering DB Schema Fix (Drop & Recreate) ---")
    try:
        res = requests.get(f"{BASE_URL}/fix-db-schema", timeout=30)
        if res.status_code == 200:
            print("✅ Schema Fixed Successfully!")
            print(f"Response: {res.json()}")
        else:
            print(f"❌ Failed to fix schema: {res.status_code} - {res.text}")
            return
    except Exception as e:
        print(f"❌ Connection Error during Schema Fix: {e}")
        return

    # Wait a moment for DB to settle
    time.sleep(2)

    # Step 2: Create Admin
    print("\n--- Step 2: Re-creating Admin Account ---")
    admin_payload = {
        "full_name": "PG Owner",
        "email": "admin@example.com",
        "password": "admin123",
        "phone": "9876543210",
        "role": "admin"
    }

    try:
        res = requests.post(f"{BASE_URL}/users/register", json=admin_payload)
        if res.status_code == 200:
            print("✅ Admin Account Created Successfully!")
            print(f"Admin Credentials -> Email: admin@example.com | Pass: admin123")
        elif res.status_code == 400 and "already exists" in res.text:
            print("ℹ️ Admin account already exists (unexpected after wipe, but okay).")
        else:
            print(f"❌ Failed to create admin: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"❌ Connection Error during Admin Creation: {e}")

if __name__ == "__main__":
    fix_and_restore()
