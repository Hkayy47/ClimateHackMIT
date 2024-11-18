def get_energy_recommendations(building_name, buildings_data, usage_description):
    sages = [
        {
            'role': 'system',
            'content': """You are a professional energy efficiency consultant specializing in commercial building performance analysis and sustainability. Your task is to evaluate building data and generate recommendations to improve energy efficiency and reduce carbon emissions. Your responses should be structured, actionable, and backed by data."""
        },
        {
            'role': 'user',
            'content': f"""Building: {building_name}
Energy Usage: {buildings_data.loc[buildings_data['name'] == building_name, 'energy_usage'].values[0]} kWh
Area: {buildings_data.loc[buildings_data['name'] == building_name, 'area_sqft'].values[0]} sq ft
Energy Intensity: {buildings_data.loc[buildings_data['name'] == building_name, 'energy_usage'].values[0] / buildings_data.loc[buildings_data['name'] == building_name, 'area_sqft'].values[0]:.2f} kWh/sq ft
Annual CO2 Emissions: {buildings_data.loc[buildings_data['name'] == building_name, 'annual_emissions'].values[0]} kg CO2e

Usage Context: {usage_description}

Provide recommendations for improving energy efficiency."""
        }
    ]
    return sages
