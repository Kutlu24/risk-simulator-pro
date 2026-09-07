# Globaler Risiko-Simulator

Ein interaktives Streamlit-Tool, das 19 Länder nach ihrer Widerstandsfähigkeit unter sechs verschiedenen globalen Krisenszenarien einordnet (z. B. ein Russland-NATO-Konflikt, ein Hormus-Energieschock, eine Klimakrise).

🇬🇧 English version: [README.md](README.md)

## Was das Tool macht

- Bewertet jedes Land anhand von 11 Widerstandsfähigkeits-Kriterien (geografische Isolation, nukleares Risiko, politische Neutralität, wirtschaftliche Resilienz, Energieunabhängigkeit, Cybersicherheit u. a.).
- Sechs vordefinierte Krisenszenarien gewichten diese 11 Kriterien unterschiedlich, sodass dieselben Länderdaten je nach gewähltem Szenario ein anderes Ranking ergeben.
- Zeigt das Ranking als Tabelle und Balkendiagramm, mit einer kurzen Erklärung, warum das jeweilige Szenario bestimmte Länder begünstigt.

## Technik

Python, [Streamlit](https://streamlit.io/), pandas. Alle Länder-/Kriteriendaten sind fest im Skript hinterlegt — keine externe API oder CSV.

## Ausführen

```bash
pip install -r requirements.txt
streamlit run risk_simulator_app.py
```

## Hinweis

Die Länderbewertungen sind illustrative Schätzwerte zur Szenario-Erkundung, kein belastbares geopolitisches Risikomodell.
