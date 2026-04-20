import numpy as np
import cvxpy as cp
from src.metrics import daily_log_returns

# Given prices (N, T) and initial capital C, backtest a strategy where you always hold equal weights 
# in all assets, rebalancing daily.
# Return the portfolio values (into a list):
def equal_weight_strategy(timeseries, C=1000):
    N = np.shape(timeseries)[0]
    T = np.shape(timeseries)[1]
    shares = (C/N) / timeseries[:, 0]
    port_value = [C]
    value = C
    for t in range(1, T):
        value  = timeseries[:, t] @ shares
        port_value.append(value) 
    # Rebalance, but always equal weight:
        shares = (value/N)/ timeseries[:, t]
    return port_value

# Momentum Allocation Strategies:
# Allocate to stocks proportionally to their last day’s return (skip negatives, keep in cash).
# Backtest over the whole dataset and return final value.
def momentum_strategy(timeseries, C=1000):
    N = np.shape(timeseries)[0]
    T = np.shape(timeseries)[1]
    port_value = [C]
    value = C
    shares = np.array([0]*N)
    for t in range(1, T):
        if np.all(shares == 0):
            port_value.append(value)
        else:
            value = timeseries[:, t] @ shares
            port_value.append(value)
        
        # Rebalance
        ret = (timeseries[:, t] - timeseries[:, t-1])/timeseries[:, t-1]
        # We skip negatives
        ret[ret <0] = 0
        
        if np.all(ret == 0):
            shares = np.array([0]*N)
        else:
            weight = ret/np.sum(ret)
            shares = value * weight / timeseries[:, t]
    return port_value

# Repeat the momentum allocation strategy, but include a 0.1% transaction cost every time changing allocations.
# Return portfolio values.
def momentum_strategy_with_cost(timeseries, C=1000, cost = 0.001):
    N = np.shape(timeseries)[0]
    T = np.shape(timeseries)[1]
    port_value = [C]
    value = C
    shares = np.array([0]*N)
    for t in range(1, T):
        if np.all(shares == 0):
            port_value.append(value)
        else:
            # Take the transaction cost into consideration, if the allocations are changed.
            value = timeseries[:, t] @ shares * (1-cost)
            port_value.append(value)
        
        # Rebalance
        ret = (timeseries[:, t] - timeseries[:, t-1])/timeseries[:, t-1]
        ret[ret <0] = 0
        if np.all(ret == 0):
            shares = np.array([0]*N)
        else:
            weight = ret/np.sum(ret)
            shares = value * weight / timeseries[:, t]
    return port_value

# At each day t, compute each stock’s volatility over the last K=30 days.
# Allocate inversely to volatility (higher weight to low-vol stocks).
# Return daily portfolio values.
def vol_strategies(timeseries, C=1000, window = 30):
    N = np.shape(timeseries)[0]
    T = np.shape(timeseries)[1]
    # Exclude the case that the price period given cannot cover the lookback window.
    if T <= window:
        raise Exception("Please enlarge window so that the pricing period covers the look-back period")
    
    # Allow for the first K day to be uninvested, wait until the lookback window is gone.
    portfolio_value = [C]*window
    value = C
    weight = np.array(N*[0])
    shares = np.array(N*[0])
    for day in range(window,T):
        if np.all(shares == 0):
            portfolio_value.append(value)
        else:
            value = timeseries[:, day]@ shares
            portfolio_value.append(value)
            
    # Rebalance
        log_return_last_K = daily_log_returns(timeseries[:, (day-window): day])
        hist_vola = np.array([np.std(log_return_last_K[stock_num], ddof = 1) for stock_num in range(N)])
        # Use a small epsilon to avoid numerical issues.
        hist_vola = np.where(hist_vola == 0, 1e-8, hist_vola)
        # Compute weight, letting lower-volatility stocks to have higher weight
        weight = (1/hist_vola)/ np.sum((1/hist_vola))
        shares = value * weight/ timeseries[:, day]
    return portfolio_value

