# tests/test_metrics.py

import numpy as np
from bjx_meit1.metrics import evaluate_model

def test_evaluate_model():
    predictions = np.random.rand(10, 10)
    true_labels = np.random.randint(0, 10, size=(10,))
    results = evaluate_model(predictions, true_labels)
    assert 'accuracy' in results
    assert 'confusion_matrix' in results
