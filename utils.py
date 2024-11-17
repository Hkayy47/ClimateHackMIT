def get_energy_recommendations(building_name, buildings_data, usage_description):
    prompt = f"""Role: Expert Building Energy Consultant
Focus: Commercial Building Performance Analysis

Building Profile - {building_name}:
• Energy Usage: {buildings_data.loc[buildings_data['name'] == building_name, 'energy_usage'].values[0]} kWh
• Area: {buildings_data.loc[buildings_data['name'] == building_name, 'area_sqft'].values[0]} sq ft
• Energy Intensity: {buildings_data.loc[buildings_data['name'] == building_name, 'energy_usage'].values[0] / buildings_data.loc[buildings_data['name'] == building_name, 'area_sqft'].values[0]:.2f} kWh/sq ft
• Performance Rating: {buildings_data.loc[buildings_data['name'] == building_name, 'rating'].values[0]}/5
• Annual CO2 Emissions: {buildings_data.loc[buildings_data['name'] == building_name, 'annual_emissions'].values[0]} kg CO2e

Usage Context: {usage_description}

Analysis Required:

1. Performance Benchmarking
   • Compare energy intensity with peer buildings
   • Identify efficiency gaps
   • Highlight critical areas for improvement

2. Strategic Recommendations
   • Immediate actions (0-6 months)
   • Short-term improvements (6-18 months)
   • Long-term strategic changes (18+ months)
   Each recommendation must include:
   - Implementation cost range
   - Expected energy savings (%)
   - ROI timeline
   - CO2 reduction potential

3. Financial Impact Analysis
   • Implementation costs
   • Expected annual savings
   • Available incentives/rebates
   • Carbon credit opportunities

4. Sustainability Roadmap
   • Current performance baseline
   • Target metrics and timelines
   • Certification pathways (LEED, ENERGY STAR)
   • Emission reduction targets

5. Next Steps
   • Priority actions
   • Required resources
   • Key stakeholders
   • Success metrics

Comparison Metrics:
• Size-based: Buildings ±20% square footage
• Geographic: Same area performance
• Industry: Standard benchmarks

Focus on practical, cost-effective solutions with clear ROI. Use specific numbers and percentages where possible."""

    return prompt
