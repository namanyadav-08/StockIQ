import streamlit as st
import time
import random
from utils.session import set_page
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

def show_chatbot():
    # Header with animated gradient
    st.markdown("""
    <div style='background:linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); border-radius:1rem; padding:1.5rem; margin-bottom:2rem; box-shadow:0 4px 15px rgba(59, 130, 246, 0.2); animation:fadeIn 0.5s ease-out;'>
        <h1 style='color:#1e293b; margin-bottom:0.5rem; font-size:2rem;'>StockIQ </h1>
        <p style='color:rgba(255,255,255,0.9); margin:0; font-size:1rem;'>Your AI trading assistant powered by machine learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background:white; border-radius:0.75rem; padding:1.25rem; height:100%; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
            <div style='font-size:1.5rem; color:#3b82f6; margin-bottom:0.5rem;'>📊</div>
            <h3 style='margin:0 0 0.5rem 0; font-size:1rem;'>Market Analysis</h3>
            <p style='color:#64748b; font-size:0.9rem; margin:0;'>Get real-time insights on market trends and stock movements</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style='background:white; border-radius:0.75rem; padding:1.25rem; height:100%; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
            <div style='font-size:1.5rem; color:#3b82f6; margin-bottom:0.5rem;'>🎯</div>
            <h3 style='margin:0 0 0.5rem 0; font-size:1rem;'>Personalized Recommendations</h3>
            <p style='color:#64748b; font-size:0.9rem; margin:0;'>Tailored stock picks based on your trading profile</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style='background:white; border-radius:0.75rem; padding:1.25rem; height:100%; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
            <div style='font-size:1.5rem; color:#3b82f6; margin-bottom:0.5rem;'>📈</div>
            <h3 style='margin:0 0 0.5rem 0; font-size:1rem;'>Risk Assessment</h3>
            <p style='color:#64748b; font-size:0.9rem; margin:0;'>Evaluate potential risks and opportunities in your portfolio</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom:2rem;'></div>", unsafe_allow_html=True)
    
    # Chat container with custom styling
    st.markdown("""
    <div style='background:white; border-radius:1rem; padding:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03); margin-bottom:1.5rem;'>
        <h3 style='color:#3b82f6; margin-top:0; margin-bottom:1rem; font-size:1.2rem;'>Chat with Stock IQ AI</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_message = "Hello! I'm your Stock IQ AI assistant. How can I help with your trading decisions today?"
        
        # Add personalized welcome if user profile exists
        if "user_prompt" in st.session_state and st.session_state["user_prompt"]:
            profile_summary = st.session_state["user_prompt"].split('\n')[0] if '\n' in st.session_state["user_prompt"] else st.session_state["user_prompt"]
            welcome_message += f"\n\nBased on your profile, I understand you're a {profile_summary.lower() if not profile_summary.startswith('Q:') else 'trader looking for personalized insights'}. I'll tailor my recommendations accordingly."
        
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})

    # Custom chat message styling
    chat_container = st.container(border=True)
    with chat_container:
        for message in st.session_state.messages:
            is_user = message["role"] == "user"
            avatar = "👤" if is_user else "🔮"
            bg_color = "#f1f5f9" if is_user else "#f0f9ff"
            text_align = "right" if is_user else "left"
            border_radius = "1rem 1rem 0 1rem" if is_user else "1rem 1rem 1rem 0"
            margin = "0.5rem 0 0.5rem auto" if is_user else "0.5rem auto 0.5rem 0"
            max_width = "80%"
            
            st.markdown(f"""
            <div style='display:flex; flex-direction:{'row-reverse' if is_user else 'row'}; align-items:flex-start; margin-bottom:1rem;'>
                <div style='background:{bg_color}; padding:0.8rem 1rem; border-radius:{border_radius}; max-width:{max_width}; margin:{margin}; box-shadow:0 1px 2px rgba(0,0,0,0.05); text-align:{text_align};'>
                    {message['content']}
                </div>
                
            </div>
            """, unsafe_allow_html=True)

    # Suggestion chips
    if len(st.session_state.messages) <= 2:  # Show suggestions for new conversations
        st.markdown("<p style='color:#64748b; font-size:0.9rem; margin:1rem 0 0.5rem 0;'>Try asking:</p>", unsafe_allow_html=True)
        
        suggestion_col1, suggestion_col2 = st.columns(2)
        
        with suggestion_col1:
            if st.button("📊 Recommend stocks for me", key="suggest_1"):
                prompt = "Can you recommend some stocks based on my trading profile?"
                st.session_state.messages.append({"role": "user", "content": prompt})
            if st.button("📈 Current market trends", key="suggest_2"):
                prompt = "What are the current market trends I should be aware of?"
                st.session_state.messages.append({"role": "user", "content": prompt})

        with suggestion_col2:
            
                
            if st.button("🔍 Analyze my risk profile", key="suggest_3"):
                prompt = "Can you analyze my risk profile and suggest adjustments?"
                st.session_state.messages.append({"role": "user", "content": prompt})
                
            if st.button("👤 Show my trading profile", key="suggest_4"):
                prompt = "Show me my trading profile"
                st.session_state.messages.append({"role": "user", "content": prompt})

    # Before rendering the text_input, check if you need to clear it
    if st.session_state.get("clear_input", False):
        st.session_state["chat_input"] = ""
        st.session_state["clear_input"] = False

    # Input with send button
    col1, col2 = st.columns([6, 1])
    with col1:
        prompt = st.text_input("Type your message...", key="chat_input", label_visibility="collapsed")
    with col2:
        send_button = st.button("Send", key="send_button")

    if prompt and send_button:
        st.session_state.messages.append({"role": "user", "content": prompt})
        full_response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state["clear_input"] = True
        st.rerun()


def generate_response(prompt):
    # Use OpenRouter API to get a response from the model
    with st.spinner("Thinking..."):
        try:
            completion = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528:free",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"[Error from AI API: {e}]"