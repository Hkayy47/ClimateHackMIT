import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import google.generativeai as genai
import folium
from streamlit_folium import st_folium
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Configure page settings
st.set_page_config(page_title="BuildingEcoViz - Building Emissions Management", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state variables
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
st.markdown("""
    <style>
        .main {
            background-color: #1E1E1E;
            color: white;
        }
        .stRadio > label {
            color: white;
            font-weight: bold;
        }
        .stMetric {
            background-color: #2D2D2D;
            padding: 10px;
            border-radius: 5px;
        }
        div[data-testid="stHorizontalBlock"] {
            gap: 2rem;
            padding: 1rem 0;
        }
        div[data-testid="stImage"] {
            padding: 1rem 0;
        }
        hr {
            margin: 2rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Create the main layout with adjusted ratios
nav_col, content_col = st.columns([1.2, 5])
# Create two columns for the layout
nav_col, content_col = st.columns([1, 8])

with nav_col:
    # Logo at the top
    st.image("logo.png", use_column_width=True)
    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
        
    # Navigation menu with custom styling
    st.markdown("""
        <style>
            div[role="radiogroup"] > div {
                margin: 1rem 0;
                padding: 0.5rem;
                border-radius: 5px;
            }
            div[role="radiogroup"] > div:hover {
                background-color: #2D2D2D;
            }
        </style>
    """, unsafe_allow_html=True)
    
    selected_page = st.radio(
        "Navigation",
        ["Home", "Emissions Trading", "Offset Projects", "Energy Consultation", "Add Building"],
        label_visibility="collapsed"
    )

# Main content column
with content_col:
    if selected_page == "Home":
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Buildings Analyzed", len(st.session_state.buildings_data))
        with col2:
            avg_emissions = st.session_state.buildings_data['annual_emissions'].mean()
            st.metric("Average Emissions", f"{avg_emissions/1000:.1f} tons CO2e")
        with col3:
            best_building = st.session_state.buildings_data.loc[st.session_state.buildings_data['annual_emissions'].idxmin()]
            st.metric("Best Performer", f"{best_building['name']}")
        with col4:
            total_credits = st.session_state.buildings_data['credits_available'].sum()
            st.metric("Available Credits", f"{total_credits:,} tons CO2e")

        # Emissions comparison chart
        st.subheader("Emissions Comparison")
        fig = px.bar(st.session_state.buildings_data,
                    x='name', y='annual_emissions',
                    color='rating',
                    labels={'name': 'Building Name', 'annual_emissions': 'Annual Emissions (kg CO2e)'},
                    title='Building Emissions Comparison')
        st.plotly_chart(fig, use_container_width=True)

        # Map view
        st.subheader("Geographic Distribution")
        m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)
        for idx, row in st.session_state.buildings_data.iterrows():
            color = 'green' if row['rating'] == 'A' else 'orange' if row['rating'] == 'B' else 'red'
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=10,
                popup=f"{row['name']}<br>Emissions: {row['annual_emissions']:,} kg CO2e<br>Rating: {row['rating']}",
                color=color,
                fill=True
            ).add_to(m)
        st_folium(m, width=800, height=400)

    elif selected_page == "Emissions Trading":
        st.header("Carbon Credits Trading")
        
        sellers_df = st.session_state.buildings_data[
            st.session_state.buildings_data['credits_available'] > 0
        ][['name', 'credits_available', 'price_per_credit']]
        
        if not sellers_df.empty:
            st.subheader("Available Credits")
            st.dataframe(sellers_df)
            
            # Credit purchase form
            st.subheader("Purchase Credits")
            buyer = st.selectbox("Select Your Building", options=st.session_state.buildings_data['name'])
            seller = st.selectbox("Select Seller", options=sellers_df['name'])
            credits_to_buy = st.number_input(
                "Number of Credits to Purchase",
                min_value=1,
                max_value=int(sellers_df[sellers_df['name'] == seller]['credits_available'].iloc[0])
            )
            
            if st.button("Purchase Credits"):
                st.success(f"Successfully purchased {credits_to_buy:,} credits from {seller}")

    elif selected_page == "Offset Projects":
        st.header("Offset Projects")
        
        # Project filters
        col1, col2 = st.columns(2)
        with col1:
            project_type = st.multiselect(
                "Project Type",
                options=st.session_state.offset_projects['type'].unique(),
                default=st.session_state.offset_projects['type'].unique()
            )
        with col2:
            verification = st.multiselect(
                "Verification Standard",
                options=st.session_state.offset_projects['verification'].unique(),
                default=st.session_state.offset_projects['verification'].unique()
            )
        
        filtered_projects = st.session_state.offset_projects[
            (st.session_state.offset_projects['type'].isin(project_type)) &
            (st.session_state.offset_projects['verification'].isin(verification))
        ]
        
        for idx, project in filtered_projects.iterrows():
            with st.expander(f"{project['name']} - {project['credits_available']:,} credits available"):
                cols = st.columns(2)
                with cols[0]:
                    st.write(f"**Location:** {project['location']}")
                    st.write(f"**Type:** {project['type']}")
                    st.write(f"**Verification:** {project['verification']}")
                with cols[1]:
                    st.write(f"**Price per Credit:** ${project['price_per_credit']}")
                    st.write(f"**Total Credits:** {project['credits_available']:,}")
                    credits_wanted = st.number_input(
                        "Credits to Purchase",
                        key=f"purchase_{idx}",
                        min_value=0,
                        max_value=project['credits_available']
                    )
                    if st.button("Purchase Credits", key=f"button_{idx}"):
                        st.success(f"Successfully purchased {credits_wanted:,} credits")

    elif selected_page == "Energy Consultation":
        st.header("Energy Consultation")
        
        building_name = st.selectbox(
            "Select Your Building",
            options=st.session_state.buildings_data['name'].tolist(),
            key="consultation_building"
        )
        
        usage_description = st.text_area(
            "Describe energy usage patterns and concerns",
            height=150,
            placeholder="Example: Our office building operates Monday-Friday, 8am-6pm..."
        )
        
        if st.button("Get Recommendations") and usage_description:
            with st.spinner("Analyzing building data..."):
                recommendations = get_energy_recommendations(
                    building_name,
                    st.session_state.buildings_data,
                    usage_description
                )
                if recommendations:
                    st.success("Analysis complete!")
                    st.markdown(recommendations)
                    st.download_button(
                        "Download Recommendations",
                        data=recommendations,
                        file_name=f"energy_recommendations_{building_name}.md",
                        mime="text/markdown"
                    )

    elif selected_page == "Add Building":
        st.header("Add New Building")
        
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Building Name")
            new_address = st.text_input("Address")
            new_area = st.number_input("Building Area (sq ft)", min_value=0)
            new_emissions = st.number_input("Annual Emissions (kg CO2e)", min_value=0)
            new_energy = st.number_input("Annual Energy Usage (kWh)", min_value=0)
        
        with col2:
            new_rating = st.selectbox("Energy Rating", options=['A', 'B', 'C'])
            new_lat = st.number_input("Latitude", value=40.7128)
            new_lon = st.number_input("Longitude", value=-74.0060)
            new_credits = st.number_input("Available Carbon Credits", min_value=0)
            new_credit_price = st.number_input("Credit Price (USD)", min_value=0)
        
        if st.button("Add Building"):
            new_building = pd.DataFrame({
                'name': [new_name],
                'address': [new_address],
                'area_sqft': [new_area],
                'annual_emissions': [new_emissions],
                'energy_usage': [new_energy],
                'rating': [new_rating],
                'latitude': [new_lat],
                'longitude': [new_lon],
                'credits_available': [new_credits],
                'price_per_credit': [new_credit_price]
            })
            st.session_state.buildings_data = pd.concat(
                [st.session_state.buildings_data, new_building],
                ignore_index=True
            )
            st.success("Building added successfully!")