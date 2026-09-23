# Globaler Risiko-Simulator

Ein interaktives Streamlit-Tool, das 19 Länder nach ihrer Widerstandsfähigkeit unter sechs verschiedenen globalen Krisenszenarien einordnet (z. B. ein Russland-NATO-Konflikt, ein Hormus-Energieschock, eine Klimakrise).

🇬🇧 English version: [README.md](README.md)

## Was das Tool macht

- Bewertet jedes Land anhand von 11 Widerstandsfähigkeits-Kriterien (geografische Isolation, nukleares Risiko, politische Neutralität, wirtschaftliche Resilienz, Energieunabhängigkeit, Cybersicherheit u. a.).
- Sechs vordefinierte Krisenszenarien gewichten diese 11 Kriterien unterschiedlich, sodass dieselben Länderdaten je nach gewähltem Szenario ein anderes Ranking ergeben.
- Zeigt das Ranking als Tabelle, Balkendiagramm und Weltkarte (Choropleth), mit einer kurzen Erklärung, warum das jeweilige Szenario bestimmte Länder begünstigt.

## Geografische Ansicht

Unter Tabelle/Balkendiagramm färbt eine Weltkarte jedes der 19 Länder nach seinem gewichteten Score im gewählten Szenario (rot = verwundbar, grün = widerstandsfähig — dieselben Stufen wie die Badges in der Tabelle), sodass regionale Muster (z. B. "isolierte Länder der Südhalbkugel clustern hoch" beim Russland-NATO-Szenario) auf einen Blick sichtbar sind, statt Balken einzeln vergleichen zu müssen. Beim Hovern über ein gefärbtes Land erscheint der genaue Score. Gebaut mit [`folium`](https://python-visualization.github.io/folium/)/[`streamlit-folium`](https://github.com/randyzwitch/streamlit-folium); die Ländergrenzen stammen aus einer mitgelieferten Kopie von folium's eigener Referenz-`world-countries.json` (`data/`, ~250KB, damit die App zur Laufzeit nicht von einer externen URL abhängt), verknüpft über den ISO-3166-1-Alpha-3-Code (`COUNTRY_ISO3` in `risk_simulator_app.py`) — Länder außerhalb der 19 bewerteten haben schlicht keine Daten und erscheinen in der neutralen Kartenfarbe.

## Technik

Python, [Streamlit](https://streamlit.io/), pandas, folium/streamlit-folium. Alle Länder-/Kriteriendaten sind fest im Skript hinterlegt — keine externe API oder CSV.

## Ausführen

```bash
pip install -r requirements.txt
streamlit run risk_simulator_app.py
```

## Tests

```bash
pip install pytest
python -m pytest tests/
```

Deckt gezielt die Länderabdeckung der Karte ab: jedes bewertete Land hat einen ISO3-Code, jeder ISO3-Code existiert in der mitgelieferten GeoJSON, die gerenderte Karte enthält tatsächlich alle 19 Länder (keines fehlt durch einen stillen Namens-/Code-Mismatch), und ein nicht zugeordnetes Land löst einen klaren Fehler aus statt stillschweigend von der Karte zu verschwinden.

## Hinweis

Die Länderbewertungen sind illustrative Schätzwerte zur Szenario-Erkundung, kein belastbares geopolitisches Risikomodell.
