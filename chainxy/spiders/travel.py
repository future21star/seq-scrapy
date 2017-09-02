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

class TravelSpider(scrapy.Spider):
		name = "travel"
		uid_list = []
		start_urls = ['http://marriotthotelapi.netlinkrg.com/api/hotels?latitude=38.2172124&longitude=-85.42724020000003&max_distance=300000&brand=SHS']
		count = 0

		def parse(self, response):
			try:
				stores = json.loads(response.body)
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = store['hotel_name']
					item['address'] = store['address_line']
					item['address2'] = ""
					item['city'] = store['city_name']
					item['state'] = store['state_prov_code']
					item['zip_code'] = store['postal_code']
					item['country'] = "United States" 
					item['phone_number'] = store['phone']
					item['store_hours'] = ""
					item['latitude'] = store['latitude']
					item['longitude'] = store['longitude']
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					yield item
			except:
				pass			

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""

		def isNumber(self, number):
			count = 0
			for char in number:
				if char.isdigit():
					count += 1
			return count > 5

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