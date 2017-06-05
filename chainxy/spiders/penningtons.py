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
from lxml import etree

class PenningtonsSpider(scrapy.Spider):
		name = "penningtons"
		uid_list = []
		start_urls = ['http://www.penningtons.com/on/demandware.store/Sites-Penningtons_CA-Site/default/Stores-Find']
		count = 0

		def parse(self, response):
			try:
				states = response.xpath('//select[@class="input-select  storeLocatorProvince required"]/option')
				for state in states:
					state = self.validate(state.xpath('./@value'))
					url = "http://www.penningtons.com/on/demandware.store/Sites-Penningtons_CA-Site/default/ShipToStore-AssignProvince?province=%s&src=storelocator" % state
					yield scrapy.Request(url=url, callback=self.parse_store)
			except:
				pass

		def parse_store(self, response):
			try:
				stores = json.loads(response.body)['resultdata']['stores']
				for store in stores:
					item = ChainItem()
					item['store_number'] = store['ID']
					item['store_name'] = store['name']
					item['address'] = store['address1']
					item['address2'] = ""
					item['city'] = store['city']
					item['state'] = store['stateCode']
					item['zip_code'] = store['postalCode']
					item['country'] = "Canada" 
					item['phone_number'] = store['phone']
					hours = etree.HTML(store['storeHours'])
					hours = hours.xpath('.//text()')
					store['hours'] = "".join(hours[1:]).replace('\n', ';')
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