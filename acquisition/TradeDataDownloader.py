# -*- coding: utf-8 -*-
import sys
import os
import json
import pprint

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# from AcquisitionTools import AcquisitionTools
# import re
# import time, urllib, urlparse, pprint
# import requesocks
# from lxml import html
# from datetime import timedelta, datetime
# from unidecode import unidecode

class TradeDataDownloader:

    def __init__(self, currency_pair):
        self.currency_pair = currency_pair
