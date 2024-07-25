import pytest
from bjx_meit1.models import create_model, prepare_data
import numpy as np

def test_create_model():
    input_shape = (128, 128, 1)
    num_classes = 2
    model = create_model(input_shape, num_classes)
    assert model.input_shape == (None, 128, 128, 1)
    assert model.output_shape == (None, num_classes)

def test_prepare_data():
    images = np.random.rand(10, 128, 128, 1)
    labels = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    num_classes = 2
    prepared_images, prepared_labels = prepare_data(images, labels, num_classes)
    assert prepared_images.shape == images.shape
    assert prepared_labels.shape == (10, num_classes)
