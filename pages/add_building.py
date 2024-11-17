import streamlit as st
import pandas as pd

def display_add_building():
    st.header("Add New Building")
    
    
    # File upload option for CSV containing multiple buildings
    uploaded_file = st.file_uploader("Upload CSV of multiple buildings", type=["csv"])
    
    # Handle CSV upload
    if uploaded_file is not None:
        try:
            buildings_df = pd.read_csv(uploaded_file)
            st.write("CSV File Content:")
            st.dataframe(buildings_df)  # Show the CSV content
            
            # Validate CSV columns to ensure it matches the required structure
            expected_columns = [
                'name', 'address', 'area_sqft', 'annual_emissions', 'energy_usage', 
                'rating', 'latitude', 'longitude', 'credits_available', 'price_per_credit'
            ]
            
            if set(expected_columns).issubset(buildings_df.columns):
                st.success("CSV is valid. Ready to add buildings.")
                
                # Append the CSV data to the session state
                if 'buildings_data' not in st.session_state:
                    st.session_state.buildings_data = pd.DataFrame(columns=expected_columns)
                
                st.session_state.buildings_data = pd.concat(
                    [st.session_state.buildings_data, buildings_df],
                    ignore_index=True
                )
                st.success("Buildings from CSV uploaded successfully!")
            else:
                st.error(f"CSV does not contain the required columns. Expected columns: {expected_columns}")
        
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
    
    # Create two columns for input fields
    col1, col2 = st.columns(2)
    
    # Column 1 inputs (manual input for a single building)
    with col1:
        new_name = st.text_input("Building Name")
        new_address = st.text_input("Address")
        new_area = st.number_input("Building Area (sq ft)", min_value=0)
        new_emissions = st.number_input("Annual Emissions (kg CO2e)", min_value=0)
        new_energy = st.number_input("Annual Energy Usage (kWh)", min_value=0)
    
    # Column 2 inputs
    with col2:
        new_rating = st.selectbox("Energy Rating", options=['A', 'B', 'C'])
        new_lat = st.number_input("Latitude", value=40.7128)
        new_lon = st.number_input("Longitude", value=-74.0060)
        new_credits = st.number_input("Available Carbon Credits", min_value=0)
        new_credit_price = st.number_input("Credit Price (USD)", min_value=0)
    
    # Button to add a single building manually
    if st.button("Add Building Manually"):
        # Create a DataFrame with the new building's details
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
        
        # Check if session state already contains buildings data, if not initialize it
        if 'buildings_data' not in st.session_state:
            st.session_state.buildings_data = pd.DataFrame(columns=new_building.columns)
        
        # Append the new building data to the session state
        st.session_state.buildings_data = pd.concat(
            [st.session_state.buildings_data, new_building],
            ignore_index=True
        )
        
        # Show a success message
        st.success("Building added successfully!")
        
        # Optionally, display the updated buildings data
        st.write("Current Building Data:")
        st.dataframe(st.session_state.buildings_data)