import streamlit as st
import requests
import uuid
import json
from datetime import datetime

# Configuration
WEBHOOK_URL = "https://amazecannabis.app.n8n.cloud/webhook/4811f856-b1b7-4035-9f6c-961045ac72b2"
BEARER_TOKEN = "9f3e1a7b69e84f5fb12a6d0e5d2c7e9a2c3f4b5d6e7f8a9b0c1d2e3f4g5h6i7j"

# Initialize session state if not already done
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Page configuration
st.set_page_config(page_title="Chat with AI", page_icon="💬")
st.title("Chat with AI")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Prepare the payload for the webhook
    payload = {
        "sessionId": st.session_state.session_id,
        "chatInput": prompt
    }
    
    # Headers with bearer token
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Send request to n8n webhook
        response = requests.post(
            WEBHOOK_URL,
            headers=headers,
            json=payload
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the response
        ai_response = response.json().get('output', 'Sorry, I could not process your request.')
        
        # Display AI response
        with st.chat_message("assistant"):
            st.write(ai_response)
        
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the server: {str(e)}")
    except json.JSONDecodeError:
        st.error("Error parsing server response")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Display session information in sidebar
with st.sidebar:
    st.write("Session Information")
    st.write(f"Session ID: {st.session_state.session_id}")
    st.write(f"Messages in conversation: {len(st.session_state.messages)}")
