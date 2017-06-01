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
class PearlevisionSpider(scrapy.Spider):
		name = "pearlevision"
		uid_list = []

		def __init__(self):
			place_file = open('cities_us.json', 'rb')
			self.place_reader = json.load(place_file)

		def start_requests(self):
			for info in self.place_reader:
				city = info['city'].replace(" ", "%20")
				url = "http://www.pearlevision.com/webapp/wcs/stores/servlet/AjaxStoreLocatorResultsView?storeId=12002&catalogId=15951&langId=-1&resultSize=502&latitude=%s&longitude=%s&location=%s" % (info['latitude'], info['longitude'], info['city'].replace(' ','+'))
				yield scrapy.Request(url=url, callback=self.parse)
			
		def parse(self, response):
			try:
				stores = response.xpath("//td[@style='display:none']")
				for store in stores:
					item = ChainItem()
					item['store_number'] = self.validate(store.xpath('.//span[@class="storeNumber"]/text()'))
					item['store_name'] = self.validate(store.xpath('.//span[@class="storeName"]/text()'))
					item['address'] = self.validate(store.xpath('.//span[@class="address"]/text()'))
					item['address2'] = ""
					item['city'] = self.validate(store.xpath('.//span[@class="city"]/text()'))
					item['state'] = self.validate(store.xpath('.//span[@class="state"]/text()'))
					item['zip_code'] = self.validate(store.xpath('.//span[@class="zipCode"]/text()'))
					item['country'] = "United States" 
					item['phone_number'] = self.validate(store.xpath('.//span[@class="phone"]/text()'))
					item['store_hours'] = self.validate(store.xpath('.//span[@class="hours"]/text()'))
					item['latitude'] = self.validate(store.xpath('.//span[@class="latitude"]/text()'))
					item['longitude'] = self.validate(store.xpath('.//span[@class="longitude"]/text()'))
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					yield item
			except:
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




