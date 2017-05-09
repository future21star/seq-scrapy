import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class AnthonyscoalfiredSpider(scrapy.Spider):
	name = "anthonyscoalfired"
	uid_list = []
	start_urls = ["https://acfp.com/locations/"]
		
	count = dict()
	def parse(self, response):
		try:
			store_urls = response.xpath('//li[contains(@class, "menu-item-object-acfp_location_state")]')
			for store in store_urls:
				url = store.xpath('./a/@href').extract_first()	
				yield scrapy.Request(url = url, callback=self.parse_store)
		except:
			pdb.set_trace()
			pass

	def parse_store(self, response):
		try:
			stores = response.xpath('//div[@class="inside"]/div[@class="a-location"]')
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store.xpath('.//div[@class="name"]/text()'))
				item['store_number'] = ""
				item['address'] = store.xpath('.//div[@class="address"]/p/text()').extract_first()
				item['address2'] = ""
				address_parse = store.xpath('.//div[@class="address"]/p/text()').extract()[1] 
				if 'Suite' in address_parse:
					address_parse = store.xpath('.//div[@class="address"]/p/text()').extract()[2] 
				item['city'] = address_parse.strip().split(',')[0].strip()
				item['state'] = address_parse.strip().split(',')[1].split()[0]
				item['zip_code'] = address_parse.strip().split(',')[1].split()[1]
				item['phone_number'] = store.xpath('.//a[@class="phone"]/text()').extract_first()
				item['country'] = "United States"
				item['latitude'] = store.xpath('.//a[@class="directions"]/@href').extract_first().split('/')[-1][1:-1].split(',')[0]
				item['longitude'] = store.xpath('.//a[@class="directions"]/@href').extract_first().split('/')[-1][1:-1].split(',')[1]
				item['store_hours'] = ""
				if self.validate_with_index(store.xpath('.//div[@class="hours"]//text()'), 4) != "":
					item['store_hours'] = self.validate_with_index(store.xpath('.//div[@class="hours"]//text()'), 4) + self.validate_with_index(store.xpath('.//div[@class="hours"]//text()'),5) + ";"
				if self.validate_with_index(store.xpath('.//div[@class="hours"]//text()'),7) != "":
					item['store_hours'] += self.validate_with_index(store.xpath('.//div[@class="hours"]//text()'),7) + self.validate_with_index(store.xpath('.//div[@class="hours"]//text()'), 8) + ";" 
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

	def validate_with_index(self, xpath, index):
		try:
			return xpath.extract()[index]
		except:
			return ""