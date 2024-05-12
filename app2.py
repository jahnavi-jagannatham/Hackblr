import streamlit as st
from pathlib import Path
import base64
import os
import pandas as pd
from streamlit import session_state
import subprocess
import numpy as np

def login():
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

    st.title("LOGIN AS :blue[INVESTOR]")
    username = st.text_input("USER NAME")
    session_state["investorname"] = username
    password = st.text_input("PASSWORD",type="password")
    login= st.button("LOG IN")
    if login:
        if authenticate_user(username, password):
            st.session_state['page'] = 'invest'
        else:
            st.error("Invalid username or password.")
 
    st.write("<div style='text-align: center;'><p style='font-size: 24px;'>New  user ? Dont have  an  account</p> </div>", unsafe_allow_html=True)
    col1,col2,col3=st.columns([2,2,1])
    signup=col2.button("SIGN UP")
    if signup:
        st.session_state['page'] = 'signup'

def signup_page():
    if st.button("Back to Login"):
        st.session_state['page'] = 'login'

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

    st.title("Sign Up as Investor")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

     # Add a selection box for choosing an investment domain
    investment_domain = st.multiselect(
        "Select the domain you are interested in investing:",
        ('AI', 'Blockchain', 'Cyber Security', 'Sustainability', 'E-Commerce' ,'Healthcare')
    )
    

    if st.button("Create Account"):
        # Pass the investment domain to the add_investor function
        add_user(new_username, new_password, investment_domain)
        st.session_state['page'] = 'login'


# Function to add a new user to CSV
def add_user(username, password, domain):
    # Create a DataFrame with the username, password, and domain
    df = pd.DataFrame({
        'username': [username], 
        'password': [password], 
        'domain': [', '.join(domain)]  # Join the list into a comma-separated string
    })
    # Append the new investor data to the CSV file
    df.to_csv('users.csv', mode='a', header=False, index=False)

# Function to authenticate user
def authenticate_user(username, password):
    df = pd.read_csv('users.csv')
    #hashed_password = hash_password(password)
    if ((df['username'] == username) & (df['password'] == password)).any():
        return True
    else:
        return False

def invest():
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

    st.title("Invest")
    if "investorname" in session_state:
        username = session_state["investorname"]
    st.write(f"<span style='font-size: 24px; font-family: \"Comic Sans MS\", cursive, sans-serif'>Welcome, {username}!</span>", unsafe_allow_html=True)
    st.markdown("<p style='color: lightblue; font-size: 20px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Look at the innovative ideas!""</p>",
    unsafe_allow_html=True)
    but1=st.button("Ideas")
    if but1:
        st.session_state['page'] = 'ideas'
    st.markdown("<p style='color: lightblue; font-size: 20px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Look at the ideas which you liked""</p>",
    unsafe_allow_html=True)
    but2=st.button("Liked Ideas")
    if but2:
        st.session_state['page'] = 'likedideas'
    st.markdown("<p style='color: lightblue; font-size: 20px; font-family: \"Comic Sans MS\", cursive, sans-serif; max-width: fit-content;'>""Chat with ideators""</p>",
    unsafe_allow_html=True)
    but3=st.button("Chat")
    if but3:
        st.session_state['page'] = 'chat'

