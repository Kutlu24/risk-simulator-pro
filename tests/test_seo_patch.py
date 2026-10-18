import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import seo_patch  # noqa: E402


def test_patch_injects_once(tmp_path):
    idx = tmp_path / "index.html"
    idx.write_text("<html><head><title>Streamlit</title></head><body><div id='root'></div></body></html>", encoding="utf-8")
    assert seo_patch.patch(idx, "https://x.example") is True
    text = idx.read_text(encoding="utf-8")
    assert 'rel="canonical" href="https://x.example/"' in text and "application/ld+json" in text
    assert "<noscript><h1>Global Risk Simulator" in text and "<title>Streamlit</title>" not in text
    assert seo_patch.patch(idx, "https://x.example") is False
    assert idx.read_text(encoding="utf-8") == text
