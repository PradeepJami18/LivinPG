import streamlit as st

def apply_theme():
    """
    Applies the selected theme (Light/Dark) via CSS injection.
    Returns the current theme ('light' or 'dark').
    """
    # Initialize Session State for Theme
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # Define CSS Constants based on current state
    if st.session_state.theme == "light":
        # LIGHT THEME
        bg_color = "#ffffff"
        # Subtle orange/warm gradient for light mode
        bg_gradient = "linear-gradient(135deg, #ffffff 0%, #fff7ed 100%)" 
        text_color = "#374151" # Dark Grey
        card_bg = "#ffffff"
        card_border = "#fed7aa" # Light Orange Border
        card_shadow = "0 4px 6px -1px rgba(249, 115, 22, 0.1)" # Orange shadow hint
        sub_text = "#6b7280"
        input_bg = "#ffffff"
        input_border = "#fdba74"
        header_color = "#c2410c" # Darker Orange/Rust for headers
    else:
        # DARK THEME
        bg_color = "#111827" # deeply dark grey
        bg_gradient = "radial-gradient(circle at 50% 0%, #374151, #111827 60%)"
        text_color = "#f9fafb"
        card_bg = "rgba(17, 24, 39, 0.8)"
        card_border = "rgba(251, 146, 60, 0.2)" # Orange accent 
        card_shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.4)"
        sub_text = "#9ca3af"
        input_bg = "rgba(31, 41, 55, 0.9)"
        input_border = "rgba(251, 146, 60, 0.3)"
        header_color = "#fb923c" # Lighter orange for dark mode contrast

    # Inject CSS
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    body {{
        background-color: {bg_color};
        font-family: 'Inter', sans-serif;
        color: {text_color} !important;
    }}
    
    .stApp {{
        background: {bg_gradient};
        background-size: 100% 100vh;
        background-attachment: fixed;
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {header_color} !important;
    }}
    
    /* Global Text */
    p, div, label, span {{
        color: {text_color};
    }}

    /* Card Styling */
    .app-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        padding: 24px;
        border-radius: 20px;
        margin-bottom: 20px;
        color: {text_color};
        box-shadow: {card_shadow};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }}
    
    /* Input Fields */
    div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {input_border} !important;
    }}
    
    /* Tabs */
    button[data-baseweb="tab"] {{
        color: {text_color} !important;
    }}
    button[data-baseweb="tab"] div p {{
        color: {text_color} !important;
    }}

    /* COMPONENT STYLES */
    .title {{
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(to right, #f97316, #ea580c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }}
    .subtitle {{
        font-size: 15px;
        color: {sub_text};
        font-weight: 500;
    }}
    .section-header {{
        font-size: 18px;
        font-weight: 700;
        color: {header_color};
        margin-top: 32px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    /* Food Menu */
    .menu-day {{
        background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
    }}
    .meal-row {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        padding-bottom: 8px;
        border-bottom: 1px solid {card_border};
    }}
    .meal-row:last-child {{
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }}
    .meal-label {{
        color: {sub_text};
        font-weight: 500;
    }}
    .meal-value {{
        color: {text_color};
        font-weight: 600;
        text-align: right;
    }}

    /* Badges & Chips */
    .status-badge {{
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }}
    /* Dynamic Badge Colors (using rgba for adaptability) */
    .status-pending, .chip-yellow {{
        background: rgba(234, 179, 8, 0.15);
        color: #eab308;
        border: 1px solid rgba(234, 179, 8, 0.3);
    }}
    .status-resolved, .chip-green {{
        background: rgba(34, 197, 94, 0.15);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }}
    .chip-blue {{
        background: rgba(59, 130, 246, 0.15);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }}

    /* Stats (Admin) */
    .stat-label {{
        color: {sub_text};
        font-size: 13px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .stat-value {{
        color: {text_color};
        font-size: 28px;
        font-weight: 800;
        margin-top: 4px;
    }}
    .stat-sub {{
        color: {sub_text};
        font-size: 12px;
        margin-top: 4px;
    }}
    
    /* Global Button Styling to Fix Visibility */
    .stButton button {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {card_border} !important;
        transition: all 0.2s ease;
    }}
    .stButton button:hover {{
        border-color: #f97316 !important;
        color: #f97316 !important;
        opacity: 0.9;
    }}
    
    /* Toggle Switch Visibility Fix */
    div[data-testid="stToggle"] label[data-testid="stWidgetLabel"] {{
        color: {text_color};
        font-weight: 600;
    }}
    div[data-testid="stToggle"] span {{
        color: {text_color};
    }}
    /* The Toggle Track */
    div[data-testid="stToggle"] div[role="switch"] {{
        background-color: #cbd5e1 !important; /* Visible Grey */
        border: 1px solid {card_border};
    }}
    div[data-testid="stToggle"] div[role="switch"][aria-checked="true"] {{
        background-color: #f97316 !important; /* Orange when active */
    }}
    
    </style>
    """, unsafe_allow_html=True)

    return st.session_state.theme
