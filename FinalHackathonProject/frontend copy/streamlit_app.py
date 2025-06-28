import streamlit as st
import plotly.graph_objs as go
import random
import datetime

# --- Constants & Mock Data ---
STOCKS = [
    {"symbol": "AAPL", "name": "Apple Inc.", "logo": "🍏"},
    {"symbol": "TSLA", "name": "Tesla, Inc.", "logo": "🚗"},
    {"symbol": "MSFT", "name": "Microsoft Corp.", "logo": "💻"},
    {"symbol": "AMZN", "name": "Amazon.com, Inc.", "logo": "📦"},
    {"symbol": "META", "name": "Meta Platforms, Inc.", "logo": "📱"},
    {"symbol": "GOOG", "name": "Alphabet Inc.", "logo": "🔍"},
    {"symbol": "NVDA", "name": "NVIDIA Corporation", "logo": "🎮"},
]

SECTORS = [
    "Technology", "Healthcare", "Finance", "Energy", "Consumer Discretionary", "Industrials", "Utilities"
]

ONBOARDING_QUESTIONS = [
    ("Are you a beginner, intermediate, or expert trader?", ["Beginner", "Intermediate", "Expert"]),
    ("How much capital do you usually invest?", None),
    ("What's your average holding period?", None),
    ("Are you interested in short-term or long-term analysis?", ["Short-term", "Long-term", "Both"]),
    ("Which sectors are you most interested in?", SECTORS),
    ("List your 3 favorite stocks", None),
    ("How often do you trade per week?", None),
    ("Are you risk-averse, neutral, or risk-seeking?", ["Risk-averse", "Neutral", "Risk-seeking"]),
    ("Do you use technical indicators? (Yes/No + which ones)", None),
    ("What kind of predictions would you like (price, trend, sentiment, etc.)?", None),
]

NEWS_HEADLINES = [
    "Stock surges after strong earnings report.",
    "Analysts predict continued growth in the sector.",
    "Company announces new product line.",
    "Market volatility expected to increase.",
    "Regulatory changes impact industry outlook."
]

COLOR_GRADIENT = "linear-gradient(90deg, #1e3c72 0%, #2a5298 100%)"
BG_GRADIENT = "linear-gradient(135deg, #e0e7ff 0%, #f7f9fa 100%)"

# --- Utility Functions ---
def set_page(page):
    st.session_state["page"] = page

def init_session():
    if "page" not in st.session_state:
        st.session_state["page"] = "welcome"
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "Login"
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""
    if "user_prompt" not in st.session_state:
        st.session_state["user_prompt"] = ""
    if "onboard_answers" not in st.session_state:
        st.session_state["onboard_answers"] = [None]*len(ONBOARDING_QUESTIONS)
    if "onboard_qn" not in st.session_state:
        st.session_state["onboard_qn"] = 0
    if "selected_stock" not in st.session_state:
        st.session_state["selected_stock"] = None
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

