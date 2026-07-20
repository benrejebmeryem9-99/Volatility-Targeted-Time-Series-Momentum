import numpy as np
import pandas as pd

from src.backtest import run_backtest
from src.data_loader import add_daily_returns, download_price_data
from src.metrics import calculate_performance_metrics
from src.signals import generate_momentum_signal
from src.volatility import (
    calculate_rolling_volatility,
    calculate_volatility_scaler,
)

def apply_portfolio_volatility_target(
    portfolio_returns: pd.Series,
    target_volatility: float = 0.10,
    window: int = 20,
    maximum_leverage: float = 2.0,
    trading_days: int = 252,
) -> pd.DataFrame:
    """
    Apply a volatility target to the combined multi-asset portfolio.
    """

    if portfolio_returns.empty:
        raise ValueError("portfolio_returns cannot be empty.")

    if target_volatility <= 0:
        raise ValueError("target_volatility must be positive.")

    if window <= 0:
        raise ValueError("window must be positive.")

    if maximum_leverage <= 0:
        raise ValueError("maximum_leverage must be positive.")

    realized_volatility = (
        portfolio_returns
        .rolling(window=window)
        .std()
        .shift(1)
        * np.sqrt(trading_days)
    )

    portfolio_scaler = (
        target_volatility / realized_volatility
    ).clip(
        lower=0.0,
        upper=maximum_leverage,
    )

    targeted_return = (
        portfolio_returns * portfolio_scaler
    )

    targeted_wealth = (
        1 + targeted_return.fillna(0.0)
    ).cumprod()

    return pd.DataFrame(
        {
            "Raw_Portfolio_Return": portfolio_returns,
            "Portfolio_Realized_Volatility": realized_volatility,
            "Portfolio_Scaler": portfolio_scaler,
            "Targeted_Portfolio_Return": targeted_return,
            "Targeted_Portfolio_Wealth": targeted_wealth,
        }
    )
def compare_assets(
    tickers: dict[str, str],
    start_date: str = "2000-01-01",
    lookback_days: int = 252,
    volatility_window: int = 20,
    target_volatility: float = 0.10,
    maximum_leverage: float = 2.0,
    transaction_cost_bps: float = 5,
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    """
    Apply the strategy separately to several ETFs.

    Returns
    -------
    metrics:
        Performance metrics for each asset.

    backtests:
        Backtest results for each asset.
    """

    metrics: dict[str, pd.Series] = {}
    backtests: dict[str, pd.DataFrame] = {}

    for name, ticker in tickers.items():
        data = download_price_data(
            ticker=ticker,
            start_date=start_date,
        )

        data = add_daily_returns(data)

        prices = data["Close"].squeeze()
        returns = data["Return"].squeeze()

        volatility = calculate_rolling_volatility(
            returns=returns,
            window=volatility_window,
        )

        scaler = calculate_volatility_scaler(
            volatility=volatility,
            target_volatility=target_volatility,
            maximum_leverage=maximum_leverage,
        )

        signal = generate_momentum_signal(
            prices=prices,
            lookback_days=lookback_days,
        )

        backtest = run_backtest(
            returns=returns,
            signal=signal,
            volatility_scaler=scaler,
            transaction_cost_bps=transaction_cost_bps,
        )

        backtests[name] = backtest

        metrics[name] = calculate_performance_metrics(
            backtest["Net_Strategy_Return"]
        )

    metrics_frame = pd.DataFrame(metrics).T

    return metrics_frame, backtests


def build_strategy_return_matrix(
    backtests: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Combine the net strategy returns of all assets into one DataFrame.
    """

    if not backtests:
        raise ValueError("backtests cannot be empty.")

    strategy_returns = {}

    for asset, result in backtests.items():
        if "Net_Strategy_Return" not in result.columns:
            raise KeyError(
                f"'Net_Strategy_Return' is missing for asset {asset}."
            )

        strategy_returns[asset] = result["Net_Strategy_Return"]

    return pd.DataFrame(strategy_returns).dropna()


def calculate_inverse_volatility_weights(
    strategy_returns: pd.DataFrame,
    window: int = 20,
) -> pd.DataFrame:
    """
    Calculate lagged inverse-volatility portfolio weights.

    Assets with lower recent volatility receive larger weights.
    Weights are normalized to sum to one.
    """

    if window <= 0:
        raise ValueError("window must be positive.")

    if strategy_returns.empty:
        raise ValueError("strategy_returns cannot be empty.")

    rolling_volatility = (
        strategy_returns
        .rolling(window=window)
        .std()
        .shift(1)
    )

    inverse_volatility = 1 / rolling_volatility.replace(
        0,
        np.nan,
    )

    weights = inverse_volatility.div(
        inverse_volatility.sum(axis=1),
        axis=0,
    )

    return weights.fillna(0.0)


def build_multi_asset_portfolio(
    strategy_returns: pd.DataFrame,
    weights: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build a multi-asset portfolio using strategy returns and weights.
    """

    if strategy_returns.empty:
        raise ValueError("strategy_returns cannot be empty.")

    if weights.empty:
        raise ValueError("weights cannot be empty.")

    aligned_returns, aligned_weights = strategy_returns.align(
        weights,
        join="inner",
        axis=0,
    )

    portfolio_return = (
        aligned_returns * aligned_weights
    ).sum(axis=1)

    portfolio_wealth = (
        1 + portfolio_return
    ).cumprod()

    return pd.DataFrame(
        {
            "Portfolio_Return": portfolio_return,
            "Portfolio_Wealth": portfolio_wealth,
        }
    )