import pandas as pd
import numpy as np
import copy
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf
from datetime import datetime
from datetime import timedelta

# Check if ticker exist
def tickers_exists(tickers:list[str]):
    tickers_list = tickers
    for t in tickers_list:
        ticker = yf.Ticker(t)
        info = None
        error_list = []
        try:
            info = ticker.info
        except:
            print(f"Cannot get info of {t}, it probably does not exist")
            error_list.append(t)
            continue
        
        # Got the info of the ticker, do more stuff with it
        print(f"Info of {t}: {info}")
    if error_list.len() == 0:
        return [True, error_list]
    else:
        return [False, error_list]



# Import data
def getData(tickers:list, start_date:datetime, end_date:datetime):
    
    tickers_check = tickers_exists(tickers)
    if tickers_check[0]:
        df = yf.download(tickers,
                        start=start_date,
                        end=end_date
                        )
        df = df['Adj Close']
        return df
    else:
        return tickers_check[1]


# Calculate daily and annual returns of the stocks
returns_daily = df.pct_change()
returns_annual = returns_daily.mean() * 252

# Get daily and covariance of returns of the stocks
cov_daily = returns_daily.cov()
cov_annual = cov_daily * 252

# Actual portfolio return, volatility and sharpe
def return_performance(weights, returns_annual):
    weights /= np.sum(weights)
    return_perf = np.dot(weights, returns_annual)
    return return_perf

def volatility_performance(weights, cov_annual):
    weights /= np.sum(weights)
    volatility_perf = np.sqrt(np.dot(np.array(weights).T, np.dot(cov_annual, weights)))
    return volatility_perf


actual_volatility = volatility_performance(weights, cov_annual)
actual_return = return_performance(weights, returns_annual)    
actual_sharpe = actual_return / actual_volatility

df.head()

def optimize_potfolio(tickers:list[str], weights:list[int]):

    # 
    end_date = datetime.today()
    start_date = end_date - timedelta(days=720)
    tickers_list = tickers
    weights_list = weights
    df = getData(tickers, start_date, end_date)
    if type(df) == pd.DataFrame:
        pass

