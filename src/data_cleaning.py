import pandas as pd
import numpy as np

def filter_2024_data(data):
    data["Date"] = pd.to_datetime(data["Date"], utc=True)
    data_2024 = data[data['Date'].dt.year == 2024]
    return data_2024.sort_values('Date').reset_index(drop=True)

def summarize_data_quality(df):
    summary = pd.DataFrame({
        "NaN_count": df.isna().sum(),
        "Empty_count": (df.eq("")).sum()
    })
    return summary

def clean_and_aggregate(data_2024):
    data_2024 = data_2024.groupby(['Date', 'Ticker'], as_index=False).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
        'Brand_Name': 'first',
        'Industry_Tag': 'first',
        'Country': 'first',
        'Dividends': 'sum',
        'Stock Splits': 'sum',
        'Capital Gains': 'sum'
    })

    # remove last date
    data_2024 = data_2024[
        data_2024['Date'].dt.date != pd.to_datetime("2024-12-31").date()
    ]

    return data_2024

def get_valid_stocks(data_2024):
    stock_types = list(set(data_2024["Ticker"]))

    # remove problematic stock
    if 'CMG' in stock_types:
        stock_types.remove('CMG')

    example = data_2024[data_2024['Ticker'] == stock_types[0]].sort_values("Date")
    execution_dates = example['Date']

    valid_stocks = []
    for stock in stock_types:
        if len(data_2024[data_2024['Ticker'] == stock]) == len(execution_dates):
            valid_stocks.append(stock)

    return valid_stocks, execution_dates

def build_price_matrix(data_2024, stock_types, execution_dates):
    T = len(execution_dates)
    N = len(stock_types)

    prices = np.zeros((N, T))

    for i, stock in enumerate(stock_types):
        stock_data = data_2024[data_2024['Ticker'] == stock]
        stock_data = stock_data.sort_values("Date")

        prices[i, :] = stock_data['Open'].values

    return prices

def process_sp500(s_and_p):
    s_and_p["Date"] = pd.to_datetime(s_and_p["Date"], utc=True)
    s_and_p_2024 = s_and_p[s_and_p['Date'].dt.year == 2024]
    s_and_p_2024 = s_and_p_2024.iloc[::-1].reset_index(drop=True)

    return s_and_p_2024["Open"].values