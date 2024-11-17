import streamlit as st
from config import init_config
from home import display_home
from emissions_trading import display_emissions_trading
from energy_consultation import display_energy_consultation


# Initialize app configurations
init_config()

# Create the layout
nav_col, content_col = st.columns([1, 8])

with nav_col:
    st.image("logo.png", use_container_width=True)  # Adjust 'use_column_width' as needed
    st.write("---")
    selected_page = st.radio(
        
        "Navigation",
        ["Home", "Emissions Trading", "Energy Consultation"],
        label_visibility="collapsed"
    )

with content_col:
    if selected_page == "Home":
        display_home()
    elif selected_page == "Emissions Trading":
        display_emissions_trading()
    elif selected_page == "Energy Consultation":
        display_energy_consultation()
    
