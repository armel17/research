# -*- coding: utf-8 -*-

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
sys.path.append(dir_path)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from Indicators import Indicators
from Helpers import Helpers  # same folder module
#Indicators = Indicators()
#Helpers = Helpers()


class StrategySimulator:
    def __init__(self):
        self.helpers = Helpers()

    def test_strategy(self, data=None):
        # DATA
        if data is None:
            stock = pd.read_csv('../Data/bitcoin_histo.csv', sep=';')
            pxlast = stock['PX_LAST']
            dates = stock['Date']
        else:
            dates = pd.Series(data[0].values)
            pxlast = pd.Series(data[1].values)

        # COMPUTATIONS
        macd, macd_ema9 = Indicators.macd(pxlast, long_span=26, short_span=12, smoothing_factor=9)
        returns = pxlast.pct_change(1)
        invested = Helpers.indicators_to_investment(indicator_name='macd', data=(macd, macd_ema9))

        # PROFITABILITY
        total_profit, strat_profit = self.profitability(returns, invested)

        # PLOT
        data_plot = pd.concat([dates, total_profit, strat_profit], axis=1)
        data_plot.columns = ['dates', 'total', 'strat']
        data_plot.plot(x='dates', y=['total', 'strat'])
        # plt.figure()
        # total_profit.plot()
        # strat_profit.plot()

        # Pour voir le graphe s'afficher, mettre un breakpoint devant 'input(...)' et lancer en debug - à fixer
        input('...')


    def profitability(self, returns_mat, invested_mat):
        length_mat = len(returns_mat)
        total_return = pd.Series([0] * length_mat)
        return_strat = pd.Series([0] * length_mat)
        total_return.loc[0] = 100
        return_strat.loc[0] = 100

        for indexing in range(0, length_mat - 1):
            total_return.loc[indexing + 1] = total_return.loc[indexing] * (1 + returns_mat.loc[indexing + 1])
            return_strat.loc[indexing + 1] = return_strat.loc[indexing] * (1 + (invested_mat.loc[indexing]) * returns_mat.loc[indexing + 1])
        return total_return, return_strat


if __name__ == '__main__':
    s = StrategySimulator()
    query = {
        'ccy_pair': 'XETHZEUR',
        'timestamp': {
            '$gt': datetime.today() - timedelta(days=100)
        }
    }
    interval = 1440
    value = 'close'
    data = s.helpers.mongo_to_dict_list(table='ohlc_%s' % str(interval), query=query, output_value=value)
    data_df = s.helpers.tuple_list_to_dframe(data['close'])
    s.test_strategy()#data=data_df)
