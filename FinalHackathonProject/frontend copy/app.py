import streamlit as st
import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from utils.session import init_session
from utils.styles import apply_styles
from components.sidebar import render_sidebar
from pages.welcome import show_welcome
from pages.auth import show_auth
from pages.onboarding import show_onboarding
from pages.dashboard import show_dashboard
from pages.stock_detail import show_stock_detail
from pages.chatbot import show_chatbot

# Main App
def main():
    # Apply custom styles
    apply_styles()
    
    # Initialize session state
    init_session()
    
    # Render sidebar
    render_sidebar()
    
    # Render the appropriate page based on session state
    page = st.session_state["page"]
    
    if page == "welcome":
        show_welcome()
    elif page == "auth":
        show_auth()
    elif page == "onboard":
        show_onboarding()
    elif page == "dashboard":
        show_dashboard()
    elif page == "stock_detail":
        show_stock_detail()
    elif page == "chatbot":
        show_chatbot()
    else:
        st.error("Unknown page.")

if __name__ == "__main__":
    main()