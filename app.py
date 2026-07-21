import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import datetime

# Import local data and models
from data_fetcher import fetch_live_data, get_aqi_category, get_city_wards, CITIES
from dispersion_model import calculate_dispersion_grid, EMISSION_SOURCES
from agents import run_multi_agent_consensus, CITY_AUTHORITIES
from i18n import LANGUAGES, CITY_DEFAULT_LANG, build_advisory

# ==========================================
# PAGE CONFIG & PREMIUM CSS INJECTION
# ==========================================
st.set_page_config(
    page_title="AeroIntel | Smart City Environmental Intelligence",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Light, High-Contrast UI Styling
st.markdown("""
<style>
    /* Import fonts: Inter/Poppins for Latin text, Noto Sans for full Indic-script
       coverage (Devanagari, Kannada, Tamil, Bengali, Telugu, Gujarati, Malayalam)
       so translated advisories always render with correct glyphs instead of
       falling back to tofu boxes or mismatched system fonts. */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&family=Noto+Sans:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&family=Noto+Sans+Kannada:wght@400;600;700&family=Noto+Sans+Tamil:wght@400;600;700&family=Noto+Sans+Bengali:wght@400;600;700&family=Noto+Sans+Telugu:wght@400;600;700&family=Noto+Sans+Gujarati:wght@400;600;700&family=Noto+Sans+Malayalam:wght@400;600;700&display=swap');

    /* Soft gradient backdrop instead of flat off-white — adds depth without
       sacrificing the light theme */
    .stApp {
        background: radial-gradient(circle at 0% 0%, #eef2ff 0%, #f4f6fa 32%, #f8fafc 100%) fixed;
        color: #1e293b;
        font-family: 'Inter', 'Noto Sans', 'Noto Sans Devanagari', 'Noto Sans Kannada',
                     'Noto Sans Tamil', 'Noto Sans Bengali', 'Noto Sans Telugu',
                     'Noto Sans Gujarati', 'Noto Sans Malayalam', sans-serif;
    }

    /* Any element carrying translated / non-Latin script content gets the
       Indic-aware font stack explicitly so text never renders truncated or
       with missing glyphs when the language is switched */
    .i18n-text, .i18n-text * {
        font-family: 'Noto Sans', 'Noto Sans Devanagari', 'Noto Sans Kannada',
                     'Noto Sans Tamil', 'Noto Sans Bengali', 'Noto Sans Telugu',
                     'Noto Sans Gujarati', 'Noto Sans Malayalam', 'Inter', sans-serif !important;
        white-space: normal !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
    }

    /* Sidebar styling (clean white, subtle gradient, soft border) */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #fbfcff 100%) !important;
        border-right: 1px solid rgba(15, 23, 42, 0.08);
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-family: 'Poppins', 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    h1 {
        background: linear-gradient(90deg, #1d4ed8 0%, #7c3aed 60%, #db2777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding-bottom: 4px;
    }

    /* Card styling: white cards with soft shadow + gentle hover lift */
    .glass-card {
        background: #ffffff;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.1);
    }

    .status-card {
        border-left: 5px solid #00B050;
    }

    /* custom badge */
    .custom-badge {
        display: inline-block;
        padding: 0.3em 0.75em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 10rem;
    }

    /* Metric styling — fluid font sizing + no clipping so units like
       "µg/m³" or longer translated labels never get cut off, regardless
       of screen width */
    div[data-testid="stMetric"] {
        background: linear-gradient(160deg, #ffffff 0%, #f8faff 100%);
        border: 1px solid rgba(15, 23, 42, 0.07);
        border-radius: 14px;
        padding: 14px 12px 10px 12px;
        overflow: visible !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    div[data-testid="stMetricValue"] {
        font-size: clamp(1.05rem, 1.1vw + 0.7rem, 2rem) !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.25 !important;
        word-break: keep-all;
    }
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: clamp(0.72rem, 0.35vw + 0.6rem, 0.9rem) !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.3 !important;
    }
    div[data-testid="stMetricDelta"] {
        white-space: normal !important;
        overflow: visible !important;
        font-size: clamp(0.68rem, 0.3vw + 0.55rem, 0.85rem) !important;
    }

    /* Custom button styling */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.35);
    }

    /* Chat bubbles for Agents */
    .agent-chat {
        padding: 12px 16px;
        border-radius: 14px;
        margin-bottom: 12px;
        border: 1px solid rgba(15, 23, 42, 0.06);
        background: #ffffff;
        transition: transform 0.15s ease;
    }
    .agent-chat:hover { transform: translateX(2px); }
    .agent-chat.meteo { background: rgba(59, 130, 246, 0.06); border-left: 4px solid #3b82f6; }
    .agent-chat.geo { background: rgba(168, 85, 247, 0.06); border-left: 4px solid #a855f7; }
    .agent-chat.health { background: rgba(239, 68, 68, 0.06); border-left: 4px solid #ef4444; }
    .agent-chat.consensus { background: rgba(16, 185, 129, 0.06); border-left: 4px solid #10b981; }

    /* Map frame: transparent so the basemap / page gradient shows through
       instead of a solid white card sitting on top of the map */
    div[data-testid="stIFrame"] {
        border-radius: 16px;
        border: 1px solid rgba(15, 23, 42, 0.1);
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.08);
        background: transparent !important;
    }
    div[data-testid="stIFrame"] iframe {
        background: transparent !important;
    }
    .leaflet-container {
        background: transparent !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #c7d2fe; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #a5b4fc; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# STATE MANAGEMENT
# ==========================================
if "dispatched_tickets" not in st.session_state:
    st.session_state["dispatched_tickets"] = set()
if "dispatch_log" not in st.session_state:
    st.session_state["dispatch_log"] = []
if "inspections_logged" not in st.session_state:
    st.session_state["inspections_logged"] = 0

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #3b82f6;'>AeroIntel Command</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #64748b; font-size:0.85rem;'>Smart City Environmental Intelligence</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

selected_city = st.sidebar.selectbox("🎯 Target Urban Center", list(CITIES.keys()))
active_view = st.sidebar.radio("🗺️ Control Rooms", [
    "Live Dashboard & Plume Map",
    "AI Agent Source Attribution",
    "Forecasting & Policy Simulator",
    "Enforcement & Dispatch Console",
    "Citizen Health Risk Advisory"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### Map Layers")
map_tiles = st.sidebar.selectbox("🗺️ Map Base Layer", [
    "CartoDB Positron (Light/Visible)",
    "OpenStreetMap (Standard Roads)",
    "CartoDB Dark Matter (Dark Mode)"
], index=0)
plume_opacity = st.sidebar.slider(
    "🎚️ Plume Layer Transparency", 0.10, 0.80, 0.30, step=0.05,
    help="Lower values make the pollution heatmap more transparent so the basemap underneath stays visible."
)

#st.sidebar.markdown("---")
#st.sidebar.markdown("### Active Interventions")
#st.sidebar.metric("Active Patrols/Sprinklers", len(st.session_state["dispatched_tickets"]))
#st.sidebar.metric("Inspections Completed", st.session_state["inspections_logged"])

# ==========================================
# DATA RETRIEVAL (LIVE API CONNECTION)
# ==========================================
with st.spinner("Connecting to Open-Meteo Environmental Sensors..."):
    df = fetch_live_data(selected_city)

if df is None:
    st.error("Unable to contact live air sensors. Please verify network connection.")
    st.stop()

# Get latest hourly data (current hour)
current_time = datetime.datetime.now()
df_current = df[df["time"] <= current_time]
if df_current.empty:
    df_current = df.iloc[[0]]
else:
    df_current = df_current.iloc[[-1]]

live_row = df_current.iloc[0]
live_aqi = int(live_row["aqi"])
live_pm25 = float(live_row["pm2_5"])
live_pm10 = float(live_row["pm10"])
live_co = float(live_row["carbon_monoxide"])
live_no2 = float(live_row["nitrogen_dioxide"])
live_so2 = float(live_row["sulphur_dioxide"])
live_o3 = float(live_row["ozone"])
live_temp = float(live_row["temperature"])
live_humidity = float(live_row["humidity"])
live_wind_spd = float(live_row["wind_speed"])
live_wind_dir = float(live_row["wind_direction"])

aqi_cat, aqi_color, aqi_bg = get_aqi_category(live_aqi)

# ==========================================
# ROOM 1: LIVE DASHBOARD & PLUME MAP
# ==========================================
if active_view == "Live Dashboard & Plume Map":
    st.markdown(f"# 🗺️ Smart Command Center: {selected_city} Metros")
    st.markdown("Fusing live regulatory CAAQMS sensors, local wind vectors, and dispersion modeling grids.")

    # 1. Live Stats Row
    cols = st.columns(6)
    
    with cols[0]:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 5px solid {aqi_color}; padding: 15px;">
            <p style="margin:0; font-size:0.8rem; color:#64748b;">AQI STATUS</p>
            <h2 style="margin:5px 0; color:{aqi_color} !important;">{live_aqi}</h2>
            <span class="custom-badge" style="background:{aqi_bg}; color:{aqi_color};">{aqi_cat}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[1]:
        st.metric("PM2.5 (Fine dust)", f"{live_pm25:.1f} µg/m³")
    with cols[2]:
        st.metric("PM10 (Coarse dust)", f"{live_pm10:.1f} µg/m³")
    with cols[3]:
        st.metric("NO₂ (Exhaust)", f"{live_no2:.1f} µg/m³")
    with cols[4]:
        st.metric("SO₂ (Industrial)", f"{live_so2:.1f} µg/m³")
    with cols[5]:
        # Wind arrow calculation
        directions = ["↑ N", "↗ NE", "→ E", "↘ SE", "↓ S", "↙ SW", "← W", "↖ NW"]
        dir_idx = int(((live_wind_dir + 22.5) % 360) / 45)
        st.metric("Wind Vector", f"{live_wind_spd:.1f} km/h", f"Blows from {directions[dir_idx]} ({live_wind_dir}°)")

    # 2. Main Map Layout
    col_map, col_details = st.columns([3, 1])
    
    with col_map:
        map_frame = st.container(border=True)
        map_frame.markdown("### 🗺️ Live 1km Dispersion Grid Overlay (Gaussian Plume Simulation)")
        
        # Calculate dispersion grid based on live weather parameters
        city_center = CITIES[selected_city]
        
        # Pull active policy reductions from session state if any
        reductions = {}
        if "active_traffic_reduction" in st.session_state:
            reductions["Traffic"] = st.session_state["active_traffic_reduction"]
        if "active_ind_reduction" in st.session_state:
            reductions["Industrial"] = st.session_state["active_ind_reduction"]
        if "active_const_reduction" in st.session_state:
            reductions["Construction"] = st.session_state["active_const_reduction"]
            
        grid = calculate_dispersion_grid(
            selected_city, 
            city_center["lat"], 
            city_center["lon"], 
            live_wind_spd, 
            live_wind_dir, 
            live_pm25,  # background PM2.5
            reductions
        )
        
        # Build Folium Map with selectable tile layer for high visibility
        tile_dict = {
            "CartoDB Positron (Light/Visible)": "CartoDB positron",
            "OpenStreetMap (Standard Roads)": "OpenStreetMap",
            "CartoDB Dark Matter (Dark Mode)": "CartoDB dark_matter"
        }
        m = folium.Map(location=[city_center["lat"], city_center["lon"]], zoom_start=12, tiles=tile_dict[map_tiles])
        
        # 1. Add Heatmap representation of dispersion
        # Softer, lighter pastel gradient (was saturated teal/red/purple) so the
        # plume overlay matches the light UI theme instead of looking heavy/dark,
        # while keeping the same low->high severity color order.
        if grid:
            heat_data = [[p["lat"], p["lon"], p["pm2_5"]] for p in grid]
            HeatMap(
                heat_data, 
                radius=22, 
                blur=18, 
                max_zoom=13,
                min_opacity=plume_opacity,
                gradient={0.1: '#a7f3d0', 0.2: '#bef264', 0.4: '#fde68a', 0.7: '#fdba74', 0.9: '#fca5a5', 1.0: '#e9d5ff'}
            ).add_to(m)
            
        # 2. Add CAAQMS Stations
        wards = get_city_wards(selected_city)
        for w in wards:
            # Shift coordinate slightly to represent station near ward center
            w_lat, w_lon = w["lat"] + 0.005, w["lon"] - 0.005
            w_aqi = int(live_aqi * (w["vulnerability"] / 7.5)) # Mock local variation
            _, w_color, _ = get_aqi_category(w_aqi)
            
            # Draw marker with a white halo/outline so it stands out clearly on any basemap
            folium.CircleMarker(
                location=[w_lat, w_lon],
                radius=9,
                popup=f"<b>CAAQMS Station: {w['name']}</b><br>AQI: {w_aqi}<br>PM2.5: {int(w_aqi * 0.45)} µg/m³",
                color="#ffffff",
                weight=2,
                fill=True,
                fill_color=w_color,
                fill_opacity=0.75
            ).add_to(m)
            
        # 3. Add Emission Hotspots
        sources = EMISSION_SOURCES.get(selected_city, [])
        for s in sources:
            source_icon = 'industry' if 'Industrial' in s['type'] or 'Power' in s['type'] else 'truck' if 'Traffic' in s['type'] else 'fire'
            folium.Marker(
                location=[s["lat"], s["lon"]],
                popup=f"<b>Source: {s['name']}</b><br>Type: {s['type']}<br>Height: {s['H']}m<br>Strength (Q): {s['Q']} ug/s",
                icon=folium.Icon(color='red' if s["Q"] > 1000 else 'orange', icon=source_icon, prefix='fa')
            ).add_to(m)
            
        # Display Map (rendered inside the bordered frame for a clear visual boundary)
        with map_frame:
            st_folium(m, width="100%", height=600)
        
    with col_details:
        st.markdown("### Map Legend & Metrics")
        st.markdown("""
        **Plume Heatmap Intensity:**
        - 🟢 **Green (5-30 µg/m³)**: Low impact grid cell.
        - 🟡 **Yellow (31-60 µg/m³)**: Satisfactory.
        - 🟠 **Orange (61-120 µg/m³)**: High particulate load.
        - 🔴 **Red (121-250 µg/m³)**: Severe plume footprint.
        - 🟣 **Purple (>250 µg/m³)**: Direct stack centerline.
        """)
        
        st.markdown("---")
        st.markdown("### Registered Local Sources")
        for s in sources:
            icon = "🏭" if 'Industrial' in s['type'] or 'Power' in s['type'] else "🚛" if 'Traffic' in s['type'] else "🔥"
            st.markdown(f"**{icon} {s['name']}**")
            st.markdown(f"<span style='font-size:0.8rem; color:#64748b;'>Type: {s['type']} | Stack Height: {s['H']}m</span>", unsafe_allow_html=True)
            st.progress(min(s["Q"] / 2500, 1.0))
            st.markdown("---")

# ==========================================
# ROOM 2: AI AGENT SOURCE ATTRIBUTION
# ==========================================
elif active_view == "AI Agent Source Attribution":
    st.markdown(f"# 🛰️ Source Attribution Engine: {selected_city}")
    st.markdown("Multi-Agent AI analysis modeling spatial-temporal air quality dynamics.")
    
    # Run agent consensus reasoning
    dialogue, attribution, confidence, recs = run_multi_agent_consensus(
        selected_city, live_temp, live_humidity, live_wind_spd, live_wind_dir, live_pm25, live_pm10, live_aqi
    )
    
    col_chart, col_chat = st.columns([1, 1])
    
    with col_chart:
        st.markdown(f"### Spatial Attribution Consensus")
        st.markdown(f"**Overall Confidence Score: `{confidence}%`** (Calculated based on wind vector and sensor reliability)")
        
        # Plotly Pie Chart
        fig = px.pie(
            names=list(attribution.keys()),
            values=list(attribution.values()),
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Plasma_r,
            title="Aerosol Fingerprint Breakdown"
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e293b',
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Plotly Bar Chart showing confidence intervals
        st.markdown("### Attribution Confidence Margin")
        categories = list(attribution.keys())
        percentages = list(attribution.values())
        errors = [max(1.0, float(val) * 0.08) for val in percentages]  # Mock 8% error margin
        
        fig_bar = go.Figure(data=[
            go.Bar(
                name='Contribution',
                x=categories,
                y=percentages,
                error_y=dict(type='data', array=errors, visible=True),
                marker_color='#3b82f6'
            )
        ])
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#1e293b',
            xaxis=dict(showgrid=False),
            yaxis=dict(title='Percentage %', showgrid=True, gridcolor='rgba(15,23,42,0.08)')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_chat:
        st.markdown("### Multi-Agent Debate Logs")
        
        # Agent conversations formatted in bubbles
        for msg in dialogue:
            sender = msg["sender"]
            avatar = msg["avatar"]
            txt = msg["message"]
            
            bubble_class = "consensus"
            if "Meteorological" in sender:
                bubble_class = "meteo"
            elif "Geospatial" in sender:
                bubble_class = "geo"
            elif "Vulnerability" in sender:
                bubble_class = "health"
                
            st.markdown(f"""
            <div class="agent-chat {bubble_class}">
                <div style="font-weight: 700; margin-bottom: 5px; color: #0f172a;">{avatar} {sender}</div>
                <div style="font-size: 0.9rem; line-height: 1.5;">{txt}</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# ROOM 3: FORECASTING & POLICY SIMULATOR
# ==========================================
elif active_view == "Forecasting & Policy Simulator":
    st.markdown(f"# 🧪 Proactive Policy Simulator & Forecasts: {selected_city}")
    st.markdown("Test municipal policies in real-time and observe the immediate simulated drop in the 72-hour AQI projection.")
    
    # 1. Timeline & Forecast Graphs
    st.markdown("### Business-As-Usual (BAU) 72h AQI Forecast")
    
    # Fetch 72 hours of forecast data
    times = df["time"]
    pm25_forecast = df["pm2_5"]
    pm10_forecast = df["pm10"]
    wind_forecast = df["wind_speed"]
    
    # Policy controls in a row
    st.markdown("### Enact Administrative Interventions")
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    
    with col_p1:
        traffic_red = st.slider("🚛 Restrict Diesel & Transit", 0, 100, 0, step=10, key="traffic_slider") / 100
        st.session_state["active_traffic_reduction"] = traffic_red
        
    with col_p2:
        ind_red = st.slider("🏭 Throttle Industrial Output", 0, 100, 0, step=10, key="ind_slider") / 100
        st.session_state["active_ind_reduction"] = ind_red
        
    with col_p3:
        const_red = st.slider("🏗️ Halt Wards Construction", 0, 100, 0, step=10, key="const_slider") / 100
        st.session_state["active_const_reduction"] = const_red
        
    with col_p4:
        biomass_red = st.slider("🔥 Suppress Landfill Burning", 0, 100, 0, step=10, key="biomass_slider") / 100
        st.session_state["active_biomass_reduction"] = biomass_red
        
    # Calculate simulated reduction factor based on attribution and slider values
    # Run attribution to get baseline weights
    _, attribution, _, _ = run_multi_agent_consensus(
        selected_city, live_temp, live_humidity, live_wind_spd, live_wind_dir, live_pm25, live_pm10, live_aqi
    )
    
    # Map weights
    w_traffic = attribution["Traffic / Vehicular"] / 100
    w_ind = attribution["Industrial Stack Emissions"] / 100
    w_const = attribution["Construction Fugitive Dust"] / 100
    w_biomass = attribution["Biomass & Waste Burning"] / 100
    
    # Total reduction fraction for PM2.5
    total_reduction = (traffic_red * w_traffic) + (ind_red * w_ind) + (const_red * w_const) + (biomass_red * w_biomass)
    
    # Calculate simulated PM2.5 and PM10
    sim_pm25_forecast = pm25_forecast * (1.0 - total_reduction)
    
    # Back-calculate AQI for simulated values
    sim_aqi_forecast = [int(val * 2.2) for val in sim_pm25_forecast] # Simple scaling for plotting
    bau_aqi_forecast = [int(val * 2.2) for val in pm25_forecast]
    
    # Render interactive forecast comparison
    fig_forecast = go.Figure()
    
    # Business-As-Usual line
    fig_forecast.add_trace(go.Scatter(
        x=times, y=bau_aqi_forecast,
        mode='lines',
        name='Business As Usual (Forecast)',
        line=dict(color='#ef4444', width=2.5, dash='dot')
    ))
    
    # Enacted policy line
    fig_forecast.add_trace(go.Scatter(
        x=times, y=sim_aqi_forecast,
        mode='lines',
        name='Simulated Intervention Policy',
        line=dict(color='#10b981', width=3)
    ))
    
    fig_forecast.update_layout(
        title="72-Hour Projective AQI (Policy Effectiveness Comparison)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#1e293b',
        xaxis=dict(gridcolor='rgba(15,23,42,0.08)'),
        yaxis=dict(title='AQI', gridcolor='rgba(15,23,42,0.08)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Analysis metrics
    st.markdown("### Simulated Intervention Impact Analysis")
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        initial_peak = max(bau_aqi_forecast)
        simulated_peak = max(sim_aqi_forecast)
        st.metric("Peak AQI Over 72h", f"{simulated_peak}", f"-{initial_peak - simulated_peak} (BAU Peak: {initial_peak})", delta_color="inverse")
        
    with col_m2:
        reducted_perc = total_reduction * 100
        st.metric("Total PM2.5 Source Reduction", f"{reducted_perc:.1f} %", "Admin containment")
        
    with col_m3:
        projected_avg = int(np.mean(sim_aqi_forecast))
        st.metric("Average Forecasted AQI", f"{projected_avg}", f"-{int(np.mean(bau_aqi_forecast)) - projected_avg}", delta_color="inverse")

# ==========================================
# ROOM 4: ENFORCEMENT & DISPATCH CONSOLE
# ==========================================
elif active_view == "Enforcement & Dispatch Console":
    st.markdown(f"# 🚨 Enforcement Intelligence & Inspector Dispatch: {selected_city}")
    st.markdown("Identify localized emissions violations, assign priority ranking, and dispatch smart containment equipment.")
    
    _, _, _, recs = run_multi_agent_consensus(
        selected_city, live_temp, live_humidity, live_wind_spd, live_wind_dir, live_pm25, live_pm10, live_aqi
    )
    
    st.markdown("### Prioritized Enforcement Task List")
    
    # Render tickets
    for idx, rec in enumerate(recs):
        ticket_id = f"{selected_city[:3].upper()}-{idx+101}"
        
        is_dispatched = ticket_id in st.session_state["dispatched_tickets"]
        status_text = "🛡️ Active/Dispatched" if is_dispatched else "⚠️ Pending Intervention"
        card_border = "#10b981" if is_dispatched else "#ef4444"
        
        st.markdown(f"""
        <div class="glass-card" style="border-left: 6px solid {card_border}; padding: 15px; margin-bottom:15px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; font-size:1.1rem; color:#0f172a;">{rec['title']} (ID: {ticket_id})</span>
                <span class="custom-badge" style="background:rgba(15,23,42,0.04); color:{card_border}; border: 1px solid {card_border};">{status_text}</span>
            </div>
            <p style="margin: 8px 0 3px 0; color:#64748b; font-size:0.9rem;"><b>Priority Weight:</b> {rec['priority']} | <b>Source Category:</b> {rec['category']}</p>
            <p style="margin: 3px 0; color:#334155; font-size:0.95rem;"><b>Impact Assessment:</b> {rec['impact']}</p>
            <p style="margin: 3px 0; color:#475569; font-size:0.95rem;"><b>Recommended Enforcement Protocol:</b> {rec['action']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if not is_dispatched:
                if st.button(f"Dispatch Unit {ticket_id}", key=f"btn_{ticket_id}"):
                    st.session_state["dispatched_tickets"].add(ticket_id)
                    st.session_state["dispatch_log"].insert(0, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Dispatched enforcement patrol to {rec['title']}.")
                    st.rerun()
            else:
                if st.button(f"Log Inspection Report {ticket_id}", key=f"log_{ticket_id}"):
                    st.session_state["dispatched_tickets"].remove(ticket_id)
                    st.session_state["inspections_logged"] += 1
                    st.session_state["dispatch_log"].insert(0, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Completed audit inspection for {ticket_id}. Violation report registered.")
                    st.success(f"Inspection Report Logged for ticket {ticket_id}!")
                    st.rerun()
                    
        st.markdown("<br>", unsafe_allow_html=True)
        
    st.markdown("### Live Enforcement Activity Log")
    if st.session_state["dispatch_log"]:
        st.code("\n".join(st.session_state["dispatch_log"]), language="bash")
    else:
        st.info("No active operations dispatched yet today. Monitor pending items above to launch responses.")

# ==========================================
# ROOM 5: CITIZEN HEALTH RISK ADVISORY
# ==========================================
elif active_view == "Citizen Health Risk Advisory":
    st.markdown(f"# 📢 Public Health Risk & Advisory Console: {selected_city}")
    st.markdown("Automated advisories, personalized to this city's own pollution source, hotspot and most vulnerable ward, translated in regional languages for municipal broadcast.")

    # 1. Select Language — every language below has a FULL, self-consistent
    # translation (title, messages, SMS, IVR script, and UI labels), so
    # switching languages never leaves English text mixed in.
    lang_names = list(LANGUAGES.keys())
    default_lang_name = CITY_DEFAULT_LANG.get(selected_city, "English")
    default_lang_idx = lang_names.index(default_lang_name) if default_lang_name in lang_names else 0

    lang_name = st.selectbox("🌐 Select Translation Output", lang_names, index=default_lang_idx, key="advisory_lang_select")
    lang_code = LANGUAGES[lang_name]

    # 2. Pull this city's own data to personalize the advisory:
    #    - dominant pollution source (from the multi-agent attribution)
    #    - top emission hotspot (highest-strength registered source)
    #    - most vulnerable ward (highest vulnerability score)
    #    - local municipal authority name
    _, city_attrib, _, _ = run_multi_agent_consensus(
        selected_city, live_temp, live_humidity, live_wind_spd, live_wind_dir, live_pm25, live_pm10, live_aqi
    )
    dominant_source_en = max(city_attrib, key=city_attrib.get)

    city_sources = EMISSION_SOURCES.get(selected_city, [])
    hotspot_name = max(city_sources, key=lambda s: s["Q"])["name"] if city_sources else selected_city

    city_wards_list = get_city_wards(selected_city)
    top_ward_name = max(city_wards_list, key=lambda w: w["vulnerability"])["name"] if city_wards_list else selected_city

    municipal_name = CITY_AUTHORITIES.get(selected_city, {}).get("municipal", "Municipal Corporation")

    ad = build_advisory(
        lang_code, selected_city, live_aqi, aqi_cat, dominant_source_en,
        hotspot_name, top_ward_name, municipal_name
    )

    col_msg, col_vulnerable = st.columns([2, 1])

    with col_msg:
        st.markdown(f"""
        <div class="glass-card i18n-text" style="border-left: 5px solid {aqi_color};">
            <h3>📢 {ad['title']} ({lang_name})</h3>
            <p style="font-size:1.15rem; line-height:1.7; color:#0f172a;">
                {ad['severe'] if live_aqi > 200 else ad['moderate'] if live_aqi > 100 else ad['good']}
            </p>
            <hr style="border-color: rgba(15,23,42,0.1);">
            <h5>{ad['school_header']}</h5>
            <p>{ad['school_msg']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<div class='i18n-text'><h3>{ad['broadcast_header']}</h3></div>", unsafe_allow_html=True)
        st.text_area(ad["sms_label"], ad["sms"], height=90)
        st.text_area(ad["ivr_label"], ad["ivr"], height=110)

    with col_vulnerable:
        st.markdown(f"<div class='i18n-text'><h3>{ad['vulnerable_header']}</h3><p>{ad['vulnerable_desc']}</p></div>", unsafe_allow_html=True)

        for w in city_wards_list:
            vuln_score = w["vulnerability"]
            badge_color = "red" if vuln_score > 8.0 else "orange" if vuln_score > 6.5 else "green"
            st.markdown(f"""
            <div style="background: rgba(15,23,42,0.02); border: 1px solid rgba(15,23,42,0.08); padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#0f172a;">{w['name']}</span>
                    <span class="custom-badge" style="background:rgba(15,23,42,0.04); color:{badge_color}; border: 1px solid {badge_color};">Vuln: {vuln_score}/10</span>
                </div>
                <div class="i18n-text" style="font-size:0.8rem; color:#64748b; margin-top:4px;">{ad['zone_label']}: {w['type']}</div>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# FOOTER INFORMATION
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 0.8rem;'>"
    "AeroIntel Command Dashboard • Real-time Data powered by Open-Meteo Air Quality & Weather API • Gaussian Plume Model v2.4"
    "</p>", 
    unsafe_allow_html=True
)
