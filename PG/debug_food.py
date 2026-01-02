import requests

try:
    r = requests.get("http://127.0.0.1:8000/food")
    print(f"Status: {r.status_code}")
    print(f"Content: {r.text}")
    try:
        data = r.json()
        print("JSON Parsed Successfully")
        print(data)
        if isinstance(data, list):
            if len(data) > 0:
                print(f"First item keys: {data[0].keys()}")
            else:
                print("List is empty")
    except Exception as e:
        print(f"JSON Parse Error: {e}")

except Exception as e:
    print(f"Request Error: {e}")
