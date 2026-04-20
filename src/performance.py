import numpy as np
from src.metrics import daily_log_returns
def annualized_sharpe_ratio(timeseries, risk_free_rate=0.0): # Here the timeseries should be an 1D array
    T = len(timeseries)

    simple_returns = np.exp(daily_log_returns(np.array([timeseries])))-1

    excess_returns = simple_returns - risk_free_rate / T
    
    mean_excess = np.mean(excess_returns)
    std_excess = np.std(excess_returns, ddof=1)
    
    sharpe = mean_excess / std_excess
    
    sharpe_annualized = sharpe * np.sqrt(T)
    return sharpe_annualized

# Given daily portfolio returns, compute the historical VaR at confidence level α = 0.95.
# Return the 5% quantile of returns.
def historical_VaR(timeseries, alpha = 0.95): # Here the timeseries should be 1D
    return abs(np.quantile(timeseries, 1- alpha, method = "higher")) # Using the higher nearst method, which is more conservative.

# Given a portfolio value time series, compute the maximum drawdown (largest peak-to-trough loss), in percentage.
# Return the drawdown percentage and the indices where it starts and ends.
def maximum_drawdown(timeseries): # Here the time series is 1D.
    drawdown = 0
    idx = []
    for i in range(len(timeseries)-1):
        j = 1
        while i + j < len(timeseries) and timeseries[i+j] <= timeseries[i+j-1]:
            j += 1
        down_rate = (timeseries[i] - timeseries[i+j-1])/timeseries[i]
        if down_rate > drawdown:
            idx = [i, i+j-1]
            drawdown = down_rate
    return [drawdown]+idx