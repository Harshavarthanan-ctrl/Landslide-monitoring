from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np

class LandslideRiskClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, X, y):
        """
        X: Feature matrix [CNN_features + LSTM_features + Static_features]
        y: Labels [0: Low, 1: Medium, 2: High]
        """
        self.model.fit(X, y)
        print("Model trained successfully.")

    def predict(self, features):
        """
        Predicts risk level.
        features: 1D array or 2D array of samples
        """
        prediction = self.model.predict(features)
        return prediction

    def save_model(self, path="rf_model.pkl"):
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
            
    def load_model(self, path="rf_model.pkl"):
        with open(path, "rb") as f:
            self.model = pickle.load(f)

if __name__ == "__main__":
    # Mock training
    clf = LandslideRiskClassifier()
    # 128 CNN features + 32 LSTM features + 2 Static (Slope, Elevation) = 162 total features
    X_mock = np.random.rand(100, 162)
    y_mock = np.random.randint(0, 3, 100)
    clf.train(X_mock, y_mock)
