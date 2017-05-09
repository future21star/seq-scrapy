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

class HavertysSpider(scrapy.Spider):
		name = "havertys"
		uid_list = []
		start_urls = ['https://www.havertys.com/furniture/allstores']
		count = 0

		def parse(self, response):
			try:
				stores = response.xpath('//li[@class="storeListEntry"]')
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = self.validate(store.xpath('.//div[@class="storeName"]/text()'))
					details = store.xpath('.//span[@class="storeDetails"]/span/text()').extract()
					item['address'] = details[0]
					item['address2'] = ""
					item['city'] = details[1].split(',')[0].strip()
					item['state'] = details[1].split(',')[1].split()[0]
					item['zip_code'] = details[1].split(',')[1].split()[1]
					item['country'] = "United States" 
					item['phone_number'] = details[2]
					if "Coming Soon" in details[3]:
						item['store_hours'] = ""
						item['coming_soon'] = 1
					else:
						item['store_hours'] = details[3] + ";" + details[4]
						item['coming_soon'] = 0
					lat_lng = store.xpath('.//a[contains(@href, "https://maps.google.com?daddr=")]/@href').extract_first()
					item['latitude'] = lat_lng.split("=")[-1].split(',')[0]
					item['longitude'] = lat_lng.split("=")[-1].split(',')[1]
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