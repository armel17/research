# -*- coding: utf-8 -*-
import sys
import os
import json
import pprint
import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
import time
from APICallCounter import APICallCounter

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


class KrakenAPI:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.kraken
        self.session = requests.session()
        self.public_url = 'https://api.kraken.com/0/public/'
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'nl,en-US;q=0.8,en;q=0.6,en-GB;q=0.4,fr;q=0.2',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'cache-control': 'max-age=0',
            'authority': 'api.kraken.com',
            # 'cookie': '__cfduid=d5ee08fd9f625efa3e624593b426f54981486480951; dev=lROZyVvpxISGBA0Ont1TiGPhA_D_VHmOiDp3RPqsGzo; _ga=GA1.2.906282867.1486480955; _gid=GA1.2.788736959.1506965213; __zlcmid=flgKQkuR1iywrC',
            # 'referer': 'https://support.kraken.com/hc/en-us/articles/218198197-How-to-pull-all-trade-data-using-the-Kraken-REST-API',
        }
        self.counter = APICallCounter(client_tier=2)

    def public_method(self, name, params):
        # 'name' must start with capital letter
        url = self.public_url + name
        # TODO - Check that all public method increase counter by 2, or not
        if self.counter.add_call(count_increase=2):
            result = self.session.get(url, headers=self.headers, params=params)
            return result
        else:
            return '%s public method not run' % name

    def download_ohlc_data(self, currency_pair):
        for interval in [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]:
            print('Start downloading %s for %s sec interval' % (currency_pair, str(interval)))
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

                print('Current API calls count: %s' % str(self.counter.api_calls_count))
                result = self.public_method('OHLC', params)
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
    k = KrakenAPI()
    test = {
        'timestamp': datetime.now()
    }
    pair = 'XXBTZEUR'
    k.download_ohlc_data(pair)
    #k.save_to_mongo([test, test])
