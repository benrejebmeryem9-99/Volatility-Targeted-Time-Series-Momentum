import pandas as pd

from src.backtest import run_backtest
from src.metrics import calculate_performance_metrics
from src.signals import generate_momentum_signal
from src.volatility import calculate_volatility_scaler


def compare_lookback_periods(
    prices: pd.Series,
    returns: pd.Series,
    volatility: pd.Series,
    lookback_periods: list[int],
    target_volatility: float = 0.10,
    maximum_leverage: float = 2.0,
    transaction_cost_bps: float = 5.0,
) -> tuple[pd.DataFrame, dict[int, pd.DataFrame]]:
    """Compare momentum strategies with different lookback periods."""

    if not lookback_periods:
        raise ValueError("lookback_periods cannot be empty.")

    scaler = calculate_volatility_scaler(
        volatility=volatility,
        target_volatility=target_volatility,
        maximum_leverage=maximum_leverage,
    )

    metrics_results = {}
    backtest_results = {}

    for lookback in lookback_periods:
        if lookback <= 0:
            raise ValueError(
                "Every lookback period must be positive."
            )

        signal = generate_momentum_signal(
            prices=prices,
            lookback_days=lookback,
        )

        backtest = run_backtest(
            returns=returns,
            signal=signal,
            volatility_scaler=scaler,
            transaction_cost_bps=transaction_cost_bps,
        )

        metrics = calculate_performance_metrics(
            backtest["Net_Strategy_Return"]
        )

        metrics_results[f"{lookback} days"] = metrics
        backtest_results[lookback] = backtest

    metrics_table = pd.DataFrame(metrics_results).T

    return metrics_table, backtest_results 