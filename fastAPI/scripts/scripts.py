import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import yfinance as yf

from datetime import datetime
from datetime import timedelta

#-----------------------------------------------------------------------
# Check if tickers exist
def tickers_exist(tickers:list[str]) -> list[bool,list[str]]:
    tickers_list = tickers
    error_list = []
    for t in tickers_list:
        ticker = yf.Ticker(t)
        info = None
        try:
            info = ticker.history(
                                period='7d',
                                interval='1d'
                                )
        except:
            print(f"Cannot get info of {t}, it probably does not exist")
            error_list.append(t)
            continue
        # Got the info of the ticker
        print(f"{t} exist")
    if len(error_list) == 0:
        return [True, error_list]
    else:
        return [False, error_list]
    
#-----------------------------------------------------------------------
# Import data
def getData(tickers:list, start_date:datetime, end_date:datetime) -> pd.DataFrame:
    df = yf.download(tickers,
                    start=start_date,
                    end=end_date
                    )
    df = df['Adj Close']
    return df

#-----------------------------------------------------------------------
# return and volatility
def return_performance(weights, returns_annual):
    weights /= np.sum(weights)
    return_perf = np.dot(weights, returns_annual)
    return return_perf

def volatility_performance(weights, cov_annual):
    weights /= np.sum(weights)
    volatility_perf = np.sqrt(np.dot(np.array(weights).T, np.dot(cov_annual, weights)))
    return volatility_perf

