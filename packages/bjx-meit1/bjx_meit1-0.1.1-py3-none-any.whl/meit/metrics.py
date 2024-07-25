# bjx_meit/metrics.py

from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np

def evaluate_model(predictions: np.ndarray, true_labels: np.ndarray) -> dict:
    """Evaluate model performance."""
    accuracy = accuracy_score(true_labels, np.argmax(predictions, axis=1))
    conf_matrix = confusion_matrix(true_labels, np.argmax(predictions, axis=1))
    return {"accuracy": accuracy, "confusion_matrix": conf_matrix}
