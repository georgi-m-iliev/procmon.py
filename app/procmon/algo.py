import numpy as np

from app.core.config import settings


def rolling_stats(values):
    if len(values) < settings.ROLLING_WINDOW_LIMIT:
        return None, None  # Not enough data
    mean = np.mean(values)
    std = np.std(values)
    return mean, std


def is_anomaly(value, mean, std, threshold):
    if std == 0:
        return False
    z = abs((value - mean) / std)
    return z > threshold