def ideas():
    if st.button("Back"):
        st.session_state['page'] = 'invest'
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
  
    st.title("These are the ideas presented by our ideators")

    try:
        # Read CSV data into a Pandas DataFrame
        df_ideators = pd.read_csv("ideators.csv")
        df_users = pd.read_csv("users.csv")

        # Filter rows with non-empty 'idea' values
        df_filtered_ideas = df_ideators[df_ideators['idea'].notna()] 

        # Get the domain of the logged-in investor
        investorname = st.session_state["investorname"]
        investor_domain = df_users.loc[df_users['username'] == investorname, 'domain'].iloc[0]

        # Display ideas and usernames in a loop with formatting
        for index, row in df_filtered_ideas.iterrows():
            ideator_domain = row["domain"]
            if ideator_domain == investor_domain:
                username = row["username"]
                idea = row["idea"]

                # Create button with username as label
                review_button = st.button(username)

                # Handle button click (if clicked)
                if review_button:
                    session_state["ideatorname"] = username
                    st.session_state['page'] = 'idea_page'
                    # Navigate to the "idea" page with username as query parameter

                # Display username and idea with formatting
                st.write(f"<div style='border-bottom: 1px solid lightgray; padding-bottom: 10px; margin-bottom: 10px;'>**{username}** - {idea}</div>", unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("Error: 'ideators.csv' or 'users.csv' file not found. Please ensure the files exist.")

def idea_page():
    if st.button("Back"):
        st.session_state['page'] = 'invest'
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

    ideatorname = st.session_state["ideatorname"]

    st.title(f"{ideatorname}'s Idea")
    
    # Read ideators.csv to get user's idea
    df_ideas = pd.read_csv('ideators.csv')
    
    # Filter the dataframe for the user's idea
    user_idea = df_ideas[df_ideas['username'] == ideatorname]['idea'].values

    # Check if user has provided an idea
    if len(user_idea) > 0:
        st.write("Your idea: ", user_idea[0])
    else:
        st.write("You haven't provided any idea yet.")

    video_filename = f"{ideatorname}.mp4"
    if os.path.isfile(video_filename):
        st.video(video_filename)
    else:
        st.write(f"No video found for {ideatorname}")

    
    like_button = st.button("Like Idea")

    if like_button:
        # Read investors.csv
        df_investors = pd.read_csv('users.csv')
        
        # Check if 'liked-ideas' column exists, if not create it
        if 'liked-ideas' not in df_investors.columns:
            df_investors['liked-ideas'] = ''
        
        # Update 'liked-ideas' for the corresponding investor
        investorname = st.session_state["investorname"]
        idx = df_investors[df_investors['username'] == investorname].index
        
        if not idx.empty:
            current_likes = df_investors.loc[idx[0], 'liked-ideas']
            ideatorname = str(ideatorname)  # Ensure ideatorname is a string
            if current_likes:
                current_likes = str(current_likes)  # Ensure current_likes is a string
                df_investors.at[idx[0], 'liked-ideas'] = current_likes + ',' + ideatorname
            else:
                df_investors.at[idx[0], 'liked-ideas'] = ideatorname
        
        # Save the updated dataframe back to investors.csv
        df_investors.to_csv('users.csv', index=False)

    review_text = st.text_area("Write your review here:")
    
    # Text field to score the idea out of 5
    idea_score = st.number_input("Rate the idea out of 5:", min_value=1, max_value=5)
    
    # Button to submit review and score
    if st.button("Submit Review and Score"):
        # Read ideators.csv
        df_ideators = pd.read_csv('ideators.csv')
        
        # Check if 'reviews' column exists, if not create it
        if 'reviews' not in df_ideators.columns:
            df_ideators['reviews'] = ''
        
        # Check if 'scores' column exists, if not create it
        if 'scores' not in df_ideators.columns:
            df_ideators['scores'] = ''
        
        # Update 'reviews' for the corresponding ideator
        idx = df_ideators[df_ideators['username'] == ideatorname].index
        
        if not idx.empty:
            current_reviews = df_ideators.loc[idx[0], 'reviews']
            if current_reviews:
                df_ideators.at[idx[0], 'reviews'] += f',{review_text}'
            else:
                df_ideators.at[idx[0], 'reviews'] = review_text
            
            # Update 'scores' for the corresponding ideator
            current_scores = df_ideators.loc[idx[0], 'scores']
            if current_scores:
                df_ideators.at[idx[0], 'scores'] += f',{idea_score}'
            else:
                df_ideators.at[idx[0], 'scores'] = idea_score
        
        # Save the updated dataframe back to ideators.csv
        df_ideators.to_csv('ideators.csv', index=False)
        st.success("Review and score submitted successfully!")

def likedideas():
    if st.button("Back"):
        st.session_state['page'] = 'invest'
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

    st.title("These are the ideas which you've liked")

    investorname = st.session_state["investorname"]
    
    # Read investors.csv to get liked ideas
    df_investors = pd.read_csv('users.csv')
    
    # Filter the dataframe for the investor's liked ideas
    liked_ideas = df_investors[df_investors['username'] == investorname]['liked-ideas'].values
    
    if len(liked_ideas) > 0:
        # Split the liked_ideas string into a list of ideator usernames
        liked_ideas_list = liked_ideas[0].split(',')
        
        # Read ideators.csv
        df_ideators = pd.read_csv('ideators.csv')
        
        # Filter the dataframe for the liked ideas
        liked_ideas_df = df_ideators[df_ideators['username'].isin(liked_ideas_list)]
        
        if not liked_ideas_df.empty:
            st.write("Ideas liked by", investorname)
            for index, row in liked_ideas_df.iterrows():
                st.write("Ideator:", row['username'])
                st.write("Idea:", row['idea'])
                st.write("---")
        else:
            st.write("No ideas liked by", investorname)
    else:
        st.write("No ideas liked by", investorname)

    st.write("Check market-value of the idea using our AI-powered bot")
    bot=st.button("Check market-value:")
    if bot:
        subprocess.Popen(["streamlit", "run", "assessbot.py"])


def chat():
    if st.button("Back "):
        st.session_state['page'] = 'invest'
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

    st.title("Chat with the ideators")

    df_ideators = pd.read_csv('ideators.csv')
    unique_ideator_names = set(df_ideators['username'])

    # Display buttons for each unique ideator
    for ideatorname in unique_ideator_names:
        if st.button(ideatorname):
            st.session_state['ideatorname']=ideatorname
            # If button clicked, navigate to chat page for the selected ideator
            st.session_state['page'] = 'chatideator'

import os
import streamlit as st
import pandas as pd
from datetime import datetime

import os
import pandas as pd
from datetime import datetime
import streamlit as st

def chat_with_ideator():
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
    # Handle back button
    back = st.button("Back")
    if back:
        st.session_state['page'] = 'chat'

    # Retrieve ideatorname and investorname from session state
    ideatorname = st.session_state['ideatorname']
    investorname = st.session_state['investorname']
    st.title(f"Chat with {ideatorname}")

    # Load existing chats or create a new DataFrame
    if os.path.isfile('chats.csv'):
        df_chats = pd.read_csv('chats.csv')
    else:
        df_chats = pd.DataFrame(columns=['from', 'to', 'chat', 'timestamp'])

    # Filter existing chats between the investor and ideator
    chats_ideator_to_investor = df_chats[(df_chats['from'] == ideatorname) & (df_chats['to'] == investorname)]
    chats_investor_to_ideator = df_chats[(df_chats['from'] == investorname) & (df_chats['to'] == ideatorname)]

    # Combine both sets of chats
    all_chats = pd.concat([chats_ideator_to_investor, chats_investor_to_ideator], ignore_index=True)

    # Sort combined chats by timestamp in ascending order
    all_chats = all_chats.sort_values(by='timestamp', ascending=True)

    # Display combined chats
    for index, row in all_chats.iterrows():
        if row['from'] == ideatorname:
            st.write(f"{ideatorname}: {row['chat']}")
        else:
            st.write(f"{investorname}: {row['chat']}")

    # Textbox for new chat
    new_chat = st.text_input("Your message:")
    send_button = st.button("Send")

    if send_button and new_chat.strip():
        # Get the current timestamp
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append new chat to DataFrame
        new_row = pd.DataFrame({'from': [investorname], 'to': [ideatorname], 'chat': [new_chat], 'timestamp': [current_timestamp]})
        df_chats = pd.concat([df_chats, new_row], ignore_index=True)

        # Save updated chats
        df_chats.to_csv('chats.csv', index=False)

        # Clear the text input
        new_chat = ''
    
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['page'] == 'login':
        login()
    elif st.session_state['page'] == 'signup':
        signup_page()
    elif st.session_state['page']=='invest':
        invest()
    elif st.session_state['page']=='ideas':
        ideas()
    elif st.session_state['page']=='likedideas':
        likedideas()
    elif st.session_state['page']=='chat':
        chat()
    elif st.session_state['page']=='idea_page':
        idea_page()
    elif st.session_state['page']=='chatideator':
        chat_with_ideator()
    

if __name__== "__main__":
    main()