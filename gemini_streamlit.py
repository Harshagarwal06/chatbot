import os
import requests
import streamlit as st

# Correctly access the secret
API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure API
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Streamlit page config
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcome message from the bot
    st.session_state.messages.append({"role": "assistant", "content": "Hi! I'm Gemini. How can I help you today?"})

def generate_response(prompt):
    """Get response from Gemini API"""
    contents = [{"role": msg["role"], "parts": [{"text": msg["content"]}]} 
               for msg in st.session_state.messages]
    contents.append({"role": "user", "parts": [{"text": prompt}]})
    
    data = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.9,
            "maxOutputTokens": 1000
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}?key={API_KEY}",
            headers={'Content-Type': 'application/json'},
            json=data
        )
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error: {str(e)}"

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input with placeholder
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message with avatar
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Display a spinner while generating the response
    with st.spinner("Thinking..."):
        response = generate_response(prompt)
    
    # Display bot response with avatar
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar controls
with st.sidebar:
    st.title("Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared!")
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("- Type your message in the chat box below.")
    st.markdown("- Click 'Clear Chat History' to restart the conversation.")
    st.markdown("- Enjoy chatting with the Gemini AI!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by [Harsh Agarwal]")
