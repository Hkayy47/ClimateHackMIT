import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize session state variables
def init_config():
    if 'buildings_data' not in st.session_state:
        # Mock data for buildings
        st.session_state.buildings_data = pd.DataFrame({
            'name': ['SUStain'],
            'address': ['sus aven'],
            'area_sqft': [690],
            'annual_emissions': [30],
            'energy_usage': [20],
            'rating': ['5'],
            'latitude': [42.3601],
            'longitude': [71.0589],
            'credits_available': [40],
            'price_per_credit': [20.5]
        })

    if 'offset_projects' not in st.session_state:
        # Mock data for offset projects
        st.session_state.offset_projects = pd.DataFrame({
            'name': [''],
            'credits_available': [''],
            'price_per_credit': [''],
            'location': [''],
            'type': [''],
            'verification': ['']
        })

    # Configure page settings
    st.set_page_config(page_title="BuildingEcoViz - Building Emissions Management", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")
