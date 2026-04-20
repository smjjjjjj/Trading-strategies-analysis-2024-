from src.performance import (
        annualized_sharpe_ratio,
        historical_VaR,
        maximum_drawdown)
from src.metrics import daily_log_returns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def run_evaluation(results, risk_free_rate, alpha, sharpe_ratio, VAR, max_drawdown):
    print('===== Evaluation part=====')
    if sharpe_ratio == 1:
        print('----- Sharpe Ratio with risk free rate ' + str(risk_free_rate)+ '-----')
        sharpe_ratios = {
    "Equal weight strategy": annualized_sharpe_ratio(results["Equal Weight strategy"], risk_free_rate),
    "Momentum Allocation strategy": annualized_sharpe_ratio(results["Momentum strategy"], risk_free_rate),
    "Momentum Allocation strategy with cost": annualized_sharpe_ratio(results["Momentum strategy with cost"], risk_free_rate),
    "Volatility parity strategy": annualized_sharpe_ratio(results["Volatility parity strategy"], risk_free_rate),
    "Kelly strategy (long-only)": annualized_sharpe_ratio(results["Kelly allocation strategy (long-only)"], risk_free_rate),
    "Minimum variance strategy (long-only)": annualized_sharpe_ratio(results["Minimum variance strategy (long-only)"], risk_free_rate),
}
        print("Average Sharpe ratio of the following strategies:")
    for name, value in sharpe_ratios.items():
        print(f"-- {name}: {value:.4f}")

    best_strategy = max(sharpe_ratios, key=sharpe_ratios.get)
    worst_strategy = min(sharpe_ratios, key=sharpe_ratios.get)

    print("Based on the Sharpe ratio, the best performed strategy is " + str(best_strategy)+ ".")
    print("The worst performed strategy is " + str(worst_strategy) + ".")


    if VAR == 1:
        print('----- Historical value at risk level at  ' + str(alpha)+ '-----')
        var_results = {
    "Equal weight strategy": historical_VaR(daily_log_returns(np.array([results["Equal Weight strategy"]])), alpha),
    "Momentum Allocation strategy": historical_VaR(daily_log_returns(np.array([results["Momentum strategy"]])), alpha),
    "Momentum Allocation strategy with cost": historical_VaR(daily_log_returns(np.array([results["Momentum strategy with cost"]])), alpha),
    "Volatility parity strategy": historical_VaR(daily_log_returns(np.array([results["Volatility parity strategy"]])), alpha),
    "Kelly strategy (long-only)": historical_VaR(daily_log_returns(np.array([results["Kelly allocation strategy (long-only)"]])), alpha),
    "Minimum variance strategy (long-only)": historical_VaR(daily_log_returns(np.array([results["Minimum variance strategy (long-only)"]])), alpha),
}

        print("Historical VaR at the confidence level α = " + str(alpha) + " of :")
        for name, value in var_results.items():
            print(f"-- {name}: {value:.4f}")

