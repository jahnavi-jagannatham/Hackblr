import streamlit as st
from pathlib import Path
import base64
import os
import pandas as pd
from streamlit import session_state
def ideate():
    st.title("Ideate ")
    st.markdown("<p style='color: lightblue; font-size: 25px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Do you've your idea and working model ready?""</p>",
    unsafe_allow_html=True)
    st.markdown("<p style='color: white; font-size: 25px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Don't wait anymore, start pitching your idea!""</p>",
    unsafe_allow_html=True)
    but1=st.button("Share a New Idea")
    if but1:
        st.session_state['page'] = 'shareidea'

    st.markdown("<p style='color: lightblue; font-size: 25px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Have an idea but don't know how to build a prototype?""</p>",
    unsafe_allow_html=True)
    st.markdown("<p style='color: white; font-size: 25px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""We've got your back, build prototype with the help of our AI""</p>",
    unsafe_allow_html=True)
    but2=st.button("Develop a prototype")
    if but2:
        pass
    st.markdown("<p style='color: lightblue; font-size: 25px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Not very sure about your idea?""</p>",
    unsafe_allow_html=True)
    st.markdown("<p style='color: white; font-size: 25px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""No worries, our AI-powered bot will help you to improve it!""</p>",
    unsafe_allow_html=True)
    but3=st.button("Improve your existing idea")
    if but3:
        pass
    st.markdown("<p style='color: lightblue; font-size: 25px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Already submitted your idea? Check your idea status:""</p>",
    unsafe_allow_html=True)
    but4=st.button("Check status")
    if but4:
        pass

import streamlit as st

import pandas as pd

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
        st.session_state['page'] = 'ideate'

    if st.session_state['page'] == 'ideate':
        ideate()
    elif st.session_state['page'] == 'shareidea':
        shareidea()

if __name__== "__main__":
    main()
