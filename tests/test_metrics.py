import numpy as np
import pandas as pd

from src.metrics import calculate_performance_metrics


def test_metrics_return_expected_names():
    returns = pd.Series(
        [0.01, -0.005, 0.012, -0.003, 0.008],
        index=pd.date_range("2024-01-01", periods=5),
    )

    metrics = calculate_performance_metrics(returns)

    expected_metrics = {
        "CAGR",
        "Annualized Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
        "Maximum Drawdown",
        "Calmar Ratio",
    }

    assert expected_metrics.issubset(metrics.index)


def test_annualized_volatility_is_non_negative():
    returns = pd.Series(
        [0.01, -0.02, 0.015, 0.005, -0.01],
    )

    metrics = calculate_performance_metrics(returns)

    assert metrics["Annualized Volatility"] >= 0


def test_maximum_drawdown_is_not_positive():
    returns = pd.Series(
        [0.01, -0.05, 0.02, -0.03, 0.01],
    )

    metrics = calculate_performance_metrics(returns)

    assert metrics["Maximum Drawdown"] <= 0


def test_metrics_do_not_contain_infinity():
    returns = pd.Series(
        [0.01, -0.005, 0.012, -0.003, 0.008],
    )

    metrics = calculate_performance_metrics(returns)

    assert not np.isinf(metrics.to_numpy(dtype=float)).any()