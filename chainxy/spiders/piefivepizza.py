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

class PiefivepizzaSpider(scrapy.Spider):
		name = "piefivepizza"
		uid_list = []
		start_urls = ['https://www.piefivepizza.com/locations/']
		count = 0

		def parse(self, response):
			for state_url in response.xpath("//area[contains(@href, 'https://www.piefivepizza.com/locations/?state=')]/@href").extract():
				yield scrapy.Request(url=state_url, callback=self.parse_store_url)

		def parse_store_url(self, response):
			try:
				stores = response.xpath('//div[@class="loc-search-results"]/div[@class="row"]')
				for store in stores:
					item = ChainItem()
					if len(store.xpath('.//span[@class="loc-status"]')) > 0:
						item['coming_soon'] = 1
					else:
						item['coming_soon'] = 0
					item['store_number'] = ""
					item['store_name'] = self.validate(store.xpath('.//span[@class="loc-name"]/a/text()'))
					item['address'] = self.validate(store.xpath('.//span[@class="loc-address-1"]/text()'))
					item['address2'] = ""
					item['city'] = self.validate(store.xpath('.//span[@class="loc-address-3"]/text()')).split(',')[0].strip()
					item['state'] = self.validate(store.xpath('.//span[@class="loc-address-3"]/text()')).split(',')[1].split()[0].strip()
					try:
						item['zip_code'] = self.validate(store.xpath('.//span[@class="loc-address-3"]/text()')).split(',')[1].split()[1].strip()
					except:
						item['zip_code'] = ""
					item['country'] = "United States"
					try: 	
						item['phone_number'] = self.validate(store.xpath('.//span[@class="loc-phone"][1]/text()')).split('.')[-1].strip()
					except:
						item['phone_number'] = ""
					item['store_hours'] = self.validate(store.xpath('.//span[@class="loc-hours"]/text()'))
					index = stores.index(store) + 1
					pos = response.body.find(', ' + str(index) + ']')
					item['longitude'] = ""
					item['latitude'] = ""
					pos -= 1
					while response.body[pos] != ',':
						item['longitude'] += response.body[pos]
						pos -= 1
					item['longitude'] = item['longitude'].strip()[::-1]
					pos -= 1						
					while response.body[pos] != ',':
						item['latitude'] += response.body[pos]
						pos -= 1
					item['latitude'] = item['latitude'].strip()[::-1]
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					yield item
			except:
				pdb.set_trace()
				pass			

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""

		def getInfo(self, response):
			try:
				start = response.body.find("location_data.push( ") + 20
				pos = response.body.find("location_data.push( ") + 20
				info = ""
				while response.body[pos] != '}':
					if response.body[pos:pos+2] != "\'":
						info += response.body[pos]
					else:
						info += "'"
					pos += 1
				info += '}'
				return info.decode('utf8').replace("\'", "").replace('\t','').replace('\n','')
			except:
				return ""

		def getValue(self, info, property):
			try:
				pos = info.find(property + ":") + len(property) + 2
				value = ""
				while info[pos] != ",":
					value += info[pos]
					pos += 1
				return value
			except:
				return ""

		def getSpecificValue(self, info, property):
			try:
				pos = info.find(property) + len(property) + 3
				value = ""
				while info[pos:pos+2] != "</":
					value += info[pos]
					pos += 1
				return value.strip()
			except:
				return ""