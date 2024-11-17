import streamlit as st
from utils import get_energy_recommendations

def display_energy_consultation():
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