# At each day, compute daily return distribution across stocks. Use Kelly formula to allocate weights.
# Use a rolling window of K = 30 days to estimate the covariance.
def Kelly_strategies(timeseries, C=1000,  window = 30, positive_weight = True):
    # Here is an additional input of positive_weight. The reason is the following:
    # The Kelly optimal weights are determined by the maximization problem w^T \mu-0.5 w^T \Sigma w, under constraint sum(w) == 1.
    # Mathematically, they are equivalent to w_t = \Sigma_t^{-1} \mu_t with normalization where:
    # Sigma_t is the covariance function and \mu_t is the daily log return function at time point t.
    # For the case when positive_weight is set to be False, we use the second form, since it is numerically better.
    # If it is set to be True, then we use the first form (maximization problem), but with extra constraint of w>= 0
    # It turns out that imposing positive weights always performs better, since our rolling window 30 is not larger enough.
    # Therefore, the covariance matrix could not be accurate enough, and the portfolio value will have strong fluctuations.
    # Especially under the case that we allow for short positions.
    N = np.shape(timeseries)[0]
    T = np.shape(timeseries)[1]
    if T <= window:
        raise Exception("Please enlarge window so that the pricing period covers the look-back period")
    portfolio_value = [C]*window
    value = C
    weight = np.array(N*[0])
    shares = np.array(N*[0])
    for day in range(window, T):
        if np.all(shares == 0):
            portfolio_value.append(value)
        else:
            value = timeseries[:, day]@ shares
            portfolio_value.append(value)
        
    # Rebalance:
        prices_last_K = timeseries[:, (day - window):day]
        daily_return_last_K = np.exp(daily_log_returns(prices_last_K))-1
        mu = np.mean(daily_return_last_K, axis = 1)
        sigma = np.cov(daily_return_last_K, ddof = 1)
        w = cp.Variable(N)
        objective = cp.Maximize(mu @ w - 0.5 * cp.quad_form(w, sigma))
    # Differ the case between whether imposing positive weights:    
        if positive_weight:
    # Use the maximization form:
            constraints = [cp.sum(w) == 1, w >= 0]
            prob = cp.Problem(objective, constraints)
            prob.solve()
            if prob.status not in ["optimal", "optimal_inaccurate"]:
                raise ValueError("No optimal solution found")
            weight = np.array(w.value).flatten()
    # Use the linear equation system form:
        else:
            weight = np.linalg.solve(sigma, mu)
            if not np.all(weight == 0):
                weight = weight/ np.sum(weight)
        
        shares = value * weight / timeseries[:, day]
    return portfolio_value
  

  # Given covariance matrix of stock returns, compute weights for the minimum variance portfolio.
# Return the weight vector.

# Similarly, for the minimum variance weight, one option is to minimize the variance w^T \Sigma w under constraint sum(w) = 1;
# Or, alternatively, we could use the explicit solution of \Sigma w = 1, where 1 is the one vector, and normalize them.
# If we impose the extra condition of long only, then we need to use the first definition by adding extra constraint of w>= 0.
def minimum_variance_weight(covariance):
    N, T = np.shape(covariance)
    if N != T:
        raise Exception("Input matrix is not a covariance matrix, please double check further.")
    one = np.ones(N)
    nominator = np.linalg.solve(covariance, one)
    return nominator/(one @ nominator)

def minimum_variance_weight_long_only(sigma):
    N = sigma.shape[0]
    w = cp.Variable(N)

    # Objective: minimize variance = w^T Σ w
    objective = cp.Minimize(cp.quad_form(w, sigma))

    # Constraints: weights sum to 1 and are non-negative
    constraints = [cp.sum(w) == 1, w >= 0]

    prob = cp.Problem(objective, constraints)
    prob.solve()

    if prob.status not in ["optimal", "optimal_inaccurate"]:
        raise ValueError("QP solver did not find a solution!")

    return np.array(w.value).flatten()

# At each day, compute daily return distribution across stocks. Use minimum variance formula to allocate weights.
# Use a rolling window of K = 30 days to estimate the covariance.
def MV_strategies(timeseries, C,  window = 30, positive_weight = True):
    
    N = np.shape(timeseries)[0]
    T = np.shape(timeseries)[1]
    if T <= window:
        raise Exception("Please enlarge window so that the pricing period covers the look-back period")
    portfolio_value = [C]*window
    value = C
    weight = np.array(N*[0])
    shares = np.array(N*[0])
    for day in range(window, T):
        if np.all(shares == 0):
            portfolio_value.append(value)
        else:
            value = timeseries[:, day]@ shares
            portfolio_value.append(value)
        
    # Rebalance
        prices_last_K = timeseries[:, (day - window):day]
        daily_return_last_K = np.exp(daily_log_returns(prices_last_K))-1
        sigma = np.cov(daily_return_last_K,rowvar=True,  ddof = 1)
        if positive_weight: 
        # Similarly, under the case that positive_weight = True, we use the optimizing problem;
            weight = minimum_variance_weight_long_only(sigma)
        else:
        # under the case that positive_weight = False, we use the linear equation system for numerical reasons.
            weight = minimum_variance_weight(sigma)
        shares = value * weight / timeseries[:, day]
    return portfolio_value
