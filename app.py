import streamlit as st
from config import init_config
from pages.home import display_home
from pages.emissions_trading import display_emissions_trading
from pages.offset_projects import display_offset_projects
from pages.energy_consultation import display_energy_consultation
from pages.add_building import display_add_building

# Initialize app configurations
init_config()

# Custom CSS for left-aligned navigation and styling
st.markdown("""
    <style>
        /* Hide default sidebar styling */
        .css-1d391kg {
            padding-top: 0;
        }
        
        /* Left sidebar styling */
        section[data-testid="stSidebar"] {
            width: 15rem !important;
            background-color: #1E1E1E;
            padding: 0;
        }
        
        /* Logo container */
        .logo-container {
            padding: 1rem;
            background-color: #1E1E1E;
            margin: 0;
            width: 100%;
        }
        
        /* Navigation styling */
        .nav-container {
            padding: 1rem 0;
        }
        
        /* Radio button styling */
        div[role="radiogroup"] > div {
            padding: 0.5rem 1rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        div[role="radiogroup"] > div:hover {
            background-color: #2D2D2D;
        }
        
        /* Hide default radio button */
        div[role="radiogroup"] input[type="radio"] {
            display: none;
        }
        
        /* Main content area */
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: none;
        }
        
        /* Metrics styling */
        div[data-testid="metric-container"] {
            background-color: #2D2D2D;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        div[data-testid="metric-container"] label {
            color: #B0B0B0 !important;
        }
        
        div[data-testid="metric-container"] div {
            color: white !important;
        }
        
        /* Chart container */
        div[data-testid="stPlotlyChart"] {
            background-color: #2D2D2D;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        hr {
            margin: 0;
            border-color: #333;
        }
    </style>
""", unsafe_allow_html=True)



# Create the layout
nav_col, content_col = st.columns([1, 8])

with nav_col:
    # Navigation section
    st.image("logo.png", use_column_width=True)
    st.markdown("---")
    
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
