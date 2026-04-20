from src.strategies import (
        equal_weight_strategy,
        momentum_strategy,
        momentum_strategy_with_cost,
        vol_strategies,
        Kelly_strategies,
        MV_strategies)
from src.visualization import plot_portfolio

def run_backtesting(prices):
    # =========================================================
    # STRATEGY CONFIGURATION
    # =========================================================

    strategies = [
        equal_weight_strategy,
        momentum_strategy,
        momentum_strategy_with_cost,
        vol_strategies,
        Kelly_strategies,
        MV_strategies
    ]

    strategy_names = [
        "Equal Weight strategy",
        "Momentum strategy",
        "Momentum strategy with cost",
        "Volatility parity strategy",
        "Kelly allocation strategy (long-only)",
        "Minimum variance strategy (long-only)"
    ]
# Change the Hyperparameter HERE!!
    strategy_params = [
        {"C": 1000},
        {"C": 1000},
        {"C": 1000, "cost": 0.001},
        {"C": 1000, "window": 30},
        {"C": 1000, "window": 30, "positive_weight": True},
        {"C": 1000, "window": 30, "positive_weight": True}
    ]

    # =========================================================
    # RUN BACKTESTS
    # (IMPORTANT: assumes `prices` is provided externally)
    # =========================================================

    results = {}

    for i, strategy in enumerate(strategies):
        params = strategy_params[i]

        portfolio = strategy(prices, **params)

        plot_portfolio(portfolio, strategy_names[i])

        results[strategy_names[i]] = portfolio

    return results


# Optional direct execution
if __name__ == "__main__":
    raise RuntimeError(
        "run_backtesting() requires 'prices'. Import and call it from main.py"
    )