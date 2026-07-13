import yfinance as yf
import pandas as pd


def download_data(
    ticker: str,
    start: str = "2000-01-01",
    end: str = None,
):
    """
    Download historical price data.

    Parameters
    ----------
    ticker : str
        Stock ticker.
    start : str
        Start date.
    end : str
        End date.

    Returns
    -------
    pandas.DataFrame
    """

    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
    )

    df.dropna(inplace=True)

    return df
