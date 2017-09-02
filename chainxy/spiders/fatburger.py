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

class FatburgerSpider(scrapy.Spider):
		name = "fatburgers"
		uid_list = []
		start_urls = ['https://www.fatburger.com/domestic']
		count = []

		def parse(self, response):
			for url in response.xpath('//a[contains(@href, "https://www.fatburger.com/locations/")]'):
				extracted_url = url.xpath('./@href').extract_first()
				item = ChainItem()
				# if extracted_url == "https://www.fatburger.com/locations/torrance":
				# 	pdb.set_trace()
				if extracted_url == "https://www.fatburger.com/locations/venice":
					item['state'] = "CA"
					item['city'] = "Los Angeles"
				else:
					item['state'] = self.validateState(url.xpath('./text()').extract_first().split(',')[-1].strip())
					item['city'] = self.getCity(url.xpath('./text()').extract_first().split(',')[0]).strip()
				request = scrapy.Request(url=extracted_url, callback=self.parse_store)
				request.meta['item'] = item
 				yield request

		def parse_store(self, response):
			temp = response.xpath('//div[@class="sqs-block-content"][1]//text()').extract()
			temp = filter(lambda a: a.strip()!= "" and a.strip() != "Menu", temp)
			item = response.meta['item']
			item['store_number'] = ""
			item['store_name'] = temp[0]	
			store_hour_index = 4
			if self.isPhoneNumber(temp[2]):
				address = temp[1]
				item['phone_number'] = temp[2]
				store_hour_index = 4
			else: 				
				address = temp[1] + " , " + temp[2]
				item['phone_number'] = temp[3]
				store_hour_index = 5
			item['address'] = address.split(',')[0].strip()
			item['phone_number'] = item['phone_number'].replace('.', '-').split(":")[-1].strip()
			item['address2'] = ""
			item['zip_code'] = address.split(',')[-1].strip().split()[-1]
			item['country'] = "United States" 
			item['store_hours'] = ""
			while self.hasNumber(temp[store_hour_index]):
				item['store_hours'] += temp[store_hour_index] + ";"
				store_hour_index += 1			
			item['latitude'] = response.xpath('//meta[@property="og:latitude"]/@content').extract_first()
			item['longitude'] = response.xpath('//meta[@property="og:longitude"]/@content').extract_first()
			#item['store_type'] = info_json["@type"]
			if item['state'] == 'CA':
				self.count.append(item["city"])
			print "pp"
			print self.count
			item['other_fields'] = ""
			item['coming_soon'] = 0
			yield item

		def validate(self, xpath):
			try:
				return self.replaceUnknownLetter(xpath.extract_first().strip())
			except:
				return ""

		def replaceUnknownLetter(self, source):
			try:
				formatted_value = source.encode('utf8').replace('\xc3', '').replace('\xa9', 'e').replace('\xa8', 'e').replace('\xb4', 'o').replace('\xb3', 'o').replace('\xb9', 'u').replace('\xba', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
				return formatted_value
			except:
				return source
		def format(self, item):
			try:
				return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
			except:
				return ''			

		def isPhoneNumber(self, str):
			str = str.replace('(', '').replace(')', '').replace('-', '').replace('-', '').replace(' ','').replace('.', '').strip()
			count = 0
			for char in str:
				if not char.isdigit():
					return False
			return True

		def hasNumber(self, str):
			for char in str:
				if char.isdigit():
					return True
			return False

		def getCity(self, str):
			try:
				city = ""
				if ('(' in str):
					pos = str.find('(') + 1
					while (str[pos] != ')' and str[pos] != ','):
						city += str[pos]
						pos += 1
				else:
					city = str
				return city
			except:
				return str

		def validateState(self, state):
			try:
				if ('(' in state):
					start = state.find('(')
					end = state.find(')') + 1
					return state.replace(state[start:end], "").strip()
				return state
			except:
				return state