import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class ElevenSpider(scrapy.Spider):
		name = "eleven"
		uid_list = []

		headers = { "Content-Type": "application/json", "Accept":"*/*" }

		def __init__(self):
			place_file = open('uscanplaces.csv', 'rb')
			self.place_reader = csv.reader(place_file)

		def start_requests(self):
			for row in self.place_reader:
				request_url = "https://www.7-eleven.com/api/location/searchstores"
				form_data = {
					'Filters' : [],
					'PageNumber' : "0",
					"PageSize" : "100000",
					"SearchRangeMiles" : "5",
					"SourceLatitude" : row[0],
					"SourceLongitude": row[1]
				}
				yield scrapy.Request(url=request_url, method="POST", body=json.dumps(form_data), headers=self.headers, callback=self.parse_store)

		# get longitude and latitude for a state by using google map.
		def parse_store(self, response):
			# try:
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store, 'StoreName')
				item['store_number'] = self.validate(store, 'StoreNumber')
				item['address'] = self.validate(store, 'Address1') 
				item['address2'] = self.validate(store, 'Address2')
				item['phone_number'] = self.validate(store, 'Phone')
				item['city'] = self.validate(store, 'City')
				item['state'] = self.validate(store, 'State')
				item['zip_code'] = self.validate(store, 'Zip')
				item['country'] = 'US'
				item['latitude'] = self.validate(store, 'Latitude')
				item['longitude'] = self.validate(store,  'Longitude')
				item['store_hours'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if item['store_number'] == "" or (item["store_number"] in self.uid_list):
				    return
				self.uid_list.append(item["store_number"])
				yield item

		def validate(self, store, attribute):
			if (attribute in store) and (store[attribute] != "null") :
				return store[attribute]
			return ""


