import pandas as pd
import numpy as np

def random_portfolios(tickers: list[str], returns_annual, cov_annual) -> pd.DataFrame:

    # empty lists to store returns, volatility and weights of imiginary portfolios
    port_returns = []
    port_volatility = []
    stock_weights = []
    sharpe_ratio = []
    # set the number of combinations for imaginary portfolios
    num_assets = len(tickers)
    num_portfolios = 60000
    #set random seed for reproduction's sake
    np.random.seed(101)
    # populate the empty lists with each portfolios returns,risk and weights
    for single_portfolio in range(num_portfolios):
        # generate random weights and normalize.
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        returns = np.dot(weights, returns_annual)
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
        sharpe = returns / volatility
        # append results to list
        sharpe_ratio.append(sharpe)
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)
    # a dictionary for Returns and Risk values of each portfolio
    portfolio = {'Returns': port_returns,
                'Volatility': port_volatility,
                'Sharpe Ratio': sharpe_ratio}
    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter,symbol in enumerate(tickers):
        portfolio[symbol+' weight'] = [weight[counter] for weight in stock_weights]
    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)
    # get better labels for desired arrangement of columns
    column_order = ['Returns', 'Volatility','Sharpe Ratio'] + [stock+' weight' for stock in tickers]
    # reorder dataframe columns
    df = df[column_order]

    return df



def performance_random_portfolio(df: pd.DataFrame, actual_volatility, actual_return):

    # find min Volatility & max sharpe values in the dataframe (df)
    min_volatility = df['Volatility'].min()
    max_sharpe = df['Sharpe Ratio'].max()
    

    # use the min, max values to locate and create the two special portfolios
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_volatility]

    # Find optimal return portfolio for actual Volatility and Return

    closest_volatility = df.iloc[(df['Volatility']-(actual_volatility)).abs().argsort()[:10]]
    max_return_for_volatility = closest_volatility[closest_volatility['Returns']==closest_volatility['Returns'].max()]

    closest_return = df.iloc[(df['Returns']-actual_return).abs().argsort()[:10]]
    min_volatility_for_return = closest_return[closest_return['Volatility']==closest_return['Volatility'].min()]

    

    # # Plot tangent, best ratio Return(mean)/Volatility(std dev)
    # tangent = df.loc[(df['Returns']/df['Volatility']).idxmax()]
    # x_tangent = [0,tangent['Volatility'],1]
    # y_tangent = [0,tangent['Returns'],tangent['Returns']/tangent['Volatility']]

    return sharpe_portfolio, min_variance_port, min_volatility_for_return, max_return_for_volatility