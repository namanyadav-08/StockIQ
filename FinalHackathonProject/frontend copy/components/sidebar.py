import streamlit as st
from data.constants import NAVIGATION_ITEMS

def render_sidebar():
    """Render the sidebar with navigation and user info"""
    with st.sidebar:
        # Logo and title
        st.markdown("<div class='sidebar-logo'>🔮 StockIQ</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
        
        # Navigation items
        current_page = st.session_state["page"]
        for label, nav in NAVIGATION_ITEMS:
            if current_page == nav:
                st.markdown(f"<div class='badge'>{label}</div>", unsafe_allow_html=True)
            else:
                if st.button(f"{label}", key=f"nav_{nav}"):
                    st.session_state["page"] = nav
        
        # User info (if logged in)
        if st.session_state.get("user_email"):
            st.markdown(
                f"<div class='sidebar-user'>👤 {st.session_state['user_email']}</div>", 
                unsafe_allow_html=True
            )
            
        # Add a logout button if user is logged in
        if st.session_state.get("logged_in"):
            if st.button("Logout", key="sidebar_logout"):
                st.session_state["logged_in"] = False
                st.session_state["user_email"] = ""
                st.session_state["page"] = "welcome"