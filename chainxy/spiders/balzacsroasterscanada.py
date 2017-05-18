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
from lxml import etree

class BalzacsroasterscanadaSpider(scrapy.Spider):
		name = "balzacsroasterscanada"
		uid_list = []
		start_urls = ['http://www.balzacs.com/locations/']
		domain = 'http://www.balzacs.com'

		def parse(self, response):
			stores = response.xpath('//ul[@class="sidebar-nav"]//a[contains(@href, "http://www.balzacs.com/locations/")]/@href').extract()
			for store in stores:
				yield scrapy.Request(url=store, callback=self.parse_store)
		def parse_store(self, response):
			try:
				item = ChainItem()
				store = response 
				item['store_number'] = ""
				item['store_name'] = self.validate(store.xpath('//span[@class="name"]/text()'))
				addr = store.xpath('//div[@class="td-inner"]/address[1]/text()').extract()
				item['address'] = self.validate(store.xpath('//span[@class="address"]/text()'))
				item['address2'] = ""
				addr = self.validate(store.xpath('//span[@class="postal"]/text()'))
				item['city'] = addr.split(',')[0].strip()
				item['state'] = addr.split(',')[1].strip()
				item['zip_code'] = addr.split(',')[2].strip()
				item['country'] = "Canada"
				item['phone_number'] = self.validate(store.xpath('//span[@class="phone"]/text()')).strip().replace(' ', '-')
				hours = store.xpath('//section[@id="cafe-info"]//table//td//text()').extract()
				hours = [a.strip() for a in hours if a.strip() != ""]
				item['store_hours'] = ""
				for hour in hours:
					if hours.index(hour) % 2 == 0:
						item['store_hours'] += hour + ":"
					else:
						item['store_hours'] += hour + ";"
				try:
					lat_lng = self.validate(store.xpath('//iframe[contains(@src, "https://www.google.com/maps/")]/@src')).split("2d")[-1]
					item['latitude'] = lat_lng.split('!')[1][2:]
					item['longitude'] = lat_lng.split('!')[0]
				except:
					lat_lng = self.validate(store.xpath('//iframe[contains(@src, "http://maps.google.com/maps?")]/@src')).split("ll=")[-1].split('&')[0]
					item['latitude'] = lat_lng.split(',')[0]
					item['longitude'] = lat_lng.split(',')[1]
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
			except:
				pass
		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""
		def replaceUnknownLetter(self, source):
			try:
				formatted_value = source.encode('utf8').replace('\xc3', '').replace('\xa9', 'e').replace('\xa8', 'e').replace('\xb4', 'o').replace('\xb3', 'o').replace('\xb9', 'u').replace('\xba', 'u').replace('\x89', 'E').replace('\xaa', 'e').replace('\x89', 'E').replace('\xa2', 'a').replace('\xac', 'i').replace('\xad', 'i').replace('\xae', 'i')
				return formatted_value
			except:
				return source

