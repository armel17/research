# -*- coding: utf-8 -*-
import sys

sys.path.append('./')
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
import json
import pprint
import requests
from datetime import datetime, timedelta
from pymongo import MongoClient, errors, ASCENDING, DESCENDING, TEXT
import time
from APICallCounter import APICallCounter


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

    #
    # PUBLIC METHODS
    #
    def public_method(self, name, params=None):
        # 'name' must start with capital letter
        url = self.public_url + name
        # TODO - Check that all public method increase counter by 2, or not
        if self.counter.add_call(count_increase=2):
            result = self.session.get(url, headers=self.headers, params=params)
            return result
        else:
            return '%s public method not run' % name


#
# PRIVATE METHODS
#




if __name__ == '__main__':
    k = KrakenAPI()

