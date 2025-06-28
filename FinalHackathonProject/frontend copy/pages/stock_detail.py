import streamlit as st
import plotly.graph_objs as go
import random
import datetime
from utils.session import set_page
from data.constants import STOCKS, NEWS_HEADLINES
from components.chatbot import render_chatbot
import yfinance as yf
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import tempfile
import os

def show_stock_detail():
    """Show detailed information for a selected stock with improved UI and real predictions only"""
    # Get the selected stock from session state
    symbol = st.session_state["selected_stock"]
    stock = next((s for s in STOCKS if s["symbol"] == symbol), None)
    
    if not stock:
        st.error("Stock not found.")
        set_page("dashboard")
        return
    
    # Fetch last 50 real closing prices
    ticker = symbol
    data = yf.download(ticker, period="90d")
    if data is None or data.empty or 'Close' not in data:
        st.error("Failed to fetch data for this stock. Please try again later.")
        return
    closes = data['Close'].dropna().values[-50:]
    if len(closes) < 50:
        st.error("Not enough data to fetch 50 closing prices.")
        return
    st.markdown("#### Last 50 real closing prices:")
    st.code(", ".join([f"{float(x):.2f}" for x in closes]), language="text")
    
    # Call FastAPI backend for predictions
    api_url = "http://127.0.0.1:8000/predict"
    try:
        response = requests.post(api_url, json={
            "symbol": symbol,
            "last_50_prices": closes.tolist()
        })
        if response.status_code == 200:
            preds = response.json()["predicted_prices"]
        else:
            st.error(f"Prediction API error: {response.text}")
            return
    except Exception as e:
        st.error(f"Failed to connect to prediction API: {e}")
        return
    
    # Prepare chart data for both chart types
    chart_dates = [f"Day {i+1}" for i in range(50)] + [f"Pred {i+1}" for i in range(5)]
    chart_prices = [float(x) for x in closes] + [float(x) for x in preds]

    # Create a card container for stock details
    st.markdown(f"""<div class='card' style='max-width:900px; margin:auto; margin-bottom:2rem; background:#f5f6fa; border:1px solid #e5e7eb;'>""", unsafe_allow_html=True)
    # Stock header with logo, symbol, and name
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:1.5rem; margin-bottom:1.5rem; background:linear-gradient(135deg, #f5f6fa 0%, #e3e9f3 100%); padding:1.5rem; border-radius:1rem;'>
            <div class='stock-logo-large' style='font-size:4rem; background:#2563eb; color:#1e293b; width:5rem; height:5rem; display:flex; align-items:center; justify-content:center; border-radius:1rem; box-shadow:0 10px 15px -3px rgba(37,99,235,0.13);'>
                {stock['logo']}
            </div>
            <div style='flex:1;'>
                <div style='display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;'>
                    <span style='font-size:2.2rem; font-weight:800; color:#222;'>{stock['symbol']}</span>
                    <span class='badge' style='background:#2563eb; color:#1e293b;'>{stock['name']}</span>
                </div>
                <div style='color:#555; font-size:1rem; display:flex; gap:1rem; align-items:center;'>
                    <span>Technology</span>
                    <span style='width:4px; height:4px; background:#bbb; border-radius:50%;'></span>
                    <span>NASDAQ</span>
                    <span style='width:4px; height:4px; background:#bbb; border-radius:50%;'></span>
                    <span>United States</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Show predicted prices as a clear table
    st.markdown("<h4 style='margin-top:2em; color:#2563eb;'>Predicted prices for next 5 days:</h4>", unsafe_allow_html=True)
    pred_df = pd.DataFrame({"Day": [f"Day {i+1}" for i in range(5)], "Predicted Price": [f"${float(preds[i]):.2f}" for i in range(5)]})
    st.markdown("<div style='background:#fff; border:1px solid #e5e7eb; border-radius:0.7rem; padding:1em; margin-bottom:1.5em;'>", unsafe_allow_html=True)
    st.dataframe(pred_df, hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Chart switcher
    chart_type = st.radio(
        "Select chart type:",
        ("Line + Markers (Default)", "Area + Bar Combo"),
        horizontal=True,
        index=0,
        key="chart_type_switch"
    )

    if chart_type == "Line + Markers (Default)":
        # Plot last 50 + next 5 predicted prices in a beautiful chart
        line_fig = go.Figure()
        line_fig.add_trace(go.Scatter(
            x=chart_dates,
            y=chart_prices,
            mode='lines+markers',
            name='Price',
            line=dict(color='#3b82f6', width=4, shape='spline', smoothing=1.3),
            marker=dict(color=['#3b82f6']*50 + ['#f59e42']*5, size=[8]*50 + [18]*5, symbol=['circle']*50 + ['star']*5),
            hovertemplate='Day: %{x}<br>Price: $%{y:.2f}<extra></extra>'
        ))
        line_fig.add_trace(go.Scatter(
            x=chart_dates[50:],
            y=chart_prices[50:],
            mode='markers+text',
            name='Prediction',
            marker=dict(color='#f59e42', size=22, symbol='star', line=dict(width=2, color='#2563eb')),
            text=[f"${float(p):.2f}" for p in preds],
            textposition="top center",
            hovertemplate='Prediction: %{x}<br>Price: $%{y:.2f}<extra></extra>'
        ))
        line_fig.update_layout(
            title=f"{stock['symbol']} - Last 50 Real Prices & Next 5 Predicted",
            xaxis_title="Day",
            yaxis_title="Price ($)",
            height=500,
            margin=dict(l=20, r=20, t=60, b=20),
            plot_bgcolor='#fff',
            paper_bgcolor='#fff',
            xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)', tickprefix='$'),
            hovermode='x unified',
            font=dict(color='#222'),
            showlegend=False,
        )
        st.markdown("<div style='background:#fff; border:1px solid #e5e7eb; border-radius:0.7rem; box-shadow:0 2px 12px rgba(37,99,235,0.07); padding:1.5em; margin-bottom:2em;'>", unsafe_allow_html=True)
        st.plotly_chart(line_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # --- Area + Bar Combo chart ---
        area_bar_fig = go.Figure()
        # Area for last 50
        area_bar_fig.add_trace(go.Scatter(
            x=chart_dates[:50],
            y=chart_prices[:50],
            mode='lines',
            name='Last 50 Prices',
            line=dict(color='#2563eb', width=3, shape='spline', smoothing=1.2),
            fill='tozeroy',
            fillcolor='rgba(37,99,235,0.13)',
            hovertemplate='Day: %{x}<br>Price: $%{y:.2f}<extra></extra>'
        ))
        # Bars for next 5
        area_bar_fig.add_trace(go.Bar(
            x=chart_dates[50:],
            y=chart_prices[50:],
            name='Predicted',
            marker=dict(color='#f59e42', line=dict(width=2, color='#2563eb')),
            text=[f"${float(p):.2f}" for p in preds],
            textposition='outside',
            width=0.6,
            hovertemplate='Prediction: %{x}<br>Price: $%{y:.2f}<extra></extra>'
        ))
        area_bar_fig.update_layout(
            title=f"{stock['symbol']} - Last 50 Real Prices & Next 5 Predicted (Area + Bar)",
            xaxis_title="Day",
            yaxis_title="Price ($)",
            height=500,
            margin=dict(l=20, r=20, t=60, b=20),
            plot_bgcolor='#fff',
            paper_bgcolor='#fff',
            xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)', tickprefix='$'),
            hovermode='x unified',
            font=dict(color='#222'),
            showlegend=False,
            barmode='overlay',
        )
        st.markdown("<div style='background:#fff; border:1px solid #e5e7eb; border-radius:0.7rem; box-shadow:0 2px 12px rgba(37,99,235,0.07); padding:1.5em; margin-bottom:2em;'>", unsafe_allow_html=True)
        st.plotly_chart(area_bar_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # News headlines section
    st.markdown("<h4 style='color:#2a5298; margin-top:1.5rem;'>Latest News</h4>", unsafe_allow_html=True)
    
    # --- Finnhub News Integration ---
    def get_finnhub_news(symbol, api_key):
        today = datetime.date.today()
        last_month = today - datetime.timedelta(days=30)
        url = (
            f"https://finnhub.io/api/v1/company-news"
            f"?symbol={symbol}&from={last_month}&to={today}&token={api_key}"
        )
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    FINNHUB_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    news_items = get_finnhub_news(symbol, FINNHUB_API_KEY)

    if news_items:
        for article in news_items[:5]:
            st.markdown(f"**[{article['headline']}]({article['url']})**", unsafe_allow_html=True)
            st.write(article['summary'])
            dt = datetime.datetime.fromtimestamp(article['datetime'])
            st.write(f"*Source: {article['source']} | Date: {dt.strftime('%Y-%m-%d %H:%M')}*")
            st.markdown("---")
    else:
        st.write("No news found for this stock.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Download Report Button ---
    def safe_latin1(text):
        return text.encode('latin-1', 'replace').decode('latin-1')

    def create_pdf_report(symbol, preds, news_items, closes):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, safe_latin1(f'Stock Report: {symbol}'), ln=True, align='C')
        pdf.ln(8)
        # Add chart image
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(list(range(1, 51)), closes, label='Last 50 Prices', color='#3b82f6')
        ax.plot(list(range(51, 56)), preds, label='Predicted', color='#f59e42')
        ax.set_title(safe_latin1(f'{symbol} - Last 50 Prices & Next 5 Predicted'))
        ax.set_xlabel('Day')
        ax.set_ylabel('Price ($)')
        ax.legend()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            plt.tight_layout()
            plt.savefig(tmpfile, format='png')
            plt.close(fig)
            tmpfile_path = tmpfile.name
        pdf.image(tmpfile_path, x=10, y=None, w=pdf.w-20)
        os.remove(tmpfile_path)
        pdf.ln(70)
        # Add predictions
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, safe_latin1('Predicted Prices (Next 5 Days):'), ln=True)
        pdf.set_font('Arial', '', 12)
        for i, p in enumerate(preds):
            pdf.cell(0, 8, safe_latin1(f'Day {i+1}: ${float(p):.2f}'), ln=True)
        pdf.ln(4)
        # Add news headlines
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, safe_latin1('Latest News Headlines:'), ln=True)
        pdf.set_font('Arial', '', 12)
        for article in news_items[:5]:
            pdf.multi_cell(0, 8, safe_latin1(f"- {article['headline']}"))
        out = pdf.output(dest='S')
        if isinstance(out, str):
            return out.encode('latin-1')
        if isinstance(out, bytearray):
            return bytes(out)
        return out

    pdf_bytes = None
    if st.button('Download Report (PDF)', use_container_width=True):
        # Only use the data already fetched
        pdf_bytes = create_pdf_report(symbol, preds, news_items, closes)
    if pdf_bytes:
        st.download_button(
            label='Click here to download your PDF report',
            data=pdf_bytes,
            file_name=f'{symbol}_report.pdf',
            mime='application/pdf',
            use_container_width=True
        )

    # Back button
    if st.button("Back to Dashboard", use_container_width=True):
        set_page("dashboard")

    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"], .stTabs [aria-selected="true"] {
        color: #1e293b !important;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
