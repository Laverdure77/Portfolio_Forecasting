from datetime import datetime
from datetime import timedelta

from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles

import uvicorn

from pydantic import BaseModel

from scripts.scripts import tickers_exist
from scripts.scripts import getData
from scripts.scripts import optimize_potfolio


app = FastAPI()

class Ticker(BaseModel):
    tickers: list[str]
    weights: list[int]

@app.get("/")
async def root():
    return {"message": "Welcome to Portfolio Optimizer!"}

@app.post("/tickers/")
async def create_item(input: Ticker):
    tickers_list = input.tickers
    weights_list = input.weights
    end_date = datetime.today()
    start_date = end_date - timedelta(days=1500)
    
    # Check if tickers in list exist
    check_tickers = tickers_exist(tickers_list)
    
    # Return message if weights sum != 100
    if sum(weights_list) != 100:
        return {"message": "Please check the sum of weights is equal to 100 !"}
    
    # Return message if some tickers do not exist
    if check_tickers[0] == False:
        return {"message": f"Tickers {check_tickers[1]} do no exist !"}
    
    # Get tickers
    df = getData(tickers_list, start_date, end_date)
    
    # Compute optimal portfolio
    optimal = optimize_potfolio(df, tickers_list, weights_list)
    
    # Endpoints to graphs
    graphs = {
            'efficient_frontier': '/graphs/efficient_frontier.png',
            'weights' : '/graphs/optimisation_plot.png'
            }
    
    return optimal, graphs

# Static files
app.mount("/graphs", StaticFiles(directory="fastAPI/graphs"), name="graphs")


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)