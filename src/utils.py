"""
This module contains utility functions used throughout the project.
"""

import pandas as pd


def inlier_mask(series: pd.Series, iqr_window: float = 1.5) -> pd.Series:
    """Compute a boolean mask that identifies inliers in a series."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return (q1 - iqr*iqr_window <= series) & (series <= q3 + iqr*iqr_window)
