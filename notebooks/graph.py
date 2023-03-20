import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

#  Plot Efficient Frontier
def plot_efficient_frontier(df:pd.DataFrame, sharpe_portfolio, min_variance_port, min_volatility_for_return, max_return_for_volatility, x_actual, y_actual):
    # plot frontier, max sharpe & min Volatility values with a scatterplot
    ax = sns.scatterplot(data=df, x='Volatility', y='Returns', hue='Sharpe Ratio',
                    cmap='RdYlGn', edgecolors='black', label="shape")
    sns.scatterplot(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='o', s=100, label='Max Ratio')
    sns.scatterplot(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='green', marker='o', s=100, label='Min Volatility')
    sns.scatterplot(x=x_actual, y=y_actual, c='orange', marker='o', s=150, label='Actual Portfolio')
    # sns.lineplot(x=x_tangent, y=y_tangent , linestyle='--')

    sns.scatterplot(x=max_return_for_volatility['Volatility'], y=max_return_for_volatility['Returns'], c='blue', marker='o', s=50, label='Max Return')
    sns.scatterplot(x=min_volatility_for_return['Volatility'], y=min_volatility_for_return['Returns'], c='blue', marker='o', s=50, label='Min Volatility')


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

    # find max Volatility & max Returns values in the dataframe (df) for x_lim and y_lim
    max_volatility = df['Volatility'].max()
    min_volatility = df['Volatility'].min()
    max_return = df['Returns'].max()
    min_return = df['Returns'].min()
    # Set the axis limits
    plt.xlim(min_volatility * 0.7, max_volatility * 1.1)  # add some padding to the left and right
    plt.ylim(min_return * 0.5, max_return * 1.1)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.xlabel('Volatility (Std. Deviation)')
    plt.ylabel('Expected Returns')
    plt.title('Efficient Frontier')
    plt.show()