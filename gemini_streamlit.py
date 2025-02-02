import os
import requests
import streamlit as st
#from dotenv import load_dotenv

# Load environment variables
#load_dotenv('api.env')

API_KEY = st.secrets[GEMINI_API_KEY]
# Configure API
#API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Streamlit page config
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and display bot response
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.markdown(response)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar controls
with st.sidebar:
    st.title("Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
    st.markdown("---")
    st.markdown("**Instructions:**\n- Type your message below\n- Click 'Clear Chat History' to restart")
