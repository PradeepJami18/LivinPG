import streamlit as st
import requests
import datetime
from utils.theme import apply_theme

import os
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Admin | Smart PG Living",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- THEME & STYLES ----------------
theme = apply_theme()

# ---------------- STATE MANAGEMENT ----------------
if "token" not in st.session_state or st.session_state.token is None:
    st.switch_page("pages/login_page.py")

if st.session_state.role != "admin":
    st.switch_page("pages/resident_dashboard.py")


if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"



headers = {"Authorization": f"Bearer {st.session_state.token}"}


# ---------------- HEADER ----------------
col_head1, col_head2, col_head3 = st.columns([5, 2, 1.5])

with col_head1:
    st.markdown("## ⚡ Smart PG Admin")

with col_head2:
    # Theme Toggle
    is_dark = st.session_state.theme == "dark"
    if st.toggle("🔆", value=is_dark, key="theme_toggle_adm"):
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"
        
    if st.session_state.theme != theme:
         st.rerun()

with col_head3:
    if st.button("🚪 Logout", key="top_logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/login_page.py")

# ---------------- MAIN CONTENT AREA ----------------
tab = st.session_state.active_tab

if tab == "Dashboard":
    # FETCH REAL STATS
    total_residents = 0
    revenue = 0
    pending_revenue = 0
    capacity = 100
    active_issues = 0
    staff = 0
    
    try:
        s_res = requests.get(f"{BASE_URL}/stats", headers=headers)
        if s_res.status_code == 200:
            stats = s_res.json()
            total_residents = stats.get("total_residents", 0)
            revenue = stats.get("revenue", 0)
            pending_revenue = stats.get("pending_revenue_count", 0)
            capacity = stats.get("capacity", 100)
            active_issues = stats.get("active_issues", 0)
            staff = stats.get("total_staff", 0)
    except:
        pass

    st.markdown(f"""
    <div class="app-card">
        <h3 style="margin:0;">PG Overview</h3>
        <p style="font-size:14px;">Real-time insights.</p>
    </div>
    """, unsafe_allow_html=True)

    # ROW 1
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="app-card" style="padding:16px;">
            <div class="stat-label">Residents</div>
            <div class="stat-value">{total_residents}</div>
            <div class="stat-sub">Occupancy: {total_residents}/{capacity}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="app-card" style="padding:16px;">
            <div class="stat-label">Revenue</div>
            <div class="stat-value">₹ {revenue}</div>
            <div class="stat-sub">Pending txns: {pending_revenue}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="app-card" style="padding:16px;">
            <div class="stat-label">Issues</div>
            <div class="stat-value" style="color:#facc15;">{active_issues}</div>
            <div class="stat-sub">Active Tickets</div>
        </div>
        """, unsafe_allow_html=True)

elif tab == "Payments":
    st.markdown("### 💸 Payment Approvals")

    # QR CODE UPLOAD SECTION
    col_qr1, col_qr2 = st.columns([3, 1])
    with col_qr1:
        st.info("ℹ️ Upload your Payment QR Code here. Residents will see this to scan and pay.")
    with col_qr2:
        qr_file = st.file_uploader("Upload QR", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        if qr_file is not None:
            # Ensure assets directory exists
            import os
            os.makedirs("streamlit_app/assets", exist_ok=True)
            with open("streamlit_app/assets/qrcode.png", "wb") as f:
                f.write(qr_file.getbuffer())
            st.success("QR Code Updated!")
    
    st.markdown("---")
    
    try:
        p_r = requests.get(f"{BASE_URL}/payments", headers=headers)
        if p_r.status_code == 200:
            payments = p_r.json()
            if not payments:
                st.info("No payment records found.")
            else:
                for p in payments:
                    status_color = "chip-green" if p['status'] == "Approved" else "chip-yellow"
                    user_name = p.get('user_name', 'Unknown Resident')
                    
                    st.markdown(f"""
                    <div class="app-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-size:18px; font-weight:700;">₹ {p['amount']}</span>
                                <div style="font-size:14px; font-weight:600;">{user_name}</div>
                                <div style="font-size:12px;">ID: {p['transaction_id']}</div>
                                <div style="font-size:12px;">Date: {p['created_at'].split('T')[0]}</div>
                            </div>
                            <span class="status-badge {status_color}">{p['status']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if p['status'] == "Pending":
                        if st.button(f"Approve #{p['id']}", key=f"pay_{p['id']}", use_container_width=True):
                            requests.put(f"{BASE_URL}/payments/{p['id']}/approve", headers=headers)
                            st.rerun()
        else:
            st.error("Failed to load payments")
    except:
        st.error("Connection error")

elif tab == "Residents":
    col_r1, col_r2 = st.columns([4,1])
    with col_r1:
        st.markdown("### 👥 Residents Directory")
    with col_r2:
        if st.button("🔄 Sync"):
            st.rerun()

    try:
        r = requests.get(f"{BASE_URL}/users/residents", headers=headers)
        if r.status_code == 200:
            residents = r.json()
            for res in residents:
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(f"""
                    <div class="app-card" style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0px;">
                        <div>
                            <div style="font-weight:700; font-size:16px;">{res['full_name']}</div>
                            <div style="font-size:14px;">{res['email']}</div>
                        </div>
                        <span class="status-badge chip-blue">Resident</span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.write("")
                    if st.button("🗑️", key=f"del_{res['id']}", help="Remove Resident", use_container_width=True):
                         try:
                             d_res = requests.delete(f"{BASE_URL}/users/{res['id']}", headers=headers)
                             if d_res.status_code == 200:
                                 st.success("Removed!")
                                 st.rerun()
                             else:
                                 st.error("Failed")
                         except:
                             st.error("Error")
        else:
            st.error("Failed to load residents")
    except:
        st.error("Backend error")

elif tab == "Complaints":
    st.markdown("### 📝 Issues Tracker")
    
    try:
        r = requests.get(f"{BASE_URL}/complaints/all", headers=headers)
        if r.status_code == 200:
            complaints = r.json()
            if not complaints:
                st.info("No active issues.")
            else:
                for c in complaints:
                    status_cls = "chip-green" if c["status"] == "Resolved" else "chip-yellow"
                    
                    st.markdown(f"""
                    <div class="app-card">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="font-weight:700;">{c['category']}</span>
                            <span class="status-badge {status_cls}">{c['status']}</span>
                        </div>
                        <div style="font-size:14px; margin-top:8px;">{c['description']}</div>
                        <div style="font-size:12px; margin-top:12px; text-align:right;">
                            Raised by: {c['user']['full_name']} | ID: #{c['id']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if c["status"] != "Resolved":
                        if st.button(f"Mark Resolved #{c['id']}", key=f"res_{c['id']}"):
                            requests.put(f"{BASE_URL}/complaints/{c['id']}/resolve", headers=headers)
                            st.rerun()
        else:
            st.error("Failed to fetch issues")
    except:
        st.error("Connection error")

elif tab == "Food":
    st.markdown("### 🍽️ Kitchen Manager")
    
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("#### Update Weekly Menu")
    with st.form("food_menu_update"):
        col1, col2 = st.columns(2)
        with col1:
             day = st.selectbox("Select Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        breakfast = st.text_input("🍳 Breakfast")
        lunch = st.text_input("🍛 Lunch")
        dinner = st.text_input("🌙 Dinner")
        
        if st.form_submit_button("Update Menu", use_container_width=True):
            try:
                r = requests.post(f"{BASE_URL}/food", json={"day": day, "breakfast": breakfast, "lunch": lunch, "dinner": dinner}, headers=headers)
                if r.status_code == 200:
                    st.success("Menu updated!")
                else:
                    st.error("Update failed")
            except:
                st.error("Connection failed")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- BOTTOM NAV (Resident Style) ----------------
st.markdown("---") # Separator
nav_c1, nav_c2, nav_c3, nav_c4, nav_c5, nav_c6 = st.columns(6)

with nav_c1:
    if st.button("⚡ Dash", key="nav_d", use_container_width=True):
        st.session_state.active_tab = "Dashboard"
        st.rerun()
with nav_c2:
    if st.button("💸 Pay", key="nav_p", use_container_width=True):
        st.session_state.active_tab = "Payments"
        st.rerun()
with nav_c3:
    if st.button("🍽️ Food", key="nav_f", use_container_width=True):
        st.session_state.active_tab = "Food"
        st.rerun()
with nav_c4:
    if st.button("📝 Issue", key="nav_c", use_container_width=True):
        st.session_state.active_tab = "Complaints"
        st.rerun()
with nav_c5:
    if st.button("👥 Users", key="nav_u", use_container_width=True):
        st.session_state.active_tab = "Residents"
        st.rerun()
with nav_c6:
    if st.button("🚪 Exit", key="nav_out", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/login_page.py")



