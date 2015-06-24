import pandas as pd
import math

def stats(portfolio_return, SPY):
    mean_return = portfolio_return.mean()
    std = portfolio_return.std()
    sharp_ratio = mean_return/std
    SPY_mean = SPY.mean()
    SPY_var = SPY.var()
    SPY_std = SPY.std()
    cov_SPY = portfolio_return.cov(SPY)
    corr = cov_SPY / (std * SPY_std)
    beta = cov_SPY / SPY_var
    alpha = mean_return - beta * SPY_mean

    # Print    
    print 'Annulized Mean Return:'
    print 12 * mean_return
    print
    print 'Volatility:'
    print math.sqrt(12) * std
    print 
    print 'Sharpe Ratio:'
    print math.sqrt(12) * sharp_ratio
    print
    print 'S&P 500 annulized return:'
    print 12 * SPY_mean
    print 
    print 'Market volatility:'
    print math.sqrt(12) * SPY_std
    print
    print 'Correlation with S&P 500:'
    print corr
    print
    print 'Alpha and beta with respect to S&P 500:'
    print 'alpha =', 12 * alpha, '; beta =', beta

