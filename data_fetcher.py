import requests
import pandas as pd
import streamlit as st
from datetime import datetime

# Coordinates of 15 major Indian metro/tier-1 cities (was 5)
CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126},
    "Patna": {"lat": 25.5941, "lon": 85.1376},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
    "Kochi": {"lat": 9.9312, "lon": 76.2673},
    "Guwahati": {"lat": 26.1445, "lon": 91.7362},
}

@st.cache_data(ttl=3600)  # Cache API calls for 1 hour to prevent rate limiting
def fetch_live_data(city_name):
    """
    Fetches real-time and forecasted weather & air quality data from Open-Meteo APIs.
    Merges them into a clean pandas DataFrame.
    """
    if city_name not in CITIES:
        return None
    
    lat = CITIES[city_name]["lat"]
    lon = CITIES[city_name]["lon"]
    
    # 1. Fetch Air Quality Data
    aq_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    aq_params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi",
        "timezone": "Asia/Kolkata",
        "forecast_days": 3
    }
    
    # 2. Fetch Weather Data
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m",
        "timezone": "Asia/Kolkata",
        "forecast_days": 3
    }
    
    try:
        aq_res = requests.get(aq_url, params=aq_params, timeout=10)
        weather_res = requests.get(weather_url, params=weather_params, timeout=10)
        
        if aq_res.status_code != 200 or weather_res.status_code != 200:
            st.error(f"API Error. AQ Code: {aq_res.status_code}, Weather Code: {weather_res.status_code}")
            return None
            
        aq_data = aq_res.json()["hourly"]
        weather_data = weather_res.json()["hourly"]
        
        # Convert to DataFrames
        df_aq = pd.DataFrame(aq_data)
        df_weather = pd.DataFrame(weather_data)
        
        # Merge on time
        df = pd.merge(df_aq, df_weather, on="time")
        df["time"] = pd.to_datetime(df["time"])
        
        # Rename columns to standard readable format
        df.rename(columns={
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidity",
            "wind_speed_10m": "wind_speed",
            "wind_direction_10m": "wind_direction"
        }, inplace=True)
        
        # Calculate Indian AQI approximation (sub-index approximation from US AQI or raw PM2.5/PM10)
        # Indian AQI categories: 
        # 0-50 (Good), 51-100 (Satisfactory), 101-200 (Moderate), 201-300 (Poor), 301-400 (Very Poor), 401+ (Severe)
        df["aqi"] = df.apply(lambda row: calculate_indian_aqi(row["pm2_5"], row["pm10"]), axis=1)
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching data for {city_name}: {str(e)}")
        return None

def calculate_indian_aqi(pm25, pm10):
    """
    Approximates the Indian National Air Quality Index (AQI) based on CPCB break-points for PM2.5 and PM10.
    """
    # PM2.5 breakpoints: [0-30, 31-60, 61-90, 91-120, 121-250, 250+] -> AQI: [0-50, 51-100, 101-200, 201-300, 301-400, 401-500]
    # PM10 breakpoints: [0-50, 51-100, 101-250, 251-350, 351-430, 430+] -> AQI: [0-50, 51-100, 101-200, 201-300, 301-400, 401-500]
    
    def get_pm25_sub(v):
        if v <= 30: return (v * 50 / 30)
        elif v <= 60: return 50 + (v - 30) * 50 / 30
        elif v <= 90: return 100 + (v - 60) * 100 / 30
        elif v <= 120: return 200 + (v - 90) * 100 / 30
        elif v <= 250: return 300 + (v - 120) * 100 / 130
        else: return 400 + (v - 250) * 100 / 100
        
    def get_pm10_sub(v):
        if v <= 50: return (v * 50 / 50)
        elif v <= 100: return 50 + (v - 50) * 50 / 50
        elif v <= 250: return 100 + (v - 100) * 100 / 150
        elif v <= 350: return 200 + (v - 250) * 100 / 100
        elif v <= 430: return 300 + (v - 350) * 100 / 80
        else: return 400 + (v - 430) * 100 / 100
        
    sub_25 = get_pm25_sub(pm25) if pd.notna(pm25) else 0
    sub_10 = get_pm10_sub(pm10) if pd.notna(pm10) else 0
    
    return int(max(sub_25, sub_10))

def get_aqi_category(aqi):
    """Returns the CPCB AQI category and corresponding color hex."""
    if aqi <= 50:
        return "Good", "#00B050", "#E2F0D9"  # Category name, Text Color, Background Tint
    elif aqi <= 100:
        return "Satisfactory", "#92D050", "#EAF1DD"
    elif aqi <= 200:
        return "Moderate", "#FFC000", "#FFF2CC"
    elif aqi <= 300:
        return "Poor", "#FF0000", "#FCE4D6"
    elif aqi <= 400:
        return "Very Poor", "#7030A0", "#E1D5E7"
    else:
        return "Severe", "#C00000", "#FFC7CE"

