import os
import urllib.parse
from dotenv import load_dotenv, find_dotenv

def check_host():
    load_dotenv(find_dotenv())
    
    db_url = os.getenv("DATABASE_URL", "")
    db_host = os.getenv("DB_HOST", "localhost")
    
    print(f"--- DATABASE CONFIG CHECK ---")
    if db_url:
        # Mask password
        try:
            parsed = urllib.parse.urlparse(db_url)
            print(f"Target Host (from DATABASE_URL): {parsed.hostname}")
            if "render" in str(parsed.hostname):
                print(">> Connected to RENDER (Cloud) <<")
            else:
                print(f">> Connected to {parsed.hostname} <<")
        except:
            print(f"Target Host (from DATABASE_URL): Unable to parse")
    else:
        print(f"Target Host (from DB_HOST): {db_host}")
        if db_host in ["localhost", "127.0.0.1"]:
            print(">> Connected to LOCALHOST (Your Laptop) <<")
        else:
            print(f">> Connected to {db_host} <<")

if __name__ == "__main__":
    check_host()
