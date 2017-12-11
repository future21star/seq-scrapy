import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class AmericanSignatureFurnitureSpider(scrapy.Spider):
	name = "americansignaturefurniture"
	uid_list = []
	start_urls = ["https://www.americansignaturefurniture.com/store-locator/show-all-locations"]
	start_urls_ = ["https://www.americansignaturefurniture.com/store-locator/show-all-locations"]		
	def parse(self, response):
		try:
			stores = response.xpath('//div[@class="store-locator-stores-result-list"]/div')
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store.xpath('.//strong[@class="sl-storename"]//text()'))
				item['store_number'] = ""
				item['address'] = self.validate(store.xpath('.//span[@itemprop="streetAddress"]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('.//span[@itemprop="addressLocality"]/text()'))
				item['state'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"]/text()'))
				item['zip_code'] = self.validate(store.xpath('.//span[@itemprop="postalCode"]/text()'))
				item['phone_number'] = self.validate(store.xpath('.//span[@itemprop="telephone"]/text()'))
				item['country'] = "United States"
				item['latitude'] = ""
				item['longitude'] = ""
				item['store_hours'] = ""
				hours = store.xpath('.//div[@class="store-hours-table"]/ul')
				for hour in hours:
					item['store_hours'] += self.validate(hour.xpath('./li[1]/text()')) + ":" + self.validate(hour.xpath('./li[2]/time/text()')) + ";"
				item['other_fields'] = ""
				item['coming_soon'] = 0
				if item['phone_number'] == "" or item['phone_number'] in self.uid_list:
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

		import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class AmericanSignatureFurnitureSpider(scrapy.Spider):
	name = "americansignaturefurniture"
	uid_list = []
	start_urls = ["https://www.americansignaturefurniture.com/store-locator/show-all-locations"]
	start_urls_ = ["https://www.americansignaturefurniture.com/store-locator/show-all-locations"]		
	def parse(self, response):
		try:
			stores = response.xpath('//div[@class="store-locator-stores-result-list"]/div')
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store.xpath('.//strong[@class="sl-storename"]//text()'))
				item['store_number'] = ""
				item['address'] = self.validate(store.xpath('.//span[@itemprop="streetAddress"]/text()'))
				item['address2'] = ""
				item['city'] = self.validate(store.xpath('.//span[@itemprop="addressLocality"]/text()'))
				item['state'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"]/text()'))
				item['zip_code'] = self.validate(store.xpath('.//span[@itemprop="postalCode"]/text()'))
				item['phone_number'] = self.validate(store.xpath('.//span[@itemprop="telephone"]/text()'))
				item['country'] = "United States"
				item['latitude'] = ""
				item['longitude'] = ""
				item['store_hours'] = ""
				hours = store.xpath('.//div[@class="store-hours-table"]/ul')
				for hour in hours:
					item['store_hours'] += self.validate(hour.xpath('./li[1]/text()')) + ":" + self.validate(hour.xpath('./li[2]/time/text()')) + ";"
				item['other_fields'] = ""
				item['coming_soon'] = 0
				if item['phone_number'] == "" or item['phone_number'] in self.uid_list:
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
