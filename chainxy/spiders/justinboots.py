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

class JustinbootsSpider(scrapy.Spider):
		translator = Translator()
		name = "justinboots"
		uid_list = []
		count = 0
		headers = {
		    "Accept":"application/json, text/javascript, */*; q=0.01",
		    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
		    "X-Requested-With":"XMLHttpRequest"
		}

		def __init__(self):
			place_file = open('cities_us.json', 'rb')
			self.place_reader = json.load(place_file)

		def start_requests(self):
			for info in self.place_reader:
				url = "http://www.justinboots.com/ajax/get-retailers"
				form_data = {
				    "form_id":"retailers",
				    "address":info['city']
				}
				yield FormRequest(url=url, formdata=form_data, headers=self.headers, callback=self.parse_city)

		def parse_city(self, response):		    	
			if 'locations' in json.loads(response.body):
				stores = json.loads(response.body)['locations']
				if isinstance(stores, (int, float)) == False:
					for store in stores:
						item = ChainItem()
						item['store_number'] = ""
						item['store_name'] = store["business"]
						item['address'] = store["address"]
						item['address2'] = ""
						item['city'] = store["city"]
						item['state'] = store["state"]
						item['zip_code'] = store["zip"]
						item['country'] = store["country"]
						item['phone_number'] = store["phone"]
						item['store_hours'] = ""
						item['latitude'] = store["Latitude"]
						item['longitude'] = store["Longitude"]
						#item['store_type'] = info_json["@type"]
						item['other_fields'] = ""
						item['coming_soon'] = 0
						if item['address'] != "" and item['address'] in self.uid_list:
							continue
						if item['phone_number'] != "" and item['phone_number'] in self.uid_list:
							continue
						self.uid_list.append(item['address'])
						self.uid_list.append(item['phone_number'])
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
