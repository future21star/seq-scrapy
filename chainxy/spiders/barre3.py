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

class Barre3Spider(scrapy.Spider):
		name = "barre3"
		uid_list = []
		start_urls = ['http://barre3.com/studio-locations']
		domain = "http://barre3.com"

		def parse(self, response):
			try:
				for url in response.xpath('//li[@class="studio-listing-item"]/a/@href').extract():
					yield scrapy.Request(url=self.domain+url, callback=self.parse_store)
	 		except:
	 			pass

		def parse_store(self, response):
			try:
				info = self.getInfo(response)
				item = ChainItem()
				item['store_number'] = ""
				item['store_number'] = ""				
				item['store_name'] = ""
				item['address'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][1]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[0].strip()
				add = item['state'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()
				try:
					item['state'] = " ".join(self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()[:-1])
				except:
					item['state'] = ""
				try:
					item['zip_code'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()[-1]
				except:
					item['zip_code'] = ""
				item['country'] = "United States" 
				item['phone_number'] = self.validate(response.xpath('//li[@class="text-header--sub studio-contact-info"][1]/text()'))
				item['store_hours'] = ""
				item['latitude'] = self.getValue(info, "lat")
				item['longitude'] = self.getValue(info, "long")
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				if 'coming soon' in self.validate(response.xpath('//h2[@class="h2 text-script--large"]/text()')):
					item['coming_soon'] = 1
				else:
					item['coming_soon'] = 0
				if self.isZipCode(item['zip_code']):
					yield item
			except:
				pdb.set_trace()
				pass			
		def parse_stores_first(self, response):
			try:
				info = self.getInfo(response)
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = ""
				item['address'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][1]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[0].strip()
				add = item['state'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()
				try:
					item['state'] = " ".join(self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()[:-1])
				except:
					item['state'] = ""
				try:
					item['zip_code'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()[-1]
				except:
					item['zip_code'] = ""
				item['country'] = "United States" 
				item['phone_number'] = self.validate(response.xpath('//li[@class="text-header--sub studio-contact-info"][1]/text()'))
				item['store_hours'] = ""
				item['latitude'] = self.getValue(info, "lat")
				item['longitude'] = self.getValue(info, "long")
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				if 'coming soon' in self.validate(response.xpath('//h2[@class="h2 text-script--large"]/text()')):
					item['coming_soon'] = 1
				else:
					item['coming_soon'] = 0
				if self.isZipCode(item['zip_code']):
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

		def isZipCode(self, zip_code):
			count = 0
			for str in zip_code:
				if str.isdigit():
					count += 1
			return count > 4

		
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

class Barre3Spider(scrapy.Spider):
		name = "barre3"
		uid_list = []
		start_urls = ['http://barre3.com/studio-locations']
		domain = "http://barre3.com"

		def parse(self, response):
			try:
				for url in response.xpath('//li[@class="studio-listing-item"]/a/@href').extract():
					yield scrapy.Request(url=self.domain+url, callback=self.parse_store)
	 		except:
	 			pass

		def parse_store(self, response):
			try:
				info = self.getInfo(response)
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = ""
				item['address'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][1]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[0].strip()
				add = item['state'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()
				try:
					item['state'] = " ".join(self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()[:-1])
				except:
					item['state'] = ""
				try:
					item['zip_code'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()[-1]
				except:
					item['zip_code'] = ""
				item['country'] = "United States" 
				item['phone_number'] = self.validate(response.xpath('//li[@class="text-header--sub studio-contact-info"][1]/text()'))
				item['store_hours'] = ""
				item['latitude'] = self.getValue(info, "lat")
				item['longitude'] = self.getValue(info, "long")
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				if 'coming soon' in self.validate(response.xpath('//h2[@class="h2 text-script--large"]/text()')):
					item['coming_soon'] = 1
				else:
					item['coming_soon'] = 0
				if self.isZipCode(item['zip_code']):
					yield item
			except:
				pdb.set_trace()
				pass			
		def parse_stores_first(self, response):
			try:
				info = self.getInfo(response)
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = ""
				item['address'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][1]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[0].strip()
				add = item['state'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()
				try:
					item['state'] = " ".join(self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()[:-1])
				except:
					item['state'] = ""
				try:
					item['zip_code'] = self.validate(response.xpath('//span[@class="text-header--sub studio-contact-info"][2]/text()')).split(',')[1].split()[-1]
				except:
					item['zip_code'] = ""
				item['country'] = "United States" 
				item['phone_number'] = self.validate(response.xpath('//li[@class="text-header--sub studio-contact-info"][1]/text()'))
				item['store_hours'] = ""
				item['latitude'] = self.getValue(info, "lat")
				item['longitude'] = self.getValue(info, "long")
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				if 'coming soon' in self.validate(response.xpath('//h2[@class="h2 text-script--large"]/text()')):
					item['coming_soon'] = 1
				else:
					item['coming_soon'] = 0
				if self.isZipCode(item['zip_code']):
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

		def isZipCode(self, zip_code):
			count = 0
			for str in zip_code:
				if str.isdigit():
					count += 1
			return count > 4
		
