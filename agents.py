import random
import numpy as np

# Local governing bodies per city — used to make enforcement measures genuinely
# city-specific (different agency names, different phrasing) instead of a
# generic template with only the city name swapped in.
CITY_AUTHORITIES = {
    "Delhi": {"pcb": "Delhi Pollution Control Committee (DPCC)", "traffic": "Delhi Traffic Police", "municipal": "MCD", "transit_note": "Odd-Even vehicle rationing", "water_source": "DJB tanker fleet"},
    "Mumbai": {"pcb": "Maharashtra Pollution Control Board (MPCB)", "traffic": "Mumbai Traffic Police", "municipal": "BMC", "transit_note": "coastal road diesel-fleet checks", "water_source": "BMC water tankers"},
    "Bengaluru": {"pcb": "Karnataka State Pollution Control Board (KSPCB)", "traffic": "Bengaluru Traffic Police", "municipal": "BBMP", "transit_note": "IT-corridor peak-hour diversions", "water_source": "BWSSB tanker units"},
    "Chennai": {"pcb": "Tamil Nadu Pollution Control Board (TNPCB)", "traffic": "Chennai Traffic Police", "municipal": "Greater Chennai Corporation (GCC)", "transit_note": "port-corridor freight rerouting", "water_source": "Metrowater tankers"},
    "Kolkata": {"pcb": "West Bengal Pollution Control Board (WBPCB)", "traffic": "Kolkata Traffic Police", "municipal": "KMC", "transit_note": "riverfront freight corridor checks", "water_source": "KMC water tankers"},
    "Hyderabad": {"pcb": "Telangana State Pollution Control Board (TSPCB)", "traffic": "Hyderabad Traffic Police", "municipal": "GHMC", "transit_note": "HITEC City corridor smart-signal throttling", "water_source": "HMWSSB tanker fleet"},
    "Pune": {"pcb": "Maharashtra Pollution Control Board (MPCB)", "traffic": "Pune Traffic Police", "municipal": "PMC", "transit_note": "IT-corridor shuttle enforcement", "water_source": "PMC water tankers"},
    "Ahmedabad": {"pcb": "Gujarat Pollution Control Board (GPCB)", "traffic": "Ahmedabad Traffic Police", "municipal": "AMC", "transit_note": "textile-belt freight corridor checks", "water_source": "AMC tanker units"},
    "Jaipur": {"pcb": "Rajasthan State Pollution Control Board (RSPCB)", "traffic": "Jaipur Traffic Police", "municipal": "JMC", "transit_note": "heritage-zone diesel restriction", "water_source": "JMC water tankers"},
    "Lucknow": {"pcb": "UP Pollution Control Board (UPPCB)", "traffic": "Lucknow Traffic Police", "municipal": "LMC", "transit_note": "ring-road freight diversion", "water_source": "LMC tanker fleet"},
    "Bhopal": {"pcb": "Madhya Pradesh Pollution Control Board (MPPCB)", "traffic": "Bhopal Traffic Police", "municipal": "BMC (Bhopal Municipal Corporation)", "transit_note": "lakefront traffic calming", "water_source": "BMC water tankers"},
    "Patna": {"pcb": "Bihar State Pollution Control Board (BSPCB)", "traffic": "Patna Traffic Police", "municipal": "PMC (Patna Municipal Corporation)", "transit_note": "riverine freight-yard checks", "water_source": "PMC tanker units"},
    "Chandigarh": {"pcb": "Chandigarh Pollution Control Committee (CPCC)", "traffic": "Chandigarh Traffic Police", "municipal": "MC Chandigarh", "transit_note": "sector-grid signal optimization", "water_source": "MC Chandigarh tankers"},
    "Kochi": {"pcb": "Kerala State Pollution Control Board", "traffic": "Kochi City Traffic Police", "municipal": "Kochi Municipal Corporation", "transit_note": "backwater freight corridor checks", "water_source": "Kochi Corporation tankers"},
    "Guwahati": {"pcb": "Pollution Control Board Assam (PCBA)", "traffic": "Guwahati Traffic Police", "municipal": "GMC", "transit_note": "riverine freight-yard diversion", "water_source": "GMC water tankers"},
}

