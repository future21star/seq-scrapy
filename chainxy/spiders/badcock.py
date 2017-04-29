import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class BadcockSpider(scrapy.Spider):
	name = "badcock"
	uid_list = []

	def __init__(self):
		place_file = open('citiesusca.json', 'rb')
		self.place_reader = json.load(place_file)
		
	def start_requests(self):
		for city in self.place_reader:
			info = self.place_reader[city]
			if info['country'] == "United States":
				request_url = "https://www.badcock.com/stores?latitude=%s&longitude=%s&locator_query=%s&range=500" % (info['latitude'], info['longitude'], info['city'].replace(' ', '+'))
				yield scrapy.Request(url=request_url, callback=self.parse_store)

	def parse_store(self, response):
		try:
			store_locations = []
			locations = response.xpath('//script/text()').extract()[-1]
			locations = json.loads(locations[locations.find("addMarkers(") + 11 : locations.find("}]);\n") + 2])
			for location in locations:
				store_locations.append({
					'lat' : location['lat'],
					'lng' : location['lng']
					})
			stores = response.xpath('//div[@class="store-location"]')
			for store in stores:
				item = ChainItem()
				item['store_name'] = ""
				item['store_number'] = ""
				if "#" in store.xpath('.//div[@class="accent-heading"]/text()').extract()[-1]:
					item['store_number'] = store.xpath('.//div[@class="accent-heading"]/text()').extract()[-1].strip().split('#')[-1][:-1]
				item['address'] = store.xpath('.//address/strong/text()').extract_first()
				item['address2'] = ""
				item['phone_number'] = store.xpath('.//address/text()').extract()[4].strip()
				item['city'] = store.xpath('.//address/text()').extract()[2].strip().split(',')[0]
				item['state'] = store.xpath('.//address/text()').extract()[2].strip().split(',')[1].split()[0]
				item['zip_code'] = store.xpath('.//address/text()').extract()[2].strip().split(',')[1].split()[1]
				item['country'] = "United States"
				item['latitude'] = store_locations[stores.index(store)]['lat']
				item['longitude'] = store_locations[stores.index(store)]['lng']
				item['store_hours'] = ""
				for hour in store.xpath('.//div[@class="store-hours"]/small/div'):
					item['store_hours'] += hour.xpath('./text()').extract_first().strip().replace('\n', '') + ";"
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				if item['phone_number'] != "" and item['phone_number'] in self.uid_list:
					continue
				self.uid_list.append(item['phone_number'])
				yield item
		except:
			pass
