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

class CapitoldentalcareSpider(scrapy.Spider):
		name = "capitoldentalcare"
		uid_list = []
		start_urls = ['http://capitoldentalcare.com/members/find-a-dentist/']
		count = 0

		def parse(self, response):
			try:
				cities = response.xpath('//a[contains(@href, "http://capitoldentalcare.com/members/search-results")]')
				for city in cities:
					url = city.xpath('./@href').extract_first()
					city_name = city.xpath('./text()').extract_first()
					request = scrapy.Request(url=url, callback=self.parse_store)
					request.meta['city'] = city_name
					yield request
			except:
				pass

		def parse_store(self, response):
			try:

				stores = response.xpath('//div[contains(@class, "result_box")]')
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = self.validate(store.xpath('./h2[@class="result_title"]/text()'))
					addr = store.xpath('.//div[@class="result_contents"]/text()').extract()
					addr = [a.strip() for a in addr if a.strip() != ""]
					item['address'] = addr[-3].strip()
					item['address2'] = ""
					item['city'] = addr[-2].split(',')[0].strip()
					item['state'] = "OR"
					item['zip_code'] = addr[-2].split(',')[-1].strip()
					item['country'] = "United States" 
					item['phone_number'] = addr[-1].replace('Referral Required', '').strip()
					item['store_hours'] = ""
					item['latitude'] = ""
					item['longitude'] = ""
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					if item['store_name'] != "" and item['store_name'] in self.uid_list:
						continue
					self.uid_list.append(item['store_name'])
					if item['phone_number'] != "" and item['phone_number'] in self.uid_list:
						continue
					self.uid_list.append(item['phone_number'])
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