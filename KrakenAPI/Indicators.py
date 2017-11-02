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
