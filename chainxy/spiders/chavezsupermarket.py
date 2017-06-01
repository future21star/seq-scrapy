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

class ChavezsupermarketSpider(scrapy.Spider):
		name = "chavezsupermarket"
		uid_list = []
		start_urls = ['http://www.chavezsuper.com/locations.html']
		count = 0

		def parse(self, response):
			try:
				stores = response.xpath('//span[@class="addresstxt"]')
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = ""
					addr = store.xpath('./text()').extract()
					addr = [a.strip() for a in addr if a.strip() != ""]
					item['address'] = addr[0].strip()
					item['address2'] = ""
					item['city'] = addr[1].split(',')[0].strip()
					item['state'] = addr[1].split(',')[1].split()[0].strip().replace('.', '')
					item['zip_code'] = addr[1].split(',')[1].split()[-1].strip()
					item['country'] = "United States" 
					item['phone_number'] = addr[2].strip().split('Tel:')[-1].strip()
					item['store_hours'] = store.xpath('./span[@class="locationsgreentext"]/text()').extract_first().split('Store Hours:')[-1].strip()
					item['latitude'] = ""
					item['longitude'] = ""
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