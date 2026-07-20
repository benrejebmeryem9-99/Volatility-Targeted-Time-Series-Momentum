import numpy as np
import pandas as pd
import pytest

from src.volatility import (
    calculate_rolling_volatility,
    calculate_volatility_scaler,
)


def test_rolling_volatility_has_correct_length():
    returns = pd.Series(
        [0.01, -0.02, 0.015, 0.005, -0.01],
        index=pd.date_range("2024-01-01", periods=5),
    )

    volatility = calculate_rolling_volatility(
        returns,
        window=3,
    )

    assert len(volatility) == len(returns)


def test_rolling_volatility_is_non_negative():
    returns = pd.Series(
        [0.01, -0.02, 0.015, 0.005, -0.01],
    )

    volatility = calculate_rolling_volatility(
        returns,
        window=3,
    )

    valid_values = volatility.dropna()

    assert (valid_values >= 0).all()


def test_volatility_scaler_respects_maximum_leverage():
    volatility = pd.Series(
        [0.05, 0.10, 0.20, 0.01],
    )

    scaler = calculate_volatility_scaler(
        volatility,
        target_volatility=0.10,
        maximum_leverage=2.0,
    )

    assert scaler.max() <= 2.0


def test_invalid_volatility_window():
    returns = pd.Series([0.01, 0.02, -0.01])

    with pytest.raises(ValueError):
        calculate_rolling_volatility(
            returns,
            window=0,
        )