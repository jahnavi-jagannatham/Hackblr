import streamlit as st
import webbrowser
import socket
import os
import threading
import time
from pathlib import Path
import base64
import os

def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port

def run_streamlit_code(code):
    port = get_free_port()
    with open('temp_app.py', 'w') as f:
        f.write(code)

    # Start Streamlit server in a separate thread
    streamlit_thread = threading.Thread(target=start_streamlit_server, args=(port,))
    streamlit_thread.start()

    # Wait for the server to start before opening the browser
    time.sleep(2)

    webbrowser.open(f'http://localhost:{port}')

def start_streamlit_server(port):
    os.system(f'streamlit run temp_app.py --server.port={port} --server.headless=true')

def main():
    current_dir = Path(__file__).parent
    background_image = current_dir / "background_image4.png"
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
    st.title(":blue[Test your streamlit prototype]")
    code = st.text_area("Enter your Streamlit code:", height=300)
    run_button = st.button("Run")

    if run_button:
        run_streamlit_code(code)

if __name__ == "__main__":
    main()