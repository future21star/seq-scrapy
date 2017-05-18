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

class RogerdunnSpider(scrapy.Spider):
		name = "rogerdunn"
		uid_list = []
		start_urls = ['http://www.worldwidegolfshops.com/assets/images/xml/stores.xml']

		def parse(self, response):
			for store in response.xpath('//store'):
					item = ChainItem()
					item['store_number'] = self.validate(store.xpath('./@ID')).replace("HUNTS", "")
					item['store_name'] = self.validate(store.xpath('./name/text()'))
					addr = store.xpath('//div[@class="address"]/text()').extract()
					item['address'] = self.validate(store.xpath('./address/street/text()'))
					item['address2'] = ""
					item['city'] = self.validate(store.xpath('./address/city/text()'))
					item['state'] = self.validate(store.xpath('./address/state/text()'))
					item['zip_code'] = self.validate(store.xpath('./address/zip/text()'))
					item['latitude'] = self.validate(store.xpath('./address/lat/text()'))
					item['longitude'] = self.validate(store.xpath('./address/lng/text()'))
					item['country'] = "United States" 
					item['phone_number'] = self.validate(store.xpath('./phone/text()'))
					hours = store.xpath('./hours//text()').extract()
					hours = [a.strip() for a in hours if a.strip() != ""]
					item['store_hours'] = "weekday:" + hours[0] + ";" + "sat:" + hours[1] + ";" + "sun:" + hours[0] + ";"
					#item['store_type'] = info_json["@type"]
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




