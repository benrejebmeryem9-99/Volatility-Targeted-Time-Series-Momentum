import pandas as pd


def run_backtest(
    returns: pd.Series,
    signal: pd.Series,
    volatility_scaler: pd.Series,
    transaction_cost_bps: float = 0.0,
) -> pd.DataFrame:
    """
    Run a volatility-targeted momentum backtest.

    Parameters
    ----------
    returns:
        Daily asset returns.
    signal:
        Shifted momentum signal: 1 for long, -1 for short, 0 for neutral.
    volatility_scaler:
        Shifted volatility-targeting exposure.
    transaction_cost_bps:
        Transaction cost in basis points applied to daily turnover.

    Returns
    -------
    pd.DataFrame
        Backtest results with positions, turnover, costs, and strategy returns.
    """

    if transaction_cost_bps < 0:
        raise ValueError("transaction_cost_bps cannot be negative.")

    result = pd.concat(
        [
            returns.rename("Asset_Return"),
            signal.rename("Momentum_Signal"),
            volatility_scaler.rename("Volatility_Scaler"),
        ],
        axis=1,
    ).dropna()
    result = result[result["Momentum_Signal"] != 0].copy()

    result["Position"] = (
        result["Momentum_Signal"]
        * result["Volatility_Scaler"]
    )

    result["Gross_Strategy_Return"] = (
        result["Position"]
        * result["Asset_Return"]
    )

    result["Turnover"] = (
        result["Position"]
        .diff()
        .abs()
        .fillna(result["Position"].abs())
    )

    transaction_cost_rate = transaction_cost_bps / 10_000

    result["Transaction_Cost"] = (
        result["Turnover"]
        * transaction_cost_rate
    )

    result["Net_Strategy_Return"] = (
        result["Gross_Strategy_Return"]
        - result["Transaction_Cost"]
    )

    result["Buy_and_Hold_Wealth"] = (
        1 + result["Asset_Return"]
    ).cumprod()

    result["Strategy_Wealth"] = (
        1 + result["Net_Strategy_Return"]
    ).cumprod()

    return result
