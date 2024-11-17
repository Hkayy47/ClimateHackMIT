import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from io import StringIO
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

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

def get_rating_color(rating):
    """Return color based on 1-5 rating scale."""
    color_map = {
        1: 'red',
        2: 'orange',
        3: 'yellow',
        4: 'lightgreen',
        5: 'green'
    }
    return color_map.get(rating, 'gray')

def upload_buildings_data():
    """Handle CSV upload for building data."""
    st.subheader("Upload Buildings Data")
    
    # Show expected CSV format
    st.markdown("""
    #### Expected CSV Format:
    Your CSV should include the following columns:
    - name
    - address
    - area_sqft
    - annual_emissions
    - energy_usage
    - rating (1-5, where 5 is best)
    - latitude
    - longitude
    - credits_available
    - price_per_credit
    """)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read the CSV file
            string_data = StringIO(uploaded_file.getvalue().decode("utf-8"))
            new_data = pd.read_csv(string_data)
            
            # Validate required columns
            required_columns = ['name', 'address', 'area_sqft', 'annual_emissions', 
                              'energy_usage', 'rating', 'latitude', 'longitude', 
                              'credits_available', 'price_per_credit']
            
            missing_columns = [col for col in required_columns if col not in new_data.columns]
            
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
                return
            
            # Validate data types
            try:
                new_data['area_sqft'] = pd.to_numeric(new_data['area_sqft'])
                new_data['annual_emissions'] = pd.to_numeric(new_data['annual_emissions'])
                new_data['energy_usage'] = pd.to_numeric(new_data['energy_usage'])
                new_data['latitude'] = pd.to_numeric(new_data['latitude'])
                new_data['longitude'] = pd.to_numeric(new_data['longitude'])
                new_data['credits_available'] = pd.to_numeric(new_data['credits_available'])
                new_data['price_per_credit'] = pd.to_numeric(new_data['price_per_credit'])
                new_data['rating'] = pd.to_numeric(new_data['rating'])
            except ValueError as e:
                st.error(f"Error converting numeric columns: {str(e)}")
                return
            
            # Validate ratings (1-5)
            if not new_data['rating'].between(1, 5).all():
                st.error("Rating must be between 1 and 5")
                return
            
            # Preview the data
            st.subheader("Data Preview")
            st.dataframe(new_data.head())
            
            # Add confirmation button
            if st.button("Confirm Upload"):
                # Append new data to existing data
                st.session_state.buildings_data = pd.concat([st.session_state.buildings_data, new_data], 
                                                          ignore_index=True)
                st.success(f"Successfully added {len(new_data)} buildings to the database!")
                
                # Show updated total
                st.info(f"Total buildings in database: {len(st.session_state.buildings_data)}")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
def predict_emissions(historical_data, forecast_years=5):
    """
    Calculate emission predictions based on historical data.
    
    Args:
        historical_data (pd.DataFrame): DataFrame containing historical emissions data
        forecast_years (int): Number of years to forecast
    """
    if len(historical_data) < 2:
        st.warning("Insufficient historical data for prediction. Need at least 2 data points.")
        return None
        
    # Prepare data for prediction
    X = np.arange(len(historical_data)).reshape(-1, 1)
    y = historical_data['annual_emissions'].values
    
    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate future dates for prediction
    future_X = np.arange(len(historical_data), len(historical_data) + forecast_years).reshape(-1, 1)
    predictions = model.predict(future_X)
    
    return predictions

