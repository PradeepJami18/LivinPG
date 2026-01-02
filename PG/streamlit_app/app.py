import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart PG Living",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- HIDE SIDEBAR ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DEFAULTS ----------------
if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.name = None

# ---------------- ROUTING ----------------
if st.session_state.token is None:
    st.switch_page("pages/login_page.py")   # filename only
else:
    if st.session_state.role == "admin":
        st.switch_page("pages/admin_dashboard.py")
    else:
        st.switch_page("pages/resident_dashboard.py")