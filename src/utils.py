"""
This module contains utility functions used throughout the project.
"""

import os
import pickle
from typing import Any

import pandas as pd
import torch
import torch.nn as nn

# The default directory for saving models and other helpers.
DEFAULT_MODEL_DIR = os.path.join("..", "models")


def inlier_mask(series: pd.Series, iqr_window: float = 1.5) -> pd.Series:
    """Compute a boolean mask that identifies inliers in a series."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return (q1 - iqr*iqr_window <= series) & (series <= q3 + iqr*iqr_window)


def store_model_weights(model: nn.Module, name: str, dir: str = DEFAULT_MODEL_DIR) -> None:
    """Save the state dict of a given model to disk."""
    os.makedirs(dir, exist_ok=True)

    filepath = os.path.join(dir, f"{name}-statedict.pt")
    torch.save(model.state_dict(), filepath)
    print(f"Saved model state dict to '{filepath}'")


def load_model_weights(model: nn.Module, name: str, dir: str = DEFAULT_MODEL_DIR) -> None:
    """Load the state dict of a model from disk."""
    filepath = os.path.join(dir, f"{name}-statedict.pt")
    model.load_state_dict(torch.load(filepath))


def store_model_helper(object: Any, filename: str, dir: str = DEFAULT_MODEL_DIR) -> None:
    """Save an object to disk using `pickle`."""
    os.makedirs(dir, exist_ok=True)

    filepath = os.path.join(dir, filename)
    pickle.dump(object, open(filepath, "wb"))
    print(f"Pickled the object to '{filepath}'")


def load_model_helper(filename: str, dir: str = DEFAULT_MODEL_DIR) -> Any:
    """Load an object from disk using `pickle`."""
    filepath = os.path.join(dir, filename)
    return pickle.load(open(filepath, "rb"))
