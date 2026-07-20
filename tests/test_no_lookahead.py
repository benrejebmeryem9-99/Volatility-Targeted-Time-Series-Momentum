import numpy as np
import pandas as pd

from src.signals import generate_momentum_signal


def test_no_lookahead_bias():
    prices = pd.Series(
        np.arange(100, 200, dtype=float),
        index=pd.date_range(
            start="2024-01-01",
            periods=100,
            freq="D",
        ),
        name="Price",
    )

    full_signal = generate_momentum_signal(
        prices=prices,
        lookback_days=20,
    )

    truncated_prices = prices.iloc[:70]

    truncated_signal = generate_momentum_signal(
        prices=truncated_prices,
        lookback_days=20,
    )

    pd.testing.assert_series_equal(
        full_signal.iloc[:70],
        truncated_signal,
    )