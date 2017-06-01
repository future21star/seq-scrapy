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
import yaml
class TitlenineSpider(scrapy.Spider):
		name = "titlenine"
		uid_list = []
		start_urls = ["https://www.titlenine.com/store-locator/all-stores.do"]
		domain = "https://www.titlenine.com"

		def parse(self, response):
			try:
				stores = response.xpath('//div[@class="eslStore ml-storelocator-headertext"]/a/@href').extract()
				for store in stores:
					url = self.domain + store
					yield scrapy.Request(url, callback=self.parse_store)
			except:
				pdb.set_trace()
				pass

		def parse_store(self, response):
			try:
				store = response
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = self.validate(store.xpath('//div[@class="eslStore"]/text()'))
				item['address'] = self.validate(store.xpath('//div[@class="eslAddress1"]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('//span[@class="eslCity"]/text()')).replace(',', '')
				item['state'] = self.validate(store.xpath('//span[@class="eslStateCode"]/text()'))
				item['zip_code'] = self.validate(store.xpath('//span[@class="eslPostalCode"]/text()'))
				item['country'] = "United States" 
				item['phone_number'] = self.validate(store.xpath('//div[@class="eslPhone"]/text()'))
				hours = store.xpath('//span[@class="ml-storelocator-hours-details"]/text()').extract()
				hours = [a.strip() for a in hours if a.strip() != ""]
				item['store_hours'] = ";".join(hours)
				lat_lng = response.body
				item['latitude'] = lat_lng.split('"latitude":')[1].split(',')[0].strip()
				item['longitude'] = lat_lng.split('"longitude":')[1].split('}')[0].strip()
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
			except:
				pdb.set_trace()
				pass			

		def validate(self, xpath):
			try:
				return self.replaceUnknownLetter(xpath.extract_first().strip())
			except:
				return ""

		def replaceUnknownLetter(self, source):
			try:
				formatted_value = source.encode('utf8').replace('\xc3', '').replace('\xa9', 'e').replace('\xa8', 'e').replace('\xb4', 'o').replace('\xb3', 'o').replace('\xb9', 'u').replace('\xba', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
				# if "x8" in formatted_value or "x9" in formatted_value or "xa" in formatted_value or "xb" in formatted_value:
				# 	pdb.set_trace()
				return formatted_value
			except:
				return source
		def format(self, item):
			try:
				return unicodedata.normalize('NFKD', item).encode('ascii','ignore').strip()
			except:
				return ''			




