# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

stock = pd.read_csv('../Data/bitcoin_histo.csv', sep=';')
pxlast = stock['PX_LAST']
dates = stock['Date']
ema26 = pd.ewma(pxlast, span=26)
ema12 = pd.ewma(pxlast, span=12)
macd = ema12 - ema26
macd_ema9 = pd.ewma(macd, span=9)
length = len(pxlast)
# x_axis = np.transpose(np.arange(1,length+1,1))
invested = pd.Series([0] * (length - 1))
# returns = []
# for i in range(1, length + 1):
#     returns[i] = pxlast[i]

returns = pxlast.pct_change(1)

for i in range(0, length - 1):
    if macd.loc[i] > macd_ema9.loc[i]:
        invested.loc[i] = 1
    else:
        invested.loc[i] = 0

x_axis = np.arange(1, length+1, 1)

# plt.plot(x_axis, pxlast, x_axis, ema12, x_axis, ema26)


def profitability(returns_mat, invested_mat):
    length_mat = len(returns_mat)
    total_return = pd.Series([0] * length_mat)
    return_strat = pd.Series([0] * length_mat)
    total_return.loc[0] = 100
    return_strat.loc[0] = 100

    for indexing in range(0, length_mat - 1):
        total_return.loc[indexing + 1] = total_return.loc[indexing] * (1 + returns_mat.loc[indexing + 1])
        return_strat.loc[indexing + 1] = return_strat.loc[indexing] * (1 + (invested_mat.loc[indexing]) * returns_mat.loc[indexing + 1])
    return total_return, return_strat


test_profit = profitability(returns, invested)

input('...')