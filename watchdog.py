#!/usr/bin/env python3
"""Watchdog"""

import httplib2
from lxml import etree
from time import sleep
from random import random
from urllib.parse import urlencode

FEED_URL = 'http://www.eshop-simecek.cz/xml_feed_all.php'
FEED_FILE = './_feed.xml'
CACHE = '.cache'

def get_feed(url, dest):
    """Get feed from url and store to dest"""
    http = httplib2.Http(CACHE)
    response, content = http.request(url)
    feed = content.decode('WINDOWS-1250')
    with open(dest, mode='w', encoding='WINDOWS-1250') as file:
        file.write(feed)

# load ignore list
ignored = []
with open('./ignore.txt', mode='r', encoding='utf-8') as file:
    for line in file:
        ignored.append(line.strip())

# fetch feed for parsing
get_feed(FEED_URL, FEED_FILE)

# parse feed
checked = set()
parser = etree.XMLParser(recover=True)
tree = etree.parse(FEED_FILE, parser)
for item in tree.findall('SHOPITEM'):
    product = item.find('PRODUCT')
    price = item.find('PRICE_VAT')
    if product is None or price is None:
        continue

    product = product.text.split(" - ", 1)[0]
    price = int(price.text)

    # remove ignored part
    for ignore in ignored:
        product = product.replace(ignore, '').strip()

    if product in checked or price < 256:
        continue

    checked.add(product)

    # prepare query
    params = {
        'q': product,
        'order': 'price',
        'minPrice': int(price * 0.7),
        'maxPrice': price - 1
    }

    # search for cheaper
    url = 'http://zbozi.cz/items?{}'.format(urlencode(params))
    http = httplib2.Http(CACHE)
    response, content = http.request(url)

    html = content.decode('utf-8')
    if html.find('<div id="results">') > 0:
        print('{0} ({1},-)'.format(product, price))
        print(url)
        print()

    # pretend human
    sleep(random() * 100)
