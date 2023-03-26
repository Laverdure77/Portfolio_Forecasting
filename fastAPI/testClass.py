from datetime import datetime
from datetime import timedelta

# from fastAPI.helpers import portfolio as pf
from helpers.portfolio import Portfolio


end_date = datetime.today()
start_date = end_date - timedelta(days=1500)
tickers = ["AAL","BABA","META","AAPL"]
weights = [20, 30, 30, 20]

pf = Portfolio(tickers, weights)
pf.tickers_exist()

if pf.exist :
    pf.getData(start_date, end_date)
    # print(pf.excluded)
    opt = pf.optimize()

print(opt['Max_Return_for_actual_volatility'])
# df, excluded_tickers = pf.getData(start_date, end_date)
# print(df.head())
# print(pf.tickers)