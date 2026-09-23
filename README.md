# Global Risk Simulator

An interactive Streamlit tool that ranks 19 countries by resilience under six different global-crisis scenarios (e.g. a Russia-NATO conflict, a Hormuz energy shock, a climate crisis).

🇩🇪 German version: [README.de.md](README.de.md)

## What it does

- Scores each country on 11 resilience criteria (geographic isolation, nuclear risk, political neutrality, economic resilience, energy independence, cybersecurity, and more).
- Six preset crisis scenarios apply a different weighting to those 11 criteria, so the same country data produces a different ranking depending on the scenario selected.
- Shows the resulting ranking as a table, a bar chart, and a world choropleth map, with a short explanation of why that scenario favors certain countries.

## Geographic view

Below the table/bar chart, a world map colors each of the 19 countries by its weighted score for the selected scenario (red = vulnerable, green = resilient — same tiers as the table's badges), so regional patterns (e.g. "isolated, southern-hemisphere countries cluster high" for the Russia-NATO scenario) are visible at a glance rather than requiring a scan across bar-chart labels. Hover a colored country for its exact score. Built with [`folium`](https://python-visualization.github.io/folium/)/[`streamlit-folium`](https://github.com/randyzwitch/streamlit-folium); country boundaries come from a vendored copy of folium's own reference `world-countries.json` (`data/`, ~250KB, so the app doesn't depend on an external URL at runtime) keyed by ISO-3166-1 alpha-3 code (`COUNTRY_ISO3` in `risk_simulator_app.py`) — countries outside the 19 scored here simply have no data and render in the map's neutral color.

## Tech stack

Python, [Streamlit](https://streamlit.io/), pandas, folium/streamlit-folium. All country/criteria data is hardcoded in the script — no external API or CSV.

## Running it

```bash
pip install -r requirements.txt
streamlit run risk_simulator_app.py
```

## Tests

```bash
pip install pytest
python -m pytest tests/
```

Covers the map's country coverage specifically: every scored country has an ISO3 code, every ISO3 code exists in the vendored GeoJSON, the rendered map actually contains all 19 countries (not silently missing one due to a name/code mismatch), and an unmapped country raises a clear error instead of silently vanishing from the map.

## Note

The country scores are illustrative estimates for scenario exploration, not a rigorous geopolitical risk model.
