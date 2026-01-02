import streamlit as st

def resident_nav(current="home"):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏠 Home", use_container_width=True):
            if current != "home":
                st.switch_page("pages/resident_dashboard.py")

    with col2:
        if st.button("🍽️ Food", use_container_width=True):
            if current != "food":
                st.switch_page("pages/foodmenu_resident.py")

    with col3:
        if st.button("🧾 Complaints", use_container_width=True):
            if current != "complaints":
                st.switch_page("pages/complaints_resident.py")

    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("pages/login_page.py")
def admin_nav(current="dashboard"):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/admin_dashboard.py")

    with col2:
        if st.button("🍽️ Food", use_container_width=True):
            st.switch_page("pages/foodmenu_admin.py")

    with col3:
        if st.button("🧾 Complaints", use_container_width=True):
            st.switch_page("pages/complaints_admin.py")

    with col4:
        st.button("👥 Residents", use_container_width=True)

    with col5:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("pages/login_page.py")
