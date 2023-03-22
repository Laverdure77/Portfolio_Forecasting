# Portfolio Optimizer API

## Description  

Using historical datas from yahoo finance,
this API allows users to optimize a portfolio based on Efficient Frontier optimisation.  
The user enters a list of tickers and corresponding weigths in the portfolio, the API returns four different portfolio optimisation based on return versus risk ratio.  
The API is built on the FastAPI framework and deployed, using Docker, on render.com.

<br/>
<p align="center">
    <img src="./datas/efficient_frontier.png"
         alt="Efficient Frontier graph">
</p>

<p align="center">
  <a href="#Efficient-frontier">Efficient frontier</a> •
  <a href="#How-Does-It-Work">How Does It Work</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#API-Endpoints">API Endpoints</a> •
  <a href="#Parameters">Parameters</a> •
  <a href="#Graphs">Graphs</a> •
  <a href="#Dependencies ">Dependencies </a>
</p>

## Efficient frontier

Efficient frontier optimization (Monte Carlo simulation) is a method used in finance to find the optimal portfolio of assets that provides the highest expected return for a given level of risk or the lowest risk for a given level of expected return.  
It involves calculating the expected returns and covariance matrix of a set of assets, and then finding the set of portfolios that lie on the efficient frontier, which represents the best possible trade-off between expected return and risk.  
This optimization method can be used to construct portfolios that are well-diversified and optimized for a specific level of risk tolerance or investment objective.
 
## How Does It Work  

Based on 4 years of historicl datas, the python script calculate the annual means (returns) and covariance of returns (volality) of the stocks.   
Then it generates 60000 portfolios by randomly assigning weights to each stock.  
For each portfolio, it calculates the returns, volatility, and Sharpe ratio.  
Sharpe ratio is the ratio between the return to volatility.  
Finally, it returns the best porfolio for:
- minimum risk
- best SHAPE ratio
- best return for actual risk
- minimum risk for actual return

## How To Use
The API is deployed on render.com, on <a href="https://portfolio-optimizer.onrender.com/">https://portfolio-optimizer.onrender.com/</a> 
  > **Note**
  > Check the status of the API on Render.com by visiting the API's homepage or status page.  
If the API is currently offline or unavailable, wait for it to wake up.
This may take a few minutes or more, depending on the reason for the outage.
Once the API is awake and running, you can start making requests to it as usual.
The API response could take up to 2 minutes due to restricted cpu usage on the server.

## API Endpoints  
### Root  
Endpoint to check if the API is running.  
Request:

```sql
GET /
```

Response:

```json
{
  "message": "Welcome to Portfolio Optimizer!"
}
```
### Docs
Endpoint to access the interactive documentation.  
<a href="https://portfolio-optimizer.onrender.com/docs">https://portfolio-optimizer.onrender.com/docs</a> 
Request:

```sql
GET /docs
```

<p align="center">
<img src=".\datas\fast_api.png" alt="efficient frontier" align="center" heigth=200px width=auto> 
</p>

#### Tickers 

Endpoint to optimize a portfolio of tickers.

Request:

```sql
POST /tickers/
```

#### Parameters

The POST request body is a JSON format with two keys:  

tickers: a list of strings containing the tickers of the assets in the portfolio.  
weights: a list of integers containing the weights of the assets in the portfolio.  

You can test it on the post tab of the api documentation, or using an api client like thunderclient or postman.

<p align="center" width=200px>
<img src=".\datas\query_render.png" alt="Query_render" align="center"> 

</p>
<p align="center">
<img src=".\datas\thunderclient.png" alt="Query_thunderclient" align="center"> 
</p>

Response:

If successful, the endpoint returns a JSON object containing the optimized portfolio and URLs to two graphs.




If there is an error, the endpoint returns a JSON object with an error message:

- Please remove similar tickers!  
- Please check the sum of weights is equal to 100!  
- Tickers [ticker1, ticker2] do not exist!  
- Not enough historical data for those tickers: [ticker1], please remove them from the tickers list.  

#### Graphs

Endpoint to access static graph files.

Request:

```sql
GET /graphs/efficient_frontier.png
GET /graphs/optimisation_plot.png
```

Response:

A static image file.
<table border="0">
 <tr>
    <td><p style="font-size:1em" align="center">Efficient frontier</b></td>
    <td><img src=".\datas\efficient_frontier.png" alt="efficient frontier" align="center"></td>
 </tr>
 <tr>
    <td><p style="font-size:1em" align="center">Portfolio optimisation</b></td>
    <td><img src=".\datas\optimisation_plot.png" alt="graph from clustering model" align="center"></td>
 </tr>
</table>

The efficient frontier graph shows:  

- the position of the actual portfolio in orange,  
- the best return portfolio in red,  
- the minimum risk portfolio in green,  
- the portfolio optimizing the return for the actual risk, in blue (verticla arrow),  
- the porfolio reducing the risk for the actual return, in blue (horizontal arrow).  

The portfolio optimisation graph shows the weights for each portfolio.  

### Time line

9 working days to discover Time Series, portfolio optimisation, build the app and deployment.
### Possible Improvements

- Improve the script to optimize the best return for actual risk and minimum risk for actual return portfolio:
  in some cases, those optimized portfolio ( blue points on graphs) are not relevant.  
  They are choosen amongst the random portfolio created, and the script doesn't find any better porfolio , especially when actual portoflio lies already near the efficient frontier.
- Build a user fiendly interface
### Dependencies  

- Python 3.11  
- FastAPI  
- NumPy  
- Pandas  
- Matplotlib
- Seaborn

---

> GitHub  [Meulemans Philippe](https://github.com/Laverdure77) &nbsp;&middot;&nbsp;
> LinkedIn  [Meulemans Philippe](https://www.linkedin.com/in/meulemans-philippe/) &nbsp;&middot;&nbsp;
