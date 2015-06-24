#!/usr/bin/python

import pandas.io.data as web
import pandas as pd
import numpy as np
from datetime import date

action = 'update' # update or new
exchange = 'S&P500'

stock_list = pd.read_csv('../historical_performance_data/companylist_{}.csv'.format(exchange)).iloc[:,0]
data_start = date(2015,5,23)
data_end = date.today()
spy = web.DataReader('SPY','yahoo',data_start,data_end)['Adj Close']
data_date_range = spy.index
stock_data_index = {}
stock_data = pd.DataFrame(index = data_date_range)
monthly_stock_data = pd.DataFrame()

index = 0
f = pd.Series()
for stock in stock_list:
    try:
        f = web.DataReader(stock,'yahoo',data_start,data_end)['Adj Close']
    except:
        continue
    print stock + ' data extracted'
    stock_data_index[stock] = index
    stock_data[stock]=f
    index += 1

if action == 'update' :
    with open('../historical_performance_data/stock_data_' + exchange + '.csv', 'a') as f:
        stock_data.to_csv(f, header=False)
elif action == 'new' :
    monthly_stock_data = np.round(stock_data.resample('M', how='mean').to_period(),2)
    stock_data.to_csv('../historical_performance_data/stock_data_' + exchange + '.csv')
    monthly_stock_data.to_csv('../historical_performance_data/monthly_stock_data_' + exchange + '.csv')