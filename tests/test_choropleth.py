"""Guards the choropleth map's country coverage - a missing ISO3 entry
would silently drop a country from the map (it'd render in the neutral
no-data color instead of its actual score) without raising anywhere else,
since Streamlit apps don't have anything else exercising this path."""
import importlib.util
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_app_module():
    spec = importlib.util.spec_from_file_location("risk_simulator_app", PROJECT_ROOT / "risk_simulator_app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_country_has_an_iso3_code():
    app = _load_app_module()
    missing = [c for c in app.df["Country"] if c not in app.COUNTRY_ISO3]
    assert not missing, f"COUNTRY_ISO3 is missing an entry for: {missing}"


def test_every_iso3_code_exists_in_the_world_geojson():
    app = _load_app_module()
    with open(app.WORLD_COUNTRIES_GEOJSON, encoding="utf-8") as f:
        world = json.load(f)
    known_ids = {feature["id"] for feature in world["features"]}
    missing = [iso for iso in app.COUNTRY_ISO3.values() if iso not in known_ids]
    assert not missing, f"ISO3 codes not found in world-countries.json: {missing}"


def test_build_resilience_map_renders_every_country():
    app = _load_app_module()
    result_df, _ = app.calculate_scores(app.df.copy(), "1")
    rendered_html = app.build_resilience_map(result_df)._repr_html_()
    missing = [iso for iso in app.COUNTRY_ISO3.values() if iso not in rendered_html]
    assert not missing, f"ISO3 codes missing from the rendered map HTML: {missing}"


def test_build_resilience_map_raises_on_unmapped_country():
    app = _load_app_module()
    result_df, _ = app.calculate_scores(app.df.copy(), "1")
    result_df.loc[0, "Country"] = "Atlantis"  # not in COUNTRY_ISO3 on purpose
    try:
        app.build_resilience_map(result_df)
    except ValueError as e:
        assert "Atlantis" in str(e)
    else:
        raise AssertionError("expected build_resilience_map to raise ValueError for an unmapped country")


def test_live_frame_filters_sorts_and_reports_missing():
    sys_path = str(PROJECT_ROOT)
    import sys
    sys.path.insert(0, sys_path)
    import live_risk

    payload = {"ranked": [
        {"iso3": "CHE", "structural_score": 80.0, "exposure_km": 3000, "nuclear_armed": False, "completeness": 1.0},
        {"iso3": "NZL", "structural_score": 90.5, "exposure_km": 18000, "nuclear_armed": False, "completeness": 0.9},
        {"iso3": "XXX", "structural_score": 99.0},
    ]}
    frame, missing = live_risk.to_frame(payload, {"CHE": "Switzerland", "NZL": "New Zealand", "ISL": "Iceland"})
    assert list(frame["Country"]) == ["New Zealand", "Switzerland"]
    assert missing == ["Iceland"]
    assert set(live_risk.SCENARIO_SLUGS) == {"1", "2", "3", "4", "5", "6"}
