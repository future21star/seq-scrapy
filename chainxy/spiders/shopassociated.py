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

class ShopassociatedSpider(scrapy.Spider):
		name = "shopassociated"
		uid_list = []
		start_urls = ['http://www.shopassociated.com/locations/']
		count = 0

		def parse(self, response):
			stores = self.getStores(response.body)
			for store in stores:
				item = ChainItem()
				item['store_number'] = store['storeNumber']
				item['store_name'] = store['name']
				item['address'] = store['address1']
				item['address2'] = ""
				item['city'] = store['city']
				item['state'] = store['state']
				item['zip_code'] = store['zipCode']
				item['country'] = "United States" 
				item['phone_number'] = store['phone']
				try:
					item['store_hours'] = store['hourInfo']
				except:
					item['store_hours'] = ""
				item['coming_soon'] = 0
				item['latitude'] = store['latitude']
				item['longitude'] = store['longitude']
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				yield item

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""

		def getStores(self, response):
			pos = response.find("var stores = ") + 13
			str = ""
			while response[pos:pos+2] != "];":
				str += response[pos]
				pos += 1
			str += "]"
			return json.loads(str) 