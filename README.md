<div align="center">

# Volatility-Targeted Time-Series Momentum

### A Multi-Asset Quantitative Finance Research Project

Dynamic Risk Management • Time-Series Momentum • Portfolio Construction • Open Science

<br>

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?style=for-the-badge&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?style=for-the-badge)

<br>

![Research](https://img.shields.io/badge/Research-Quantitative%20Finance-0055A4?style=flat-square)
![Momentum](https://img.shields.io/badge/Strategy-Time--Series%20Momentum-success?style=flat-square)
![Risk](https://img.shields.io/badge/Risk-Volatility%20Targeting-red?style=flat-square)
![Portfolio](https://img.shields.io/badge/Portfolio-Multi--Asset-purple?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)
![Open Source](https://img.shields.io/badge/Open%20Science-Reproducible-blueviolet?style=flat-square)

</div>

# Project Overview

Volatility-targeted investing has become one of the most influential approaches to dynamic risk management in quantitative finance. Rather than maintaining constant portfolio exposure, volatility-targeted strategies continuously adjust leverage according to changing market conditions in an effort to stabilize portfolio risk.

This project develops and evaluates a **Volatility-Targeted Time-Series Momentum (VTM)** strategy using a diversified portfolio of exchange-traded funds (ETFs) representing multiple asset classes. The complete framework progresses from a single-asset implementation to a diversified multi-asset portfolio before introducing **portfolio-level volatility targeting**.

The project is fully implemented in **Python**, follows a modular software architecture, includes **unit tests**, and provides a fully reproducible research notebook.

---

# Research Question

> **Can portfolio-level volatility targeting improve the risk-adjusted performance of a diversified time-series momentum strategy compared with a conventional momentum portfolio?**

---

# Methodology

The complete strategy follows the workflow below.

```text
Historical Market Data
          │
          ▼
 Daily Return Calculation
          │
          ▼
 Momentum Signal Generation
          │
          ▼
 Rolling Volatility Estimation
          │
          ▼
 Position Scaling
          │
          ▼
 Multi-Asset Portfolio Construction
          │
          ▼
 Portfolio-Level Volatility Targeting
          │
          ▼
 Performance Evaluation
```

---

# Strategy Components

The framework consists of the following modules:

- Historical market data collection
- Daily return calculation
- Time-series momentum signal generation
- Rolling volatility estimation
- Volatility scaling
- Transaction cost modelling
- Single-asset backtesting
- Multi-asset portfolio construction
- Portfolio-level volatility targeting
- Performance evaluation
- Robustness analysis

---

# Asset Universe

The strategy is evaluated across six representative ETFs covering multiple asset classes.

| ETF | Asset Class |
|------|-------------|
| SPY | U.S. Equities |
| QQQ | Technology Equities |
| GLD | Gold |
| TLT | Long-Term U.S. Treasury Bonds |
| DBC | Commodities |
| VNQ | Real Estate |

---

# Repository Structure

```text
Volatility-Targeted-Time-Series-Momentum/

├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_Analysis.ipynb
│   └── 02_Main_Backtest.ipynb
│
├── results/
│   ├── figures/
│   ├── performance_metrics.csv
│   ├── multi_asset_metrics.csv
│   ├── portfolio_metrics.csv
│   └── portfolio_weights.csv
│
├── src/
│   ├── backtest.py
│   ├── data_loader.py
│   ├── experiments.py
│   ├── metrics.py
│   ├── multi_asset.py
│   ├── signals.py
│   ├── visualization.py
│   └── volatility.py
│
├── tests/
│   ├── test_backtest.py
│   ├── test_metrics.py
│   ├── test_no_lookahead.py
│   └── test_volatility.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Key Results

The study compares:

- Buy-and-Hold
- Single-Asset Momentum Strategy
- Diversified Multi-Asset Portfolio
- Portfolio-Level Volatility Targeting

Portfolio-level volatility targeting improved the overall risk-adjusted performance by restoring the portfolio to the desired **10% annualized volatility target**, increasing annualized return while improving the Sharpe, Sortino and Calmar ratios.

---

# Figures

## Wealth Curve

<p align="center">
<img src="results/wealth_curves.png" width="850">
</p>

---

## Drawdown Comparison

<p align="center">
<img src="results/drawdowns.png" width="850">
</p>

---

## Portfolio Allocation

*(Generated in the notebook.)*

---

## Portfolio Volatility

*(Generated in the notebook.)*

---

# Main Features

- Modular Python implementation
- Fully reproducible research notebook
- Multi-asset portfolio construction
- Portfolio-level volatility targeting
- Transaction cost modelling
- Unit testing
- Professional visualization
- Clean software architecture

---

# Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- PyTest
- Jupyter Notebook

---

# Installation

Clone the repository:

```bash
git clone https://github.com/benrejebmeryem9-99/Volatility-Targeted-Time-Series-Momentum.git
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the main notebook:

```text
notebooks/02_Main_Backtest.ipynb
```

---

# References

- Moskowitz, T., Ooi, Y., & Pedersen, L. (2012). *Time Series Momentum*. Journal of Financial Economics.
- Moreira, A., & Muir, T. (2017). *Volatility-Managed Portfolios*. Journal of Finance.
- Barroso, P., & Santa-Clara, P. (2015). *Momentum Has Its Moments*. Journal of Financial Economics.
- Hurst, B., Ooi, Y., & Pedersen, L. (2017). *A Century of Evidence on Trend-Following Investing*.

---



# License

This project is released under the MIT License.

---

<div align="center">


</div>