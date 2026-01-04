import requests

from utils.config import BASE_URL

def register_user(data):
    return requests.post(f"{BASE_URL}/users/register", json=data)

def login_user(data):
    return requests.post(f"{BASE_URL}/users/login", json=data)

def add_complaint(token, data):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(f"{BASE_URL}/complaints", json=data, headers=headers)

def get_food_menu():
    return requests.get(f"{BASE_URL}/food")
