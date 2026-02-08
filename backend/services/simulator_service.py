import random
import time

class LandslideSimulator:
    def __init__(self):
        # Store state for "Real-Time Mimic" features
        self.soil_moisture = {
            "Nilgiris (Ooty)": 20.0,
            "Kodaikanal (Dindigul)": 15.0,
            "Valparai (Coimbatore)": 25.0,
            "Yercaud (Salem)": 18.0,
            "Kolli Hills (Namakkal)": 12.0,
            "Megamalai (Theni)": 22.0,
            "Javadi Hills (Tirupattur)": 10.0,
            "Yelagiri (Tirupattur)": 8.0,
            "Courtallam (Tenkasi)": 28.0,
            "Coonoor (Nilgiris)": 21.0
        }
        # Coordinates for the regions
        self.coordinates = {
            "Nilgiris (Ooty)": {"lat": 11.4102, "lon": 76.6950},
            "Kodaikanal (Dindigul)": {"lat": 10.2381, "lon": 77.4892},
            "Valparai (Coimbatore)": {"lat": 10.3204, "lon": 76.9554},
            "Yercaud (Salem)": {"lat": 11.7753, "lon": 78.2093},
            "Kolli Hills (Namakkal)": {"lat": 11.2485, "lon": 78.3387},
            "Megamalai (Theni)": {"lat": 9.7296, "lon": 77.3996},
            "Javadi Hills (Tirupattur)": {"lat": 12.5931, "lon": 78.8687},
            "Yelagiri (Tirupattur)": {"lat": 12.5796, "lon": 78.6385},
            "Courtallam (Tenkasi)": {"lat": 8.9341, "lon": 77.2762},
            "Coonoor (Nilgiris)": {"lat": 11.3530, "lon": 76.7959}
        }

    def simulate_landslide_risk(self, location_name):
        """
        Simulates environmental factors based on regional historical logic.
        """
        # 1. Realistic Slope (Historical Constant for the region)
        # Most landslides in TN happen on slopes between 20-45 degrees
        slope = random.uniform(15.0, 48.0)

        # 2. Weighted Rainfall Simulation (Probability of storm events)
        # Logic: 70% chance of no/light rain, 20% moderate, 10% extreme storm
        roll = random.random()
        # 2. Weighted Rainfall Simulation (Probability of storm events)
        # Logic: 80% chance of no/light rain, 15% moderate, 5% extreme storm
        # This reduces the frequency of "High" alerts everywhere at once
        roll = random.random()
        if roll < 0.80:
            rainfall = random.uniform(0.0, 5.0)    # Low/No Rain
        elif roll < 0.95:
            rainfall = random.uniform(10.0, 35.0)  # Moderate Rain
        else:
            rainfall = random.uniform(50.0, 120.0) # Extreme Rainfall Event

        # Update Soil Moisture (Cumulative Saturation)
        # Increase significantly with rain, decrease slowly with "sun"
        current_moisture = self.soil_moisture.get(location_name, 20.0)
        if rainfall > 10:
            current_moisture += (rainfall * 0.1)  # Absorb rain
        else:
            current_moisture -= 0.5  # Dry out
        
        # Cap moisture between 0 and 100
        current_moisture = max(0.0, min(100.0, current_moisture))
        self.soil_moisture[location_name] = current_moisture

        # Vibration Triggers (Simulate passing heavy vehicle or minor tremor)
        ground_vibration = random.uniform(0.0, 5.0) # mm/s
        if random.random() < 0.05: # 5% chance of a tremor
            ground_vibration = random.uniform(15.0, 30.0)

        # Topographic Wetness Index (TWI) & NDVI (Vegetation)
        # Synthesize these to match the frontend RiskMap requirements
        # High moisture + flat area = High TWI. Steep slope = Low TWI (water runs off)
        twi = (current_moisture / 5.0) + (10.0 / (slope + 1)) 
        twi = round(min(20.0, max(0.0, twi)), 2)

        # NDVI: Lower after landslides or in urban areas. Randomize slightly.
        ndvi = random.uniform(0.1, 0.8)

        # 3. Threshold Warning Logic
        risk_level = "Low"
        confidence = "85%"

        # High Risk Conditions:
        # - Steep slope AND Heavy Rain
        # - OR High Soil Moisture AND Vibration
        if (slope > 30 and rainfall > 40) or (current_moisture > 80 and ground_vibration > 10):
            risk_level = "High"
            confidence = "98%"
        elif slope > 20 or rainfall > 15 or current_moisture > 60:
            risk_level = "Medium"
            confidence = "92%"

        coords = self.coordinates.get(location_name, {"lat": 11.0, "lon": 77.0})

        return {
            "region": location_name,
            "risk": risk_level,
            "lat": coords["lat"],
            "lon": coords["lon"],
            "metrics": {
                "slope": round(slope, 2),
                "rain": round(rainfall, 2),
                "twi": twi,
                "ndvi": round(ndvi * 100, 1), # Convert 0-1 to percentage for frontend
                "moisture": round(current_moisture, 2),
                "vibration": round(ground_vibration, 2)
            },
            "details": f"Simulated: Rain {round(rainfall, 1)}mm, Slope {round(slope, 1)}°, Moisture {round(current_moisture, 1)}%",
            "confidence": confidence,
            "timestamp": time.strftime("%H:%M:%S")
        }
