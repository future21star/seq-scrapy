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

class JugojuiceSpider(scrapy.Spider):
		name = "jugojuice"
		uid_list = []
		start_urls = ['https://www.jugojuice.com/locations/list/']
		count = 0

		def parse(self, response):
			try:
				stores = response.xpath('//article[@class="location"]')
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = self.validate(store.xpath('.//h3[@itemprop="name"]/text()'))
					item['address'] = self.validate(store.xpath('.//span[@itemprop="streetAddress"]/text()'))
					item['address2'] = ""
					item['city'] = self.validate(store.xpath('.//span[@itemprop="addressLocality"]/text()'))
					item['state'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"][1]/text()'))
					item['zip_code'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"][2]/text()'))
					item['country'] = "United States" 
					item['phone_number'] = self.validate(store.xpath('.//div[@itemprop="telephone"]/text()'))
					hours =  store.xpath('.//div[@class="hours"]/p[2]//text()').extract()
					for hour in hours:
						hours[hours.index(hour)] = hour.strip()
					item['store_hours'] = ";".join(hours)
					src = self.validate(store.xpath('.//img[contains(@src, "maps.googleapis.com/maps/api/staticmap")]/@src'))
					pos = src.find("center=") + 7
					item['latitude'] = ""
					item['longitude'] = ""
					while src[pos] != ',':
						item['latitude'] += src[pos]
						pos += 1
					item['latitude'] = item['latitude'].strip()
					pos += 1
					while src[pos] != '&':
						item['longitude'] += src[pos]
						pos += 1
					item['longitude'] = item['longitude'].strip()
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
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