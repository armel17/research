# -*- coding: utf-8 -*-
import sys
import os
import json
import pprint
import requests
from datetime import datetime, timedelta
from pymongo import MongoClient

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

    def public_method(self, name, params):
        # 'name' must start with capital letter
        url = self.public_url + name
        result = self.session.get(url, headers=self.headers, params=params)
        return result

    def get_ohlc_data(self, currency_pair):
        all_elements = self.db['ohlc'].find({'ccy_pair': currency_pair, 'last': {'$gt': 0}}).sort('last')
        if all_elements.count() == 0:
            since = 0
        else:
            since = max([x for x in all_elements])

        theEnd = False
        while not theEnd:

            params = {
                'pair': currency_pair,
                'interval': 1440,  # in minutes: 1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600
                'since': since
            }

            result = self.public_method('OHLC', params)
            result_json = json.loads(result.text)
            error = result_json['error']
            results = result_json['result']
            last = results['last']
            print(datetime.fromtimestamp(int(last)))

            if since == last:
                theEnd = True
            else:
                since = last

    def save_to_mongo(self, dicts):
        self.db['ohlc'].insert_many(dicts)


if __name__ == '__main__':
    k = KrakenAPI()
    test = {
        'timestamp': datetime.now()
    }
    pair = 'XXBTZEUR'
    k.get_ohlc_data(pair)
    #k.save_to_mongo([test, test])
