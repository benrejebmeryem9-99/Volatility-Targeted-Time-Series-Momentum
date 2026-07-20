import pandas as pd

from src.backtest import run_backtest


def create_test_data():
    dates = pd.date_range(
        start="2024-01-01",
        periods=5,
        freq="D",
    )

    returns = pd.Series(
        [0.01, -0.02, 0.015, 0.005, -0.01],
        index=dates,
        name="Return",
    )

    signal = pd.Series(
        [0.0, 1.0, -1.0, 1.0, 1.0],
        index=dates,
        name="Momentum_Signal",
    )

    scaler = pd.Series(
        [1.0, 1.0, 1.0, 1.0, 1.0],
        index=dates,
        name="Volatility_Scaler",
    )

    return returns, signal, scaler


def test_backtest_returns_expected_columns():
    returns, signal, scaler = create_test_data()

    result = run_backtest(
        returns=returns,
        signal=signal,
        volatility_scaler=scaler,
        transaction_cost_bps=5,
    )

    expected_columns = {
        "Asset_Return",
        "Momentum_Signal",
        "Volatility_Scaler",
        "Position",
        "Gross_Strategy_Return",
        "Turnover",
        "Transaction_Cost",
        "Net_Strategy_Return",
        "Buy_and_Hold_Wealth",
        "Strategy_Wealth",
    }

    assert expected_columns.issubset(result.columns)


def test_backtest_output_index_is_correct():
    returns, signal, scaler = create_test_data()

    result = run_backtest(
        returns=returns,
        signal=signal,
        volatility_scaler=scaler,
        transaction_cost_bps=5,
    )

    assert result.index.equals(returns.index[1:])


def test_transaction_costs_are_non_negative():
    returns, signal, scaler = create_test_data()

    result = run_backtest(
        returns=returns,
        signal=signal,
        volatility_scaler=scaler,
        transaction_cost_bps=5,
    )

    assert (result["Transaction_Cost"] >= 0).all()


def test_net_return_equals_gross_return_minus_cost():
    returns, signal, scaler = create_test_data()

    result = run_backtest(
        returns=returns,
        signal=signal,
        volatility_scaler=scaler,
        transaction_cost_bps=5,
    )

    expected_net_return = (
        result["Gross_Strategy_Return"]
        - result["Transaction_Cost"]
    )

    pd.testing.assert_series_equal(
        result["Net_Strategy_Return"],
        expected_net_return,
        check_names=False,
    )