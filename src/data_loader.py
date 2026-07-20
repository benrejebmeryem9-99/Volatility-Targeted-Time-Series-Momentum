from pathlib import Path

import pandas as pd
import yfinance as yf


def download_price_data(
    ticker: str,
    start_date: str,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Download adjusted historical market data from Yahoo Finance."""

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No data was downloaded for ticker: {ticker}")

    data = data.dropna().copy()
    data.index = pd.to_datetime(data.index)
    data.index.name = "Date"

    return data


def add_daily_returns(data: pd.DataFrame) -> pd.DataFrame:
    """Add simple daily returns calculated from adjusted closing prices."""

    result = data.copy()

    if "Close" not in result.columns:
        raise KeyError("The DataFrame must contain a 'Close' column.")

    result["Return"] = result["Close"].pct_change()

    return result.dropna()


def save_data(data: pd.DataFrame, file_path: str) -> None:
    """Save a DataFrame as a CSV file."""

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path) 