def style():
    st.markdown(f"""
        <style>
        body {{background: {BG_GRADIENT};}}
        .main {{background: transparent !important;}}
        .stApp {{background: {BG_GRADIENT};}}
        .stButton>button {{background: {COLOR_GRADIENT}; color: white; border-radius: 10px; font-weight: 600; transition: 0.2s; box-shadow: 0 2px 8px #b6c2d9;}}
        .stButton>button:hover {{filter: brightness(1.1); box-shadow: 0 4px 16px #b6c2d9;}}
        .stTextInput>div>div>input, .stTextArea>div>textarea {{border-radius: 8px; background: #f7f9fa;}}
        .stRadio>div>label, .stCheckbox>div>label {{font-size: 1.1rem;}}
        .card {{border-radius: 18px; background: #fff; box-shadow: 0 2px 16px #e3e8ee; padding: 2.2rem 2rem 2rem 2rem; margin-bottom: 2rem; transition: box-shadow 0.2s;}}
        .card:hover {{box-shadow: 0 6px 24px #b6c2d9;}}
        .stock-card {{border-radius: 16px; background: #fff; box-shadow: 0 2px 12px #e3e8ee; padding: 1.5rem; margin-bottom: 1.5rem; transition: box-shadow 0.2s; display: flex; align-items: center; gap: 1.2rem;}}
        .stock-card:hover {{box-shadow: 0 6px 24px #b6c2d9;}}
        .stock-logo {{font-size: 2.5rem; margin-right: 1rem;}}
        .progress-bar-bg {{background: #e0e7ff; border-radius: 8px; height: 12px; width: 100%; margin-bottom: 1.2rem;}}
        .progress-bar-fill {{background: {COLOR_GRADIENT}; border-radius: 8px; height: 12px;}}
        .chatbox {{position: fixed; bottom: 32px; right: 32px; width: 370px; background: rgba(255,255,255,0.85); border-radius: 18px; box-shadow: 0 2px 24px #b6c2d9; z-index: 100; padding: 1.2rem; backdrop-filter: blur(8px);}}
        .chat-messages {{max-height: 220px; overflow-y: auto; margin-bottom: 0.5rem;}}
        .chat-input-row {{display: flex; gap: 0.5rem;}}
        .badge {{display: inline-block; background: #e0e7ff; color: #1e3c72; border-radius: 8px; padding: 0.2rem 0.7rem; font-size: 0.95rem; margin-right: 0.5rem; font-weight: 600;}}
        .hero {{background: {COLOR_GRADIENT}; border-radius: 24px; padding: 3.5rem 2rem 2.5rem 2rem; color: white; text-align: center; margin-bottom: 2.5rem; box-shadow: 0 4px 32px #b6c2d9;}}
        .hero-logo {{font-size: 4.5rem; margin-bottom: 1rem;}}
        .hero-title {{font-size: 3.2rem; font-weight: 900; letter-spacing: 2px; margin-bottom: 0.5rem;}}
        .hero-desc {{font-size: 1.4rem; margin-bottom: 2rem;}}
        .sidebar-logo {{font-size: 2.2rem; font-weight: 800; color: #1e3c72; margin-bottom: 1.5rem;}}
        .sidebar-user {{margin-top: 2rem; font-size: 1.1rem; color: #2a5298;}}
        </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
def sidebar():
    with st.sidebar:
        st.markdown("<div class='sidebar-logo'>🔮 Stock Oracle</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
        page = st.session_state["page"]
        navs = [
            ("Welcome", "welcome"),
            ("Login/Signup", "auth"),
            ("Onboarding", "onboard"),
            ("Dashboard", "dashboard"),
            ("Stock Detail", "stock_detail")
        ]
        for label, nav in navs:
            if page == nav:
                st.markdown(f"<div class='badge'>{label}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='margin-bottom:0.5rem; color:#2a5298;'>{label}</div>", unsafe_allow_html=True)
        if st.session_state.get("user_email"):
            st.markdown(f"<div class='sidebar-user'>👤 {st.session_state['user_email']}</div>", unsafe_allow_html=True)

# --- Page Functions ---
def welcome_page():
    st.markdown(f"""
        <div class='hero'>
            <div class='hero-logo'>🔮</div>
            <div class='hero-title'>Stock Oracle</div>
            <div class='hero-desc'>Your AI-powered Stock Market Predictor<br>Modern, Insightful, and Beautifully Simple</div>
            <div style='margin-top:2.5rem;'>
                <form action="#" method="post">
                    <button style="background:{COLOR_GRADIENT}; color:white; border:none; border-radius:12px; font-size:1.3rem; font-weight:700; padding:0.8rem 2.5rem; box-shadow:0 2px 12px #b6c2d9; cursor:pointer;">Get Started</button>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Get Started", key="welcome_btn"):
        set_page("auth")

# --- Auth Page ---
def auth_page():
    st.markdown("<div class='card' style='max-width:420px; margin:auto;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#1e3c72; text-align:center;'>Login / Signup</h2>", unsafe_allow_html=True)
    st.toggle("Switch to Signup" if st.session_state["auth_mode"] == "Login" else "Switch to Login",
              key="auth_toggle",
              value=(st.session_state["auth_mode"] == "Signup"),
              on_change=lambda: st.session_state.update({"auth_mode": "Signup" if st.session_state["auth_mode"] == "Login" else "Login"}))
    email = st.text_input("Email", key="auth_email")
    password = st.text_input("Password", type="password", key="auth_password")
    if st.button(st.session_state["auth_mode"], use_container_width=True):
        if email and password:
            st.session_state["user_email"] = email
            st.session_state["logged_in"] = True
            set_page("onboard")
        else:
            st.error("Please enter both email and password.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Onboarding Quiz ---
def onboarding_page():
    qn_idx = st.session_state["onboard_qn"]
    qn, opts = ONBOARDING_QUESTIONS[qn_idx]
    st.markdown("<div class='card' style='max-width:540px; margin:auto;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#1e3c72; text-align:center;'>Trader Onboarding</h3>", unsafe_allow_html=True)
    # Progress bar
    progress = int((qn_idx+1)/len(ONBOARDING_QUESTIONS)*100)
    st.markdown(f"""
        <div class='progress-bar-bg'>
            <div class='progress-bar-fill' style='width:{progress}%;'></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:1.2rem; font-weight:600; margin-bottom:1.2rem;'>{qn_idx+1}/10</div>", unsafe_allow_html=True)
    answer = None
    if qn_idx == 4:  # Sectors (checkboxes)
        answer = st.multiselect(qn, opts, key=f"onboard_{qn_idx}")
    elif qn_idx == 5:  # 3 favorite stocks
        answer = st.text_input(qn, key=f"onboard_{qn_idx}")
    elif qn_idx == 8:  # Technical indicators
        use_ind = st.radio("Do you use technical indicators?", ["Yes", "No"], key=f"onboard_{qn_idx}_yn")
        which = st.text_input("Which ones?", key=f"onboard_{qn_idx}_which") if use_ind == "Yes" else "None"
        answer = f"{use_ind} - {which}"
    elif opts:
        answer = st.radio(qn, opts, key=f"onboard_{qn_idx}")
    else:
        answer = st.text_input(qn, key=f"onboard_{qn_idx}")
    st.session_state["onboard_answers"][qn_idx] = answer
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Previous", disabled=qn_idx==0, use_container_width=True):
            st.session_state["onboard_qn"] -= 1
    with col2:
        if st.button("Next", disabled=answer in [None, ""], use_container_width=True):
            if qn_idx < len(ONBOARDING_QUESTIONS)-1:
                st.session_state["onboard_qn"] += 1
    if qn_idx == len(ONBOARDING_QUESTIONS)-1 and answer not in [None, ""]:
        if st.button("Continue to Stocks", key="onboard_continue", use_container_width=True):
            # Summarize user profile
            profile = []
            for i, (q, _) in enumerate(ONBOARDING_QUESTIONS):
                profile.append(f"Q{i+1}: {q} -> {st.session_state['onboard_answers'][i]}")
            st.session_state["user_prompt"] = "\n".join(profile)
            set_page("dashboard")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Stock Dashboard ---
def dashboard_page():
    st.markdown("<h2 style='color:#1e3c72; margin-bottom:1.5rem;'>Select a Stock</h2>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, stock in enumerate(STOCKS):
        with cols[idx%3]:
            st.markdown(f"""
                <div class='stock-card'>
                    <span class='stock-logo'>{stock['logo']}</span>
                    <div>
                        <div style='font-size:1.3rem; font-weight:700; color:#1e3c72;'>{stock['symbol']}</div>
                        <div style='color:#2a5298; font-size:1.05rem; margin-bottom:0.5rem;'>{stock['name']}</div>
                        <form action="#" method="post">
                            <button name="select_{stock['symbol']}" style="width:100%; background: {COLOR_GRADIENT}; color: white; border: none; border-radius: 8px; padding: 0.5rem 0; font-weight: 600;">View Details</button>
                        </form>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"View {stock['symbol']}", key=f"btn_{stock['symbol']}"):
                st.session_state["selected_stock"] = stock['symbol']
                set_page("stock_detail")

# --- Stock Detail Page ---
def stock_detail_page():
    symbol = st.session_state["selected_stock"]
    stock = next((s for s in STOCKS if s["symbol"] == symbol), None)
    if not stock:
        st.error("Stock not found.")
        set_page("dashboard")
        return
    st.markdown(f"<div class='card' style='max-width:900px; margin:auto; margin-bottom:2rem;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex; align-items:center; gap:1.2rem; margin-bottom:1.2rem;'><span class='stock-logo'>{stock['logo']}</span><span style='font-size:2rem; font-weight:800; color:#1e3c72;'>{stock['symbol']}</span><span class='badge'>{stock['name']}</span></div>", unsafe_allow_html=True)
    # --- Price & Change ---
    price = round(random.uniform(100, 500), 2)
    change = round(random.uniform(-3, 3), 2)
    st.markdown(f"<div style='font-size:2.2rem; font-weight:700; color:{'#2ecc71' if change>=0 else '#e74c3c'};'>${price} <span style='font-size:1.1rem;'>{'+' if change>=0 else ''}{change}%</span></div>", unsafe_allow_html=True)
    # --- Line Chart ---
    dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(6, -1, -1)]
    prices = [round(price + random.uniform(-5, 5), 2) for _ in range(7)]
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines+markers', name='Price'))
    line_fig.update_layout(title="Last 7 Days", xaxis_title="Date", yaxis_title="Price ($)", height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(line_fig, use_container_width=True)
    # --- Candlestick Chart (Optional) ---
    if st.checkbox("Show Candlestick Chart"):
        ohlc = [
            {
                "open": p + random.uniform(-2, 2),
                "high": p + random.uniform(0, 4),
                "low": p - random.uniform(0, 4),
                "close": p + random.uniform(-2, 2)
            } for p in prices
        ]
        candle_fig = go.Figure(data=[go.Candlestick(
            x=dates,
            open=[o['open'] for o in ohlc],
            high=[o['high'] for o in ohlc],
            low=[o['low'] for o in ohlc],
            close=[o['close'] for o in ohlc],
        )])
        candle_fig.update_layout(title="Candlestick Chart", height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(candle_fig, use_container_width=True)
    # --- News Headlines ---
    st.markdown("<h4 style='color:#2a5298; margin-top:1.5rem;'>Latest News</h4>", unsafe_allow_html=True)
    for i in range(3):
        st.markdown(f"- {random.choice(NEWS_HEADLINES)}")
    st.markdown("</div>", unsafe_allow_html=True)
    # --- Chatbot Section ---
    chatbot_ui()
    if st.button("Back to Dashboard", use_container_width=True):
        set_page("dashboard")

# --- Chatbot ---
def chatbot_ui():
    st.markdown("""
        <div class='chatbox'>
            <div style='font-weight:700; color:#1e3c72; margin-bottom:0.5rem; font-size:1.1rem;'>Ask DeepSeek about this stock</div>
    """, unsafe_allow_html=True)
    # Chat history
    chat_history = st.session_state.get("chat_history", [])
    chat_container = st.container()
    with chat_container:
        st.markdown("<div class='chat-messages'>", unsafe_allow_html=True)
        for msg, sender in chat_history:
            align = 'right' if sender == 'user' else 'left'
            color = '#2a5298' if sender == 'user' else '#e3e8ee'
            st.markdown(f"<div style='text-align:{align}; background:{color}; border-radius:8px; padding:0.4rem 0.8rem; margin-bottom:0.2rem; display:inline-block; max-width:80%;'>"
                        f"<b>{'You' if sender=='user' else 'DeepSeek'}:</b> {msg}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    # Input row
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("", placeholder="Type your question...", key="chat_input")
        submitted = st.form_submit_button("Send")
        if submitted and user_input:
            chat_history.append((user_input, "user"))
            # Simulate response
            chat_history.append((f"[Simulated response to: '{user_input}']", "bot"))
            st.session_state["chat_history"] = chat_history

# --- Main App ---
def main():
    style()
    init_session()
    sidebar()
    page = st.session_state["page"]
    if page == "welcome":
        welcome_page()
    elif page == "auth":
        auth_page()
    elif page == "onboard":
        onboarding_page()
    elif page == "dashboard":
        dashboard_page()
    elif page == "stock_detail":
        stock_detail_page()
    else:
        st.error("Unknown page.")

if __name__ == "__main__":
    main() 