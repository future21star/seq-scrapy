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

class SeriouscoffeeSpider(scrapy.Spider):
		name = "seriouscoffee"
		uid_list = []
		start_urls = ['http://www.seriouscoffee.com/locations/']
		count = 0
		domain = "http://www.seriouscoffee.com"

		def parse(self, response):
			stores = response.xpath('//div[@class="fusion-submenu-wrapper level2 columns4"]/ul/li//ol/li/a')
			for store in stores:
				url = self.domain + store.xpath('./@href').extract_first()
				yield scrapy.Request(url=url, callback=self.parse_store)

		def parse_store(self, response):
			item = ChainItem()
			item['store_number'] = ""
			item['store_name'] = self.validate(response.xpath('//h1[@class="cms_locations_heading"]/text()'))
			addr = response.xpath('//div[@class="location_address"]/text()').extract()
			item['address'] = " ".join(addr[:-2]).strip()
			item['address2'] = ""
			item['city'] = addr[-2].split(',')[0].strip()
			item['state'] = addr[-2].split(',')[1].strip()
			item['zip_code'] = addr[-1].strip()
			item['country'] = "Canada" 
			item['phone_number'] = self.validate(response.xpath('//div[@class="location_contact"]/text()'))
			hours = response.xpath('//table[@class="locations_timetable_table"]/tr')
			item['store_hours'] = ""
			for hour in hours:
				item['store_hours'] += ":".join(hour.xpath('.//text()').extract()) + ";"
			item['latitude'] = ""
			item['longitude'] = ""
			if response.body.find("var latitude =") > -1:
				pos = response.body.find("var latitude =") + 14
				lat_lng = response.body
				item['latitude'] = ""
				while lat_lng[pos] != ";":
					item['latitude'] += lat_lng[pos]
					pos += 1
				item['latitude'] = item['latitude'].strip()
				pos = response.body.find("var longitude  =") + 16
				item['longitude'] = ""
				while lat_lng[pos] != ";":
					item['longitude'] += lat_lng[pos]
					pos += 1			
			#item['store_type'] = info_json["@type"]
			item['coming_soon'] = 0
			item['other_fields'] = ""
			yield item	

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""
