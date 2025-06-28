import streamlit as st
import random

def render_chatbot():
    """Render the chatbot UI in the bottom right corner"""
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
            text_color = 'white' if sender == 'user' else '#333'
            
            st.markdown(
                f"<div style='text-align:{align}; margin-bottom:0.5rem;'>"
                f"<div style='background:{color}; color:{text_color}; border-radius:12px; "
                f"padding:0.6rem 1rem; display:inline-block; max-width:80%; box-shadow:0 1px 3px rgba(0,0,0,0.1);'>"
                f"<b>{'You' if sender=='user' else 'DeepSeek'}:</b> {msg}</div></div>", 
                unsafe_allow_html=True
            )
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "", 
                placeholder="Type your question about this stock...", 
                key="chat_input"
            )
            
        with col2:
            submitted = st.form_submit_button("Send")
            
        if submitted and user_input:
            # Add user message to chat history
            chat_history.append((user_input, "user"))
            
            # Generate a simulated response
            responses = [
                f"Based on recent trends, {st.session_state.get('selected_stock', 'this stock')} is showing promising growth potential.",
                f"The technical indicators for {st.session_state.get('selected_stock', 'this stock')} suggest cautious optimism.",
                f"Analysts are divided on {st.session_state.get('selected_stock', 'this stock')}, with some predicting a breakout and others concerned about valuation.",
                f"Recent news about {st.session_state.get('selected_stock', 'this stock')} has been generally positive, which could drive short-term gains.",
                f"The market sentiment around {st.session_state.get('selected_stock', 'this stock')} is currently bullish, but watch for volatility."
            ]
            
            # Add bot response to chat history
            chat_history.append((random.choice(responses), "bot"))
            
            # Update session state
            st.session_state["chat_history"] = chat_history
    
    # Close the chatbox div
    st.markdown("</div>", unsafe_allow_html=True)