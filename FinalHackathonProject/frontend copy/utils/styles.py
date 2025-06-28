import streamlit as st

# Color constants - Modern color palette
PRIMARY_COLOR = "#3b82f6"  # Bright blue
SECONDARY_COLOR = "#6366f1"  # Indigo
ACCENT_COLOR = "#8b5cf6"  # Purple
BG_COLOR = "#f8fafc"  # Light background
COLOR_GRADIENT = "linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%)"  # Blue to purple
BG_GRADIENT = "linear-gradient(135deg, #f1f5f9 0%, #f8fafc 100%)"  # Subtle light gradient

def apply_styles():
    """Apply custom CSS styling to the app"""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        html, body, .stApp {{
            background-image: url('https://static.vecteezy.com/system/resources/thumbnails/019/576/577/small/abstract-white-wavy-ripple-pattern-background-curve-line-texture-for-modern-graphic-design-element-website-banner-and-poster-or-business-card-decoration-vector.jpg') !important;
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            background-position: center center !important;
            background-color: transparent !important;
            color: #222 !important;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .main, .block-container {{
            background: transparent !important;
        }}
        
        /* Force dark text for all radio, select, tab, and button options */
        .stRadio label, .stRadio div[role="radio"], .stSelectbox div, .stSelectbox label, .stTabs [data-baseweb="tab"], .stTabs [aria-selected="true"], .stButton>button, .stCheckbox label {{
            color: #1e293b !important;
            font-weight: 600 !important;
        }}
        
        /* Fix radio/checkbox selected dot color */
        .stRadio div[role="radio"][aria-checked="true"] > div:first-child {{
            border-color: #2563eb !important;
            background: #2563eb !important;
        }}
        
        /* Input and select border and placeholder contrast */
        .stTextInput>div>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div {{
            border-radius: 8px !important;
            background: #f7f9fa !important;
            border: 1.5px solid #2563eb !important;
            color: #1e293b !important;
        }}
        .stTextInput>div>div>input::placeholder, .stTextArea>div>textarea::placeholder {{
            color: #64748b !important;
            opacity: 1 !important;
        }}
        
        /* Table header contrast */
        th, .stDataFrame th, .stTable th {{
            color: #1e293b !important;
            background: #e0e7ef !important;
            font-weight: 700 !important;
        }}
        
        /* Graph selector (tab) background and text */
        .stTabs [data-baseweb="tab-list"] {{
            background: #f7f9fa !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }}
        .stTabs [aria-selected="true"] {{
            background: #dbeafe !important;
            color: #1e293b !important;
        }}
        
        /* Button text always dark unless on dark bg */
        .stButton>button {{
            color: #1e293b !important;
            background: #e0e7ef !important;
            border-radius: 0.5rem !important;
            font-weight: bold !important;
            transition: 0.2s;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
            padding: 0.6rem 1.2rem;
        }}
        .stButton>button[style*="background: #2563eb"], .stButton>button[style*="background:#2563eb"] {{
            color: #fff !important;
        }}
        
        /* Buttons */
        .stButton>button {{background: #2563eb !important; color: #fff !important; border-radius: 0.5rem !important; font-weight: bold; transition: 0.2s; box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2); padding: 0.6rem 1.2rem;}}
        .stButton>button:hover {{filter: brightness(1.05); box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); transform: translateY(-1px);}}
        
        /* Form elements */
        .stTextInput>div>div>input, .stTextArea>div>textarea {{border-radius: 10px; background: white; border: 1px solid #e2e8f0; transition: all 0.2s; font-size: 0.95rem;}}
        .stTextInput>div>div>input:focus, .stTextArea>div>textarea:focus {{box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2); border-color: #6366f1;}}
        .stRadio>div, .stCheckbox>div {{background: white; border-radius: 10px; padding: 0.8rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}}
        .stRadio>div>label, .stCheckbox>div>label {{font-size: 1rem; font-weight: 500;}}
        .stSelectbox>div>div>div {{border-radius: 10px; border: 1px solid #e2e8f0;}}
        
        /* Cards */
        .card {{background: #f5f6fa; border-radius: 1.2rem; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 4px 24px rgba(30,60,114,0.07); border: 1px solid #e5e7eb;}}
        .card:hover {{box-shadow: 0 4px 12px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.03); transform: translateY(-2px);}}
        
        /* Stock Cards */
        .stock-card {{border-radius: 14px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.03); padding: 1.2rem; margin-bottom: 1rem; transition: all 0.2s; display: flex; align-items: center; gap: 1rem; border: 1px solid #f1f5f9;}}
        .stock-card:hover {{box-shadow: 0 4px 12px rgba(0,0,0,0.05); transform: translateY(-2px); border-left: 3px solid #6366f1;}}
        .stock-logo {{font-size: 2.2rem; background: #f8fafc; border-radius: 12px; width: 3rem; height: 3rem; display: flex; align-items: center; justify-content: center;}}
        .stock-logo-large {{font-size:3rem; background:#2563eb; color:#1e293b; width:4rem; height:4rem; display:flex; align-items:center; justify-content:center; border-radius:0.75rem; box-shadow:0 10px 15px -3px rgba(37,99,235,0.13);}}
        .stock-symbol {{font-size:1.5rem; font-weight:700; color:#3b82f6;}}
        .stock-name {{font-size:0.9rem; color:#555; margin-bottom:0.5rem;}}
        .stock-price {{font-size:1.2rem; font-weight:700;}}
        .stock-change {{font-size:0.9rem; margin-left:0.5rem;}}
        .stock-chart {{height:50px; margin-top:1rem;}}
        
        /* Metric Badges */
        .metric-badge {{background:#f1f5f9; padding:0.75rem 1rem; border-radius:0.5rem; min-width:5rem; text-align:center;}}
        .metric-label {{font-size:0.75rem; color:#888; margin-bottom:0.25rem;}}
        .metric-value {{font-size:1rem; font-weight:600; color:#0f172a;}}
        
        /* Progress bar */
        .progress-bar-bg {{background: #f1f5f9; border-radius: 10px; height: 8px; width: 100%; margin-bottom: 1rem;}}
        .progress-bar-fill {{background: {COLOR_GRADIENT}; border-radius: 10px; height: 8px; transition: width 0.3s ease-in-out;}}
        
        /* Chatbox */
        .chatbox {{position: fixed; bottom: 24px; right: 24px; width: 360px; background: white; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); z-index: 100; padding: 1.2rem; transition: all 0.3s; border: 1px solid #f1f5f9;}}
        .chatbox:hover {{box-shadow: 0 6px 20px rgba(0,0,0,0.1);}}
        .chat-messages {{max-height: 240px; overflow-y: auto; margin-bottom: 0.8rem; scrollbar-width: thin; scrollbar-color: #e2e8f0 transparent;}}
        .chat-messages::-webkit-scrollbar {{width: 4px;}}
        .chat-messages::-webkit-scrollbar-track {{background: transparent;}}
        .chat-messages::-webkit-scrollbar-thumb {{background-color: #e2e8f0; border-radius: 4px;}}
        .chat-input-row {{display: flex; gap: 0.5rem;}}
        
        /* Badges */
        .badge {{display: inline-block; background: #2563eb; color: #1e293b; border-radius: 0.7rem; padding: 0.4em 1em; margin: 0.2em; font-weight: bold; font-size: 1.1em;}}
        
        /* Hero section */
        .hero {{background: {COLOR_GRADIENT}; border-radius: 20px; padding: 3rem 2rem; color: #1e293b; text-align: center; margin-bottom: 2rem; box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2); position: relative; overflow: hidden;}}
        .hero::before {{content: ""; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%); animation: pulse 15s infinite;}}
        @keyframes pulse {{0% {{transform: scale(1);}} 50% {{transform: scale(1.05);}} 100% {{transform: scale(1);}}}}
        .hero-logo {{font-size: 4rem; margin-bottom: 1rem;}}
        .hero-title {{font-size: 2.8rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.5rem;}}
        .hero-desc {{font-size: 1.2rem; margin-bottom: 1.5rem; opacity: 0.9;}}
        
        /* Sidebar */
        .sidebar-logo {{font-size: 2rem; font-weight: 700; color: #2563eb; margin-bottom: 1rem; letter-spacing: -0.02em; display: flex; align-items: center; gap: 0.5rem;}}
        .sidebar-user {{margin-top: 2rem; font-size: 1rem; color: #333; background: #f8fafc; padding: 0.75rem; border-radius: 10px; border-left: 3px solid #3b82f6;}}
        .social-btn {{background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.5rem; padding: 0.5rem 1rem; font-size: 0.9rem; cursor: pointer; transition: all 0.2s;}}
        .social-btn:hover {{background: #f1f5f9; border-color: #cbd5e1; transform: translateY(-2px);}}
        
        /* Animations */
        @keyframes fadeIn {{from {{opacity: 0; transform: translateY(8px);}} to {{opacity: 1; transform: translateY(0);}}}}
        @keyframes slideIn {{from {{opacity: 0; transform: translateX(-10px);}} to {{opacity: 1; transform: translateX(0);}}}}
        .stApp > header {{animation: fadeIn 0.4s ease-out;}}
        .main .block-container {{animation: fadeIn 0.4s ease-out;}}
        .sidebar .sidebar-content {{animation: slideIn 0.4s ease-out;}}
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {{background-color: white; border-radius: 10px; padding: 0.3rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}}
        .stTabs [data-baseweb="tab"] {{border-radius: 8px; padding: 0.5rem 1rem; margin: 0.2rem;}}
        .stTabs [aria-selected="true"] {{background: {COLOR_GRADIENT}; color: #1e293b !important;}}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .hero {{padding: 2rem 1rem;}}
            .hero-title {{font-size: 2.2rem;}}
            .hero-desc {{font-size: 1rem;}}
            .chatbox {{width: 90%; right: 5%; left: 5%;}}
        }}
        </style>
    """, unsafe_allow_html=True)