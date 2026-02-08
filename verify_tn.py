from ai_engine.inference import LandslideInferenceEngine
import ee
import os

# Ensure env var is set for GEE Loader
os.environ["EE_PROJECT_ID"] = "ee-hamdhan04"

def test_tn_prediction():
    print("Initializing Engine...")
    engine = LandslideInferenceEngine()
    
    # Nilgiris (Steep)
    lat_ooty = 11.4102
    lon_ooty = 76.6950
    
    # Chennai (Flat)
    lat_chennai = 13.0827
    lon_chennai = 80.2707
    
    # Valparai (Medium/Steep)
    lat_valparai = 10.3204
    lon_valparai = 76.9554
    
    print(f"\n--- Testing Ooty ({lat_ooty}, {lon_ooty}) ---")
    # Mocking slope since we can't connect to GEE live without valid project
    engine.gee_loader.get_elevation_data = lambda x, y: {'slope': 40, 'elevation': 2200}
    risk = engine.predict_risk(lat_ooty, lon_ooty)
    print(f"Risk: {risk} (Expected: High)")

    print(f"\n--- Testing Chennai ({lat_chennai}, {lon_chennai}) ---")
    engine.gee_loader.get_elevation_data = lambda x, y: {'slope': 2, 'elevation': 10}
    risk = engine.predict_risk(lat_chennai, lon_chennai)
    print(f"Risk: {risk} (Expected: Low)")
    
    print(f"\n--- Testing Valparai ({lat_valparai}, {lon_valparai}) ---")
    engine.gee_loader.get_elevation_data = lambda x, y: {'slope': 25, 'elevation': 1200}
    risk = engine.predict_risk(lat_valparai, lon_valparai)
    print(f"Risk: {risk} (Expected: Medium)")

if __name__ == "__main__":
    test_tn_prediction()
