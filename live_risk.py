"""Live-data mode: pulls the data-driven risk ranking from Global Monitor (World Bank indicators)
instead of the hand-entered scores in risk_simulator_app.py. No extra dependency: stdlib urllib."""
from __future__ import annotations

import json
import urllib.request

import pandas as pd

# Scenario ids of the hand-scored model -> Global Monitor scenario slugs (same six crises).
SCENARIO_SLUGS = {
    '1': 'general-balanced-crisis',
    '2': 'russia-nato-conflict',
    '3': 'china-us-tension',
    '4': 'hormuz-energy-shock',
    '5': 'climate-water-wars',
    '6': 'tech-energy-revolution',
}


def fetch(base_url: str, scenario_id: str, timeout: float = 20.0) -> dict:
    url = f"{base_url.rstrip('/')}/api/risk/{SCENARIO_SLUGS[scenario_id]}"
    with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310 - fixed https base URL from config
        return json.load(resp)


def to_frame(payload: dict, iso3_to_country: dict[str, str]) -> tuple[pd.DataFrame, list[str]]:
    """Rows for the countries in `iso3_to_country`, sorted by structural score (best first).

    Returns (frame, names of requested countries the live data could not rank)."""
    by_iso = {row['iso3']: row for row in payload.get('ranked', [])}
    rows, missing = [], []
    for iso, name in iso3_to_country.items():
        row = by_iso.get(iso)
        if row is None:
            missing.append(name)
            continue
        rows.append({
            'Country': name,
            'Weighted Score': float(row['structural_score']),
            'Exposure (km)': row.get('exposure_km'),
            'Nuclear-armed': bool(row.get('nuclear_armed')),
            'Completeness': row.get('completeness'),
        })
    frame = pd.DataFrame(rows, columns=['Country', 'Weighted Score', 'Exposure (km)', 'Nuclear-armed', 'Completeness'])
    return frame.sort_values('Weighted Score', ascending=False).reset_index(drop=True), missing
