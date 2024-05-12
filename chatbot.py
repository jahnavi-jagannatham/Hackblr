import os
import streamlit as st
from google.generativeai import GenerativeModel
import google.generativeai as genai
from pathlib import Path
import base64
import os
from dotenv import load_dotenv
import pandas as pd

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

def assign_domain(row):
    idea = row['description']
    domain = model.estimate(idea, topk=1)[0]['domain']
    return domain

st.set_page_config(
    page_title="AI Chatbot",
    page_icon=":brain:",  # Favicon emoji
    layout="wide"
)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

current_dir = Path(__file__).parent
background_image = current_dir / "background_image3.png"
with open(background_image, "rb") as f:
    image_bytes = f.read()
encoded_image = base64.b64encode(image_bytes).decode()
background_style = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{encoded_image}");
    background-size: cover;
    background-position: center;
}}
.stFileUploader > div > div > div > div {{
    color: black; /* Set input text color to black */
}}
</style>
"""
st.markdown(background_style, unsafe_allow_html=True)

st.title(":blue[Build your prototype by generating streamlit code]")

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

user_prompt = st.chat_input("Ask your question...")


if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to model and get the response
    try:
        gemini_response = st.session_state.chat_session.send_message(
            f"Give streamlit code to build the following idea: {user_prompt}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    else:
        # Display model's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

