import streamlit as st
from pathlib import Path
import base64
import os
import pandas as pd
from streamlit import session_state

def home_page():
    current_dir = Path(__file__).parent
    background_image = current_dir / "background_image.png"
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
    # Title and Welcome Message
    st.title("Welcome to :blue[Kick-Start-Up!]")
    st.markdown("<p style='color: lightblue; font-size: 30px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Connecting Social Impact Projects with Potential Investors""</p>",
    unsafe_allow_html=True)

    # Description
    st.markdown(
    "<p style='color: white; font-size: 15px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>"
    "Kick-Start-Up is a platform dedicated to fostering sustainability and driving positive change. "
    "We bridge the gap between social impact projects and investors who are passionate about making a difference. "
    "Whether you're an investor looking to support impactful initiatives or an ideator seeking funding to bring your vision to life, "
    "Kick-Start-Up is your platform for sustainable change."
    "</p>",
    unsafe_allow_html=True  
    )

    # Buttons for Login
    # Buttons for Login with increased size
    col1, col2 = st.columns([2,2])
    ideatorlogin=col1.button("Login as Ideator")
    if ideatorlogin: 
        st.session_state['page'] = 'ideatorlogin'
    investorlogin=col2.button("Login as Investor")
    if investorlogin:
        st.session_state['page'] = 'investorlogin'
    # Custom CSS to increase button size
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            width: 200px; /* Adjust button width as needed */
            height: 50px; /* Adjust button height as needed */
            font-size: 30px; /* Adjust font size as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def authenticate_user(username, password):
    df = pd.read_csv('ideators.csv')
    #hashed_password = hash_password(password)
    if ((df['username'] == username) & (df['password'] == password)).any():
        return True
    else:
        return False

def ideatorlogin():
    st.title("LOGIN AS :red[IDEATOR]")
    username = st.text_input("USER NAME")
    session_state["username"] = username
    password = st.text_input("PASSWORD",type="password")
    login= st.button("LOG IN")
    if login:
        if authenticate_user(username, password):
            st.session_state['page'] = 'ideate'
        else:
            st.error("Invalid username or password.")
    st.write("<div style='text-align: center;'><p style='font-size: 24px;'>New  user ? Dont have  an  account</p> </div>", unsafe_allow_html=True)
    col1,col2,col3=st.columns([2,2,1])
    ideatorsignup=col2.button("SIGN UP AS IDEATOR")
    if ideatorsignup:
        st.session_state['page'] = 'ideatorsignup'
    return username

def ideatorsignup():
    st.title("Sign Up as Ideator")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
         add_ideator(new_username, new_password)
         st.session_state['page'] = 'home'

# Function to add a new user to CSV
def add_ideator(username, password):
    df = pd.DataFrame({'username': [username], 'password': [password]})
    df.to_csv('ideators.csv', mode='a', index=False)

def investorlogin():
    st.title("LOGIN AS :blue[INVESTOR]")
    username = st.text_input("USER NAME")
    password = st.text_input("PASSWORD",type="password")
    login= st.button("LOG IN")
    if login:
        if authenticate_user(username, password):
            st.session_state['page'] = 'invest'
        else:
            st.error("Invalid username or password.")
    st.write("<div style='text-align: center;'><p style='font-size: 24px;'>New  user ? Dont have  an  account</p> </div>", unsafe_allow_html=True)
    col1,col2,col3=st.columns([2,2,1])
    ideatorsignup=col2.button("SIGN UP AS INVESTOR")
    if ideatorsignup:
        st.session_state['page'] = 'investorsignup'
    

def investorsignup():
    st.title("Sign Up as Investor")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
         add_investor(new_username, new_password)
         st.session_state['page'] = 'home'

def add_investor(username, password):
    df = pd.DataFrame({'username': [username], 'password': [password]})
    df.to_csv('investors.csv', mode='a', index=False)

def ideate():
    st.title("Ideate ")
    if "username" in session_state:
        username = session_state["username"]
    st.write(username)
    st.markdown("<p style='color: lightblue; font-size: 30px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Do you've your idea and working model ready?""</p>",
    unsafe_allow_html=True)
    but1=st.button("Share a New Idea")
    if but1:
        st.session_state['page'] = 'shareidea'
    st.markdown("<p style='color: lightblue; font-size: 30px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Have an idea but don't know how to build a prototype? </br> We've got your back, build prototype with the help of our AI""</p>",
    unsafe_allow_html=True)
    but2=st.button("Develop a prototype")
    if but2:
        pass
    st.markdown("<p style='color: lightblue; font-size: 30px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Improve your idea with the help of AI-powered bot""</p>",
    unsafe_allow_html=True)
    but3=st.button("Improve your existing idea")
    if but3:
        pass

def shareidea():
  st.title("Share your Idea")

  # Check if username is available in session state
  if "username" in session_state:
    username = session_state["username"]

    # Read ideators.csv
    try:
      df = pd.read_csv("ideators.csv")
    except FileNotFoundError:
      st.error("Error: 'ideators.csv' not found. Please create the file.")
      return

    # Authenticate username (assuming password column exists)
    if username not in df["username"].tolist():
      st.error("Invalid username. Please check your credentials.")
      return

    # Text box for entering the idea
    idea = st.text_area("Enter your idea here:")

    # File uploader for uploading files
    uploaded_file = st.file_uploader("Upload supporting files (if any):", type=["pdf", "txt", "jpg", "png"])

    # Submit button
    if st.button("Submit"):
      # Code to handle idea submission

      # Check if idea is entered
      if not idea:
        st.error("Please enter your idea.")
        return

      # Check if "idea" column exists
      if "idea" not in df.columns:
        df["idea"] = ""  # Create the new column

      # Update idea for the username
      df.loc[df["username"] == username, "idea"] = idea

      # Save the updated DataFrame to CSV
      try:
        df.to_csv("ideators.csv", index=False)
        st.success("Idea submitted successfully!")
      except Exception as e:
        st.error(f"Error saving idea: {e}")

      # Handle uploaded file (optional)
      if uploaded_file:
        # Implement logic to save the uploaded file (e.g., with a unique filename)
        # You can use libraries like os for file manipulation
        st.success("File uploaded successfully!")

  else:
    st.info("Please login as an Ideator first.")

 
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    if st.session_state['page'] == 'home':
        home_page()
    elif st.session_state['page'] == 'ideatorlogin':
        ideatorlogin()
    elif st.session_state['page'] == 'ideatorsignup':
        ideatorsignup()
    elif st.session_state['page'] == 'ideate':
        ideate()
    elif st.session_state['page'] == 'investorlogin':
        investorlogin()
    elif st.session_state['page'] == 'investorsignup':
        investorsignup()
    elif st.session_state['page'] == 'shareidea':
        shareidea()

if __name__== "__main__":
    main()