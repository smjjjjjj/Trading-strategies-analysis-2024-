import numpy as np
from src.metrics import daily_log_returns, rolling_sharpe_ratio
from src.factors import beta
from src.cluster import cluster, build_cluster_dict
from src.visualization import (
        plot_log_returns,
        plot_rolling_sharpe,
        plot_betas)
def run_analysis(prices, data_2024, sp500_prices, stocks):
    # ===== RETURNS =====
    returns = daily_log_returns(prices)
    plot_log_returns(returns)

    # ===== SHARPE EXAMPLE =====
    stock_name = "GOOGL"
    stock_price = (
        data_2024[data_2024["Ticker"] == stock_name]
        .sort_values("Date")["Open"]
        .values
    )

    sharpe = rolling_sharpe_ratio(stock_price)
    plot_rolling_sharpe(sharpe, 30, stock_name)

    # ===== BETA =====
    market_returns = daily_log_returns(np.array([sp500_prices]))[0]

    betas = beta(returns, market_returns)
    plot_betas(stocks, betas)

    # ===== CLUSTERING =====
    correlation_bound = 0.7
    clusters = cluster(prices, correlation_bound)
    cluster_dict = build_cluster_dict(clusters, stocks)

    sorted_groups = sorted(cluster_dict.items(), key=lambda x: len(x[1]), reverse=True)

    print('===== Groups (multiple stocks with correlation >= ' + str(correlation_bound) + ")=====")
    for i, (_, group) in enumerate(sorted_groups):
        if len(group) > 1:
            print(f"Group {i+1}: {group}")


if __name__ == "__main__":
    run_analysis()