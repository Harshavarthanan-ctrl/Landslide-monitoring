import numpy as np
import warnings

# Try importing TensorFlow, mock if missing (for Python 3.13 support)
try:
    import tensorflow as tf
    TF_AVAILABLE = True
    from .models.cnn_feature_extractor import build_cnn_extractor
    from .models.lstm_rainfall import build_lstm_model
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available (Python 3.13?). Running in Mock Mode.")

from .models.rf_risk_classifier import LandslideRiskClassifier

from .data_loaders.gee_loader import GEELoader

class LandslideInferenceEngine:
    def __init__(self):
        self.gee_loader = GEELoader()
        self.rf = LandslideRiskClassifier()

        if TF_AVAILABLE:
            self.cnn = build_cnn_extractor()
            self.lstm = build_lstm_model()
        else:
            self.cnn = None
            self.lstm = None

    def predict_risk(self, lat, lon):
        print(f"Analyzing historical vulnerability for location: {lat}, {lon}")
        
        # 1. Get Static Data (Slope)
        try:
            geo_data = self.gee_loader.get_elevation_data(lat, lon)
            slope = geo_data.get('slope', 0)
        except Exception as e:
            print(f"GEE Error: {e}")
            slope = np.random.uniform(5, 45) # Mock slope
        
        # 2. Historical Logic (No Real-Time)
        # We classify risk purely on Topography for the "Vulnerability Assessment"
        
        # Thresholds (Historical/Static)
        # Steep slopes in TN (Nilgiris) are historically high risk
        
        if slope > 35:
            result = "High" # Historically prone
        elif slope > 15:
            result = "Medium" # Moderately prone
        else:
            result = "Low" # Low probability
            
        print(f"Slope: {slope:.2f}, Vulnerability: {result}")
        return result


if __name__ == "__main__":
    engine = LandslideInferenceEngine()
    # Generate a random prediction
    # We need to fit the RF first to avoid errors in this mock script since it's fresh
    X_mock = np.random.rand(10, 162)
    y_mock = np.random.randint(0, 3, 10)
    engine.rf.train(X_mock, y_mock)
    
    print(f"Risk Assessment: {engine.predict_risk(10.0889, 77.0595)}")
