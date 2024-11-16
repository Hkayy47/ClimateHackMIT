import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import openai  # For LLM integration
import folium
from streamlit_folium import st_folium

# Configure page settings
st.set_page_config(page_title="BuildingEcoViz - Building Emissions Management", page_icon="🏢", layout="wide")

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
        'credits_available': [0, 15000, 0, 5000, 0],  # Carbon credits available for trading
        'price_per_credit': [0, 25, 0, 22, 0]  # Price per carbon credit in USD
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

# Title and description
st.title("BuildingEcoViz - Commercial Building Emissions Management")
st.write("Compare, analyze, and offset carbon emissions for commercial buildings")

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Building Comparison", 
    "Emissions Trading", 
    "Offset Projects",
    "Energy Consultation",
    "Add Building"
])

with tab1:
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
                 x='name',
                 y='annual_emissions',
                 color='rating',
                 labels={'name': 'Building Name',
                        'annual_emissions': 'Annual Emissions (kg CO2e)'},
                 title='Building Emissions Comparison')
    st.plotly_chart(fig, use_container_width=True)

    # Efficiency scatter plot
    st.subheader("Emissions Efficiency")
    fig = px.scatter(st.session_state.buildings_data,
                    x='area_sqft',
                    y='annual_emissions',
                    size='energy_usage',
                    color='rating',
                    hover_name='name',
                    labels={'area_sqft': 'Building Area (sq ft)',
                           'annual_emissions': 'Annual Emissions (kg CO2e)',
                           'energy_usage': 'Energy Usage (kWh)'},
                    title='Emissions vs Building Size')
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

with tab2:
    st.header("Carbon Credits Trading")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Available Credits for Purchase")
        sellers_df = st.session_state.buildings_data[
            st.session_state.buildings_data['credits_available'] > 0
        ][['name', 'credits_available', 'price_per_credit']]
        
        if not sellers_df.empty:
            st.dataframe(sellers_df)
            
            # Credit purchase form
            st.subheader("Purchase Credits")
            buyer = st.selectbox("Select Your Building", 
                               options=st.session_state.buildings_data['name'])
            seller = st.selectbox("Select Seller", 
                                options=sellers_df['name'])
            credits_to_buy = st.number_input("Number of Credits to Purchase", 
                                           min_value=1,
                                           max_value=int(sellers_df[
                                               sellers_df['name'] == seller
                                           ]['credits_available'].iloc[0]))
            
            if st.button("Purchase Credits"):
                st.success(f"Successfully purchased {credits_to_buy:,} credits from {seller}")
        else:
            st.write("No credits currently available for purchase")
    
    with col2:
        st.subheader("Credit Price Trends")
        # Mock price trend data
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
        prices = 20 + np.random.normal(0, 2, len(dates))
        
        fig = px.line(x=dates, y=prices,
                     labels={'x': 'Date', 'y': 'Credit Price (USD)'},
                     title='Carbon Credit Price History')
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Offset Projects")
    
    # Project filters
    col1, col2 = st.columns(2)
    with col1:
        project_type = st.multiselect("Project Type",
                                    options=st.session_state.offset_projects['type'].unique(),
                                    default=st.session_state.offset_projects['type'].unique())
    with col2:
        verification = st.multiselect("Verification Standard",
                                    options=st.session_state.offset_projects['verification'].unique(),
                                    default=st.session_state.offset_projects['verification'].unique())
    
    filtered_projects = st.session_state.offset_projects[
        (st.session_state.offset_projects['type'].isin(project_type)) &
        (st.session_state.offset_projects['verification'].isin(verification))
    ]
    
    # Display projects
    for idx, project in filtered_projects.iterrows():
        with st.expander(f"{project['name']} - {project['credits_available']:,} credits available"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Location:** {project['location']}")
                st.write(f"**Type:** {project['type']}")
                st.write(f"**Verification:** {project['verification']}")
            
            with col2:
                st.write(f"**Price per Credit:** ${project['price_per_credit']}")
                st.write(f"**Total Credits Available:** {project['credits_available']:,}")
                
                # Purchase form
                credits_wanted = st.number_input("Credits to Purchase",
                                               key=f"purchase_{idx}",
                                               min_value=0,
                                               max_value=project['credits_available'])
                if st.button("Purchase Credits", key=f"button_{idx}"):
                    st.success(f"Successfully purchased {credits_wanted:,} credits from {project['name']}")

with tab4:
    st.header("Energy Consultation")
    
    # Building selector
    building_name = st.selectbox(
        "Select Your Building",
        options=st.session_state.buildings_data['name'].tolist(),
        key="consultation_building"
    )
    
    # Energy usage description
    usage_description = st.text_area(
        "Describe your building's energy usage patterns and concerns",
        height=150,
        placeholder="Example: Our office building operates Monday-Friday, 8am-6pm. " +
        "We have central HVAC, fluorescent lighting throughout, and 50 workstations..."
    )
    
    if st.button("Get Recommendations") and usage_description:
        # Mock LLM response
        recommendations = """Based on your description, here are some recommendations:

1. HVAC Optimization:
   - Implement smart scheduling to reduce off-hours operation
   - Consider upgrading to a more efficient system
   
2. Lighting:
   - Replace fluorescent lights with LED fixtures
   - Install occupancy sensors in less-used areas
   
3. Workstations:
   - Enable power management settings on all computers
   - Install smart power strips to reduce phantom loads

Estimated potential savings: 15-20% reduction in energy usage."""

        st.success("Analysis complete!")
        st.write(recommendations)

with tab5:
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
        
        st.session_state.buildings_data = pd.concat([st.session_state.buildings_data, new_building],
                                                   ignore_index=True)
        st.success("Building added successfully!")

# Sidebar with additional information
with st.sidebar:
    st.header("About BuildingEcoViz")
    st.write("""
    BuildingEcoViz helps building owners and managers:
    - Compare their building's emissions with nearby properties
    - Trade carbon credits with other buildings
    - Purchase verified carbon offsets
    - Get AI-powered recommendations for energy efficiency
    - Track and analyze emissions over time
    - Meet sustainability reporting requirements
    """)
    
    st.header("Rating System")
    st.write("""
    **Rating A:** < 50 kg CO2e/sq ft/year
    **Rating B:** 50-75 kg CO2e/sq ft/year
    **Rating C:** > 75 kg CO2e/sq ft/year
    """)
    
    # Emissions forecast
    st.header("Emissions Forecast")
    forecast_building = st.selectbox(
        "Select Building",
        options=st.session_state.buildings_data['name'].tolist(),
        key="forecast_building"
    )
    
    # Generate mock forecast data
    forecast_dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    base_emissions = st.session_state.buildings_data[
        st.session_state.buildings_data['name'] == forecast_building
    ]['annual_emissions'].iloc[0] / 12
    
    # Add seasonal variation and slight downward trend
    forecast_emissions = base_emissions * (
        1 + 0.2 * np.sin(np.arange(len(forecast_dates)) * 2 * np.pi / 12) - 
        0.1 * np.arange(len(forecast_dates)) / len(forecast_dates)
    )
    
    fig = px.line(x=forecast_dates, y=forecast_emissions,
                 labels={'x': 'Date', 'y': 'Projected Emissions (kg CO2e)'},
                 title='12-Month Emissions Forecast')
    st.plotly_chart(fig, use_container_width=True)
    
    st.header("Need Help?")
    st.write("Contact our support team at support@buildingecovis.com")