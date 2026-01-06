import requests
import sys

# Force UTF-8 for Windows console
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://livinpg-backend.onrender.com"

def diagnose_server():
    print(f"Checking Server: {BASE_URL}")

    # 1. Check Root
    try:
        res = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"Root: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Root Error: {e}")

    # 2. Check Login
    print("Checking Login...")
    try:
        res = requests.post(f"{BASE_URL}/users/login", json={"email": "admin@example.com", "password": "admin123"}, timeout=10)
        print(f"Login: {res.status_code}")
        if res.status_code != 200:
             print(f"Error Body: {res.text}")
        else:
             print("Login OK")
    except Exception as e:
        print(f"Login Error: {e}")

if __name__ == "__main__":
    diagnose_server()
