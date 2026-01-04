import streamlit as st
import requests
from components.bottom_nav import admin_nav

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Complaints | Admin", layout="wide")

# ---------------- SECURITY ----------------
if "token" not in st.session_state:
    st.switch_page("pages/login_page.py")

if st.session_state.role != "admin":
    st.switch_page("pages/resident_dashboard.py")

from utils.config import BASE_URL
HEADERS = {
    "Authorization": f"Bearer {st.session_state.token}"
}

# ---------------- HEADER ----------------
st.markdown("## 🛠️ Complaints Management")
st.caption("Resolve resident issues")

st.divider()

# ---------------- FETCH COMPLAINTS ----------------
r = requests.get(f"{BASE_URL}/complaints/all", headers=HEADERS)

if r.status_code != 200:
    st.error("Unable to fetch complaints")
    st.stop()

complaints = r.json()

for c in complaints:
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(f"""
        <div style="background:#ffffff;padding:16px;border-radius:16px;color:#0f172a;border:1px solid #e2e8f0;">
            <b>Resident:</b> {c['user']['full_name']} ({c['user']['email']})<br>
            <b>Category:</b> {c['category']}<br>
            <b>Description:</b> {c['description']}<br>
            <b>Status:</b> {c['status']}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if c["status"] == "Pending":
            if st.button("✅ Resolve", key=c["id"]):
                rr = requests.put(
                    f"{BASE_URL}/complaints/{c['id']}/resolve",
                    headers=HEADERS
                )

                if rr.status_code == 200:
                    st.success("Resolved")
                    st.rerun()
                else:
                    st.error("Failed to resolve")

    st.markdown("<br>", unsafe_allow_html=True)

# ---------------- NAV ----------------
st.divider()
admin_nav(current="complaints")