def run_multi_agent_consensus(city_name, temp, humidity, wind_spd, wind_dir, pm25, pm10, aqi):
    """
    Simulates a multi-agent consensus debate analyzing the air pollution situation.
    Uses actual live meteorological and pollutant values to construct a coherent,
    data-driven analytical dialogue.
    
    Returns:
        dialogue: List of dicts with sender, avatar, message.
        attribution: Dict of source categories and percentages.
        confidence: Overall confidence score.
        recs: List of prioritized enforcement actions.
    """
    
    # 1. Determine meteorological stability based on wind speed and humidity
    stability = "Stable / Dispersion Poor"
    if wind_spd > 15:
        stability = "Unstable / Good Dispersion"
    elif wind_spd > 8:
        stability = "Neutral / Moderate Dispersion"
        
    # Determine main direction name
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = int(((wind_dir + 11.25) % 360) / 22.5)
    wind_dir_text = directions[idx]
    
    # Custom city profile parameters (baseline source attribution shares)
    city_profiles = {
        "Delhi": {
            "traffic": 34, "industrial": 25, "biomass": 22, "construction": 12, "dust": 7,
            "hotspots": ["Anand Vihar", "Okhla Phase III", "Ghazipur Landfill"]
        },
        "Mumbai": {
            "traffic": 30, "industrial": 28, "biomass": 10, "construction": 24, "dust": 8,
            "hotspots": ["Deonar Landfill", "Chembur", "Sion Metro Construction"]
        },
        "Bengaluru": {
            "traffic": 42, "industrial": 18, "biomass": 8, "construction": 26, "dust": 6,
            "hotspots": ["Silk Board Junction", "Whitefield", "Peenya"]
        },
        "Chennai": {
            "traffic": 25, "industrial": 45, "biomass": 8, "construction": 14, "dust": 8,
            "hotspots": ["Manali Petrochem", "Ennore Power Plant", "T Nagar"]
        },
        "Kolkata": {
            "traffic": 32, "industrial": 35, "biomass": 18, "construction": 10, "dust": 5,
            "hotspots": ["Howrah Freight", "Cossipore Foundries", "Dhapa Landfill"]
        },
        "Hyderabad": {
            "traffic": 38, "industrial": 24, "biomass": 8, "construction": 22, "dust": 8,
            "hotspots": ["Patancheru Industrial Cluster", "HITEC City", "Uppal"]
        },
        "Pune": {
            "traffic": 40, "industrial": 22, "biomass": 6, "construction": 26, "dust": 6,
            "hotspots": ["Pimpri-Chinchwad", "Hinjewadi", "Wagholi"]
        },
        "Ahmedabad": {
            "traffic": 28, "industrial": 42, "biomass": 10, "construction": 14, "dust": 6,
            "hotspots": ["Naroda Industrial Estate", "Odhav", "Bopal"]
        },
        "Jaipur": {
            "traffic": 30, "industrial": 26, "biomass": 12, "construction": 18, "dust": 14,
            "hotspots": ["Sanganer", "Jhotwara", "Ajmer Road"]
        },
        "Lucknow": {
            "traffic": 32, "industrial": 20, "biomass": 24, "construction": 16, "dust": 8,
            "hotspots": ["Talkatora Industrial Area", "Alambagh", "Chinhat"]
        },
        "Bhopal": {
            "traffic": 30, "industrial": 30, "biomass": 14, "construction": 18, "dust": 8,
            "hotspots": ["Govindpura", "Kolar Road", "MP Nagar"]
        },
        "Patna": {
            "traffic": 34, "industrial": 18, "biomass": 26, "construction": 14, "dust": 8,
            "hotspots": ["Phulwari Sharif", "Danapur", "Patliputra"]
        },
        "Chandigarh": {
            "traffic": 36, "industrial": 16, "biomass": 20, "construction": 20, "dust": 8,
            "hotspots": ["Industrial Area Phase I", "Sector 17", "Manimajra"]
        },
        "Kochi": {
            "traffic": 30, "industrial": 34, "biomass": 6, "construction": 22, "dust": 8,
            "hotspots": ["Eloor-Edayar", "Vyttila", "Kakkanad"]
        },
        "Guwahati": {
            "traffic": 28, "industrial": 36, "biomass": 16, "construction": 14, "dust": 6,
            "hotspots": ["Noonmati Refinery", "Maligaon", "Fancy Bazaar"]
        }
    }
    
    profile = city_profiles.get(city_name, city_profiles["Delhi"])
    authority = CITY_AUTHORITIES.get(city_name, CITY_AUTHORITIES["Delhi"])
    
    # Dynamic adjustments based on live data
    # High PM10 relative to PM2.5 indicates high construction/road dust
    ratio = pm10 / pm25 if pm25 > 0 else 1.0
    construction_adj = 0
    dust_adj = 0
    if ratio > 2.0:
        construction_adj = 6
        dust_adj = 4
    elif ratio < 1.4:
        # High PM2.5 fraction indicates combustion/biomass/industrial stack
        construction_adj = -4
        dust_adj = -2
        
    # High humidity traps pollution, exaggerating heavy vehicle exhaust (NO2/PM2.5)
    traffic_adj = 0
    if humidity > 75:
        traffic_adj = 4
    
    # Compile attribution
    attrib = {
        "Traffic / Vehicular": max(5, profile["traffic"] + traffic_adj),
        "Industrial Stack Emissions": max(5, profile["industrial"]),
        "Construction Fugitive Dust": max(5, profile["construction"] + construction_adj),
        "Biomass & Waste Burning": max(5, profile["biomass"]),
        "Resuspended Road Dust / Others": max(5, profile["dust"] + dust_adj)
    }
    
    # Normalize percentages to sum to 100
    total = sum(attrib.values())
    attrib = {k: round((v / total) * 100, 1) for k, v in attrib.items()}
    
    # Compute statistical confidence score
    # Lower wind speed means higher concentration local signals (easier to attribute -> higher confidence)
    # Higher wind means transboundary mixing (lower confidence)
    confidence_score = round(92.0 - (wind_spd * 0.8) - (abs(humidity - 50) * 0.1), 1)
    confidence_score = max(50.0, min(confidence_score, 98.0))
    
    # Create agents dialogue
    dialogue = [
        {
            "sender": "Meteorological Agent (MeteoShield-AI)",
            "avatar": "🌡️",
            "message": f"Establishing ambient meteorological profile for {city_name}. Current station reading is {aqi} AQI (PM2.5: {pm25} µg/m³, PM10: {pm10} µg/m³). "
                       f"Wind is blowing FROM {wind_dir_text} ({wind_dir}° ) at {wind_spd} km/h. Temperature is {temp}°C, Relative Humidity at {humidity}%. "
                       f"Atmospheric Boundary Layer (ABL) stability classification: **{stability}**. "
                       f"{'Low ventilation index is causing local stagnation.' if wind_spd < 7 else 'Moderate wind speed is aiding cross-ward dispersion.'}"
        },
        {
            "sender": "Geospatial Source Attribution Agent (GeoSource-AI)",
            "avatar": "🛰️",
            "message": f"Analyzing geospatial emitter registry along the wind vector path. With wind blowing towards the opposite direction of {wind_dir_text}, "
                       f"plumes from major clusters like {', '.join(profile['hotspots'][:2])} are vectoring downwind. "
                       f"Correlating PM2.5/PM10 ratio of {ratio:.2f}. The primary particulate signature reflects "
                       f"{'heavy secondary combustion aerosols (high PM2.5 fraction), likely industrial/exhaust.' if ratio < 1.6 else 'coarse dust particles (high PM10 fraction), indicative of active construction and road dust.'} "
                       f"We estimate the source attribution to be: Vehicular ({attrib['Traffic / Vehicular']}%), "
                       f"Industrial ({attrib['Industrial Stack Emissions']}%), and Construction Dust ({attrib['Construction Fugitive Dust']}%)."
        },
        {
            "sender": "Public Health & Vulnerability Agent (HealthAlert-AI)",
            "avatar": "🏥",
            "message": f"Exposure vulnerability mapping activated. In the downwind quadrant of the active plume, "
                       f"we have identified receptor hotspots. Based on the target city ward map, population density is high, "
                       f"with critical receptors (schools and clinics) located within a 3km radius. "
                       f"Given the AQI is {aqi} ({'Poor' if aqi > 200 else 'Moderate' if aqi > 100 else 'Satisfactory'}), "
                       f"exposure risk is classified as **{'HIGH' if aqi > 200 else 'MEDIUM' if aqi > 100 else 'LOW'}**. "
                       f"Recommending language-targeted advisories and targeted containment at source."
        },
        {
            "sender": "Consensus Engine (AeroIntel-Consensus)",
            "avatar": "🤖",
            "message": f"Consensus reached with **{confidence_score}% statistical confidence**. "
                       f"Attribution is finalized. Recommending immediate dispatch of localized enforcement agents "
                       f"to active coordinates upwind of the affected wards."
        }
    ]
    
    # Generate action recommendations based on top attribution categories
    recs = []
    sorted_attrib = sorted(attrib.items(), key=lambda x: x[1], reverse=True)
    
    for i, (cat, val) in enumerate(sorted_attrib[:3]):
        priority = "URGENT" if aqi > 250 else "HIGH" if aqi > 150 else "MEDIUM"
        if "Traffic" in cat:
            recs.append({
                "title": f"{authority['traffic']}: Deploy Wardens & RTO Checks at {profile['hotspots'][0]}",
                "priority": priority,
                "category": "Vehicular",
                "impact": f"Targeting heavy diesel transport contributing {val}% of current local emissions in {city_name}.",
                "action": f"{authority['traffic']} to enforce idling limits, verify PUC certificates, and activate {authority['transit_note']} on approach roads to {profile['hotspots'][0]}."
            })
        elif "Industrial" in cat:
            recs.append({
                "title": f"{authority['pcb']}: Stack Emission Audit at {profile['hotspots'][1]}",
                "priority": priority,
                "category": "Industrial",
                "impact": f"Targeting point source stack emissions contributing {val}% of pollution in {city_name}.",
                "action": f"{authority['pcb']} to inspect stack scrubbers, verify continuous emission monitoring feed, and issue closure notice to units at {profile['hotspots'][1]} found violating norms."
            })
        elif "Construction" in cat:
            recs.append({
                "title": f"{authority['municipal']}: Fugitive Dust Suppression at {profile['hotspots'][-1]}",
                "priority": priority if len(profile['hotspots']) > 2 else "HIGH",
                "category": "Construction",
                "impact": f"Addressing building dust and construction traffic contributing {val}% of PM10 in {city_name}.",
                "action": f"{authority['municipal']} to deploy mechanical water-mist cannons using the {authority['water_source']}, inspect windbreak netting, and check geotextile covering compliance at {profile['hotspots'][-1]}."
            })
        elif "Biomass" in cat:
            recs.append({
                "title": f"{authority['municipal']}: Waste Burning Inspection & Night Patrols",
                "priority": "HIGH",
                "category": "Biomass/Waste",
                "impact": f"Targeting illegal solid waste open combustion causing {val}% PM2.5 spike near {profile['hotspots'][-1]}, {city_name}.",
                "action": f"{authority['municipal']} to deploy night patrol drones near {profile['hotspots'][-1]}, and fine contractors failing landfill/cover duties, coordinating with {authority['pcb']} for repeat-offender action."
            })
            
    return dialogue, attrib, confidence_score, recs
