#!/usr/bin/env python
# Watchdog

FEED = 'http://www.eshop-simecek.cz/xml_feed_all.php'

import urllib2 as urllib
import xml.dom.minidom as minidom

def getName(name):
	"""Get product name"""
	return name.childNode.data

def getPrice(price):
	"""Get product price"""
	return price.childNode.data

def checkPrice(name, price):
	"""Checks price of product"""
	params = {'q': name, 'order': 'price', 'minPrice': 0, 'maxPrice': price}
	url = 'http://zbozi.cz/items?' + urllib.urlencode(params)
	sock = urllib.urlopen(url)
	html = sock.read()
	sock.close()

	print(url)
	print(html)

# get feed
feed = ""
sock = urllib.urlopen(FEED)
for line in sock:
	if line.find('SHOP') >= 0 or line.find('PRODUCT') >= 0 or line.find('PRICE') >= 0:
		feed += line.decode('windows-1250').encode('utf-8')
sock.close()

print feed
exit()

# parse feed
doc = minidom.parseString(feed)

# get products
for item in doc.getElementsByTagName('SHOPITEM'):
	name = getName(item.getElementsByTagName('PRODUCT')[0])
	price = getPrice(item.getElementsByTagName('PRICE_VAT')[0])
	checkPrice(name, price)
	exit()

# gc
doc.unlink()
