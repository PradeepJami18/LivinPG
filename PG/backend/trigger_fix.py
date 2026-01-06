import requests
import time

BASE_URL = "https://livinpg-backend.onrender.com"

def fix_schema():
    print("Waiting for deployment...")
    # I'll just try immediately, user can run it later if it fails
    
    try:
        print(f"Calling {BASE_URL}/fix-db-schema ...")
        res = requests.get(f"{BASE_URL}/fix-db-schema", timeout=30)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_schema()
