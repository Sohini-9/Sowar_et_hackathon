import numpy as np
import pandas as pd

# Define key emission sources for each city
EMISSION_SOURCES = {
    "Delhi": [
        {"name": "Anand Vihar Transit Hub", "lat": 28.6473, "lon": 77.3158, "Q": 850, "H": 5, "type": "Traffic/Road Dust"},
        {"name": "Okhla Industrial Area", "lat": 28.5355, "lon": 77.2711, "Q": 1200, "H": 45, "type": "Industrial Stack"},
        {"name": "Ghazipur Landfill", "lat": 28.6231, "lon": 77.3292, "Q": 950, "H": 10, "type": "Biomass/Waste Burning"},
        {"name": "Bawana Industrial Zone", "lat": 28.7981, "lon": 77.0427, "Q": 1500, "H": 60, "type": "Industrial Stack"}
    ],
    "Mumbai": [
        {"name": "Deonar Landfill", "lat": 19.0430, "lon": 72.9230, "Q": 1100, "H": 8, "type": "Biomass/Waste Burning"},
        {"name": "Chembur Refinery Cluster", "lat": 19.0150, "lon": 72.9050, "Q": 1800, "H": 80, "type": "Petrochemical Industrial"},
        {"name": "Sion Metro Construction Site", "lat": 19.0390, "lon": 72.8619, "Q": 700, "H": 4, "type": "Fugitive Construction Dust"},
        {"name": "JNPT Port Shipping Terminal", "lat": 18.9500, "lon": 72.9500, "Q": 1300, "H": 30, "type": "Marine Diesel Fleet"}
    ],
    "Bengaluru": [
        {"name": "Peenya Industrial Area", "lat": 13.0285, "lon": 77.5195, "Q": 1400, "H": 50, "type": "Heavy Industrial"},
        {"name": "Silk Board Transit Choke", "lat": 12.9176, "lon": 77.6244, "Q": 900, "H": 3, "type": "Vehicular/Traffic"},
        {"name": "Whitefield Construction Ward", "lat": 12.9698, "lon": 77.7500, "Q": 800, "H": 6, "type": "Construction/Fugitive Dust"},
        {"name": "Bellandur Waste Dump", "lat": 12.9304, "lon": 77.6784, "Q": 600, "H": 2, "type": "Waste Burning"}
    ],
    "Chennai": [
        {"name": "Manali Petrochem & Refinery", "lat": 13.1670, "lon": 80.2600, "Q": 2000, "H": 90, "type": "Industrial Stack"},
        {"name": "Ennore Thermal Power Plant", "lat": 13.2161, "lon": 80.3247, "Q": 2500, "H": 120, "type": "Coal Power Plant"},
        {"name": "T Nagar Commercial Choke", "lat": 13.0418, "lon": 80.2341, "Q": 800, "H": 3, "type": "High Density Vehicular"},
        {"name": "Guindy Industrial Estate", "lat": 13.0067, "lon": 80.2206, "Q": 950, "H": 35, "type": "Light Industrial"}
    ],
    "Kolkata": [
        {"name": "Howrah Freight Terminal", "lat": 22.5785, "lon": 88.3102, "Q": 1400, "H": 15, "type": "Diesel Freight/Dust"},
        {"name": "Cossipore Foundry Cluster", "lat": 22.6178, "lon": 88.3712, "Q": 1600, "H": 55, "type": "Metal Foundries/Coal"},
        {"name": "Dhapa Garbage Burning Ground", "lat": 22.5480, "lon": 88.4020, "Q": 1100, "H": 5, "type": "Biomass/Waste Burning"},
        {"name": "Salt Lake Bypass Construction", "lat": 22.5735, "lon": 88.4331, "Q": 650, "H": 5, "type": "Construction"}
    ],
    "Hyderabad": [
        {"name": "Patancheru Industrial Cluster", "lat": 17.5322, "lon": 78.2665, "Q": 1600, "H": 55, "type": "Industrial Stack"},
        {"name": "HITEC City Traffic Corridor", "lat": 17.4435, "lon": 78.3772, "Q": 750, "H": 4, "type": "Traffic/Commercial"},
        {"name": "Uppal Construction Belt", "lat": 17.4064, "lon": 78.5590, "Q": 700, "H": 5, "type": "Fugitive Construction Dust"}
    ],
    "Pune": [
        {"name": "Pimpri-Chinchwad Industrial Estate", "lat": 18.6298, "lon": 73.7997, "Q": 1500, "H": 50, "type": "Industrial Stack"},
        {"name": "Hinjewadi IT Corridor Traffic", "lat": 18.5912, "lon": 73.7389, "Q": 800, "H": 3, "type": "Vehicular/Traffic"},
        {"name": "Wagholi Construction Zone", "lat": 18.5793, "lon": 73.9846, "Q": 650, "H": 4, "type": "Fugitive Construction Dust"}
    ],
    "Ahmedabad": [
        {"name": "Naroda Industrial Estate", "lat": 23.0731, "lon": 72.6636, "Q": 1900, "H": 70, "type": "Industrial Stack"},
        {"name": "Odhav Chemical Cluster", "lat": 23.0339, "lon": 72.6663, "Q": 1400, "H": 45, "type": "Chemical/Industrial"},
        {"name": "Bopal Construction Corridor", "lat": 23.0339, "lon": 72.4695, "Q": 700, "H": 5, "type": "Construction"}
    ],
    "Jaipur": [
        {"name": "Sanganer Textile & Dyeing Units", "lat": 26.8199, "lon": 75.8020, "Q": 1200, "H": 30, "type": "Industrial Stack"},
        {"name": "Jhotwara Industrial Area", "lat": 26.9500, "lon": 75.7400, "Q": 1000, "H": 40, "type": "Industrial Stack"},
        {"name": "Ajmer Road Traffic Corridor", "lat": 26.8850, "lon": 75.7700, "Q": 750, "H": 3, "type": "Vehicular/Traffic"}
    ],
    "Lucknow": [
        {"name": "Talkatora Industrial Area", "lat": 26.8398, "lon": 80.8890, "Q": 1100, "H": 35, "type": "Industrial Stack"},
        {"name": "Alambagh Transit Hub", "lat": 26.8103, "lon": 80.9106, "Q": 800, "H": 4, "type": "Vehicular/Traffic"},
        {"name": "Chinhat Brick Kilns", "lat": 26.8890, "lon": 81.0210, "Q": 900, "H": 8, "type": "Brick Kiln/Dust"}
    ],
    "Bhopal": [
        {"name": "Govindpura Industrial Estate", "lat": 23.2408, "lon": 77.4600, "Q": 1300, "H": 45, "type": "Industrial Stack"},
        {"name": "Kolar Road Construction Belt", "lat": 23.1500, "lon": 77.4200, "Q": 700, "H": 5, "type": "Construction"},
        {"name": "MP Nagar Traffic Choke", "lat": 23.2350, "lon": 77.4340, "Q": 650, "H": 3, "type": "Vehicular/Traffic"}
    ],
    "Patna": [
        {"name": "Phulwari Sharif Industrial Area", "lat": 25.5833, "lon": 85.0833, "Q": 1000, "H": 30, "type": "Industrial Stack"},
        {"name": "Danapur Rail Freight Yard", "lat": 25.6350, "lon": 85.0450, "Q": 850, "H": 6, "type": "Diesel Freight/Traffic"},
        {"name": "Patliputra Construction Zone", "lat": 25.6127, "lon": 85.1010, "Q": 600, "H": 4, "type": "Construction"}
    ],
    "Chandigarh": [
        {"name": "Industrial Area Phase I", "lat": 30.7046, "lon": 76.8060, "Q": 900, "H": 35, "type": "Industrial Stack"},
        {"name": "Sector 17 Commercial Traffic", "lat": 30.7410, "lon": 76.7822, "Q": 600, "H": 3, "type": "Vehicular/Traffic"},
        {"name": "Manimajra Construction Belt", "lat": 30.7275, "lon": 76.8419, "Q": 550, "H": 4, "type": "Construction"}
    ],
    "Kochi": [
        {"name": "Eloor-Edayar Industrial Belt", "lat": 10.0500, "lon": 76.3050, "Q": 2000, "H": 60, "type": "Heavy Chemical/Industrial"},
        {"name": "Vyttila Traffic Junction", "lat": 9.9680, "lon": 76.3190, "Q": 700, "H": 3, "type": "Vehicular/Traffic"},
        {"name": "Kakkanad IT Corridor Construction", "lat": 10.0159, "lon": 76.3419, "Q": 650, "H": 4, "type": "Construction"}
    ],
    "Guwahati": [
        {"name": "Noonmati Oil Refinery", "lat": 26.1867, "lon": 91.7789, "Q": 1800, "H": 80, "type": "Industrial Stack"},
        {"name": "Maligaon Rail Yard", "lat": 26.1544, "lon": 91.6398, "Q": 800, "H": 6, "type": "Diesel Freight/Traffic"},
        {"name": "Fancy Bazaar Commercial Traffic", "lat": 26.1875, "lon": 91.7458, "Q": 700, "H": 3, "type": "Vehicular/Traffic"}
    ]
}

