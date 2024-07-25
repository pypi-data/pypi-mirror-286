# bjx_meit/utils.py

def save_model(model, filepath: str) -> None:
    """Save a Keras model to a file."""
    model.save(filepath)

def load_model(filepath: str):
    """Load a Keras model from a file."""
    from tensorflow.keras.models import load_model
    return load_model(filepath)
