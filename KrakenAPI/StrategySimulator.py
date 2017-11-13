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
            pxlast_csv_str = stock['PX_LAST']
            pxlast = pd.to_numeric(pxlast_csv_str)
            dates_csv_str = stock['Date']
            dates = pd.to_datetime(dates_csv_str, dayfirst=True)
        else:
            dates = pd.Series(data[0].values)
            pxlast = pd.Series(data[1].values)

        # COMPUTATIONS
        macd, macd_ema9 = Indicators.macd(pxlast, long_span=26, short_span=12, smoothing_factor=9)
        returns = pxlast.pct_change(1)
        invested = Helpers.indicators_to_investment(indicator_name='macd', data=(macd, macd_ema9))

        # ema_difference = Indicators.ema_diff(pxlast, long_span=26, short_span=12)
        # returns = pxlast.pct_change(1)
        # invested = Helpers.indicators_to_investment(indicator_name='ema_diff', data=(ema_difference))

        # PROFITABILITY
        total_profit, strat_profit = self.profitability(returns, invested)

        # PLOT
        data_plot = pd.concat([dates, total_profit, strat_profit], axis=1)
        data_plot.columns = ['dates', 'total', 'strat']
        data_plot.plot(x='dates', y=['total', 'strat'])

        # data_plot_1 = pd.concat([dates, pxlast], axis=1)
        # data_plot_1.columns = ['dates', 'MongoData']
        #
        #
        #
        # data_plot_2 = pd.concat([dates_csv, pxlast_csv], axis=1)
        # data_plot_2.columns = ['dates', 'CSV']
        #
        # plt.plot(data_plot_1['dates'], data_plot_1['MongoData'])
        # plt.plot(data_plot_2['dates'], data_plot_2['CSV'])
        #
        # plt.show()

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
    ccy_pairs = ['XETHZEUR', 'XXBTZEUR', 'XETCZEUR']
    since_date = datetime.strptime('01-01-2017', '%d-%m-%Y')
    interval = 60
    value_type = 'close'
    data_df = s.helpers.mongo_to_df(ccy_pairs=ccy_pairs, since_date=since_date, interval=interval,
                                    value_type=value_type)
    data_df.plot()
    plt.show(block=True)

    # query = {
    #     'ccy_pair': 'XETHZEUR',
    #     'timestamp': {
    #         '$gt': datetime.today() - timedelta(days=365)
    #     }
    # }
    # value = 'close'
    # data = s.helpers.mongo_to_dict_list(table='ohlc_%s' % str(interval), query=query, output_value=value)
    # data_df = s.helpers.tuple_list_to_dframe(data['close'])
    # s.test_strategy(data=data_df)
