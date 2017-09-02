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

class ImlovinitatSpider(scrapy.Spider):
		translator = Translator()
		name = "imlovinitat"
		uid_list = []
		start_urls = ['http://www.mcdonalds.at/restaurant-finder']
		count = 0

		def parse(self, response):
			stores = response.xpath('//div[@class="item-list"]/ul/li')
			for store in stores:
				url = "http://www.mcdonalds.at" + store.xpath('./a/@href').extract_first()
				yield scrapy.Request(url=url, callback=self.parse_store)				

		def parse_store(self, response):
			item = ChainItem()
			item['store_number'] = ""
			item['store_name'] = ""
			item['address'] = self.translator.translate(self.validate(response.xpath('//div[@class="street"]/text()').extract_first())).text
			item['address2'] = ""
			item['city'] = self.translator.translate(self.validate(response.xpath('//div[@class="postal-code-city"]/text()').extract_first()).split(' ')[-1]).text
			item['state'] = ""
			item['zip_code'] = self.validate(response.xpath('//div[@class="postal-code-city"]/text()').extract_first()).split(' ')[0]
			item['country'] = "Austria"
			item['phone_number'] = self.validate(response.xpath('//div[@class="field--phone inline"]/text()').extract_first())
			hours = response.xpath('//div[contains(@class,"opening-hours-container")]')[0].xpath('./ul/li')
			item['store_hours'] = ""			
			for hour in hours:
				item['store_hours'] += self.translator.translate(hour.xpath('./span/text()').extract_first()).text + ":" + self.translator.translate(hour.xpath('./text()').extract_first()).text + ";"
			item['latitude'] = response.body.split('latitude":"')[-1].split('",')[0]
			item['longitude'] = response.body.split('longitude":"')[-1].split('",')[0]
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
