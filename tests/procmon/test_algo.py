import pytest
import numpy as np
from unittest import mock

from app.procmon.algo import rolling_stats, is_anomaly


@mock.patch('app.core.config.settings.ROLLING_WINDOW_LIMIT', new=5)
def test_rolling_stats_not_enough_data():
    values = [1, 2, 3]
    mean, std = rolling_stats(values)
    assert mean is None
    assert std is None


@mock.patch('app.core.config.settings.ROLLING_WINDOW_LIMIT', new=3)
def test_rolling_stats_enough_data():
    values = [1, 2, 3]
    expected_mean = np.mean(values)
    expected_std = np.std(values)
    mean, std = rolling_stats(values)
    assert mean == expected_mean
    assert std == expected_std


def test_is_anomaly_with_zero_std():
    assert is_anomaly(10, mean=10, std=0, threshold=2) is False


def test_is_anomaly_below_threshold():
    assert is_anomaly(10.1, mean=10, std=1, threshold=2) is False


def test_is_anomaly_above_threshold():
    assert is_anomaly(15, mean=10, std=1, threshold=3) is True
