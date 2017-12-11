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

class BuddysSpider(scrapy.Spider):
		name = "buddys"
		uid_list = []
		start_urls = ['https://www.buddyrents.com/storelocator/storelocator_data.php?origLat=37.09024&origLng=-95.712891&origAddress=5000+Estate+Enighed%2C+Independence%2C+KS+67301%2C+USA&formattedAddress=&boundsNorthEast=&boundsSouthWest=']
		count = 0

		def parse(self, response):
			try:
				stores = json.loads(response.body)
				for store in stores:
					item = ChainItem()
					item['store_number'] = store['id']
					item['store_name'] = store['name']
					item['address'] = store['address']
					item['address2'] = store['address2']
					item['city'] = store['city']
					item['state'] = store['state']
					item['zip_code'] = store['postal']
					item['country'] = "United States" 
					item['phone_number'] = store['phone']
					hours = store['hours1'] + ";" + store['hours2'] + ";" + store['hours3'] + ";"
					store['hours'] = hours.replace('COMING SOON:', '').strip()
					item['latitude'] = store['lat']
					item['longitude'] = store['lng']
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					if 'COMING SOON' in hours:
						item['coming_soon'] = 1
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

class BuddysSpider(scrapy.Spider):
		name = "buddys"
		uid_list = []
		start_urls = ['https://www.buddyrents.com/storelocator/storelocator_data.php?origLat=37.09024&origLng=-95.712891&origAddress=5000+Estate+Enighed%2C+Independence%2C+KS+67301%2C+USA&formattedAddress=&boundsNorthEast=&boundsSouthWest=']
		count = 0

		def parse(self, response):
			try:
				stores = json.loads(response.body)
				for store in stores:
					item = ChainItem()
					item['store_number'] = store['id']
					item['store_name'] = store['name']
					item['address'] = store['address']
					item['address2'] = store['address2']
					item['city'] = store['city']
					item['state'] = store['state']
					item['zip_code'] = store['postal']
					item['country'] = "United States" 
					item['phone_number'] = store['phone']
					hours = store['hours1'] + ";" + store['hours2'] + ";" + store['hours3'] + ";"
					store['hours'] = hours.replace('COMING SOON:', '').strip()
					item['latitude'] = store['lat']
					item['longitude'] = store['lng']
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					if 'COMING SOON' in hours:
						item['coming_soon'] = 1
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
