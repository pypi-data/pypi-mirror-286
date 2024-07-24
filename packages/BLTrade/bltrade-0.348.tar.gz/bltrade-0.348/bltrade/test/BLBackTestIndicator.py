# BLBackTest framework
# author:jiawenze
# date: 2024/06/27

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])


# Import the backtrader platform
import backtrader as bt
import yfinance as yf



class BLBigFishSignal(bt.Indicator):
    lines = ('signal',)
    params = (('p1', 5), ('p2', 30),)

    def __init__(self):
        sma1 = bt.indicators.SMA(period=self.p.p1)
        sma2 = bt.indicators.SMA(period=self.p.p2)
        self.lines.signal = sma1 - sma2
        print(f"sma1={sma1}")
        print(f"sma2={sma2}")
        print(self.lines.signal)


    def next(self):
        #print("lines:处理了%d个数据, 总共有%d个数据" % (len(self.lines),self.lines.buflen()))
        #print("data:已经处理了%d个数据, 总共有%d个数据" % (len(self.data),self.data.buflen()))
        print(self.data.close)
        




if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    #cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../datas/orcl-1995-2014.txt')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,  
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values before this date
    todate=datetime.datetime(2000, 12, 31),
    # Do not pass values after this date
    reverse=False)
    
    #data = bt.feeds.PandasData(dataname=yf.download('AAPL', '2000-07-06', '2020-07-07', auto_adjust=True))

    #data = bt.feeds.PandasData(dataname=yf.download('AAPL', '2018-07-01', '2021-07-30', auto_adjust=False))
    
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    cerebro.add_signal(bt.SIGNAL_LONG,
                           BLBigFishSignal,
                           p1=10,
                           p2=2)

    # Set our desired cash start
    cerebro.broker.setcash(1000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
