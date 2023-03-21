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
print('data uploaded')

#-------------------------------------------------------------------
# Split train test (30 days test)
start_date = stock.first_valid_index()
end_date = stock.last_valid_index()
split_date = pd.to_datetime(stock.last_valid_index()) - timedelta(days=30)
train = stock.loc[stock.index < split_date]
test = stock.loc[stock.index >= split_date]
print('split done')

#-------------------------------------------------------------------
# Pacf 
nlags = pacf(stock, nlags=12, alpha=.05) 
relevant_lags = [i for i,v in enumerate(nlags[0]) if v > 0.25]
print('pacf done')

#-------------------------------------------------------------------
# Create features

def create_features(data: pd.DataFrame, relevant_lags: list):
        data = data.copy()
        data['year'] = data.index.year
        data['month'] = data.index.month
        data['week'] = data.index.isocalendar().week.astype("int64")
        # from partial autocorrelation analysis, build relevant lags.
        for i in relevant_lags:
                if i > 0:
                        data[f'lag_{i}'] = data[data.columns[0]].shift(i)
        # remove nan rows due to lags 
        data = data.dropna()
        return(data)

stock = create_features(stock, relevant_lags)
print(stock.dtypes)
print('features created')
#-------------------------------------------------------------------
# Create features on train and test, and selection of target and features

train = create_features(train, relevant_lags)
test = create_features(test, relevant_lags)

FEATURES = stock.columns[1:]
TARGET = stock.columns[0]
print(FEATURES)
# test.dropna()
# train.dropna()

#-------------------------------------------------------------------
# Splitting on X and y for train and test sets.
X_train = train[FEATURES]
y_train = train[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]
print('test train done')

#-------------------------------------------------------------------
# Cross Validation on historical datas

tss = TimeSeriesSplit(n_splits=5, test_size=12, gap=10 )

fold = 0
preds = []
rmse_scores = []
mape_scores = []
for train_idx, val_idx in tss.split(stock):  
        train = stock.iloc[train_idx]
        test = stock.iloc[val_idx]

        train = create_features(train, relevant_lags)
        test = create_features(test, relevant_lags)

        FEATURES = stock.columns[1:]
        TARGET = stock.columns[0]

        X_train = train[FEATURES]
        y_train = train[TARGET]

        X_test = test[FEATURES]
        y_test = test[TARGET]

        reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
                                n_estimators=1000,
                                early_stopping_rounds=50,
                                objective='reg:linear',
                                max_depth=3,
                                learning_rate=0.01,
                                )
        reg.fit(X_train, y_train,
                eval_set=[(X_train, y_train), (X_test, y_test)],
                verbose=100)

        y_pred = reg.predict(X_test)
        preds.append(y_pred)
        rmse_score = np.sqrt(mse(y_test, y_pred))
        mape_score = mape(y_test, y_pred)
        rmse_scores.append(rmse_score)
        mape_scores.append(mape_score)

print(f'Mean RMSE score across folds {np.mean(rmse_scores):0.4f}')
print(f'Fold RMSE scores:{rmse_scores}')
print(f'Mean MAPE score across folds {np.mean(mape_scores):0.4f}')
print(f'Fold MAPE scores:{mape_scores}')
# print(reg.get_params())

#-------------------------------------------------------------------
# Features importance
fi = pd.DataFrame(data=reg.feature_importances_, index=reg.feature_names_in_ , columns=['importance'])
fi.sort_values(by='importance', ascending=True).plot(kind='barh', title='FEATURES Importance')
# plt.show()

#-------------------------------------------------------------------
# Prediction

