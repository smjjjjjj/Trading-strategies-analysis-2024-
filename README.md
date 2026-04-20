# Trading-strategies-analysis (2024)
**Project type:** Quantitative Finance — Backtesting & Risk Analysis  
**Languages/Libs:** Python, NumPy, pandas, matplotlib

## Summary
This project collects historical price data for 58 U.S. stocks and the S&P 500 ETF, performs data cleaning, implements multiple portfolio allocation strategies (Equal-Weight, Momentum, Volatility Parity, Kelly Criterion, Minimum-Variance), and backtests them over 2024. For each strategy we produce equity curves, calculate performance metrics (volatility, Sharpe), and compare risk metrics (VaR, max drawdown).
## Features

- Data preprocessing and cleaning
- Factor analysis (beta estimation)
- Correlation-based clustering
- Strategy implementation:
  - Equal Weight
  - Momentum
  - Momentum with transaction costs
  - Volatility Parity
  - Kelly Criterion
  - Minimum Variance
- Backtesting engine
- Performance metrics:
  - Sharpe Ratio
  - Value at Risk (VaR)
  - Maximum Drawdown

# Project Structure

├── src/              # Core logic (strategies, metrics, etc.)
├── scripts/          # Pipeline scripts
├── data/             # Data, as zip file
├── notebook/         # Exploratory analysis
├── results/          # Output plots / reports
├── main.py           # Entry point
├── requirements.txt

## Installation

```bash
pip install -r requirements.txt
```
## Data
Two datasets are used here, both could be downloaded from Kaggle:
- `World_stock_price_dataset.csv`: Stock prices from 2000 to 2025 (from https://www.kaggle.com/datasets/nelgiriyewithana/world-stock-prices-daily-updating?resource=download).
- `S_and_P_500_dataset.csv`: S&P 500 ETF prices from 1993 to 2024 (from: https://www.kaggle.com/datasets/yousefeddin/s-and-p-500-stock-price-end-of-2024).
The datasets are compressed and stored under data/raw, which could be decompressed directly to be used.
PLEASE place them in the `data/raw` folder BEFORE running the code!

## Usage

### Run full pipeline

```bash
python main.py
```

Runs the entire workflow: data processing → strategy backtesting → evaluation.

---

### Run individual components

#### Data analysis (cleaning, clustering, factor analysis)

```bash
python scripts/run_analysis.py
```

#### Backtesting strategies

```bash
python scripts/run_backtests.py
```

#### Performance evaluation

```bash
python scripts/run_evaluation.py
```

## Sample visual results
Consider the maximum drawdown (largest peak-to-trough loss) of each portfolio strategy:
![Max Drawdown](Figures/Maximum%20drawdown.png)


## Sample table results
Ranking through three metrics: Sharpe ratio, VaR (at level 95%) and maximum drawdown
| Strategy                                   | Sharpe Ratio Rank | VaR (95%) Rank | Max Drawdown Rank |
|--------------------------------------------|------------------|----------------|------------------|
| Equal Weight Strategy                       | 3                | 3              | 5                |
| Momentum Allocation Strategy                | 2                | 4              | 3                |
| Momentum Allocation Strategy (Cost 0.1%)    | 5                | 5              | 4                |
| Volatility Parity Strategy                  | 4                | 2              | 1                |
| Kelly Strategy (Long-Only)                  | 6                | 6              | 6                |
| Minimum Variance Strategy (Long-Only)       | 1                | 1              | 2                |



## Conclusions
- **Minimum-Variance Strategy** delivered the best risk-adjusted performance, achieving top Sharpe ratio and lowest VaR, as its allocation favors low-volatility assets and naturally diversifies risk.
- **Volatility Parity Strategy** had the lowest maximum drawdown because it dynamically scaled exposure to risky stocks down during volatile periods, limiting large losses.
- **Momentum Strategy (No Cost)** generated strong returns by riding short-term trends, but its higher turnover led to larger drawdowns during reversals.
- **Momentum Strategy (With Costs)** underperformed significantly once transaction costs were included, highlighting the importance of execution costs in high-turnover strategies.
- **Kelly Criterion Strategy** was the most aggressive, leading to large swings in portfolio value and the weakest Sharpe ratio, as real-world returns are rarely stationary enough to justify full Kelly betting.
- **Equal-Weight Strategy** served as a balanced benchmark: reasonable performance, moderate drawdowns, but no risk targeting — leaving room for improvement versus optimized approaches.


## Complete notebook files and results
- `notebook/Stock_price_project.ipynb` — cleaned notebook ready for GitHub.
- `results/Stock_price_project_results.pdf` — full PDF report with figures and results.
