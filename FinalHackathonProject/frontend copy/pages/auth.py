import streamlit as st
from utils.session import set_page

def show_auth():
    """Show the login/signup page with improved UI"""
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Glass-morphism card with improved styling
        st.markdown("<div class='glass-card' style='background:#f5f6fa; border:1px solid #e5e7eb;'>" , unsafe_allow_html=True)
        
        # Animated title with new styling
        st.markdown("""
            <div class='animated-title' style='color:#2563eb;'>StockIQ</div>
            <div style='text-align:center; margin-bottom:2rem; color:#555; font-weight:500;'>Your AI-Powered Trading Assistant</div>
        """, unsafe_allow_html=True)
        
        # Toggle between login and signup with improved tabs
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
        
        with login_tab:
            # Login form with improved styling
            with st.form("login_form"):
                st.markdown("<p style='font-size:0.9rem; color:#555; margin-bottom:0.5rem;'>Welcome back! Enter your credentials to continue.</p>", unsafe_allow_html=True)
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                
                # Remember me checkbox
                col1, col2 = st.columns([1, 1])
                with col1:
                    remember = st.checkbox("Remember me", value=True)
                with col2:
                    st.markdown("<div style='text-align:right;'><a href='#' style='color:#3b82f6; text-decoration:none; font-size:0.9rem;'>Forgot password?</a></div>", unsafe_allow_html=True)
                
                submit = st.form_submit_button("Login")
                
                if submit:
                    if email and password:  # Simple validation
                        # Show success message with animation
                        st.success("Login successful! Redirecting...")
                        st.session_state["logged_in"] = True
                        st.session_state["user_email"] = email
                        set_page("onboard")
                    else:
                        st.error("Please enter both email and password")
        
        with signup_tab:
            # Signup form with improved styling
            with st.form("signup_form"):
                st.markdown("<p style='font-size:0.9rem; color:#555; margin-bottom:0.5rem;'>Create an account to get personalized stock predictions.</p>", unsafe_allow_html=True)
                new_email = st.text_input("Email", placeholder="your@email.com")
                new_password = st.text_input("Password", type="password", placeholder="••••••••")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                
                # Terms and conditions checkbox
                st.checkbox("I agree to the Terms of Service and Privacy Policy", value=True)
                
                submit = st.form_submit_button("Create Account")
                
                if submit:
                    if new_email and new_password and confirm_password:  # Simple validation
                        if new_password == confirm_password:
                            # Show success message with animation
                            st.success("Account created successfully! Redirecting to onboarding...")
                            st.session_state["logged_in"] = True
                            st.session_state["user_email"] = new_email
                            set_page("onboard")
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.error("Please fill in all fields")
        
        # Social login options
        st.markdown("""
            <div style='text-align:center; margin-top:1.5rem;'>
                <p style='color:#888; font-size:0.9rem; margin-bottom:0.5rem;'>Or continue with</p>
                <div style='display:flex; justify-content:center; gap:1rem;'>
                    <button class='social-btn' style='background:#2563eb; color:#1e293b;'>Google</button>
                    <button class='social-btn' style='background:#222; color:#fff;'>Apple</button>
                    <button class='social-btn' style='background:#222; color:#fff;'>GitHub</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Close the card div
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<style>
.stRadio>div>label, .stSelectbox>div>div>div, .stCheckbox>div>label {
    color: #1e293b !important;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)