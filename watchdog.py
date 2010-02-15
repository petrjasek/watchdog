#!/usr/bin/env python
# Watchdog

FEED = 'http://www.eshop-simecek.cz/xml_feed_all.php'

import urllib
import xml.dom.minidom as minidom
import htmlparser

def getName(name):
	"""Get product name"""
	return name.firstChild.data.encode('utf-8')

def getPrice(price):
	"""Get product price"""
	return int(price.firstChild.data)

def checkPrice(name, price):
	"""Checks price of product"""
	params = {'q': name, 'order': 'price', 'minPrice': 0, 'maxPrice': price - 1}
	url = 'http://zbozi.cz/items?' + urllib.urlencode(params)
	sock = urllib.urlopen(url)
	html = sock.read()
	sock.close()

	parser = htmlparser.htmlParser()
	parser.feed(html)
	parser.close()

	if parser.products:
		print url

# get feed
feed = ""
sock = urllib.urlopen(FEED)
for line in sock:
	if line.find('SHOP') >= 0 or line.find('PRODUCT') >= 0 or line.find('PRICE') >= 0:
		feed += line.decode('windows-1250').encode('utf-8')
sock.close()

# parse feed
doc = minidom.parseString(feed)

# check price for products
for item in doc.getElementsByTagName('SHOPITEM'):
	name = getName(item.getElementsByTagName('PRODUCT')[0])
	price = getPrice(item.getElementsByTagName('PRICE_VAT')[0])
	checkPrice(name, price)


# gc
doc.unlink()
