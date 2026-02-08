import tensorflow as tf
from tensorflow.keras import layers, models

def build_lstm_model(input_shape=(30, 1)):
    """
    Builds an LSTM model for rainfall time-series analysis.
    Input: Sequence of rainfall data (e.g., last 30 days)
    Output: Rainfall embedding or direct risk prediction.
    """
    model = models.Sequential([
        layers.LSTM(50, activation='relu', input_shape=input_shape, return_sequences=False),
        layers.Dense(32, activation='relu', name="temporal_features")
    ])
    return model

if __name__ == "__main__":
    model = build_lstm_model()
    model.summary()
