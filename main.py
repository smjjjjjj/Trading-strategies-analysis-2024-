from src.data_loader import load_data
from src.data_cleaning import (
    filter_2024_data,
    clean_and_aggregate,
    get_valid_stocks,
    build_price_matrix,
    process_sp500
)

from scripts.run_analysis import run_analysis
from scripts.run_backtests import run_backtesting
from scripts.run_evaluation import run_evaluation

# ===== DATA PIPELINE =====
data, sp500 = load_data(
    "World_stock_price_dataset.csv",
    "S_and_P_500_dataset.csv"
)

data_2024 = filter_2024_data(data)
data_2024 = clean_and_aggregate(data_2024)

stocks, dates = get_valid_stocks(data_2024)
prices = build_price_matrix(data_2024, stocks, dates)

sp500_prices = process_sp500(sp500)

# ===== ANALYSIS =====
run_analysis(prices, data_2024, sp500_prices, stocks)

# ===== BACKTEST =====
# Hyperparameters could be changed in run_backtests.py
results = run_backtesting(prices)

# ===== EVALUATION =====
risk_free_rate=0.0
alpha = 0.95
# If want to skip one metric, just set them into 0.
sharpe_ratio = 1
VAR = 1
max_drawdown = 1

run_evaluation(results, risk_free_rate, alpha, sharpe_ratio, VAR, max_drawdown)