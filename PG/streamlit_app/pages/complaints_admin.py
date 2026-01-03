import streamlit as st
import requests
from components.bottom_nav import admin_nav
from utils.theme import apply_theme

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Manage Complaints | Smart PG",
    layout="wide"
)

# ---------------- THEME ----------------
theme = apply_theme()

# ---------------- SECURITY ----------------
if "token" not in st.session_state:
    st.switch_page("pages/login_page.py")

if st.session_state.role != "admin":
    st.switch_page("pages/resident_dashboard.py")

BASE_URL = "http://127.0.0.1:8000"
HEADERS = {
    "Authorization": f"Bearer {st.session_state.token}"
}

# ---------------- HEADER ----------------
# ---------------- HEADER ----------------
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("## 🧾 Complaints Management")
    st.caption("View and resolve resident issues")
with col2:
    is_dark = st.session_state.theme == "dark"
    if st.toggle("🔆", value=is_dark, key="theme_toggle_ca"):
        st.session_state.theme = "dark"
        st.rerun()
    else:
        st.session_state.theme = "light"
        if st.session_state.theme != theme:
            st.rerun()

st.divider()

# ---------------- FETCH COMPLAINTS ----------------
try:
    res = requests.get(
        f"{BASE_URL}/complaints/all",
        headers=HEADERS
    )

    if res.status_code == 200:
        complaints = res.json()

        if not complaints:
            st.info("No complaints available")
        else:
            for c in complaints:
                status_cls = "chip-green" if c["status"] == "Resolved" else "chip-yellow"

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(
                        f"""
                        <div class="app-card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <h4>🧾 {c['category']}</h4>
                                <span class="status-badge {status_cls}">{c['status']}</span>
                            </div>
                            <p style="margin-top:8px;">{c['description']}</p>
                            <p style="font-size:12px; margin-top:8px; color:inherit; opacity:0.8;">
                                👤 <b>{c['user']['full_name']}</b> | 
                                📧 {c['user']['email']}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:
                    if c["status"] != "Resolved":
                        if st.button(
                            "✅ Resolve",
                            key=f"resolve_{c['id']}"
                        ):
                            requests.put(
                                f"{BASE_URL}/complaints/{c['id']}/resolve",
                                headers=HEADERS
                            )
                            st.rerun()

    else:
        st.error("❌ Failed to load complaints")

except:
    st.error("🚫 Backend not reachable")

# ---------------- BOTTOM NAV ----------------
st.divider()
admin_nav(current="complaints")
