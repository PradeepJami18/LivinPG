import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def register_admin():
    print("--- Registering Default Admin ---")
    
    email = "admin@example.com"
    password = "admin123"
    
    payload = {
        "full_name": "System Admin",
        "email": email,
        "password": password,
        "phone": "9999999999",
        "role": "admin"
    }

    try:
        # 1. Try Register
        res = requests.post(f"{BASE_URL}/users/register", json=payload)
        
        if res.status_code == 200:
            print("SUCCESS: Admin created.")
            print(f"Email: {email}")
            print(f"Password: {password}")
        elif res.status_code == 400 and "already exists" in res.text:
             print("INFO: Admin already exists.")
             print(f"Email: {email}")
             print("Password: (Unknown, possibly 'admin123')")
        else:
            print(f"ERROR: Failed to register. {res.status_code} {res.text}")
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    register_admin()
