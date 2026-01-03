import streamlit as st
import requests
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Forgot Password | Smart PG", layout="centered")

import os
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# ---------------- STYLES ----------------
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
    }
    .auth-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        max_width: 400px;
        margin: auto;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.markdown('<div class="auth-card">', unsafe_allow_html=True)
st.title("🔐 Reset Password")
st.markdown("Enter your registered email to set a new password.")

with st.form("reset_form"):
    email = st.text_input("Email Address", placeholder="john@example.com")
    new_password = st.text_input("New Password", type="password", placeholder="Enter new password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter new password")
    
    submit = st.form_submit_button("Reset Password", use_container_width=True)

    if submit:
        if not email or not new_password:
            st.error("Please fill in all fields")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            try:
                res = requests.put(
                    f"{BASE_URL}/users/reset-password",
                    json={"email": email, "new_password": new_password}
                )
                
                if res.status_code == 200:
                    st.success("✅ Password updated successfully!")
                    time.sleep(1)
                    st.switch_page("pages/login_page.py")
                elif res.status_code == 404:
                    st.error("❌ Email not found.")
                else:
                    st.error(f"❌ Failed to reset. Error: {res.text}")
            except Exception as e:
                st.error(f"Server error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅ Back to Login"):
        st.switch_page("pages/login_page.py")
