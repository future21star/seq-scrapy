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

class JohnnybruscosSpider(scrapy.Spider):
		name = "johnnybruscos"
		uid_list = []
		start_urls = ['http://www.johnnybruscos.com/locations/locations-map/']
		count = 0
		domain = "http://www.johnnybruscos.com"

		def parse(self, response):
			try:
				for url in response.xpath('//div[@id="wpseo-storelocator-results"]//a/@href').extract():
					yield scrapy.Request(url=self.domain+url, callback=self.parse_store_url)
					# yield scrapy.Request(url="http://www.johnnybruscos.com/location/hickory-flat/", callback=self.parse_store)
	 		except:
	 			pass

	 	def parse_store_url(self, response):
	 		try:
		 		for store_url in response.xpath('//a[contains(@href, "http://www.johnnybruscos.com/location/")]/@href').extract():
		 			yield scrapy.Request(url=store_url, callback=self.parse_store)
		 	except:
		 		pass

		def parse_store(self, response):
			try:
				info = self.getInfo(response)
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = self.getValue(info, "name")
				item['address'] = self.getValue(info, "address")
				item['address2'] = ""
				item['city'] = self.getSpecificValue(info, "addressLocality")
				item['state'] = self.getSpecificValue(info, "addressRegion")
				item['zip_code'] = self.getSpecificValue(info, "postalCode")
				item['country'] = "United States" 
				item['phone_number'] = self.getValue(info, "phone").replace('.', '-')
				try:				
					hours = "".join(response.xpath('//div[@class="single-tab store-info"][1]/div[@class="info-section"][2]/text()').extract()).replace('\t','').replace('\n','').strip().split("  ")
					hours = filter(lambda a: a.strip()!= "", hours)
					item['store_hours'] = ";".join(hours)
				except:
					item['store_hours'] = ""
				item['latitude'] = self.getValue(info, "lat")
				item['longitude'] = self.getValue(info, "long")
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