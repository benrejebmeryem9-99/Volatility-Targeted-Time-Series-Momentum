import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_rolling_volatility(
    returns: pd.Series,
    window: int = 20,
    annualization_factor: int = TRADING_DAYS,
) -> pd.Series:
    """
    Calculate annualized rolling volatility.

    Parameters
    ----------
    returns:
        Series of daily returns.
    window:
        Number of trading days used in the rolling estimation.
    annualization_factor:
        Number of trading days per year.

    Returns
    -------
    pd.Series
        Annualized rolling volatility.
    """

    if window <= 1:
        raise ValueError("window must be greater than 1.")

    volatility = returns.rolling(window=window).std()

    return volatility * np.sqrt(annualization_factor)


def calculate_ewma_volatility(
    returns: pd.Series,
    span: int = 60,
    annualization_factor: int = TRADING_DAYS,
) -> pd.Series:
    """
    Calculate annualized exponentially weighted volatility.
    """

    if span <= 1:
        raise ValueError("span must be greater than 1.")

    variance = returns.pow(2).ewm(
        span=span,
        adjust=False,
    ).mean()

    return np.sqrt(variance * annualization_factor)


def calculate_volatility_scaler(
    volatility: pd.Series,
    target_volatility: float = 0.10,
    maximum_leverage: float = 2.0,
) -> pd.Series:
    """
    Calculate the exposure required to target a specified volatility.

    The scaler is shifted by one trading day to prevent look-ahead bias.
    """

    if target_volatility <= 0:
        raise ValueError("target_volatility must be positive.")

    if maximum_leverage <= 0:
        raise ValueError("maximum_leverage must be positive.")

    scaler = target_volatility / volatility

    scaler = scaler.replace([np.inf, -np.inf], np.nan)
    scaler = scaler.clip(lower=0, upper=maximum_leverage)

    return scaler.shift(1)


def apply_volatility_targeting(
    returns: pd.Series,
    volatility: pd.Series,
    target_volatility: float = 0.10,
    maximum_leverage: float = 2.0,
) -> pd.DataFrame:
    """
    Apply volatility targeting to a return series.
    """

    scaler = calculate_volatility_scaler(
        volatility=volatility,
        target_volatility=target_volatility,
        maximum_leverage=maximum_leverage,
    )

    result = pd.DataFrame(
        {
            "Return": returns,
            "Estimated_Volatility": volatility,
            "Volatility_Scaler": scaler,
        }
    )

    result["Targeted_Return"] = (
        result["Return"] * result["Volatility_Scaler"]
    )

    return result.dropna()