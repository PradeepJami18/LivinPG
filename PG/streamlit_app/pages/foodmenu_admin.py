import streamlit as st
import requests
from components.bottom_nav import admin_nav
from utils.theme import apply_theme

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Food Menu Admin | Smart PG",
    layout="centered"
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
    st.markdown("## 🍽️ Manage Food Menu")
    st.caption("Add or update daily meals")
with col2:
    is_dark = st.session_state.theme == "dark"
    if st.toggle("Dark Mode", value=is_dark, key="theme_toggle_fa"):
        st.session_state.theme = "dark"
        st.rerun()
    else:
        st.session_state.theme = "light"
        if st.session_state.theme != theme:
            st.rerun()

st.divider()

# ---------------- ADD / UPDATE MENU ----------------
with st.form("food_form"):
    day = st.selectbox(
        "Day",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    breakfast = st.text_input("🍳 Breakfast")
    lunch = st.text_input("🍛 Lunch")
    dinner = st.text_input("🌙 Dinner")

    submit = st.form_submit_button("💾 Save Menu")

    if submit:
        if not all([breakfast, lunch, dinner]):
            st.error("❌ Please fill all meals")
        else:
            res = requests.post(
                f"{BASE_URL}/food",
                headers=HEADERS,
                json={
                    "day": day,
                    "breakfast": breakfast,
                    "lunch": lunch,
                    "dinner": dinner
                }
            )

            if res.status_code == 200:
                st.success("✅ Food menu updated successfully")
            else:
                st.error("❌ Failed to update menu")

st.divider()

# ---------------- VIEW EXISTING MENU ----------------
st.markdown("### 📋 Current Menu")

try:
    res = requests.get(
        f"{BASE_URL}/food",
        headers=HEADERS
    )

    if res.status_code == 200:
        menu = res.json()

        if not menu:
            st.info("No menu added yet")
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
        st.error("Unable to fetch menu")

except:
    st.error("🚫 Backend not reachable")

# ---------------- BOTTOM NAV ----------------
st.divider()
admin_nav(current="food")
