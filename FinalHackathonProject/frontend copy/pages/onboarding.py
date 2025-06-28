import streamlit as st
from utils.session import set_page
from data.constants import ONBOARDING_QUESTIONS

def show_onboarding():
    """Show the onboarding quiz with improved UI"""
    # Initialize onboarding state if not already done
    if "onboard_qn" not in st.session_state:
        st.session_state["onboard_qn"] = 0
        st.session_state["onboard_answers"] = []
        
    # Get current question index
    qn_idx = st.session_state["onboard_qn"]
    qn, opts = ONBOARDING_QUESTIONS[qn_idx]
    
    # Create a card container
    st.markdown("""
        <div class='card' style='max-width:540px; margin:auto; 
                 transform:translateY(0px); transition:transform 0.3s ease-out;'
             onmouseover="this.style.transform='translateY(-5px)'" 
             onmouseout="this.style.transform='translateY(0px)'">
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <h2 style='color:#3b82f6; margin-bottom:0.5rem;'>Trader Profile</h2>
        <p style='color:#6366f1; margin-bottom:1.5rem;'>Let's customize your experience to get better predictions</p>
    """, unsafe_allow_html=True)
    
    # Title with animation
    st.markdown("""
        <h3 style='color:#1e3c72; text-align:center; margin-bottom:1.5rem;'>
            <span style='position:relative; display:inline-block;'>
                Trader Onboarding
                <span style='position:absolute; bottom:-5px; left:0; width:0; height:2px; 
                      background:linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); 
                      animation:underline 1s forwards;'></span>
            </span>
        </h3>
        <style>
            @keyframes underline {
                to { width: 100%; }
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress = int((qn_idx+1)/len(ONBOARDING_QUESTIONS)*100)
    st.markdown(f"""
        <div class='progress-bar-bg'>
            <div class='progress-bar-fill' style='width:{progress}%;'></div>
        </div>
        <div style='display:flex; justify-content:space-between; margin-bottom:1.5rem;'>
            <div style='font-size:1rem; font-weight:600;'>Question {qn_idx+1}/{len(ONBOARDING_QUESTIONS)}</div>
            <div style='font-size:1rem; color:#2a5298;'>{progress}% Complete</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Question with animation
    st.markdown(f"""
        <div style='font-size:1.2rem; font-weight:600; margin-bottom:1.5rem; 
                  animation:fadeIn 0.5s ease-out;'>
            {qn}
        </div>
        <style>
            @keyframes fadeIn {{
                from {{ opacity:0; transform:translateY(10px); }}
                to {{ opacity:1; transform:translateY(0); }}
            }}
        </style>
    """, unsafe_allow_html=True)
    
    # Answer input based on question type with improved styling
    answer = None
    
    st.markdown("<div style='background:#f8fafc; padding:1.5rem; border-radius:0.5rem; margin-bottom:1.5rem;'>", unsafe_allow_html=True)
    
    if qn_idx == 4:  # Sectors (checkboxes)
        st.markdown("<p style='color:#64748b; font-size:0.9rem; margin-bottom:0.5rem;'>Select all that apply</p>", unsafe_allow_html=True)
        answer = st.multiselect("Select sectors", opts, key=f"onboard_{qn_idx}")
    elif qn_idx == 5:  # 3 favorite stocks
        st.markdown("<p style='color:#64748b; font-size:0.9rem; margin-bottom:0.5rem;'>Separate with commas (e.g., AAPL, MSFT, GOOGL)</p>", unsafe_allow_html=True)
        answer = st.text_input("Enter your favorite stocks", key=f"onboard_{qn_idx}")
    elif qn_idx == 8:  # Technical indicators
        use_ind = st.radio("Do you use technical indicators?", ["Yes", "No"], key=f"onboard_{qn_idx}_yn")
        if use_ind == "Yes":
            st.markdown("<p style='color:#64748b; font-size:0.9rem; margin-bottom:0.5rem;'>Separate with commas (e.g., MACD, RSI, Moving Averages)</p>", unsafe_allow_html=True)
            which = st.text_input("Which ones?", key=f"onboard_{qn_idx}_which")
        else:
            which = "None"
        answer = f"{use_ind} - {which}"
    elif opts:  # Multiple choice
        answer = st.radio("", opts, key=f"onboard_{qn_idx}", horizontal=True if len(opts) <= 4 else False)
    else:  # Free text
        st.markdown("<p style='color:#64748b; font-size:0.9rem; margin-bottom:0.5rem;'>Please provide a detailed answer</p>", unsafe_allow_html=True)
        answer = st.text_input("", key=f"onboard_{qn_idx}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Store answer in session state
    st.session_state["onboard_answers"][qn_idx] = answer
    
    # Navigation buttons with improved styling
    st.markdown("<div style='display:flex; gap:1rem; margin-top:1rem;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Previous", disabled=qn_idx==0, use_container_width=True, key="prev_btn", type="secondary"):
            st.session_state["onboard_qn"] -= 1
            st.rerun()
    
    with col2:
        next_disabled = answer in [None, ""] or (isinstance(answer, list) and len(answer) == 0)
        next_text = "Next →" if qn_idx < len(ONBOARDING_QUESTIONS)-1 else "Finish"
        
        if st.button(next_text, disabled=next_disabled, use_container_width=True, key="next_btn", type="primary"):
            if qn_idx < len(ONBOARDING_QUESTIONS)-1:
                st.session_state["onboard_qn"] += 1
                st.rerun()
            else:
                # Last question - create user profile and proceed
                profile = []
                for i, (q, _) in enumerate(ONBOARDING_QUESTIONS):
                    profile.append(f"Q{i+1}: {q} -> {st.session_state['onboard_answers'][i]}")
                
                # Create a structured prompt for ML model
                st.session_state["user_prompt"] = "\n".join(profile)
                
                # Show success message with confetti
                st.balloons()
                st.success("Profile created successfully! Your personalized trading experience is ready.")
                
                # Proceed to dashboard
                set_page("dashboard")
                st.rerun()
    
    # Close the navigation container
    st.markdown("</div>", unsafe_allow_html=True)

    # For radio/select options, Streamlit uses default, but if any custom style is set, override it:
    st.markdown("""
    <style>
    .stRadio>div>label, .stSelectbox>div>div>div, .stCheckbox>div>label {
        color: #1e293b !important;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)