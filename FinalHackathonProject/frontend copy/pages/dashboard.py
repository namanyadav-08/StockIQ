import streamlit as st
import random
from utils.session import set_page
from data.constants import STOCKS, SECTORS
import yfinance as yf
from datetime import datetime

def show_dashboard():
    """Display the dashboard with a grid of animated stock cards"""
    # Header with welcome message
    if st.session_state.get("user_email"):
        st.markdown(f"""
            <h2 style='color:#2563eb; margin-bottom:0.5rem;'>Welcome, {st.session_state["user_email"].split('@')[0]}!</h2>
            <p style='color:#0057b8; margin-bottom:2rem; font-size:1.1rem;'>Here's your personalized stock dashboard</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <h2 style='color:#2563eb; margin-bottom:2rem;'>Stock Dashboard</h2>
        """, unsafe_allow_html=True)
    
    # User profile card - Show the prompt created from onboarding
    if "user_prompt" in st.session_state and st.session_state["user_prompt"]:
        with st.expander("Your Trading Profile", expanded=False):
            st.markdown("<div style='background:#f8fafc; padding:1rem; border-radius:8px; font-family:monospace; white-space:pre-wrap;'>", unsafe_allow_html=True)
            st.write(st.session_state["user_prompt"])
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:0.8rem; color:#64748b; margin-top:0.5rem;'>This profile is used to personalize your stock predictions.</div>", unsafe_allow_html=True)

    # --- Top Picks for You Section (moved up) ---
    onboard_answers = st.session_state.get("onboard_answers", [])
    if not onboard_answers or len(onboard_answers) < 6:
        # Onboarding skipped or not enough answers: show message only
        st.markdown("<h3 style='color:#2563eb; margin-bottom:1rem;'>Top Picks for You</h3>", unsafe_allow_html=True)
        st.markdown("<div style='color:#888; font-size:1.1rem; margin-bottom:2em;'>Top Picks: Not available</div>", unsafe_allow_html=True)
    else:
        top_picks = []
        # Get favorite sectors (Q5, index 4), favorite stocks (Q6, index 5), and risk profile (Q8, index 7)
        favorite_sectors = onboard_answers[4] if len(onboard_answers) > 4 else []
        favorite_stocks = onboard_answers[5] if len(onboard_answers) > 5 else None
        user_risk = onboard_answers[7] if len(onboard_answers) > 7 else None
        risk_map = {
            "Risk-averse": "Low",
            "Neutral": "Medium",
            "Risk-seeking": "High"
        }
        user_risk_level = risk_map.get(user_risk, None) if isinstance(user_risk, str) else None
        if favorite_stocks is None:
            favorite_stocks = []
        if isinstance(favorite_stocks, str):
            favorite_stocks = [s.strip().upper() for s in favorite_stocks.split(",") if s.strip()]
        # 1. Add favorite stocks if present in STOCKS
        for stock in STOCKS:
            if stock["symbol"] in favorite_stocks and stock not in top_picks:
                top_picks.append(stock)
        # 2. Add stocks from favorite sectors (avoid duplicates)
        for stock in STOCKS:
            if stock["sector"] in favorite_sectors and stock not in top_picks:
                top_picks.append(stock)
        # 3. Add stocks matching user risk profile (avoid duplicates)
        for stock in STOCKS:
            if user_risk_level and stock["risk"] == user_risk_level and stock not in top_picks:
                top_picks.append(stock)
        # Limit to 3 picks
        top_picks = top_picks[:3]
        if top_picks:
            st.markdown("<h3 style='color:#2563eb; margin-bottom:1rem;'>Top Picks for You</h3>", unsafe_allow_html=True)
            pick_cols = st.columns(len(top_picks))
            for idx, stock in enumerate(top_picks):
                with pick_cols[idx]:
                    # Risk badge color
                    risk_color = {
                        'Low': '#22c55e',      # green
                        'Medium': '#f59e42',   # orange
                        'High': '#ef4444'      # red
                    }.get(stock.get('risk', 'Medium'), '#f59e42')
                    st.markdown(f"""
                        <div class='stock-card' style='background:#e0f2fe; border:2px solid #2563eb; padding:2em 1em; border-radius:1em; text-align:center; margin-bottom:1.5em; min-height:180px; display:flex; flex-direction:column; align-items:center; justify-content:center;'>
                            <span style='font-size:3rem;'>{stock['logo']}</span>
                            <div style='font-size:1.3rem; font-weight:700; color:#222; margin-bottom:0.2em;'>{stock['name']}</div>
                            <div style='font-size:1.1rem; color:#2563eb; margin-bottom:0.5em;'>{stock['symbol']}</div>
                            <span style='display:inline-block; background:{risk_color}; color:#fff; font-size:0.78rem; font-weight:600; border-radius:1em; padding:0.13em 0.7em; margin:0.08em 0.15em 0.08em 0;'>Risk: {stock['risk']}</span>
                            <span style='display:inline-block; background:#2563eb; color:#fff; font-size:0.78rem; font-weight:600; border-radius:1em; padding:0.13em 0.7em; margin:0.08em 0 0.08em 0.15em;'>Sector: {stock['sector']}</span>
                        </div>
                    """, unsafe_allow_html=True)

    # Filters
    st.markdown("<h3 style='color:#2563eb; margin-bottom:1rem;'>Stocks</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_sectors = st.multiselect(
            "Filter by Sector",
            options=SECTORS,
            default=[]
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=["Symbol (A-Z)", "Price (High to Low)", "Price (Low to High)", "% Change"]
        )
    
    # Stock cards grid
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    
    # Create a 3-column grid
    cols = st.columns(3)
    
    for idx, stock in enumerate(STOCKS):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class='stock-card' style='cursor:pointer; background:#f5f6fa; border:1px solid #e5e7eb; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:3em 1.5em; min-height:240px; box-shadow:0 4px 24px rgba(30,60,114,0.07);'>
                    <span class='stock-logo' style='font-size:3.5rem; color:#2563eb; margin-bottom:1.5rem;'>{stock['logo']}</span>
                    <div style='font-size:1.5rem; font-weight:800; color:#222; text-align:center;'>{stock['name']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"View {stock['symbol']}", key=f"btn_{stock['symbol']}"):
                st.session_state["selected_stock"] = stock['symbol']
                set_page("stock_detail")
    
    # No stocks found message
    if not STOCKS:
        st.markdown("""
            <div style='text-align:center; padding:3rem; color:#666;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>🔍</div>
                <div style='font-size:1.2rem; font-weight:600;'>No stocks found</div>
                <div>Try adjusting your filters</div>
            </div>
        """, unsafe_allow_html=True)