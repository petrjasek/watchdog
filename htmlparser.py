#!/usr/bin/env python
# HTML parser

from sgmllib import SGMLParser

class htmlParser(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.products = 0
	
	def start_div(self, attrs):
		id = [v for k, v in attrs if k == 'id']
		if id == 'results':
			self.products = 1
