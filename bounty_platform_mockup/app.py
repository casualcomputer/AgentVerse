import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Bounty Platform Mockup", page_icon="🏆", layout="wide")

# --- Mock User Store (in-memory for demo) ---
if 'users' not in st.session_state:
    st.session_state['users'] = []  # List of dicts: {username, email, password, role}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# --- Registration & Login Workflow ---
def register_user():
    st.subheader("Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Register as", ["Poster (Company)", "Builder (AI Engineer)"])
        submit = st.form_submit_button("Register")
        if submit:
            if not username or not email or not password:
                st.error("All fields are required.")
            elif any(u['username'] == username for u in st.session_state['users']):
                st.error("Username already exists.")
            else:
                st.session_state['users'].append({
                    'username': username,
                    'email': email,
                    'password': password,
                    'role': role.split()[0].lower()  # 'poster' or 'builder'
                })
                st.success("Registration successful! Please log in.")
                st.session_state['show_register'] = False

def login_user():
    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login")
        if submit:
            user = next((u for u in st.session_state['users'] if u['username'] == username and u['password'] == password), None)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = user
                st.success(f"Welcome, {user['username']}! You are logged in as a {user['role']}.")
            else:
                st.error("Invalid username or password.")

# --- Onboarding Page ---
def onboarding():
    st.title("Welcome to the Bounty Platform Mockup")
    st.write("Register or log in to get started.")
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            st.session_state['show_register'] = True
    with col2:
        if st.button("Login"):
            st.session_state['show_register'] = False
    if st.session_state['show_register']:
        register_user()
    else:
        login_user()

# --- Logout ---
def logout():
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None
    st.session_state['show_register'] = False
    st.success("Logged out.")

# --- Main App ---
def main_app():
    user = st.session_state['current_user']
    st.sidebar.title("Bounty Platform")
    st.sidebar.markdown(f"**Logged in as:** {user['username']} ({user['role'].capitalize()})")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()
    st.sidebar.markdown("---")
    st.sidebar.info("This is a mockup demo. No real data is stored.")

    # --- Tabs ---
    tabs = st.tabs(["🏢 Post Bounty", "🧑‍💻 Join & Submit", "🏅 Leaderboard", "⭐ Social Score"])

    # --- Mock Data ---
    mock_bounties = [
        {"Title": "Titanic Survival Predictor", "Reward": 500, "Deadline": "2024-06-30", "Status": "Open", "Requirements": "scikit-learn, pandas", "Dataset": "Titanic.csv"},
        {"Title": "Chatbot for Customer Support", "Reward": 800, "Deadline": "2024-07-15", "Status": "Open", "Requirements": "transformers, torch", "Dataset": "SupportChats.json"},
    ]
    mock_leaderboard = [
        {"Bounty": "Titanic Survival Predictor", "Winner": "@alice", "Score": 0.87, "Reward": 500},
        {"Bounty": "Chatbot for Customer Support", "Winner": "@bob", "Score": 0.92, "Reward": 800},
    ]
    mock_social = [
        {"User": "@alice", "Score": 98, "Penalties": 0, "Completed": 3},
        {"User": "@bob", "Score": 85, "Penalties": 1, "Completed": 2},
        {"User": "@charlie", "Score": 60, "Penalties": 2, "Completed": 1},
    ]

    # --- Post Bounty Tab ---
    with tabs[0]:
        st.header("🏢 Post a New Bounty")
        if user['role'] != 'poster':
            st.warning("Only Posters (companies) can post bounties.")
        else:
            st.write("Companies can post new bounties for AI agents, specify requirements, upload datasets, and set rewards.")
            with st.form("post_bounty_form"):
                title = st.text_input("Bounty Title", "Titanic Survival Predictor")
                description = st.text_area("Description", "Build an agent to predict Titanic survival.")
                requirements = st.text_input("Dependency Requirements (comma-separated)", "scikit-learn, pandas")
                dataset = st.file_uploader("Upload Dataset (CSV, JSON, etc.)")
                example_data = st.text_area("Example Input/Output", "{'Pclass': 3, 'Sex': 'male', ...} -> 0 (not survived)")
                reward = st.number_input("Reward (tokens)", min_value=100, value=500, step=50)
                deadline = st.date_input("Deadline", datetime(2024, 6, 30))
                submitted = st.form_submit_button("Post Bounty")
                if submitted:
                    st.success(f"Bounty '{title}' posted! (mockup)")
            st.markdown("---")
            st.subheader("Open Bounties")
            st.dataframe(pd.DataFrame(mock_bounties))

    # --- Join & Submit Tab ---
    with tabs[1]:
        st.header("🧑‍💻 Join a Bounty & Submit Solution")
        if user['role'] != 'builder':
            st.warning("Only Builders (AI engineers) can join and submit solutions.")
        else:
            st.write("AI engineers can join open bounties, download datasets, and submit their solutions.")
            st.markdown("---")
            st.subheader("Available Bounties")
            st.dataframe(pd.DataFrame(mock_bounties))
            st.markdown("---")
            st.subheader("Submit Solution (mockup)")
            with st.form("submit_solution_form"):
                bounty = st.selectbox("Select Bounty", [b["Title"] for b in mock_bounties])
                username = st.text_input("Your Username", user['username'])
                code = st.file_uploader("Upload Code (zip, py, etc.)")
                notes = st.text_area("Notes/Description")
                submit = st.form_submit_button("Submit Solution")
                if submit:
                    st.success(f"Solution for '{bounty}' submitted by {username}! (mockup)")

    # --- Leaderboard Tab ---
    with tabs[2]:
        st.header("🏅 Leaderboard & Rewards")
        st.write("See the top solutions and reward winners for each bounty.")
        st.dataframe(pd.DataFrame(mock_leaderboard))

    # --- Social Score Tab ---
    with tabs[3]:
        st.header("⭐ Social Score & Penalties")
        st.write("Track your reputation, completed bounties, and any penalties.")
        st.dataframe(pd.DataFrame(mock_social))
        st.info("Low social scores or repeated no-shows may restrict access to high-value bounties.")

# --- App Routing ---
if not st.session_state['logged_in']:
    onboarding()
else:
    main_app() 