#-----------------------------------------------------------------------
#  Optimize Portfolio
def optimize_potfolio(df: pd.DataFrame, tickers_list:list[str], weights_list:list[int]):
    # Calculate daily and annual returns of the stocks
    returns_daily = df.pct_change()
    returns_annual = returns_daily.mean() * 252
    # Get daily and covariance of returns of the stocks
    cov_daily = returns_daily.cov()
    cov_annual = cov_daily * 252
    # Actual portfolio return, volatility and sharpe
    actual_volatility = volatility_performance(weights_list, cov_annual)
    actual_return = return_performance(weights_list, returns_annual)    
    actual_sharpe = actual_return / actual_volatility
    # a dictionary for Returns and Risk values of each portfolio
    actual_portfolio = {'Returns': actual_return,
                        'Volatility': actual_volatility,
                        'Sharpe Ratio': actual_sharpe
                        }
    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter,symbol in enumerate(tickers_list):
        actual_portfolio[symbol+' weight'] = weights_list[counter]
    # make a nice dataframe of the extended dictionary
    actual_portfolio_df = pd.DataFrame.from_dict(actual_portfolio, orient='index').T
    # empty lists to store returns, volatility and weights of imiginary portfolios
    port_returns = []
    port_volatility = []
    stock_weights = []
    sharpe_ratio = []
    # set the number of combinations for imaginary portfolios
    num_assets = len(tickers_list)
    num_portfolios = 60000
    #set random seed for reproduction's sake
    np.random.seed(101)
    # populate the empty lists with each portfolios returns,risk and weights
    for single_portfolio in range(num_portfolios):
        # generate random weights and normalize.
        weights_list = np.random.random(num_assets)
        weights_list /= np.sum(weights_list)
        # portfolio performance
        returns = return_performance(weights_list, returns_annual)  
        volatility = volatility_performance(weights_list, cov_annual)
        sharpe = returns / volatility
        # append result to dedicated list
        sharpe_ratio.append(sharpe)
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights_list)

    # a dictionary for Returns and Risk values of each portfolio
    portfolio = {'Returns': port_returns,
                'Volatility': port_volatility,
                'Sharpe Ratio': sharpe_ratio}
    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter,symbol in enumerate(tickers_list):
        portfolio[symbol+' weight'] = [weight[counter] for weight in stock_weights]
    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)
    # get better labels for desired arrangement of columns
    column_order = ['Returns', 'Volatility','Sharpe Ratio'] + [stock+' weight' for stock in tickers_list]
    # reorder dataframe columns
    df = df[column_order]

    # find min Volatility & max sharpe values in the dataframe (df)
    min_volatility = df['Volatility'].min()
    max_sharpe = df['Sharpe Ratio'].max()
    # find max Volatility & max Returns values in the dataframe (df) for x_lim and y_lim
    max_volatility = df['Volatility'].max()
    max_return = df['Returns'].max()
    min_return = df['Returns'].min()
    # use the min, max values to locate and create the two special portfolios
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_volatility]
    # Plot tangent, best ratio Return(mean)/Volatility(std dev)
    tangent = df.loc[(df['Returns']/df['Volatility']).idxmax()]
    x_tangent = [0,tangent['Volatility'],1]
    y_tangent = [0,tangent['Returns'],tangent['Returns']/tangent['Volatility']]
    # Actual portfolio Return and Volatility
    x_actual = [actual_volatility]
    y_actual = [actual_return]
    # Find optimal return portfolio for actual Volatility and Return
    closest_volatility = df.iloc[(df['Volatility']-(actual_volatility)).abs().argsort()[:10]]
    max_return_for_volatility = closest_volatility[closest_volatility['Returns']==closest_volatility['Returns'].max()]
    closest_return = df.iloc[(df['Returns']-actual_return).abs().argsort()[:10]]
    min_volatility_for_return = closest_return[closest_return['Volatility']==closest_return['Volatility'].min()]

    # plot frontier, max sharpe & min Volatility values with a scatterplot
    fig, ax = plt.subplots(figsize=(6, 4))
    ax = sns.scatterplot(
                    data=df, x='Volatility', y='Returns',
                    hue='Sharpe Ratio',
                    cmap='RdYlGn', 
                    edgecolors='black', 
                    label="shape"
                    )
    
    sns.scatterplot(
                    x=sharpe_portfolio['Volatility'], 
                    y=sharpe_portfolio['Returns'], 
                    c='red',
                    marker='o', 
                    s=100, 
                    label='Max Ratio'
                    )
    
    sns.scatterplot(
                    x=min_variance_port['Volatility'],
                    y=min_variance_port['Returns'], 
                    c='green', 
                    marker='o', 
                    s=100, 
                    label='Min Volatility'
                    )
    
    sns.scatterplot(
                    x=x_actual, 
                    y=y_actual, 
                    c='orange', 
                    marker='o', 
                    s=150, 
                    label='Actual Portfolio'
                    )
    
    sns.lineplot(
                x=x_tangent, 
                y=y_tangent, 
                linestyle='--'
                )

    sns.scatterplot(
                    x=max_return_for_volatility['Volatility'], 
                    y=max_return_for_volatility['Returns'], 
                    c='blue', 
                    marker='o', 
                    s=50, 
                    label='Max Return'
                    )
    
    sns.scatterplot(
                    x=min_volatility_for_return['Volatility'],
                    y=min_volatility_for_return['Returns'], 
                    c='blue', 
                    marker='o', 
                    s=50, 
                    label='Min Volatility'
                    )

    plt.annotate("", 
                xy=(max_return_for_volatility['Volatility'], max_return_for_volatility['Returns']),
                xytext=(x_actual[0], y_actual[0]),
                arrowprops=dict(arrowstyle="simple", color="white")
                )
    plt.annotate("", 
                xy=(min_volatility_for_return['Volatility'],min_volatility_for_return['Returns']),
                xytext=(x_actual[0], y_actual[0]),
                arrowprops=dict(arrowstyle="simple", color="white")
                )

    # Set the axis limits
    plt.xlim(min_volatility * 0.7, max_volatility * 1.1)  # add some padding to the left and right
    plt.ylim(min_return * 0.5, max_return * 1.1)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.xlabel('Volatility (Std. Deviation)')
    plt.ylabel('Expected Returns')
    plt.title('Efficient Frontier')

    efficient_frontier_plot = './graphs/efficient_frontier.png'
    with open(efficient_frontier_plot, mode='w') as f:
        plt.savefig(efficient_frontier_plot, dpi='figure', format='png', metadata=None,
            bbox_inches='tight', pad_inches=0.1,
            facecolor='auto', edgecolor='auto',
            backend=None
        )
    plt.close()

    # plot weights for each portfolio
    def plot_weights ():
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1,figsize=(len(tickers_list)*1.5, 12))
        fig.tight_layout(pad=2.5)
        plt.axis('equal')

        sns.barplot(actual_portfolio_df.iloc[:,-len(tickers_list):], color='orange', ax=ax1)
        sns.barplot(min_variance_port.iloc[:,-len(tickers_list):], color='green', ax=ax2)
        sns.barplot(sharpe_portfolio.iloc[:,-len(tickers_list):], color='red',ax=ax3)
        sns.barplot(min_volatility_for_return.iloc[:,-len(tickers_list):], color='blue', ax=ax4)
        sns.barplot(max_return_for_volatility.iloc[:,-len(tickers_list):], color='blue', ax=ax5)

        ax1.set_title('Actual portfolio')
        ax2.set_title('Min Risk portfolio')
        ax3.set_title('Max Return portfolio')
        ax4.set_title('Min Risk for actual Return')
        ax5.set_title('Max Return for actual Risk')

        ax1.set_ylim(0,100)
        ax2.set_ylim(0,1)
        ax3.set_ylim(0,1)
        ax4.set_ylim(0,1)
        ax5.set_ylim(0,1)

        optimisation_plot = './graphs/optimisation_plot.png'
        with open(optimisation_plot, mode='w') as f:
            plt.savefig(optimisation_plot, dpi='figure', format='png', metadata=None,
                bbox_inches='tight', pad_inches=0.1,
                facecolor='auto', edgecolor='auto',
                backend=None
            )
        plt.close()
    
    plot_weights()

    return { 
            'min_variance_portfolio': min_variance_port.to_dict('records'),
            'sharpe_portfolio': sharpe_portfolio.to_dict('records'),
            'Max_Return_for_actual_volatility' : {
                                                'actual_volatility': max_return_for_volatility['Volatility'].values[0],
                                                'weights': max_return_for_volatility.iloc[:,-len(tickers_list):].to_dict('records')
                                                },
            'Min Volability for actual Return' : {
                                                'actual_return': min_volatility_for_return['Returns'].values[0],
                                                'weights': min_volatility_for_return.iloc[:,-len(tickers_list):].to_dict('records')
                                                }
            }