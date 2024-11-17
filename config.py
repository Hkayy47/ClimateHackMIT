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
            'name': ['Tech Plaza', 'Green Tower', 'Downtown Office', 'Innovation Hub', 'Central Building'],
            'address': ['123 Tech St', '456 Green Ave', '789 Main St', '321 Innovation Rd', '654 Central Blvd'],
            'area_sqft': [50000, 75000, 60000, 40000, 55000],
            'annual_emissions': [75000, 45000, 95000, 65000, 85000],
            'energy_usage': [250000, 180000, 320000, 220000, 280000],
            'rating': ['B', 'A', 'C', 'B', 'C'],
            'latitude': [40.7128, 40.7139, 40.7118, 40.7108, 40.7148],
            'longitude': [-74.0060, -74.0070, -74.0050, -74.0040, -74.0080],
            'credits_available': [0, 15000, 0, 5000, 0],
            'price_per_credit': [0, 25, 0, 22, 0]
        })

    if 'offset_projects' not in st.session_state:
        # Mock data for offset projects
        st.session_state.offset_projects = pd.DataFrame({
            'name': ['Forest Restoration', 'Solar Farm', 'Wind Energy', 'Methane Capture'],
            'credits_available': [50000, 75000, 60000, 40000],
            'price_per_credit': [20, 18, 22, 15],
            'location': ['Amazon', 'Nevada', 'Texas', 'California'],
            'type': ['Forestry', 'Renewable Energy', 'Renewable Energy', 'Industrial'],
            'verification': ['Gold Standard', 'VCS', 'VCS', 'Gold Standard']
        })

    # Configure page settings
    st.set_page_config(page_title="BuildingEcoViz - Building Emissions Management", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")
