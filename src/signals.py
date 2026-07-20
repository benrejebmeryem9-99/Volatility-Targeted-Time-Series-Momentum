import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_momentum_return(
    prices: pd.Series,
    lookback_days: int = TRADING_DAYS,
) -> pd.Series:
    """
    Calculate the historical return over the selected lookback period.
    """

    if lookback_days <= 0:
        raise ValueError("lookback_days must be positive.")

    return prices.pct_change(periods=lookback_days)


def generate_momentum_signal(
    prices: pd.Series,
    lookback_days: int = TRADING_DAYS,
) -> pd.Series:
    """
    Generate a time-series momentum signal.

    Signal values:
        1  = long
       -1  = short
        0  = neutral

    The signal is shifted by one day to avoid look-ahead bias.
    """

    momentum_return = calculate_momentum_return(
        prices=prices,
        lookback_days=lookback_days,
    )

    signal = pd.Series(
        np.where(
            momentum_return > 0,
            1.0,
            np.where(momentum_return < 0, -1.0, 0.0),
        ),
        index=prices.index,
        name="Momentum_Signal",
    )


    return signal.shift(1)