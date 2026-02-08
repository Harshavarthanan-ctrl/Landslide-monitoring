import tensorflow as tf
from tensorflow.keras import layers, models

def build_cnn_extractor(input_shape=(256, 256, 3)):
    """
    Builds a CNN model to extract features from satellite imagery.
    Input: Satellite Image (e.g., 256x256 RGB or SAR)
    Output: Feature vector (e.g., 128-d)
    """
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(128, activation='relu', name="feature_vector"),
        # We don't add a final classification layer here if we use this as a feature extractor
        # directly feeding into the Random Forest or a final dense layer.
        # But for training this CNN independently, we might add:
        # layers.Dense(3, activation='softmax') # Low, Medium, High
    ])
    
    return model

if __name__ == "__main__":
    model = build_cnn_extractor()
    model.summary()
