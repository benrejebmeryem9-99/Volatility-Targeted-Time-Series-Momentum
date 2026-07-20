import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_cagr(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS,
) -> float:
    """Calculate the compound annual growth rate."""

    clean_returns = returns.dropna()

    if clean_returns.empty:
        return np.nan

    total_return = (1 + clean_returns).prod()
    number_of_years = len(clean_returns) / periods_per_year

    if number_of_years <= 0 or total_return <= 0:
        return np.nan

    return total_return ** (1 / number_of_years) - 1


def calculate_annualized_volatility(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS,
) -> float:
    """Calculate annualized return volatility."""

    return returns.dropna().std() * np.sqrt(periods_per_year)


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = TRADING_DAYS,
) -> float:
    """Calculate the annualized Sharpe ratio."""

    clean_returns = returns.dropna()

    if clean_returns.empty:
        return np.nan

    daily_risk_free_rate = risk_free_rate / periods_per_year
    excess_returns = clean_returns - daily_risk_free_rate
    volatility = excess_returns.std()

    if volatility == 0:
        return np.nan

    return (
        excess_returns.mean()
        / volatility
        * np.sqrt(periods_per_year)
    )


def calculate_sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = TRADING_DAYS,
) -> float:
    """Calculate the annualized Sortino ratio."""

    clean_returns = returns.dropna()

    if clean_returns.empty:
        return np.nan

    daily_risk_free_rate = risk_free_rate / periods_per_year
    excess_returns = clean_returns - daily_risk_free_rate

    downside_returns = excess_returns[
        excess_returns < 0
    ]

    downside_deviation = downside_returns.std()

    if downside_deviation == 0 or np.isnan(downside_deviation):
        return np.nan

    return (
        excess_returns.mean()
        / downside_deviation
        * np.sqrt(periods_per_year)
    )


def calculate_max_drawdown(
    returns: pd.Series,
) -> float:
    """Calculate maximum drawdown from a return series."""

    wealth = (1 + returns.dropna()).cumprod()
    running_peak = wealth.cummax()
    drawdown = wealth / running_peak - 1

    return drawdown.min()


def calculate_calmar_ratio(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS,
) -> float:
    """Calculate the Calmar ratio."""

    cagr = calculate_cagr(
        returns,
        periods_per_year=periods_per_year,
    )

    max_drawdown = calculate_max_drawdown(returns)

    if max_drawdown == 0 or np.isnan(max_drawdown):
        return np.nan

    return cagr / abs(max_drawdown)


def calculate_performance_metrics(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = TRADING_DAYS,
) -> pd.Series:
    """Calculate the main strategy performance metrics."""

    return pd.Series(
        {
            "CAGR": calculate_cagr(
                returns,
                periods_per_year,
            ),
            "Annualized Volatility": (
                calculate_annualized_volatility(
                    returns,
                    periods_per_year,
                )
            ),
            "Sharpe Ratio": calculate_sharpe_ratio(
                returns,
                risk_free_rate,
                periods_per_year,
            ),
            "Sortino Ratio": calculate_sortino_ratio(
                returns,
                risk_free_rate,
                periods_per_year,
            ),
            "Maximum Drawdown": calculate_max_drawdown(
                returns
            ),
            "Calmar Ratio": calculate_calmar_ratio(
                returns,
                periods_per_year,
            ),
        }
    )
