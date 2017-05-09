import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class KwikshopSpider(scrapy.Spider):
		name = "kwikshop"
		uid_list = []

		headers = { }

		def __init__(self):
			place_file = open('states.json', 'rb')
			self.place_reader = json.load(place_file)

		def start_requests(self):
			for state in self.place_reader:
				request_url = "https://www.kwikshop.com/stores?address=%s&maxResults=200&open24Hours=false&radius=30000&showAllStores=true&storeType=&useLatLong=false" % state["code"]
				yield scrapy.Request(url=request_url, callback=self.parse_store)

		def parse_store(self, response):
			try:
				stores = json.loads(response.body)
				for store in stores:
					item = ChainItem()
					info = store['storeInformation']
					item['store_name'] = self.validate(info, 'localName')
					item['store_number'] = self.validate(info, 'storeNumber')
					item['address'] = info['address']['addressLineOne']
					item['address2'] = ""
					item['city'] = info['address']['city']
					item['state'] = info['address']['state']
					item['zip_code'] = info['address']['zipCode']
					item['phone_number'] = info['phoneNumber']
					item['country'] = "United States"
					item['latitude'] = info['latLong']['latitude']
					item['longitude'] = info['latLong']['longitude']
					item['store_hours'] = ""
					hours = store['storeHours']
					for key in hours:
						item['store_hours'] += key + ":" + hours[key] + ";"
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = ""
					if item['store_number'] != "" and item["store_number"] in self.uid_list:
					    return
					self.uid_list.append(item["store_number"])
					yield item
			except:
				pdb.set_trace()
				pass

		def validate(self, store, attribute):
			if attribute in store:
				return store[attribute]
			return ""


