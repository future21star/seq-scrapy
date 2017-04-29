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

class FreshMarketSpider(scrapy.Spider):
		name = "freshmarket"
		uid_list = []
		start_urls = ['https://www.thefreshmarket.com/your-market/store-locator']

		def parse(self, response):
			try:
				script = response.xpath('//script/text()')[1].extract()
				info = json.loads(script[script.find("window.__data=") + 14: -1])
				stores = info['stores']['allStores']
				for store in stores:
					item = ChainItem()
					item['store_number'] = self.validate(store, 'storeNumber')
					item['store_name'] = self.validate(store, 'storeName')
					item['address'] = self.validate(store, 'address')
					item['address2'] = ""
					item['city'] = self.validate(store, 'city')
					item['state'] = self.validate(store, 'state')
					item['zip_code'] = self.validate(store, 'postalCode')
					item['country'] = "United States"
					item['phone_number'] = self.validate(store, 'phoneNumber').replace('.', '-')
					location = self.validate(store,'storeLocation')
					item['latitude'] = location[location.find("'lat': ") + 7 : location.find(",")]
					item['longitude'] = location[location.find("'lon': ") + 7 : -1]	
					item['store_hours'] = self.validate(store, 'moreStoreHours')
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 1 if self.validate(store, 'comingSoon') == 'True' else 0
					yield item
			except:
				pass

		def validate(self, store, property):
			try:
				return str(store[property]).strip()
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