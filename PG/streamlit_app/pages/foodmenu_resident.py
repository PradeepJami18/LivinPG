import streamlit as st
import requests
from components.bottom_nav import resident_nav
from utils.theme import apply_theme

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Food Menu | Smart PG",
    layout="centered"
)

# ---------------- THEME ----------------
theme = apply_theme()

# ---------------- SECURITY ----------------
if "token" not in st.session_state:
    st.switch_page("pages/login_page.py")

if st.session_state.role != "resident":
    st.switch_page("pages/admin_dashboard.py")

# ---------------- HEADER ----------------
# ---------------- HEADER ----------------
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("## 🍽️ Today’s Food Menu")
    st.caption("Healthy meals, served on time")
with col2:
    is_dark = st.session_state.theme == "dark"
    if st.toggle("🔆", value=is_dark, key="theme_toggle_fr"):
        st.session_state.theme = "dark"
        st.rerun()
    else:
        st.session_state.theme = "light"
        if st.session_state.theme != theme:
            st.rerun()

st.divider()

# ---------------- FETCH MENU (BACKEND) ----------------
BASE_URL = "http://127.0.0.1:8000"

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

try:
    response = requests.get(f"{BASE_URL}/food", headers=headers)

    if response.status_code == 200:
        menu = response.json()

        if not menu:
            st.info("🍴 Food menu not updated yet")
        else:
            for item in menu:
                st.markdown(
                    f"""
                    <div class="app-card">
                        <div class="menu-day">📅 {item['day']}</div>
                        <div class="meal-row">
                            <span class="meal-label">🍳 Breakfast</span>
                            <span class="meal-value">{item['breakfast']}</span>
                        </div>
                        <div class="meal-row">
                            <span class="meal-label">🍛 Lunch</span>
                            <span class="meal-value">{item['lunch']}</span>
                        </div>
                        <div class="meal-row">
                            <span class="meal-label">🌙 Dinner</span>
                            <span class="meal-value">{item['dinner']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.error("❌ Unable to load food menu")

except Exception:
    st.error("🚫 Backend not reachable")

# ---------------- BOTTOM NAV ----------------
st.divider()
resident_nav(current="food")
