# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 00:33:05 2025

@author: kutlu
"""

import json
from pathlib import Path

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

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

# ISO-3166-1 alpha-3 codes for the 19 countries above - needed to join scores
# onto the world-boundaries GeoJSON for the choropleth map (its features are
# keyed by this code, not by country name, since names alone are ambiguous
# across sources, e.g. "Russia" vs "Russian Federation").
COUNTRY_ISO3 = {
    'New Zealand': 'NZL', 'Iceland': 'ISL', 'Switzerland': 'CHE', 'Uruguay': 'URY',
    'Ireland': 'IRL', 'Costa Rica': 'CRI', 'Chile': 'CHL', 'Australia': 'AUS',
    'Canada': 'CAN', 'Finland': 'FIN', 'Portugal': 'PRT', 'Malaysia': 'MYS',
    'Botswana': 'BWA', 'Argentina': 'ARG', 'Japan': 'JPN', 'Italy': 'ITA',
    'China': 'CHN', 'Russia': 'RUS', 'India': 'IND',
}
WORLD_COUNTRIES_GEOJSON = Path(__file__).parent / "data" / "world-countries.json"

scenario_weights = {
    '1': {'name': 'General Balanced Crisis', 'weights': {'Geographic Isolation': 0.15, 'Nuclear Risk': 0.15, 'Political Neutrality': 0.10, 'Economic Resilience': 0.10, 'Domestic Social Stability': 0.10, 'Infrastructure & Health': 0.10, 'Public Preparedness': 0.05, 'Climate Resilience': 0.05, 'Energy Independence': 0.05, 'Cybersecurity': 0.05, 'Demographic Resilience': 0.05}},
    '2': {'name': 'Russia-NATO Conflict', 'weights': {'Geographic Isolation': 0.25, 'Nuclear Risk': 0.25, 'Political Neutrality': 0.20, 'Economic Resilience': 0.05, 'Domestic Social Stability': 0.05, 'Infrastructure & Health': 0.0, 'Public Preparedness': 0.05, 'Climate Resilience': 0.0, 'Energy Independence': 0.10, 'Cybersecurity': 0.05, 'Demographic Resilience': 0.0}},
    '3': {'name': 'China-US Tension (Economic Crisis)', 'weights': {'Geographic Isolation': 0.15, 'Nuclear Risk': 0.05, 'Political Neutrality': 0.15, 'Economic Resilience': 0.25, 'Domestic Social Stability': 0.10, 'Infrastructure & Health': 0.05, 'Public Preparedness': 0.0, 'Climate Resilience': 0.10, 'Energy Independence': 0.05, 'Cybersecurity': 0.10, 'Demographic Resilience': 0.0}},
    '4': {'name': 'Strait of Hormuz Crisis (Energy Shock)', 'weights': {'Geographic Isolation': 0.10, 'Nuclear Risk': 0.0, 'Political Neutrality': 0.05, 'Economic Resilience': 0.20, 'Domestic Social Stability': 0.15, 'Infrastructure & Health': 0.05, 'Public Preparedness': 0.0, 'Climate Resilience': 0.10, 'Energy Independence': 0.30, 'Cybersecurity': 0.0, 'Demographic Resilience': 0.05}},
    '5': {'name': 'Climate Crisis & Water Wars', 'weights': {'Geographic Isolation': 0.15, 'Nuclear Risk': 0.0, 'Political Neutrality': 0.05, 'Economic Resilience': 0.10, 'Domestic Social Stability': 0.20, 'Infrastructure & Health': 0.10, 'Public Preparedness': 0.0, 'Climate Resilience': 0.30, 'Energy Independence': 0.0, 'Cybersecurity': 0.0, 'Demographic Resilience': 0.10}},
    '6': {'name': 'Technological Energy Revolution', 'weights': {'Geographic Isolation': 0.0, 'Nuclear Risk': 0.0, 'Political Neutrality': 0.05, 'Economic Resilience': 0.30, 'Domestic Social Stability': 0.20, 'Infrastructure & Health': 0.10, 'Public Preparedness': 0.0, 'Climate Resilience': 0.0, 'Energy Independence': 0.0, 'Cybersecurity': 0.20, 'Demographic Resilience': 0.15}}
}
#---------------------------------------------------

# Small hand-drawn inline SVGs, one per scenario theme (no icon library/CDN
# involved - just inline path data), shown next to the "why does this matter"
# explanation so each scenario reads at a glance, not just as body text.
SCENARIO_ICONS = {
    '1': """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="3" x2="12" y2="19"/><line x1="4" y1="7" x2="20" y2="7"/>
        <path d="M4 7 L1.6 12.4 a2.6 2.6 0 0 0 4.8 0 L4 7"/>
        <path d="M20 7 L17.6 12.4 a2.6 2.6 0 0 0 4.8 0 L20 7"/>
        <line x1="8" y1="19" x2="16" y2="19"/></svg>""",
    '2': """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2.5 L19.5 5.5 V11.5 C19.5 17 16 20.5 12 21.8 C8 20.5 4.5 17 4.5 11.5 V5.5 Z"/>
        <line x1="9" y1="11" x2="15" y2="11"/></svg>""",
    '3': """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/>
        <text x="12" y="16.5" text-anchor="middle" font-size="11" fill="currentColor" stroke="none" font-family="inherit">$</text></svg>""",
    '4': """<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" stroke="none">
        <path d="M13 2 L4 14 H10 L9 22 L20 10 H14 Z"/></svg>""",
    '5': """<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" stroke="none">
        <path d="M12 2 C12 2 5 11.2 5 15.6 A7 7 0 0 0 19 15.6 C19 11.2 12 2 12 2 Z"/></svg>""",
    '6': """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="7" y="7" width="10" height="10" rx="1.2"/>
        <line x1="12" y1="2" x2="12" y2="7"/><line x1="12" y1="17" x2="12" y2="22"/>
        <line x1="2" y1="12" x2="7" y2="12"/><line x1="17" y1="12" x2="22" y2="12"/></svg>""",
}


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


def tier_for_rank(rank: int, n: int) -> tuple[str, str, str]:
    """Split the ranked table into resilience tiers by rank position.

    Returns (label, text_color, background_color) for a small badge.
    """
    third = n / 3
    if rank < third:
        return "Resilient", "#8fd19e", "rgba(143, 209, 158, 0.16)"
    if rank < 2 * third:
        return "Moderate", "#e0b04a", "rgba(224, 176, 74, 0.16)"
    return "Vulnerable", "#e08a7a", "rgba(224, 138, 122, 0.16)"
#---------------------------------------------------


# 3. GEOGRAPHIC VIEW (choropleth map)
#---------------------------------------------------
def build_resilience_map(result_df: pd.DataFrame) -> folium.Map:
    """A world choropleth colored by resilience score, alongside the
    existing table/bar chart - a ranking like this is inherently
    geographic, and regional patterns (e.g. "isolated/southern-hemisphere
    countries cluster high in this scenario") are easy to miss in a bar
    chart but jump out on a map. RdYlGn (red-yellow-green) mirrors the
    tier badges above (Vulnerable=red, Moderate=amber, Resilient=green)
    rather than an arbitrary palette. Countries outside our 19 simply have
    no score and render in the map's neutral no-data color - that gap is
    itself informative (this tool doesn't claim global coverage).
    """
    geo_df = result_df[['Country', 'Weighted Score']].copy()
    geo_df['ISO3'] = geo_df['Country'].map(COUNTRY_ISO3)
    unmapped = geo_df[geo_df['ISO3'].isna()]
    if not unmapped.empty:
        # Fail loudly rather than silently drop a country from the map -
        # a missing ISO3 entry here means COUNTRY_ISO3 wasn't updated
        # alongside `data` above.
        raise ValueError(
            f"No ISO3 code mapped for: {', '.join(unmapped['Country'])} - "
            "add it to COUNTRY_ISO3."
        )

    # Plain OpenStreetMap tiles, not a CartoDB dark variant: folium's dark
    # CartoDB tiles now require a registered API key we don't have (as of
    # folium 0.20) - OpenStreetMap needs no key and is guaranteed to render.
    m = folium.Map(location=[15, 10], zoom_start=2, tiles="OpenStreetMap")
    folium.Choropleth(
        geo_data=str(WORLD_COUNTRIES_GEOJSON),
        data=geo_df,
        columns=['ISO3', 'Weighted Score'],
        key_on='feature.id',
        fill_color='RdYlGn',
        nan_fill_color='#2a2f38',  # matches the app's dark theme, not folium's default white
        fill_opacity=0.85,
        line_opacity=0.3,
        legend_name='Weighted Resilience Score',
    ).add_to(m)

    # Country-name + score tooltip on hover - the choropleth's color alone
    # doesn't tell you the exact number or which country you're looking at.
    country_lookup = geo_df.set_index('ISO3')[['Country', 'Weighted Score']].to_dict('index')
    with open(WORLD_COUNTRIES_GEOJSON, encoding='utf-8') as f:
        world_geojson = json.load(f)
    scored_features = [feat for feat in world_geojson['features'] if feat['id'] in country_lookup]
    for feat in scored_features:
        info = country_lookup[feat['id']]
        feat['properties']['tooltip'] = f"{info['Country']}: {info['Weighted Score']:.2f}"
    folium.GeoJson(
        {'type': 'FeatureCollection', 'features': scored_features},
        style_function=lambda _: {'fillOpacity': 0, 'weight': 0},
        tooltip=folium.GeoJsonTooltip(fields=['tooltip'], aliases=[''], labels=False),
    ).add_to(m)
    return m
#---------------------------------------------------


# 4. STREAMLIT UI
#---------------------------------------------------
st.set_page_config(page_title="Global Risk Simulator", layout="wide")

# Real typography beyond what config.toml's theme.font (sans serif/serif/
# monospace only) can express - a serif display face for headings (analyst-
# report register), a technical sans for body copy, and a monospace face for
# the scenario explainer/labels, all real Google Fonts loaded via CDN link.
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Petrona:wght@500;600;700&family=Archivo:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
      h1, h2, h3 { font-family: 'Petrona', Georgia, serif !important; letter-spacing: -0.01em; }
      h1 { font-weight: 600 !important; }
      body, p, div, span, label { font-family: 'Archivo', -apple-system, sans-serif; }
      div[data-testid="stExpander"] summary, div[data-testid="stExpander"] p,
      .stSelectbox label p { font-family: 'Roboto Mono', ui-monospace, monospace !important; font-size: 0.92rem; }
      div[data-testid="stMarkdownContainer"] > p { color: #b8b3a8; }
      .risk-icon { display: inline-flex; vertical-align: middle; margin-right: 8px; color: #c9782f; }
      table.risk-table { width: 100%; border-collapse: collapse; font-family: 'Archivo', sans-serif; font-size: 0.92rem; }
      table.risk-table th { text-align: left; padding: 8px 10px; color: #8b8578; font-family: 'Roboto Mono', monospace; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid #2a2f38; }
      table.risk-table td { padding: 7px 10px; border-bottom: 1px solid #1c2027; color: #e8e6e1; }
      .tier-badge { display: inline-block; padding: 2px 9px; border-radius: 999px; font-size: 0.78rem; font-weight: 500; }
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
    # Build the ranking as a styled HTML table with a resilience-tier badge
    # per row, instead of a plain dataframe, so relative standing reads at
    # a glance rather than requiring the reader to scan raw numbers.
    n_countries = len(result_df)
    rows_html = []
    for rank, row in result_df.iterrows():
        label, color, bg = tier_for_rank(rank, n_countries)
        rows_html.append(
            f"<tr><td>{rank + 1}</td><td>{row['Country']}</td>"
            f"<td>{row['Weighted Score']:.2f}</td>"
            f"<td><span class='tier-badge' style='color:{color};background:{bg};'>{label}</span></td></tr>"
        )
    table_html = (
        "<table class='risk-table'><thead><tr>"
        "<th>#</th><th>Country</th><th>Score</th><th>Tier</th>"
        "</tr></thead><tbody>" + "".join(rows_html) + "</tbody></table>"
    )
    st.markdown(table_html, unsafe_allow_html=True)

with col2:
    st.subheader("Visual Score Comparison")
    # Prepare data for the chart
    chart_data = result_df.set_index('Country')['Weighted Score']
    st.bar_chart(chart_data)

    with st.expander("ℹ️ Why Does This Scenario Matter? (Explanation)"):
        icon = SCENARIO_ICONS[selected_id]
        if selected_id == '1':
            text = "A baseline starting point in which all factors are weighted in a balanced way."
        elif selected_id == '2':
            text = "Geographic distance, neutrality, and staying off nuclear target lists become the most important factors. Southern-hemisphere countries and isolated islands stand out."
        elif selected_id == '3':
            text = "Economic self-sufficiency, strong industry, and low dependence on technology imports become critical. Economies far from the Pacific and Atlantic-focused hold the advantage."
        elif selected_id == '4':
            text = "Energy independence overrides everything else. Net energy exporters (Canada, Australia) and renewable-energy leaders (Iceland, Uruguay) come out ahead in this crisis."
        elif selected_id == '5':
            text = "Countries with water and food resources, temperate climates, distance from migration routes, and social cohesion become the safest places. Isolation and resource wealth are the key."
        elif selected_id == '6':
            text = "Diversified, innovative, high-tech economies not dependent on fossil fuels come out ahead in this revolution. A young, educated population is a major advantage."
        st.markdown(f"<span class='risk-icon'>{icon}</span>{text}", unsafe_allow_html=True)

# Full-width, below the table/chart columns rather than squeezed into
# col1/col2 - a world map needs real horizontal room to be readable.
st.subheader("🗺️ Geographic View")
st.caption("Same scores as the table/chart above, mapped by country - regional patterns are easy to miss in a bar chart but obvious on a map.")
st_folium(build_resilience_map(result_df), width=None, height=420, returned_objects=[])
#---------------------------------------------------
