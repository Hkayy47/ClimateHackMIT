import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

def init_config():
    """Ensure session state is initialized."""
    if 'buildings_data' not in st.session_state:
        st.session_state.buildings_data = pd.DataFrame({
            'name': [],
            'address': [],
            'area_sqft': [],
            'annual_emissions': [],
            'energy_usage': [],
            'rating': [],
            'latitude': [],
            'longitude': [],
            'credits_available': [],
            'price_per_credit': []
        })
    if 'offset_projects' not in st.session_state:
        st.session_state.offset_projects = pd.DataFrame({
            'name': [],
            'credits_available': [],
            'price_per_credit': [],
            'location': [],
            'type': [],
            'verification': []
        })

def display_add_building():
    # Ensure session state is initialized before accessing it
    init_config()

    if st.session_state.buildings_data.empty or 'annual_emissions' not in st.session_state.buildings_data.columns:
        st.warning("No building data available. Please upload data to get started.")
        return

    # Safely calculate metrics
    num_buildings = len(st.session_state.buildings_data)
    avg_emissions = (
        st.session_state.buildings_data['annual_emissions'].mean()
        if 'annual_emissions' in st.session_state.buildings_data.columns and not st.session_state.buildings_data['annual_emissions'].isnull().all()
        else 0
    )
    best_building = (
        st.session_state.buildings_data.loc[st.session_state.buildings_data['annual_emissions'].idxmin()]
        if 'annual_emissions' in st.session_state.buildings_data.columns and not st.session_state.buildings_data['annual_emissions'].isnull().all()
        else None
    )
    total_credits = (
        st.session_state.buildings_data['credits_available'].sum()
        if 'credits_available' in st.session_state.buildings_data.columns
        else 0
    )

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Buildings Analyzed", num_buildings)
    with col2:
        st.metric("Average Emissions", f"{avg_emissions/1000:.1f} tons CO2e" if avg_emissions > 0 else "N/A")
    with col3:
        st.metric("Best Performer", best_building['name'] if best_building is not None else "N/A")
    with col4:
        st.metric("Available Credits", f"{total_credits:,} tons CO2e" if total_credits > 0 else "N/A")

    # Emissions comparison chart
    if 'annual_emissions' in st.session_state.buildings_data.columns and not st.session_state.buildings_data['annual_emissions'].isnull().all():
        st.subheader("Emissions Comparison")
        fig = px.bar(st.session_state.buildings_data,
                     x='name', y='annual_emissions',
                     color='rating',
                     labels={'name': 'Building Name', 'annual_emissions': 'Annual Emissions (kg CO2e)'},
                     title='Building Emissions Comparison')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No emissions data available for comparison.")

    # Map view
    if not st.session_state.buildings_data.empty and 'latitude' in st.session_state.buildings_data.columns and 'longitude' in st.session_state.buildings_data.columns:
        st.subheader("Geographic Distribution")
        first_building = st.session_state.buildings_data.iloc[0]
        map_center = [first_building.get('latitude', 0), first_building.get('longitude', 0)]
        m = folium.Map(location=map_center, zoom_start=13)

        for _, row in st.session_state.buildings_data.iterrows():
            color = 'green' if row.get('rating', '') == 'A' else 'orange' if row.get('rating', '') == 'B' else 'red'
            folium.CircleMarker(
                location=[row.get('latitude', 0), row.get('longitude', 0)],
                radius=10,
                popup=f"{row.get('name', 'Unknown')}<br>Emissions: {row.get('annual_emissions', 'N/A')} kg CO2e<br>Rating: {row.get('rating', 'N/A')}",
                color=color,
                fill=True
            ).add_to(m)

        st_folium(m, width=800, height=400)
    else:
        st.info("No geographic data available.")

