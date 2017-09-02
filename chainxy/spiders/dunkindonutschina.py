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
from googletrans import Translator

class DunkindonutschinaSpider(scrapy.Spider):
		translator = Translator()
		name = "dunkindonutschina"
		uid_list = []
		start_urls = ['http://www.dunkindonutschina.com/store.php']
		count = 0

		def parse(self, response):
			regions = response.xpath('//div[@class="navlist"]/a')
			for region in regions:
				if regions.index(region) != 0:
					url = "http://www.dunkindonutschina.com/" + region.xpath('./@href').extract_first()
					yield scrapy.Request(url=url, callback=self.parse_store)				

		def parse_store(self, response):
				stores = response.xpath('//div[@id="center_right"]/div[@class="store_entry"]')
				for store in stores:
					item = ChainItem()
					item['store_number'] = ""
					item['store_name'] = self.translator.translate(self.validate(store.xpath(".//a[@class='hei18']/text()").extract_first())).text
					item['address'] = self.translator.translate(self.validate(store.xpath(".//a[3]/text()").extract_first())).text
					item['address2'] = ""
					item['city'] = ""
					item['state'] = ""
					item['zip_code'] = ""
					item['country'] = "China"
					item['phone_number'] = self.translator.translate(self.validate(store.xpath(".//a[5]/text()").extract_first())).text
					item['store_hours'] = self.translator.translate(self.validate(store.xpath(".//a[7]/text()").extract_first())).text
					item['latitude'] = ""
					item['longitude'] = ""
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = 0
					yield item
					
		def validate(self, str):
			if str == None:
				return ""
			return str.strip()
		def getZipCode(self, src):
			temps = src.replace(',',' ').replace('\r\n',' ').split(' ')
			while len(temps) != 0:
				temp = temps.pop()
				try:
					zipcode = int(temp)
					break
				except:
					continue
			return str(zipcode)
