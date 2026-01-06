import requests
import sys

# Force UTF-8 for Windows console
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://livinpg-backend.onrender.com"

def diagnose_server():
    print("--- DIAGNOSTIC START ---")
    try:
        res = requests.post(f"{BASE_URL}/users/login", json={"email": "admin@example.com", "password": "admin123"}, timeout=20)
        print(f"Status: {res.status_code}")
        if res.status_code != 200:
             print("ERROR DETAILS:")
             print(res.text)
        else:
             print("SUCCESS")
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    diagnose_server()
