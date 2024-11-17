import streamlit as st
import pandas as pd
import google.generativeai as genai
# config.py
EI_API_KEY = "your_api_key_here"

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize session state variables
def init_config():
    if 'buildings_data' not in st.session_state:
        # Mock data for buildings
        st.session_state.buildings_data = pd.DataFrame({
            
        })

    if 'offset_projects' not in st.session_state:
        # Mock data for offset projects
        st.session_state.offset_projects = pd.DataFrame({
           
        })

    # Configure page settings
    st.set_page_config(page_title="BuildingEcoViz - Building Emissions Management", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")
