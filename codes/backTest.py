
from momentumPortfolio import MomentumPortfolio as MP
from stats import stats as stats
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import math
import sys

class BackTest(MP):

    def __init__(self, backtest_start = None, backtest_end = None, long_number = 5, short_number = 5, ranking_period = 6, stock_exchange = 'S&P500', holding_period = 1):
        MP.__init__(self, long_number, short_number, ranking_period, stock_exchange, date.today())
        self.holding_period = holding_period
        self.backtest_end = backtest_end if backtest_end != None else date.today() + relativedelta(months = -holding_period)
        self.backtest_start = backtest_start if backtest_start != None else self.backtest_end + relativedelta(months = -12)
        self.backtest_return = pd.DataFrame(columns=['Long', 'Short', 'Average', 'SPY'])

        self.get_first_trading_dates_of_month()

    # run this method to get backtest result
    def backtest(self, *args):
        self.to_file()      # write results to .txt file
        if len(args) == 0:
            rdelta = relativedelta(self.backtest_end, self.backtest_start)
            months = rdelta.years * 12 + rdelta.months

            for i in range(months + 1):
                self.today = self.backtest_start + relativedelta(months = i)
                print '{}-{m:02d}'.format(self.today.year, m = self.today.month)
                self.update(self.today)
                print '\nMonmentum portfolio and their past performance:'
                print 'Long:' 
                print self.momentum_long
                print '\nShort:' 
                print self.momentum_short
                self.get_return()
            self.backtest_return = self.backtest_return[['Long', 'Short', 'Average', 'SPY']]
            print self.backtest_return, '\n'
            self.to_csv()
            stats(self.backtest_return['Long'], self.backtest_return['SPY'])
        else:
            self.backtest_start = args[0]
            self.backtest_end = args[1]
            self.backtest()

    def get_return(self):
        today = self.today
        future = today + relativedelta(months = self.holding_period)
        buy_date = self.month_beginnings['{}-{}'.format(today.year, today.month)]
        sell_date = self.month_beginnings['{}-{}'.format(future.year, future.month)]

        long_returns = pd.Series()
        for stock in self.momentum_long.index:
            start_price = self.stock_data.loc[buy_date, stock]
            end_price = self.stock_data.loc[sell_date, stock]
            stock_return = (end_price - start_price) / start_price
            long_returns[stock] = stock_return / self.holding_period if not math.isnan(stock_return) else -1 / float(self.holding_period)
        long_average = long_returns.mean()
        long_returns['Average'] = long_average

        short_returns = pd.Series()
        for stock in self.momentum_short.index:
            start_price = self.stock_data.loc[buy_date, stock]
            end_price = self.stock_data.loc[sell_date, stock]
            stock_return = (start_price - end_price) / start_price
            short_returns[stock] = stock_return / self.holding_period if not math.isnan(stock_return) else -1 / float(self.holding_period)
        short_average = short_returns.mean()
        short_returns['Average'] = short_average

        SPY_start_price = self.stock_data.loc[buy_date, 'SPY']
        SPY_end_price = self.stock_data.loc[sell_date, 'SPY']
        SPY_return = (SPY_end_price - SPY_start_price) / (self.holding_period *SPY_start_price)

        average = (long_average + short_average) / 2
        self.backtest_return = self.backtest_return.append(pd.DataFrame({'Long': long_average, 'Short': short_average, 'Average': average, 'SPY':SPY_return}, index = ['{}-{m:02d}'.format(self.today.year, m = self.today.month)]))

        print '\nPortfolio Returns:'
        print 'Long:'
        print long_returns
        print '\nShort:' 
        print short_returns
        print


    def get_first_trading_dates_of_month(self):
    # Get first trading date of each month
        self.month_beginnings = pd.Series()
        trading_dates = self.trading_dates
        prev_month = 0
        for dates in trading_dates:
            if dates.month == prev_month:
                continue
            else:
                self.month_beginnings = self.month_beginnings.append(pd.Series(dates, index = ['{}-{}'.format(dates.year, dates.month)]))
                prev_month = dates.month

    def to_csv(self):
        start = self.backtest_start
        end = self.backtest_end
        fileName = '{}_{}.{}-{}.{}_{}_{}_{}_returns'.format(self.stock_exchange, start.year, start.month, end.year, end.month, self.long_number, self.ranking_period, self.holding_period)
        self.backtest_return.to_csv('../{}.csv'.format(fileName))

    def to_file(self):
        start = self.backtest_start
        end = self.backtest_end
        fileName = '{}_{}.{}-{}.{}_{}_{}_{}'.format(self.stock_exchange, start.year, start.month, end.year, end.month, self.long_number, self.ranking_period, self.holding_period)
        f = open('../{}.txt'.format(fileName), 'w')
        sys.stdout = Tee(sys.stdout, f)

# Enable writing to files while displaying in console
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

def main():
    test = BackTest()
    test.backtest(date(2001, 1, 1), date(2015, 5, 1))
if __name__ == '__main__':
    main()
