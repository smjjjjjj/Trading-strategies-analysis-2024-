import pandas as pd

# --------------If you want to use your own dataset, just change the following two lines ------------------
# Data source: https://www.kaggle.com/datasets/nelgiriyewithana/world-stock-prices-daily-updating/versions/400?resource=download
def load_data(stock_price_dataset, S_P_500_dataset):
    data = pd.read_csv('data/raw/' + stock_price_dataset, encoding='utf-8')
    s_and_p = pd.read_csv('data/raw/' + S_P_500_dataset, encoding='utf-8')
    return data, s_and_p