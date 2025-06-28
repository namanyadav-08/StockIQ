import streamlit as st
from data.constants import ONBOARDING_QUESTIONS

def set_page(page):
    """Set the current page in session state"""
    st.session_state["page"] = page

def init_session():
    """Initialize all session state variables"""
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