# Lower (less negative) VaR is usually better (less risk)! 
        best_strategy = min(var_results, key=var_results.get)   
        worst_strategy = max(var_results, key=var_results.get)  

        print("Based on the historical VaR, the best performed strategy is " + str(best_strategy)+ ".")
        print("The worst performed strategy is " + str(worst_strategy) + ".")
    
    if max_drawdown == 1:
        # Backtesting on all strategies that are implemented above, visualize their maximum drawdown period.
        equal_weight_drawdown = maximum_drawdown(results["Equal Weight strategy"])
        Momentum_Allocation_drawdown = maximum_drawdown(results["Momentum strategy"])
        Momentum_Allocation_cost_drawdown = maximum_drawdown(results["Momentum strategy with cost"])
        Vol_drawdown = maximum_drawdown(results["Volatility parity strategy"])
        Kelly_drawdown = maximum_drawdown(results["Kelly allocation strategy (long-only)"])
        MV_drawdown = maximum_drawdown(results["Minimum variance strategy (long-only)"])
        T = len(results["Equal Weight strategy"])
        time = np.linspace(0, T, T)
        plt.figure(figsize=(12, 6))

        strategies = [
    ("Equal Weight", time, results["Equal Weight strategy"], equal_weight_drawdown, "blue"),
    ("Momentum Allocation", time, results["Momentum strategy"], Momentum_Allocation_drawdown, "green"),
    ("Momentum (With Cost)", time, results["Momentum strategy with cost"], Momentum_Allocation_cost_drawdown, "orange"),
    ("Volatility Strategy", time, results["Volatility parity strategy"], Vol_drawdown, "purple"),
    ("Kelly strategy (long only)", time, results["Kelly allocation strategy (long-only)"], Kelly_drawdown, "red"),
    ("Minimum variance strategy (long only)", time, results["Minimum variance strategy (long-only)"], MV_drawdown, "cyan")]

        for title, t, portfolio, dd, color in strategies:
            dd_rate, start_idx, end_idx = dd
            plt.plot(t, portfolio, label=f"{title} (Drawdown: {dd_rate*100:.1f}%)", color=color)
            # Highlight drawdown zone
            plt.axvspan(t[start_idx], t[end_idx], color=color, alpha=0.2)
            plt.scatter([t[start_idx], t[end_idx]],
                [portfolio[start_idx], portfolio[end_idx]],
                color=color, edgecolor="black", zorder=3)
        plt.title("Portfolio Values with Max Drawdowns Highlighted")
        plt.xlabel("Time Index")
        plt.ylabel("Portfolio Value")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        drawdowns = {
    "Equal weight strategy": equal_weight_drawdown[0],
    "Momentum Allocation strategy": Momentum_Allocation_drawdown[0],
    "Momentum Allocation strategy with cost": Momentum_Allocation_cost_drawdown[0],
    "Volatility parity strategy": Vol_drawdown[0],
    "Kelly strategy (long-only)": Kelly_drawdown[0],
    "Minimum variance strategy (long-only)": MV_drawdown[0]}

        best_strategy = min(drawdowns, key=drawdowns.get)   # min = smallest drawdown = best
        worst_strategy = max(drawdowns, key=drawdowns.get)  # max = largest drawdown = worst

        print("Based on the maximum drawdown, the best performed strategy is " + str(best_strategy)+ ".")
        print("The worst performed strategy is " + str(worst_strategy) + ".")
    
    if max_drawdown * VAR * sharpe_ratio == 1:
 # A short summary on the ranking for the above three metrics
        data = {
    "Equal weight strategy": {
        "Sharpe Ratio": sharpe_ratios["Equal weight strategy"],
        "0.05-VaR": var_results["Equal weight strategy"],
        "Max Drawdown": drawdowns["Equal weight strategy"]
    },
    "Momentum Allocation strategy": {
        "Sharpe Ratio": sharpe_ratios["Momentum Allocation strategy"],
        "0.05-VaR": var_results["Momentum Allocation strategy"],
        "Max Drawdown": drawdowns["Momentum Allocation strategy"]
    },
    "Momentum Allocation strategy with cost": {
        "Sharpe Ratio": sharpe_ratios["Momentum Allocation strategy with cost"],
        "0.05-VaR": var_results["Momentum Allocation strategy with cost"],
        "Max Drawdown": drawdowns["Momentum Allocation strategy with cost"]
    },
    "Volatility parity strategy": {
        "Sharpe Ratio": sharpe_ratios["Volatility parity strategy"],
        "0.05-VaR": var_results["Volatility parity strategy"],
        "Max Drawdown": drawdowns["Volatility parity strategy"]
    },
    "Kelly strategy (long-only)": {
        "Sharpe Ratio": sharpe_ratios["Kelly strategy (long-only)"],
        "0.05-VaR": var_results["Kelly strategy (long-only)"],
        "Max Drawdown": drawdowns["Kelly strategy (long-only)"]
    },
    "Minimum variance strategy (long-only)": {
        "Sharpe Ratio": sharpe_ratios["Minimum variance strategy (long-only)"],
        "0.05-VaR": var_results["Minimum variance strategy (long-only)"],
        "Max Drawdown": drawdowns["Minimum variance strategy (long-only)"]
    }
}

        df = pd.DataFrame(data).T  

# For Sharpe: higher is better → descending rank
# For VaR: Lower (closer to 0) is better → ascending rank
# For Drawdown: lower is better → ascending rank
        ranking_df = pd.DataFrame(index=df.index)
        ranking_df["Sharpe Ratio rank"] = df["Sharpe Ratio"].rank(ascending=False).astype(int)
        ranking_df["VaR (level = " + str(alpha) + ") rank"] = df["0.05-VaR"].rank(ascending=True).astype(int)
        ranking_df["Max Drawdown rank"] = df["Max Drawdown"].rank(ascending=True).astype(int)

        print("\n=== Strategy Ranking Table (1 = Best, 6 = Worst) ===")
        print(ranking_df)
