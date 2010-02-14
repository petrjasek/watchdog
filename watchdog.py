#!/usr/bin/env python
# Watchdog

FEED = 'http://www.eshop-simecek.cz/xml_feed_all.php'
FILE = 'feed.xml'

import random
import urllib2
import xml
import xml.dom.minidom as minidom

def updateFeed():
	"""Gets feed and stores it"""
	feed = urllib2.urlopen(FEED)
	file = open(FILE, 'w')
	for line in feed:
		file.write(line.decode('windows-1250').encode('utf-8'))
	file.close()

def getFeed(filename):
	"""Load feed and decode it"""
	f = open(filename, 'r')

def getName(name):
	"""Get product name"""
	return name.childNodes[0].data

def getPrice(price):
	"""Get product price"""
	return price.childNodes[0].data

# update feed
#updateFeed()

# parse feed

try:
	feed = minidom.parse(FILE)
except xml.parsers.expat.ExpatError:
	pass

# get products
for item in feed.getElementsByTagName('SHOPITEM'):
	name = getName(item.getElementsByTagName('PRODUCT')[0])
	price = getPrice(item.getElementsByTagName('PRICE_VAT')[0])
	print(name, price)

# gc
feed.unlink()
