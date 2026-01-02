import streamlit as st
import requests
from utils.theme import apply_theme

import os
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Register | Smart PG Living",
    layout="wide"
)

# ---------------- THEME ----------------
# Ensures the page is white (Light Mode)
if "theme" not in st.session_state:
    st.session_state.theme = "light"
theme = apply_theme()

# Hide Streamlit sidebar navigation
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)




# ---------------- HEADER ----------------
col_pad1, col_center, col_pad2 = st.columns([1, 2, 1])
with col_center:
    try:
        st.image("streamlit_app/assets/logo.JPG", width=120, use_container_width=False)
    except:
        st.warning("Logo not found")

st.markdown("""
    <div style='text-align: center; color: #c2410c; font-weight: 800; font-size: 32px; margin-top: 10px; margin-bottom: 2px; text-transform: uppercase;'>
        LivinPG
    </div>
    <div style='text-align: center; color: #6b7280; font-size: 16px; margin-bottom: 20px;'>
        Create New Account
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

# Track registration success
if "registered" not in st.session_state:
    st.session_state.registered = False

with st.form("register_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Register as",
        ["resident", "admin"]
    )

    submit = st.form_submit_button("Create Account")

    if submit:
        if not full_name or not email or not phone or not password:
            st.error("❌ Please fill all fields")
        else:
            response = requests.post(
                f"{BASE_URL}/users/register",
                json={
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "password": password,
                    "role": role
                }
            )

            if response.status_code == 200:
                st.success("✅ Account created successfully")
                st.info("Please login to continue")
                st.session_state.registered = True
            else:
                try:
                    st.error(response.json().get("detail", "Registration failed"))
                except:
                    st.error("❌ Registration failed")

# 👉 Navigation button OUTSIDE the form
if st.session_state.registered:
    st.markdown("---")
    if st.button("🔐 Go to Login"):
        st.session_state.registered = False
        st.switch_page("pages/login_page.py")
