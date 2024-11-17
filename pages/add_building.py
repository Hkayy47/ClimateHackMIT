import streamlit as st
import pandas as pd

def display_add_building():
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
