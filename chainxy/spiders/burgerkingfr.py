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

class BurgerkingfrSpider(scrapy.Spider):
		name = "burgerkingfr"
		uid_list = []
		start_urls = ['https://api.burgerking.fr/shops']
		count = 0
		domain = "https://www.burgerking.com"

		def parse(self, response):
			translator = Translator()
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				item['store_number'] = ""
				try:
					item['store_name'] = translator.translate(store["name"]).text
					item['address'] = translator.translate(store["address"]).text
					item['address2'] = ""
					item['city'] = translator.translate(store["city"]).text
					item['store_name1'] = translator.translate(store["name"]).text
					item['address1'] = translator.translate(store["address"]).text
					item['address21'] = ""
					item['city1'] = translator.translate(store["city"]).text					
				except:
					pdb.set_trace()
				item['state'] = ""
				item['zip_code'] = store["zipCode"]
				item['country'] = "France"
				item['phone_number'] = store["phone"]
				store_hours_classes = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
				item['store_hours'] = ""
				for hour_class in store_hours_classes:
					xpath = './div[@class="bk-location_' + hour_class + '_dining"]/text()'
					item['store_hours'] += hour_class + ":" + store["schedule"][hour_class]["open"] + "-" + store["schedule"][hour_class]["close"] + ";"
				item['latitude'] = store["position"]["lat"]
				item['longitude'] = store["position"]["lng"]
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
