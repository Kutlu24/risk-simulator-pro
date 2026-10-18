"""Adds GEO/SEO tags to Streamlit's static index.html at startup.

Streamlit renders everything client-side, so crawlers that do not run JavaScript see an empty page.
This script (run before `streamlit run`, see render.yaml / Dockerfile) injects a title, description,
canonical, Open Graph tags, JSON-LD and a <noscript> about text. It is idempotent (marker comment).
The public origin comes from SITE_URL or Render's RENDER_EXTERNAL_URL.
"""
import html
import json
import os
import sys
from pathlib import Path

MARKER = "<!--seo-patch-->"
TITLE = "Global Risk Simulator: Country Resilience Ranking under Six Crisis Scenarios"
DESC = ("Interactive tool that ranks 19 countries by resilience on 11 criteria under six global-crisis scenarios "
        "such as a Russia-NATO conflict, a Hormuz energy shock or a climate crisis, with table, chart and world map.")
FAQ = [
    ("What does the Global Risk Simulator do?",
     "It scores 19 countries on 11 resilience criteria (for example geographic isolation, energy independence and cybersecurity) "
     "and re-weights the criteria for each of six crisis scenarios, so the ranking changes with the scenario."),
    ("Where does the data come from?",
     "All country scores are hand-entered assumptions stored in the script; there is no live data feed. Treat the ranking as an illustration, not a forecast."),
]


def build(site: str) -> tuple[str, str]:
    e = html.escape
    ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": "Global Risk Simulator", "description": DESC,
           "url": site, "applicationCategory": "EducationalApplication", "operatingSystem": "Any (web browser)",
           "isAccessibleForFree": True},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    head = [MARKER, f"<title>{e(TITLE)}</title>", f'<meta name="description" content="{e(DESC)}">',
            f'<meta property="og:title" content="{e(TITLE)}">', f'<meta property="og:description" content="{e(DESC)}">']
    if site:
        head += [f'<link rel="canonical" href="{e(site)}/">', f'<meta property="og:url" content="{e(site)}/">']
    head.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>")
    about = "<noscript><h1>Global Risk Simulator</h1><p>" + e(DESC) + "</p>" + "".join(
        f"<h2>{e(q)}</h2><p>{e(a)}</p>" for q, a in FAQ) + "</noscript>"
    return "\n".join(head), about


def patch(index: Path, site: str) -> bool:
    text = index.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    head, about = build(site)
    text = text.replace("<title>Streamlit</title>", "")  # the default title; ours replaces it
    text = text.replace("</head>", head + "\n</head>", 1).replace("<body>", "<body>" + about, 1)
    index.write_text(text, encoding="utf-8")
    return True


if __name__ == "__main__":
    import streamlit

    site = (os.environ.get("SITE_URL") or os.environ.get("RENDER_EXTERNAL_URL") or "").rstrip("/")
    idx = Path(streamlit.__file__).parent / "static" / "index.html"
    try:
        print("seo_patch:", "patched" if patch(idx, site) else "already patched", idx)
    except OSError as exc:  # never block startup because of SEO tags
        print("seo_patch: skipped:", exc, file=sys.stderr)
