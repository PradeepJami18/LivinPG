import streamlit as st
import requests
from components.bottom_nav import resident_nav
from utils.theme import apply_theme

import os
from utils.config import BASE_URL

# ---------------- PAGE CONFIG (FIRST) ----------------
st.set_page_config(
    page_title="Resident | Smart PG Living",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- THEME & STYLES ----------------
theme = apply_theme()

# ---------------- SECURITY ----------------
if "token" not in st.session_state or st.session_state.token is None:
    st.switch_page("pages/login_page.py")

if st.session_state.role != "resident":
    st.switch_page("pages/admin_dashboard.py")

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

# ---------------- HIDE SIDEBAR & NAV (Handled by theme somewhat, but ensuring consistency) ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
[data-testid="stSidebarNav"] {display:none;}
/* Form Styles */
div[data-testid="stForm"] {
    background: transparent;
    border: none;
    padding: 0;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([5, 2, 1.5])

with col1:
    st.markdown("## 🏠 Smart PG Living")

with col2:
    # Theme Toggle
    is_dark = st.session_state.theme == "dark"
    if st.toggle("🔆", value=is_dark, key="theme_toggle_res"):
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"
    # Note: st.toggle automatically triggers rerun on change usually, but sometimes needs help.
    # We rely on the rerun loop. If needed we can force it.
    if st.session_state.theme != theme: # If changed
         st.rerun()

with col3:
    if st.button("🚪 Logout", key="logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/login_page.py")

st.markdown(f"""
<div class="app-card">
    <div class="title">Welcome Back, {st.session_state.name.split(' ')[0]}! 👋</div>
    <div class="subtitle">Have a great day at your second home.</div>
</div>
""", unsafe_allow_html=True)

# ---------------- TABS ----------------
# ---------------- TABS ----------------
tab1, tab_pay, tab2 = st.tabs(["🍽️ Food Menu", "💸 Payments", "🛠️ Support & Complaints"])

# ---------------- TAB 1: FOOD MENU ----------------
with tab1:
    col_a, col_b = st.columns([4, 1])
    with col_a:
        st.markdown('<div class="section-header">Weekly Meal Plan</div>', unsafe_allow_html=True)
    with col_b:
        if st.button("🔄 Refresh", key="refresh_food"):
            st.rerun()

    try:
        r = requests.get(f"{BASE_URL}/food", headers=headers)

        if r.status_code == 200:
            menu = r.json()
            if not menu:
                st.info("🍴 The kitchen hasn't posted the menu yet.")
            else:
                for item in menu:
                    st.markdown(f"""
                    <div class="app-card">
                        <div class="menu-day">{item['day']}</div>
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
                    """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ Unable to load food menu. Status: {r.status_code}")
    except Exception as e:
        st.error(f"🔌 Connectivity issue: {e}")

# ---------------- TAB: PAYMENTS ----------------
with tab_pay:
    st.markdown('<div class="section-header">Make a Payment</div>', unsafe_allow_html=True)
    
    # QR Code Display
    import os
    if os.path.exists("streamlit_app/assets/qrcode.png"):
         _, col_mid, _ = st.columns([1, 1, 1])
         with col_mid:
             st.image("streamlit_app/assets/qrcode.png", caption="Scan to Pay", width=200)
             st.markdown("""
             <div style="background: rgba(0,0,0,0.05); padding: 8px; border-radius: 8px; text-align: center; margin-top: 5px; margin-bottom: 20px;">
                 <div style="display: flex; justify-content: center; margin-bottom: 4px;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/PhonePe_Logo.svg/1280px-PhonePe_Logo.svg.png" width="100">
                 </div>
                 <div style="color: #1d4ed8; font-size: 16px; font-weight: 700; letter-spacing: 0.5px;">+91 6300243051</div>
             </div>
             """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No QR Code uploaded by Admin yet. Please ask for bank details.")

    with st.form("pay_form", clear_on_submit=True):
        amount = st.number_input("Amount (₹)", min_value=1, step=100, value=5000)
        txn_id = st.text_input("Transaction ID / UTR Number", placeholder="e.g. UPI12345678")
        
        if st.form_submit_button("✅ Submit Payment", use_container_width=True):
            if not txn_id:
                st.warning("Please enter a Transaction ID")
            else:
                try:
                    pr = requests.post(f"{BASE_URL}/payments", json={"amount": amount, "transaction_id": txn_id}, headers=headers)
                    if pr.status_code == 200:
                        st.success("Payment submitted! Admin will approve shortly.")
                        st.rerun()
                    else:
                        st.error("Failed to submit payment")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

    st.markdown("---")
    col_p1, col_p2 = st.columns([4,1])
    with col_p1:
        st.markdown('<div class="section-header">Payment History</div>', unsafe_allow_html=True)
    with col_p2:
        if st.button("🔄 Refresh", key="refresh_pay"): 
            st.rerun()
    
    try:
        my_pay_r = requests.get(f"{BASE_URL}/payments/my", headers=headers)
        if my_pay_r.status_code == 200:
            my_payments = my_pay_r.json()
            if not my_payments:
                st.info("No payment history.")
            else:
                for p in my_payments:
                    status_color = "chip-green" if p['status'] == "Approved" else "chip-yellow"
                    st.markdown(f"""
                    <div class="app-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-size:18px; font-weight:700;">₹ {p['amount']}</span>
                                <div style="font-size:12px;">ID: {p['transaction_id']}</div>
                            </div>
                            <span class="status-badge {status_color}">{p['status']}</span>
                        </div>
                        <div style="margin-top:8px; font-size:12px; text-align:right;">
                            {p['created_at'].split('T')[0]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("Could not load history")

# ---------------- TAB 2: COMPLAINTS ----------------
with tab2:
    st.markdown('<div class="section-header">Raise a New Ticket</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="app-card" style="padding: 16px;">', unsafe_allow_html=True)
        with st.form("complaint_form", clear_on_submit=True):
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                category = st.selectbox(
                    "Issue Category",
                    ["Water Supply", "Electricity/Power", "Food Quality", "Housekeeping", "Wi-Fi", "Other"]
                )
            with col_c2:
                priority = st.selectbox("Priority", ["Normal", "High", "Critical"]) # Just for UI, backend treats same for now

            description = st.text_area("Description", placeholder="Describe the issue in detail...")
            
            submit_col1, submit_col2 = st.columns([1,3])
            with submit_col1:
                submit = st.form_submit_button("� Submit Ticket", use_container_width=True)
                
            if submit:
                if len(description) < 5:
                    st.warning("Please provide a more detailed description.")
                else:
                    try:
                        res = requests.post(
                            f"{BASE_URL}/complaints",
                            json={
                                "category": category,
                                "description": f"[{priority}] {description}"
                            },
                            headers=headers
                        )

                        if res.status_code == 200:
                            st.toast("✅ Complaint submitted successfully!", icon="🎉")
                            st.rerun()
                        else:
                            st.error("❌ Failed to submit complaint.")
                    except:
                        st.error("🔌 Server not reachable.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    col_h1, col_h2 = st.columns([4,1])
    with col_h1:
        st.markdown('<div class="section-header">My Ticket History</div>', unsafe_allow_html=True)
    with col_h2:
        if st.button("🔄 Refresh", key="refresh_complaints"):
            st.rerun()

    try:
        r = requests.get(f"{BASE_URL}/complaints/my", headers=headers)
        if r.status_code == 200:
            complaints = r.json()
            if not complaints:
                st.info("👍 You have no active complaints.")
            else:
                for c in complaints:
                    status_class = "status-resolved" if c["status"] == "Resolved" else "status-pending"
                    icon = "✅" if c["status"] == "Resolved" else "⏳"
                    
                    st.markdown(f"""
                    <div class="app-card">
                        <div style="display:flex; justify-content:space-between; align-items:start;">
                            <div>
                                <span style="font-weight:700; font-size:16px;">{c['category']}</span>
                                <div style="margin-top:4px; font-size:14px;">{c['description']}</div>
                            </div>
                            <span class="status-badge {status_class}">
                                {icon} {c['status']}
                            </span>
                        </div>
                        <div style="margin-top:12px; font-size:12px; text-align:right;">
                            ID: #{c['id']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("⚠️ Unable to fetch history.")
    except:
        st.error("🔌 Server error.")

# ---------------- BOTTOM NAV ----------------
resident_nav(current="home")