def display_predictive_analysis():
    """Display predictive analysis section in the Streamlit app."""
    st.header("📈 Predictive Analysis")
    
    if st.session_state.buildings_data.empty:
        st.warning("Please upload building data to view predictions.")
        return
        
    # Sidebar controls for prediction parameters
    st.sidebar.subheader("Prediction Settings")
    forecast_years = st.sidebar.slider("Forecast Years", 1, 10, 5)
    reduction_target = st.sidebar.number_input(
        "Annual Emission Reduction Target (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=5.0
    )
    
    # Calculate current total emissions
    current_total = st.session_state.buildings_data['annual_emissions'].sum()
    
    # Generate predictions
    historical_data = pd.DataFrame({
        'annual_emissions': [current_total]
    })
    
    # Add some synthetic historical data based on current total
    # This would ideally be replaced with actual historical data
    for i in range(2):
        historical_val = current_total * (1 + np.random.uniform(-0.1, 0.1))
        historical_data = pd.concat([
            pd.DataFrame({'annual_emissions': [historical_val]}),
            historical_data
        ])
    
    predictions = predict_emissions(historical_data, forecast_years)
    
    if predictions is not None:
        # Calculate target reduction pathway
        target_emissions = [current_total]
        for _ in range(forecast_years):
            target_emissions.append(target_emissions[-1] * (1 - reduction_target/100))
            
        # Create visualization
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=list(range(len(historical_data))),
            y=historical_data['annual_emissions'],
            name='Historical',
            line=dict(color='blue')
        ))
        
        # Predictions
        fig.add_trace(go.Scatter(
            x=list(range(len(historical_data), len(historical_data) + forecast_years)),
            y=predictions,
            name='Predicted (Business as Usual)',
            line=dict(color='red', dash='dash')
        ))
        
        # Target pathway
        fig.add_trace(go.Scatter(
            x=list(range(len(historical_data) - 1, len(historical_data) + forecast_years)),
            y=target_emissions,
            name=f'Target ({reduction_target}% Annual Reduction)',
            line=dict(color='green', dash='dash')
        ))
        
        fig.update_layout(
            title='Emissions Forecast vs Reduction Target',
            xaxis_title='Years from Present',
            yaxis_title='Total Annual Emissions (kg CO2e)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate and display key metrics
        final_predicted = predictions[-1]
        final_target = target_emissions[-1]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Current Annual Emissions",
                f"{current_total/1000:.1f} tons CO2e"
            )
        with col2:
            predicted_change = ((final_predicted - current_total) / current_total) * 100
            st.metric(
                f"Predicted Emissions in {forecast_years} Years",
                f"{final_predicted/1000:.1f} tons CO2e",
                f"{predicted_change:+.1f}%",
                delta_color="inverse"
            )
        with col3:
            target_change = ((final_target - current_total) / current_total) * 100
            st.metric(
                "Target Emissions",
                f"{final_target/1000:.1f} tons CO2e",
                f"{target_change:+.1f}%",
                delta_color="inverse"
            )
            
        # Recommendations based on analysis
        st.subheader("📋 Recommendations")
        emission_gap = final_predicted - final_target
        if emission_gap > 0:
            st.warning(f"""
            To reach your {reduction_target}% annual reduction target, you need to:
            - Reduce emissions by an additional {emission_gap/1000:.1f} tons CO2e by year {forecast_years}
            - Focus on buildings with lowest energy ratings first
            - Consider implementing energy efficiency measures
            - Explore renewable energy options
            """)
        else:
            st.success(f"""
            You are on track to meet your {reduction_target}% annual reduction target!
            Continue with current emission reduction strategies and consider:
            - Setting more ambitious targets
            - Sharing best practices across your building portfolio
            - Exploring innovative technologies for further improvements
            """)
            
        # Detailed building-level predictions
        st.subheader("🏢 Building-Level Predictions")
        building_predictions = pd.DataFrame({
            'Building': st.session_state.buildings_data['name'],
            'Current Emissions': st.session_state.buildings_data['annual_emissions'],
            f'Predicted Emissions (Year {forecast_years})': st.session_state.buildings_data['annual_emissions'] * 
                (final_predicted / current_total),
            'Current Rating': st.session_state.buildings_data['rating']
        }).sort_values('Current Emissions', ascending=False)
        
        st.dataframe(building_predictions.style.format({
            'Current Emissions': '{:.1f}',
            f'Predicted Emissions (Year {forecast_years})': '{:.1f}'
        }))

def display_home():
    # Add upload section at the top
    upload_buildings_data()
    
    st.markdown("---")  # Add separator
    
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

    st.markdown("---")
    display_predictive_analysis()

    # Emissions comparison chart
    if 'annual_emissions' in st.session_state.buildings_data.columns and not st.session_state.buildings_data['annual_emissions'].isnull().all():
        st.subheader("Emissions Comparison")
        fig = px.bar(st.session_state.buildings_data,
                     x='name', y='annual_emissions',
                     color='rating',
                     color_continuous_scale=['red', 'orange', 'yellow', 'lightgreen', 'green'],
                     labels={'name': 'Building Name', 
                            'annual_emissions': 'Annual Emissions (kg CO2e)',
                            'rating': 'Rating (1-5)'},
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
            color = get_rating_color(row.get('rating', 0))
            folium.CircleMarker(
                location=[row.get('latitude', 0), row.get('longitude', 0)],
                radius=10,
                popup=f"{row.get('name', 'Unknown')}<br>Emissions: {row.get('annual_emissions', 'N/A')} kg CO2e<br>Rating: {row.get('rating', 'N/A')}/5",
                color=color,
                fill=True
            ).add_to(m)

        st_folium(m, width=800, height=400)
    else:
        st.info("No geographic data available.")
          