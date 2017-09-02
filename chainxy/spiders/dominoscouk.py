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

class dominoscoukSpider(scrapy.Spider):
		translator = Translator()
		name = "dominoscouk"
		uid_list = []
		start_urls = ['https://www.dominos.co.uk/store/ourstores#1']
		count = 0

		def parse(self, response):
			stores = response.xpath('//a[@class="btn-spaced-min"]')
			for store in stores:
				url = "https://www.dominos.co.uk" + store.xpath('./@href').extract_first()
				yield scrapy.Request(url=url, callback=self.parse_store)				

		def parse_store(self, response):
			item = ChainItem()
			item['store_number'] = ""
			if self.validate(response.xpath('//div[@class="store-address-container"]/h5/text()').extract_first()) == '':
				return
			item['store_name'] = self.validate(response.xpath('//div[@class="store-address-container"]/h5/text()').extract_first())
			item['address'] = self.validate(response.xpath('//div[@class="store-address-container"]/div[@class="store-address"]/div[1]/text()').extract_first()) + " " + self.validate(response.xpath('//div[@class="store-address-container"]/div[@class="store-address"]/div[2]/text()').extract_first())
			item['address2'] = ""
			item['city'] = self.validate(response.xpath('//div[@class="store-address-container"]/div[@class="store-address"]/div[3]/text()').extract_first())
			item['state'] = ""
			item['zip_code'] = self.validate(response.xpath('//div[@class="store-address-container"]/div[@class="store-address"]/div[4]/text()').extract_first())
			item['country'] = "United Kingdom"
			item['phone_number'] =  self.validate(response.xpath('//div[@class="store-address-container"]/div[@class="store-address"]/div[contains(@class, "store-telephone")]/text()').extract_first())
			days = response.xpath('//li[@class="opening-day-flow-root"]')[1:]
			item['store_hours'] = ""
			for day in days:
				item['store_hours'] += self.validate(day.xpath('./span[@class="opening-day-float-left"]/text()').extract_first()) + self.validate(day.xpath('./span[@class="opening-day-float-right"]/text()').extract_first()) + ";"
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
