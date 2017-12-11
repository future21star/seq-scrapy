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

class AndpizzaSpider(scrapy.Spider):
		name = "andpizza"
		uid_list = []
		start_urls = ['https://andpizza.com/']
		count = 0
		domain = "http://www.thecapitalgrille.com"

		def parse(self, response):
			try:
				for store1 in response.xpath('//div[@class="locationHolder expandable"]/div[contains(@class, "location")]'):
					if store1.xpath("./@class").extract_first() == "airport-locations grid-100":
						for store2 in store1.xpath('./div[contains(@class,"location")]'):
							store = store2
							item = ChainItem()
							item['store_number'] = ""
							item['store_name'] = ""
							address = store.xpath('.//address//text()').extract()
							item['address'] = address[0]
							item['address2'] = ""
							if len(address) > 2:
								item['city'] = address[-2].split(',')[0].strip()
								item['state'] = address[-2].split(',')[1].split()[0].strip()
								item['zip_code'] = address[-2].split(',')[1].split()[1].strip()
								item['country'] = "United States" 
								item['phone_number'] = address[-1].replace('.', '-')
							else:
								item['city'] = address[-1].split(',')[0].strip()
								item['state'] = address[-1].split(',')[1].split()[0].strip()
								item['zip_code'] = address[-1].split(',')[1].split()[1].strip()
								item['country'] = "United States" 
								item['phone_number'] = ""
							hours = store.xpath('.//div[@class="hours"]//text()').extract()
							item['store_hours'] = ""
							for hour in hours:
								if hours.index(hour) % 2 == 0:
									item['store_hours'] += hour + ":"
								else:
									item['store_hours'] += hour + ";"
								lat_lng = self.validate(store.xpath('.//li[@class="map"]/a/@href'))
							try:
								item['latitude'] = lat_lng.split('/')[-2].split(',')[0][1:]
								item['longitude'] = lat_lng.split('/')[-2].split(',')[1]
							except:
								try:
									pos = lat_lng.find("sll=") + 4
									item['latitude'] = ""
									while lat_lng[pos] != ',':
										item['latitude'] += lat_lng[pos]
										pos += 1
									pos += 1
									item['longitude'] = ""
									while lat_lng[pos] != '&':
										item['longitude'] += lat_lng[pos]
										pos += 1
								except:
									item['latitude'] = ""
									item['longitude'] = ""
							#item['store_type'] = info_json["@type"]
							item['other_fields'] = ""
							item['coming_soon'] = 0
							if "Coming soon!" in self.validate(store.xpath('.//div[@class="hours"]/span/text()')):
								item['coming_soon'] = 1
								item['store_hours'] = ""
							yield item
					else:
						store = store1
						item = ChainItem()
						item['store_number'] = ""
						item['store_name'] = ""
						address = store.xpath('.//address//text()').extract()
						item['address'] = address[0]
						if item['address'] == "Concourse C, Gate C28":
							pdb.set_trace()
						item['address2'] = ""
						if len(address) > 2:
							item['city'] = address[-2].split(',')[0].strip()
							item['state'] = address[-2].split(',')[1].split()[0].strip()
							item['zip_code'] = address[-2].split(',')[1].split()[1].strip()
							item['country'] = "United States" 
							item['phone_number'] = address[-1].replace('.', '-')
						else:
							item['city'] = address[-1].split(',')[0].strip()
							item['state'] = address[-1].split(',')[1].split()[0].strip()
							item['zip_code'] = address[-1].split(',')[1].split()[1].strip()
							item['country'] = "United States" 
							item['phone_number'] = ""
							item['city1'] = item['state']
						hours = store.xpath('.//div[@class="hours"]//text()').extract()
						item['store_hours'] = ""
						for hour in hours:
							if hours.index(hour) % 2 == 0:
								item['store_hours'] += hour + ":"
							else:
								item['store_hours'] += hour + ";"
							lat_lng = self.validate(store.xpath('.//li[@class="map"]/a/@href'))
						try:
							item['latitude'] = lat_lng.split('/')[-2].split(',')[0][1:]
							item['longitude'] = lat_lng.split('/')[-2].split(',')[1]
						except:
							try:
								pos = lat_lng.find("sll=") + 4
								item['latitude'] = ""
								while lat_lng[pos] != ',':
									item['latitude'] += lat_lng[pos]
									pos += 1
								pos += 1
								item['longitude'] = ""
								while lat_lng[pos] != '&':
									item['longitude'] += lat_lng[pos]
									pos += 1
							except:
								item['latitude'] = ""
								item['longitude'] = ""
						#item['store_type'] = info_json["@type"]
						item['other_fields'] = ""
						item['coming_soon'] = 0
						if "Coming soon!" in self.validate(store.xpath('.//div[@class="hours"]/span/text()')):
							item['coming_soon'] = 1
							item['store_hours'] = ""
						yield item			
			except:
				pdb.set_trace()
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

