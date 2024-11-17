import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium

def display_home():
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
