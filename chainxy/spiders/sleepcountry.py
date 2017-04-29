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
import ast 

class SleepcountrySpider(scrapy.Spider):
		name = "sleepcountry"
		uid_list = []
		start_urls = ['http://www.sleepcountry.ca/aboutus/findastore.aspx']

		def parse(self, response):
			try:
				script = response.xpath('//script[@type="text/javascript"]/text()')[10].extract()
				info = script[script.find("var locations = ") + 16: script.find("var arrStores") - 7]
				info = info.replace('\r\n' , '').replace('<br />', ';')
				stores = ast.literal_eval(info)
				for store in stores:
					item = ChainItem()
					item['store_number'] = store[0]
					item['store_name'] = self.validate(store, 'storeName')
					item['address'] = store[4]
					item['address2'] = ""
					item['city'] = store[5]
					item['state'] = store[6]
					item['zip_code'] = store[7]
					item['country'] = "Canada"
					item['phone_number'] = store[8]
					item['latitude'] = store[1]
					item['longitude'] = store[2]
					item['store_hours'] = store[9]
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = "0"
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