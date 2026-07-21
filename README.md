# 🌡️ AeroIntel — Smart City Environmental Intelligence

AeroIntel is a Streamlit dashboard that turns live weather and air-quality data into
actionable, city-specific pollution intelligence for 15 major Indian metros. It combines
a real-time monitoring map, a Gaussian-plume dispersion model, a simulated multi-agent
source-attribution engine, a policy "what-if" simulator, an enforcement dispatch console,
and multilingual citizen health advisories — all in one app.

## ✨ Features

- **Live Dashboard & Plume Map** — Pulls live PM2.5, PM10, and meteorological data
  (temperature, humidity, wind speed/direction) from the Open-Meteo API and renders it
  on an interactive Folium map with a pollution heatmap layer.
- **AI Agent Source Attribution** — A simulated multi-agent "debate" (meteorological,
  geospatial, public health, and consensus agents) that reasons over live conditions to
  estimate what fraction of local pollution comes from traffic, industry, construction
  dust, or biomass/waste burning, and produces a confidence score.
- **Forecasting & Policy Simulator** — A Gaussian plume dispersion model over known
  emission hotspots per city, letting you simulate the effect of interventions (e.g.
  restricting diesel traffic, throttling industrial output, halting construction, or
  suppressing waste burning) on the pollution grid.
- **Enforcement & Dispatch Console** — Converts source attribution into prioritized,
  city-specific enforcement actions addressed to the real local authorities (e.g. DPCC,
  MPCB, BBMP, traffic police, municipal corporations).
- **Citizen Health Risk Advisory** — Generates localized, multilingual (10 Indian
  languages, including Hindi, Tamil, Kannada, Bengali, Telugu, Gujarati, Malayalam, and
  Assamese) health advisories, SMS text, and IVR scripts based on current AQI and
  dominant pollution source.
- **15 Cities Covered** — Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Pune,
  Ahmedabad, Jaipur, Lucknow, Bhopal, Patna, Chandigarh, Kochi, and Guwahati, each with
  its own emission sources, wards, vulnerability scores, and governing authorities.

## 🗂️ Project Structure

```
urban_air_quality/
├── app.py                # Streamlit UI, page layout, and view routing
├── data_fetcher.py        # Live data retrieval from Open-Meteo + Indian AQI calculation
├── dispersion_model.py     # Gaussian plume dispersion model & emission source registry
├── agents.py              # Simulated multi-agent source attribution & enforcement recs
├── i18n.py                 # Multilingual advisory templates and translations
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Internet access (the app fetches live data from the [Open-Meteo](https://open-meteo.com/) API)

### Installation

```bash
git clone <this-repo-url>
cd urban_air_quality
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

The app will open in your browser, typically at `http://localhost:8501`.

## 🧪 How It Works

1. **Data ingestion** — `data_fetcher.py` calls the Open-Meteo air-quality and weather
   forecast APIs for the selected city, merges them into a single time-indexed
   DataFrame, and derives an approximate Indian CPCB AQI from PM2.5/PM10 breakpoints.
2. **Dispersion modeling** — `dispersion_model.py` applies a Gaussian plume equation
   over each city's known emission sources (industrial stacks, landfills, construction
   sites, traffic corridors) to estimate a 25×25 pollution concentration grid, adjusted
   for current wind speed and direction.
3. **Source attribution** — `agents.py` synthesizes live meteorological and pollutant
   readings into a source-attribution breakdown (traffic, industrial, construction,
   biomass, dust) and a narrated "agent dialogue," then generates enforcement
   recommendations addressed to the real local pollution control board, traffic police,
   and municipal authority for that city.
4. **Localization** — `i18n.py` builds fully-translated advisory messages (not just
   partial strings) in the citizen's regional language, filling in live data such as
   AQI category, dominant source, and hotspot ward.

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — app framework
- [Folium](https://python-visualization.github.io/folium/) + `streamlit-folium` — interactive maps
- [Plotly](https://plotly.com/python/) — charts
- [Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) — data processing
- [Open-Meteo](https://open-meteo.com/) — live weather & air-quality data source

## ⚠️ Disclaimer

Source attribution percentages, dispersion grids, and agent dialogue in this project are
**simulated/heuristic estimates** for demonstration purposes, built on top of live
meteorological data — they are not certified regulatory measurements. Do not use this
tool as the sole basis for real enforcement or public health decisions.


