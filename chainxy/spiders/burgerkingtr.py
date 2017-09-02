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

class BurgerkingtrSpider(scrapy.Spider):
		translator = Translator()
		name = "burgerkingtr"
		uid_list = []
		start_urls = ['https://www.burgerking.com.tr/Restaurants/GetRestaurants/']
		count = 0
		domain = "https://www.burgerking.com"

		def parse(self, response):
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				item['store_number'] = ""
				item['store_name'] = self.translate(store["data"]["title"])
				item['address'] = self.translate(store["data"]["address"])
				item['address2'] = ""
				item['city'] = self.translate(store["data"]["city"])
				item['state'] = ""
				item['zip_code'] = ""
				item['country'] = "Turkey" 
				item['phone_number'] = ""
				item['store_hours'] = ""
				item['latitude'] = store["lat"]
				item['longitude'] = store["lng"]
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item
		
		def translate(self, src):
			return self.translator.translate(src).text
			
		def validate(self, str):
			if str == None:
				return ""
			return str
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
