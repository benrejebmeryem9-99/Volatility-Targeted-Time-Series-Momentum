from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_wealth_curves(
    results: pd.DataFrame,
    output_path: str | None = None,
) -> None:
    """Plot strategy and buy-and-hold cumulative wealth."""

    required_columns = {
        "Strategy_Wealth",
        "Buy_and_Hold_Wealth",
    }

    missing_columns = required_columns.difference(results.columns)

    if missing_columns:
        raise KeyError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    plt.figure(figsize=(12, 6))

    plt.plot(
        results.index,
        results["Strategy_Wealth"],
        label="Volatility-Targeted Momentum",
    )

    plt.plot(
        results.index,
        results["Buy_and_Hold_Wealth"],
        label="Buy and Hold",
    )

    plt.title("Cumulative Wealth Comparison")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, dpi=300, bbox_inches="tight")

    plt.show()


def calculate_drawdown(
    wealth: pd.Series,
) -> pd.Series:
    """Calculate drawdown from a cumulative wealth series."""

    running_peak = wealth.cummax()

    return wealth / running_peak - 1


def plot_drawdowns(
    results: pd.DataFrame,
    output_path: str | None = None,
) -> None:
    """Plot strategy and buy-and-hold drawdowns."""

    strategy_drawdown = calculate_drawdown(
        results["Strategy_Wealth"]
    )

    benchmark_drawdown = calculate_drawdown(
        results["Buy_and_Hold_Wealth"]
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        results.index,
        strategy_drawdown,
        label="Volatility-Targeted Momentum",
    )

    plt.plot(
        results.index,
        benchmark_drawdown,
        label="Buy and Hold",
    )

    plt.title("Drawdown Comparison")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, dpi=300, bbox_inches="tight")

    plt.show()
    