# -*- coding: utf-8 -*-
import sys
import os
import csv
import numpy as np
import pandas as pd
# import pandas.io.data as web
# import stockstats
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
x_axis = np.arange(1, length+1,1)
# x_axis = np.transpose(np.arange(1,length+1,1))
invested = []
# returns = []
# for i in range(1, length + 1):
#     returns[i] = pxlast[i]

returns = pxlast.pct_change(1)

for i in range(0, length):
    if macd[i] > macd_ema9[i]:
        invested[i] = 1
    else:
        invested[i] = 0

plt.plot(x_axis, pxlast, x_axis, ema12, x_axis, ema26)
# plt.plot(x_axis, ts['ema12'])
# plt.plot(x_axis, ts['ema26'])
input('...')






