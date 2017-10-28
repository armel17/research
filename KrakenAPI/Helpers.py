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
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


class Helpers:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.kraken

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
        return pd.DataFrame(tuple_list,index=[x[0] for x in tuple_list])

    def test_mongo_to_list(self):
        query = {
            'ccy_pair': 'XETHZEUR',
            'timestamp': {
                '$gt': datetime.today() - timedelta(days=100)
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
    h.test_mongo_to_list()
