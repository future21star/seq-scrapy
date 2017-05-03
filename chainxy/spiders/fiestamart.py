import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
import unicodedata

class FiestamartSpider(scrapy.Spider):
		name = "fiestamart"
		uid_list = []
		start_urls = ['http://fiestamart.com/umbraco/storelocator/Location.xml']

		def parse(self, response):
			try:
				stores = response.xpath('//marker')
				for store in stores:
					item = ChainItem()
					item['store_number'] = self.validate(store.xpath('./@name'))
					item['store_name'] = ""
					item['address'] = self.validate(store.xpath('./@address'))
					item['address2'] = self.validate(store.xpath('./@address2'))
					item['city'] = self.validate(store.xpath('./@city'))
					item['state'] = self.validate(store.xpath('./@state'))
					item['zip_code'] = self.validate(store.xpath('./@postal'))
					item['country'] = "United States" 
					item['phone_number'] = self.validate(store.xpath('./@phone'))
					item['store_hours'] = self.validate(store.xpath('./@hours1'))
					item['latitude'] = self.validate(store.xpath('./@lat'))
					item['longitude'] = self.validate(store.xpath('./@lng'))
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					yield item
			except:
				pass			

		def validate(self, xpath):
			try:
				return self.replaceUnknownLetter(xpath.extract_first().strip())
			except:
				return ""

		def replaceUnknownLetter(self, source):
			try:
				formatted_value = source.encode('utf8').replace('\xc3', '').replace('\xa9', 'e').replace('\xa8', 'e').replace('\xb4', 'o').replace('\xb3', 'o').replace('\xb9', 'u').replace('\xba', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
				# if "x8" in formatted_value or "x9" in formatted_value or "xa" in formatted_value or "xb" in formatted_value:
				# 	pdb.set_trace()
				return formatted_value
			except:
				return source
		def format(self, item):
			try:
				return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
			except:
				return ''			




