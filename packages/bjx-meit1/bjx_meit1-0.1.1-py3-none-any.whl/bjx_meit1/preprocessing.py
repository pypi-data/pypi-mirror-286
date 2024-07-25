# bjx_meit/preprocessing.py

import cv2
import numpy as np

def load_image(image_path: str) -> np.ndarray:
    """Load an image from a file path."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found or unable to read.")
    return image

def preprocess_image(image: np.ndarray, resize_shape: tuple = (128, 128)) -> np.ndarray:
    """Preprocess image by resizing and normalization."""
    image_resized = cv2.resize(image, resize_shape)
    image_normalized = image_resized / 255.0
    return image_normalized
