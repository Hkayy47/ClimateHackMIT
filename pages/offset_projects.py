import streamlit as st

def display_offset_projects():
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
