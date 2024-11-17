import streamlit as st
from config import init_config
from pages.home import display_home
from pages.emissions_trading import display_emissions_trading
from pages.offset_projects import display_offset_projects
from pages.energy_consultation import display_energy_consultation
from pages.add_building import display_add_building

# Initialize app configurations
init_config()

# Create the layout
nav_col, content_col = st.columns([1, 8])

with nav_col:
    selected_page = st.radio(
        "Navigation",
        ["Home", "Emissions Trading", "Offset Projects", "Energy Consultation", "Add Building"],
        label_visibility="collapsed"
    )

with content_col:
    if selected_page == "Home":
        display_home()
    elif selected_page == "Emissions Trading":
        display_emissions_trading()
    elif selected_page == "Offset Projects":
        display_offset_projects()
    elif selected_page == "Energy Consultation":
        display_energy_consultation()
    elif selected_page == "Add Building":
        display_add_building()
