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
import yaml

class TriohockeySpider(scrapy.Spider):
		name = "triohockey"
		uid_list = []
		start_urls = ['http://www.triohockey.ca/data/stores.json']

		def parse(self, response):
			try:
				stores = json.loads(response.body)['data']
				for store in stores:
					item = ChainItem()
					item['store_number'] = store['store_number']
					item['store_name'] = store['name_en']
					item['address'] = store['address1_en']
					item['address2'] = store['address2_en']
					item['city'] = store['city']
					item['state'] = store['province']
					item['zip_code'] = store['postal_code']
					item['country'] = "Canada" 
					item['phone_number'] = store['telephone'].replace('.', '-')
					days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
					item['store_hours'] = ""
					for day in days:
						item['store_hours'] += day + ":" + store[day + '_opening'] + "-" + store[day+ '_closing'] + ";"
					item['latitude'] = store['latitude']
					item['longitude'] = store['longitude']
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




