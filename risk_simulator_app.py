# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 00:33:05 2025

@author: kutlu
"""

import streamlit as st
import pandas as pd

# 1. CORE DATA AND SETTINGS
#---------------------------------------------------
data = {
    'Country': ['New Zealand', 'Iceland', 'Switzerland', 'Uruguay', 'Ireland', 'Costa Rica', 'Chile', 'Australia',
             'Canada', 'Finland', 'Portugal', 'Malaysia', 'Botswana', 'Argentina', 'Japan', 'Italy', 'China', 'Russia', 'India'],
    'Geographic Isolation': [9, 10, 5, 7, 8, 7, 9, 9, 7, 4, 7, 6, 8, 9, 8, 6, 4, 3, 5],
    'Nuclear Risk': [10, 10, 10, 10, 10, 10, 10, 9, 6, 5, 6, 7, 10, 10, 7, 6, 5, 4, 6],
    'Political Neutrality': [10, 9, 10, 10, 10, 10, 8, 6, 4, 3, 5, 7, 9, 8, 5, 5, 3, 3, 6],
    'Economic Resilience': [8, 7, 10, 7, 8, 6, 7, 9, 9, 8, 7, 8, 5, 3, 9, 7, 8, 5, 6],
    'Domestic Social Stability': [9, 10, 10, 9, 9, 9, 6, 8, 9, 10, 8, 7, 8, 4, 9, 7, 6, 4, 6],
    'Infrastructure & Health': [9, 9, 10, 8, 9, 7, 7, 9, 9, 10, 8, 8, 5, 6, 10, 9, 8, 7, 5],
    'Public Preparedness': [6, 6, 10, 5, 5, 4, 5, 7, 6, 10, 5, 4, 3, 4, 8, 6, 7, 8, 5],
    'Climate Resilience': [8, 6, 7, 9, 7, 8, 8, 7, 9, 7, 6, 7, 6, 9, 5, 5, 5, 8, 7],
    'Energy Independence': [6, 10, 7, 8, 5, 8, 6, 9, 10, 7, 3, 8, 4, 7, 3, 2, 4, 9, 4],
    'Cybersecurity': [8, 8, 9, 6, 8, 5, 6, 9, 9, 9, 7, 7, 3, 5, 9, 8, 8, 6, 6],
    'Demographic Resilience': [8, 7, 6, 7, 8, 8, 7, 9, 9, 5, 4, 7, 8, 6, 2, 2, 3, 3, 9]
}
df = pd.DataFrame(data)

scenario_weights = {
    '1': {'name': 'General Balanced Crisis', 'weights': {'Geographic Isolation': 0.15, 'Nuclear Risk': 0.15, 'Political Neutrality': 0.10, 'Economic Resilience': 0.10, 'Domestic Social Stability': 0.10, 'Infrastructure & Health': 0.10, 'Public Preparedness': 0.05, 'Climate Resilience': 0.05, 'Energy Independence': 0.05, 'Cybersecurity': 0.05, 'Demographic Resilience': 0.05}},
    '2': {'name': 'Russia-NATO Conflict', 'weights': {'Geographic Isolation': 0.25, 'Nuclear Risk': 0.25, 'Political Neutrality': 0.20, 'Economic Resilience': 0.05, 'Domestic Social Stability': 0.05, 'Infrastructure & Health': 0.0, 'Public Preparedness': 0.05, 'Climate Resilience': 0.0, 'Energy Independence': 0.10, 'Cybersecurity': 0.05, 'Demographic Resilience': 0.0}},
    '3': {'name': 'China-US Tension (Economic Crisis)', 'weights': {'Geographic Isolation': 0.15, 'Nuclear Risk': 0.05, 'Political Neutrality': 0.15, 'Economic Resilience': 0.25, 'Domestic Social Stability': 0.10, 'Infrastructure & Health': 0.05, 'Public Preparedness': 0.0, 'Climate Resilience': 0.10, 'Energy Independence': 0.05, 'Cybersecurity': 0.10, 'Demographic Resilience': 0.0}},
    '4': {'name': 'Strait of Hormuz Crisis (Energy Shock)', 'weights': {'Geographic Isolation': 0.10, 'Nuclear Risk': 0.0, 'Political Neutrality': 0.05, 'Economic Resilience': 0.20, 'Domestic Social Stability': 0.15, 'Infrastructure & Health': 0.05, 'Public Preparedness': 0.0, 'Climate Resilience': 0.10, 'Energy Independence': 0.30, 'Cybersecurity': 0.0, 'Demographic Resilience': 0.05}},
    '5': {'name': 'Climate Crisis & Water Wars', 'weights': {'Geographic Isolation': 0.15, 'Nuclear Risk': 0.0, 'Political Neutrality': 0.05, 'Economic Resilience': 0.10, 'Domestic Social Stability': 0.20, 'Infrastructure & Health': 0.10, 'Public Preparedness': 0.0, 'Climate Resilience': 0.30, 'Energy Independence': 0.0, 'Cybersecurity': 0.0, 'Demographic Resilience': 0.10}},
    '6': {'name': 'Technological Energy Revolution', 'weights': {'Geographic Isolation': 0.0, 'Nuclear Risk': 0.0, 'Political Neutrality': 0.05, 'Economic Resilience': 0.30, 'Domestic Social Stability': 0.20, 'Infrastructure & Health': 0.10, 'Public Preparedness': 0.0, 'Climate Resilience': 0.0, 'Energy Independence': 0.0, 'Cybersecurity': 0.20, 'Demographic Resilience': 0.15}}
}
#---------------------------------------------------


# 2. SCORE CALCULATION
#---------------------------------------------------
def calculate_scores(df, scenario_id):
    scenario = scenario_weights[scenario_id]
    weights = scenario['weights']
    score_columns = list(weights.keys())

    # Multiply each factor's score by its weight and sum across factors
    df['Weighted Score'] = (df[score_columns] * pd.Series(weights)).sum(axis=1)

    sorted_df = df.sort_values(by='Weighted Score', ascending=False).reset_index(drop=True)
    return sorted_df, scenario['name']
#---------------------------------------------------


# 3. STREAMLIT UI
#---------------------------------------------------
st.set_page_config(page_title="Global Risk Simulator", layout="wide")

# Real typography beyond what config.toml's theme.font (sans serif/serif/
# monospace only) can express - a serif display face for headings (analyst-
# report register, not a generic dashboard sans) and a monospace face for
# the scenario explainer/labels, both real Google Fonts loaded via CDN link.
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600;6..72,700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
      h1, h2, h3 { font-family: 'Newsreader', Georgia, serif !important; letter-spacing: -0.01em; }
      h1 { font-weight: 600 !important; }
      div[data-testid="stExpander"] summary, div[data-testid="stExpander"] p,
      .stSelectbox label p { font-family: 'IBM Plex Mono', ui-monospace, monospace !important; font-size: 0.92rem; }
      div[data-testid="stMarkdownContainer"] > p { color: #b8b3a8; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌍 Dynamic Global Risk Simulator")
st.markdown("""
This tool analyzes how resilient countries are under different global crisis scenarios.
Each scenario assigns different weights to different factors (economy, geography, energy, etc.), dynamically changing the country ranking.
""")

# Dropdown menu (selectbox) for scenario selection
scenario_name_to_id = {v['name']: k for k, v in scenario_weights.items()}
selected_scenario_name = st.selectbox(
    'Please select the scenario you want to analyze:',
    list(scenario_name_to_id.keys())
)

# Run the calculation for the selected scenario
selected_id = scenario_name_to_id[selected_scenario_name]
result_df, scenario_name = calculate_scores(df.copy(), selected_id)

# Show the results
st.header(f"📊 Scenario Results: {scenario_name}")

# Split the page into two columns
col1, col2 = st.columns((1, 1.2))  # Column width ratios

with col1:
    st.subheader("Country Ranking")
    # Format and display the scores
    display_df = result_df[['Country', 'Weighted Score']].copy()
    display_df['Weighted Score'] = display_df['Weighted Score'].map('{:.2f}'.format)
    st.dataframe(display_df, height=620)

with col2:
    st.subheader("Visual Score Comparison")
    # Prepare data for the chart
    chart_data = result_df.set_index('Country')['Weighted Score']
    st.bar_chart(chart_data)

    with st.expander("ℹ️ Why Does This Scenario Matter? (Explanation)"):
        if selected_id == '1':
            st.write("A baseline starting point in which all factors are weighted in a balanced way.")
        elif selected_id == '2':
            st.write("Geographic distance, neutrality, and staying off nuclear target lists become the most important factors. Southern-hemisphere countries and isolated islands stand out.")
        elif selected_id == '3':
            st.write("Economic self-sufficiency, strong industry, and low dependence on technology imports become critical. Economies far from the Pacific and Atlantic-focused hold the advantage.")
        elif selected_id == '4':
            st.write("Energy independence overrides everything else. Net energy exporters (Canada, Australia) and renewable-energy leaders (Iceland, Uruguay) come out ahead in this crisis.")
        elif selected_id == '5':
            st.write("Countries with water and food resources, temperate climates, distance from migration routes, and social cohesion become the safest places. Isolation and resource wealth are the key.")
        elif selected_id == '6':
            st.write("Diversified, innovative, high-tech economies not dependent on fossil fuels come out ahead in this revolution. A young, educated population is a major advantage.")
#---------------------------------------------------