def calculate_dispersion_grid(city_name, center_lat, center_lon, wind_speed_kmh, wind_dir_deg, background_pm25, policy_reductions=None):
    """
    Computes a 2D grid representing PM2.5 dispersion using a Gaussian Plume Model.
    
    Arguments:
    - city_name: Name of the city
    - center_lat, center_lon: Center coordinates of the grid
    - wind_speed_kmh: Wind speed in km/h (will convert to m/s)
    - wind_dir_deg: Wind direction in degrees (where the wind is blowing FROM)
    - background_pm25: Background PM2.5 concentration (from Open-Meteo)
    - policy_reductions: Dictionary containing source category reductions (e.g. {"Traffic": 0.20})
    
    Returns:
    - List of dicts: [{'lat': l, 'lon': ln, 'pm2_5': val}]
    """
    sources = EMISSION_SOURCES.get(city_name, [])
    if not sources:
        return []
        
    # Convert wind speed to m/s, limit minimum wind to 0.5 m/s to prevent infinity
    u = max(wind_speed_kmh * 1000 / 3600, 0.5)
    
    # Wind direction in degrees is where wind is blowing FROM.
    # The direction of the plume flow (downwind direction) is FROM + 180 degrees.
    # Convert to radians for trigonometric rotation
    theta_rad = np.radians((wind_dir_deg + 180) % 360)
    
    # Grid parameters
    grid_size = 25  # 25x25 grid
    lat_range = 0.18  # Span +/- 0.09 around center
    lon_range = 0.18
    
    lats = np.linspace(center_lat - lat_range/2, center_lat + lat_range/2, grid_size)
    lons = np.linspace(center_lon - lon_range/2, center_lon + lon_range/2, grid_size)
    
    # Approximate meters conversion factors
    r_earth = 6371000.0
    lat_to_m = np.radians(1.0) * r_earth
    lon_to_m = np.radians(1.0) * r_earth * np.cos(np.radians(center_lat))
    
    grid_data = []
    
    for lat in lats:
        for lon in lons:
            total_pm25 = background_pm25
            
            # Compute concentration from each source
            for source in sources:
                s_lat = source["lat"]
                s_lon = source["lon"]
                
                # Check policy reduction for source type
                q_mod = 1.0
                if policy_reductions:
                    for category, red_fraction in policy_reductions.items():
                        if category.lower() in source["type"].lower():
                            q_mod = max(0.0, 1.0 - red_fraction)
                            break
                            
                Q = source["Q"] * q_mod
                H = source["H"]
                
                # Convert coordinates to relative meters from source
                dy = (lat - s_lat) * lat_to_m
                dx = (lon - s_lon) * lon_to_m
                
                # Rotate coordinates so downwind is the positive x-axis (u-direction)
                # x_down is distance along the wind direction
                # y_cross is the perpendicular distance
                x_down = dx * np.sin(theta_rad) + dy * np.cos(theta_rad)
                y_cross = -dx * np.cos(theta_rad) + dy * np.sin(theta_rad)
                
                # If upwind, the plume hasn't reached here yet.
                # However, to simulate some lateral diffusion/turbulent mixing upwind, 
                # we add a tiny threshold or just strict x_down > 0.
                if x_down <= 10.0:
                    continue
                
                # Compute dispersion coefficients (Pasquill-Gifford stability class D/C approximation)
                # Adding 20m/10m base to prevent divide by zero near stack
                sig_y = 0.12 * x_down + 30.0
                sig_z = 0.08 * x_down + 15.0
                
                # Ground level Gaussian Plume equation
                # C = (Q / (pi * u * sig_y * sig_z)) * exp(-y_cross^2 / (2 * sig_y^2)) * exp(-H^2 / (2 * sig_z^2))
                c = (Q / (np.pi * u * sig_y * sig_z)) * \
                    np.exp(- (y_cross ** 2) / (2 * sig_y ** 2)) * \
                    np.exp(- (H ** 2) / (2 * sig_z ** 2))
                
                # Add to grid point (caps to make display sensible)
                total_pm25 += min(c, 800.0)
            
            # Clip PM2.5 to realistic levels
            total_pm25 = max(5.0, min(total_pm25, 999.0))
            
            grid_data.append({
                "lat": float(lat),
                "lon": float(lon),
                "pm2_5": round(total_pm25, 1)
            })
            
    return grid_data