class AndpizzaSpider(scrapy.Spider):
		name = "andpizza"
		uid_list = []
		start_urls = ['https://andpizza.com/']
		count = 0
		domain = "http://www.thecapitalgrille.com"

		def parse(self, response):
			try:
				for store1 in response.xpath('//div[@class="locationHolder expandable"]/div[contains(@class, "location")]'):
					if store1.xpath("./@class").extract_first() == "airport-locations grid-100":
						for store2 in store1.xpath('./div[contains(@class,"location")]'):
							store = store2
							item = ChainItem()
							item['store_number'] = ""
							item['store_name'] = ""
							address = store.xpath('.//address//text()').extract()
							item['address'] = address[0]
							item['address2'] = ""
							if len(address) > 2:
								item['city'] = address[-2].split(',')[0].strip()
								item['state'] = address[-2].split(',')[1].split()[0].strip()
								item['zip_code'] = address[-2].split(',')[1].split()[1].strip()
								item['country'] = "United States" 
								item['phone_number'] = address[-1].replace('.', '-')
							else:
								item['city'] = address[-1].split(',')[0].strip()
								item['state'] = address[-1].split(',')[1].split()[0].strip()
								item['zip_code'] = address[-1].split(',')[1].split()[1].strip()
								item['country'] = "United States" 
								item['phone_number'] = ""
							hours = store.xpath('.//div[@class="hours"]//text()').extract()
							item['store_hours'] = ""
							for hour in hours:
								if hours.index(hour) % 2 == 0:
									item['store_hours'] += hour + ":"
								else:
									item['store_hours'] += hour + ";"
								lat_lng = self.validate(store.xpath('.//li[@class="map"]/a/@href'))
							try:
								item['latitude'] = lat_lng.split('/')[-2].split(',')[0][1:]
								item['longitude'] = lat_lng.split('/')[-2].split(',')[1]
							except:
								try:
									pos = lat_lng.find("sll=") + 4
									item['latitude'] = ""
									while lat_lng[pos] != ',':
										item['latitude'] += lat_lng[pos]
										pos += 1
									pos += 1
									item['longitude'] = ""
									while lat_lng[pos] != '&':
										item['longitude'] += lat_lng[pos]
										pos += 1
								except:
									item['latitude'] = ""
									item['longitude'] = ""
							#item['store_type'] = info_json["@type"]
							item['other_fields'] = ""
							item['coming_soon'] = 0
							if "Coming soon!" in self.validate(store.xpath('.//div[@class="hours"]/span/text()')):
								item['coming_soon'] = 1
								item['store_hours'] = ""
							yield item
					else:
						store = store1
						item = ChainItem()
						item['store_number'] = ""
						item['store_name'] = ""
						address = store.xpath('.//address//text()').extract()
						item['address'] = address[0]
						if item['address'] == "Concourse C, Gate C28":
							pdb.set_trace()
						item['address2'] = ""
						if len(address) > 2:
							item['city'] = address[-2].split(',')[0].strip()
							item['state'] = address[-2].split(',')[1].split()[0].strip()
							item['zip_code'] = address[-2].split(',')[1].split()[1].strip()
							item['country'] = "United States" 
							item['phone_number'] = address[-1].replace('.', '-')
						else:
							item['city'] = address[-1].split(',')[0].strip()
							item['state'] = address[-1].split(',')[1].split()[0].strip()
							item['zip_code'] = address[-1].split(',')[1].split()[1].strip()
							item['country'] = "United States" 
							item['phone_number'] = ""
							item['city1'] = item['state']
						hours = store.xpath('.//div[@class="hours"]//text()').extract()
						item['store_hours'] = ""
						for hour in hours:
							if hours.index(hour) % 2 == 0:
								item['store_hours'] += hour + ":"
							else:
								item['store_hours'] += hour + ";"
							lat_lng = self.validate(store.xpath('.//li[@class="map"]/a/@href'))
						try:
							item['latitude'] = lat_lng.split('/')[-2].split(',')[0][1:]
							item['longitude'] = lat_lng.split('/')[-2].split(',')[1]
						except:
							try:
								pos = lat_lng.find("sll=") + 4
								item['latitude'] = ""
								while lat_lng[pos] != ',':
									item['latitude'] += lat_lng[pos]
									pos += 1
								pos += 1
								item['longitude'] = ""
								while lat_lng[pos] != '&':
									item['longitude'] += lat_lng[pos]
									pos += 1
							except:
								item['latitude'] = ""
								item['longitude'] = ""
						#item['store_type'] = info_json["@type"]
						item['other_fields'] = ""
						item['coming_soon'] = 0
						if "Coming soon!" in self.validate(store.xpath('.//div[@class="hours"]/span/text()')):
							item['coming_soon'] = 1
							item['store_hours'] = ""
						yield item			
			except:
				pdb.set_trace()
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
