import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

def create_model(input_shape: tuple, num_classes: int):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def prepare_data(images: np.ndarray, labels: np.ndarray, num_classes: int) -> tuple:
    # Ensure labels are one-hot encoded
    labels = np.eye(num_classes)[labels]
    return images, labels
