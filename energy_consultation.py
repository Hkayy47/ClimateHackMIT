import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import google.generativeai as genai

def get_gemini_response(prompt):
    """Get response from Gemini model"""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def display_energy_consultation():
    st.header("🏢 Energy Consultation")
    
    if st.session_state.buildings_data.empty:
        st.warning("Please upload building data first.")
        return
    
    # Building selection
    building_name = st.selectbox(
        "Select Your Building",
        options=st.session_state.buildings_data['name'].tolist(),
        key="consultation_building"
    )
    
    # Get building data
    building_data = st.session_state.buildings_data[
        st.session_state.buildings_data['name'] == building_name
    ].iloc[0]
    
    # Calculate energy intensity
    energy_intensity = building_data['energy_usage'] / building_data['area_sqft']
    
    # Display current metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Rating", f"{building_data['rating']}/5")
    with col2:
        st.metric("Annual Energy Usage", f"{building_data['energy_usage']} kWh")
    with col3:
        st.metric("Annual Emissions", f"{building_data['annual_emissions']} kg CO2e")
    with col4:
        st.metric("Energy Intensity", f"{energy_intensity:.2f} kWh/sq ft")

    # Usage description
    st.subheader("Building Usage Details")
    usage_template = """Please provide details about:
• Operating hours and days
• Current HVAC system age and type
• Lighting systems
• Number of occupants
• Recent renovations
• Specific areas of concern
• Energy efficiency goals"""
    
    usage_description = st.text_area(
        "Describe your building's usage patterns and concerns",
        height=150,
        placeholder=usage_template
    )
    
    if st.button("Generate Recommendations") and usage_description:
        with st.spinner("Analyzing building data..."):
            # Create prompt for Gemini
            prompt = f"""Role: Expert Building Energy Consultant
Focus: Commercial Building Performance Analysis

Building Profile - {building_name}:
• Energy Usage: {building_data['energy_usage']} kWh
• Area: {building_data['area_sqft']} sq ft
• Energy Intensity: {energy_intensity:.2f} kWh/sq ft
• Performance Rating: {building_data['rating']}/5
• Annual CO2 Emissions: {building_data['annual_emissions']} kg CO2e

Usage Context: {usage_description}

Provide a detailed analysis including:

1. Performance Assessment
   • Current efficiency level
   • Major improvement areas
   • Comparison with industry standards

2. Specific Recommendations
   • Immediate actions (0-6 months)
   • Short-term improvements (6-18 months)
   • Long-term strategic changes (18+ months)
   Include for each:
   - Estimated implementation cost
   - Expected energy savings
   - ROI timeline
   - CO2 reduction potential

3. Financial Analysis
   • Implementation costs
   • Expected annual savings
   • Available incentives
   • Carbon credit opportunities

4. Sustainability Roadmap
   • Current baseline
   • Target metrics
   • Certification pathways
   • Emission reduction goals

Format the response with clear headers, bullet points, and specific numbers."""

            # Get Gemini's response
            recommendations = get_gemini_response(prompt)
            
            if recommendations:
                st.success("Analysis complete!")
                st.markdown(recommendations)
                st.download_button(
                    "Download Report",
                    data=recommendations,
                    file_name=f"energy_recommendations_{building_name}.md",
                    mime="text/markdown"
                )

    # Add peer comparison visualization
    st.subheader("Peer Building Comparison")
    similar_buildings = st.session_state.buildings_data[
        (st.session_state.buildings_data['area_sqft'].between(
            building_data['area_sqft'] * 0.8,
            building_data['area_sqft'] * 1.2
        )) &
        (st.session_state.buildings_data['name'] != building_name)
    ]
    
    if not similar_buildings.empty:
        fig = go.Figure()
        
        # Add current building
        fig.add_trace(go.Bar(
            x=[building_name],
            y=[building_data['energy_usage']],
            name='Selected Building',
            marker_color='blue'
        ))
        
        # Add peer buildings
        fig.add_trace(go.Bar(
            x=similar_buildings['name'],
            y=similar_buildings['energy_usage'],
            name='Peer Buildings',
            marker_color='lightgray'
        ))
        
        fig.update_layout(
            title='Energy Usage Comparison with Similar-Sized Buildings',
            xaxis_title='Building Name',
            yaxis_title='Energy Usage (kWh)',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
