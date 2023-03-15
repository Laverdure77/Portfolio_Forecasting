import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_percentage_error as mape
from sklearn.model_selection import TimeSeriesSplit
from datetime import datetime
from datetime import timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from pmdarima.arima import auto_arima
from pmdarima.arima import ADFTest
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
  
plt.style.use('fivethirtyeight')


#-------------------------------------------------------------------
# Import datas
filename = './datas/apple.csv'
stock = pd.read_csv(filename)
stock.index = pd.to_datetime(stock.index)
stock = stock.asfreq(freq='D')
stock = stock.fillna(method='bfill')

#-------------------------------------------------------------------
# Split train test (30 days test)
start_date = stock.first_valid_index()
end_date = stock.last_valid_index()
split_date = pd.to_datetime(stock.last_valid_index()) - timedelta(days=30)
train = stock.loc[stock.index < split_date]
test = stock.loc[stock.index >= split_date]

#-------------------------------------------------------------------
# Pacf 
nlags = pacf(stock, nlags=12, alpha=.05) 
relevant_lags = [i for i,v in enumerate(nlags[0]) if v > 0.25]

#-------------------------------------------------------------------
# Create features

def create_features(data: pd.DataFrame, relevant_lags: list):
    data = data.copy()
    data['year'] = data.index.year
    data['month'] = data.index.month
    # from partial autocorrelation analysis, build relevant lags.
    for i in relevant_lags:
        if i > 0:
            data[f'lag_{i}'] = data[data.columns[0]].shift(i)
    # remove nan rows due to lags 
    data = data.dropna()
    return(data)


stock = create_features(stock, relevant_lags)
#-------------------------------------------------------------------
# Create features
print(stock.head())