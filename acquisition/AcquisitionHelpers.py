# -*- coding: utf-8 -*-
import sys

sys.path.append('../KrakenAPI')
import os
import json
import pprint
import requests
from datetime import datetime, timedelta
from pymongo import MongoClient, errors, ASCENDING, DESCENDING, TEXT
import time
from KrakenAPI import KrakenAPI

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


class AcquisitionHelpers:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.kraken
        self.kraken_api = KrakenAPI()

    def download_ohlc_data(self, currency_pair):
        for interval in [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]:
            print('Start downloading %s for %s min interval' % (currency_pair, str(interval)))
            collection = 'ohlc_%s' % (str(interval))

            all_elements = self.db[collection].find({'ccy_pair': currency_pair}, {'timestamp': 1})
            if all_elements.count() == 0:
                since = 0
            else:
                since = int(max([x['timestamp'] for x in all_elements]).timestamp())

            theEnd = False
            while not theEnd:

                params = {
                    'pair': currency_pair,
                    'interval': interval,
                    'since': since
                }

                print('Current API calls count: %s' % str(self.kraken_api.counter.api_calls_count))
                result = self.kraken_api.public_method('OHLC', params)
                if result.status_code == 200:
                    result_json = json.loads(result.text)
                    error = result_json['error']
                    if error == []:
                        results = result_json['result']
                        datapoints = self.json_to_datapoints(results)
                        self.save_to_mongo(collection, datapoints)
                        last = results['last']
                        # print(datetime.fromtimestamp(int(last)))

                        if since == last:
                            theEnd = True
                        else:
                            since = last
                    else:
                        print(error)
                        theEnd = True
            print('Done')

    def get_tradable_asset_pairs(self):
        result = self.kraken_api.public_method(name='AssetPairs')
        try:
            if result.status_code == 200:
                result_json = json.loads(result.text)
                error = result_json['error']
                if error == []:
                    asset_pairs = result_json['result']
                else:
                    raise Exception('Could not get tradable asset pairs.')
            else:
                raise Exception('Could not get tradable asset pairs.')
        except Exception as e:
            print(str(e))
            asset_pairs = None
        return asset_pairs

    def build_database(self, asset_pairs=None):
        if asset_pairs is None:
            asset_pairs = list(self.get_tradable_asset_pairs().keys())
        if type(asset_pairs) is not list:
            print('asset_pairs should be a list.')
            return None

        first_pair = True
        for asset_pair in asset_pairs:
            print('Downloading %s data' % asset_pair)
            self.download_ohlc_data(asset_pair)
            if first_pair:
                for interval in [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]:
                    collection = 'ohlc_%s' % (str(interval))
                    try:
                        self.db[collection].create_index([('timestamp', ASCENDING)], background=True)
                        self.db[collection].create_index([('ccy_pair', ASCENDING), ('timestamp', ASCENDING)],
                                                         background=True)
                    except Exception as e:
                        print(e)
                first_pair = False
            print('Done')

    def save_to_mongo(self, collection, datapoints):
        for datapoint in datapoints:
            element_in_mongo = self.db[collection].find_one(
                {
                    'ccy_pair': datapoint['ccy_pair'],
                    'timestamp': datapoint['timestamp']
                }
            )
            if element_in_mongo is None:
                self.db[collection].insert_one(datapoint)

    def json_to_datapoints(self, json_results):
        ccy_pair = [x for x in json_results][0]
        datapoints = []

        for point in json_results[ccy_pair]:
            datapoint = {'ccy_pair': ccy_pair}
            datapoint['timestamp'] = datetime.fromtimestamp(point[0])
            datapoint['open'] = float(point[1])
            datapoint['high'] = float(point[2])
            datapoint['low'] = float(point[3])
            datapoint['close'] = float(point[4])
            datapoint['vwap'] = float(point[5])
            datapoint['volume'] = float(point[6])
            datapoint['count'] = float(point[7])
            datapoints.append(datapoint)

        return datapoints


if __name__ == '__main__':
    h = AcquisitionHelpers()
    # test = {
    #     'timestamp': datetime.now()
    # }
    # pair = 'XETHZEUR'
    # h.download_ohlc_data(pair)
    # pprint.pprint(h.get_tradable_asset_pairs().keys())
    h.build_database()
    # h.save_to_mongo([test, test])
    print('...')
