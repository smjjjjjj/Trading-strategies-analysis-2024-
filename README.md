# Trading-strategies-analysis (2024)
**Project type:** Quantitative Finance — Backtesting & Risk Analysis  
**Languages/Libs:** Python, NumPy, pandas, matplotlib

## Summary
This project collects historical price data for 58 U.S. stocks and the S&P 500 ETF, performs data cleaning, implements multiple portfolio allocation strategies (Equal-Weight, Momentum, Volatility Parity, Kelly Criterion, Minimum-Variance), and backtests them over 2024. For each strategy we produce equity curves, calculate performance metrics (volatility, Sharpe), and compare risk metrics (VaR, max drawdown).

## Sample visual results
Consider the maximum drawdown (largest peak-to-trough loss) of each portfolio strategy:
![Max Drawdown](Figures/Maximum%20drawdown.png)


## Sample table results
Ranking through three metrics: Sharpe ratio, VaR (at level 0.05) and maximum drawdown
| Strategy                                   | Sharpe Ratio Rank | VaR (0.05) Rank | Max Drawdown Rank |
|--------------------------------------------|------------------|----------------|------------------|
| Equal Weight Strategy                       | 3                | 3              | 5                |
| Momentum Allocation Strategy                | 2                | 4              | 3                |
| Momentum Allocation Strategy (Cost 0.1%)    | 5                | 5              | 4                |
| Volatility Parity Strategy                  | 4                | 2              | 1                |
| Kelly Strategy (Long-Only)                  | 6                | 6              | 6                |
| Minimum Variance Strategy (Long-Only)       | 1                | 1              | 2                |



## Conclusions
- **Volatility Parity** provided the most stable risk-adjusted performance (lowerst maximum drawdown).
- **Momentum (no cost)** outperformed on absolute returns but suffered higher drawdowns.
- **Kelly Criterion** showed aggressive allocation, leading to high volatility and large swings in portfolio value.
- Including **transaction costs** significantly reduced Momentum strategy returns, showing importance of execution assumptions.
- **Minimum-Variance** wass the best strategy overall, with the best sharpe ratio and VaR ranking.

## How to run
1. Place your CSV files in a `data/` folder next to the notebook:
   - `data/stocks.csv`
   - `data/sp500_etf.csv`
2. Open `Stock_price_project_clean.ipynb` with Jupyter and run cells top-to-bottom.
3. The notebook will create output figures inline.

## Files
- `Stock_price_project_clean.ipynb` — cleaned notebook ready for GitHub.
- `Stock_Price_Project_Report_with_Figures.pdf` — full PDF report with figures and results.
