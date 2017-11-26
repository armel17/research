# -*- coding: utf-8 -*-

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
sys.path.append(dir_path)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pprint as pp
from Indicators import Indicators
from Helpers import Helpers  # same folder module
#Indicators = Indicators()
#Helpers = Helpers()


class StrategySimulator:
    def __init__(self):
        self.helpers = Helpers()

    def test_strategy(self, indicator, params=None, data=None):
        # DATA
        if data is None:
            stock = pd.read_csv('../Data/bitcoin_histo.csv', sep=';')
            pxlast_csv_str = stock['PX_LAST']
            pxlast = pd.to_numeric(pxlast_csv_str)
            dates_csv_str = stock['Date']
            dates = pd.to_datetime(dates_csv_str, dayfirst=True)
        else:
            # dates = pd.Series(data[0].values)
            pxlast = data  # pd.Series(data[1].values)

        # COMPUTATIONS

        if indicator == 'macd':
            ss = params[0]
            ls = params[1]
            sf = params[2]
            macd, macd_ema9 = Indicators.macd(pxlast, short_span=ss, long_span=ls, smoothing_factor=sf)
            returns = pxlast.pct_change(1)
            invested = Helpers.indicators_to_investment(indicator_name='macd', data=(macd, macd_ema9))
        elif indicator == 'ema':
            ema_difference = Indicators.ema_diff(pxlast, long_span=26, short_span=12)
            returns = pxlast.pct_change(1)
            invested = Helpers.indicators_to_investment(indicator_name='ema_diff', data=ema_difference)
        elif indicator == 'macd_rsi':
            macd, macd_ema9 = Indicators.macd(pxlast, long_span=26, short_span=12, smoothing_factor=9)
            rsi = Indicators.RSI(pxlast, period=14)
            invested = Helpers.indicators_to_investment(indicator_name='macd_rsi', data=(macd, macd_ema9, rsi))

        # PROFITABILITY
        total_profit, strat_profit = self.profitability(returns, invested)

        # return strat_profit.iloc[-1].values[0]

        # PLOT
        data_plot = pd.concat([total_profit, strat_profit], axis=1)
        data_plot.plot()
        plt.show()

        # data_plot = pd.concat([dates, total_profit, strat_profit], axis=1)
        # data_plot.columns = ['dates', 'total', 'strat']
        # data_plot.plot(x='dates', y=['total', 'strat'])

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


    def profitability(self, returns_mat, invested_mat):
        # Check returns matrix has no NaN - if so - replace by 0
        returns_mat.fillna(0, inplace=True)
        length_mat = len(returns_mat)
        total_return = pd.DataFrame().reindex_like(returns_mat)
        return_strat = pd.DataFrame().reindex_like(returns_mat)
        total_return.iloc[0] = 100
        return_strat.iloc[0] = 100

        for i in range(0, length_mat - 1):
            total_return.iloc[i + 1] = total_return.iloc[i] * (1 + returns_mat.iloc[i + 1])
            return_strat.iloc[i + 1] = return_strat.iloc[i] * (1 + (invested_mat.iloc[i]) * returns_mat.iloc[i + 1])
        return total_return, return_strat


if __name__ == '__main__':
    s = StrategySimulator()
    ccy_pairs = [
        'XXBTZEUR',
        # 'XXBTZUSD',
        'XETHZEUR',
        # 'XETHZUSD',
        'XETCZEUR',
        # 'XETCZUSD',
        'XXRPZEUR',
        # 'XXRPZUSD',
    ]
    since_date = datetime.strptime('25-06-2017', '%d-%m-%Y')
    interval = 1440
    value_type = 'close'
    data_df = s.helpers.mongo_to_df(ccy_pairs=ccy_pairs, since_date=since_date, interval=interval,
                                    value_type=value_type)

    # CORRELATION
    data_df_returns = data_df.pct_change(1)
    correl_matrix = data_df_returns.corr()
    pp.pprint(correl_matrix)

    data_df_returns = data_df_returns.dropna().reset_index()
    del data_df_returns['index']
    ref = 'XXBTZEUR'
    data_ref_returns = data_df_returns[ref]
    ref_name = ref + ' - ref'
    data_ref_returns.name = ref_name

    # pd.concat([data_ref_returns, data_df_returns], ignore_index=True, axis=1)
    auto_correl_results = pd.DataFrame()
    all_data = pd.concat([data_ref_returns, data_df_returns], axis=1)
    for lag in range(0, 100, 1):
        if lag > 0:
            all_data[ref_name] = all_data[ref_name].shift(1)
        auto_correl_results = pd.concat([auto_correl_results, all_data.corr()[ref_name]], axis=1)

    auto_correl_results = auto_correl_results.transpose().reset_index()
    del auto_correl_results['index']
    auto_correl_results.plot()
    plt.show(block=True)

    # data_df.plot()
    # plt.show(block=True)

    # query = {
    #     'ccy_pair': 'XETHZEUR',
    #     'timestamp': {
    #         '$gt': datetime.today() - timedelta(days=365)
    #     }
    # }
    # value = 'close'
    # data = s.helpers.mongo_to_dict_list(table='ohlc_%s' % str(interval), query=query, output_value=value)
    # data_df = s.helpers.tuple_list_to_dframe(data['close'])




    # OPTIMIZATION TEST
    # i = 3
    # j = 10
    # k = 3
    # s.test_strategy(indicator='macd', params=(i, j, k), data=data_df)
    #
    # tot_returns = np.zeros((i, j, k))
    # for ss in range(1, i, 2):
    #     for ls in range(2, j, 4):
    #         for sf in range(1, k, 2):
    #             pp.pprint((ss, ls, sf))
    #             tot_returns[ss, ls, sf] = s.test_strategy(indicator='macd', params=(ss, ls, sf), data=data_df)
    #
    # pp.pprint(tot_returns)
    # pp.pprint(np.unravel_index(tot_returns.argmax(), tot_returns.shape))
