#!/usr/local/bin/python
import urllib2, urllib, sys, getopt

from optparse import OptionParser
from bs4 import BeautifulSoup

class Crawler():
	""" Class to handle crawl in shoping.com
		and return two queries total item count
		for specific item and item name in the
		given page """

	soup = ""
	total_number_of_item = 0
	current_page_number = 1
	searching_item = ""
	search_all = True
	current_page_items = []

	def __init__(self, *args, **kwargs):
		self.searching_item = kwargs.get("search_item")
		page_number = kwargs.get("page_number")
		if page_number:
			self.current_page_number = int(page_number)
			self.search_all = False
		self.get_http_response()

	def get_paginated_url(self):
		""" Method will retunr url with current pagination
			and item name as arguments """

		url = "http://www.shopping.com/products~PG-%s?KW=%s" % (
			self.current_page_number, urllib.quote_plus(self.searching_item))
		self.current_page_number += 1
		return url
	
	def get_http_response(self):
		""" get the response from the shoping.com using urllib2
			and give that response to BeautifulSoup for
			manipulating the html content easly """

		url = self.get_paginated_url()
		if self.total_number_of_item > 0:
			print "Calculating, %s %s are found till now!" % (
				self.total_number_of_item, self.searching_item)
		response = urllib2.urlopen(url)
		self.soup = BeautifulSoup(response.read(),
								  "html.parser")
		self.find_item_count(self.soup)
	
	def find_item_count(self, soup):
		""" We know that items in website as wraped with div
			with class of gridBox, so we are find all grid
			box in page and get its count, based on the count
			we are recursively calling this two methods"""
		items_tags = soup.find_all("div", {"class": "gridBox"})
		self.current_page_items = items_tags
		item_count = len(items_tags)
		if item_count:
			self.total_number_of_item += item_count
			# If search_all is true only, we are doing the
			# recursion because if user pass the page number
			# we only need to show that page number detail
			if self.search_all:
				self.get_http_response()
			
	def get_result(self):
		""" Method with print the result """
		if self.total_number_of_item:
			if self.search_all:
				print "%s %s are found." % (
						self.total_number_of_item,
						self.searching_item)
			else:
				index = 1
				for item in self.current_page_items:
					item_a = item.find_all("a", {"class": "productName"})[0]
					if item_a.span:
						print "%s %s" % (index, item_a.span.get("title"))
					else:
						print "%s %s" % (index, item_a.get("title"))
					index += 1
		else:
			print "%s are not found." % (self.searching_item)



if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-i", "--item", dest="item_name",
                  help="Name want searh", metavar="ITEM")
	parser.add_option("-p", "--pagenumber", dest="page_number",
                  help="if specify page, find only that page")

	(options, args) = parser.parse_args()

	item_name = options.item_name
	page_number = options.page_number
	if item_name:
		crowler = Crawler(search_item=item_name,
						  page_number=page_number)
		crowler.get_result()
	else:
		print  "Please provid a item name to find.\n\
			    as argument --item or -i\n\
		        for specify page number --pagenumber or -p"

