
# tests/test_preprocessing.py

import pytest
import numpy as np
from bjx_meit1.preprocessing import load_image, preprocess_image

def test_load_image():
    image = load_image('xray1.jpg')
    assert isinstance(image, np.ndarray)
    assert image.shape[0] > 0 and image.shape[1] > 0

def test_preprocess_image():
    image = np.random.rand(256, 256)
    processed_image = preprocess_image(image)
    assert processed_image.shape == (128, 128)
    assert np.max(processed_image) <= 1.0
