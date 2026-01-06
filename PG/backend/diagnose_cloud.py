import requests
import json

BASE_URL = "https://livinpg-backend.onrender.com"

def diagnose_server():
    print(f"Checking Server: {BASE_URL}")

    # 1. Check Root Endpoint
    try:
        res = requests.get(f"{BASE_URL}/")
        print(f"Root Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"❌ Root Check Connection Failed: {e}")

    # 2. Check Login (to see if it hits DB error)
    print("\nAttempting Login (Diag)...")
    try:
        payload = {"email": "admin@example.com", "password": "admin123"}
        res = requests.post(f"{BASE_URL}/users/login", json=payload)
        
        print(f"Login Status: {res.status_code}")
        if res.status_code == 500:
            print("❌ INTERNAL SERVER ERROR")
            print("Response:", res.text)
        elif res.status_code == 200:
            print("✅ Login SUCCESS")
        else:
            print(f"Login Failed: {res.text}")

    except Exception as e:
        print(f"❌ Login Connection Failed: {e}")

if __name__ == "__main__":
    diagnose_server()
