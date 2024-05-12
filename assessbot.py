import os
import streamlit as st
from google.generativeai import GenerativeModel
import google.generativeai as genai
from pathlib import Path
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure GenerativeAI with API key
genai.configure(api_key=GOOGLE_API_KEY)

# Create Generative Model instance
model = GenerativeModel('gemini-pro')

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

st.set_page_config(
    page_title="AI Chatbot",
    page_icon=":brain:",  # Favicon emoji
    layout="wide")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title(":blue[Assess the Idea and get info on ROI using our AI]")

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

user_prompt = st.chat_input("Enter your idea...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to model and get the response
    try:
        gemini_response = st.session_state.chat_session.send_message(
            f"Provide a market analysis and ROI estimation for the following idea: {user_prompt}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    else:
        # Display model's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)