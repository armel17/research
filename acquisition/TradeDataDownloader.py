# -*- coding: utf-8 -*-
import sys

sys.path.append('./')
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

from AcquisitionHelpers import AcquisitionHelpers
# import re
# import time, urllib, urlparse, pprint
# import requesocks
# from lxml import html
# from datetime import timedelta, datetime
# from unidecode import unidecode

class TradeDataDownloader:
    def __init__(self):
        self.acquisition_helpers = AcquisitionHelpers()
        self.currency_pairs = {
            # Maintain manually ...
            # 'BCHEUR': {
            #     'download_data': True
            # },
            # 'BCHUSD': {
            #     'download_data': True
            # },
            # 'BCHXBT': {
            #     'download_data': True
            # },
            # 'DASHEUR': {
            #     'download_data': False
            # },
            # 'DASHUSD': {
            #     'download_data': False
            # },
            # 'DASHXBT': {
            #     'download_data': False
            # },
            # 'EOSETH': {
            #     'download_data': False
            # },
            # 'EOSXBT': {
            #     'download_data': False
            # },
            # 'GNOETH': {
            #     'download_data': False
            # },
            # 'GNOXBT': {
            #     'download_data': False
            # },
            # 'USDTZUSD': {
            #     'download_data': False
            # },
            # 'XETCXETH': {
            #     'download_data': True
            # },
            # 'XETCXXBT': {
            #     'download_data': True
            # },
            # 'XETCZEUR': {
            #     'download_data': True
            # },
            # 'XETCZUSD': {
            #     'download_data': True
            # },
            # 'XETHXXBT': {
            #     'download_data': True
            # },
            # 'XETHXXBT.d': {
            #     'download_data': False
            # },
            # 'XETHZCAD': {
            #     'download_data': True
            # },
            # 'XETHZCAD.d': {
            #     'download_data': False
            # },
            'XETHZEUR': {
                'download_data': True
            },
            # 'XETHZEUR.d': {
            #     'download_data': False
            # },
            # 'XETHZGBP': {
            #     'download_data': True
            # },
            # 'XETHZGBP.d': {
            #     'download_data': False
            # },
            # 'XETHZJPY': {
            #     'download_data': True
            # },
            # 'XETHZJPY.d': {
            #     'download_data': False
            # },
            # 'XETHZUSD': {
            #     'download_data': True
            # },
            # 'XETHZUSD.d': {
            #     'download_data': False
            # },
            # 'XICNXETH': {
            #     'download_data': False
            # },
            # 'XICNXXBT': {
            #     'download_data': False
            # },
            # 'XLTCXXBT': {
            #     'download_data': False
            # },
            # 'XLTCZEUR': {
            #     'download_data': False
            # },
            # 'XLTCZUSD': {
            #     'download_data': False
            # },
            # 'XMLNXETH': {
            #     'download_data': False
            # },
            # 'XMLNXXBT': {
            #     'download_data': False
            # },
            # 'XREPXETH': {
            #     'download_data': False
            # },
            # 'XREPXXBT': {
            #     'download_data': False
            # },
            # 'XREPZEUR': {
            #     'download_data': False
            # },
            # 'XXBTZCAD': {
            #     'download_data': True
            # },
            # 'XXBTZCAD.d': {
            #     'download_data': False
            # },
            # 'XXBTZEUR': {
            #     'download_data': True
            # },
            # 'XXBTZEUR.d': {
            #     'download_data': False
            # },
            # 'XXBTZGBP': {
            #     'download_data': True
            # },
            # 'XXBTZGBP.d': {
            #     'download_data': False
            # },
            # 'XXBTZJPY': {
            #     'download_data': True
            # },
            # 'XXBTZJPY.d': {
            #     'download_data': False
            # },
            # 'XXBTZUSD': {
            #     'download_data': True
            # },
            # 'XXBTZUSD.d': {
            #     'download_data': False
            # },
            # 'XXDGXXBT': {
            #     'download_data': False
            # },
            # 'XXLMXXBT': {
            #     'download_data': False
            # },
            # 'XXMRXXBT': {
            #     'download_data': False
            # },
            # 'XXMRZEUR': {
            #     'download_data': False
            # },
            # 'XXMRZUSD': {
            #     'download_data': False
            # },
            # 'XXRPXXBT': {
            #     'download_data': True
            # },
            # 'XXRPZEUR': {
            #     'download_data': True
            # },
            # 'XXRPZUSD': {
            #     'download_data': True
            # },
            # 'XZECXXBT': {
            #     'download_data': False
            # },
            # 'XZECZEUR': {
            #     'download_data': False
            # },
            # 'XZECZUSD': {
            #     'download_data': False
            # }
        }

    def update_ohlc_db(self):
        count = 1
        for key in self.currency_pairs.keys():
            print('%s/%s' % (str(count), str(len(self.currency_pairs.keys()))))
            if 'download_data' in self.currency_pairs[key]:
                if self.currency_pairs[key]['download_data']:
                    self.acquisition_helpers.build_database(asset_pairs=[key])
            count += 1


if __name__ == '__main__':
    t = TradeDataDownloader()
    t.update_ohlc_db()
