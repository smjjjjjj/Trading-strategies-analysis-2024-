import pandas as pd
import numpy as np

# You are given a prices array of shape (N, T), where N = number of stocks and T = number of days.
# Return a (N, T-1) array of daily log returns.
def daily_log_returns(timeseries):
    N = np.shape(timeseries)[0]
    T = np.shape(timeseries)[1]
    daily_return = np.zeros((N, T-1))
    for day in range(1, T):
        daily_return[:, day - 1] = np.log(timeseries[:, day] / timeseries[:, day-1])
    return daily_return

def rolling_sharpe_ratio(timeseries, K = 30): # Here the time series is 1D.
    T = len(timeseries)
    if T <= K:
        raise Exception("Please enlarge K so that the pricing period covers the look-back period")
    Sharpe_ratio = [np.nan] * K
    for day in range(K, T):
        log_return = daily_log_returns(np.array([timeseries[day - K: day]]))
        Sharpe_ratio.append(np.mean(log_return)/np.std(log_return, ddof = 1)) # In short period, assume risk-free rate is zero
    return Sharpe_ratio