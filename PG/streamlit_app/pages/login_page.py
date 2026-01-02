import streamlit as st
import base64
from services.auth import login_user
from utils.theme import apply_theme

st.set_page_config(
    page_title="Smart PG Living",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- IDLE THEME INIT ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"
theme = apply_theme()

# ---------------- BACKGROUND SETUP ----------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    img_base64 = get_base64_of_bin_file("streamlit_app/assets/logo.JPG")
    # Position strictly in center with FIXED size to guarantee text alignment
    bg_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: 600px auto; /* Fixed width to ensure fit matches margins */
        background-position: center 60px; /* Fixed top offset */
        background-repeat: no-repeat;
        background-color: #ffffff;
    }}
    
    /* Hide Default Headers */
    header {{visibility: hidden;}}
    
    /* Input Field Styling */
    div[data-testid="stTextInput"] {{
        margin-bottom: -15px !important;
    }}
    div[data-testid="stTextInput"] input {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid #ea580c !important; 
        border-radius: 4px !important;
        color: #374151 !important;
        height: 35px;
        font-size: 14px;
        box-shadow: none !important;
    }}
    div[data-testid="stTextInput"] label {{
        font-size: 13px;
        color: #374151;
        font-weight: 700;
        margin-bottom: 2px;
    }}
    
    /* Button Styling */
    .stButton button {{
        background-color: #ea580c !important; /* Orange */
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600;
        height: 38px;
        letter-spacing: 0.5px;
    }}
    .stButton button:hover {{
        background-color: #c2410c !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(234, 88, 12, 0.3);
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)
except:
    pass 

# ---------------- GLOBAL STYLES ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
[data-testid="stSidebarNav"] {display:none;}

.inside-container {
    max-width: 380px;
    margin: 0 auto;
    margin-top: 180px; /* Aligns with roof area */
    padding: 0px 20px; /* Reduced vertical padding */
    text-align: center;
}
.header-text {
    text-align: center;
    color: #c2410c; /* Rust Orange */
    font-weight: 800;
    font-size: 32px;
    margin-bottom: 0px; /* Remove bottom margin */
    text-transform: uppercase;
    text-shadow: 2px 2px 0px #ffffff;
}
.sub-text {
    text-align: center;
    color: #4b5563;
    font-weight: 600;
    font-size: 13px;
    margin-bottom: 10px; /* Reduced from 24px */
}
</style>
""", unsafe_allow_html=True)


# ---------------- CONTENT ----------------
# Header Container (Roof)
st.markdown('<div class="inside-container">', unsafe_allow_html=True)
st.markdown('<div class="header-text">LIVINPG</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Welcome back! Please login.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Form Container (Door)
col1, col_door, col2 = st.columns([1, 1.4, 1])

with col_door:
    email = st.text_input("Email", placeholder="resident@example.com")
    # Removed spacer
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    st.write("")
    
    if st.button("-> Login", use_container_width=True):
        if not email or not password:
            st.warning("⚠️ Enter credentials")
        else:
            success = login_user(email, password)
            if success:
                st.switch_page("app.py")
            else:
                st.error("❌ Invalid credentials")
    
    # Removed divider <---
    st.write("") # Tiny gap instead of large divider
    
    if st.button("Create New Account", use_container_width=True):
        st.switch_page("pages/register.py")
    
