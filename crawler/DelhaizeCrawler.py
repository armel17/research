# -*- coding: utf-8 -*-
import sys,os

import lxml
from lxml import html
import pprint, re, time
from datetime import timedelta, datetime
import json
import requests
from unidecode import unidecode

start_page = "http://www.delhaize.be/fr-be"

session = requests.session()
headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest'
                }

page_result = session.get(start_page, headers=headers, verify=False)
tree = html.fromstring(page_result.text)
all_sections = tree.xpath('//div[contains(@class,"top-level-container")]/ul/li/a')

categories_url = []
#List comprehension
categories_url = [start_page + x.get('href').split('fr-be')[-1] for x in all_sections]

products = {}

for url in categories_url:
    try:
        page_result = session.get(url + '/getSearchPageData?pageSize=1000', headers=headers, verify=False)
        json_page_result = json.loads(page_result.text)
        raw_products = json_page_result['results']
        for raw_product in raw_products:
            title = raw_product['name']
            price = raw_product['price']['unitPrice']
            products[title] = price

    except Exception:
        print('')

pprint.pprint(products)

#for section in all_sections:
#    url = start_page + section.get('href').split('fr-be')[-1]
#    categories_url.append(url)

pprint.pprint(categories_url)


