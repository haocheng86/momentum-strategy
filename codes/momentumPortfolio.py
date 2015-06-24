#!/usr/bin/python

import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta
import sys

class MomentumPortfolio(object):

    def __init__(self, long_number = 10, short_number = 10, ranking_period = 3, stock_exchange = 'S&P500', today = date.today()):

        # Parameters
        self.long_number = long_number  # Number of stocks to long in the portfolio
        self.short_number = short_number  # Number of stocks to short in the portfolio
        self.ranking_period = ranking_period  # Number of months in ranking period
        self.stock_exchange = stock_exchange  # Stock exchange
        self.today = today  # Date to pick
        self.momentum_long = pd.Series()
        self.momentum_short = pd.Series()

        self.get_data()
        self.pick()

    def pick(self):       
        start = self.today + relativedelta(months = -self.ranking_period)  # fine tunes
        end = self.today + relativedelta(months = -1)
        self.start_month = str(start.year) + '-' + str(start.month)
        self.end_month = str(end.year) + '-' + str(end.month)
        stock_data_ranking = self.monthly_stock_data.loc[self.start_month:self.end_month]
        
        # Average return in the ranking period
        stock_performance = pd.Series()
        for stock in stock_data_ranking:
            if stock_data_ranking[stock].iloc[0] > 0:
                starting_price = stock_data_ranking[stock].iloc[0]
                ending_price = stock_data_ranking[stock].iloc[self.ranking_period - 1]
                stock_return = (ending_price - starting_price) / starting_price
                stock_performance[stock] = stock_return / self.ranking_period
            else: stock_performance[stock] = np.NaN
        stock_performance.sort(ascending = False)
        
        # Portfolio    
        self.momentum_long = stock_performance.head(self.long_number)
        self.momentum_short = stock_performance.dropna(how = 'any').tail(self.short_number)

    def update(self, today = date.today()):
        self.today = today 
        self.pick()

    def get_data(self):  # Get stock data from .csv file.
        dataFile = '../historical_performance_data/stock_data_{}.csv'.format(self.stock_exchange)
        self.stock_data = pd.read_csv(dataFile, parse_dates=[0])
        self.stock_data.index = self.stock_data['Date']
        self.trading_dates = self.stock_data['Date']
        self.stock_data = self.stock_data.drop('Date', 1)
        
        # Delete questionable data from yahoo    
        if self.stock_exchange == 'NYSE':
            del self.stock_data['SMA']  # 2010-10-01 - 2011-10-01
            del self.stock_data['BNA']  # 2011-08-01 - 2012-08-01
            del self.stock_data['BBX']  # 2008-03-01 - 2009-03-01
            del self.stock_data['SSE']  # 2014-04-01 - 2015-04-01
            del self.stock_data['CTC']  # 2009-12-01 - 2010-12-01
        elif self.stock_exchange == 'NASDAQ':
            del self.stock_data['VTNR'] # 2003-04-01 - 2004-04-01
            del self.stock_data['AMBI'] # 2007-03-01 - 2008-03-01
            del self.stock_data['VRML'] # 2008-07-01 - 2009-07-01
            del self.stock_data['VGGL']
            del self.stock_data['CUI']  # 2011-06-01 - 2012-06-01
            del self.stock_data['CAR']  # 2009-03-01 - 2010-03-01
            del self.stock_data['CTIC'] # 2009-03-01 - 2010-03-01
        # Not really problems:
        # YRCW, SCSS

        self.monthly_stock_data = np.round(self.stock_data.resample('M', how='mean').to_period(), 2)

    # Output file
    def to_file(self):
        fileName = '{}_{}_{}_pick'.format(self.stock_exchange, self.today, self.ranking_period)
        f = open('../{}.txt'.format(fileName), 'w')
        sys.stdout = Tee(sys.stdout, f)

    def show(self):
        print 'Long:' 
        print 'Stock   Average monthly return in previous {} months'.format(self.ranking_period)
        print self.momentum_long
        print '\nShort:' 
        print self.momentum_short


# Enable writing to files while displaying in console
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

def main():
    mp = MomentumPortfolio(ranking_period = 3)
    mp.to_file()    # write results to .txt file
    mp.show()


if __name__ == '__main__':
	main()