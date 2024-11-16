import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Mock API response data
def get_mock_api_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    df = pd.DataFrame({
        'date': date_range,
        'consumption.electricity': np.random.uniform(100, 200, len(date_range)),
        'emissions.electricity': np.random.uniform(50, 100, len(date_range))
    })
    
    total_consumption = df['consumption.electricity'].sum()
    total_emissions = df['emissions.electricity'].sum()
    
    return df, total_consumption, total_emissions

def suggest_carbon_offsets(emissions):
    if emissions < 1000:
        return [
            {"name": "Plant Trees", "offset": 500, "cost": 50},
            {"name": "Support Local Renewable Energy", "offset": 750, "cost": 100}
        ]
    elif emissions < 5000:
        return [
            {"name": "Invest in Wind Farm", "offset": 2000, "cost": 300},
            {"name": "Sponsor Energy Efficient Appliances", "offset": 1500, "cost": 250}
        ]
    else:
        return [
            {"name": "Large-scale Reforestation Project", "offset": 5000, "cost": 1000},
            {"name": "Industrial Energy Efficiency Program", "offset": 7500, "cost": 1500}
        ]

st.set_page_config(page_title="EcoViz - Carbon Offset Platform", page_icon="🌿", layout="wide")

st.title("EcoViz - Carbon Offset Platform")
st.write("Visualize your office's carbon emissions and find ways to offset them.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Office Details")
    office_size = st.number_input("Office Size (sq ft)", min_value=100, max_value=100000, value=5000)
    num_employees = st.number_input("Number of Employees", min_value=1, max_value=1000, value=50)
    energy_source = st.selectbox("Primary Energy Source", ["Grid Electricity", "Solar Power", "Wind Power"])

    if st.button("Calculate Emissions"):
        with st.spinner("Calculating emissions..."):
            # In a real app, you would make an API call here
            df, total_consumption, total_emissions = get_mock_api_data()
            
            st.session_state.df = df
            st.session_state.total_consumption = total_consumption
            st.session_state.total_emissions = total_emissions

if 'df' in st.session_state:
    with col2:
        st.subheader("Carbon Emissions Visualization")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.df['date'],
            y=st.session_state.df['emissions.electricity'],
            mode='lines',
            fill='tozeroy',
            name='Carbon Emissions'
        ))
        fig.update_layout(
            title='Daily Carbon Emissions',
            xaxis_title='Date',
            yaxis_title='Emissions (kg CO2)',
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Total Electricity Consumption", f"{st.session_state.total_consumption:.2f} kWh")
        st.metric("Total Carbon Emissions", f"{st.session_state.total_emissions:.2f} kg CO2")

    st.subheader("Carbon Offset Recommendations")
    offset_suggestions = suggest_carbon_offsets(st.session_state.total_emissions)
    
    for suggestion in offset_suggestions:
        with st.expander(f"{suggestion['name']} - Offset {suggestion['offset']} kg CO2"):
            st.write(f"Cost: ${suggestion['cost']}")
            if st.button(f"Purchase Offset: {suggestion['name']}", key=suggestion['name']):
                st.success(f"You've purchased the {suggestion['name']} offset!")

st.sidebar.header("About EcoViz")
st.sidebar.write("""
EcoViz helps companies visualize their office space carbon emissions and find ways to offset them through carbon credits.
Our platform provides accurate emissions calculations and tailored offset recommendations to help you reduce your carbon footprint.
""")

st.sidebar.header("Need Help?")
st.sidebar.write("Contact our support team at support@ecoviz.com")