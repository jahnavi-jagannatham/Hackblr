import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import cohere
from pathlib import Path
import base64
import os

# Load the existing CSV file
data = pd.read_csv("ideas.csv")

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

def chat_with_csv(df, prompt):
    co = cohere.Client(api_key=cohere_api_key)
    response = co.chat(model="command-r-plus", message=prompt)
    return response.text

st.set_page_config(layout='wide')
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

st.title("Improve your existing idea using our AI powered-bot")

input_text = st.text_input("Enter your query", placeholder="Ask me anything...")
if input_text:
    result = chat_with_csv(data, input_text)
    st.success(result)