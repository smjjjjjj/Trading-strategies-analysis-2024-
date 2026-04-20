import matplotlib.pyplot as plt
import numpy as np

def plot_log_returns(returns, N = 5):
    returns = returns[:N]
    T = returns.shape[1]
    time = np.arange(T)

    plt.figure(figsize=(12, 6))
    for i in range(len(returns)):
        plt.plot(time, returns[i])
    plt.title('Log return for asset number 1 to ' + str(N) + ', T = '+str(T) + ' days')
    plt.xlabel("Time")
    plt.ylabel("log returns")
    plt.show()

def plot_rolling_sharpe(sharpe, window, stock_name):
    T = len(sharpe)
    time = np.arange(T)

    plt.figure(figsize=(12, 6))
    plt.plot(time[window:], sharpe[window:])
    plt.title(f"Rolling Sharpe ({stock_name}, window={window})")
    plt.xlabel("Time")
    plt.ylabel("Sharpe Ratio")
    plt.show()

def plot_betas(stock_names, betas):
    sorted_idx = np.argsort(betas)[::-1]

    plt.figure(figsize=(14, 6))
    plt.bar([stock_names[i] for i in sorted_idx], betas[sorted_idx])
    plt.xticks(rotation=90)
    plt.xlabel("Stock")
    plt.ylabel("Beta")
    plt.title("Stocks Sorted by Beta")
    plt.tight_layout()
    plt.show()

def plot_portfolio(portfolio_value, title="Portfolio Value"):
    T = len(portfolio_value)
    time = np.arange(T)

    plt.figure(figsize=(12, 6))
    plt.plot(time, portfolio_value)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Portfolio Value")
    plt.show()