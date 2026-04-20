import numpy as np

def beta(stock_log_returns, market_returns):
    # In default case, we use the log returns of the S&P 500 ETF prices as the market index.
    b = []
    for stock in stock_log_returns:
        # Do the linear regression between the market index (S&P 500 ETF) and the stock prices.
        b.append(np.polyfit(market_returns, stock, 1)[0])
    return np.array(b)