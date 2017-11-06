# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


class Indicators(object):
    @staticmethod
    def macd(data, short_span=12, long_span=26, smoothing_factor=9):
        if type(data) is not pd.Series:
            raise TypeError('MACD requires time series data to be of pandas.Series type.')
        elif any([x for x in [short_span, long_span, smoothing_factor] if type(x) is not int]):
            raise TypeError('MACD requires arguments to be integers, except time series data.')
        else:
            try:
                ema_short_span = pd.ewma(data, span=short_span)
                ema_long_span = pd.ewma(data, span=long_span)
                macd = ema_short_span - ema_long_span
                macd_ewma = pd.ewma(macd, span=smoothing_factor)
                return macd, macd_ewma
            except Exception as e:
                print('Unhandled exception in Indicators.macd: ' + str(e))
                return None, None

    def ema_diff(data, short_span=12, long_span=26):
        if type(data) is not pd.Series:
            raise TypeError('EMA_diff requires time series data to be of pandas.Series type.')
        elif any([x for x in [short_span, long_span] if type(x) is not int]):
            raise TypeError('EMA_diff requires arguments to be integers, except time series data.')
        else:
            try:
                ema_short_span = pd.ewma(data, span=short_span)
                ema_long_span = pd.ewma(data, span=long_span)
                ema_difference = ema_short_span - ema_long_span
                return ema_difference
            except Exception as e:
                print('Unhandled exception in Indicators.ema_diff: ' + str(e))
                return None

    def RSI(data, period):
        if type(data) is not pd.Series:
            raise TypeError('RSI requires time series data to be of pandas.Series type.')
        elif type(period) is not int:
            raise TypeError('RSI requires arguments to be integers, except time series data.')
        else:
            delta = data.diff()
            u = delta * 0
            d = u.copy()
            u[delta > 0] = delta[delta > 0]
            d[delta < 0] = -delta[delta < 0]
            u[u.index[period - 1]] = np.mean(u[:period])  # first value is sum of avg gains
            u = u.drop(u.index[:(period - 1)])
            d[d.index[period - 1]] = np.mean(d[:period])  # first value is sum of avg losses
            d = d.drop(d.index[:(period - 1)])
            rs = pd.stats.moments.ewma(u, com=period - 1, adjust=False) / \
                pd.stats.moments.ewma(d, com=period - 1, adjust=False)
            return 100 - 100 / (1 + rs)
