import requests
import streamlit as st

from utils.config import BASE_URL

def login_user(email, password):
    try:
        r = requests.post(
            f"{BASE_URL}/users/login",
            json={"email": email, "password": password}
        )

        if r.status_code == 200:
            data = r.json()
            st.session_state.token = data["access_token"]
            st.session_state.role = data["role"]
            st.session_state.name = data.get("full_name", "")
            return True
        else:
            return False
    except Exception:
        return False
