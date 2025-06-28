##############################################
# Test Example: Predicting Google Stock Price
##############################################


import main

# IMPORT THE LIBRARY
import yfinance as yf
from datetime import datetime
import streamlit as st
import numpy as np
import plotly.graph_objs as go
import os
from main import main as predict_next
import streamlit.components.v1 as components

# CREATE TICKER INSTANCE FOR AMAZON
#Initialize API
GOOG = yf.Ticker("GOOG")
#Make the end date the current day
end_date = datetime.now().strftime('%Y-%m-%d')
#Pull Stock Price History
goog_hist = GOOG.history(start='2017-01-01',end=end_date)



goog_close = goog_hist['Close']
goog_value = goog_close.values
goog_value = np.array(goog_value).reshape(-1, 1)

print(goog_value[-50:])





models = {
    "google": "./models/Goog.keras",
    # "amazon": "./models/Amzn.keras",
    # "tesla": "./models/Tsla.keras",
    # "apple": "./models/Aapl.keras",
    # "nvidia": "./models/Nvda.keras"

}

output = main.main(model="./Goog.keras", array=goog_value[-50:])

print(output)

MODEL_PATHS = {
    'AAPL': './models/Aapl.keras',
    'GOOG': './models/Goog.keras',
    'AMZN': './models/Amzn.keras',
    'TSLA': './models/Tsla.keras',
    'NVDA': './models/Nvda.keras',
    'META': './models/Meta.keras',
}

STOCK_NAMES = {
    'AAPL': 'Apple Inc.',
    'GOOG': 'Alphabet Inc.',
    'AMZN': 'Amazon.com, Inc.',
    'TSLA': 'Tesla, Inc.',
    'NVDA': 'NVIDIA Corporation',
    'META': 'Meta Platforms, Inc.',
}

YF_TICKERS = {
    'AAPL': 'AAPL',
    'GOOG': 'GOOG',
    'AMZN': 'AMZN',
    'TSLA': 'TSLA',
    'NVDA': 'NVDA',
    'META': 'META'
}

st.set_page_config(page_title="StockIQ Model Demo", layout="centered")

# Custom dark theme CSS
st.markdown('''
    <style>
    body, .stApp { background-color: #181c20 !important; color: #f1f1f1 !important; }
    .main, .block-container { background-color: #181c20 !important; }
    .card { background: #23272e; border-radius: 1.2rem; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 4px 24px rgba(30,60,114,0.15); }
    .stButton>button { background: #3b82f6 !important; color: white !important; border-radius: 0.5rem !important; font-weight: bold; }
    .stCode, .stMarkdown, .stTable, .stDataFrame { background: #23272e !important; color: #f1f1f1 !important; border-radius: 0.7rem; }
    .badge { display: inline-block; background: #3b82f6; color: white; border-radius: 0.7rem; padding: 0.4em 1em; margin: 0.2em; font-weight: bold; font-size: 1.1em; }
    </style>
''', unsafe_allow_html=True)

# Sidebar navigation
sidebar_options = ["Welcome", "Dashboard"] + list(MODEL_PATHS.keys())
st.sidebar.title("StockIQ Dashboard 🚀")
page = st.sidebar.radio("Select Stock", sidebar_options)

if page == "Welcome":
    st.markdown("""
    <div class='card' style='text-align:center;'>
        <h1 style='color:#3b82f6; font-size:3em; margin-bottom:0.2em;'>Welcome to <span style='color:#f1f1f1;'>StockIQ</span></h1>
        <p style='font-size:1.3em; color:#b0b3b8;'>Your AI-powered stock prediction hackathon toolkit.<br>Pick a stock from the sidebar to get started!</p>
        <img src='https://img.freepik.com/free-vector/gradient-stock-market-concept_23-2149166910.jpg' width='60%' style='border-radius:1em; margin:2em auto;' />
        <div style='margin-top:2em;'></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:2em'></div>", unsafe_allow_html=True)
elif page == "Dashboard":
    st.markdown("""
    <div class='card'>
        <h1 style='color:#3b82f6; margin-bottom:0.5em;'>StockIQ Model Demo</h1>
        <p style='font-size:1.2em;'>Select a stock from the sidebar to see real ML-powered price predictions for the next 5 days!<br><br><b>Built for hackathons. Ready for the future.</b></p>
    </div>
    """, unsafe_allow_html=True)
    for symbol in MODEL_PATHS:
        st.markdown(f"<div class='card'><h2 style='color:#f1f1f1;'>{STOCK_NAMES[symbol]} <span style='color:#3b82f6;'>({symbol})</span></h2><a href='?page={symbol}' style='color:#3b82f6; font-weight:bold;'>Go to {symbol} page →</a></div>", unsafe_allow_html=True)
else:
    symbol = page
    st.markdown(f"<div class='card'><h1 style='color:#3b82f6;'>{STOCK_NAMES[symbol]} <span style='color:#f1f1f1;'>({symbol})</span> Prediction</h1>", unsafe_allow_html=True)
    st.markdown(f"**Model file:** <span style='color:#3b82f6;'>{MODEL_PATHS[symbol]}</span>", unsafe_allow_html=True)
    # Fetch last 50 real closing prices
    ticker = YF_TICKERS[symbol]
    data = yf.download(ticker, period="90d")
    if data is None or data.empty or 'Close' not in data:
        st.error("Failed to fetch data for this stock. Please try again later.")
        st.stop()
    closes = data['Close'].dropna().values[-50:]
    if len(closes) < 50:
        st.error("Not enough data to fetch 50 closing prices.")
        st.stop()
    st.markdown("#### Last 50 real closing prices:")
    st.code(", ".join([f"{float(x):.2f}" for x in closes]), language="text")
    price_array = np.array(closes).reshape(-1, 1)
    model_path = MODEL_PATHS[symbol]
    if not os.path.exists(model_path):
        st.error("Model file not found.")
        st.stop()
    # Predict next 5 days iteratively
    last50 = price_array.flatten().tolist()
    preds = []
    for i in range(5):
        arr = np.array(last50[-50:]).reshape(-1, 1)
        pred = predict_next(model=model_path, array=arr)
        if hasattr(pred, '__len__') and not isinstance(pred, str):
            pred = float(pred[0])
        else:
            pred = float(pred)
        preds.append(pred)
        last50.append(pred)
    # Display predicted prices as badges
    st.markdown("<h4 style='margin-top:2em;'>Predicted prices for next 5 days:</h4>", unsafe_allow_html=True)
    badges_html = " ".join([f"<span class='badge'>Day {i+1}: ${preds[i]:.2f}</span>" for i in range(5)])
    st.markdown(badges_html, unsafe_allow_html=True)
    # Show a beautiful graph: last 50 prices + next 5 predicted
    chart_dates = [f"Day {i+1}" for i in range(50)] + [f"Pred {i+1}" for i in range(5)]
    chart_prices = [float(x) for x in closes] + preds
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=chart_dates,
        y=chart_prices,
        mode='lines+markers',
        name='Price',
        line=dict(color='#3b82f6', width=4),
        marker=dict(color=['#3b82f6']*50 + ['#f59e42']*5, size=10, symbol=['circle']*50 + ['star']*5)
    ))
    line_fig.update_layout(
        title=f"{symbol} - Last 50 Real Prices & Next 5 Predicted",
        xaxis_title="Day",
        yaxis_title="Price ($)",
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='#181c20',
        paper_bgcolor='#181c20',
        xaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(230,230,230,0.1)', tickprefix='$'),
        hovermode='x unified',
        font=dict(color='#f1f1f1')
    )
    st.plotly_chart(line_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

