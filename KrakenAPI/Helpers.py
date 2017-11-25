# -*- coding: utf-8 -*-
import sys
import os
import json
import pprint
import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


class Helpers:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.kraken

    ##########################
    # Data related functions #
    ##########################

    def mongo_to_tuple_list(self, table, query, output_value=None, index='timestamp'):
        if output_value is None:
            return None
        else:
            all_elements = self.db[table].find(query, no_cursor_timeout=True).sort([(index, 1)])
            data = [(x[index], x[output_value]) for x in all_elements]
            return data

    def mongo_to_dict_list(self, table, query, output_value=None, index='timestamp'):
        if output_value is None:
            return None
        else:
            output = {}
            if type(output_value) is list:
                for value in output_value:
                    data = self.mongo_to_tuple_list(table, query, output_value=value, index=index)
                    output[value] = data
            else:
                data = self.mongo_to_tuple_list(table, query, output_value=output_value, index=index)
                output[output_value] = data
            return output

    def tuple_list_to_dframe(self, tuple_list, index=0):
        if type(index) is int:
            return pd.DataFrame([x[1] for x in tuple_list], index=[x[index] for x in tuple_list])
        else:
            print('Index type must be an int.')
            return None

    def mongo_to_df(self, ccy_pairs, since_date, interval=60, value_type='close'):
        all_data = None
        column_names = []
        if type(ccy_pairs) is list:
            for pair in ccy_pairs:
                query = {
                    'ccy_pair': pair,
                    'timestamp': {
                        '$gt': since_date
                    }
                }
                data_raw = self.mongo_to_dict_list(table='ohlc_%s' % str(interval), query=query,
                                                   output_value=value_type)
                data_df = self.tuple_list_to_dframe(data_raw['close'])
                if data_df.size > 0:
                    column_names.append(pair)
                    if all_data is None:
                        all_data = data_df
                    else:
                        all_data = pd.concat([all_data, data_df], axis=1)
            all_data.columns = column_names
            return all_data


    #############################
    # Finance related functions #
    #############################
    @staticmethod
    def indicators_to_investment(indicator_name='', data=()):
        results = None
        if indicator_name != '' and data != ():
            if indicator_name == 'macd':
                macd = data[0]
                macd_ewma = data[1]
                # TODO - Rewrite for DataFrame input and not Series
                results = pd.DataFrame(macd > macd_ewma)
            elif indicator_name == 'ema_diff':
                ema_diff = data[0]
                results = pd.DataFrame(
                    ema_diff > 0)  # pd.Series([x > 0 for x in zip(ema_diff)])  # will be autopromoted to int
            elif indicator_name == 'macd_rsi':
                macd = data[0]
                macd_ewma = data[1]
                rsi = data[2]
                # TODO - @Rom - Et puis? :D

        return results

    #####################
    # Testing functions #
    #####################

    def test_mongo_to_list(self):
        query = {
            'ccy_pair': 'XETHZEUR',
            'timestamp': {
                '$gt': datetime.today() - timedelta(days=1000)
            }
        }
        interval = 1440
        value = 'close'
        data = self.mongo_to_dict_list(table='ohlc_%s' % str(interval), query=query, output_value=value)
        data_df = self.tuple_list_to_dframe(data['close'])
        data_df.plot()
        input('...')


if __name__ == '__main__':
    h = Helpers()
    # h.test_mongo_to_list()

    ccy_pairs = ['XETHZEUR', 'XXBTZEUR', 'XETCZEUR']
    since_date = datetime.strptime('01-01-2017', '%d-%m-%Y')
    interval = 60
    value_type = 'close'
    data_df = h.mongo_to_df(ccy_pairs=ccy_pairs, since_date=since_date, interval=interval, value_type=value_type)
    data_df.plot()
    plt.show(block=True)
