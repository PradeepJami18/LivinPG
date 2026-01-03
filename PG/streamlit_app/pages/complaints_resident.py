import streamlit as st
import requests
from components.bottom_nav import resident_nav
from utils.theme import apply_theme

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Raise Complaint | Smart PG",
    layout="centered"
)

# ---------------- THEME ----------------
theme = apply_theme()

# ---------------- SECURITY ----------------
if "token" not in st.session_state:
    st.switch_page("pages/login_page.py")

if st.session_state.role != "resident":
    st.switch_page("pages/admin_dashboard.py")

# ---------------- COMPLAINTS (BACKEND) ----------------
import os
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
HEADERS = {
    "Authorization": f"Bearer {st.session_state.token}"
}

# ---------------- HEADER ----------------
# ---------------- HEADER ----------------
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("## 🧾 Raise a Complaint")
    st.caption("We’re here to help. Report any issue below.")
with col2:
    is_dark = st.session_state.theme == "dark"
    if st.toggle("🔆", value=is_dark, key="theme_toggle_cr"):
        st.session_state.theme = "dark"
        st.rerun()
    else:
        st.session_state.theme = "light"
        if st.session_state.theme != theme:
            st.rerun()

st.divider()

# ---------------- COMPLAINT FORM ----------------
with st.form("complaint_form"):
    category = st.selectbox(
        "Complaint Type",
        ["Water", "Electricity", "Food", "Cleanliness", "Room Issue", "Other"]
    )

    description = st.text_area(
        "Describe the issue",
        placeholder="Explain the problem clearly...",
        height=120
    )

    submit = st.form_submit_button("🚀 Submit Complaint")

    if submit:
        if not description:
            st.error("❌ Please describe the issue")
        else:
            try:
                res = requests.post(
                    f"{BASE_URL}/complaints",
                    headers=HEADERS,
                    json={
                        "category": category,
                        "description": description
                    }
                )

                if res.status_code == 200:
                    st.success("✅ Complaint submitted successfully")
                else:
                    st.error("❌ Failed to submit complaint")

            except:
                st.error("🚫 Backend not reachable")

st.divider()

# ---------------- VIEW COMPLAINT STATUS ----------------
st.markdown("### 📋 Your Complaints")

try:
    res = requests.get(
        f"{BASE_URL}/complaints/my",
        headers=HEADERS
    )

    if res.status_code == 200:
        complaints = res.json()

        if not complaints:
            st.info("No complaints submitted yet")
        else:
            for c in complaints:
                # Use theme classes
                status_cls = "status-resolved" if c['status'] == "Resolved" else "status-pending"
                st.markdown(
                    f"""
                    <div class="app-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4>🧾 {c['category']}</h4>
                            <span class="status-badge {status_cls}">{c['status']}</span>
                        </div>
                        <p style="margin-top:8px;">{c['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.error("Unable to fetch complaints")

except:
    st.error("🚫 Backend not reachable")

# ---------------- BOTTOM NAV ----------------
st.divider()
resident_nav(current="complaints")
