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

class MrheroSpider(scrapy.Spider):
		name = "mrhero"
		uid_list = []
		start_urls = ['https://www.mrhero.com/locations_county.php']
		count = 0

		def parse(self, response):
			try:
				stores = response.xpath('//table[1]/tr')
				for store in stores:
					if stores.index(store) > 0:
						item = ChainItem()
						item['store_number'] = ""
						item['store_name'] = "Mr.Hero"
						item['address'] = self.validate(store.xpath('.//input[@name="address"]/@value'))
						item['address2'] = ""
						item['city'] = self.validate(store.xpath('.//input[@name="city"]/@value'))
						item['state'] = self.validate(store.xpath('.//input[@name="state"]/@value'))
						item['zip_code'] = self.validate(store.xpath('.//input[@name="zippy"]/@value'))
						item['country'] = "United States" 
						if self.isPhoneNumber(store.xpath('./td[1]/text()').extract()[-1]):
							item['phone_number'] = store.xpath('./td[1]/text()').extract()[-1]
						else:
							item['phone_number'] = ""
						item['store_hours'] = ""
						item['latitude'] = ""
						item['longitude'] = ""
						#item['store_type'] = info_json["@type"]
						item['other_fields'] = ""
						item['coming_soon'] = 0
						yield item
			except:
				pdb.set_trace()
				pass			

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""

		def isPhoneNumber(self, str):
			str = str.replace('(', '').replace(')', '').replace('-', '').replace('-', '').replace(' ','').replace('.', '').strip()
			count = 0
			for char in str:
				if not char.isdigit():
					return False
			return True
