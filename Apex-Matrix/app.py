import streamlit as st
import requests

# --- AUTHENTICATION CONFIGURATION ---
# Change this to your desired master password or load it from environment secrets
MASTER_PASSWORD = "ApexSecure2026!"

def check_password():
    """Returns True if the user entered the correct password."""
    def password_entered():
        if st.session_state["password"] == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password in session state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Enter Master Passcode to Access Apex Matrix", 
            type="password", 
            key="password", 
            on_change=password_entered
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input(
            "Enter Master Passcode to Access Apex Matrix", 
            type="password", 
            key="password", 
            on_change=password_entered
        >
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

# Run the authentication check
if not check_password():
    st.stop() # Halts script execution here if not logged in

# ==========================================
# YOUR REST OF STREAMLIT DASHBOARD CODE BELOW
# ==========================================
st.set_page_config(page_title="Apex HVII Matrix", layout="wide")
st.title("Apex Real Estate Evaluation Matrix")
st.markdown("Enter property financials to generate a Presidential-Tier HVII Score.")

# ... [Rest of your sidebar, inputs, and API request logic] ...
            st.error("Invalid API Key or Server Error.")