def get_city_wards(city_name):
    """
    Returns localized mock wards for each city with center coordinates.
    This helps in generating 1km grid predictions and ward-level attributions.
    """
    wards = {
        "Delhi": [
            {"name": "Dwarka", "lat": 28.5889, "lon": 77.0583, "vulnerability": 7.5, "type": "Residential"},
            {"name": "Okhla Phase III", "lat": 28.5355, "lon": 77.2711, "vulnerability": 6.8, "type": "Industrial"},
            {"name": "Anand Vihar", "lat": 28.6473, "lon": 77.3158, "vulnerability": 9.2, "type": "Traffic Choke"},
            {"name": "Punjabi Bagh", "lat": 28.6678, "lon": 77.1332, "vulnerability": 8.0, "type": "Residential"},
            {"name": "Bawana", "lat": 28.7981, "lon": 77.0427, "vulnerability": 5.5, "type": "Industrial"},
            {"name": "Connaught Place", "lat": 28.6304, "lon": 77.2177, "vulnerability": 8.5, "type": "Commercial"},
            {"name": "R K Puram", "lat": 28.5660, "lon": 77.1744, "vulnerability": 7.8, "type": "Residential"},
            {"name": "Jahangirpuri", "lat": 28.7264, "lon": 77.1691, "vulnerability": 9.0, "type": "Waste Burn/Industrial"}
        ],
        "Mumbai": [
            {"name": "Bandra West", "lat": 19.0596, "lon": 72.8295, "vulnerability": 8.0, "type": "Residential/Coastal"},
            {"name": "Chembur", "lat": 19.0618, "lon": 72.8992, "vulnerability": 7.2, "type": "Industrial"},
            {"name": "Dharavi", "lat": 19.0380, "lon": 72.8538, "vulnerability": 9.5, "type": "High Density Residential"},
            {"name": "Andheri East", "lat": 19.1176, "lon": 72.8631, "vulnerability": 8.2, "type": "Commercial/Traffic"},
            {"name": "Deonar", "lat": 19.0430, "lon": 72.9230, "vulnerability": 8.8, "type": "Landfill/Waste Burning"},
            {"name": "Colaba", "lat": 18.9067, "lon": 72.8147, "vulnerability": 6.5, "type": "Residential/Coastal"},
            {"name": "Mulund", "lat": 19.1726, "lon": 72.9565, "vulnerability": 7.0, "type": "Residential"},
            {"name": "Sion", "lat": 19.0390, "lon": 72.8619, "vulnerability": 8.6, "type": "Traffic Hub"}
        ],
        "Bengaluru": [
            {"name": "Whitefield", "lat": 12.9698, "lon": 77.7500, "vulnerability": 7.8, "type": "Tech Hub/Construction"},
            {"name": "Mahadevapura", "lat": 12.9890, "lon": 77.6890, "vulnerability": 8.2, "type": "Industrial/Traffic"},
            {"name": "Peenya", "lat": 13.0285, "lon": 77.5195, "vulnerability": 6.5, "type": "Heavy Industrial"},
            {"name": "Silk Board Junction", "lat": 12.9176, "lon": 77.6244, "vulnerability": 9.4, "type": "Severe Traffic Choke"},
            {"name": "Jayanagar", "lat": 12.9275, "lon": 77.5906, "vulnerability": 8.5, "type": "Residential/Green"},
            {"name": "Kengeri", "lat": 12.9090, "lon": 77.4853, "vulnerability": 6.8, "type": "Residential/Industrial"},
            {"name": "Hebbal", "lat": 13.0359, "lon": 77.5970, "vulnerability": 8.0, "type": "Traffic/Construction"},
            {"name": "Malleshwaram", "lat": 13.0031, "lon": 77.5682, "vulnerability": 7.9, "type": "Residential/Commercial"}
        ],
        "Chennai": [
            {"name": "Manali", "lat": 13.1670, "lon": 80.2600, "vulnerability": 6.0, "type": "Refinery/Industrial"},
            {"name": "T Nagar", "lat": 13.0418, "lon": 80.2341, "vulnerability": 9.0, "type": "Dense Commercial"},
            {"name": "Velachery", "lat": 12.9815, "lon": 80.2180, "vulnerability": 7.8, "type": "Residential/Construction"},
            {"name": "Ennore", "lat": 13.2161, "lon": 80.3247, "vulnerability": 6.5, "type": "Thermal Power Plant"},
            {"name": "Guindy", "lat": 13.0067, "lon": 80.2206, "vulnerability": 8.2, "type": "Industrial/Transit"},
            {"name": "Adyar", "lat": 13.0063, "lon": 80.2574, "vulnerability": 7.5, "type": "Residential/Green"},
            {"name": "Royapuram", "lat": 13.1146, "lon": 80.2922, "vulnerability": 8.5, "type": "Coastal/High Density"}
        ],
        "Kolkata": [
            {"name": "Howrah", "lat": 22.5785, "lon": 88.3102, "vulnerability": 9.0, "type": "Industrial/Traffic Hub"},
            {"name": "Salt Lake Sector V", "lat": 22.5735, "lon": 88.4331, "vulnerability": 8.0, "type": "Commercial/IT Hub"},
            {"name": "Ballygunge", "lat": 22.5280, "lon": 88.3659, "vulnerability": 8.5, "type": "Residential"},
            {"name": "Jadavpur", "lat": 22.4990, "lon": 88.3710, "vulnerability": 7.8, "type": "Institutional/Residential"},
            {"name": "Victoria Memorial Area", "lat": 22.5448, "lon": 88.3425, "vulnerability": 6.0, "type": "Green Buffer Zone"},
            {"name": "Behala", "lat": 22.4988, "lon": 88.3150, "vulnerability": 8.3, "type": "High Density Residential"},
            {"name": "Cossipore", "lat": 22.6178, "lon": 88.3712, "vulnerability": 7.2, "type": "Industrial/Freight"}
        ],
        "Hyderabad": [
            {"name": "Patancheru", "lat": 17.5322, "lon": 78.2665, "vulnerability": 8.4, "type": "Heavy Industrial"},
            {"name": "HITEC City", "lat": 17.4435, "lon": 78.3772, "vulnerability": 7.6, "type": "IT/Commercial Traffic"},
            {"name": "Uppal", "lat": 17.4064, "lon": 78.5590, "vulnerability": 7.2, "type": "Construction/Residential"},
            {"name": "Balanagar", "lat": 17.4586, "lon": 78.4380, "vulnerability": 8.0, "type": "Industrial"},
            {"name": "Secunderabad", "lat": 17.4399, "lon": 78.4983, "vulnerability": 7.5, "type": "Traffic Hub/Commercial"}
        ],
        "Pune": [
            {"name": "Pimpri-Chinchwad", "lat": 18.6298, "lon": 73.7997, "vulnerability": 8.6, "type": "Heavy Industrial"},
            {"name": "Hinjewadi", "lat": 18.5912, "lon": 73.7389, "vulnerability": 7.4, "type": "IT Corridor/Traffic"},
            {"name": "Wagholi", "lat": 18.5793, "lon": 73.9846, "vulnerability": 7.0, "type": "Construction/Residential"},
            {"name": "Katraj", "lat": 18.4575, "lon": 73.8668, "vulnerability": 6.8, "type": "Residential/Traffic"},
            {"name": "Shivajinagar", "lat": 18.5308, "lon": 73.8475, "vulnerability": 7.9, "type": "Commercial/Traffic Choke"}
        ],
        "Ahmedabad": [
            {"name": "Naroda", "lat": 23.0731, "lon": 72.6636, "vulnerability": 8.8, "type": "Industrial Estate"},
            {"name": "Odhav", "lat": 23.0339, "lon": 72.6663, "vulnerability": 8.2, "type": "Industrial/Chemical"},
            {"name": "Bopal", "lat": 23.0339, "lon": 72.4695, "vulnerability": 6.5, "type": "Construction/Residential"},
            {"name": "Vastrapur", "lat": 23.0367, "lon": 72.5300, "vulnerability": 6.0, "type": "Residential"},
            {"name": "Maninagar", "lat": 22.9963, "lon": 72.6081, "vulnerability": 7.6, "type": "Traffic/Commercial"}
        ],
        "Jaipur": [
            {"name": "Sanganer", "lat": 26.8199, "lon": 75.8020, "vulnerability": 7.8, "type": "Textile/Dyeing Industrial"},
            {"name": "Jhotwara", "lat": 26.9500, "lon": 75.7400, "vulnerability": 7.5, "type": "Industrial Area"},
            {"name": "Malviya Nagar", "lat": 26.8535, "lon": 75.8060, "vulnerability": 6.8, "type": "Residential"},
            {"name": "Vidhyadhar Nagar", "lat": 26.9530, "lon": 75.7700, "vulnerability": 6.5, "type": "Residential"},
            {"name": "Mansarovar", "lat": 26.8628, "lon": 75.7461, "vulnerability": 7.0, "type": "Traffic/Commercial"}
        ],
        "Lucknow": [
            {"name": "Talkatora", "lat": 26.8398, "lon": 80.8890, "vulnerability": 7.9, "type": "Industrial Area"},
            {"name": "Alambagh", "lat": 26.8103, "lon": 80.9106, "vulnerability": 7.6, "type": "Transit Hub"},
            {"name": "Gomti Nagar", "lat": 26.8467, "lon": 81.0140, "vulnerability": 6.5, "type": "Residential/Commercial"},
            {"name": "Chinhat", "lat": 26.8890, "lon": 81.0210, "vulnerability": 7.2, "type": "Brick Kiln/Dust Belt"},
            {"name": "Aliganj", "lat": 26.8890, "lon": 80.9280, "vulnerability": 6.8, "type": "Residential"}
        ],
        "Bhopal": [
            {"name": "Govindpura", "lat": 23.2408, "lon": 77.4600, "vulnerability": 7.8, "type": "Industrial Estate"},
            {"name": "Kolar Road", "lat": 23.1500, "lon": 77.4200, "vulnerability": 6.9, "type": "Construction Belt"},
            {"name": "MP Nagar", "lat": 23.2350, "lon": 77.4340, "vulnerability": 7.2, "type": "Commercial/Traffic Choke"},
            {"name": "Bairagarh", "lat": 23.2649, "lon": 77.3487, "vulnerability": 6.5, "type": "Residential/Industrial"},
            {"name": "Habibganj", "lat": 23.2266, "lon": 77.4362, "vulnerability": 6.7, "type": "Transit Hub"}
        ],
        "Patna": [
            {"name": "Phulwari Sharif", "lat": 25.5833, "lon": 85.0833, "vulnerability": 7.6, "type": "Industrial Area"},
            {"name": "Danapur", "lat": 25.6350, "lon": 85.0450, "vulnerability": 7.2, "type": "Rail Freight/Diesel"},
            {"name": "Patliputra", "lat": 25.6127, "lon": 85.1010, "vulnerability": 6.5, "type": "Construction/Residential"},
            {"name": "Rajendra Nagar", "lat": 25.6100, "lon": 85.1400, "vulnerability": 7.0, "type": "Residential/Commercial"},
            {"name": "Kankarbagh", "lat": 25.5883, "lon": 85.1450, "vulnerability": 7.4, "type": "High Density Residential"}
        ],
        "Chandigarh": [
            {"name": "Industrial Area Phase I", "lat": 30.7046, "lon": 76.8060, "vulnerability": 7.0, "type": "Industrial Estate"},
            {"name": "Sector 17", "lat": 30.7410, "lon": 76.7822, "vulnerability": 6.5, "type": "Commercial/Traffic"},
            {"name": "Manimajra", "lat": 30.7275, "lon": 76.8419, "vulnerability": 6.8, "type": "Construction/Residential"},
            {"name": "Sector 22", "lat": 30.7350, "lon": 76.7770, "vulnerability": 6.0, "type": "Residential"},
            {"name": "Sector 38 West", "lat": 30.7280, "lon": 76.7560, "vulnerability": 6.3, "type": "Residential/Commercial"}
        ],
        "Kochi": [
            {"name": "Eloor-Edayar", "lat": 10.0500, "lon": 76.3050, "vulnerability": 8.6, "type": "Heavy Chemical/Industrial"},
            {"name": "Vyttila", "lat": 9.9680, "lon": 76.3190, "vulnerability": 7.4, "type": "Traffic Junction"},
            {"name": "Kakkanad", "lat": 10.0159, "lon": 76.3419, "vulnerability": 6.8, "type": "IT Corridor/Construction"},
            {"name": "Fort Kochi", "lat": 9.9658, "lon": 76.2422, "vulnerability": 5.5, "type": "Coastal/Residential"},
            {"name": "Edappally", "lat": 10.0236, "lon": 76.3084, "vulnerability": 7.0, "type": "Commercial/Traffic"}
        ],
        "Guwahati": [
            {"name": "Noonmati", "lat": 26.1867, "lon": 91.7789, "vulnerability": 8.2, "type": "Oil Refinery/Industrial"},
            {"name": "Maligaon", "lat": 26.1544, "lon": 91.6398, "vulnerability": 7.5, "type": "Rail Yard/Diesel"},
            {"name": "Fancy Bazaar", "lat": 26.1875, "lon": 91.7458, "vulnerability": 7.0, "type": "Commercial/Traffic"},
            {"name": "Six Mile", "lat": 26.1310, "lon": 91.8010, "vulnerability": 6.5, "type": "Residential/Traffic"},
            {"name": "Beltola", "lat": 26.1200, "lon": 91.7900, "vulnerability": 6.2, "type": "Residential"}
        ]
    }
    return wards.get(city_name, [])
