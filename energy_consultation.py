import streamlit as st
import google.generativeai as genai

def get_gemini_response(messages):
    model = genai.GenerativeModel('gemini-pro')
    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    response = model.generate_content(prompt)
    return response.text

def get_building_context(building_name, buildings_data):
    building = buildings_data[buildings_data['name'] == building_name].iloc[0]
    energy_intensity = building['energy_usage'] / building['area_sqft']
    
    return {
        'role': 'system',
        'content': f"""You are a professional energy efficiency consultant analyzing this building:
        
        Building Name: {building_name}
        Energy Usage: {building['energy_usage']} kWh
        Area: {building['area_sqft']} sq ft
        Energy Intensity: {energy_intensity:.2f} kWh/sq ft
        Performance Rating: {building['rating']}/5
        Annual CO2 Emissions: {building['annual_emissions']} kg CO2e
        
        Provide specific, actionable advice based on this data and the user's questions.
        Focus on practical recommendations and clear explanations."""
    }

def display_energy_consultation():
    st.title("🏢 Energy Efficiency Chatbot")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_building' not in st.session_state:
        st.session_state.current_building = None

    # Check if building data exists
    if st.session_state.buildings_data.empty:
        st.warning("⚠️ No building data available. Please upload data to continue.")
        return

    # Building Selection
    building_name = st.selectbox(
        "Choose your building:",
        options=st.session_state.buildings_data['name'].tolist()
    )

    # Reset chat if building changes
    if st.session_state.current_building != building_name:
        st.session_state.messages = []
        st.session_state.current_building = building_name

    # Display Building Metrics
    building_data = st.session_state.buildings_data[
        st.session_state.buildings_data['name'] == building_name
    ].iloc[0]
    energy_intensity = building_data['energy_usage'] / building_data['area_sqft']

    st.subheader("📊 Building Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Rating", f"{building_data['rating']}/5")
    col2.metric("Energy Usage", f"{building_data['energy_usage']} kWh")
    col3.metric("Annual Emissions", f"{building_data['annual_emissions']} kg CO2e")
    col4.metric("Energy Intensity", f"{energy_intensity:.2f} kWh/sq ft")

    # Chat Interface
    st.subheader("💬 Chat with the Energy Consultant")

    # Display chat messages
    for message in st.session_state.messages:
        if message['role'] != 'system':
            with st.chat_message(message['role']):
                st.write(message['content'])

    # Chat input
    if prompt := st.chat_input("Ask about energy efficiency recommendations"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get building context if this is the first message
        if len(st.session_state.messages) == 1:
            context = get_building_context(building_name, st.session_state.buildings_data)
            messages_with_context = [context] + st.session_state.messages
        else:
            messages_with_context = st.session_state.messages

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(messages_with_context)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # Download Chat Log
    if st.session_state.messages:
        chat_log = "\n\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in st.session_state.messages 
            if msg['role'] != 'system'
        ])
        st.download_button(
            "📥 Download Consultation Report",
            data=chat_log,
            file_name=f"energy_consultation_{building_name}.txt",
            mime="text/plain"
        )

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()