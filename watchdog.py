#!/usr/bin/env python
# Watchdog

FEED = 'http://www.eshop-simecek.cz/xml_feed_all.php'

import urllib
import xml.dom.minidom as minidom
from sgmllib import SGMLParser

checked = set() # names checked allready
ignore = [] # names to be ignored

# search for div id='results' ~ cheaper products exists
class htmlParser(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.products = False
	
	def start_div(self, attrs):
		id = [v for k, v in attrs if k == 'id']
		if id == ['results']:
			self.products = True

def getName(name):
	"""Get product name"""
	name = name.firstChild.data.encode('utf-8')
	for i in ignore:
		name = name.replace(i, "").lstrip()
	return name

def getPrice(price):
	"""Get product price"""
	return int(price.firstChild.data)

def checkPrice(name, price):
	"""Checks price of product"""
	# gets part of name suitable for search
	name = name.split(" - ", 1)[0]

	# check if not searched allready
	if name in checked:
		return
	else:
		checked.add(name)

	# params for search
	params = {
		'q': '%s' % name,
		'order': 'price',
		'minPrice': int(price * 0.7),
		'maxPrice': price - 1
		}

	# search for cheaper
	url = 'http://zbozi.cz/items?' + urllib.urlencode(params)
	sock = urllib.urlopen(url)
	html = sock.read()
	sock.close()

	# parse recieved html
	parser = htmlParser()
	parser.feed(html)
	parser.close()

	# prints output
	if parser.products:
		print name, "(" + str(price) + ",-)"
		print url
		print

# get feed
# filter unusefull lines
feed = ""
sock = urllib.urlopen(FEED)
for line in sock:
	if line.find('SHOP') >= 0 or line.find('PRODUCT') >= 0 or line.find('PRICE') >= 0:
		feed += line.decode('windows-1250').encode('utf-8')
sock.close()

# load ignore list
f = open('./ignore.txt', 'r')
for line in f:
	ignore.append(line.rstrip())
f.close()

# parse feed
doc = minidom.parseString(feed)

# check price for products
for item in doc.getElementsByTagName('SHOPITEM'):
	name = getName(item.getElementsByTagName('PRODUCT')[0])
	price = getPrice(item.getElementsByTagName('PRICE_VAT')[0])
	checkPrice(name, price)

doc.unlink()

