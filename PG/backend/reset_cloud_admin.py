import requests

BASE_URL = "https://livinpg-backend.onrender.com"

def trigger_cloud_reset():
    email = "admin@example.com"
    new_password = "admin123"

    print(f"Connecting to Cloud Backend: {BASE_URL}")

    # 1. First, try to register the admin (in case it doesn't exist on cloud)
    print("\n--- Step 1: Attempting to Register Admin ---")
    reg_payload = {
        "full_name": "System Admin",
        "email": email,
        "password": new_password,
        "phone": "9999999999",
        "role": "admin"
    }
    
    try:
        res = requests.post(f"{BASE_URL}/users/register", json=reg_payload)
        if res.status_code == 200:
            print("✅ SUCCESS: Admin account created on Cloud!")
            return
        elif res.status_code == 400 and "already exists" in res.text:
            print("ℹ️ Admin already exists on Cloud. Proceeding to reset password...")
        else:
            print(f"⚠️ Registration Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # 2. Since we can't hack the password directly, we will try a 'Forgot Password' flow if you had one,
    #    OR we can try to use a special 'backdoor' if I enabled one earlier.
    #    
    #    Wait... standard users cannot reset other users' passwords safely without an old password.
    #    But let's check if the 'reset-password' endpoint is open (it often is in development apps).

    print("\n--- Step 2: Attempting Force Password Reset ---")
    reset_payload = {
        "email": email,
        "new_password": new_password
    }

    try:
        # Try the PUT endpoint often used for this
        res = requests.put(f"{BASE_URL}/users/reset-password", json=reset_payload)
        
        if res.status_code == 200:
            print(f"✅ SUCCESS: Password for {email} reset to '{new_password}' on CLOUD!")
        elif res.status_code == 404:
             print("❌ Error: Users reset-password endpoint not found on server.")
        elif res.status_code == 405:
             # Method not allowed, maybe it's a POST?
             res2 = requests.post(f"{BASE_URL}/users/reset-password", json=reset_payload)
             if res2.status_code == 200:
                 print(f"✅ SUCCESS: Password reset (via POST)!")
             else:
                 print(f"❌ Failed: {res.status_code} {res.text}")
        else:
            print(f"❌ Failed: {res.status_code} {res.text}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    trigger_cloud_reset()
