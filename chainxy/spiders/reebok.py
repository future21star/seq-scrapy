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

class ReebokSpider(scrapy.Spider):
		name = "reebok"
		uid_list = []
		start_urls = ['http://reebokstorelocator.ca/']

		def parse(self, response):
			try:
				stores = yaml.load((response.body.split("locations = ")[-1].split("}};")[0] + "}}").replace("<br\/>", "    ").replace("\/", "  "))
				for _id in stores:
					store = stores[_id]
					item = ChainItem()
					item['store_number'] = store['id']
					item['store_name'] = store['full_name']
					item['address2'] = ""
					addr = store['address'].replace('<br>', ' ')
					item['address'] = addr.split(",")[0].replace('    ', " ").strip()
					item['city'] = store['location']
					item['state'] = addr.split(',')[-1].split("    ")[0].strip()
					item['zip_code'] = addr.split(',')[-1].split("    ")[-1].strip()
					item['country'] = "Canada" 
					item['phone_number'] = store['phone'].replace('.', '-')
					item['store_hours'] = store['hours'].replace("    ", ";").replace('<  br>', ';').replace('<br   >', ';').replace('<br>', ';')
					item['latitude'] = store['lat']
					item['longitude'] = store['lng']
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




