# Global Risk Simulator

An interactive Streamlit tool that ranks 19 countries by resilience under six different global-crisis scenarios (e.g. a Russia-NATO conflict, a Hormuz energy shock, a climate crisis).

🇩🇪 German version: [README.de.md](README.de.md)

## What it does

- Scores each country on 11 resilience criteria (geographic isolation, nuclear risk, political neutrality, economic resilience, energy independence, cybersecurity, and more).
- Six preset crisis scenarios apply a different weighting to those 11 criteria, so the same country data produces a different ranking depending on the scenario selected.
- Shows the resulting ranking as both a table and a bar chart, with a short explanation of why that scenario favors certain countries.

## Tech stack

Python, [Streamlit](https://streamlit.io/), pandas. All country/criteria data is hardcoded in the script — no external API or CSV.

## Running it

```bash
pip install -r requirements.txt
streamlit run risk_simulator_app.py
```

## Note

The country scores are illustrative estimates for scenario exploration, not a rigorous geopolitical risk model.
