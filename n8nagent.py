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

# Function to make the API call
def send_message_to_webhook(message, session_id):
    payload = {
        "sessionId": session_id,
        "chatInput": message
    }
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Debug information
        st.sidebar.write("Sending request with payload:", payload)
        
        response = requests.post(
            WEBHOOK_URL,
            headers=headers,
            data=json.dumps(payload),  # Explicitly convert to JSON string
            verify=True  # Enable SSL verification
        )
        
        # Debug information
        st.sidebar.write("Response status code:", response.status_code)
        st.sidebar.write("Response headers:", dict(response.headers))
        
        try:
            st.sidebar.write("Response content:", response.text)
        except:
            st.sidebar.write("Could not display response content")
        
        response.raise_for_status()
        return response.json().get('output', 'Sorry, I could not process your request.')
        
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {str(e)}")
        return f"Error: {str(e)}"
    except json.JSONDecodeError as e:
        st.error(f"JSON decode error: {str(e)}")
        return "Error: Could not parse server response"
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return f"Error: {str(e)}"

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
    
    # Show a spinner while waiting for the response
    with st.spinner('Waiting for response...'):
        # Get AI response
        ai_response = send_message_to_webhook(prompt, st.session_state.session_id)
        
        # Display AI response
        with st.chat_message("assistant"):
            st.write(ai_response)
        
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Display session information in sidebar
with st.sidebar:
    st.write("Session Information")
    st.write(f"Session ID: {st.session_state.session_id}")
    st.write(f"Messages in conversation: {len(st.session_state.messages)}")
