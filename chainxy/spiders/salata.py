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

class SalataSpider(scrapy.Spider):
		name = "salata"
		uid_list = []
		start_urls = ['http://www.salata.com/locations']
		count = 0

		def parse(self, response):
			try:
				stores = response.xpath('//div[contains(@class,"loc-wrapper neutra linen-light")]')
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = self.validate(store.xpath('.//div[@class="loc-info-name"]/span/text()'))
					addr = store.xpath('.//div[@class="loc-info-address"]/text()').extract()
					item['address'] = addr[0].strip()
					item['address2'] = ""
					item['city'] = store.xpath('./@data-city').extract_first()
					item['state'] = store.xpath('./@data-state').extract_first()
					item['zip_code'] = store.xpath('./@data-zip').extract_first()
					item['country'] = "United States" 
					item['phone_number'] = store.xpath('.//div[@class="loc-info-phone"]/text()').extract()[-1]
					item['store_hours'] = self.validate(store.xpath('.//div[@class="loc-hours-times"]/text()'))
					if (len(store.xpath('./@data-loc-guid')) > 0 and 'coming soon' in store.xpath('./@data-loc-guid').extract_first()) or ('Coming Soon' in item['phone_number']) or ('Coming Soon' in item['store_hours']):
						item['coming_soon'] = 1
					else:
						item['coming_soon'] = 0
					item['phone_number'] = item['phone_number'].replace('Coming Soon!', '')
					item['store_hours'] = item['store_hours'].replace('Coming Soon!', '')
					item['latitude'] = store.xpath('./@data-lat').extract_first()
					item['longitude'] = store.xpath('./@data-lng').extract_first()
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					yield item
			except:
				pdb.set_trace()
				pass			

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""
